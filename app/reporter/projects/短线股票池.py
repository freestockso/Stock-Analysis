stat1 = '一日上涨1%'.decode('utf-8')
stat3 = '三日上涨3%'.decode('utf-8')
stat5 = '五日上涨5%'.decode('utf-8')
if statistics.get(strategic,{}).get(stat1,0)>0.8 \
   or statistics.get(strategic,{}).get(stat3,0)>0.8 \
   or statistics.get(strategic,{}).get(stat5,0)>0.8: 
    result[name].append(strategic)
