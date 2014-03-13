from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

import sqlite3
from os import path
from android_apps_crawler import settings


class AppPipeline(object):
    def process_item(self, item, spider):
        log.msg("Catch an AppItem", level=log.INFO)
        return item

class SQLitePipeline(object):
    filename = ''
    conn = None
    def __init__(self):
        self.filename += settings.MARKET_NAME
        self.filename += ".db"
        self.filename = path.join(settings.DATABASE_DIR, self.filename)
        print self.filename
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        try:
            self.conn.execute('insert into apps(url) values(?)',
                        (item['url'],)
                    )
            self.conn.commit()
            log.msg("Inserting into database");
        except sqlite3.IntegrityError:
            print "Duplicated"
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.create_table()
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.commit()

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self):
        self.conn = sqlite3.connect(self.filename)
        self.conn.execute("create table apps( \
                id integer primary key autoincrement, \
                url varchar(100) not null unique, \
                downloaded int default 0)"
            )
        self.conn.commit()
