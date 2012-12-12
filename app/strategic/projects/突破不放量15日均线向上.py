#low['-1']<ma15['-1']
#price['-1']>ma15['-1']
#price['0']>ma15['0']
#low['0']>ma15['0']
#volume['0']/volume['-1']<1.1 or volume['0']/volume['-2']<1.1 or volume['0']/volume['-3']<1.1 or volume['0']/volume['-4']<1.1 or volume['0']/volume['-5']<1.1
#volume['0']/volume['-1']<2  and volume['0']/volume['-2']<2 and volume['0']/volume['-3']<2 and volume['0']/volume['-4']<2 and volume['0']/volume['-5']<2
#volume['-1']/volume['-2']<1.1 or volume['-1']/volume['-3']<1.1 or volume['-1']/volume['-4']<1.1 or volume['-1']/volume['-5']<1.1
#ma15['0']>ma15['-1']
if stock[date][code].close > stock.ma(15) and \
    stock.low > stock.ma(15) and \
    stock[date].index(-1).close >stock[date].index(-1).ma(15) \
    and stock[date].index(-1).low < stock[date].index(-1).ma(15) \
    and (stock[date].volume < 1.1 * stock[date].index(-1).volume \
    or stock[date].volume < 1.1 * stock[date].index(-2).volume \
    or stock[date].volume < 1.1 * stock[date].index(-3).volume\
    or stock[date].volume < 1.1 * stock[date].index(-4).volume\
    or stock[date].volume < 1.1 * stock[date].index(-5).volume ) \
    and stock[date].ma(15) > stock[date].index(-1).ma(15):
    result[name].append(code)
