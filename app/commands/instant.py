#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
在股市交易时间里即时计算
"""

import sys,os,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME = os.path.join(__dir__,"..","..")
sys.path.insert(0,SYS_HOME)
#from app.compute.Compute import Compute
from lib.stk import Date,Downloader,Stock
from lib.stk.data.Extract import Extract
from lib.stk.element.Report import Report
from lib.stk.element.Strategic import Strategic
from lib.stk.statistics import Bayes,Profile
from lib.stk.data import Dumper

def run(conf={}):
    date = Date.getInstantDate() #instant date 应该Date.getDate +1,key的编码问题
    conf['date']=date

    logging.info("start downloading instant data.Date is %s" % conf['date'])
    downloader = Downloader(conf = conf)
    downloader.download("instant")

    logging.info("start computing instant data.Date is %s"% conf['date'])
    stock=Stock(conf)
    extract = Extract(conf = conf)
    extract.extract(project = "instant", stock = stock, date = date)

    logging.info("start instant strategic data.Date is %s" %conf['date'])
    strategic_conf ={}
    strategic_conf.update(conf)
    strategic_conf['stock']=stock
    strategic = Strategic(conf = strategic_conf)
    strategicResult = strategic.compute()
    Dumper.dump(path = os.path.join(conf.get("SYS_HOME"),conf.get("INSTANT_DATA_PATH"),"strategic.json"),data = strategicResult)

    logging.info("Start Bayes statistics.Date is %s"% conf['date'])
    conf['strategic']=strategic
    bayesHandler = Bayes(conf)
    bayes = bayesHandler.posterior()
    Dumper.dump(path = os.path.join(conf.get("SYS_HOME"),conf.get("INSTANT_DATA_PATH"),"bayes.json"),data = bayes)

    logging.info("Start report.Date is %s"% conf['date'])
    report = Report(conf = conf)
    report.compute(strategic = strategic , statistics = bayes)
    print report

    #profile
    profile_conf =  {"stock":stock,"date":date}
    profile_conf.update(conf)
    profile = Profile(profile_conf)
    profile.viewProfile()

    path = os.path.join(conf.get("SYS_HOME"),conf.get("INSTANT_REPORT_DATA_PATH"))
    Dumper.dump(path = path,data = report.data)
    return report.data

if __name__ == '__main__':
    __dir__ = os.path.realpath(os.path.dirname(__file__))
    SYS_HOME=os.path.join(__dir__,"..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    run(conf)
