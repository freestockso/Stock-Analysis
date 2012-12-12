#low['0'] < 0.98 * open['0']
#low['0'] < 0.98 * close['0']
#high['0'] < 1.01 * close['0']
#close['0'] < max['30']*0.7
if stock[date][code].low < 0.98 * stock.open and \
   stock.low < 0.98 * stock.close  and \
   stock.high <1.01 * stock.close and \
   stock.close < stock.max(30)*0.7:
    result[name].append(code)
