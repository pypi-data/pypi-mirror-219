import logging
from datetime import datetime, timedelta
from typing import Union

from scrapy import Request
from scrapy.crawler import Crawler
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.job import job_dir

from crawler_utils.elasticsearch.dupefilter_strategies import DupeFilterStrategyLoader, ElasticDupeFilterStrategy
from crawler_utils.elasticsearch.request_fingerprint import default_request_fingerprint
from crawler_utils.elasticsearch.storage import ElasticSearchStorage, ElasticSearchStorageLoader
from crawler_utils.talisman_job_env import TalismanJobEnvironment

CURRENT_VERSION = 'current'
DEFAULT_INTERVAL = timedelta(days=30)

logger = logging.getLogger(__name__)


class ElasticRFPDupeFilter(RFPDupeFilter):
    """ Request fingerprint duplicates filter based on Elasticsearch storage.

    Requires ElasticRequestsDownloaderMiddleware to be enabled to index requests.
    Additionally, for some dupefilter strategies one needs to enable them as middlewares - either explicitly
    or with crawler_utils.elasticsearch.dupefilter_strategies.DupeFilterStrategyMiddlewareHook

    Settings:

    DUPEFILTER_ELASTICSEARCH_ENABLED
    Enables this dupefilter. If False, falls back to RFPDupeFilter. Default: True.

    ELASTICSEARCH_REQUESTS_SETTINGS
    ES settings as dict. See ElasticSearchStorage for example.

    ELASTICSEARCH_REQUESTS_INDEX
    ES index as string. Default: scrapy-job-requests.

    DUPEFILTER_STRATEGY
    Strategy to filter requests
    - 'noop' (default) - ignores ES and relies on local filter
    - 'depth' - basic strategy which queries ES for all requests with at least given depth
    - 'news' - suggested strategy for news sites, equivalent to depth with min_request_depth=2
    - 'delta_fetch_items' - suggested strategy for sitemaps, filters requests which produced items in previous crawls
    - 'drop_unproductive_requests' - experimental strategy which works like delta fetch, but additionally tries to
    filter unproductive requests - such that no requests following them produce items
    - subclass of crawler_utils.elasticsearch.dupefilter_strategies.ElasticDupeFilterStrategy as dotted path

    DUPEFILTER_MIN_REQUEST_DEPTH
    For depth-based strategies, bypass search in ES for all requests with lesser depth.
    Default: 0 - search in ES for all requests.

    DUPEFILTER_INTERVAL
    Time interval to search for duplicates in ES, in seconds. Default: last 30 days.

    DUPEFILTER_STARTING_FROM_VERSION
    Search in requests issued by this version of crawler or higher. Accepts version number or 'current' (default).

    DUPEFILTER_WITHIN_PERIODIC
    If True, search only in current periodic job requests. Has no effect outside periodic. Default: False.

    """

    def __init__(self,
                 es_storage: ElasticSearchStorage,
                 index: str,
                 dupefilter_strategy: ElasticDupeFilterStrategy,
                 interval: timedelta = DEFAULT_INTERVAL,
                 job_env: TalismanJobEnvironment = None,
                 starting_from_version: Union[int, str] = CURRENT_VERSION,
                 within_periodic: bool = False,
                 path: str = None,
                 debug: bool = False):
        super().__init__(path, debug)
        self.storage = es_storage
        self.index = index
        self.dupefilter_strategy = dupefilter_strategy
        self.interval = interval
        self.job_env = job_env or TalismanJobEnvironment()
        self.starting_from_version = starting_from_version
        self.within_periodic = within_periodic

        dupefilter_strategy.dupefilter = self

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        settings = crawler.settings

        # load strategy first, so it will work as extension even if dupefilter becomes disabled
        dupefilter_strategy = DupeFilterStrategyLoader.from_crawler(crawler)

        if not settings.getbool('DUPEFILTER_ELASTICSEARCH_ENABLED', True):
            return RFPDupeFilter.from_settings(settings)

        es_storage = ElasticSearchStorageLoader.from_crawler(crawler, 'ELASTICSEARCH_REQUESTS_SETTINGS')
        index = crawler.settings.get('ELASTICSEARCH_REQUESTS_INDEX', 'scrapy-job-requests')

        if not es_storage.index_exists(index):
            logger.warning(f'ES index "{index}" does not exist. Falling back to RFPDupeFilter')
            return RFPDupeFilter.from_settings(settings)

        if 'DUPEFILTER_INTERVAL' in settings:
            interval = timedelta(seconds=settings.getint('DUPEFILTER_INTERVAL'))
        else:
            interval = DEFAULT_INTERVAL

        job_env = TalismanJobEnvironment.from_settings(settings)
        starting_from_version = settings.get('DUPEFILTER_STARTING_FROM_VERSION', CURRENT_VERSION)
        within_periodic = settings.getbool('DUPEFILTER_WITHIN_PERIODIC', False)
        debug = settings.getbool('DUPEFILTER_DEBUG')

        return cls(es_storage=es_storage,
                   index=index,
                   dupefilter_strategy=dupefilter_strategy,
                   interval=interval,
                   job_env=job_env,
                   starting_from_version=starting_from_version,
                   within_periodic=within_periodic,
                   path=job_dir(settings),
                   debug=debug)

    def close(self, reason):
        super().close(reason)
        self.storage.close()

    def search_constraints(self):
        constraints = []

        if self.interval > timedelta():
            constraints.append({
                'range': {
                    '@timestamp': {  # maybe we should use last_seen instead?
                        'gte': (datetime.now() - self.interval).isoformat()
                    }
                }
            })

        if self.job_env.crawler_id:
            constraints.append({
                'match': {
                    'crawler_id': self.job_env.crawler_id
                }
            })

        if self.starting_from_version == CURRENT_VERSION:
            if self.job_env.version_id:
                constraints.append({
                    'match': {
                        'version_id': self.job_env.version_id
                    }
                })
        elif self.starting_from_version:
            constraints.append({
                'range': {
                    'version_id': {
                        'gte': int(self.starting_from_version)
                    }
                }
            })

        if self.within_periodic and self.job_env.periodic_job_id:
            constraints.append({
                'match': {
                    'periodic_job_id': self.job_env.periodic_job_id
                }
            })

        return constraints

    def request_in_base(self, request):
        queries = [{
            'match': {
                'fingerprint': self.request_fingerprint(request)
            }
        }]

        queries.extend(self.search_constraints())

        custom_query = self.dupefilter_strategy.query(request)
        if custom_query:
            queries.append(custom_query)

        return self.storage.exists_by_query(f'{self.index},{self.index}-*',
                                            query={'bool': {'must': queries}})

    def request_seen(self, request: Request):
        if super().request_seen(request):
            return True
        if not request.meta.get('depth'):
            return False
        seen = self.dupefilter_strategy.before_query_filter(request)
        if seen is not None:
            return seen
        if self.request_in_base(request):
            request.meta['dupefilter/found_in_base'] = True
            return True
        return False

    def request_fingerprint(self, request):
        return default_request_fingerprint(request)

    def log(self, request, spider):
        super().log(request, spider)
        if request.meta.get('dupefilter/found_in_base'):
            spider.crawler.stats.inc_value('dupefilter/found_in_base', spider=spider)
