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

    def getProfit(self, client):
        return self.ce.getLegProfit(client) + self.pe.getLegProfit(client)

    def setupStraddle(self, spot, client, expDate):
        Utils.logger.info("setting up initial position at " + str(spot))
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        self.ce.exp_date = expDate
        self.pe.exp_date = expDate
        liveUtils.execute_in_parallel([self.ce.setStrike, self.pe.setStrike], initialPremium, atm, client)
        self.strikeStack = []
        self.mean.append(spot)

    def adjust(self, spot, client):
        cestrike = self.ce.reExecute(client) if self.pe.currentAdjustmentLevel == 0 else 0
        pestrike = self.pe.reExecute(client) if self.ce.currentAdjustmentLevel == 0 else 0
        if cestrike:
            self.strikeStack.append(cestrike)
            self.mean.append(spot)
            if Utils.adjustmentShift and self.ce.currentAdjustmentLevel == 2:
                self.pe.shiftIn(client)
        elif pestrike:
            self.strikeStack.append(pestrike)
            self.mean.append(spot)
            if Utils.adjustmentShift and self.pe.currentAdjustmentLevel == 2:
                self.ce.shiftIn(client)

    def reEnter(self, spot, client):
        if self.ce.currentAdjustmentLevel >= 1 and spot < self.mean[-2]:
            self.mean.pop()
            self.pe.updatePremium(client)
            self.ce.reEnter(self.strikeStack.pop(), client)
            Utils.logger.info("after rematch the premiums are, ce - {}, pe - {}".format(self.ce.premium, self.pe.premium))
        elif self.pe.currentAdjustmentLevel >= 1 and spot > self.mean[-2]:
            self.mean.pop()
            self.ce.updatePremium(client)
            self.pe.reEnter(self.strikeStack.pop(), client)
            Utils.logger.info("after rematch the premiums are, ce - {}, pe - {}".format(self.ce.premium, self.pe.premium))

    def exit(self, client):
        profit = self.getProfit(client)
        self.ce.exit(client)
        self.pe.exit(client)
        self.realizedProfit = 0
        self.strikeStack = 0
        return profit
