#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
选出符合预设标准的股票
"""
import os,sys,logging
from Expression import Expression
import Date
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from data import Reader,Dumper,Check
try:
    from statistics.bayes.Bayes import Bayes
except ImportError:
    from lib.stk.statistics.bayes.Bayes import Bayes

SUFFIX = ".json"
REPORTER_DATA_PATH = "data/reporter/"
REPORTER_PROJECT_PATH = "app/reporter/projects/"
TRIGGER_PROHABILITY=0.9
BAYES_DATA_PATH = "data/statistics/bayes/"

class Report(object):
    def __init__(self,date=None,conf={}):
        self.date = date or conf.get("date",Date.getDate())
        self.data = conf.get("data",{})
        self.conf = conf

    def check(self):
        check = Check.Check(conf = self.conf)
        if not check.checkReporterCondition(date = self.date):
            raise ValueError("Reporter is invailable.date:%s" % self.date)

    def getTrade(self,date=None):
        """
            得到符合交易条件的数据
            >>> report.data = case['fullreport']
            >>> report.getTrade(date = '20110902') == testResult['getTrade1']
            True
        """
        trade = {}
        date = date or self.date
        if not date in self.data:
            self.data[date] = self.load(date)
        report = self.data.get(date,None)
        if not report:
            return {}
        for code in report:
            for statisticsName in report[code]['statistics']:
                probability = report[code]['statistics'][statisticsName]
                if probability > TRIGGER_PROHABILITY:
                    if not code in trade:
                        trade[code]={}
                    if not 'strategic' in trade[code]:
                        trade[code]['strategic'] = report[code]['strategic']
                    if not 'statistics' in trade[code]:
                        trade[code]['statistics'] = {}
                    trade[code]['statistics'][statisticsName]=probability
        return trade

    def load(self,date):
        if not self.data.get(date,None):
            reporterPath = os.path.join(self.conf.get("SYS_HOME",""),self.conf.get("REPORTER_DATA_PATH",REPORTER_DATA_PATH),date+SUFFIX)
            self.data[date] = Reader.read(reporterPath)
        return self.data.get(date,None)  

    def dump(self):
        if self.data:
            path = os.path.join(conf.get("SYS_HOME",""),conf.get("REPORTER_DATA_PATH",REPORTER_DATA_PATH),self.date+SUFFIX)
            Dumper.dump(path = path , data = report.data)
            logging.info("Reporter result : %s" % str(report))
        else:
            logging.warning("Reporter run fail.")


    def compute(self,strategic,statistics):
        """
        传入统计数据和模型数据，计算得出报告

        >>> report.compute(strategic = case['strategic'] , statistics = case['statistics']) == testResult['compute']
        True

        """
        projectPath=os.path.join(self.conf.get("SYS_HOME"),self.conf.get("REPORTER_PROJECT_PATH",REPORTER_PROJECT_PATH))
        expression=Expression(self.conf)
        expressions = expression.load(path=projectPath)
        result={}
        for func in expressions:
            result[func.get("name")]=[]
        expression.execute(expression= self.conf.get("expressions",expressions), context = {"result":result},conf = {"dataName":"statistics","data":statistics,"itemName" : "strategic"})
        #format data
        self.data=self.getFullReporter(strategic = strategic,statistics = statistics ,report = result)
        return self.data

    def getFullReporter(self,strategic , statistics, report ):
        """
        传入统计数据和一个report的project，获得符合条件的股票代码等数据。
        得到如下形式的结果
        {
            ...
            "601919":{"statistics":{"stat1":0.954545,"stat2":0.8,"stat3":0.39130435},"strategic":["stra1","stra2"]},
            ...
        }
        >>> report.getFullReporter(report = case['report'],strategic = case['strategic'], statistics = case['statistics']) == testResult['getFullReport']
        True
        """
        res = {}
        for reportName in report:
            reportData = report[reportName]
            res[reportName]={}
            for code in strategic.allCode:
                for strategicName in reportData:
                    if code in strategic.get(strategicName):
                        if not code in res[reportName]:
                            res[reportName][code] = {}
                        if statistics and strategicName in statistics:
                            res[reportName][code].update({strategicName:statistics[strategicName]})
        result = self.merge(res)
        return result

    def merge(self,data):
        """
        >>> data = case['merge']
        >>> report.merge(data) == testResult['merge']
        True
        """
        result={}
        for reportName in  data:
            for code in data[reportName]:
                result[code]={'strategic':data[reportName][code].keys(),"statistics":{}}
                reportStatistics={}
                for strategicName in data[reportName][code]:
                    subStatistics = data[reportName][code][strategicName];
                    for statisticsName in subStatistics:
                        if not statisticsName in reportStatistics:
                            reportStatistics[statisticsName] = []
                        reportStatistics[statisticsName].append(subStatistics[statisticsName])
                for statisticsName in reportStatistics:
                    stats=reportStatistics[statisticsName]
                    result[code]["statistics"][statisticsName]=Bayes.combining(stats)
        return result

if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    from lib.stk.tests.element.report import case , result as testResult
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    report = Report(conf = conf)
    doctest.testmod()
