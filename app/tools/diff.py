#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
探寻各种条件对准确率的影响
实验对照组：当前accurency

实验组:
    - 1. all days
    - 2. all days + 马
    - 3. 正
    - 4. 正 + 马
"""
"""
init 
"""
import os,sys,logging
from lib.stk.element import Stock,Date,Dumper
from lib.util import Log,Conf
__dir__ = os.path.realpath(os.path.dirname(__file__))
APP_HOME=os.path.join(__dir__,"..")
SYS_HOME=os.path.join(APP_HOME,"..")
SYS_LIB_HOME=os.path.join(SYS_HOME,"lib")
sys.path.insert(0,SYS_HOME)
conf=Conf.load(os.path.join(SYS_HOME,"conf","stock.yaml"),os.path.join(SYS_HOME,"conf","downloader.yaml"))
conf["SYS_HOME"] = SYS_HOME
logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
Log.set(logPath = logPath,printLevel = logging.ERROR)
stock = Stock(conf)
###################### TRAIN
"""
训练 整体 statistics 和 strategic likelihood
用 element/statistics来载入这些数据
"""
TRAIN_DATA_PATH = os.path.join(SYS_HOME,"data","train")

#train all days data and gaussian data
from lib.stk.statistics.Gaussian import Gaussian
subject = [[-0.1,-0.09],[-0.09,-0.08],[-0.08,-0.07],[-0.07,-0.06],[-0.06,-0.05],[-0.05,-0.04],[-0.04,-0.03],[-0.03,-0.02],[-0.02,-0.01],[-0.01,0],[0,0.01],[0.01,0.02],[0.02,0.03],[0.03,0.04],[0.04,0.05],[0.05,0.06],[0.06,0.07],[0.07,0.08],[0.08,0.09],[0.09,0.1]]


# strategic likelihood
from lib.stk.element.Strategic import Strategic
STRATEGIC_PATH = ""
strategic = Strategic(conf)
##################### PREDICT
"""
strategic match and markov p to reduct posterior

"""
FIND_PATH = os.path.join("data","find")

#bayes
from lib.stk.inference.Bayes import Bayes
bayes = Bayes(conf)

for i in range(0,conf['MIN_DATA_NUM']):
    date = Date.getDate(0-i)
    gaussian = Gaussian(conf = conf)
    gaussian_stat = {}
    stat = {}   
    dates = []
    stock.date = date
    #
    for date in stock.allDate:
        dates.append(date)
    for item in subject:
        gaussian_stat[str(item)] = gaussian_stat.get(str(item),0) + gaussian.cumulative(subject = item,stock = stock,date = dates)
        stat[str(item)] = stat.get(str(item),0) + gaussian.statistics(subject = item,stock = stock , date = dates)
    # statistics
    stat = gaussian.sort(stat)
    logging.info("dump statistics data")
    Dumper.dump(path = os.path.join(TRAIN_DATA_PATH,"statistics.json"),data = stat)
    # Gaussian 
    gaussian_stat = gaussian.sort(gaussian_stat)
    logging.info("dump gaussian data")
    Dumper.dump(path = os.path.join(TRAIN_DATA_PATH,"gaussian.json"),data = gaussian_stat)
    #all days
    conf['date'] = date
    prior = 0
    posterior = bayes.posteriors(pripor = stat) 

    #all days + markov
    markov_posterior = bayes.posteriors(pripor = stat,markov = True)

    #gaus
    gaussion_posterior = bayes.posteriors(pripor = gaussian_stat) 

    #gaus + markov
    gaussion_markov_posterior = bayes.posteriors(pripor = gaussian_stat) 

"""
report
"""
#################### ACCURENCY
"""
get accurency
"""
from lib.stk.statistics import Accuracy





