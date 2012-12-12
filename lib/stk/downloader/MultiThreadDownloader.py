#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@note 由于多线程时用原类初始化函数初始化了Detail一遍，因此在调用本模块时参数最好在实例化时传递，而不要实例化后改self.xxx
"""
import sys,os,threading,logging
if sys.version > (3,0):
    import queue
else:
    import Queue as queue
#import Parser,Fetcher,Dumper
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from util import Util
from data.Data import Data
from element import Date
THREAD_NUM=10

class MultiThreadDownloader:
    def __init__(self,conf={}):
        self.conf = conf
        self.dataHandler = Data(conf)
        self.allCode = self.dataHandler.get("allCode")
        self.date = conf.get('date',Date.getDate()) #抓取指定日期的detail
        self.sourceName=conf.get('SOURCE_NAME')
        self.threadNum = int(conf.get('THREAD_NUM',THREAD_NUM)) # 采用多线程模式抓取数据时的线程数

    def download(self):
        """
        >>> app=MultiThreadDownloader(conf)
        >>> app.stock.allCode

        >>> app.download()
        True
        """
        logging.debug("Start downloading data...\nCrawl mode is mutil.")
        conf = {}
        conf.update(self.conf)
        conf['handle']=self.handle
        conf['date'] = self.date
        oQueue = queue.Queue()
        for code in self.allCode:
            if type(code) == int:
                code = Util.getCode(code)
            oQueue.put(code)
        for i in range(self.threadNum):
            conf["queue"]=oQueue
            multiThreadCrawlHandler = MultiThreadHandler(conf = conf)
            multiThreadCrawlHandler.setDaemon(True)
            multiThreadCrawlHandler.start()
        oQueue.join()               
        return True

    def handle(self,code,date):
        raise NotImplementedError
        #url=self.getUrl(code,date)
        #fetchData=Fetcher.fetch(url)
        #parseData=parser.parse(fetchData)
        #dumper.dump(date,code,parseData)


class MultiThreadHandler(threading.Thread):
    def __init__(self,conf={}):
        threading.Thread.__init__(self)
        self.conf = conf

    def run(self):
        date = self.conf.get("date",Date.getDate())
        queue = self.conf.get('queue')
        handle = self.conf.get('handle')
        if queue:
            while True:
                code=queue.get()
                try:
                    handle(date = date ,code = code)
                    queue.task_done()
                except:
                    logging.error('Error hanpped when download data.')
                    queue.task_done()
