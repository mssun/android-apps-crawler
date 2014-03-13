import re

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from scrapy import log

from urlparse import urlparse
from urlparse import urljoin

from android_apps_crawler.items import AppItem
from android_apps_crawler import settings
from android_apps_crawler import custom_parser


class AndroidAppsSpider(Spider):
    name = "android_apps_spider"
    scrape_rules = settings.SCRAPE_RULES

    def __init__(self, market=None, database_dir="../repo/databases/", *args, **kwargs):
        super(AndroidAppsSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = settings.ALLOWED_DOMAINS[market]
        self.start_urls = settings.START_URLS[market]
        settings.MARKET_NAME = market
        settings.DATABASE_DIR = database_dir

    def parse(self, response):
        response_domain = urlparse(response.url).netloc
        appItemList = []
        cookie = {}
        xpath_rule = self.scrape_rules['xpath']
        for key in xpath_rule.keys():
            if key in response_domain:
                appItemList.extend(
                        self.parse_xpath(response, xpath_rule[key]))
                break
        custom_parser_rule = self.scrape_rules['custom_parser']
        for key in custom_parser_rule.keys():
            if key in response_domain:
                appItemList.extend(
                        getattr(custom_parser, custom_parser_rule[key])(response))
                break
        #if "appchina" in response_domain:
        #    xpath = "//a[@id='pc-download' and @class='free']/@href"
        #    appItemList.extend(self.parse_xpath(response, xpath))
        #elif "hiapk" in response_domain:
        #    xpath = "//a[@class='linkbtn d1']/@href"
        #    appItemList.extend(self.parse_xpath(response, xpath))
        #elif "android.d.cn" in response_domain:
        #    xpath = "//a[@class='down']/@href"
        #    appItemList.extend(self.parse_xpath(response, xpath))
        #elif "anzhi" in response_domain:
        #    xpath = "//div[@id='btn']/a/@onclick"
        #    appItemList.extend(self.parse_anzhi(response, xpath))
        #else:
        #    pass
        sel = Selector(response)
        for url in sel.xpath('//a/@href').extract():
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
        sel = Selector(response)
        for url in sel.xpath(xpath).extract():
            url = urljoin(response.url, url)
            log.msg("Catch an application: %s" % url, level=log.INFO)
            appItem = AppItem()
            appItem['url'] = url
            appItemList.append(appItem)
        return appItemList

    #def parse_anzhi(self, response, xpath):
    #    appItemList = []
    #    hxs = HtmlXPathSelector(response)
    #    for script in hxs.select(xpath).extract():
    #        id = re.search(r"\d+", script).group()
    #        url = "http://www.anzhi.com/dl_app.php?s=%s&n=5" % (id,)
    #        appItem = AppItem()
    #        appItem['url'] = url
    #        appItemList.append(appItem)
    #    return appItemList


