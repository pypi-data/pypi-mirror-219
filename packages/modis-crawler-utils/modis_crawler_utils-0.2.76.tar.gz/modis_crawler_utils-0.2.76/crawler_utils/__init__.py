# flake8: noqa: F401
from crawler_utils.mongodb import MongoConnection
from crawler_utils.mongodb import MongoDBStorage
from crawler_utils.mongodb import MongoDBPipeline

from crawler_utils.files import FilesPipeline

from crawler_utils.images import ImagesPipeline
from crawler_utils.images import VkImagesPipeline
from crawler_utils.images import ImgPushImagesPipeline

from crawler_utils.kafka import KafkaPipeline

from crawler_utils.logstash import LogstashLoggerExtension
from crawler_utils.logstash import LogstashDumpStatsExtension
from crawler_utils.elasticsearch import ElasticRFPDupeFilter
from crawler_utils.elasticsearch import ElasticRequestsDownloaderMiddleware
from crawler_utils.elasticsearch import ElasticItemsPipeline
from crawler_utils.talisman_spider_state import TalismanSpiderState
from crawler_utils.uuid import UUIDPipeline
from crawler_utils.trust_level import TrustLevelPipeline

from crawler_utils.proxypy import ProxyPyDownloaderMiddleware
from crawler_utils.talisman_proxy import TalismanProxyChainDownloaderMiddleware
