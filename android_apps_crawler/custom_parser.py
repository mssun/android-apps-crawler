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

def parse_anzhi(response):
    xpath = "//div[@id='btn']/a/@onclick"
    appItemList = []
    hxs = HtmlXPathSelector(response)
    for script in hxs.select(xpath).extract():
        id = re.search(r"\d+", script).group()
        url = "http://www.anzhi.com/dl_app.php?s=%s&n=5" % (id,)
        appItem = AppItem()
        appItem['url'] = url
        appItemList.append(appItem)
    return appItemList

