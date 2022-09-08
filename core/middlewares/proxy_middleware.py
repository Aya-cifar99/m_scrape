import random
from w3lib.http import basic_auth_header
from core.constants.global_constants import PROXY_USERNAME, PROXY_PASSWORD


class CustomProxyMiddleware(object):
    # TODO: Add proxy servers
    proxies = [
        'http://pr.oxylabs.io:7777'
    ]

    def __init__(self, *args, **kwargs):
        self.proxy = self._get_random_proxy()

    def process_request(self, request, spider):
        request.meta['proxy'] = self._get_random_proxy()
        request.headers["Proxy-Authorization"] = basic_auth_header(PROXY_USERNAME, PROXY_PASSWORD)
    def _get_random_proxy(self):
        proxy = random.choice(self.proxies)
        return proxy
