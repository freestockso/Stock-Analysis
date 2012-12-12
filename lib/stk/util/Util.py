#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging,re,sys,os
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)

SUFFIX=".json"

def getCode(num):
    strNum=str(num)
    while len(strNum)<6 :
        strNum='0'+strNum
    return strNum

def getDate(data):
    if type(data) == str:
        try:
            utf8Data=data.decode("utf-8")
        except:
            try:
                utf8Data=data.decode("gbk")
            except:
                pass
    reDate=re.compile("date:(\d+)")
    try:
        tmpData=reDate.search(utf8Data)
        if tmpData!=None:
            date=tmpData.group(1)
    except AttributeError:
        print (reDate.search(utf8Data))
    return date

def getLastCode(path):
    """
        path最好用绝对路径
        >>> __dir__ = os.path.realpath(os.path.dirname(__file__))
        >>> getLastCode(path=os.path.join(__dir__,"../tests/testDetailData/20100520"))
        '000502'
    """
    return max(map(lambda name:name.rstrip(SUFFIX),os.listdir(os.path.join(path))))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
