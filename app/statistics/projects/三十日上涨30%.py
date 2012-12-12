#price['0']/price['-30']>1.3
result[code][name] = stock[date][code].max(30) > stock.index(-30).close * 1.3
