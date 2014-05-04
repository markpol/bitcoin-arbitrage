from .market import Market

class Kraken(Market):
    CODES = {
        'USD': 'ZUSD',
        'EUR': 'ZEUR',
        'BTC': 'XXBT',
        'LTC': 'XLTC',
        'DOGE': 'XXDG'
    }

    INVERT_PRICE_CODES = (
       #'XXBTXLTC'
    )

    def __init__(self, **kwargs):
        super(Kraken, self).__init__(**kwargs)
        self.update_rate = 30

    def update_depth(self):
        url = 'https://api.kraken.com/0/public/Depth'
        params = {'pair': self.get_currency_code_pair()}
        self.depth = self.format_depth(self.send_update_depth_request(url,params=params))

    def get_currency_code_pair(self):
        return '%s%s' % (self.CODES[self.amount_currency],
                         self.CODES[self.price_currency])

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x[0]), reverse=reverse)
        r = []
        for i in l:
            if False: #self.code in self.INVERT_PRICE_CODES:
                price = 1/float(i[0])
                amount = float(i[1]) * float(i[0])
            else:
                price = float(i[0])
                amount = float(i[1])
            r.append({'price': price, 'amount': amount})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['result'][self.get_currency_code_pair()]['bids'], True)
        asks = self.sort_and_format(depth['result'][self.get_currency_code_pair()]['asks'], False)
        if False: #self.code in self.INVERT_PRICE_CODES:
            # flip asks and bids (because we inverted price)
            return {'asks': bids, 'bids': asks}
        else:
            return {'asks': asks, 'bids': bids}
