import time
from datetime import datetime

from scrapy import signals

from crawler_utils.elasticsearch.request_fingerprint import default_request_fingerprint
from crawler_utils.elasticsearch.storage import ElasticSearchStorage, ElasticSearchStorageLoader
from crawler_utils.talisman_job_env import TalismanJobEnvironment


class ElasticRequestsDownloaderMiddleware:

    def __init__(self,
                 es_storage: ElasticSearchStorage,
                 index: str,
                 job_env: TalismanJobEnvironment = None):
        self.es_storage = es_storage
        self.index = index
        self.job_env = job_env or TalismanJobEnvironment()

    @classmethod
    def from_crawler(cls, crawler):
        es_storage = ElasticSearchStorageLoader.from_crawler(crawler, 'ELASTICSEARCH_REQUESTS_SETTINGS')
        index = crawler.settings.get('ELASTICSEARCH_REQUESTS_INDEX', 'scrapy-job-requests')
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        mid = cls(es_storage, index, job_env)
        crawler.signals.connect(mid.close_spider, signal=signals.spider_closed)
        return mid

    def process_request(self, request, spider):
        request.meta['request_timer/start'] = time.time()

    def process_response(self, request, response, spider):
        item = self._request_item_base(request)
        item['url'] = response.url
        item['http_status'] = response.status
        item['response_size'] = len(response.body)
        self.es_storage.index(self.index, item)
        return response

    def process_exception(self, request, exception, spider):
        if 'request_timer/start' in request.meta:
            item = self._request_item_base(request)
            self.es_storage.index(self.index, item)
        return

    def _request_item_base(self, request):
        timestamp = time.time()
        timestamp_iso = datetime.fromtimestamp(timestamp).isoformat()
        item = {
            'url': request.url,
            'request_url': request.url,
            'method': request.method,
            'fingerprint': self._request_fingerprint(request),
            'duration': int(timestamp - request.meta['request_timer/start']),
            'last_seen': timestamp_iso,
            '@timestamp': timestamp_iso
        }
        if self.job_env.job_id:
            item['job_id'] = self.job_env.job_id
        if self.job_env.crawler_id:
            item['crawler_id'] = self.job_env.crawler_id
        if self.job_env.version_id:
            item['version_id'] = int(self.job_env.version_id)  # int to enable sorting on
        if self.job_env.periodic_job_id:
            item['periodic_job_id'] = self.job_env.periodic_job_id
        return item

    @staticmethod
    def _request_fingerprint(request):
        return default_request_fingerprint(request)

    def close_spider(self, spider):
        self.es_storage.close()
