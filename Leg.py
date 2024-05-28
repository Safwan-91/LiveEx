import calendar
import threading

import Utils
import liveUtils
from Utils import *


def getOppTransaction(transactionType):
    return "sell" if transactionType == "buy" else "buy"


class LEG:

    def __init__(self, type, transactionType, strategyNo):
        self.type = type
        self.transactionType = transactionType
        self.Strike = None
        self.exp_date = None
        self.symbol = None
        self.premium = None
        self.currentAdjustmentLevel = 0
        self.realizedProfit = 0
        self.shift = strikeDifference if type == "CE" else -strikeDifference
        self.hedge = None
        self.strategyNo = strategyNo

    def setStrike(self, premiumTarget, atm, client, priceDict):
        """
        fetches the strike which has premium closest to premium target.
        """
        Utils.logger.info(
            "strategy_" + str(self.strategyNo) + " - " + "fetching strike for {} side with premium {}".format(self.type,
                                                                                                              premiumTarget))
        intialStrike = atm if atm else int(self.Strike)
        newStrike = intialStrike
        while abs(intialStrike - newStrike) <= 8000:
            symbol = self.getShonyaSymbol(str(newStrike))
            premium = 0
            try:
                premium = priceDict[symbol] if symbol in priceDict else liveUtils.getQuote(symbol, self.getSymbol(str(newStrike)), client, priceDict)
            except Exception as e:
                Utils.logger.error(e)
            if premium < premiumTarget:
                self.premium = premium
                Utils.logger.info(
                    "strategy_" + str(self.strategyNo) + " - " + "{} fetched with premium {}".format(symbol, premium))
                self.setLegPars(symbol, client, priceDict)
                return symbol
            newStrike = newStrike + self.shift

    def setLegPars(self, symbol, client, priceDict):
        self.Strike = symbol[-5:] if Utils.index not in ["SENSEX", "BANKEX"] else symbol[-7:-2]
        # if self.transactionType == "sell" and not self.symbol:
        #     self.setHedge(20, tokenData, client, users)
        self.symbol = symbol
        self.premium = priceDict[symbol] if symbol in priceDict else liveUtils.getQuote(symbol, self.getSymbol(), client, priceDict)
        liveUtils.placeOrder(client, self.getSymbol(), self.transactionType, self.premium, self.strategyNo)
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " +
                          self.type + " parameters set with strike {} and premium {}".format(self.Strike,
                                                                                             self.premium), )

    def getLegProfit(self, priceDict):
        if self.hedge:
            return self.realizedProfit + self.getLegUnRealizedProfit(priceDict) + self.hedge.getLegProfit(priceDict)
        else:
            return self.realizedProfit + self.getLegUnRealizedProfit(priceDict)

    def getLegUnRealizedProfit(self, priceDict):
        try:
            if self.premium and self.transactionType == "sell":
                return self.premium - priceDict[self.getShonyaSymbol()]
            elif self.premium and self.transactionType == "buy":
                return priceDict[self.getShonyaSymbol()] - self.premium
            else:
                return 0
        except Exception as e:
            Utils.logger.error("strategy_" + str(self.strategyNo) + " - " + "exception occurred {}".format(e))
            return self.premium

    def flush(self):
        self.Strike = None
        self.exp_date = None
        self.premium = 0
        self.symbol = None
        self.currentAdjustmentLevel = 0
        self.realizedProfit = 0
        self.hedge = None

    def reExecute(self, client, priceDict):
        """
        when the current leg hits SL we do an adjustment in the leg to a farther strike
        :param client:
        :param priceDict:
        :param tokenData:
        :return:
        """
        if self.getLegUnRealizedProfit(priceDict) < - SLMap[self.currentAdjustmentLevel][self.strategyNo] * self.premium:
            self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
            initialStrike = self.Strike
            Utils.logger.info("strategy_" + str(
                self.strategyNo) + " - " + self.type + " leg adjustment occured, initiating order placement")
            if self.currentAdjustmentLevel == Utils.noOfAdjustment:
                threading.Thread(target=self.exit, args=(client, priceDict)).start()
                self.premium = 0
                self.currentAdjustmentLevel += 1
                # self.hedge.realizedProfit += self.hedge.getLegUnRealizedProfit(client)
                # self.hedge.premium = 0
                return int(initialStrike)
            else:
                liveUtils.placeOrder(client, self.getSymbol(), getOppTransaction(self.transactionType),
                                     priceDict[self.symbol], self.strategyNo)
                self.setStrike(adjustmentPercent * self.premium, None, client, priceDict)
                # self.setHedge(priceDict, 20, tokenData)
                self.currentAdjustmentLevel += 1
                return int(initialStrike)
        return 0

    def reEnter(self, straddleCentre, client, priceDict):
        """
        when the spot price comes back to the intial straddle or strangle price we do a reentry.
        :return:
        """
        if straddleCentre:
            Utils.logger.info(
                "strategy_" + str(self.strategyNo) + " - " + self.type + " leg rematch occured, initiating rematch ")
            self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
            liveUtils.placeOrder(client, self.getSymbol(), getOppTransaction(self.transactionType),
                                 priceDict[self.symbol], self.strategyNo)
            symbol = self.getShonyaSymbol(str(straddleCentre))
            self.premium = 0
            self.setLegPars(symbol, client, priceDict)
            # self.setHedge(priceDict, 20, tokenData)
            self.currentAdjustmentLevel -= 1
            return 0

    def shiftIn(self, client, priceDict):
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "shifting in initialized for " + self.type)
        self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
        liveUtils.placeOrder(client, self.getSymbol(), getOppTransaction(self.transactionType),
                             priceDict[self.symbol], self.strategyNo)
        symbol = self.getShonyaSymbol(str(int(self.Strike) - Utils.shiftAmount * self.shift))
        self.setLegPars(symbol, client, priceDict)

    def setHedge(self, hedgeDist, client):
        transactionType = "buy" if self.transactionType == "sell" else "sell"
        self.hedge = LEG(self.type, transactionType) if not self.hedge else self.hedge
        self.hedge.type = self.type
        self.hedge.exp_date = self.exp_date
        if hedgeDist > 10:
            hedgestrike = str(round((int(self.Strike) + hedgeDist * self.shift) / 100) * 100)
        else:
            hedgestrike = str(int(self.Strike) + hedgeDist * self.shift)
        symbol = index + self.exp_date + hedgestrike + self.type
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "hedge", end=" ")
        self.hedge.setLegPars(symbol, client)

    def updatePremium(self, priceDict):
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "updating premium for " + self.symbol)
        self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
        self.premium = priceDict[self.symbol]
        if self.hedge:
            self.hedge.updatePremium(priceDict)

    def exit(self, client, priceDict):
        if not self.premium:
            return
        Utils.logger.info("strategy_" + str(self.strategyNo) + " - " + "exiting leg")
        liveUtils.placeOrder(client, self.getSymbol(), getOppTransaction(self.transactionType),
                             priceDict[self.symbol], self.strategyNo)
        if self.hedge:
            self.hedge.exit(client, priceDict)

    def getShonyaSymbol(self, strike=None):
        if not strike:
            strike = self.Strike
        map = {"O": 10, "N": 11, "D": 12}
        if self.exp_date[2].isnumeric():
            m = int(self.exp_date[2]) if self.exp_date[2] not in map else map[self.exp_date[2]]
            expDate = self.exp_date[-2:] + calendar.month_abbr[m].upper() + self.exp_date[:2]
        else:
            expDate = "28MAY24"
        return Utils.index + expDate + self.type[
            0] + strike if Utils.index not in ["SENSEX","BANKEX"] else Utils.index + self.exp_date + strike + self.type

    def getSymbol(self, strike=None):
        if not strike:
            strike = self.Strike
        return Utils.index + self.exp_date + strike + self.type
