#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,SYS_HOME)
#from app.compute.Compute import Compute
from lib.stk import Date, Stock
from lib.stk.data.Extract import Extract

def run(conf={}):
    logging.info("Start compute app.")
    logging.debug("Compute init conf is %s" % str(conf))
    date=conf.get('date',Date.getDate())
    stock=conf.get("stock",Stock(conf))
    extract = Extract(conf = conf)
    extract.extract(project = "fromDetailToAdv", stock = stock, date = date)
    stock.data.dump()
    return True
    #app = Compute(conf)
    #return app.run()
