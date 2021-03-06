from .market import Market

class Btce(Market):

    def __init__(self, **kwargs):
        super(Btce, self).__init__(**kwargs)

    def update_depth(self):
        url = 'https://btc-e.com/api/2/%s/depth' % self.get_currency_code_pair()
        self.depth = self.format_depth(self.send_update_depth_request(url))

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x[0]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i[0]), 'amount': float(i[1])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['bids'], True)
        asks = self.sort_and_format(depth['asks'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == "__main__":
    market = Btce()
    print(market.get_ticker())
