import logging
import urllib.parse as urlparse
from urllib.parse import parse_qs
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from .proxy_middleware import CustomProxyMiddleware
import time


class TooManyRequestsRetryMiddleware(RetryMiddleware):

    def __init__(self, crawler):
        super(TooManyRequestsRetryMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        params = request.meta.get('params', {})
        if request.meta.get('dont_retry', False):
            return response
        elif response.status == 407:
            message = f"unable to complete request , {request} \n" \
                      f"Authentication required."
            logging.error(message)
        elif response.status in self.retry_http_codes:
            self.crawler.engine.pause()
            message = f'Too many requests are hitting the server:- response_code: {response.status} ' \
                          f'\n Request: {request}' \
                          f'\n Route Name: {params.get("origin_code")}_{params.get("destination_code")}' \
                          f'\n Travel Date: {params.get("travel_date")}' \
                          f'\n Return Date: {params.get("return_date")}' \
                          f'\n ERROR: {response.text}'
            logging.error(message)
            time.sleep(5)
            self.crawler.engine.unpause()
            reason = response_status_message(response.status)
            retry_request = self._retry(request, reason, spider)
            if not retry_request:
                message = f'Gave up retrying for request : {request}' \
                          f'\n Travel Date: {params.get("travel_date")}' \
                          f'\n Return Date: {params.get("return_date")}' \
                          f'\n Route : {params.get("origin_code")}_{params.get("destination_code")}' \
                          f'\n Failed {request.meta.get("retry_times", 0)} times.'
                logging.error(message)
            return retry_request or response
        return response
