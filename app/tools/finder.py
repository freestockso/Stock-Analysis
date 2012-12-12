#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Finder.py --strategic= --date=
"""
import os,sys
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
sys.path.insert(0,SYS_HOME)

from lib.util import Log,Conf
from lib.stk import Expression

PROJECT_PATH="app/strategic/projects"

class Finder:
    def __init__(self,conf={}):
        self.conf = conf

    def find(self):
        expression=Expression(conf)
        projectPath=os.path.join(conf.get("SYS_HOME"),conf.get("STRATEGIC_PROJECT_PATH",PROJECT_PATH))
        projects = ["放2倍以上量"]
        expressions=expression.load(path = projectPath , project =projects)
        result={}
        for projectName in projects:
            result[projectName]=[]
        expression.execute(expression = expressions, context = {"result":result})
        return result

if __name__ == '__main__':
    conf=Conf.load(\
        os.path.join(SYS_HOME,"conf","stock.yaml"),
        os.path.join(SYS_HOME,"conf","downloader.yaml"))
    conf["SYS_HOME"]=SYS_HOME
    conf["date"]='20110927'
    Log.set(os.path.join(SYS_HOME,conf.get("LOG_PATH")))
    app=Finder(conf)
    print app.find()
