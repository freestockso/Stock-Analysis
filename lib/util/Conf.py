#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,SYS_LIB_HOME)
import yaml
def load(*pathes):
    conf={}
    for path in pathes:
        if os.path.exists(path):
            fh=open(path,"r")
            data=yaml.load(fh)
            conf.update(data)
    return conf
