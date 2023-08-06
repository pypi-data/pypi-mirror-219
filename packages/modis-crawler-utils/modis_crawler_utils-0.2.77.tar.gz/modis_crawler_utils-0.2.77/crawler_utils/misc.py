from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import load_object, create_instance


def create_instance_from_settings(crawler, settings, setting_key, aliases, defaults):
    def load(cls_or_path):
        cls = load_object(cls_or_path)
        return create_instance(cls, settings=settings, crawler=crawler)

    if obj_name := settings.get(setting_key):
        obj_type = aliases.get(obj_name, obj_name)
        return load(obj_type)
    for obj_type in defaults:
        try:
            return load(obj_type)
        except NotConfigured:
            pass
