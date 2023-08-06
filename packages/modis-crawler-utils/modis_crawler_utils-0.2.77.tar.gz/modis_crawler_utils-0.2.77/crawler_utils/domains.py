from urllib.parse import urlsplit

from itemadapter import ItemAdapter


def get_domain(url, from_level=2):
    netloc = urlsplit(url).netloc
    if not (isinstance(from_level, int) and from_level > 0):
        return netloc
    return '.'.join(netloc.rsplit('.', maxsplit=from_level)[-from_level:])


class ItemDomainsCollectorPipeline:

    def __init__(self, crawler):
        self.domains = set()
        crawler.stats.set_value('item_domains', self.domains)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        if url := ItemAdapter(item).get('_url'):
            self.domains.add(get_domain(url))
        return item
