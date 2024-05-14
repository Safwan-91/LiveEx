import Straddle
import Utils
import liveUtils


class Strategy:

    def __init__(self, transactionType, strategyNo):
        self.strategyNo = strategyNo
        self.straddle = Straddle.STRADDLE(transactionType, strategyNo)
        self.mtm = 0
        self.rematchStack = []
        self.shift = 200
        self.currentAdjustmentLevel = 0
        self.noOfAdjustments = 1
        self.hedgeStrategyDirection = None
        self.started = False

    def start(self, client, spot, expDate, priceDict):
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade started")
        self.straddle.setupStraddle(spot, client, expDate, priceDict)
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "straddle mean is " + str(self.straddle.mean))
        # self.straddle.ce.setHedge(priceDict, 20, self.tokenData)
        # self.straddle.pe.setHedge(priceDict, 20, self.tokenData)
        # self.hedgeAdjustment(spot, priceDict)
        self.started = True

    def end(self, client, priceDict):
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "trade ended")
        self.started = False
        return self.straddle.exit(client, priceDict)

    def piyushAdjustment(self, spot, client, currentTime, priceDict):
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
        self.straddle.reEnter(spot, client, priceDict)
        self.straddle.adjust(spot, client, priceDict)
        Utils.logger.info("strategy_" + str(
            self.strategyNo) + " - " + "piyush adjustment check and adjustments if any done successfully")

    def getMTM(self, priceDict):
        return round(self.straddle.getProfit(priceDict), 2)
