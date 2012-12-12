#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,SYS_HOME)
from lib.stk import Downloader,Date
from lib.stk.data.Check import Check 
MIN_DATA_NUM=15

def run(conf={}):
    """
    @param {Dict} conf
    @param conf.date 抓取日期
    @param {'min'|'detail'|'info'} [conf.download] 数据更新内容.day为日线数据，detail为详细数据,info为股票代码,对应的公司名等数据
    @param {'detail'|'all'|'day'} [conf.mode] 当数据抓取模式为'day'时,'day'数据抓取模式。detail为从detail数据中抓取数据。all为抓取所有数据。day为更新每日数据
    @param {'single'|'mutil'} [conf.thread] 当数据抓取模式为'detail'时,采取的线程模式。single为单线程,mutil为多线程
    """
    logging.info("Start spider.")
    downloader=Downloader(conf)
    check = Check(conf)
    date = conf.get("date",Date.getDate())
    checkIndex = 0
    while checkIndex < conf.get("MIN_DATA_NUM",MIN_DATA_NUM):
        checkDate=Date.getDate(0-checkIndex,date)
        checkReport = check.check(checkDate)
        if not checkReport:
            logging.info("Download %s 's data." % checkDate)
            downloader.download(name="detail",conf={"date":checkDate})
        checkIndex += 1
    logging.info("Download finish.")
    return True
