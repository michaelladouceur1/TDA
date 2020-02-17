from utils import *
from tdapi import *
from btstrategies import *
import backtrader as bt 
import backtrader.feeds as btfeeds
import datetime

cerebro = bt.Cerebro()

cerebro.broker.set_cash(100000)

print(f'Starting Portfolio Value: ${cerebro.broker.getvalue()}')

res = get_recent_data('QQQ','year',5,'daily',1)
res = timestamp_to_iso(res)
# res = sma(res,30,'close')
# res = sma(res,15,'close')
# print(res)
data = bt.feeds.PandasData(dataname=res, datetime=-1)

cerebro.adddata(data)

cerebro.addstrategy(MyStrategy)

cerebro.run()

cerebro.plot(iplot=False)

print(f'Final Portfolio Value: ${cerebro.broker.getvalue()}')