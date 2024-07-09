from utils import liveUtils, Utils
from user.shonya import Shonya


class PriceStream:
    def __init__(self):
        self.api = Shonya(client_id='def').login()
        self.feedStarted = False
        self.expDate = Utils.expDate
        self.priceDict = {}
        self.tickSymbolMap = {}
        self.l = []

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
                    for i in range(-5,15):
                        symbolce = liveUtils.getShonyaSymbol(str(atm + i * Utils.strikeDifference), Utils.expDate, "CE")
                        symbolpe = liveUtils.getShonyaSymbol(str(atm - i * Utils.strikeDifference), Utils.expDate, "PE")
                        tokence = self.api.searchscrip(Utils.fnoExchange, symbolce)["values"][0]["token"]
                        tokenpe = self.api.searchscrip(Utils.fnoExchange, symbolpe)["values"][0]["token"]
                        self.l.append(Utils.fnoExchange + '|' + tokence)
                        self.l.append(Utils.fnoExchange + '|' + tokenpe)
                        self.tickSymbolMap[tokence] = symbolce
                        self.tickSymbolMap[tokenpe] = symbolpe
                    self.feedStarted = True
                    self.api.subscribe(self.l)
                    Utils.logger.debug("all subscribed")
                else:
                    if "lp" in tick_data:
                        self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["lp"])
                    elif "bp1" in tick_data:
                        self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["bp1"])
                while len(self.priceDict["addons"]) != 0:
                    Utils.logger.debug("inside subscribing addons for " + self.priceDict["addons"][-1])
                    symbol = self.priceDict["addons"].pop()
                    token = self.api.searchscrip(Utils.fnoExchange, symbol)["values"][0][
                        "token"]
                    self.tickSymbolMap[token] = symbol
                    self.api.subscribe(Utils.fnoExchange + '|' + token)

            except Exception as e:
                Utils.logger.error("Exception in price feed - {}".format(e))

        def open_callback():
            Utils.logger.debug("in open callback")
            if self.l:
                self.api.subscribe(self.l)
                Utils.logger.debug("all subscribed")
            self.api.subscribe(
                Utils.indexExchange + '|' + Utils.indexToken)

        self.api.start_websocket(subscribe_callback=event_handler_feed_update, socket_open_callback=open_callback)