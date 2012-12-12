#price['0']/price['-15']>1.15
result[code][name] = stock[date][code].max(15) > stock.index(-15).close * 1.15
