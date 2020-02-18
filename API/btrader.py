from utils import timestamp_to_iso
from tdapi import get_recent_data
from btstrategies import *
import backtrader as bt 
import datetime
import pandas as pd

cerebro = bt.Cerebro()

c_init = 100000

cerebro.broker.set_cash(c_init)

print(f'Starting Portfolio Value: ${cerebro.broker.getvalue()}')

res1 = get_recent_data('SPY','year',5,'daily',1)
res1 = timestamp_to_iso(res1)
res2 = get_recent_data('FNV','year',1,'daily',1)
res2 = timestamp_to_iso(res2)

data1 = bt.feeds.PandasData(dataname=res1, datetime=-1)
cerebro.adddata(data1,name='data1')

# data2 = bt.feeds.PandasData(dataname=res2, datetime=-1)
# data2.plotinfo.plotmaster = data1
# cerebro.adddata(data2,name='data2')

# cerebro.addstrategy(BuyAndHold)
cerebro.addstrategy(OverUnder)

# cerebro.addsizer(bt.sizers.FixedSize)

cerebro.run()

print(f'Final Portfolio Value: ${cerebro.broker.getvalue()}')
print(f'ROI: {((cerebro.broker.getvalue()/c_init)-1)*100}%')

cerebro.plot(iplot=False)