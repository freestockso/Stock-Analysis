#low['0']==open['0']
#close['0']>1.04 * open['0']
#max['10']*0.8>close['-1']
if stock[date][code].low == stock.open and \
   stock.close > 1.04 * stock.open and \
   stock[date].max(10) * 0.8 > stock[date].index(-1).close:
   result[name].append(code)
