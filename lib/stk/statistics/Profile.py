#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
报告市场整体情况

验证理论成功概率:
    80%个股收盘价大于30日均价时---大盘即将见顶；
    5%以内个股收盘价大于30日均价时---大盘见底。
"""
import os,sys
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from element import Stock,Date

class Profile:
    def __init__(self,conf={}):
        self.conf=conf
        self.stock=conf.get("stock",Stock(conf))
        self.date=conf.get("date",Date.getDate())

    def profile(self):
        res={"highThanMa30":0,"lowThanMa30":0,"total":0}
        for code in self.conf.get("allCode",self.stock.allCode):
            price=self.stock[self.date][code].close
            ma30=self.stock.ma(30)
            if price and ma30:
                if float(price)>float(ma30):
                    res['highThanMa30']=res['highThanMa30']+1
                elif float(price)<float(ma30):
                    res['lowThanMa30']=res['lowThanMa30']+1
                res['total']=res['total']+1
        return res
    
    def viewProfile(self):
        data = self.profile()
        print("""80%个股收盘价大于30日均价时---大盘即将见顶；
5%以内个股收盘价大于30日均价时---大盘见底。""")
        print(data)
        if float(data['total']):
            highThanMa30Rate=float(data['highThanMa30'])/float(data['total'])
        else:
            highThanMa30Rate=0
        print("收盘价大于30日均价:"+str(highThanMa30Rate))
        if float(data['total']):
            lowThanMa30Rate=float(data['lowThanMa30'])/float(data['total'])
        else:
            lowThanMa30Rate=0
        print("收盘价小于30日均价:"+str(lowThanMa30Rate))

if __name__=="__main__":
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
    app=Profile(conf)
    app.viewProfile()
