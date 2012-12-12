#min['10']==min['100']
#close['-4']>open['-4']
#close['-4']/open['-4']<1.03
#close['-3']>open['-3']
#close['-3']/open['-3']<1.03
#close['-2']>open['-2']
#close['-2']/open['-2']<1.03
#close['-1']>open['-1']
#close['-1']/open['-1']<1.03
#close['0']>open['0']
#close['0']/open['0']<1.03
#(price['-2']+price['-1']+price['0'])/3>(price['-4']+price['-3']+price['-2']+price['-1']+price['0'])/5*1.01
if stock[date][code].close > stock.open and \
   stock.close <1.03 * stock.open and \
   stock.min(10) == stock.min(100) and \
   stock[date].index(-1).close > stock.open and \
   stock.close <1.03 * stock.open and \
   stock[date].index(-2).close > stock.open and \
   stock.close <1.03 * stock.open and \
   stock[date].index(-3).close > stock.open and \
   stock.close <1.03 * stock.open and \
   stock[date].index(-4).close > stock.open and \
   stock.close <1.03 * stock.open and \
   (stock[date].close + stock[date].index(-1).close + stock[date].index(-2).close )/3 > (stock[date].close + stock[date].index(-1).close + stock[date].index(-2).close + stock[date].index(-3).close + stock[date].index(-4).close)/5*1.01 :
    result[name].append(code)
