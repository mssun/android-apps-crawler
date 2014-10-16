from scrapy.exceptions import IgnoreRequest

class DownloaderMiddleware(object):
    def process_request(self, request, spider):
        if (spider.settings['PROXIES']):
            request.meta["proxy"] = spider.settings['PROXIES']['http']
        if request.url[-3:].lower() in ["apk", "png", "jpg", "exe", "doc",
                "zip", "rar"]:
            print "Ignore request!"
            raise IgnoreRequest

