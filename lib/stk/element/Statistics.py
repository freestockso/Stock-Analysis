#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计符合设定目标的策略数据，如突破均线后是否在5天内上涨5%,用以训练 Bayesian 推断需要的数据。

输出结果:
{
    "strategic1": {
        "statistics1": 0.5456382620410913, 
        "statistics2": 0.16773324351633545, 
    }, 
    ...
    "all":{
        "statistics1": 0.5456382620410913, 
        "statistics2": 0.16773324351633545, 
    }
}
"""
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from data import Reader,Dumper
from Expression import Expression
from Strategic import Strategic
import Date
from Stock import Stock
STATISTICS_DATA_PATH = "data/statistics/"
MIN_DATA_NUM = 15

class Statistics(object):
    def __init__(self,date = None ,conf={}):
        self.date = date or conf.get("date",Date.getDate())
        self.data = conf.get("data",{})
        self.cacheTotalStatistics = True #对统计所有日期是否使用之前统计数据
        self.stock = conf.get("stock",Stock(conf))
        self.conf = conf

    def getDataPath(self,date = None,dataType = "result"):
        if dataType == "result":
            date = date or self.date
            return os.path.join(self.conf.get("SYS_HOME",""),self.conf.get("STATISTICS_DATA_PATH",STATISTICS_DATA_PATH),date+conf.get("DATA_SUFFIX",".json"))
        elif dataType == "cache":
            return os.path.join(self.conf.get("SYS_HOME",""),self.conf.get("STATISTICS_DATA_PATH",STATISTICS_DATA_PATH),"statistics_cache"+conf.get("DATA_SUFFIX",".json"))

    def check(self):
        """
        检测指定日期的statistics数据是否已存在
        """
        dataPath = self.getDataPath(date = self.date)
        return os.path.exists(dataPath)

    def get(self,name):
        """
        获取整体或某策略的统计结果
        """
        if not self.data:
            self.load()
        return self.data.get(name)

    def load(self):
        """
        载入相关statistics数据
        """ 
        dataPath = self.getDataPath(date = self.date)
        self.data = Reader.read(dataPath)
        if not self.data:
                raise IOError
        return self.data  
    
    def collect(self,strategic = None ,statisticsProjectPath = None):
        """
        对于整体数据，缓存之前计算。对于指定策略，暂时只收集15日内数据，反映短期内变动情况。
        收集统计数据
        >> statistics.stock == testCase['stock']
        >> statistics.collect()
        
        收集指定策略统计数据
        >> statistics.stock == testCase['stock']
        >> statistics.collect(strategic = testCase['collectStrategic']) 

        @param {list} strategic  符合策略的code list
        """
        conf={}
        conf.update(self.conf)
        isCache = False
        data={}
        if strategic: #计算指定策略统计
            allCode = strategic #符合指定策略的 code 可通过strategic[date][strategicName]读出
            allDate = []
            for i in range(0,conf.get("MIN_DATA_NUM",MIN_DATA_NUM)):
                date=Date.getDate(0-i,conf.get('date',Date.getDate()))
                allDate.append(date)
        else:    #计算整体统计
            isCache = True
            allDate = self.stock.allDate
            allCode = self.stock.allCode

        if isCache: #读取之前统计缓存
            data = Reader.read(path = self.getDataPath(dataType = "cache"))
            for date in allDate:
                if date in data and date in allDate:
                    allDate.remove(date)
            
        conf.update({
            "date":self.date,
            "stock":self.stock,
            "allCode":allCode
        })

        expression=Expression(conf)
        statisticsProjectPath = statisticsProjectPath or os.path.join(conf.get("SYS_HOME"),conf.get("STATISTICS_PROJECT_PATH"))
        expressions = expression.load(path = statisticsProjectPath)
        for date in allDate:
            result={} #初始化result变量，让result能在公式里直接使用,并且result[name]也能使用
            for code in allCode:
                result[code]={}
            expression.execute(expression= conf.get("expressions",expressions), context = {"result":result,"date":date})
            if not result:
                break;
            data[date]=result
        if isCache:
            Dumper.dump(path = self.getDataPath(dataType = "cache"),data =data)
        return data

    def handle(self,data):
        """
        计算概率
        Prior Probability 先验概率 P(A)，即根据训练材料得出的假设概率。如统计最近15天里上涨5%的股票的概率。
        1-prior P(A')的概率。
        >> statistics.handle(data = testCase['statisticsCount'])
        """
        count = {}
        total = 0
        for date in data:
            for code in data[date]:
                for statisticsName in data[date][code]:
                    if not statisticsName in count:
                        count[statisticsName] = 0
                    if data[date][code][statisticsName] == True:
                        count[statisticsName] += 1
                total +=1
        probability = {}
        for statisticsName in count:
            subCount = count[statisticsName] or 0
            probability[statisticsName] = float(subCount) / total
        return probability

    def compute(self):
        """
        计算整体和指定策略的统计数据
        >> statistics.stock = testCase['stock']
        >>> statistics.compute()
        """
        result = {}
        #result['total'] = self.handle(data = self.collect())   # 统计所有日期数据
        strategic = self.conf.get("strategic",Strategic(conf = self.conf))   # 统计指定策略数据
        for strategicName in strategic:
            result[strategicName]= self.handle(self.collect(strategic = strategic[strategicName])) 
        return result

    def dump(self):
        """
        保存所有日期的统计结果，不保存各策略短期结果。
        """
        dataPath = self.getDataPath()
        Dumper.dump(path = dataPath , data =self.data)

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
    statistics = Statistics(date = '20110902',conf = conf)
    from tests.element.statistics import case as testCase,result as testResult
    doctest.testmod()
