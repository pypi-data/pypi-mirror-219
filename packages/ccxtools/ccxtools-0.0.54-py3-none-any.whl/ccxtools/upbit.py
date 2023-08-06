import ccxt
from ccxtools.base.CcxtExchange import CcxtExchange


class Upbit(CcxtExchange):

    def __init__(self, who, _market, config):
        super().__init__()
        self.ccxt_inst = ccxt.upbit({
            'apiKey': config(f'UPBIT_API_KEY{who}'),
            'secret': config(f'UPBIT_SECRET_KEY{who}')
        })

    def get_last_price(self, ticker):
        res = self.ccxt_inst.fetch_ticker(f'{ticker}/KRW')
        return res['last']

    def get_best_book_price(self, ticker, side):
        res = self.ccxt_inst.fetch_order_book(f'KRW-{ticker}')
        from pprint import pprint
        pprint(res)

    def post_market_order(self, ticker, side, open_close, amount):
        raise NotImplementedError
