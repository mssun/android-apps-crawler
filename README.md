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
./crawl.sh <market name>
```
* Start downloader:
```
./downloader.py <database file path> <output directory>
```

Supported Third-party Markets (market names used in crawl.sh)
-----------------------------
* AppChina: http://www.appchina.com (appchina.com)
* Hiapk: http://apk.hiapk.com (hiapk.com)
* Anzhi: http://www.anzhi.com (anzhi.com)
* android.d.cn: http://android.d.cn (android.d.cn)
* mumayi: http://www.mumayi.com (mumayi.com)
* gfan: http://apk.gfan.com (gfan.com)
* nduoa: http://www.nduoa.com (nduoa.com)
* 3gyu: http://www.3gyu.com (3gyu.com)
* angeeks: http://apk.angeeks.com (angeeks.com)
* appfun: http://www.appfun.cn (appfun.cn)
* jimi168: http://www.jimi168.com (jimi168.com)
* Keep adding...

More Android Markets
--------------------
See: https://github.com/mssun/android-markets-list
