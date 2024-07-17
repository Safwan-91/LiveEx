from core.Leg import LEG
from utils import Utils, liveUtils, Constants


class STRADDLE:
    def __init__(self, transactionType, strategyNo):
        self.strategyNo = strategyNo
        self.ce = LEG("CE", transactionType, strategyNo)
        self.pe = LEG("PE", transactionType, strategyNo)
        self.realizedProfit = 0
        self.strikeStack = []
        self.mean = []
        self.buy = True if transactionType == "buy" else False

    def getProfit(self, priceDict):
        return self.ce.getLegProfit(priceDict) + self.pe.getLegProfit(priceDict)

    def setupStraddle(self, index, priceDict):
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "setting up initial position at " + str(priceDict[index]))
        atm = (round(float(priceDict[index]) / self.getPar("strikeDifference")) * self.getPar("strikeDifference"))
        initialPremium = self.getPar("initialPremiumMultiplier")*priceDict[self.getPar("index")]
        liveUtils.execute_in_parallel([(self.ce.setStrike, (initialPremium, atm, priceDict)), (self.pe.setStrike, (initialPremium, atm, priceDict))])
        self.strikeStack = []
        self.mean.append(priceDict[index])

    def adjust(self, spot, priceDict):
        cestrike = self.ce.reExecute(priceDict) if self.pe.currentAdjustmentLevel == 0 else 0
        pestrike = self.pe.reExecute(priceDict) if self.ce.currentAdjustmentLevel == 0 else 0
        if cestrike:
            self.strikeStack.append(cestrike)
            self.mean.append(spot)
            if self.getPar("adjustmentShift") and self.ce.currentAdjustmentLevel == 2:
                self.pe.shiftIn(priceDict)
        elif pestrike:
            self.strikeStack.append(pestrike)
            self.mean.append(spot)
            if self.getPar("adjustmentShift") and self.pe.currentAdjustmentLevel == 2:
                self.ce.shiftIn(priceDict)

    def reEnter(self, spot, priceDict):
        if self.ce.currentAdjustmentLevel >= 1 and spot < self.mean[-2]:
            self.mean.pop()
            self.pe.updatePremium(priceDict)
            self.ce.reEnter(self.strikeStack.pop(), priceDict)
            Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "after rematch the premiums are, ce - {}, pe - {}".format(self.ce.premium, self.pe.premium))
        elif self.pe.currentAdjustmentLevel >= 1 and spot > self.mean[-2]:
            self.mean.pop()
            self.ce.updatePremium(priceDict)
            self.pe.reEnter(self.strikeStack.pop(), priceDict)
            Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "after rematch the premiums are, ce - {}, pe - {}".format(self.ce.premium, self.pe.premium))

    def exit(self, priceDict):
        profit = self.getProfit(priceDict)
        self.ce.exit(priceDict)
        self.pe.exit(priceDict)
        self.realizedProfit = 0
        self.strikeStack = 0
        return profit

    def setHedge(self, hedgeDist, priceDict):
        liveUtils.execute_in_parallel([(self.ce.setHedge, (hedgeDist, priceDict)), (self.pe.setHedge, (hedgeDist, priceDict))])

    def getAllSymbols(self):
        symbols = [self.ce.getShonyaSymbol(), self.pe.getShonyaSymbol()]
        if self.ce.hedge:
            symbols.append(self.ce.getShonyaSymbol(distFromStrike=6))
            symbols.append(self.ce.getShonyaSymbol(distFromStrike=20))
        if self.pe.hedge:
            symbols.append(self.pe.getShonyaSymbol(distFromStrike=6))
            symbols.append(self.pe.getShonyaSymbol(distFromStrike=20))
        return symbols

    def getPar(self, parameter):
        return Utils.parameters[self.strategyNo][parameter]
