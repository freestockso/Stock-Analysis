#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,logging
import Date
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from data.Data import Data

class Stock(object):
    def __init__(self,conf={}):
        self.conf=conf
        self.code=None
        self.date=None
        self.data=Data(self.conf) #store and cache data

    def __iter__(self):
        """
        support iter function for stock. 

            >>> stock.data.adv={'20110804':{'601919':{'close':'11.11'},'601920':{'close':'22.22'}}}
            >>> stock.date = None
            >>> check = True
            >>> for date in stock:
            ...    print date
            20110804
            >>> for code , price in stock['20110804']:
            ...     print code ,price
            601919 11.11
            601920 22.22

        """
        if self.date: # if set date ,then return data in date, else return all dates in stock
            data=self.data.get(name="adv",conf={"date":self.date,"code":"all"})
            if data:
                result=map(lambda code:(code , data.get(code,{})))
                if result:
                    return iter(result)
            return iter([])
        else:
            return iter(self.data.adv.keys())

    def __getitem__(self,value):
        """
        通过[],setDate 取值将会改变stock的基准值，而通过方法 index()则不会

            >>> stock.data.adv={'20110805':{'601919':{'close':'10.0'},'601920':{'close':'22.22'}}}
            >>> stock['601919']['20110805'].close
            '10.0'

        """
        if len(value)==6:
            self.code = value
        if len(value)==8:
            self.date = value
        return self

    def __getattr__(self,value):
        """
        define some simple way to access data in stock.

            >>> len(stock.allCode)>1000 #and len(stock.allCode) == len(stock.info)
            True
            >>> len(stock.info) > 100
            True
            >>> stock.data.adv={'20110804':{'601919':{'close':'11.11','volume':'111','high':'12','low':'10',"sequence": [ 7.34]},'601920':{'close':'22.22'}}}
            >>> stock['601919']['20110804'].close
            '11.11'
            >>> stock.volume
            '111'
            >>> stock.high
            '12'
            >>> stock.low
            '10'
            >>> stock['20110804']['601919'].sequence
            [7.34]
        """
        result = self.data.get(name = value,conf={"date":self.date,"code":self.code})
        if result == None:
            return 0
        else:
            return result

    def __len__(self):
        """
        get code length in stock data.
            
            >>> len(stock) > 1000
            True

        """
        return len(self.allCode)

    def index(self,index):
        self.date=Date.getDate(index , self.date)
        return self

    def ma(self,dateRange):
        """
        求指定日期内平均股价
        """
        return self.data.get(name = "ma",conf={"date":self.date,"code":self.code,"dateRange":dateRange}) or 0

    def max(self,dateRange):
        return self.data.get(name = "max",conf={"date":self.date,"code":self.code,"dateRange":dateRange}) or 0

    def min(self,dateRange):
        return self.data.get(name = "min",conf={"date":self.date,"code":self.code,"dateRange":dateRange}) or 0

if __name__ == '__main__':
    import doctest
    __dir__ = os.path.realpath(os.path.dirname(__file__))
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    stock=Stock(conf)
    doctest.testmod()
