#volume['-1'] > 1.8 * volume['0']
#open['0']>ma60['0']
#price['-1']<price['0']
if stock[date][code].volume*1.8 < stock.index(-1).volume and \
   stock[date][code].open > stock.ma(60) and \
   stock[date][code].close > stock.index(-1).close:
    result[name].append(code)
