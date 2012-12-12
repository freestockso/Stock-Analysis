#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
指定下载数名称，日期等，进行下载
"""
from Detail import Detail
from Info import Info
from Instant import Instant

class Downloader:
    def __init__(self,conf={}):
        self.module={
            "detail":Detail,
            "info":Info,
            "instant":Instant
        }
        self.conf=conf

    def download(self,name,conf={}):
        """
            >>> downloader.download("detail")

            >>> downloader.download("instant")

            >> downloader.download("info")
            >> downloader.download("adv")
        """
        self.conf.update(conf)
        if name in self.module.keys():
            downloader=self.module[name](self.conf)
            result =  downloader.download()
        return result

if __name__ == '__main__':
    import doctest,sys,os,logging
    __dir__ = os.path.realpath(os.path.dirname(__file__))
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
    downloader=Downloader(conf)
    doctest.testmod()
