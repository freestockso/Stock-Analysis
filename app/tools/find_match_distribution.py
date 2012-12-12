#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,re,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
    
from lib.stk.statistics.Gaussian import Gaussian
from lib.stk.element.Stock import Stock
import lib.stk.data.Dumper as Dumper
from lib.util import Log,Conf
conf=Conf.load(\
        os.path.join(SYS_HOME,"conf","stock.yaml"),
        os.path.join(SYS_HOME,"conf","downloader.yaml")
    )
conf["SYS_HOME"] = SYS_HOME
logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
Log.set(logPath = logPath,printLevel = logging.ERROR)

stock = Stock(conf)
subject = [
        [-0.1,-0.09],
        [-0.09,-0.08],
        [-0.08,-0.07],
        [-0.07,-0.06],
        [-0.06,-0.05],
        [-0.05,-0.04],
        [-0.04,-0.03],
        [-0.03,-0.02],
        [-0.02,-0.01],
        [-0.01,0],
        [0,0.01],
        [0.01,0.02],
        [0.02,0.03],
        [0.03,0.04],
        [0.04,0.05],
        [0.05,0.06],
        [0.06,0.07],
        [0.07,0.08],
        [0.08,0.09],
        [0.09,0.1],
    ]

gaussian = Gaussian(conf = conf)
gaussian_stat = {}
stat = {}
count = 0 
dates = []
for date in stock.allDate:
    dates.append(date)
    count += 1
    if count >30:
        break

for item in subject:
    gaussian_stat[str(item)] = gaussian_stat.get(str(item),0) + gaussian.cumulative(subject = item,stock = stock,date = dates)
    stat[str(item)] = stat.get(str(item),0) + gaussian.statistics(subject = item,stock = stock , date = dates)

################## Gaussian 
gaussian_stat = gaussian.sort(gaussian_stat)
################## statistics
stat = gaussian.sort(stat)

################### output
print "###stat###\n%s\n###stat###" % str(stat)
print "###gaussian###\n%s\n###gaussian###" % str(gaussian_stat)
