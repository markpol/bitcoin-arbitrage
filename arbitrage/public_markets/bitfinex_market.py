from .market import Market

class Bitfinex(Market):

    def __init__(self, **kwargs):
        super(Bitfinex, self).__init__(**kwargs)
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def update_depth(self):
        url = 'https://api.bitfinex.com/v1/book/%s' % self.get_currency_code_pair()
        self.depth = self.format_depth(self.send_update_depth_request(url))

    def get_currency_code_pair(self):
        return '%s%s' % (self.amount_currency.lower(),
                         self.price_currency.lower())

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x["price"]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i['price']),
                      'amount': float(i['amount'])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['bids'], True)
        asks = self.sort_and_format(depth['asks'], False)
        return {'asks': asks, 'bids': bids}


if __name__ == "__main__":
    market = Bitfinex()
    print(market.get_depth())
