#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
贝叶斯计算公式

                                      P(B|A)
        P(A|B) = P(A) * --------------------------------
                         P(B|A) * P(A) + P(B|A') * P(A')


对外接口:
    计算一个贝叶斯 Posterior Probability 值
    >>> posterior = bayes.posterior()

    计算联合概率
    >> posteriors = []
    >> for strategicName in posterior:
    ...    for statisticsName in posterior[strategicName]:
    ...        posteriors.append(posterior[strategicName][statisticsName])
    >> bayes.combining(posteriors[0],posteriors[1],posteriors[2])

"""
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,LIB_HOME)
from Train import Train

class Bayes:
    def __init__(self,conf={}):
        self.data=conf.get("BAYES_DATA",None) 
        if not self.data:
            self.data = Train(conf = conf)
            self.data.train()
        self.conf=conf

    def posterior(self,prior = None,likelihood = None):
        prior = prior or self.prior()
        likelihood = likelihood or self.likelihood()
        posterior = {}
        for strategicName in likelihood:
            for statisticsName in likelihood[strategicName]:
                if not strategicName in posterior:
                    posterior[strategicName] = {}
                posterior[strategicName][statisticsName] = prior[statisticsName] * likelihood[strategicName][statisticsName]
        return posterior

    @classmethod
    def combining(cls,*posteriors):
        """
        Combining Probabilities

                           P1 * P2 ... P15
         P =   ---------------------------------------
               P1 * P2 ... P15 + (1-P1)(1-P2)...(1-P15)
        
            >>> P1 = 0.9
            >>> P2 = 0.8
            >>> P3 = 0.7
            >>> Bayes.combining(P1,P2,P3)
            0.9882352941176471
        """
        pm=1
        pcm=1
        if len(posteriors)==1 and type(posteriors[0]) ==list:
            posteriors = posteriors[0]
        if posteriors:
            for posterior in posteriors:
                pm = pm * float(posterior)
                pcm = pcm * float(1-posterior)

        result = pm / (pm + pcm)
        return result

    def prior(self):
        """
        Prior Probability
        """
        return self.data['prior']

    def likelihood(self):
        """
        Likelihood
        """
        return self.data['likelihood']

    def likelihood2(self,priorCount,pbaCount,strategicCount,total):
        """
        计算可能性因子。
        设B为策略模型,A为统计事件
        P(B|A) 指统计事件中符合策略的概率 ，如上涨%5的股票中属于策略A的概率
        P(B|A) = len(B union A)/len(A)
        len(A) = priorCount
        len(B^A) = pbaCount
        
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

            >> train.likelihood2(priorCount,pbaCount)
            >> train.likelihood2() == testBayesTrain.result['calculateLikelihood']['likelihood']
            True
        
        @param pbaCount a发生的同时b发生的次数统计
        @param priorCount 整体发生的次数统计
        @param strategicCount 所有策略发生的统计次数
        @param total 所有数据次数统计
        count 
        {   
            "priorCount":{
                "statistics1"
            },
            "strategicCount":{
                "strategic":
            },
            "total":
        }
        """
        likelihood = {}
        for strategicName in pbaCount:
            for statisticsName in pbaCount[strategicName]:
                if not strategicName in likelihood:
                    likelihood[strategicName]={}
                if priorCount[statisticsName]:
                    subPbaCount = float(pbaCount[strategicName][statisticsName])
                    pba = float(subPbaCount/priorCount[statisticsName])
                    pbca=float(strategicCount[strategicName] - subPbaCount) \
                    / float(total - priorCount[statisticsName])
                    prior = float(priorCount[statisticsName])/total
                    likelihood=pba/float(pba * prior + pbca *( 1 - prior))
                else:
                    likelihood = 0
                likelihood[strategicName][statisticsName] = likelihood
        return likelihood
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
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    bayes=Bayes(conf)
    doctest.testmod()
