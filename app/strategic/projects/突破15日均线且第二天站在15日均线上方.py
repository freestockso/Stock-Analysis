#low['-1']<ma15['-1']
#price['-1']>ma15['-1']
#price['0']>ma15['0']
#low['0']>ma15['0']
if stock[date][code].close > stock.ma(15) and \
   stock.low > stock.ma(15) and \
   stock[date].index(-1).close >stock[date].index(-1).ma(15) \
   and stock[date].index(-1).low < stock[date].index(-1).ma(15):
    result[name].append(code)
