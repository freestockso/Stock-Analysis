#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练Bayes推断需要的数据
输出:
    prior
    likelihood

Bayes 公式:
                                      P(B|A)
        P(A|B) = P(A) * --------------------------------
                         P(B|A) * P(A) + P(B|A') * P(A')

"""
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,LIB_HOME)
from element import Stock, Expression, Date , Strategic
SUFFIX = ".json"
MIN_DATA_NUM = 15
class Train:
    def __init__(self,conf={}):
        self.stock = conf.get("stock",Stock(conf))
        self.expression = conf.get("expression",Expression(conf))
        self.data = conf.get("BAYES_TRAIN_DATA",None)
        self.conf=conf
        self.prior = {}
        self.priorCount = {}
        self.likelihood = {}
        self.pba   = {}
        self.pbaCount   = {}
        self.strategicCount = {} 
        self.total = 0
        self.date = None
        self.code = None
        self.strategic = conf.get("strategic",Strategic(conf = self.conf))

    def __getitem__(self,name):
        """
            >> train.train()
            >> type(train['likelihood']) == dict
            True
        """
        if hasattr(self,name):
            return getattr(self,name)
        else:
            return None

    def collect(self,projectPath=None):
        """
            >> projectPath = os.path.join(conf.get("SYS_HOME"),case["collect"]['projectPath'])

            >> train.collect(projectPath)
            >> type(train.collect(projectPath)) == dict
            True
        """
        conf = self.conf
        data={}
        projectPath = projectPath or os.path.join(conf.get("SYS_HOME"),conf.get("STATISTICS_PROJECT_PATH"))
        expressions = self.expression.load(path=projectPath)
        for i in range(0,conf.get("MIN_DATA_NUM",MIN_DATA_NUM)):
            date=Date.getDate(0-i,conf.get('date',Date.getDate()))
            result={}
            for code in self.stock.allCode:
                result[code]={}
            self.expression.execute(expression= conf.get("expressions",expressions), context = {"result":result,"date":date})
            if not result:
                break;
            data[date]=result
        return data   

    def collectStrategicData(self,date):
        """
            >>> train.collectStrategicData(date = '20110728')
            >>> len(train.strategicCount)>1
            True
            >>> train.strategicCount = {}
            >>> train.strategic={"20110902":{"a":['601919','601918'],"b":['610000']}}
            >>> train.collectStrategicData(date = '20110902')
            >>> train.strategicCount == {"a":2,"b":1}
            True
        """
        strategicCount = self.strategicCount
        for strategicName in self.strategic[date]:
            if not strategicName in strategicCount:
                strategicCount[strategicName] = 0
            strategicCount[strategicName] += len(self.strategic[date][strategicName])

    def train(self):
        """
        根据collect收集的数据计算prior,likelihood等值。

            >> train.train()

            >> train.prior
            >> type(train.prior)==dict
            True
            >> train.likelihood
            >> type(train.likelihood)==dict
            True

        """
        if not self.data:
            self.data = self.collect()
        data  = self.data
        self.pbaCount = {}
        self.strategicCount = {}
        for date in data:
            self.date = date
            self.collectStrategicData(date = date)
            for code in data[date]:
                self.code = code
                self.trainPrior(data[date][code])
                self.trainLikelihood(data = data[date][code] ,date = date)
        self.total = len(self.data) * len(self.stock.allCode)
        self.calculatePrior()
        self.calculateLikelihood()
    
    def trainPrior(self,data):
        count =self.priorCount
        for statisticsName in data:
            if not statisticsName in count:
                count[statisticsName] = 0
            if data[statisticsName] == True:
                count[statisticsName] += 1

    def calculatePrior(self):
        """
        prior  P(A)的概率。Prior Probability 先验概率 P(R)，即根据训练材料得出的假设概率。如统计最近15天里上涨5%的股票的概率。
        1-prior P(A')的概率。
        """
        for statisticsName in self.priorCount:
            count = self.priorCount[statisticsName] or 0
            self.prior[statisticsName] = float(count) / float(self.total)
    
    def trainLikelihood(self,data,date=None):
        """
        计算在各统计条件下各策略发生次数，如上涨5%，且属于锤头策略的发生次数
            >> testBayesTrain.initTestTrainlikelihood(train)
            >> train.trainLikelihood(case['trainLikelihood'])
            >> train.pbaCount == testBayesTrain.result['trainLikelihood']['pbaCount']
            True
        """
        pbaCount  = self.pbaCount
        date = date or self.date
        for statisticsName in data:
            for strategicName in self.strategic[self.date]:
                if not statisticsName in pbaCount:
                    pbaCount[statisticsName]={}
                if not strategicName in pbaCount[statisticsName]:
                    pbaCount[statisticsName][strategicName]  = 0
                if data[statisticsName] == True and self.code in self.strategic[strategicName]:
                    pbaCount[statisticsName][strategicName] +=1

    def calculateLikelihood(self):
        """
        计算可能性因子。设B为策略模型,A为统计事件
        P(B|A) 指统计事件中符合策略的概率 ，如上涨%5的股票中属于策略A的概率
        P(B|A) = len(B union A)/len(A)
        len(A) = self.priorCount
        len(B^A) = self.pbaCount
        
        P(B|A')指非统计事件中符合策略的概率,如没有上涨%5的股票中属于策略A的概率
        A'指 complement A
        P(B|A') = (len(B)-len(B union A)) / (total - len(A))
        len(B) = len(strategic)

        likelihood 可能性因子
                                 P(B|A)
        likelihood = -------------------------------
                     P(B|A) * P(A) + P(B|A') * P(A')

            >> testBayesTrain.initTestCalculatelikelihood(train)
            >> train.calculateLikelihood()

            >> train.likelihood
            >> train.likelihood == testBayesTrain.result['calculateLikelihood']['likelihood']
            True
        """
        for statisticsName in self.pbaCount:
            for strategicName in self.pbaCount[statisticsName]:
                if not strategicName in self.likelihood:
                    self.likelihood[strategicName]={}
                if self.priorCount[statisticsName]:
                    pbaCount = float(self.pbaCount[statisticsName][strategicName])
                    pba = float(pbaCount/self.priorCount[statisticsName])
                    pbca=float(self.strategicCount[strategicName] - pbaCount) \
                    / float(self.total - self.priorCount[statisticsName])
                    prior = float(self.prior[statisticsName])
                    num = float(pba * prior + pbca *( 1 - prior))
                    if num:
                        likelihood=pba/num
                    else:
                        likelihood=0
                else:
                    likelihood = 0
                self.likelihood[strategicName][statisticsName] = likelihood

if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(__dir__,"..","..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    path = os.path.join(LIB_HOME,"tests","statistics")
    sys.path.insert(0, path)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    from lib.stk.tests.statistics.bayes import testBayesTrain
    case = testBayesTrain.case
    result = testBayesTrain.result
    train = Train(conf)
    doctest.testmod()
