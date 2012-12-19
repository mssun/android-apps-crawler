from datetime import datetime
import os
import hashlib
import time
import urllib2
import sys
import sqlite3
from multiprocessing import Process, Lock
from threading import Thread
import Queue

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
        self.start_time = time.time()

    def open(self, url):
        self.url = url
        proxy_handler = urllib2.ProxyHandler(self.proxies)
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [
            ('User-Agent',r"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"),
            ('Referer', url)
        ]
        urllib2.install_opener(opener)
        try:
            self.opening = urllib2.urlopen(self.url)
        except urllib2.HTTPError:
            print "HTTPError" 
            return False
        meta = self.opening.info()
        #print meta
        self.file_size = int(meta.getheaders("Content-Length")[0])
        last_modified_str = meta.getheaders("Last-Modified")[0]
        self.last_modified = datetime.strptime(last_modified_str,
                '%a, %d %b %Y %H:%M:%S %Z')
        #print "Last modified: %s" % self.last_modified
        return True

    
    def download(self):
        timestamp = time.time() * 1000000
        self.file_name = "%d.apk" % timestamp
        if not os.path.exists(self.repo):
            os.makedirs(self.repo)
            os.makedirs(self.repo + os.sep +"tmp") 
        tmp_file_path = self.repo + os.sep + "tmp" + os.sep + self.file_name
        f = open(tmp_file_path, 'wb')
        #print "Downloading: %s Bytes: %s" % (self.file_name, self.file_size)
        self.file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = self.opening.read(block_sz)
            if not buffer:
                break

            self.file_size_dl += len(buffer)
            f.write(buffer)
            self.print_status()
            #end_time = time.time()
            #cost_time = end_time - start_time
            #if cost_time == 0:
            #    cost_time = 1
            #rate =  file_size_dl * 100. / 1024 / 1024 / cost_time
            #progress =  file_size_dl * 100. / self.file_size
            #
            #status = "\r%10d  [%3.2f%%]  %3dk/s" % (file_size_dl,
            #        progress,
            #        rate)
            #print status,
            #sys.stdout.flush()
        f.close()

        f = open(tmp_file_path, 'r')
        m = hashlib.md5()
        m.update(f.read())
        md5_value = m.hexdigest()
        f.close()
        new_file_name = md5_value + ".apk"
        new_path = self.repo + os.sep + new_file_name
        if os.path.isfile(new_path):
            os.remove(tmp_file_path)
        else:
            os.rename(tmp_file_path, new_path)
        print "Finish! Store as: %s" % new_file_name
    def print_status(self):
        file_name, file_size, progress, rate = self.get_status()
        print "\r%10d [%3.2f%%] %3dk/s" % (file_size, progress, rate),
        sys.stdout.flush()

    def get_status(self):
        end_time = time.time()
        cost_time = end_time - self.start_time
        if cost_time == 0:
            cost_time = 1
        rate =  self.file_size_dl   / 1024 / cost_time
        progress =  self.file_size_dl * 100. / self.file_size
        status = [self.file_name, self.file_size, progress, rate]
        return status

def get_undownloaded_url(sqlite_file, limit=1000):
    conn = sqlite3.connect(sqlite_file)
    urls = []
    c = conn.cursor()
    c.execute('select * from apps where downloaded = 0 limit %d' % limit)
    rec = c.fetchall()
    for r in rec:
        urls.append(r[1])
    conn.close()
    return urls
    

def down_sqlite(argv):
    repo = argv[1]
    sqlite_file = argv[2]
    urls = get_undownloaded_url(sqlite_file)
    queue = Queue.Queue()
    for url in urls:
        queue.put(url)
    for i in range(2):
        t = DownloadThread(queue, repo, sqlite_file)
        t.daemon = True
        t.start()
    #while True:
    #    time.sleep(5)
    #    if (queue.qsize() < 5):
    #        pass
    queue.join()
    #while True:
    #    c = conn.cursor()
    #    c.execute('select * from apps where downloaded = 0 limit 1')
    #    rec = c.fetchone()
    #    url = unicode.encode(rec[1], 'gbk')
    #    downloader = Downloader(repo=repo, proxies={"http":"http://proxy.cse.cuhk.edu.hk:8000"})
    #    if downloader.open(url) is not True:
    #        c.execute('update apps set downloaded = -1 where url = ?', (url,))
    #        conn.commit()
    #        continue
    #    downloader.download()
    #    c.execute('update apps set downloaded = 1 where url = ?', (url,))
    #    conn.commit()
    #    #time.sleep(5)
    #conn.close()

class DownloadThread(Thread):
    def __init__(self, queue, repo, sqlite_file, proxies={"http":"http://proxy.cse.cuhk.edu.hk:8000"}):
        Thread.__init__(self)
        self.repo = repo
        self.proxies = proxies
        self.sqlite_file = sqlite_file
        self.queue = queue
        #self.status_queue = status_queue
    def run(self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()
        while True:
            url = self.queue.get()
            downloader = Downloader(repo=self.repo, proxies=self.proxies)
            if downloader.open(url) is not True:
                c.execute('update apps set downloaded = -1 where url = ?', (url,))
                conn.commit()
            downloader.download()
            c.execute('update apps set downloaded = 1 where url = ?', (url,))
            conn.commit()
            self.queue.task_done()

def test(argv):
    #if len(argv) <= 1:
    #    print "error"
    #else:
    #    url = argv[3]
    #    repo =argv[2]
    #    downloader = Downloader(repo=repo, proxies={"http":"http://proxy.cse.cuhk.edu.hk:8000"})
    #    downloader.open(url)
    #    downloader.download()
    urls = []
    conn = sqlite3.connect(argv[2])
    c = conn.cursor()
    c.execute('select * from apps where downloaded = 0 limit 15')
    rec = c.fetchall()
    for r in rec:
        urls.append(r[1])
    queue = Queue.Queue()
    
    for i in range(3):
        t = DownloadProcess(queue)
        t.start()
        for url in urls:
            queue.put(url)
    queue.join()

if __name__ == "__main__":
    if sys.argv[1] == "-t":
        test(sys.argv)
    else:
        down_sqlite(sys.argv)
