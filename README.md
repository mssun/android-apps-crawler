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
* Scrapy 0.22 or up: http://scrapy.org (didn't have a full test in lower version.)
* Works on Linux, Windows, Mac OSX, BSD
* Currently, downloader cannot work on Windows.
* For Ubuntu users, "Don't use the python-scrapy package provided by Ubuntu, 
they are typically too old and slow to catch up with latest Scrapy. 
Instead, use the official [Ubuntu Packages](http://doc.scrapy.org/en/latest/topics/ubuntu.html#topics-ubuntu)."

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

Settings
--------
You can set proxy, user-agen, database name, etc in ```crawler/android_apps_crawler/settings.py``` file.

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

TODO
----
* Windows support for downloader.
* Crawl apps from shared cloud storage link (e.g, pan.baidu.com, dbank.com).
