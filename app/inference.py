#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通过Bayes公式预测股价变动概率,报告盈利概率高的股票
"""
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
APP_HOME=os.path.join(__dir__,"..")
SYS_HOME=os.path.join(APP_HOME,"..")
SYS_LIB_HOME=os.path.join(SYS_HOME,"lib")
sys.path.insert(0,SYS_HOME)

from lib.stk import Date
from lib.stk.data import Check,Reader,Dumper
from lib.stk.element.Report import Report
from lib.stk.element.Strategic import Strategic
from lib.stk.element.Stock import Stock

BAYES_DATA_PATH = "data/statistics/bayes/"
SUFFIX=".json"

def run(conf = {}):
    """
    传入日期，读入projects和传入日期的statistics.进行计算，得到符合条件的strategic和股票code
    例如一个report的project为“短线股票池”,里面定义了多少天内上涨概率大于多少的公式。如果某策略的统计数据符合该公式，则返回该策略的股票代码及其他相关信息。
    >> reporter.run({"statistics":case['statistics']})
    
    更新 statistics => probability
    注:这里statistics主要指统计得到的bayes值.
    """
    logging.info("Report program start.")
    logging.debug("Report config %s"%str(conf))
    if not "stock" in conf:
        conf['stock'] = Stock(conf)
    if not "date" in conf:
        conf['date']=Date.getDate()

    #load train/statistics data
    if "statistics" in conf:
        statistics = conf.get("statistics") #载入指定日期的监控策略
    else:
        path = os.path.join(conf.get("SYS_HOME"),conf.get("BAYES_DATA_PATH",BAYES_DATA_PATH),conf['date']+SUFFIX)
        statistics = Reader.read(path = path)

    # predict
    logging.info("Start strategic app.Date is %s" %conf['date'])
    strategic = Strategic(conf = conf)
    strategic.check()
    strategic.compute()
    strategic.dump()
    logging.info("Finish strategic compute of date %s "%conf['date'])

    #generate report
    report = Report(conf = conf)
    report.compute(strategic,statistics)
    report.check()
    report.dump()
    return report
