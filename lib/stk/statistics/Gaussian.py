#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
正态分布（normal distribution）又名高斯分布（Gaussian distribution）
若随机变量X服从一个数学期望(expectation)为μ、标准方差为σ2的高斯分布，其概率密度函数为正态分布的期望值μ决定了其位置，其标准差(standard deviation)σ决定了分布的幅度。
标准正态分布是μ = 0,σ = 1的正态分布。
计算公式：
 
 f(x) = (1/((2*Pi*σ^2)^(1/2))) * e^(-(x-μ)^2/2*σ^2)

"""
import os,sys,logging
from scipy.stats import norm

from Statistics import Statistics

__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from element import Stock,Date
from  scipy import special
Pi = 3.1415
E = 2.71828

class Gaussian(Statistics):
    def __init__(self,conf = {}):
        self.conf = conf
    
    def value(self,subject, stock , expection = None,variance = None):
        """
        计算公式见头部 
        variance 为 方差
        >> gaussian.value(subject = 0.1,stock = stock)
        """
        if not expection :
            expection = self.expection(stock = stock)
        if not variance:
            variance = self.variance(stock = stock)
        
        Y = (1/((2*Pi*(variance))**0.5)) * (E **(-((subject - expection)**2)/(2*variance)))
        return Y

    def cumulative(self,subject,expection = None,deviation = None,stock = None,date = None):
        """
        求积分
        两个值之间的概率为 gaussian(x1) - gaussian(x2)
        公式 :
        0.5 * [1+ erf( (x-expectation) /deviation * 2 **0.5)] 
        >>> gaussian.cumulative(subject = 0,deviation = 1 ,expection = 0,stock=stock)
        0.5
        
        >>> gaussian.cumulative(subject = [-0.02,-0.01],stock = stock,date ='20111024') 
        """
        
        if expection == None:
            expection = self.expection(stock = stock,date = date)
        if deviation == None:
            deviation = self.deviation(stock = stock,date = date)

        if type(subject) == list and len(subject) == 2:
            pass
        elif type(subject) in [int,float]:
            subject = [subject]
        else:
            raise ValueError

        preValue = None
        
        for item in subject:
            if deviation == 0:
                m = item
            else:
                m = (item - expection)/(deviation *(2 **0.5))
            
            #res = 0.5 * (1 + norm.cdf(m))
            res = 0.5 * (1 + special.erf(m))
            if preValue !=None :
                ret = res - preValue 
            else:
                preValue = res
                ret = res
        return ret

if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(LIB_HOME,"..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Log,Conf
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml")
        )
    conf["SYS_HOME"] = SYS_HOME
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath)

    gaussian = Gaussian()
    stock = Stock(conf)
    stock.date = '20111024'
    doctest.testmod()
