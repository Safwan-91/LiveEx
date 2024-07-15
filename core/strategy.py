import time
from datetime import datetime

from core import Straddle
from utils import liveUtils, Utils, Constants


class Strategy:

    def __init__(self, transactionType, strategyNo):
        self.overNightHedge = False
        self.mtmhit = None
        self.strategyNo = strategyNo
        self.straddle = Straddle.STRADDLE(transactionType, strategyNo)
        self.rematchStack = []
        self.currentAdjustmentLevel = 0
        self.started = False
        self.isPositional = Utils.parameters[strategyNo]["isPositional"]

    def start(self, spot, priceDict, currentime):
        if self.started or currentime < Utils.startTime[self.strategyNo] or getDateDifference(getDateDifference(Utils.parameters[self.strategyNo]["expDate"]) > Utils.parameters[self.strategyNo]["expDate"]):
            if self.overNightHedge and self.isPositional and currentime >= "09:20:00":
                self.straddle.setHedge(20, priceDict)
                self.overNightHedge = False
            pass

        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade started")
        self.straddle.setupStraddle(spot, priceDict)
        Constants.logger.info(
            "strategy_" + str(self.strategyNo) + " - " + "straddle mean is " + str(self.straddle.mean))
        self.started = True
        time.sleep(2)

    def end(self, priceDict):
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade ended")
        # self.started = False
        return self.straddle.exit(priceDict)

    def piyushAdjustment(self, spot, currentTime, priceDict):
        if self.mtmhit or not self.started:
            return
        Constants.logger.info(
            "strategy_" + str(self.strategyNo) + " - " + "checking for piyush adjustment, spot is " + str(spot))
        if int(currentTime[3:5]) % 10 == 0:
            Constants.logger.info("strategy_" + str(self.strategyNo) + " - " +
                                  "mtm is {} ce premium is {}, pe premium is {}".format(
                                      round(self.straddle.getProfit(priceDict), 2),
                                      priceDict[self.straddle.ce.symbol],
                                      priceDict[self.straddle.pe.symbol]))
            Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "ce adjustment level - " + str(
                self.straddle.ce.currentAdjustmentLevel) + " pe adjustment level - " + str(
                self.straddle.pe.currentAdjustmentLevel))
        if Utils.oneSideFullHitFlag and (
                self.straddle.pe.currentAdjustmentLevel == Utils.noOfAdjustment + 1 or self.straddle.ce.currentAdjustmentLevel == Utils.noOfAdjustment + 1):
            return
        self.straddle.reEnter(spot, priceDict)
        self.straddle.adjust(spot, priceDict)
        Constants.logger.info("strategy_" + str(
            self.strategyNo) + " - " + "piyush adjustment check and adjustments if any done successfully")

    def checkmtmhit(self, priceDict):
        if self.mtmhit or (self.started and (
                self.straddle.getProfit(priceDict) < -Utils.mtmStopLoss)):
            if not self.mtmhit:
                self.mtmhit = (self.straddle.getProfit(priceDict))
                self.end(priceDict)
                Constants.logger.info(
                    "strategy_" + str(self.strategyNo) + " - " + "mtm hit for price " + str(self.mtmhit))

    def getMTM(self, priceDict):
        return round(self.straddle.getProfit(priceDict), 2)

    def buyHedge(self, priceDict):
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "buying Hedge")
        spot = priceDict[Utils.index]
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        symbolce = Utils.index + Utils.expDate + str(int(atm) + Utils.hedgeDist * Utils.strikeDifference) + "CE"
        symbolpe = Utils.index + Utils.expDate + str(int(atm) - Utils.hedgeDist * Utils.strikeDifference) + "PE"
        shonyaSymbolce = liveUtils.getShonyaSymbol(str(int(atm) + Utils.hedgeDist * Utils.strikeDifference),
                                                   Utils.expDate, "CE")
        shonyaSymbolpe = liveUtils.getShonyaSymbol(str(int(atm) - Utils.hedgeDist * Utils.strikeDifference),
                                                   Utils.expDate, "PE")
        liveUtils.placeOrder(shonyaSymbolce, symbolce, "buy", 0, self.strategyNo)
        liveUtils.placeOrder(shonyaSymbolpe, symbolpe, "buy", 0, self.strategyNo)
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "hedge bought successfully")

    def buyOverNightHedge(self, priceDict):
        self.straddle.setHedge(6, priceDict)
        self.overNightHedge = True


def getDateDifference(date):
    day = int(date[:2])
    year = int(date[3:])
    month = int(date[2:3])
    date_object = datetime(year, month, day)
    return (date_object - datetime.now()).days
