#volume['0']/volume['-1']>2
if stock[date][code].volume and \
   stock[date][code].index(-1).volume and \
   stock[date][code].volume > 2 * stock.index(-1).volume:
    result[name].append(code)
