#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析计算公式，得到需要载入的变量,计算并返回结果
@example
    >>> path=os.path.join(LIB_HOME,"tests/projects")
    >>> expressions=expression.load(path=path)
    >>> expression.execute(expression=expressions,context={"date":'20110818',"result":{}},conf={"allCode":['000001']})
    True
    >>> len(expression.context['stock'].data.adv['20110818']['000001']['sequence'])>0
    True

    >> expression.context['stock'].data.adv['20110818']['000001']
"""
import os, sys, logging, keyword,re
import Date,Stock
__dir__ = os.path.realpath(os.path.dirname(__file__))
LIB_HOME=os.path.join(__dir__,"..")
sys.path.insert(0,LIB_HOME)

class Expression:
    def __init__(self,conf={}):
        """
        @param {list} conf["expression"] 要执行的表达式
        @parma [date] conf['date'] 要处理的日期
        @pram conf['project'] 要处理的project名。如果传入该参数，则处理该参数指定的project.否则处理expressionPath里所有的project
        @param conf['context'] exec执行公式时的环境变量
        """
        self.conf=conf
        self.code=None
        self.date=conf.get('date',Date.getDate())
        self.stock=conf.get("stock",Stock.Stock(conf))
        self.project=conf.get('project',[])
        self.context=conf.get('context',{})
        self.re={}   

    def execute(self,expression=None,context={},conf={}):
        """
        解析公式，载入数据后，运行公式
        @param {dict} expression 要处理的公式
        @param context exec执行时的本地变量
        """
        if type(conf)!=dict:
            conf={}
        options={}
        options.update(self.conf)
        options.update(conf)
        conf=options
        #default setting data: stock =>self.stock,item: code => item
        data = conf.get("data",conf.get("allCode",self.stock.allCode))
        execContext=self.getContext(context = context,conf=conf)
        #start loop exec
        expression=expression or conf.get("expression",[])
        for func in expression:
            execContext['name']=func.get("name")
            for item in data:
                execContext[conf.get("itemName","code")]=item
                self.execExpression(expression=func.get("content"),context=execContext)
        return True
    
    def getContext(self,context,conf={}):
        """
        context为exec执行时的本地变量
        """
        retContext = context or {}
        retContext[conf.get("dataName","stock")] = conf.get("data",self.stock)
        retContext['date']=self.date
        if type(context) == dict:
            retContext.update(context)
        return retContext

    def getExpressionByName(self,name,expressions):
        find = None
        for expression in expressions:
            if type(expression["name"])!=unicode:
                expression["name"] = expression["name"].decode("utf-8")
            if expression['name'] == name:
                find = expression
                break
        return find

    def execExpression(self,expression,context={},conf={}):
        """
        传入数据以及公式内容，执行公式,要返回公式执行后的数据，可采用如下形式:

        >> context={"date":'20110818',"result":'the place where to store result'}
        >> path=os.path.join(LIB_HOME,"tests/projects")
        >> expressions=expression.load(path=path)
        >> for func in expressions:
        ...     expression.execExpression(expression=func.get("content"),context=context)
        >> expression.context['result'] 
        'the place where to store result'
        """
        try:
            #import pdb;pdb.set_trace()
            if type(expression) ==str:
                exec(expression,globals(), context)
            else:
                logging.error( "expression need to be str , but is %s" % expression)
        except Exception as e:
            try:
                if type(e) ==str:
                    message = e
                else:
                    message = str(e)
            except:
                message=''
            logging.error("Expression execute error when handling %s error info is %s %s"
            % (context.get("name","unknow") , sys.exc_info()[0], message))
        if type(context)==dict:
            self.context.update(context)

    def load(self,path,project=None):
        """
        传入公式路径，载入公式内容
        >>> expressions = expression.load(path=os.path.join(LIB_HOME,'tests/expression/projects'))

        >>> expressions
        >>> len(expressions)==2
        True
        """
        exprs=[]
        for root, dirs, files in os.walk(path):
            for sFile in files:
                splitext=os.path.splitext(sFile)
                if len(splitext)>1 and splitext[1]==".py":
                    name = splitext[0]
                    if type(name)!=unicode:
                        try:
                            name = name.decode("utf-8")
                        except:
                            name = name.decode("gbk")
                    exprs.append({"name":name,"path":os.path.join(path,sFile)})
        loadExprs=[]
        for expr in exprs:
            if project and not expr.get("name",None) in project:
                continue
            fh=open(expr['path'],"r")
            content = fh.read()
            self.re['offset'] = self.re.get("offset",re.compile(r"[\[\(](-\d+)[\)\]]"))
            offset = min(map(lambda offset:int(offset),self.re['offset'].findall(content)) or [0])
            name = expr['name']
            loadExprs.append({
                'name':name,
                'path':expr['path'],
                'content':content,
                'offset':offset
            })
        return loadExprs
    
    def isValidParamName(self,name):
        """
            >>> expression.isValidParamName("insert")
            False
        """
        invalidNameList=["push","pop","insert","len"]
        if not name or keyword.iskeyword(name) or name in invalidNameList:
            return False
        return True

if __name__ == '__main__':
    import doctest
    SYS_HOME=os.path.join(__dir__,"..","..","..")
    sys.path.insert(0,SYS_HOME)
    from lib.util import Conf,Log
    conf=Conf.load(\
            os.path.join(SYS_HOME,"conf","stock.yaml"),
            os.path.join(SYS_HOME,"conf","downloader.yaml"))
    logPath=os.path.join(SYS_HOME , conf.get("LOG_PATH",""))
    Log.set(logPath = logPath , printLevel=logging.DEBUG)
    conf["SYS_HOME"]=SYS_HOME
    conf["DEBUG"]=True
    expression=Expression(conf)
    #import pdb;pdb.set_trace()
    doctest.testmod()
