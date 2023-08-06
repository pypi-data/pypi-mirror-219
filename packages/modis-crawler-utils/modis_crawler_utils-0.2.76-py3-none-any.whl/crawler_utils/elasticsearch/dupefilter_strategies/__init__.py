import logging
from abc import ABC
from typing import Optional

from scrapy import Request
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import create_instance, load_object

logger = logging.getLogger(__name__)


class ElasticDupeFilterStrategy(ABC):
    dupefilter = None

    def before_query_filter(self, request: Request) -> Optional[bool]:
        """
        Filter request before making ES query.
        Returns True if duplicate, False if not, None to query in ES.
        """
        return None

    def query(self, request: Request) -> Optional[dict]:
        """
        Returns ES query to search for request.
        It will be joined with other queries with bool:must.
        """
        return None


class NoOpStrategy(ElasticDupeFilterStrategy):
    def before_query_filter(self, request: Request) -> Optional[bool]:
        return False


BASE_DUPEFILTER_STRATEGIES = {
    'noop': f'{__name__}.NoOpStrategy',
    'depth': f'{__name__}.depth_based.DepthBasedStrategy',
    'news': f'{__name__}.depth_based.DefaultNewsStrategy',
    'delta_fetch_items': f'{__name__}.delta_fetch_items.DeltaFetchItemsStrategy',
    'drop_unproductive_requests': f'{__name__}.drop_unproductive_requests.DropUnproductiveRequestsStrategy',
}


class DupeFilterStrategyLoader:
    """
    Loads strategy from DUPEFILTER_STRATEGY setting and ensures single instance of it.
    Setting supports path to strategy class or known alias (see BASE_DUPEFILTER_STRATEGIES).
    Loads NoOpStrategy by default.
    """

    instance = None
    error = None

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        if cls.instance is not None:
            return cls.instance
        if cls.error:
            raise cls.error
        try:
            cls.instance = cls._from_crawler(crawler)
            logger.info(f'Initialized dupefilter strategy {type(cls.instance).__name__}')
            return cls.instance
        except Exception as error:
            cls.error = error
            raise cls.error

    @classmethod
    def _from_crawler(cls, crawler: Crawler):
        settings = crawler.settings
        strategy_name = settings.get('DUPEFILTER_STRATEGY', 'noop')
        strategy_cls_path = BASE_DUPEFILTER_STRATEGIES.get(strategy_name, strategy_name)
        strategy_cls = load_object(strategy_cls_path)
        return create_instance(strategy_cls, crawler=crawler, settings=settings)


class DupeFilterStrategyMiddlewareHook:
    """
    Allows to insert dupefilter strategy in middleware lists without explicitly specifying its type.
    For example, setting
    SPIDER_MIDDLEWARES = {
      'crawler_utils.elasticsearch.dupefilter_strategies.DupeFilterStrategyMiddlewareHook': 1,
      ...
    }
    will load strategy designated by DUPEFILTER_STRATEGY setting and insert it as first spider middleware.

    Installing such hook in stand/project level settings allows to specify df strategy per spider/job.
    """

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        try:
            return DupeFilterStrategyLoader.from_crawler(crawler)
        except Exception:
            raise NotConfigured()
