from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from scrapy import log

from urlparse import urlparse
from urlparse import urljoin

from android_apps_crawler.items import AppItem


class AndroidAppsSpider(BaseSpider):
    name = "android_apps_spider"
    allowed_domains = ["appchina.com"]
    start_urls = [
        "http://www.appchina.com/app/com.hg.rocketislandfree/"
    ]

    def parse(self, response):
        response_domain = urlparse(response.url).netloc
        appItemList = []
        if "appchina" in response_domain:
            appItemList.extend(self.parse_appchina(response))

        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a/@href').extract():
            url = urljoin(response.url, url)
            yield Request(url, callback=self.parse)

        for item in appItemList:
            yield item


    def parse_appchina(self, response):
        appItemList = []
        hxs = HtmlXPathSelector(response)
        for url in hxs.select(
            "//a[@id='pc-download' and @class='free']/@href"
            ).extract():
            log.msg("Catch an application: %s" % url, level=log.INFO)
            appItem = AppItem()
            appItem['url'] = url
            appItemList.append(appItem)
        return appItemList
