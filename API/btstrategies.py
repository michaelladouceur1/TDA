import backtrader as bt
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

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=30)
        self.ama = bt.indicators.RelativeStrengthIndex()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        print('ama:', self.ama[0])
        if self.order:
            return

        if not self.position:
            if (self.ama[0] > 70):
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy(size=500)

        else:
            if (self.ama[0] < 70):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell(size=500)