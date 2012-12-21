Android Apps Crawler
====================

Overview
--------
Android Apps Crawler is an extensible crawler for downloading Android applications in the third-party markets.
It can crawl the download url addresses of applications and automatically download applications
into repository.

Requirements
------------
* Python 2.6 or up
* Scrapy 0.16 or up: http://scrapy.org
* Works on Linux, Windows, Mac OSX, BSD

Usage
-----
* Set the third-party markets you want to crawl in settings.py
* Set the proxy if you have
* Start crawler: 
```
scrapy crawl android_apps_spider
```
* Start downloader:
```
python downloader.py repository_name apps_database_name
```

Supported Third-party Markets
-----------------------------
* AppChina: http://www.appchina.com
* Hiapk: http://apk.hiapk.com
* Anzhi: http://www.anzhi.com
* android.d.cn: http://android.d.cn
* mumayi: http://www.mumayi.com
* gfan: http://apk.gfan.com
* nduoa: http://www.nduoa.com
* 3gyu: http://www.3gyu.com
* Keep adding...

More Android Markets
--------------------
See: https://github.com/mssun/android-markets-list
