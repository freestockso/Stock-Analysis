#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计数据模块
跟踪每天通过策略筛选出来的股票的上涨概率。如果上涨概率超过80％，则将该策略加入到report报告的策略池里。
"""
import os, sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,SYS_HOME)

from lib.stk import Date
from lib.stk.statistics.Accuracy import Accuracy
from lib.stk.statistics.Profile import Profile
from lib.stk.data import Dumper,Check

ACCURACY_DATA_PATH = os.path.join("data","statistics","accuracy")
PROFILE_DATA_PATH = os.path.join("data","statistics","profile")
SUFFIX=".json"
PROJECT_PATH="app/statistics/projects"

def run(conf = {}):
    """
    调度整个模块。
    """
    date = conf.get('date',Date.getDate())
    logging.info("Statistics module is started.Run date is %s" % date)
    conf["projectPath"] = os.path.join(conf.get("SYS_HOME"),conf.get("STATISTICS_PROJECT_PATH"))
    check = Check.Check(conf = conf)
    if not check.checkStatisticsCondition(date = date):
        logging.warning("Statistics is invailable.date:%s" % date)
        return False

    accuracy=Accuracy(conf)
    accuracyResult = accuracy.compute(date = date)
    if accuracyResult !=False:
        path = os.path.join(conf.get("SYS_HOME",SYS_HOME),conf.get("ACCURACY_DATA_PATH",ACCURACY_DATA_PATH),date+SUFFIX)
        Dumper.dump(data = accuracyResult,path = path)
        logging.info("Accuracy statistics run success.Result is dump to %s" % path )
        logging.debug("Accuracy statistics run result %s" % accuracyResult)
    else:
        logging.info("Accuracy statistics run failed.")

    profile = Profile(conf)
    profileResult = profile.profile()
    if profileResult !=False:
        path = os.path.join(conf.get("SYS_HOME",SYS_HOME),conf.get("PROFILE_PATH",PROFILE_DATA_PATH),date+SUFFIX)
        Dumper.dump(data = profileResult,path = path)
        logging.info("Profile statistics run success.Result is dump to %s"%path)
        logging.debug("Profile statistics run result %s" % profileResult)
        return True
    else:
        logging.info("Profile statistics run failed.")
        return False
