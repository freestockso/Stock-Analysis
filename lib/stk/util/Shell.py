#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    载入默认数据和对象，建立基于python命令行的初始化环境，储存执行过程中的中间变量，便于系统调试和使用。支持自定义命令。
    实现设计:
        初始载入elements中的所有元素，数据放imported_objects中
        交互输入的命令通过如下方法执行:
            通过imp模块载入各模块
            将输入输出信息通过sys.stdout/sys.stderr显示出来

    设计命令:
        -| 
            strategic strategic1.py

"""
import os,sys,code
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)
from element import Stock 
#sys.ps1="stock >>>"
#sys.ps2="stock ..."

class Shell:
    def __init__(self,conf={}):
        self.conf=conf

    def loadObject(self):
        data = {
            "stock":Stock(self.conf),
            "conf":self.conf
        }
        return data
    
    def handle(self):
        """
        >>> shell.handle()
        
        Commands:
            usage:
                run find a code which has most high raising price.

            feature:
                - auto load data [Base.py]
                - run [Shell.excute] --- run code
        """
        # Set up a dictionary to serve as the environment for the shell, so
        # that tab completion works on objects that are imported at runtime.
        imported_objects = self.loadObject()
        #增加自动提示功能
        try: # Try activating rlcompleter, because it's handy.
            import readline
        except ImportError:
            pass
        else:
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(imported_objects).complete)
            readline.parse_and_bind("tab:complete")
        #启动命令行
        code.interact(local=imported_objects)

if __name__ == '__main__':
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    import logging
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    shell = Shell(conf)
    shell.handle()
