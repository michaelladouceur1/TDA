import backtrader as bt
import backtrader.indicators as btind
from btutils import sma

class MyStrategy(bt.Strategy):

    params = dict(
        pfast = 30,
        pslow = 45
    )

    def log(self,txt,dt=None):
        print(f'{self.dt}: {txt}')

    def __init__(self):
        self.cash_start = self.broker.get_cash()
        # sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        # self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.open = self.datas[0].open
        self.order = None
        self.prev = 'buy'
        deriv = Deriv(self.data)
        # print(f'{type(sma1)}  {sma2}')

    def next(self):
        # if not self.position:  # not in the marke
        if not self.position and self.prev != 'sell':
            self.order = self.buy(size=(int(self.broker.get_cash()/self.data)))

        # else:
        #     if self.crossover > 0.8 and self.prev == 'sell':  # if fast crosses slow to the upside
        #         self.order = self.buy(size=(int(self.broker.get_cash()/self.data)))  # enter long
        #         self.prev = 'buy'

        #     elif self.crossover < -0.8 and self.prev == 'buy':  # in the market & cross to the downside
        #         self.order = self.sell(size=(int(self.broker.get_value()/self.data)))  # close long position
        #         self.prev = 'sell'
    
    def stop(self):
        # calculate the actual returns
        self.roi = ((self.broker.get_value() / self.cash_start) - 1.0)*100
        print('ROI:        {:.2f}%'.format(self.roi))

class BuyAndHold(bt.Strategy):
    def log(self,txt,dt=None):
        print(f'{self.dt}: {txt}')

    def __init__(self):
        self.cash_start = self.broker.get_cash()
        self.order = None

    def next(self):
        # if not self.position:  # not in the marke
        if not self.position:
            self.order = self.buy(size=(int(self.broker.get_cash()/self.data)))

    def stop(self):
        # calculate the actual returns
        self.roi = ((self.broker.get_value() / self.cash_start) - 1.0)*100
        print('ROI:        {:.2f}%'.format(self.roi))