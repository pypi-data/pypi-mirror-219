import json
import os
import types
from datetime import datetime, timezone

from itemadapter import ItemAdapter

from crawler_utils.elasticsearch.storage import ElasticSearchStorage
from crawler_utils.timestamp import ensure_seconds
from crawler_utils.talisman_job_env import TalismanJobEnvironment


class ElasticItemsPipeline(object):

    def __init__(self, es_storage, index, job_id):
        self.es_storage = es_storage
        self.index = index
        self.job_id = job_id

    @classmethod
    def from_crawler(cls, crawler):
        es_settings = crawler.settings.getdict('ELASTICSEARCH_ITEMS_SETTINGS')
        es_storage = ElasticSearchStorage.from_settings(es_settings)
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        mid = cls(
            es_storage,
            index=crawler.settings.get('ELASTICSEARCH_ITEMS_INDEX', 'scrapy-job-items'),
            job_id=job_env.job_id
        )

        return mid

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            indexed_item = ItemAdapter(item).asdict()
            if self.job_id:
                indexed_item['job_id'] = self.job_id

            timestamp = item.get('_timestamp', None)
            if isinstance(timestamp, str):
                ts = timestamp
            elif isinstance(timestamp, int):
                ts = datetime.fromtimestamp(ensure_seconds(timestamp),
                                            tz=timezone.utc).isoformat()
            else:
                ts = datetime.now().isoformat()

            indexed_item = {
                '@timestamp': ts,
                'job_id': self.job_id if self.job_id else None,
                '_url': item.get('_url', None),
                '_uuid': item.get('_uuid', None),
                '_attachments': item.get('_attachments', None),
                'item': json.dumps(item)
            }

            self.es_storage.index(self.index, indexed_item)
        return item

    def close_spider(self, spider):
        self.es_storage.close()
