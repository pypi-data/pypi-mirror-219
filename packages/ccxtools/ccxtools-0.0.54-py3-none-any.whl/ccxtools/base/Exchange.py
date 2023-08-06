from abc import ABCMeta, abstractmethod


class Exchange(metaclass=ABCMeta):

    @abstractmethod
    def get_balance(self, ticker):
        raise NotImplementedError

    @abstractmethod
    def post_market_order(self, ticker, side, open_close, amount):
        raise NotImplementedError
