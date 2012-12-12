#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,SYS_HOME)
from lib.stk.downloader.Info import Info

def run(conf={}):
    conf["INFO_DATA_PATH"]=os.path.join(SYS_HOME,conf.get("INFO_DATA_PATH",""))
    app=Info(conf)
    return app.download()

