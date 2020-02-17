import backtrader as bt
import backtrader.indicators as btind
from btutils import sma

class MyStrategy(bt.Strategy):

    params = dict(
        pfast = 15,
        pslow = 45
    )

    def log(self,txt,dt=None):
        print(f'{self.dt}: {txt}')

    def __init__(self):
        self.cash_start = self.broker.get_cash()
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.open = self.datas[0].open
    
    def start(self):
        self.buy(size=(int(self.broker.get_cash()/self.data)))

    def next(self):
        # if not self.position:  # not in the market
        if self.crossover > 0:  # if fast crosses slow to the upside
            self.buy(size=(int(self.broker.get_cash()/self.data)))  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.sell(size=(int(self.broker.get_value()/self.data)*0.5))  # close long position
        # print(len(self))
        # print(self.order)
        # print(self.position)
        # print('\n')
        # if self.sma_15 > self.sma_30:
        #     self.log('BUY')
        #     self.buy(size=10)

        # else:
        #     # Do something else
        #     self.log('SELL')
        #     self.sell()

    def stop(self):
        # calculate the actual returns
        self.roi = ((self.broker.get_value() / self.cash_start) - 1.0)*100
        print('ROI:        {:.2f}%'.format(self.roi))


class BuyAndHold_More(bt.Strategy):
    params = dict(
        monthly_cash=1000.0,  # amount of cash to buy every month
    )

    def start(self):
        self.cash_start = self.broker.get_cash()
        self.val_start = 100.0

        # Add a timer which will be called on the 1st trading day of the month
        self.add_timer(
            bt.timer.SESSION_END,  # when it will be called
            monthdays=[1],  # called on the 1st day of the month
            monthcarry=True,  # called on the 2nd day if the 1st is holiday
        )

    def notify_timer(self, timer, when, *args, **kwargs):
        # Add the influx of monthly cash to the broker
        self.broker.add_cash(self.p.monthly_cash)

        # buy available cash
        target_value = self.broker.get_value() + self.p.monthly_cash
        self.order_target_value(target=target_value)

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.cash_start) - 1.0
        print('ROI:        {:.2f}%'.format(self.roi))