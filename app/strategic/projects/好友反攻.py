#close['-1']/open['-1']<0.97
#close['-1'] <= close['0']
#close['0']>open['0']
#close['0']<max['30']*0.7

if stock[date][code].index(-1).close < 0.97 * stock.open and \
   stock.index(-1).close <= stock.close  and \
   stock[date].close > stock.open and \
   stock.close < stock.max(30)*0.7:
    result[name].append(code)
