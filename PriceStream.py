import Utils
import liveUtils
from shonya import Shonya
from multiprocessing import Manager


class PriceStream:
    def __init__(self):
        self.api = Shonya(client_id='1').login()
        self.feedStarted = False
        self.expDate = Utils.expDate
        self.priceDict = Manager().dict(({}))
        self.tickSymbolMap = {}

    def connect(self):
        def event_handler_feed_update(tick_data):
            # print("in feed handler")
            # print(tick_data)
            try:

                if not self.feedStarted:
                    self.tickSymbolMap[tick_data["tk"]] = Utils.indexToken
                    self.priceDict["addons"] = []
                    self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["lp"])
                    atm = int(round(float(tick_data["lp"]) / 50) * 50)
                    l = []
                    for i in range(10):
                        symbolce = Utils.index + liveUtils.getShonyaExp(Utils.expDate) + "C" + str(atm + i * Utils.strikeDifference)
                        symbolpe = Utils.index + liveUtils.getShonyaExp(Utils.expDate) + "P" + str(atm - i * Utils.strikeDifference)
                        tokence = self.api.searchscrip("NFO", symbolce)["values"][0]["token"]
                        tokenpe = self.api.searchscrip("NFO", symbolpe)["values"][0]["token"]
                        l.append('NFO|' + tokence)
                        l.append('NFO|' + tokenpe)
                        self.tickSymbolMap[tokence] = symbolce
                        self.tickSymbolMap[tokenpe] = symbolpe
                    self.feedStarted = True
                    self.api.subscribe(l)
                    print("all subscribed")
                else:
                    self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(
                        tick_data["lp"]) if "lp" in tick_data else float(tick_data["bp1"])
                while len(self.priceDict["addons"]) != 0:
                    token = self.api.searchscrip("NFO", self.priceDict["addons"].pop())["values"][0]["token"]
                    self.api.subscribe('NFO|' + token)
            except Exception as e:
                pass
                # print("in exception")
                # print(e)

        def open_callback():
            print("in open callback")
            self.api.subscribe('NSE|' + self.api.searchscrip(Utils.indexExchange, Utils.index)["values"][0]["token"])

        self.api.start_websocket(subscribe_callback=event_handler_feed_update, socket_open_callback=open_callback)
