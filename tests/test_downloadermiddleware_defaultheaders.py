from unittest import TestCase
import six

from scrapy.contrib.downloadermiddleware.defaultheaders import DefaultHeadersMiddleware
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.utils.test import get_crawler


class TestDefaultHeadersMiddleware(TestCase):

    def get_defaults_spider_mw(self):
        crawler = get_crawler(Spider)
        spider = crawler._create_spider('foo')
        defaults = dict([(k, [v]) for k, v in \
            six.iteritems(crawler.settings.get('DEFAULT_REQUEST_HEADERS'))])
        return defaults, spider, DefaultHeadersMiddleware.from_crawler(crawler)

    def test_process_request(self):
        defaults, spider, mw = self.get_defaults_spider_mw()
        req = Request('http://www.scrapytest.org')
        mw.process_request(req, spider)
        self.assertEquals(req.headers, defaults)

    def test_update_headers(self):
        defaults, spider, mw = self.get_defaults_spider_mw()
        headers = {'Accept-Language': ['es'], 'Test-Header': ['test']}
        req = Request('http://www.scrapytest.org', headers=headers)
        self.assertEquals(req.headers, headers)

        mw.process_request(req, spider)
        defaults.update(headers)
        self.assertEquals(req.headers, defaults)
