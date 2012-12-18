from scrapy.exceptions import IgnoreRequest

class DownloaderMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = spider.settings['PROXIES']['http']
        if request.url[-3:] in ["apk", "png", "jpg", "exe"]:
            print "Ignore request!"
            raise IgnoreRequest

