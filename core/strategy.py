import os
import time
from datetime import datetime

from core import Straddle
from utils import liveUtils, Utils, Constants


class Strategy:

    def __init__(self, transactionType, strategyNo):
        self.index = Utils.parameters[strategyNo]["index"]
        self.overNightHedge = False
        self.mtmhit = None
        self.strategyNo = strategyNo
        self.straddle = Straddle.STRADDLE(transactionType, strategyNo)
        self.rematchStack = []
        self.currentAdjustmentLevel = 0
        self.started = False
        self.isPositional = Utils.parameters[strategyNo]["isPositional"]

    def start(self, priceDict, currentime):
        if self.started or currentime < self.getPar("startTime") or (getDateDifference(self.getPar("expDate")) != self.getPar("daysBeforeExpiry")):
            if self.overNightHedge and self.isPositional and "09:20:00" <= currentime <= Constants.positionalEndTime:
                self.straddle.setHedge(self.getPar("hedgeDist"), priceDict)
                self.overNightHedge = False
            return

        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade started")
        self.straddle.setupStraddle(self.index, priceDict)
        Constants.logger.info(
            "strategy_" + str(self.strategyNo) + " - " + "straddle mean is " + str(self.straddle.mean))
        self.started = True
        time.sleep(2)

    def end(self, priceDict):
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade ended")
        # self.started = False
        return self.straddle.exit(priceDict)

    def piyushAdjustment(self, currentTime, priceDict):
        if self.mtmhit or not self.started or self.checkHedgedStrategyMTMjump(priceDict):
            return
        Constants.logger.info(
            "strategy_" + str(self.strategyNo) + " - " + "checking for piyush adjustment, spot is " + str(priceDict[self.index]))
        if int(currentTime[3:5]) % 10 == 0:
            Constants.logger.info("strategy_" + str(self.strategyNo) + " - " +
                                  "mtm is {} ce premium is {}, pe premium is {}".format(
                                      round(self.straddle.getProfit(priceDict), 2),
                                      priceDict[self.straddle.ce.symbol],
                                      priceDict[self.straddle.pe.symbol]))
            Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "ce adjustment level - " + str(
                self.straddle.ce.currentAdjustmentLevel) + " pe adjustment level - " + str(
                self.straddle.pe.currentAdjustmentLevel))
        if self.getPar("oneSideFullHitFlag") and (
                self.straddle.pe.currentAdjustmentLevel == self.getPar("noOfAdjustment") + 1 or self.straddle.ce.currentAdjustmentLevel == self.getPar("noOfAdjustment") + 1):
            return
        self.straddle.reEnter(priceDict[self.index], priceDict)
        self.straddle.adjust(priceDict[self.index], priceDict)
        Constants.logger.info("strategy_" + str(
            self.strategyNo) + " - " + "piyush adjustment check and adjustments if any done successfully")

    def checkmtmhit(self, priceDict):
        if self.mtmhit or (self.started and (
                self.straddle.getProfit(priceDict) < -self.getPar("mtmStopLoss") * priceDict[self.getPar("index")])):
            if not self.mtmhit and not self.checkHedgedStrategyMTMjump(priceDict):
                self.mtmhit = (self.straddle.getProfit(priceDict))
                self.end(priceDict)
                Constants.logger.info(
                    "strategy_" + str(self.strategyNo) + " - " + "mtm hit for price " + str(self.mtmhit))

    def getMTM(self, priceDict):
        return round(self.straddle.getProfit(priceDict), 2)

    def buyHedge(self, priceDict):
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "buying Hedge")
        spot = priceDict[self.getPar("index")]
        atm = (round(float(spot) / self.getPar("strikeDifference")) * self.getPar("strikeDifference"))
        symbolce = self.getPar("index") + self.getPar("expDate") + str(int(atm) + self.getPar("hedgeDist") * self.getPar("strikeDifference")) + "CE"
        symbolpe = self.getPar("index") + self.getPar("expDate") + str(int(atm) - self.getPar("hedgeDist") * self.getPar("strikeDifference")) + "PE"
        shonyaSymbolce = liveUtils.getShonyaSymbol(self.getPar("index"), str(int(atm) + self.getPar("hedgeDist") * self.getPar("strikeDifference")),
                                                   self.getPar("expDate"), "CE")
        shonyaSymbolpe = liveUtils.getShonyaSymbol(self.getPar("index"), str(int(atm) - self.getPar("hedgeDist") * self.getPar("strikeDifference")),
                                                   self.getPar("expDate"), "PE")
        liveUtils.placeOrder(shonyaSymbolce, symbolce, "buy", 0, self.strategyNo)
        liveUtils.placeOrder(shonyaSymbolpe, symbolpe, "buy", 0, self.strategyNo)
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "hedge bought successfully")

    def buyOverNightHedge(self, priceDict):
        if datetime.now().strftime("%d") == self.getPar("expDate")[-2:]:
            os.remove(Constants.positionalObjectsPath + "\\" + "strategy_" + str(self.strategyNo))
            return
        if not self.started or not self.getPar("isPositional") or self.getPar("hedgeDist") == self.getPar("overNightHedgeDist"):
            return
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "buying overnight hedge")
        self.straddle.setHedge(self.getPar("overNightHedgeDist"), priceDict)
        self.overNightHedge = True
        
    def getPar(self, parameter):
        return Utils.parameters[self.strategyNo][parameter]

    def checkHedgedStrategyMTMjump(self, priceDict):
        return self.getPar("hedgeDist") <= 4 and self.straddle.getProfit(priceDict) < -(self.getPar("mtmStopLoss") + 0.0005) * priceDict[self.getPar("index")]


def getDateDifference(date):
    year = int("20"+date[:2])
    day = int(date[3:])
    month = int(date[2:3])
    date_object = datetime(year, month, day)
    return (date_object - datetime.now()).days + 1
