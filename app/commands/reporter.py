#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
报告盈利概率高的股票或股票策略
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

BAYES_DATA_PATH = "data/statistics/bayes/"
REPORTER_DATA_PATH = "data/reporter/"
REPORTER_PROJECT_PATH = "app/reporter/projects/"
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

    conf['REPORTER_PROJECT_PATH']=os.path.join(\
        conf.get("SYS_HOME",""),\
        conf.get("REPORTER_PROJECT_PATH",REPORTER_PROJECT_PATH))

    options={}
    options.update(conf)
    options.update(conf)
    conf=options
    date=conf.get('date',Date.getDate())
    check = Check.Check(conf = conf)
    if not check.checkReporterCondition(date = date):
        logging.warning("Reporter is invailable.date:%s" % date)
        return False
    #get statistics
    path = os.path.join(conf.get("SYS_HOME"),\
        conf.get("BAYES_DATA_PATH",BAYES_DATA_PATH),\
        date+SUFFIX)
    statistics = conf.get("statistics" , Reader.read(path = path)) #载入指定日期的监控策略
    if not statistics:
        logging.warning("Reporter not find statistics data.Exit it.")
        return None

    #filter by conditions
    strategic = Strategic(date = date ,conf = conf)
    report = Report(conf = conf)
    report.compute(strategic,statistics)

    #dump result
    if report != False:
        path = os.path.join(conf.get("SYS_HOME",""),\
            conf.get("REPORTER_DATA_PATH",REPORTER_DATA_PATH),date+SUFFIX)
        Dumper.dump(path = path , data = report.data)
        logging.info("Reporter result : %s" % str(report.data))
    else:
        logging.info("Reporter run fail.")
    return report
