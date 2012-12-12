#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计系统发出交易指令后按预设行为进行交易的成功率和准确性

    >> accuracy.compute()
    [
        {
            "strategic":[],
            "statistics":{
                "stat1":{
                    "value":0.9
                    "match":[],
                    "nomatch":[],
                    "total":100
                }
            }
        },
        ...
    ]
        
"""
import os,sys,logging
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from element import Date
from element.Expression import Expression
from element.Stock import Stock
from element.Report import Report
STATISTICS_DATE_RANGE = 15
STATISTICS_PROJECT_PATH="app/statistics/projects"
MATCH_KEY = "matchCode"
NOTMATCH_KEY="notMatchCode"

class Accuracy:
    def __init__(self,conf={}):
        self.date=conf.get("date",Date.getDate())
        self.stock = conf.get("stock",Stock(conf=conf))
        self.expression=Expression(conf)
        self.expressions = self.expression.load(\
        path = os.path.join(conf.get("SYS_HOME"),conf.get("STATISTICS_PROJECT_PATH",STATISTICS_PROJECT_PATH)))
        self.report = Report(conf=conf)
        self.data = {}
        self.conf=conf

    def compute(self,date=None):
        """
        统计最近15天交易策略的准确性,用法示例见顶部.

            >>> accuracy.compute(date = '20110804')

        """
        detail=self.collect(date = date)
        accuracy = self.statistics(detail)
        return accuracy

    def collect(self,date=None):
        """
        收集需要被统计的数据

            >> accuracy.collect(date = "20110825")

        """
        conf = self.conf
        date = date or self.date or conf.get("date")
        detail={}
        dateRange = self.conf.get("STATISTICS_DATE_RANGE",STATISTICS_DATE_RANGE)
        for i in range(0,dateRange):
            for expression in self.expressions:
                curDate = Date.getDate(0-i,date)
                offsetDate = Date.getDate(expression['offset'],curDate)
                trade = self.report.getTrade(date = offsetDate)
                execDetail = self.execExpression(data = trade,date = offsetDate)
                if not execDetail:
                    continue
                detail.update({offsetDate:execDetail}) #将前一天统计数据加上今日统计数据便得到要生成的统计数据
        return detail

    def statistics(self,detail):
        """
        合并统计数据的结果,传入需要合并的数据，返回合并完的数据。错误返回{}
        """
        accuracy = {}
        total = {}
        for date in detail:
            for statisticsName in detail[date]:
                if not statisticsName in total:
                    total[statisticsName] = {'sum':0,'count':0}
                match = detail[date][statisticsName].get(MATCH_KEY,[])
                nomatch = detail[date][statisticsName].get(NOTMATCH_KEY,[])
                total[statisticsName]['sum'] +=len(match)
                total[statisticsName]['count'] +=len(match) + len(nomatch)
                if not statisticsName in accuracy:
                    accuracy[statisticsName] = {'detail':{}}
                accuracy[statisticsName]['detail'][date] ={MATCH_KEY: match,NOTMATCH_KEY:nomatch}

        for statisticsName in total:
            if total[statisticsName]['count'] ==0 :
                accuracy[statisticsName]['value']=0
            else:
                accuracy[statisticsName]['value'] = float(total[statisticsName]['sum'])/float(total[statisticsName]['count'])
            accuracy[statisticsName]['total']=total[statisticsName]['count']
        return accuracy


    def execExpression(self,data,date):
        """
        date 指买入日期
            >> accuracy.execExpression(data = {u'200056': {'statistics': {u'\u4e00\u65e5\u4e0a\u6da81%': 1.0,u'\u4e09\u5341\u65e5\u4e0a\u6da830%': 1.0,u'\u5341\u4e94\u65e5\u4e0a\u6da815%': 1.0000000000000002},'strategic': [u'\u77ed\u65f6\u95f4\u5185\u4e0b\u8dcc19%\u4ee5\u4e0a\u540e\u653e\u91cf\u6536\u7ea2']}}, date = '20110804')
            {u'\u5341\u4e94\u65e5\u4e0a\u6da815%': {'matchCode': [], 'notMatchCode': [u'200056']}, u'\u4e00\u65e5\u4e0a\u6da81%': {'matchCode': [], 'notMatchCode': [u'200056']}}
        """
        execResult = {}
        result = {}
        today = Date.getDate()
        for code in data:
            for statisticsName in data[code].get('statistics',{}):
                expression = self.expression.getExpressionByName(name = statisticsName,expressions = self.expressions)
                if not expression:
                    continue
                if not code in execResult:
                    execResult[code]={}
                offsetDate = Date.getDate(0-expression["offset"],date)
                if int(offsetDate) > int(today):
                    continue
                context = {
                    "result":execResult,
                    "code":code,
                    "name":statisticsName,
                    "stock":self.stock,
                    "date":offsetDate
                }
                self.expression.execExpression(expression = expression.get("content"), context = context)
                if execResult[code][statisticsName] == True:
                    sub = MATCH_KEY
                else:
                    sub = NOTMATCH_KEY
                if not statisticsName in result:
                    result[statisticsName]={MATCH_KEY:[],NOTMATCH_KEY:[]}
                result[statisticsName][sub].append(code)
        return result

if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    accuracy = Accuracy(conf = conf)
    path = os.path.join(LIB_HOME,"tests","statistics")
    sys.path.insert(0, path)
    #import testAccuracy as testData
    doctest.testmod()
