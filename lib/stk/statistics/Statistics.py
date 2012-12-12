#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计各种数据:
    - expection 数学期望
    - deviation 标准差
    - variance  方差
"""
import os,sys,logging,re

__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from element import Stock,Date

class Statistics:
    def __init__(self,conf = {}):
        self.conf = conf

    def statistics(self,subject,stock,date = None):
        """
        >> subject = [0.03,0.04]
        >> statistics.statistics(subject = subject,stock = stock,date = '20111024')
        0.19164835164835164
        """
        if type(subject) == list and len(subject) == 2:
            pass
        else:
            raise ValueError

        if date == None:
            date = [Date.getDate()]
        elif date == "all":
            date = stock.allDate
        elif type(date) != list:
            date = [date]
        total = 0
        count = 0
        for oneDate in date:
            for code in stock[oneDate].allCode:
                change = stock[code].change
                if  type(change)!=float :
                    continue
                minItem = subject[0]
                maxItem = subject[1]
                if float(minItem) <= change <float(maxItem): #Do note that left is <=
                    count += 1
                total += 1
        if not total:
            p = 0
        else:
            p = float(count)/total
        return p
    
    def expection(self,stock,date = None):
        """
        期望值公式 : expection = (x1 + x2 + x3 +... +xn)/n
        >> statistics.expection(stock = stock,date = '20111024')
        0.02870564489608117
        """
        sumValue = 0
        count = 0
        if date == None:
            date = [Date.getDate()]
        elif date == "all":
            date = stock.allDate
        elif type(date) != list:
            date = [date]

        for oneDate in date:
            for code in stock[oneDate].allCode:
                change = stock[code].change
                if type(change) == float:
                    sumValue = change + sumValue
                    count +=1
        return sumValue / count

    def deviation(self,stock,date = None):
        """
        标准差公式:
        s = s*2 ** 0.5
        """
        variance = self.variance(stock = stock,date = date)
        return variance ** 0.5
        
    def variance(self,stock,date = None):
        """
        方差公式:
        s^2 = [(x1-x)^2+(x2-x)^2+......(xn-x)^2]/n
        >> statistics.variance(stock = stock,date = '20111024')
        0.0002890704988633324
        """
        ex = self.expection(stock = stock,date = date)
        total = 0 
        count = 0

        if date == None:
            date = [Date.getDate()]
        elif date == "all":
            date = stock.allDate
        elif type(date) != list:
            date = [date]

        for date in date:
            for code in stock.allCode:
                change = stock[code][date].change
                if type(change) == float:
                    total +=(change - ex)**2
                    count +=1
        return total/count

    def sort(self,data):
        """
        >>> subject = [[-0.1,-0.09],[-0.09,-0.08],[-0.08,-0.07],[-0.07,-0.06],[-0.06,-0.05],[-0.05,-0.04],[-0.04,-0.03],[-0.03,-0.02],[-0.02,-0.01],[-0.01,0],[0,0.01],[0.01,0.02],[0.02,0.03],[0.03,0.04],[0.04,0.05],[0.05,0.06],[0.06,0.07],[0.07,0.08],[0.08,0.09],[0.09,0.1],]

        >>> stat = {}
        >>> for item in subject:
        ...     value = statistics.statistics(subject = item,stock = stock)
        ...     stat[str(item)] = value
        >>> stat = statistics.sort(stat)
        >>> stat
        """
        r = re.compile("\[(.*),")
        getK = lambda k:float(r.findall(k.keys()[0])[0])
        if type(data) == dict:
            stat =[]
            for item in data:
                stat.append({item:data[item]})
        elif type(data) == list:
            stat = data
        else:
            raise ValueError
        ret = sorted(stat,key = getK)
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

    statistics = Statistics()
    stock = Stock(conf)
    
    doctest.testmod()
