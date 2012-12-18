from datetime import datetime
import os
import hashlib
import time
import urllib2
import sys
import sqlite3

class Downloader:
    proxies = {}
    url = ""
    file_name = ""
    file_size = None
    last_modified = None
    opening = None
    repo = None
    

    def __init__(self, repo, proxies={}):
        self.proxies = proxies
        self.repo = repo

    def open(self, url):
        self.url = url
        proxy_handler = urllib2.ProxyHandler(self.proxies)
        opener = urllib2.build_opener(proxy_handler)
        try:
            self.opening = opener.open(self.url)
        except urllib2.HTTPError:
            print "HTTPError" 
        meta = self.opening.info()
        #print meta
        self.file_size = int(meta.getheaders("Content-Length")[0])
        last_modified_str = meta.getheaders("Last-Modified")[0]
        self.last_modified = datetime.strptime(last_modified_str,
                '%a, %d %b %Y %H:%M:%S %Z')
        print "Last modified: %s" % self.last_modified
    
    def download(self):
        timestamp = time.time() * 1000000
        self.file_name = "%d.apk" % timestamp
        f = open(self.repo + self.file_name, 'wb')
        print "Downloading: %s Bytes: %s" % (self.file_name, self.file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = self.opening.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / self.file_size)
            status = status + chr(8)*(len(status) + 1)
            print status,
        f.close()

        f = open(self.repo + self.file_name, 'r')
        m = hashlib.md5()
        m.update(f.read())
        md5_value = m.hexdigest()
        f.close()
        new_file_name = md5_value + ".apk"
        os.rename(self.repo + self.file_name, self.repo + new_file_name)
        print chr(8) + "Finish! Store as: %s" % new_file_name


def down_sqlite(argv):
    repo = argv[1]
    sqlite_file = argv[2]
    conn = sqlite3.connect(sqlite_file)
    while True:
        c = conn.cursor()
        c.execute('select * from apps where downloaded = 0 limit 1')
        rec = c.fetchone()
        url = unicode.encode(rec[1], 'gbk')
        downloader = Downloader(repo=repo, proxies={"http":"http://proxy.cse.cuhk.edu.hk:8000"})
        downloader.open(url)
        downloader.download()
        c.execute('update apps set downloaded = 1 where url = ?', (url,))
        conn.commit()
    conn.close()


def test(argv):
    if len(argv) <= 1:
        print "error"
    else:
        url = argv[3]
        repo =argv[2]
        downloader = Downloader(repo=repo, proxies={"http":"http://proxy.cse.cuhk.edu.hk:8000"})
        downloader.open(url)
        downloader.download()

if __name__ == "__main__":
    if sys.argv[1] == "-t":
        test(sys.argv)
    else:
        down_sqlite(sys.argv)
