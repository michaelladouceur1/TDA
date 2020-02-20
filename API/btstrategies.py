import backtrader as bt
from btutils import sma

class MyStrategy(bt.Strategy):

    params = dict(
        pfast = 2,
        pslow = 8
    )

    def log(self,txt,dt=None):
        print(f'{self.dt}: {txt}')

    def __init__(self):
        self.cash_start = self.broker.get_cash()
        sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.open = self.datas[0].open
        self.order = None
        self.prev = 'buy'
        # print(f'{type(sma1)}  {sma2}')

    def next(self):
        # if not self.position:  # not in the marke
        if not self.position and self.prev != 'sell':
            self.order = self.buy(size=(int(self.broker.get_cash()/self.data)))

        else:
            if self.crossover > 0.8 and self.prev == 'sell':  # if fast crosses slow to the upside
                self.order = self.buy(size=(int(self.broker.get_cash()/self.data)))  # enter long
                self.prev = 'buy'

            elif self.crossover < -0.8 and self.prev == 'buy':  # in the market & cross to the downside
                self.order = self.sell(size=(int(self.broker.get_value()/self.data)))  # close long position
                self.prev = 'sell'
    
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
            self.order = self.buy(size=((self.broker.get_cash()//self.data)))

    def stop(self):
        # calculate the actual returns
        self.roi = ((self.broker.get_value() / self.cash_start) - 1.0)*100
        print('ROI:        {:.2f}%'.format(self.roi))


class OverUnder(bt.Strategy):

    params = dict(
        pslow = 200,
        pfast = 30
    )

    def log(self,txt,dt=None):
        print(f'{self.dt}: {txt}')

    def __init__(self):
        self.cash_start = self.broker.get_cash()
        self.sma1 = bt.ind.EMA(period=self.p.pslow)  # fast moving average
        self.sma2 = bt.ind.EMA(period=self.p.pfast)
        self.roc = bt.ind.ROC(self.sma2,period=30)
        self.open = self.datas[0].open
        self.order = None
        self.uthresh = 0.025
        self.lthresh = 0.10
        self.size = 1
        self.prev = ''

    def prenext(self):
        if not self.position:
            self.order = self.buy(size=((self.broker.get_cash()//self.data.open)))

    def next(self):
        print(f'{self.datas[0].datetime[0]}:    {self.roc[0]}')
        # if not self.position:  # not in the marke
        


        if self.open/self.sma1 >= 1+self.uthresh and self.prev != 'sell' and self.roc < 0:
            self.order = self.sell(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'sell'

        elif self.sma2 > self.sma1 and self.prev != 'sell' and self.roc < -0.025:
            self.order = self.sell(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'sell'

        elif self.open/self.sma1 <= 1-self.lthresh and self.prev != 'buy':
            self.order = self.buy(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'buy'

        elif self.sma2 > self.sma1 and self.roc > 0:
            self.order = self.buy(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'buy'

    def stop(self):
        # calculate the actual returns
        self.roi = ((self.broker.get_value() / self.cash_start) - 1.0)*100
        print('ROI:        {:.2f}%'.format(self.roi))


class OverUnderShort(bt.Strategy):

    params = dict(
        pslow = 100,
        pfast = 20
    )

    def log(self,txt,dt=None):
        print(f'{self.dt}: {txt}')

    def __init__(self):
        self.cash_start = self.broker.get_cash()
        self.sma1 = bt.ind.EMA(period=self.p.pslow)  # fast moving average
        self.sma2 = bt.ind.EMA(period=self.p.pfast)
        self.roc = bt.ind.ROC(self.sma2,period=20)
        # self.rocr = bt.ind.ROC(self.roc,period=30)
        self.open = self.datas[0].open
        self.order = None
        self.uthresh = 0.0025
        self.lthresh = 0.0025
        self.size = 1
        self.prev = ''

    def prenext(self):
        if not self.position:
            self.order = self.buy(size=((self.broker.get_cash()//self.data.open)))

    def next(self):
        print(f'{self.datas[0].datetime[0]}:    {self.roc[0]}')
        # if not self.position:  # not in the marke
        


        if self.open/self.sma1 >= 1+self.uthresh and self.prev != 'sell' and self.roc < 0:
            self.order = self.sell(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'sell'

        elif self.sma2 > self.sma1 and self.prev != 'sell' and self.roc < -0.025:
            self.order = self.sell(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'sell'

        elif self.open/self.sma1 <= 1-self.lthresh and self.prev != 'buy':
            self.order = self.buy(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'buy'

        elif self.sma2 > self.sma1 and self.roc > 0:
            self.order = self.buy(size=(int(self.broker.get_value()/self.data.open)*self.size))
            self.prev = 'buy'

    def stop(self):
        # calculate the actual returns
        self.roi = ((self.broker.get_value() / self.cash_start) - 1.0)*100
        print('ROI:        {:.2f}%'.format(self.roi))