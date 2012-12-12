#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
strategic module
"""
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,SYS_HOME)
#from app.strategic.Strategic import Strategic
from lib.stk import Stock,Date
from lib.stk.data import Dumper,Check
from lib.stk.statistics import Bayes
from lib.stk.element.Strategic import Strategic

STRATEGIC_DATA_PATH=os.path.join("data","strategic")
SUFFIX=".json"
PROJECT_PATH="app/strategic/projects"
BAYES_DATA_PATH = os.path.join("data","statistics","bayes")

def run(conf={}):
    stock=conf.get("stock",Stock(conf))
    date=conf.get('date',Date.getDate())
    logging.info("Start strategic app.Date is %s" %date)

    check = Check.Check(conf = conf)
    if not check.checkStrategicCondition(date = date):
        logging.warning("Strategic is invailable.date:%s" % date)
        return False

    strategic_conf ={}
    strategic_conf.update(conf)
    strategic_conf['stock']=stock
    strategic = Strategic(conf = strategic_conf)
    strategicResult = strategic.compute()
    path = os.path.join(conf.get("SYS_HOME"),conf.get("STRATEGIC_DATA_PATH",STRATEGIC_DATA_PATH),date+SUFFIX)
    logging.debug("Dump strategic result to %s.\nStrategic result is:\n %s" % (strategic.data,path))
    Dumper.dump(path = path,data = strategicResult)
    logging.info("Finish strategic compute of date %s "%date)


    logging.info("Start Bayes statistics.")
    bayesHandler = Bayes(conf)
    bayes = bayesHandler.posterior()
    if bayes != False:
        Dumper.dump(data = bayes,\
        path = os.path.join(conf.get("SYS_HOME"),conf.get("BAYES_DATA_PATH",BAYES_DATA_PATH),date+SUFFIX))
        logging.info("Bayes statistics run success.")
        logging.debug("Bayes statistics run result %s" % bayes)
        return True
    else:
        logging.info("Bayes statistics run fail.")
        return False

    #return app.run()
