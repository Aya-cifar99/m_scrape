import argparse
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawlers.implemented_crawlers import IMPLEMENTED_CRAWLERS

logger = logging.getLogger('crawlers')


class CrawlerExecutor:
    def __init__(self, crawler_name=None, crawler_class=None, config=None, kwargs={}):
        self.config = {'use_proxy': True}
        self.crawler_name = crawler_name
        self.crawler_class = crawler_class
        self.kwargs = kwargs
        super(__class__, self).__init__()

    def scrap(self):
        setting = get_project_settings()
        process = CrawlerProcess(settings=setting)
        process.crawl(self.crawler_class, config=self.config, **self.kwargs)
        process.start()
        logger.info('starting reactor...')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()

    parser.add_argument('--crawler', required=True)
    args = parser.parse_args()
    logging.info('Running %s %s ' % (__file__, args))
    CrawlerExecutor(crawler_name=args.crawler,
                    crawler_class=IMPLEMENTED_CRAWLERS[args.crawler],
                    ).scrap()
