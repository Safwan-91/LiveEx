from Leg import *


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

    def setupStraddle(self, spot, client, expDate, priceDict):
        Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"setting up initial position at " + str(spot))
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        self.ce.exp_date = expDate
        self.pe.exp_date = expDate
        liveUtils.execute_in_parallel([self.ce.setStrike, self.pe.setStrike], initialPremium, atm, client, priceDict)
        self.strikeStack = []
        self.mean.append(spot)

    def adjust(self, spot, client, priceDict):
        cestrike = self.ce.reExecute(client, priceDict) if self.pe.currentAdjustmentLevel == 0 else 0
        pestrike = self.pe.reExecute(client, priceDict) if self.ce.currentAdjustmentLevel == 0 else 0
        if cestrike:
            self.strikeStack.append(cestrike)
            self.mean.append(spot)
            if Utils.adjustmentShift and self.ce.currentAdjustmentLevel == 2:
                self.pe.shiftIn(client, priceDict)
        elif pestrike:
            self.strikeStack.append(pestrike)
            self.mean.append(spot)
            if Utils.adjustmentShift and self.pe.currentAdjustmentLevel == 2:
                self.ce.shiftIn(client, priceDict)

    def reEnter(self, spot, client, priceDict):
        if self.ce.currentAdjustmentLevel >= 1 and spot < self.mean[-2]:
            self.mean.pop()
            self.pe.updatePremium(priceDict)
            self.ce.reEnter(self.strikeStack.pop(), client, priceDict)
            Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"after rematch the premiums are, ce - {}, pe - {}".format(self.ce.premium, self.pe.premium))
        elif self.pe.currentAdjustmentLevel >= 1 and spot > self.mean[-2]:
            self.mean.pop()
            self.ce.updatePremium(priceDict)
            self.pe.reEnter(self.strikeStack.pop(), client, priceDict)
            Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"after rematch the premiums are, ce - {}, pe - {}".format(self.ce.premium, self.pe.premium))

    def exit(self, client, priceDict):
        profit = self.getProfit(priceDict)
        self.ce.exit(client, priceDict)
        self.pe.exit(client, priceDict)
        self.realizedProfit = 0
        self.strikeStack = 0
        return profit
