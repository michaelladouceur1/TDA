from utils import *
from tdapi import *
from btstrategies import *
import backtrader as bt 
import backtrader.feeds as btfeeds
import datetime

cerebro = bt.Cerebro()

c_init = 100000

cerebro.broker.set_cash(c_init)

print(f'Starting Portfolio Value: ${cerebro.broker.getvalue()}')

res = get_recent_data('MSFT','year',5,'daily',1)
res = timestamp_to_iso(res)
# res = sma(res,30,'close')
# res = sma(res,15,'close')
# print(res)
data = bt.feeds.PandasData(dataname=res, datetime=-1)

cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)

cerebro.run()

print(f'Final Portfolio Value: ${cerebro.broker.getvalue()}')
print(f'ROI: {((cerebro.broker.getvalue()/c_init)-1)*100}%')

cerebro.plot(iplot=False)