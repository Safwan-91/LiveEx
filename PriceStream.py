import Utils
from shonya import Shonya
from multiprocessing import Manager


class PriceStream:
    def __init__(self):
        self.api = Shonya(client_id='1').login()
        self.feedStarted = False
        self.expDate = Utils.expDate
        self.priceDict = Manager().dict(({}))

    def connect(self):
        def event_handler_feed_update(tick_data):
            print("in feed handler")
            print(tick_data)
            try:
                if not self.feedStarted:
                    self.priceDict[tick_data["ts"]] = float(tick_data["c"])
                    atm = int(round(float(tick_data["c"]) / 50) * 50)
                    l = []
                    for i in range(10):
                        symbolce = Utils.index + Utils.expDate + "C" + str(atm + i * Utils.strikeDifference)
                        symbolpe = Utils.index + Utils.expDate + "P" + str(atm - i * Utils.strikeDifference)
                        l.append('NFO|' + self.api.searchscrip("NFO", symbolce)["values"][0]["token"])
                        l.append('NFO|' + self.api.searchscrip("NFO", symbolpe)["values"][0]["token"])
                    self.feedStarted = True
                    self.api.subscribe(l)
                else:
                    self.priceDict[tick_data["ts"]] = float(tick_data["c"])
            except Exception as e:
                print(e)

        def open_callback():
            print("in open callback")
            self.api.subscribe('NSE|' + self.api.searchscrip(Utils.indexExchange, Utils.index)["values"][0]["token"])

        self.api.start_websocket(subscribe_callback=event_handler_feed_update, socket_open_callback=open_callback)
