#由于当日买入股票不能卖出，因此1日上涨%1的算法为当日最高价减去昨日收盘价
result[code][name] = stock[date][code].high > stock.index(-1).close * 1.01
