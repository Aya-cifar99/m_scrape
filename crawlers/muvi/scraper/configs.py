import datetime
import logging
import os
from datetime import date
from logging.handlers import RotatingFileHandler

from core.crawlers.base_crawler import BaseCrawler
from core.integrations.google_sheets import read_input_data
from core.integrations import slack_messages


class MuviConfigs(BaseCrawler):
    # Spider configs
    name = 'muvi'
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 200,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 5,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_FORMAT': 'json',
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408, 429, 307],
        'ITEM_PIPELINES': {
            'crawlers.muvi.scraper.pipelines.JsonWriterPipeline': 800,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'core.middlewares.retry_middleware.TooManyRequestsRetryMiddleware': 543,
            # 'core.middlewares.proxy_middleware.CustomProxyMiddleware': 350,
            # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
        },
        'HTTPPROXY_ENABLED': True
    }

    # Global variables
    today = date.today().strftime("%Y-%m-%d")

    # Configure logging
    log_path = f'../crawlers/muvi/logs/muvi_{datetime.date.today().strftime("%Y-%m-%d")}'
    handlers = [RotatingFileHandler(filename=log_path,
                                    mode='a',
                                    maxBytes=512000,
                                    backupCount=4)
                ]
    logging.basicConfig(handlers=handlers,
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    def read_api_list(self):
        sheet_df = read_input_data()
        api_list = list((sheet_df['api_ids'].iloc[0].split(",")))
        return [int(api_id) for api_id in api_list]

    def parsing_dates(self, date):
        day = date.strftime("%d")
        month = datetime.datetime.strptime(date.strftime("%m"), "%m").strftime("%b")
        year = date.strftime("%Y")
        return day + month + year

    def read_spider_params(self):
        pass
