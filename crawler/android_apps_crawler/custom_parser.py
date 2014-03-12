import re

from scrapy.selector import Selector
from android_apps_crawler.items import AppItem

def parse_anzhi(response):
    xpath = "//div[@class='detail_down']/a/@onclick"
    appItemList = []
    sel = Selector(response)
    for script in sel.xpath(xpath).extract():
        id = re.search(r"\d+", script).group()
        url = "http://www.anzhi.com/dl_app.php?s=%s&n=5" % (id,)
        appItem = AppItem()
        appItem['url'] = url
        appItemList.append(appItem)
    return appItemList

