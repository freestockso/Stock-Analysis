#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stk 是一个用来处理股票数据的库，类似于自然语言处理库nltk。它也可以在命令行中使用.如:
>>> import stk.Stock as Stock
>>> stock = Stock()
>>> for date in stock:
...     for code , price in stock[date]:
...         print "s% %s price is %s" % (date,code,price)
"""
from data.Data import Data
from element import Date,Stock,Expression
from downloader.Downloader import Downloader
__all__=["Date","Stock","Downloader","Data","Expression"]

if __name__ == '__main__':
    import doctest,sys
    sys.path.insert(0,"..")
    doctest.testmod()
