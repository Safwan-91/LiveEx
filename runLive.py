import time
import Utils
from strategy import Strategy
import liveUtils


class Live:
    def __init__(self, strategyNo):
        self.strategyNo = strategyNo
        self.mtmhit = None
        self.expDate = Utils.expDate
        self.strategy = Strategy("sell", strategyNo)
        self.hedge = False

    def callback_method(self, client, currentime, priceDict):
        if not self.hedge and currentime[:5] >= Utils.startTime[self.strategyNo][:5]:
            time.sleep(3)
            self.buyHedge(priceDict)
            self.hedge = True
            if currentime[:5] == Utils.startTime[self.strategyNo][:5]:
                return
        Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"New minute formed, executing computation")
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "the current min closes are" + str(priceDict))
        if not self.strategy.started:
            self.strategy.start(client, priceDict[Utils.indexToken],
                                self.expDate, priceDict)
        # elif currentTime >= "15:29:00":
        #     self.strategy.end(client)
        elif self.mtmhit or (self.strategy.started and (
                self.strategy.straddle.getProfit(priceDict) < -Utils.mtmStopLoss)):
            if not self.mtmhit:
                self.mtmhit = (self.strategy.straddle.getProfit(priceDict))
                self.strategy.end(client, priceDict)
                Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"mtm hit for price " + str(self.mtmhit))
            return
        elif self.strategy.started:
            self.strategy.piyushAdjustment(priceDict[Utils.indexToken], client, currentime, priceDict)
        # self.subscribeAllTokens(client)

    def subscribeAllTokens(self, client):
        Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"subscribing tokens")
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
        Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"all tokens subscribed")

    def buyHedge(self, priceDict):
        Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"buying Hedge")
        spot = priceDict[Utils.indexToken]
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        symbolce = Utils.index + self.expDate + str(int(atm) + 20 * Utils.strikeDifference) + "CE"
        symbolpe = Utils.index + self.expDate + str(int(atm) - 20 * Utils.strikeDifference) + "PE"
        # liveUtils.placeOrder(client, symbolce, "buy", 0)
        # liveUtils.placeOrder(client, symbolpe, "buy", 0)
        Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"hedge bought successfully")
