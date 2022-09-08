import logging


class BaseCrawler(object):

    def __init__(self, *args, **kwargs):
        logging.info('~~Setting up the scraper~~')