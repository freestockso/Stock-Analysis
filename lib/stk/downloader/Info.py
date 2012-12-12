#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抓取股市的股票代码和对应股票名称。可以每月抓一次。"""
import os,sys,logging
import Dumper,Fetcher,Parser

SOURCE_NAME = "cninfo"
CODE_LIST_FILE_NAME = "codes.json"

class Info:
    def __init__(self,conf={}):
        self.source=conf.get("INFO_SOURCE",[])
        Fetcher.DEBUG=conf.get("DEBUG",False)
        self.conf=conf

    def download(self):
        """
        >>> info=Info(conf)
        >>> info.download()
        """
        source = self.conf.get("SOURCE_NAME",None) or SOURCE_NAME
        parser = Parser.ParserFactory(source)
        res=[]
        for name in self.source:
            url=self.source.get(name)
            rawData = Fetcher.fetch(url)
            parseData = parser.parse(rawData)
            if parseData:
                res=res+parseData
        path = os.path.join(self.conf["INFO_DATA_PATH"],"info.json")
        logging.debug("download info list:" + str(res))
        Dumper.dump(parseData,path) #获得信息列表
        codes=list(set(                       #并对代码去重 \
            map(lambda item:item['code'],res) #获得代码列表 \
            ))
        codes.sort()                         #排序
        path = os.path.join(self.conf["INFO_DATA_PATH"],self.conf.get("CODE_LIST_FILE_NAME",CODE_LIST_FILE_NAME))
        logging.debug("download code list:"+str(codes))
        Dumper.dump(codes,path)

if __name__ == '__main__':
    import doctest
    __dir__ = os.path.realpath(os.path.dirname(__file__))
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    import lib.util.Conf as Conf
    import lib.util.Log as Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["INFO_DATA_PATH"]=os.path.join(SYS_HOME,conf.get("INFO_DATA_PATH",""))
    conf["DEBUG"]=True
    doctest.testmod()
