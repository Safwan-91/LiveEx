import time

from core import Straddle
from utils import liveUtils, Utils


class Strategy:

    def __init__(self, transactionType, strategyNo):
        self.hedge = False
        self.mtmhit = None
        self.strategyNo = strategyNo
        self.straddle = Straddle.STRADDLE(transactionType, strategyNo)
        self.rematchStack = []
        self.currentAdjustmentLevel = 0
        self.started = False

    def start(self, spot, priceDict, currentime):
        if self.started or currentime < Utils.startTime[self.strategyNo]:
            return

        if not self.hedge and currentime >= Utils.startTime[self.strategyNo]:
            self.buyHedge(priceDict)
            time.sleep(2)
            self.hedge = True
            if currentime[:5] == Utils.startTime[self.strategyNo][:5]:
                return

        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade started")
        self.straddle.setupStraddle(spot, priceDict)
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "straddle mean is " + str(self.straddle.mean))
        self.started = True
        time.sleep(2)

    def end(self, priceDict):
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade ended")
        # self.started = False
        return self.straddle.exit(priceDict)

    def piyushAdjustment(self, spot, currentTime, priceDict):
        if self.mtmhit or not self.started:
            return
        Utils.logger.info(
            "strategy_" + str(self.strategyNo) + " - " + "checking for piyush adjustment, spot is " + str(spot))
        if int(currentTime[3:5]) % 10 == 0:
            Utils.logger.info("strategy_" + str(self.strategyNo) + " - " +
                              "mtm is {} ce premium is {}, pe premium is {}".format(
                                  round(self.straddle.getProfit(priceDict), 2),
                                  priceDict[self.straddle.ce.symbol],
                                  priceDict[self.straddle.pe.symbol]))
            Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "ce adjustment level - " + str(
                self.straddle.ce.currentAdjustmentLevel) + " pe adjustment level - " + str(
                self.straddle.pe.currentAdjustmentLevel))
        if Utils.oneSideFullHitFlag and (
                self.straddle.pe.currentAdjustmentLevel == Utils.noOfAdjustment + 1 or self.straddle.ce.currentAdjustmentLevel == Utils.noOfAdjustment + 1):
            return
        self.straddle.reEnter(spot, priceDict)
        self.straddle.adjust(spot, priceDict)
        Utils.logger.info("strategy_" + str(
            self.strategyNo) + " - " + "piyush adjustment check and adjustments if any done successfully")

    def checkmtmhit(self, priceDict):
        if self.mtmhit or (self.started and (
                self.straddle.getProfit(priceDict) < -Utils.mtmStopLoss)):
            if not self.mtmhit:
                self.mtmhit = (self.straddle.getProfit(priceDict))
                self.end(priceDict)
                Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "mtm hit for price " + str(self.mtmhit))

    def getMTM(self, priceDict):
        return round(self.straddle.getProfit(priceDict), 2)

    def buyHedge(self, priceDict):
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "buying Hedge")
        spot = priceDict[Utils.index]
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        symbolce = Utils.index + Utils.expDate + str(int(atm) + Utils.hedgeDist * Utils.strikeDifference) + "CE"
        symbolpe = Utils.index + Utils.expDate + str(int(atm) - Utils.hedgeDist * Utils.strikeDifference) + "PE"
        liveUtils.placeOrder(symbolce, "buy", 0, self.strategyNo)
        liveUtils.placeOrder(symbolpe, "buy", 0, self.strategyNo)
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "hedge bought successfully")
