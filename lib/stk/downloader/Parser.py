#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,logging
class ParserFactory:
    def __init__(self,source):
        parsers={
            "qq_min" : QqMinParser,
            "qq2" : Qq2Parser,
            "sina" : SinaParser,
            "cninfo" : CninfoParser,
            "instant_qq2" : InstantQq2Parser
        }
        parser = parsers.get(source)
        self.parser = parser()
        self.parse = self.parser.parse

class InstantQq2Parser:
    def __init__(self):
        pass

    def getName(self,name):
        if type(name) == str:
            try:
                name = name.decode('uft8')
            except:
                name = name.decode('gbk')
        return name

    def parse(self,data):
        """
                                    name   code   price change ratio_change volume total
        >>> s = 'v_s_sh600470="1~六国化工~600470~11.04~-0.27~-2.39~404707~45122~";\nv_s_sh601002="1~晋亿实业~601002~10.90~-1.11~-9.24~219819~24178~";\n'
        >>> parser.parse(s)
        """
        ret={}
        lines = data.splitlines()
        for line in lines:
            items = line.split("~")
            if items and len(items)>6:
                #name = self.getName(items[1])
                code = str(items[2])
                iClose = float(items[3])
                iOpen = ""
                iLow = ""
                iHigh = ""
                #change = float(items[5])/100
                volume = float(items[6])
                ret[code]={"close":iClose,"volume":volume,"high":iHigh,"low":iLow,"open":iOpen}
        return ret

class QqMinParser:
    def __init__(self):
        self.re=re.compile("(\d+) (\d+\.\d+) (\d+)")

    def parse(self,data):
        """
        minData为抓取的js格式的数据，供INSTANT模式使用。
        [{time:'0932',price:'12.300',volume:'102'}]
        """
        result=[]
        if type(data) == str:
            try:
                decodeData=data.decode("utf-8")
            except:
                decodeData=data.decode("gbk")
        else:
            decodeData=data
        findData=self.re.findall(decodeData)
        if findData:
            for item in findData:
                result.append({"time":item[0],"price":item[1],"volume":item[2]})
        return result

class SinaParser:
    def __init__(self):
        self.re=re.compile("(.+)\t(.+)\t(.+)\t(\d+)\t(\d+)\t(.*)")
    def parse(self,data):
        if type(data) == str:
            try:
                decodeData=data.decode("utf-8")
            except:
                decodeData=data.decode("gbk")
        else:
            decodeData=data
        #成交时间 成交价 价格变动 成交量（手） 成交额（元）性质
        findData=self.re.findall(decodeData)
        detailData=[]
        for item in findData:
            stime=item[0]
            price=item[1]
            change=item[2]
            volume=item[3]
            turnover=item[4]
            action=item[5]
            detailData.append({"time":stime,"price":price,"change":change,"volume":volume,"turnover":turnover,"action":action})
        return detailData

class Qq2Parser:
    def __init__(self):
        """
        将抓取的detail数据转为统一格式进行保存
        >> data=""
        >> parser=ParserFactory("qq2")
        成交时间 成交价 价格变动 成交量（手） 成交额（元）性质
        >> parser.parse(data)
        ()
        """
        self.re=re.compile("(.+)\t(.+)\t(.+)\t(\d+)\t(\d+)\t(.*)")

    def parse(self,data):
        if type(data) == str:
            try:
                decodeData=data.decode("utf-8")
            except:
                decodeData=data.decode("gbk")
        else:
            decodeData=data

        findData=self.re.findall(decodeData)
        detailData=[]
        for item in findData:
            stime=item[0]
            price=item[1]
            change=item[2]
            volume=item[3]
            turnover=item[4]
            action=item[5]
            detailData.append({"time":stime,"price":price,"change":change,"volume":volume,"turnover":turnover,"action":action})
        return detailData

class CninfoParser:
    def __init__(self):
        #for cninfo
        #self.re=re.compile("'\);\" target='_blank'>(\d{6}) ([\w \*]+)</a></td>")
        self.re=re.compile("'\);\" target='_blank'>(\d{6}) (.*?)</a></td>")

    def parse(self,data):
        """
        >>> data="\
        <td class='zx_data3'><A href='/information/companyinfo.html' onClick=\\"setLmCode('brief?shmb900951');\\" target='_blank'>900951 st1</a></td>\\n \
        <td class='zx_data3'><A href='/information/companyinfo.html' onClick=\\"setLmCode('brief?shmb900952');\\" target='_blank'>900952 st2</a></td>\
        "
        >>> parser=ParserFactory("cninfo")
        >>> parser.parse(data)
        [{'code': u'900951', 'name': u'st1'}, {'code': u'900952', 'name': u'st2'}]
        """
        if not data:
            return None
        res=[]
        
        if type(data) == str:
            try:
                decodeData=data.decode("gbk")
            except:
                decodeData=data.decode("utf8")
        else:
            decodeData=data

        try:
            findData=self.re.findall(decodeData)
            if findData:
                for item in findData:
                    code=item[0]
                    stockName=item[1]
                    res.append({"code":code,"name":stockName})
        except AttributeError:
            logging.debug("Error happend when extract info from fetch cninfo page data.")
            logging.debug(self.re.findall(decodeData))
        return res

if __name__ == '__main__':
    import doctest
    doctest.testmod()
