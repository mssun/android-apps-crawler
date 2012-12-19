# Scrapy settings for android_apps_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'android_apps_crawler'

SPIDER_MODULES = ['android_apps_crawler.spiders']
NEWSPIDER_MODULE = 'android_apps_crawler.spiders'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
ITEM_PIPELINES = [
    'android_apps_crawler.pipelines.AppPipeline',
    'android_apps_crawler.pipelines.SQLitePipeline'
]
LOG_LEVEL = 'INFO'
DOWNLOADER_MIDDLEWARES = {
    'android_apps_crawler.middlewares.DownloaderMiddleware': 1,
}
PROXIES = {
    'http' : 'http://proxy.cse.cuhk.edu.hk:8000',
}

ALLOWED_DOMAINS = [
    #"appchina.com",
    #"hiapk.com",
    #"anzhi.com",
    #"android.d.cn",
    "mumayi.com"
]
START_URLS = [
    #"http://www.appchina.com",
    #"http://apk.hiapk.com",
    #"http://www.anzhi.com",
    #"http://android.d.cn",
    "http://www.mumayi.com",
]
SCRAPE_RULES = {
    "xpath" : {
        "appchina" : "//a[@id='pc-download' and @class='free']/@href",
        "hiapk" : "//a[@class='linkbtn d1']/@href",
        "android.d.cn" : "//a[@class='down']/@href",
        "mumayi" : "//a[@class='download fl']/@href",
    },
    "custom_parser" : {
        "anzhi" : "parse_anzhi", 
    },
}
