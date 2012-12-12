#price['0']/price['-10']>1.1
result[code][name] = stock[date][code].max(10) > stock.index(-10).close * 1.1
