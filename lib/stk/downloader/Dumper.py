#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging,os,json

DATA_TYPE="detail"

def dump(data,path,indent=0):
    dirname=os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    fp=open(path,"w")
    if indent:
        json.dump(data,fp,indent=indent)
    else:
        json.dump(data,fp)

def getPath(code,date = None,dataType = DATA_TYPE,conf = {}):
    """
    >>> getPath(date = "20111011",code = "600119",dataType = "detail",conf = conf)
    '/Volumes/ipod/Stock/data/detail/20111011/600119.json'

    >>> getPath(date = "20111011",code = "600119",dataType = "instant" , conf = conf)
    '/Users/xyz/Codes/stock/lib/stk/downloader/../../../data/instant/600119.json'
    """
    if dataType=="instant":
        dataDir = os.path.join(conf.get("SYS_HOME"),conf.get("INSTANT_MIN_DATA_PATH"))
    elif dataType=="detail":
        dataDir = os.path.join(conf.get("SYS_HOME"),conf.get("DETAIL_DATA_PATH"),date)
    path=os.path.join(dataDir,code+".json")
    return path

if __name__ == '__main__':
    import doctest,sys
    __dir__ = os.path.realpath(os.path.dirname(__file__))
    LIB_HOME=os.path.join(__dir__,"..")
    SYS_HOME=os.path.join(LIB_HOME,"..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    conf['SYS_HOME'] = SYS_HOME
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    doctest.testmod()
