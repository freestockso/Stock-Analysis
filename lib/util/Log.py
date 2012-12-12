#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,logging
LOG_PATH = os.path.join("logs","log.txt")
LOG_LEVEL = logging.DEBUG
PRINT_LEVEL = logging.INFO

def set(logPath = None,printLevel = None,logLevel = None):
    """
    配置打印的日志级别和参数
    >>> set()
    >>> logging.debug('debug message')
    >>> logging.info('info message')
    >>> logging.warn('warn message')
    >>> logging.error('error message')
    >>> logging.critical('critical message')
    """
    logPath = logPath or LOG_PATH
    logLevel = logLevel or LOG_LEVEL
    logging.basicConfig(level = logLevel,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename=logPath,filemode='a+')
    fh=logging.StreamHandler()
    printLevel = printLevel or PRINT_LEVEL
    fh.setLevel(printLevel)
    logging.getLogger().addHandler(fh)
    logging.info("Start logging, log path is "+logPath+", log level is INFO.")

if __name__ == '__main__':
    import doctest
    doctest.testmod()
