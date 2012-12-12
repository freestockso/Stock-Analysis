#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@note 由于多线程时用原类初始化函数初始化了Detail一遍，因此在调用本模块时参数最好在实例化时传递，而不要实例化后改self.xxx
"""
import sys,os,threading,logging,time
if sys.version > (3,0):
    import queue
else:
    import Queue as queue
import Parser,Fetcher,Dumper
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from util import Util
from element import Date, Stock

THREAD_NUM = 10
THREAD_MODE = "single"
DETAIL_SOURCE_NAME="qq2"
DETAIL_SOURCE={
    "qq" : "http://data.gtimg.cn/flashdata/hushen/minute/%s",
    #http://stock.gtimg.cn/data/index.php?appn=detail&action=download#&c=sz002132&d=20100802
    "qq2" : "http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=%s&d=%s",
    #http://market.finance.sina.com.cn/downxls.php?date=2010-07-23&symbol=sz002249
    "sina" : "http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s"
}

class Detail:
    def __init__(self,conf={}):
        self.conf = conf
        self.stock = Stock(self.conf)
        self.date = conf.get('date',Date.getDate()) #抓取指定日期的detail
        self.sourceName=conf.get('DETAIL_SOURCE_NAME') or DETAIL_SOURCE_NAME
        self.threadMode = conf.get('THREAD_MODE',THREAD_MODE) # Detail的线程模式 single|mutil
        self.threadNum = int(conf.get('THREAD_NUM',THREAD_NUM)) # 采用多线程模式抓取数据时的线程数
        self.parser=Parser.ParserFactory(self.sourceName)
    def download(self,date=None):
        """
        >> detail=Detail(conf)
        >> detail.stock.allCode

        >> detail.download()
        True
        """
        date = date or self.date
        logging.debug("Start downloading Detail data...\nCrawl mode is %s." % self.threadMode)
        if self.conf.get("restart"): #中断后重新开始传数据的restart模式
            lastCode=Util.getLastCode(
                path = os.path.join(self.conf.get("SYS_HOME"),
                self.conf.get("DETAIL_DATA_PATH"),date)
            ) #得到中断前最后一个抓取成功的股票代码
            codes = map(lambda code:int(code) >int (lastCode),self.stock.allCode) #得到剩余的需要抓取的代码
            logging.info("Downloader is in restart mode.Restart begin at " + str(codes[0]))
            self.conf['restart'] = False
        else:
            codes = self.stock.allCode

        if self.threadMode == "multi":  #多线程模式
            oQueue = queue.Queue()
            for code in codes:
                if type(code) == int:
                    code = Util.getCode(code)
                oQueue.put(code)
            for i in range(self.threadNum):
                self.conf["queue"]=oQueue
                oMultiThreadCrawlDetail = MultiThreadDetail(date=date,parser=self.parser,conf=self.conf)
                oMultiThreadCrawlDetail.setDaemon(True)
                oMultiThreadCrawlDetail.start()
            oQueue.join()               
        else: #单线程模式
            for code in codes:
                handleDetail(code = code,date = date,parser = self.parser,conf = self.conf)
        return True

class MultiThreadDetail(threading.Thread):
    def __init__(self,date,parser,conf={}):
        self.conf = conf
        threading.Thread.__init__(self)
        self.parser=parser
        self.date=date
        self.queue=conf.get('queue',None)
    def run(self):
        if self.queue:
            while True:
                code=self.queue.get()
                try:
                    handleDetail(date=self.date ,code = code,parser = self.parser,conf = self.conf)
                    self.queue.task_done()
                except:
                    logging.error("handleDetail error.")
                    self.queue.task_done()
def getUrl(num,date,sourceType="qq2",conf={}):
    """
    >>> getUrl(num="601919",date="20110817",conf = conf)
    'http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sh601919&d=20110817'
    """
    num=int(num)
    date=str(date)
    detailSource=conf.get("DETAIL_SOURCE",DETAIL_SOURCE)
    if sourceType=="qq":
        strNum=Util.getCode(num)
        if(num<600000):
            pre="sz"
        else:
            pre="sh"
        fileName=pre+strNum+".js"
        return detailSource.get("qq") % fileName
    elif sourceType=="sina":
        strNum=Util.getCode(num)
        if(num<600000):
            pre="sz"
        else:
            pre="sh"
        symbol=pre+strNum
        formatDate=time.strftime("%Y-%m-%d",time.strptime(date,"%Y%m%d"))
        url=detailSource.get("sina") % (formatDate,symbol)
        return url
    elif sourceType=="qq2":
        strNum=Util.getCode(num)
        if(num<600000):
            pre="sz"
        else:
            pre="sh"
        symbol=pre+strNum
        formatDate=time.strftime("%Y%m%d",time.strptime(date,"%Y%m%d"))
        url=detailSource.get("qq2") %(symbol, formatDate)
        return url

def handleDetail(code,date,parser , conf):
    url=getUrl(num = code,date = date,conf=conf)
    fetchData=Fetcher.fetch(url)
    parseData=parser.parse(fetchData)
    path = Dumper.getPath(code = code , date = date ,dataType = "detail" ,conf = conf)
    Dumper.dump(path = path,data = parseData)
    return True

if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    Fetcher.DEBUG=True
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    doctest.testmod()
