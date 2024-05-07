import time

import Utils
from strategy import Strategy
import liveUtils


class Live:
    def __init__(self):
        self.mtmhit = None
        self.expDate = Utils.expDate
        self.strategy = Strategy("sell")
        self.hedge = False

    def callback_method(self, client, currentime):
        if not self.hedge and currentime[:5] >= Utils.startTime[:5]:
            self.subscribeAllTokens(client)
            time.sleep(10)
            self.buyHedge(client)
            self.hedge = True
            if currentime[:5] == Utils.startTime[:5]:
                return
        Utils.logger.info("New minute formed, executing computation")
        if not self.strategy.started:
            self.strategy.start(client, client.IB_LTP(Utils.indexExchange, Utils.indexToken, ""),
                                self.expDate)
        # elif currentTime >= "15:29:00":
        #     self.strategy.end(client)
        elif self.mtmhit or (self.strategy.started and (
                self.strategy.straddle.getProfit(client) < -Utils.mtmStopLoss)):
            if not self.mtmhit:
                self.mtmhit = (self.strategy.straddle.getProfit(client))
                self.strategy.end(client)
                Utils.logger.info("mtm hit for price " + str(self.mtmhit))
            return
        elif self.strategy.started:
            self.strategy.piyushAdjustment(client.IB_LTP(Utils.indexExchange, Utils.indexToken, ""), client, currentime)
        self.subscribeAllTokens(client)

    def subscribeAllTokens(self, client):
        Utils.logger.info("subscribing tokens")
        client.IB_Subscribe(Utils.indexExchange, Utils.indexToken, "")
        atm = (round(float(client.IB_LTP(Utils.indexExchange, Utils.indexToken, "")) / Utils.strikeDifference) * Utils.strikeDifference) if not self.strategy.started else None
        for i in range(10):
            if atm:
                symbolce = Utils.index + self.expDate + str(int(atm) + i * Utils.strikeDifference) + "CE"
                symbolpe = Utils.index + self.expDate + str(int(atm) - i * Utils.strikeDifference) + "PE"
            else:
                symbolce = Utils.index + self.expDate + str(int(self.strategy.straddle.ce.Strike) + i * Utils.strikeDifference) + "CE"
                symbolpe = Utils.index + self.expDate + str(int(self.strategy.straddle.pe.Strike) - i * Utils.strikeDifference) + "PE"
            client.IB_Subscribe(Utils.fnoExchange, symbolce, "")
            client.IB_Subscribe(Utils.fnoExchange, symbolpe, "")
        Utils.logger.info("all tokens subscribed")

    def buyHedge(self, client):
        Utils.logger.info("buying Hedge")
        spot = client.IB_LTP(Utils.indexExchange, Utils.indexToken, "")
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        symbolce = Utils.index + self.expDate + str(int(atm) + 20 * Utils.strikeDifference) + "CE"
        symbolpe = Utils.index + self.expDate + str(int(atm) - 20 * Utils.strikeDifference) + "PE"
        liveUtils.placeOrder(client, symbolce, "buy", 0)
        liveUtils.placeOrder(client, symbolpe, "buy", 0)
        Utils.logger.info("hedge bought successfully")
