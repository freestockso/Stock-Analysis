#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,logging,imp
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..","..")
COMMANDS_DIR = os.path.join(SYS_HOME,"app","commands")

STOCK_MODULES=[
    "update",
    "compute",
    "strategic",
    "reporter",
    "statistics"
]

def execute(cmd_name,conf={},COMMANDS_DIR=[COMMANDS_DIR]):
    fp=False
    try:
        fp, pathname, description = imp.find_module(cmd_name,COMMANDS_DIR)
    except:
        logging.error("No %s commands." % cmd_name)
    else:
        cmd = imp.load_module(cmd_name, fp, pathname, description)
        cmd.run(conf = conf)
    finally:
        if fp:
            fp.close()

def run(conf={}):
    """
    计算指定模块的数据
    """
    result=True
    date = conf.get("date")
    modules = conf.get("module",STOCK_MODULES)
    logging.info("Handling Date is " + date)
    for module in modules:
        if conf.get("DEBUG"):
            result =  execute(cmd_name = module,conf=conf) or result
        else:
            try:
                result =  execute(cmd_name = module,conf=conf) or result
            except:
                logging.error("Programme doesn't has module %s or occure error when handle it." % module)
    return result
