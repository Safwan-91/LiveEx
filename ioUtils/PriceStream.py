from utils import liveUtils, Utils, Constants
from user.shonya import Shonya


class PriceStream:
    def __init__(self):
        self.api = Shonya(client_id='def').login()
        self.feedStarted = False
        self.priceDict = {}
        self.tickSymbolMap = {}
        self.indexStrategyNoMap = {}
        self.subscribedOptionList = []
        self.priceDict["addons"] = []
        self.fetchAllIndices()

    def connect(self):
        def event_handler_feed_update(tick_data):
            print("in feed handler")
            print(tick_data)
            try:
                if tick_data["tk"] in self.indexStrategyNoMap.keys() and self.priceDict.get(Constants.tokenIndexMap[tick_data["tk"]], 0) == 0:
                    self.tickSymbolMap[tick_data["tk"]] = Constants.tokenIndexMap[tick_data["tk"]]
                    self.priceDict[self.tickSymbolMap[tick_data["tk"]]] = float(tick_data["lp"])
                    self.getOptionList(self.indexStrategyNoMap[tick_data["tk"]])
                    self.api.subscribe(self.subscribedOptionList)
                    Constants.logger.debug("all subscribed for {}".format(tick_data["ts"]))
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
            if self.subscribedOptionList:
                self.api.subscribe(self.subscribedOptionList)
                Constants.logger.debug("all subscribed")
            for indexNo in self.indexStrategyNoMap.values():
                self.api.subscribe(
                    Utils.parameters[indexNo]["indexExchange"] + '|' + Constants.indexTokenMap[
                        Utils.parameters[indexNo]["index"]])

        self.api.start_websocket(subscribe_callback=event_handler_feed_update, socket_open_callback=open_callback)

    def getOptionList(self, strategyNo):
        atm = round(float(self.priceDict[Utils.parameters[strategyNo]["index"]]) / Utils.parameters[strategyNo]["strikeDifference"]) * Utils.parameters[strategyNo]["strikeDifference"]
        for i in range(-5, 25):
            symbolce = liveUtils.getShonyaSymbol(Utils.parameters[strategyNo]["index"], str(atm + i * Utils.parameters[strategyNo]["strikeDifference"]),
                                                 Utils.parameters[strategyNo]["expDate"], "CE")
            symbolpe = liveUtils.getShonyaSymbol(Utils.parameters[strategyNo]["index"], str(atm - i * Utils.parameters[strategyNo]["strikeDifference"]),
                                                 Utils.parameters[strategyNo]["expDate"], "PE")
            tokence = self.api.searchscrip(Utils.parameters[strategyNo]["fnoExchange"], symbolce)["values"][0][
                "token"]
            tokenpe = self.api.searchscrip(Utils.parameters[strategyNo]["fnoExchange"], symbolpe)["values"][0][
                "token"]
            self.subscribedOptionList.append(Utils.parameters[strategyNo]["fnoExchange"] + '|' + tokence)
            self.subscribedOptionList.append(Utils.parameters[strategyNo]["fnoExchange"] + '|' + tokenpe)
            self.tickSymbolMap[tokence] = symbolce
            self.tickSymbolMap[tokenpe] = symbolpe

    def fetchAllIndices(self):
        for i, strategy in enumerate(Utils.parameters):
            self.indexStrategyNoMap[Constants.indexTokenMap[Utils.parameters[i]["index"]]] = i
