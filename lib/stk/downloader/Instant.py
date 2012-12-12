#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,logging,time,shutil
import Parser,Fetcher,Dumper,MultiThreadDownloader

__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)

INSTANT_SOURCE_NAME = "qq_min"

INSTANT_SOURCE = {
    #http://q.jrjimg.cn/?q=cn|s&i=,002397,002356,300071,600509,300002,600520,600521&n=hq_lately&c=m&_=175601
    #"instant_jrj":"http://q.jrjimg.cn/?q=cn|s&i=%s&n=hq_lately&c=m&_=175601",
    #http://qt.gtimg.cn/r=0.5596817895772614q=sh000003,sz399001,r_hkHSI,usDJI,usIXIC,gzFCHI,gzGDAXI,gzN225,gzFTSTI,gzTWII,fqUS_GC_1,fqUS_CL_1,s_sh600520,s_sh601166,s_sh601169,s_sh600016,s_sh601328,s_sh600015,s_sh601009,s_sz002142,s_sh601998,marketStat,stdunixtime,s_pksh600000,bkqt021170,bkqt023400,bkqt033100,s_sz000752,s_sh601899,s_sz000100,s_sh600031,s_sz000002,s_sh601666,s_sh601318,s_sh600585,s_sh601901,s_sh601857,s_sz000157,s_sh600470,s_sh601002
    #"instant_qq2":"http://qt.gtimg.cn/r=%sq=%s",
    #http://data.gtimg.cn/flashdata/hushen/minute/sh600000.js?0.9015545738040455
    "qq_min" : "http://data.gtimg.cn/flashdata/hushen/minute/%s.js?%s",
}

class Instant(MultiThreadDownloader.MultiThreadDownloader):
    def __init__(self,conf={}):
        MultiThreadDownloader.MultiThreadDownloader.__init__(self,conf = conf)
        self.source=self.conf.get("INSTANT_SOURCE",INSTANT_SOURCE)
        self.use_source = self.conf.get("INSTANT_SOURCE_NAME",INSTANT_SOURCE_NAME)
        Fetcher.DEBUG=self.conf.get("DEBUG",False)
        self.codes = self.dataHandler.get("allCode")
        self.parser = Parser.ParserFactory(self.use_source)
        
        dataDir = os.path.join(conf.get("SYS_HOME"),conf.get("INSTANT_MIN_DATA_PATH"))
        if os.path.exists(dataDir):
            shutil.rmtree(dataDir)
        os.mkdir(dataDir)
        
    def getUrl(self,code):
        stime = time.time()
        source = self.source.get(self.use_source)
        if(int(code)<600000):
            pre="sz"
        else:
            pre="sh"
        url = source % (pre+code,stime)
        return url

    def handle(self,code,date):
        url=self.getUrl(code)
        rawData = Fetcher.fetch(url)
        parseData = self.parser.parse(rawData)
        path = Dumper.getPath(code = code , date = date ,dataType = "instant" ,conf = self.conf)
        Dumper.dump(data = parseData , path = path)
        return True

if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    doctest.testmod()
