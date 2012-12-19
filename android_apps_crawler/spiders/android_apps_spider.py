import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from scrapy import log

from urlparse import urlparse
from urlparse import urljoin

from android_apps_crawler.items import AppItem
from android_apps_crawler import settings


class AndroidAppsSpider(BaseSpider):
    name = "android_apps_spider"
    allowed_domains = settings.ALLOWED_DOMAINS
    start_urls = settings.START_URLS

    def parse(self, response):
        response_domain = urlparse(response.url).netloc
        appItemList = []
        cookie = {}
        if "appchina" in response_domain:
            xpath = "//a[@id='pc-download' and @class='free']/@href"
            appItemList.extend(self.parse_xpath(response, xpath))
        elif "hiapk" in response_domain:
            xpath = "//a[@class='linkbtn d1']/@href"
            appItemList.extend(self.parse_xpath(response, xpath))
        elif "android.d.cn" in response_domain:
            xpath = "//a[@class='down']/@href"
            appItemList.extend(self.parse_xpath(response, xpath))
        elif "anzhi" in response_domain:
            xpath = "//div[@id='btn']/a/@onclick"
            appItemList.extend(self.parse_anzhi(response, xpath))
        else:
            pass
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a/@href').extract():
            url = urljoin(response.url, url)
            yield Request(url, meta=cookie, callback=self.parse)

        for item in appItemList:
            yield item


    #def parse_appchina(self, response):
    #    appItemList = []
    #    hxs = HtmlXPathSelector(response)
    #    for url in hxs.select(
    #        "//a[@id='pc-download' and @class='free']/@href"
    #        ).extract():
    #        url = urljoin(response.url, url)
    #        log.msg("Catch an application: %s" % url, level=log.INFO)
    #        appItem = AppItem()
    #        appItem['url'] = url
    #        appItemList.append(appItem)
    #    return appItemList
    
    def parse_xpath(self, response, xpath):
        appItemList = []
        hxs = HtmlXPathSelector(response)
        for url in hxs.select(xpath).extract():
            url = urljoin(response.url, url)
            log.msg("Catch an application: %s" % url, level=log.INFO)
            appItem = AppItem()
            appItem['url'] = url
            appItemList.append(appItem)
        return appItemList
    
    def parse_anzhi(self, response, xpath):
        appItemList = []
        hxs = HtmlXPathSelector(response)
        for script in hxs.select(xpath).extract():
            id = re.search(r"\d+", script).group()
            url = "http://www.anzhi.com/dl_app.php?s=%s&n=5" % (id,)
            appItem = AppItem()
            appItem['url'] = url
            appItemList.append(appItem)
        return appItemList

            
