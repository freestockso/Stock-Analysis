#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
选股策略
数据结构:
{
    "\u653e2\u500d\u4ee5\u4e0a\u91cf": [
    "000558", 
    "000605", 
    ...],
    ...
}
"""
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from data import Reader,Dumper
import Date
from element.Expression import Expression
SUFFIX = ".json"
STRATEGIC_DATA_PATH = "data/strategic/"

class Strategic(object):
    def __init__(self,date=None,conf={}):
        self.conf = conf
        self.date = date or conf.get("date",Date.getDate())
        self.data = conf.get("data",{})
        self.stock = conf.get("stock",None)

    def __getattr__(self,name):
        """
            >>> strategic.data={"20110902":{"strategic1":['601919','601920']}}
            >>> len(strategic.allCode) > 1
            True
        """
        if name == "allCode":
            return self.getAllCode()
        else:
            None

    def __len__(self):
        return len(self.getAllCode())

    def __getitem__(self,name):
        """
            >> strategic.data={"20110902":{"strategic1":['601919','601920']}}
            >> '601919' in strategic["strategic1"]
            True
        """
        if name:
            if name.isdigit() and 10000000< int(name) <99999999:
                self.date =name
                return self
            else:
                return self.get(name)
        else:
            return None

    def __setitem__(self,name,value):
        if name == 'date' :
            date = int(value)
            if 10000000< date <99999999:
                self.date = date 

    def __iter__(self):
        """
            >> for item in strategic:
            ...     print item
            strategic1
        """
        return iter(self.load(date = self.date) or [])

    def get(self,name = None,date = None):
        if not date :
            date = self.date
        
        data = self.data.get(date,None)
        if not data:
            data = self.load(date = self.date)

        if name:
            return data.get(name,[])
        else:
            return data

    def load(self,date=None):
        if not self.data.get(date,None):
            strategicPath = os.path.join(self.conf.get("SYS_HOME",""),self.conf.get("STRATEGIC_DATA_PATH",STRATEGIC_DATA_PATH),date+SUFFIX)
            strategic = Reader.read(strategicPath)
            if strategic:
                self.data[date] = strategic 
            else:
                logging.warning("Load strategic data failed.Date is %s ,path is %s" % (date,strategicPath))
                self.data[date] = []
                sys.exit(2)
        return self.data.get(date,[])

    def dump(self,data,path = None):
        if not path:
            path = os.path.join(self.conf.get("SYS_HOME"),self.conf.get("STRATEGIC_DATA_PATH",STRATEGIC_DATA_PATH),self.date+SUFFIX)
        Dumper.dump(path = path,data = data)
        return True

    def getAllCode(self):
        """
            >> type(strategic.getAllCode())==list and len(strategic.getAllCode()) >1
            True
        """
        allCode=[]
        strategic = self.get(date = self.date)
        if strategic:
            for strategicName in strategic:
                allCode += strategic[strategicName]
        return list(set(allCode))

    def compute(self,stock = None):
        stock = stock or self.stock
        conf={}
        conf.update(self.conf)
        conf.update({
            "date":self.date,
            "stock":stock,
            "allCode":stock.allCode
        })
        expression=Expression(conf)
        projectPath=os.path.join(conf.get("SYS_HOME"),conf.get("STRATEGIC_PROJECT_PATH"))
        expressions=expression.load(projectPath)
        result={} #初始化result变量，让result能在公式里直接使用,并且result[name]也能使用
        for expr in expressions:
            result[expr.get("name")]=[]
        expression.execute(expression = expressions,context = {"result":result})
        self.data.update({self.date:result})
        return result


if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    #conf["data"]={"20111011":{"test":123}}
    strategic = Strategic(conf = conf)
    #print strategic.data.get("20111011")
    doctest.testmod()
