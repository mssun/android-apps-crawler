#!/usr/bin/env python
from urllib import urlopen

import time
import os
import sqlite3
import sys
from getopt import getopt
import socket

class Downloader:
    def getURLName(self, url):
        directory=os.curdir
        timestamp = time.time() * 1000000
        name="%s%srepository%s%d.apk" % (
            directory,
            os.sep,
            os.sep,
            timestamp
        )

        return name

    def createDownload(self, url, proxy=None):
        socket.setdefaulttimeout(600)
        instream=urlopen(url, None, proxy)
        
            
        filename=instream.info().getheader("Content-Length")
        if filename==None:
            filename="temp"

        return (instream, filename)


    def download(self, urls):
        proxies={}
        proxies={"http": "http://proxy.cse.cuhk.edu.hk:8000"}
        for url in urls:
            try:
                print url
                outfile=open(self.getURLName(url), "wb")
                #fileName=outfile.name.split(os.sep)[-1]
                fileName=outfile.name.split("=")[-1]
                url, length=self.createDownload(url, proxies)
                if not length:
                    length="?"

                print "Downloading %s (%s bytes) ..." % (url.url, length)
                if length!="?":
                    length=float(length)
                bytesRead=0.0
                
                print "%-15s %5.fkb " % (
                            fileName,
                            length/1024.0
                        ),
                flag = -1
                for line in url:
                    bytesRead += len(line)
                    if length != "?":
                        if flag != int(30 * bytesRead / length):
                            flag = int(30 * bytesRead / length)
                            sys.stdout.write("#")
                    
                    outfile.write(line)
                '''
                for line in url:
                    bytesRead+=len(line)
                    if length!="?":
                        print "%s: %.02f/%.02f kb (%d%%)" % (
                            fileName,
                            bytesRead/1024.0,
                            length/1024.0,
                            100*bytesRead/length
                        )

                    outfile.write(line)
                '''
                url.close()
                outfile.close()
                print " Done"
                return True
            #except IOError:
            #    print "timeout"
            #    return False
                #self.timeoutProcess(id)
            except Exception, e:
                print "Error downloading %s: %s" % (url, e)

    def timeoutProcess(self, id):
        print id
        conn = sqlite3.connect('apps_database.db')
        c = conn.cursor()
        rec = c.execute('update apps set downloaded=-1 where id=?', (id, ))
        #conn.commit()
        #conn.close()

def main():
    while True:
        conn = sqlite3.connect('apps_database.db')
        c = conn.cursor()
        rec = c.execute('select * from apps where downloaded = 0')
        url = c.fetchone()
        print url[0]
        downloader = Downloader()
        if downloader.download([unicode.encode(url[1], 'gbk')]):
            c.execute('update apps set downloaded=1 where id=?', (url[0],))
        else:
            c.execute('update apps set downloaded=-1 where id=?', (url[0], ))
        conn.commit()
        conn.close()
    
if __name__=="__main__":
    main()
