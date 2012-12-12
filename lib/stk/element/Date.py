#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
common time function
the spectious case:
1.if options is number and time is extra 24:00,but not 15:00,then today=tomorrow
如果传进函数的参数为字符串，则直接转化成当前时间。传进来的是数字的话，会转化成股市开盘的时间。
如果早于3点，由于股市没有收市，则基准日期点算做昨天
同样，如果是周六/周日，基准日期点算做周五
example:

"""
import time,math,json,os
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
DATA_PATH=os.path.join(LIB_HOME,"..","data")
ADV_DATA_PATH=os.path.join(DATA_PATH,"adv","data.json")
DETAIL_DATA_PATH=os.path.join(DATA_PATH,"detail")

def isInvalidDate(date):
    """
    过滤股市非周六周日的休假日，如端午节，劳动节，春节等
    """
    invalidDate=["20100614","20100615","20100616","20100922","20100923","20100924","20101001","20101004","20101005","20101006","20101007","20110103","20110912","20111003","20111004","20111005","20111006","20111007"]
    return  date in invalidDate

def date2time(date):
    """
        >>> date2time("20110817")
        1313510400.0
    """
    if type(date)!=str:
        date=str(date)
    intTime=time.mktime(time.strptime(date,"%Y%m%d"))
    return intTime

def time2date(intTime):
    """
        >>> time2date(1313510400)
        '20110817'
    """
    if type(intTime)!=int:
        intTime=int(intTime)
    date=time.strftime("%Y%m%d",time.localtime(intTime)) 
    return date

def getInstantDate():
    localTime=time.localtime()
    hour=int(time.strftime("%H",localTime))
    minutes=int(time.strftime("%m",localTime))
    if 15> hour >9  or (hour ==9 and minutes<30):
        return getDate(1)
    else:
        return getDate()

def getDate(index=0,date=None,numTime=None):
    """
    @param {int} [index] 相对于基准日期的偏移
    @param {str} [date] 基准日期

        >>> getDate(0,'20100609')
        '20100609'
        >>> getDate(1,"20100611")
        '20100617'
        >>> getDate(-4)
        '20110811'

    """
    #现将date转成数字型intTime，然后统一处理
    if numTime:
        intTime=int(numTime)
    elif date:
        date=str(date)
        intTime=date2time(date)
    else:
        numTime=time.time()
        intTime=numTime

    if type(index) != int:
        index=int(index)

    localTime=time.localtime(intTime)
    intWeek=int(time.strftime("%w",localTime))
    intHour=int(time.strftime("%H",localTime))
    #如果早于3点，由于股市没有收市，则基准日期点算做昨天
    #同样，如果是周六/周日，基准日期点算做周五
    num=0
    if intWeek==0:
        num=num-2
    elif (numTime and intHour <15) or intWeek==6:
        num=num-1
    #import pdb;pdb.set_trace()
    #修正的日期数(num)加上传进来的偏移量(index)，经过处理得到要返回的日期
    #使用没有周六，周日的5进制周期。
    intTime=intTime+60*24*60*num
    localTime=time.localtime(intTime)
    intResWeek=int(time.strftime("%w",localTime))
    intTime=intTime+(math.ceil((float(intResWeek)+index)/5-1)*2+index)*60*24*60
    try:
        sDate=time.strftime("%Y%m%d",time.localtime(intTime)) 
    except:
        sDate=None
        #import pdb;pdb.set_trace()
        pass
    if isInvalidDate(sDate):
        sDate=getDate(1,sDate)
    return sDate

def getDateBetween(options,date2=None):
    """
    >>> getDateBetween("20100601","20100602")
    1
    >>> getDateBetween("20100528","20100602")
    3
    >>> getDateBetween("20100602","20100507")
    18
    """
    if date2!=None:
        date1=options
    elif "date1" in options:
        date1=options['date1']
        date2=options['date2']

    if "date1" in vars() and "date2" in vars():
        if date1==date2:
            return 0
        else:
            if int(date1)<int(date2):
                tmpdate=date2
                date2=date1
                date1=tmpdate
        date1=getDate(index = 0,date=date1)
        date2=getDate(index = 0,date=date2)
        time1=date2time(date1)
        time2=date2time(date2)
        between=(float(time1)-float(time2))/(60*60*24)
        while date1!=getDate(index=between,date=date2) and int(date1)>int(date2):
            between=between-1
    else:
        return None
    between=int(between)
    return between

def getAllDate(mode="adv",advDataPath=None,detailDataPath=None):
    """
    获得所有可处理的日期
    >>> type(getAllDate(mode="adv"))==list
    True
    >>> type(getAllDate(mode="detail"))==list
    True
    """
    advDataPath = advDataPath or ADV_DATA_PATH
    detailDataPath = detailDataPath or DETAIL_DATA_PATH
    allDate=[]
    if mode=="adv":     #adv mode
        filePath=advDataPath
        if os.path.exists(filePath):
            fh=open(filePath,"r")
            data=json.load(fh)
            if data:
                for item in data:
                    allDate.append(item)
    elif mode=="detail":   #detail mode
        allDate=os.listdir(detailDataPath)
    allDate.sort()
    return allDate

if __name__ == '__main__':
    import doctest
    doctest.testmod()
