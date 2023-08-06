# -*- coding: utf-8 -*-
import logging

import certifi
from elasticsearch import Elasticsearch, helpers
from scrapy.crawler import Crawler


class ElasticSearchStorage:

    def __init__(self, es: Elasticsearch, buffer_length: int):
        self.es = es
        self.buffer_length = buffer_length
        self.items_buffer = []

    @classmethod
    def init_es_client(cls, es_settings):
        if 'hosts' not in es_settings:
            es_settings['hosts'] = 'localhost:9200'
        if not isinstance(es_settings['hosts'], list):
            es_settings['hosts'] = [es_settings['hosts']]
        if 'timeout' not in es_settings:
            es_settings['timeout'] = 60
        if 'port' not in es_settings:
            es_settings['port'] = 443
        if 'use_ssl' not in es_settings:
            es_settings['use_ssl'] = True
        if 'verify_certs' not in es_settings:
            es_settings['verify_certs'] = False
            es_settings['ssl_show_warn'] = False
        if ('client_cert' in es_settings or 'client_key' in es_settings) and \
                'ca_certs' not in es_settings:
            es_settings['ca_certs'] = certifi.where()
        return Elasticsearch(**es_settings)

    '''
        Example es_settings:
            {
                'hosts': 'localhost:9200',             # optional
                'timeout': 60,                         # optional
                'http_auth': ('login', 'password'),    # optional
                'port': 443,                           # optional
                'use_ssl': True,                       # optional
                'verify_certs': False,                 # optional
                'ssl_show_warn': False,                # optional
                'ca_certs': 'path_to_ca_certs',        # optional
                'client_key': 'path_to_key',           # optional
                'client_cert': 'path_to_cert',         # optional
                'buffer_length': 500,                  # optional
            }
    '''

    @classmethod
    def from_settings(cls, es_settings):
        es_settings = es_settings.copy()
        buffer_length = es_settings.pop('buffer_length')
        if not buffer_length:
            buffer_length = 500
        es = cls.init_es_client(es_settings)
        return cls(es, buffer_length)

    def index_exists(self, index):
        return self.es.indices.exists(index)

    def index(self, index, item):
        index_action = {
            '_index': index,
            '_source': item
        }
        self.items_buffer.append(index_action)
        if len(self.items_buffer) >= self.buffer_length:
            self.send_items()

    def send_items(self, refresh='false'):
        helpers.bulk(self.es, self.items_buffer, refresh=refresh)
        self.items_buffer = []

    @property
    def has_pending_items(self):
        return bool(self.items_buffer)

    def refresh_index(self, index):
        self.es.indices.refresh(index)

    def update_by_query(self, index, query, script, **kwargs):
        body = {'query': query, 'script': script}
        return self.es.update_by_query(index, body=body, **kwargs)

    def exists_by_query(self, index, query, **kwargs):
        return self.es.count(index=index, body={'query': query}, **kwargs)['count'] > 0

    def close(self):
        if self.has_pending_items:
            self.send_items()


class ElasticSearchStorageLoader:
    instances = {}

    @classmethod
    def from_crawler(cls, crawler: Crawler, es_settings_key: str):
        instance_or_error = cls.instances.get(es_settings_key)
        if instance_or_error is None:
            es_settings = crawler.settings.getdict(es_settings_key)
            try:
                instance_or_error = ElasticSearchStorage.from_settings(es_settings)
                cls.instances[es_settings_key] = instance_or_error
                log_level = crawler.settings.get('ELASTICSEARCH_LOG_LEVEL', logging.ERROR)
                logging.getLogger('elasticsearch').setLevel(log_level)
                return instance_or_error
            except Exception as error:
                cls.instances[es_settings_key] = error
                raise error
        elif isinstance(instance_or_error, ElasticSearchStorage):
            return instance_or_error
        else:
            raise instance_or_error
