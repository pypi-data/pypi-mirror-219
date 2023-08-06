import dataclasses
import json
import logging
import time
import typing
import urllib.parse as urlparse

import requests
from scrapy.settings import Settings

logger = logging.getLogger(__name__)

DEFAULT_PROXY_URL = 'http://proxy.talisman.ispras.ru:20718'


@dataclasses.dataclass
class TalismanProxyConfig:
    url: str
    login: str
    token: str = dataclasses.field(repr=False)
    use_tor: bool = False
    country: str = None
    ignored_countries: typing.Sequence[str] = ()
    use_fastest: bool = False

    def __post_init__(self):
        if not self.url:
            raise ValueError('Undefined talisman proxy url')
        if not self.login:
            raise ValueError('Undefined talisman proxy login')
        if not self.token:
            raise ValueError('Undefined talisman proxy token')

    @classmethod
    def from_settings(cls, settings: Settings):
        def resolve(key, proxypy_key=None, getter=settings.get):
            full_key = f'TALISMAN_PROXY_{key}'
            if full_key not in settings and proxypy_key:
                return getter(f'PROXYPY_{proxypy_key}')
            return getter(full_key)

        return cls(
            url=resolve('URL') or DEFAULT_PROXY_URL,
            login=resolve('LOGIN', proxypy_key='API_LOGIN'),
            token=resolve('TOKEN', proxypy_key='API_KEY'),
            use_tor=resolve('USE_TOR', proxypy_key='TOR', getter=settings.getbool),
            country=resolve('COUNTRY', proxypy_key='COUNTRY'),
            ignored_countries=resolve('IGNORED_COUNTRIES', proxypy_key='IGNORE_COUNTRY', getter=settings.getlist),
            use_fastest=resolve('USE_FASTEST', proxypy_key='FASTEST', getter=settings.getbool)
        )

    @property
    def full_url(self):
        parsed_url = urlparse.urlparse(self.url)
        settings = {
            "token": self.token,
            "useTor": self.use_tor,
            "country": self.country,
            "ignoredCountries": self.ignored_countries,
            "useFastest": self.use_fastest
        }
        encoded_settings = urlparse.quote(json.dumps(settings, separators=(',', ':')))
        return f'{parsed_url.scheme}://{self.login}:{encoded_settings}@{parsed_url.netloc}'


class TalismanProxyError(Exception):
    def __init__(self, config: TalismanProxyConfig, message: str):
        self.config = config
        super().__init__(message)


class ProxyServerNotAvailable(TalismanProxyError):
    def __init__(self, config: TalismanProxyConfig):
        super().__init__(config, f'Talisman proxy {config.url} is not available')


class ProxyHealthCheckError(TalismanProxyError):
    def __init__(self, config: TalismanProxyConfig, reason: str):
        super().__init__(config, f'Talisman proxy {config.url} check failed: {reason}')


class TalismanProxyChainDownloaderMiddleware:
    def __init__(self,
                 use_proxy: bool,
                 proxy_config: TalismanProxyConfig,
                 health_check_retry_times: int,
                 health_check_retry_interval: int):
        self.use_proxy = use_proxy
        self.proxy_config = proxy_config
        self.health_check_retry_times = health_check_retry_times
        self.health_check_retry_interval = health_check_retry_interval

        if self.use_proxy:
            self.health_check()

    def health_check(self):
        tries = 0
        while True:
            try:
                # It doesn't matter what url we use, because in health-check mode
                # proxy server should ignore it and respond immediately
                health_check = requests.get(url="http://demo-site.at.ispras.ru",
                                            headers={"X-Proxy-Chain-Health-Check": "1"},
                                            timeout=60,
                                            proxies={"http": self.proxy_config.full_url})
                break
            except requests.exceptions.RequestException:
                tries += 1
                logger.info(f"Proxy server connection failed {tries}/{self.health_check_retry_times} times")
                if tries < self.health_check_retry_times:
                    logger.info(f"Sleeping for {self.health_check_retry_interval} seconds")
                    time.sleep(self.health_check_retry_interval)  # intentionally blocks twisted loop
                else:
                    raise ProxyServerNotAvailable(self.proxy_config)
        if not health_check.ok:
            raise ProxyHealthCheckError(self.proxy_config, health_check.text)
        logger.info("Proxy server is available. Authorization is successful")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            use_proxy=settings.getbool('USE_TALISMAN_PROXY') or settings.getbool('USE_PROXY'),
            proxy_config=TalismanProxyConfig.from_settings(settings),
            health_check_retry_times=settings.getint('TALISMAN_PROXY_HEALTH_CHECK_RETRY_TIMES', 15),
            health_check_retry_interval=settings.getint('TALISMAN_PROXY_HEALTH_CHECK_RETRY_INTERVAL', 60)
        )

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            return
        if not request.meta.get('use_proxy', self.use_proxy):
            return
        request_proxy_config = request.meta.get('talisman_proxy_config', self.proxy_config)
        if isinstance(request_proxy_config, dict):
            request_proxy_config = dataclasses.replace(self.proxy_config, **request_proxy_config)
        elif not isinstance(request_proxy_config, TalismanProxyConfig):
            raise TypeError(f'Invalid proxy configuration type {type(request_proxy_config)} for {request}')
        request.meta['proxy'] = request_proxy_config.full_url
