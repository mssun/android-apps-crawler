from scrapy.exceptions import IgnoreRequest

class DownloaderMiddleware(object):
    def process_request(self, request, spider):
        if request.url[-3:] in ["apk", "png"]:
            print "Ignore request!"
            raise IgnoreRequest
