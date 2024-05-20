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
                    self.tickSymbolMap[tick_data["tk"]] = Utils.index
                    self.priceDict["addons"] = []
                    self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["lp"])
                    atm = int(round(float(tick_data["lp"]) / Utils.strikeDifference) * Utils.strikeDifference)
                    l = []
                    for i in range(10):
                        symbolce = liveUtils.getShonyaSymbol(str(atm + i * Utils.strikeDifference), Utils.expDate, "CE")
                        symbolpe = liveUtils.getShonyaSymbol(str(atm - i * Utils.strikeDifference), Utils.expDate, "PE")
                        tokence = self.api.searchscrip(Utils.fnoExchange, symbolce)["values"][0]["token"]
                        tokenpe = self.api.searchscrip(Utils.fnoExchange, symbolpe)["values"][0]["token"]
                        l.append(Utils.fnoExchange + '|' + tokence)
                        l.append(Utils.fnoExchange + '|' + tokenpe)
                        self.tickSymbolMap[tokence] = symbolce
                        self.tickSymbolMap[tokenpe] = symbolpe
                    self.feedStarted = True
                    self.api.subscribe(l)
                    print("all subscribed")
                else:
                    self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(
                        tick_data["lp"]) if "lp" in tick_data else float(tick_data["bp1"])
                while len(self.priceDict["addons"]) != 0:
                    token = self.api.searchscrip(Utils.fnoExchange, self.priceDict["addons"].pop())["values"][0][
                        "token"]
                    self.api.subscribe(Utils.fnoExchange + '|' + token)
            except Exception as e:
                pass
                # print("in exception")
                # print(e)

        def open_callback():
            print("in open callback")
            self.api.subscribe(
                Utils.indexExchange + '|' + Utils.indexToken)

        self.api.start_websocket(subscribe_callback=event_handler_feed_update, socket_open_callback=open_callback)
