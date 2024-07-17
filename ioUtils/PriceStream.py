from utils import liveUtils, Utils, Constants
from user.shonya import Shonya


class PriceStream:
    def __init__(self):
        self.api = Shonya(client_id='def').login()
        self.feedStarted = False
        self.priceDict = {}
        self.tickSymbolMap = {}
        self.l = []

    def connect(self):
        def event_handler_feed_update(tick_data):
            # print("in feed handler")
            # print(tick_data)
            try:

                if not self.feedStarted:
                    self.tickSymbolMap[tick_data["tk"]] = Utils.parameters[0]["index"]
                    self.priceDict["addons"] = []
                    self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["lp"])
                    atm = int(round(float(tick_data["lp"]) / Utils.parameters[0]["strikeDifference"]) * Utils.parameters[0]["strikeDifference"])
                    for i in range(-2,25):
                        symbolce = liveUtils.getShonyaSymbol(str(atm + i * Utils.parameters[0]["strikeDifference"]), Utils.parameters[0]["expDate"], "CE")
                        symbolpe = liveUtils.getShonyaSymbol(str(atm - i * Utils.parameters[0]["strikeDifference"]), Utils.parameters[0]["expDate"], "PE")
                        tokence = self.api.searchscrip(Utils.parameters[0]["fnoExchange"], symbolce)["values"][0]["token"]
                        tokenpe = self.api.searchscrip(Utils.parameters[0]["fnoExchange"], symbolpe)["values"][0]["token"]
                        self.l.append(Utils.parameters[0]["fnoExchange"] + '|' + tokence)
                        self.l.append(Utils.parameters[0]["fnoExchange"] + '|' + tokenpe)
                        self.tickSymbolMap[tokence] = symbolce
                        self.tickSymbolMap[tokenpe] = symbolpe
                    self.feedStarted = True
                    self.api.subscribe(self.l)
                    Constants.logger.debug("all subscribed")
                else:
                    if "lp" in tick_data:
                        self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["lp"])
                    elif "bp1" in tick_data:
                        self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["bp1"])
                while len(self.priceDict["addons"]) != 0:
                    Constants.logger.debug("inside subscribing addons for " + self.priceDict["addons"][-1])
                    symbol = self.priceDict["addons"].pop()
                    token = self.api.searchscrip(Utils.parameters[0]["fnoExchange"], symbol)["values"][0][
                        "token"]
                    self.tickSymbolMap[token] = symbol
                    self.api.subscribe(Utils.parameters[0]["fnoExchange"] + '|' + token)

            except Exception as e:
                Constants.logger.error("Exception in price feed - {}".format(e))

        def open_callback():
            Constants.logger.debug("in open callback")
            if self.l:
                self.api.subscribe(self.l)
                Constants.logger.debug("all subscribed")
            self.api.subscribe(
                Utils.parameters[0]["indexExchange"] + '|' + Constants.indexTokenMap[Utils.parameters[0]["index"]])

        self.api.start_websocket(subscribe_callback=event_handler_feed_update, socket_open_callback=open_callback)
