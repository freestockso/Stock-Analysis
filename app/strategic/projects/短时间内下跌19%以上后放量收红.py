#price['-4']/price['0']>1.19 or price['-3']/price['0']>1.19 or price['-2']/price['0']>1.19
#price['-1']/price['0']<1.11
#price['-2']/price['-1']<1.11
#price['-3']/price['-2']<1.11
#price['-4']/price['-3']<1.11
#短时间下跌超19%,今日放量收红,并过滤送股拆股的情况
if ((stock[date][code].close * 1.19 < stock.index('-4').close) or \
    (1.19 * stock[date].close < stock[date].index('-3').close) or \
    (1.19 * stock[date].close < stock[date].index('-2').close)) and \
    stock[date].change >0 and stock[date].index(-1).volume * 2 < stock[date].volume and \
    (stock[date].close > \
    0.89 * stock[date].index('-1').close > \
    0.89 ** 2 * stock[date].index('-2').close > \
    0.89 ** 3 * stock[date].index('-3').close > \
    0.89 ** 4 * stock[date].index('-4').close):
    result[name].append(code)
