from scrapy.exceptions import IgnoreRequest

class DownloaderMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = "http://proxy.cse.cuhk.edu.hk:8000"
        if request.url[-3:] in ["apk", "png"]:
            print "Ignore request!"
            raise IgnoreRequest

