#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This stock application is made to analyze stock infomation and get the report when to buy stocks and sell stocks.

usage:
    计算今日数据
    stock.py start
    计算特定日期的数据
    stock.py start --date=101015
    从指定日期继续开始,“断点续传”
    stock.py start --restart
    从某一日期开始计算
    stock.py start --from=101015
    从头开始计算
    stock.py start --from=beginning

    更新数据
    stock.py update
    更新指定日期数据
    stock.py update --date=101015

    更新整个市场的股票信息，如有多少股票，每个股票代码对应的名称等.
    stock.py updateInfo

    计算指定strategic
    stock.py run --module=strategic --strategic=强势股1008021536 
    依次运行计算所有日期的strategic,statistic,reporter模块
    stock.py run --module=strategic,statistic,reporter
    指定忽略的模块
    stock.py run --module=strategic,statistic,reporter --ignore=update

    用debug模式计算特定日期的数据,用于调试程序
    main.py start --date=101015 --debug

"""
import os,sys,logging,imp
__dir__ = os.path.realpath(os.path.dirname(__file__))
SYS_HOME=os.path.join(__dir__,"..")
COMMANDS_DIR = os.path.join(SYS_HOME,"app","commands")
sys.path.insert(0,SYS_HOME)

from lib.util import Log,Conf
from lib.stk import Date

STOCK_MODULES=[
    "update",
    "compute",
    "strategic",
    "reporter",
    "statistics"
]
def parseArgs(conf):
    """
    parse args 
    """
    import argparse
    args={}
    argparser=argparse.ArgumentParser(description = __doc__.strip())
    argparser.add_argument("--version",action='version', \
                           version='%(prog)s '+str(conf.get("VERSION")))
    subparsers=argparser.add_subparsers(metavar="<action>")

    #start
    startparser=subparsers.add_parser("start",description="开始运行程序.")
    startparser.set_defaults(action="run")
    startparser.add_argument("--restart",type=str)
    startparser.add_argument("--from",type=str)
    startparser.add_argument("--date",type=str)

    #run
    runparser=subparsers.add_parser("run",description="运行指定模块.")
    runparser.set_defaults(action="run")
    runparser.add_argument("--module",type=str)
    runparser.add_argument("--ignore",type=str)
    runparser.add_argument("--from",type=str)
    runparser.add_argument("--date",type=str)
    runparser.add_argument("--debug",help='用debug模式计算,用于调试程序',action="store_true")

    #update
    updateparser=subparsers.add_parser("update",description="更新指定日期数据.")
    updateparser.set_defaults(action="update")
    updateparser.add_argument("--from",type=str)
    updateparser.add_argument("--date",type=str)

    #updateInfo
    updateInfoParser=subparsers.add_parser("updateInfo",description="更新整个市场的股票信息，如有多少股票，每个股票代码对应的名称等.")
    updateInfoParser.set_defaults(action="updateInfo")
    
    #shell
    shellparser = subparsers.add_parser("shell",description="shell.")
    shellparser.set_defaults(action="shell")
    
    #instant
    instantparser = subparsers.add_parser("instant",description="instant compute for sotck.")
    instantparser.set_defaults(action="instant")

    parsedArgs=argparser.parse_args()
    
    #generate conf
    #--date
    if parsedArgs and getattr(parsedArgs,"date",None):
        args['dates'] = parsedArgs.date.split(",")
    #--from
    if getattr(parsedArgs,"from",None):
        from lib.stk.data.Check import Check
        check=Check(conf)
        args['dates'] = check.getAvailableDate(date = getattr(parsedArgs,"from"),module = getattr(parsedArgs,"module",None))
    #--module
    if getattr(parsedArgs,"module",None):
        args["module"]=[]
        modules=parsedArgs.module.split(",")
        for module in modules:
            args["module"].append(module)
    #--ignore
    if getattr(parsedArgs,"ignore",None):
        args["module"]=STOCK_MODULES
        modules=parsedArgs.ignore.split(",")
        for module in modules:
            if module in args["module"]:
                del args["module"][args["module"].index(module)]
                logging.info("Ignore "+str(module))
    #--debug
    if getattr(parseArgs,"debug",None):
        args["DEBUG"]=True
    args['action']=parsedArgs.action
    return args

def execute(cmd_name,conf={},COMMANDS_DIR=[COMMANDS_DIR]):
    fp = False
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

if __name__=="__main__" :
    if sys.argv[1:]:
        conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
        conf["SYS_HOME"]=SYS_HOME
        conf.update(parseArgs(conf))
        Log.set(os.path.join(SYS_HOME,conf.get("LOG_PATH")))
        action=conf.get("action","run")
        dates=conf.get("dates")   #如果指定多个日期，则按顺序启动实例一个一个运行
        stockCache = {} #@todo add stockCache
        if not dates  or len(dates)==0:
            conf['date']=Date.getDate()
            execute(cmd_name = action,conf=conf)
        elif len(dates)>=1:
            for sDate in dates:
                conf["date"]=sDate
                if stockCache:
                    conf['stock']=stockCache
                execute(cmd_name = action,conf=conf)
    else:
        print __doc__
