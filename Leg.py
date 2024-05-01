from datetime import datetime

import Utils
import liveUtils
from Utils import *


def getOppTransaction(transactionType):
    return "sell" if transactionType == "buy" else "buy"


class LEG:

    def __init__(self, type, transactionType):
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

    def setStrike(self, premiumTarget, atm, client):
        """
        fetches the strike which has premium closest to premium target.
        """
        Utils.logger.info("fetching strike for {} side with premium {}".format(self.type, premiumTarget))
        intialStrike = atm if atm else int(self.Strike)
        newStrike = intialStrike
        while abs(intialStrike - newStrike) <= 8000:
            symbol = index + self.exp_date + str(newStrike) + self.type
            premium = 0
            try:
                premium = liveUtils.getQuote(symbol, client)
            except Exception as e:
                Utils.logger.error(e)
            if premium < premiumTarget:
                self.premium = premium
                Utils.logger.info("{} fetched with premium {}".format(symbol, premium))
                self.setLegPars(symbol,client)
                return symbol
            newStrike = newStrike + self.shift

    def setLegPars(self, symbol, client):
        self.Strike = symbol[-7:-2]
        # if self.transactionType == "sell" and not self.symbol:
        #     self.setHedge(20, tokenData, client, users)
        self.symbol = symbol
        self.premium = liveUtils.getQuote(self.symbol, client)
        liveUtils.placeOrder(client, self.symbol, self.transactionType, self.premium)
        Utils.logger.info(self.type + " parameters set with strike {} and premium {}".format(self.Strike, self.premium), )

    def getLegProfit(self, client):
        if self.hedge:
            return self.realizedProfit + self.getLegUnRealizedProfit(client) + self.hedge.getLegProfit(client)
        else:
            return self.realizedProfit + self.getLegUnRealizedProfit(client)

    def getLegUnRealizedProfit(self, client):
        try:
            if self.premium and self.transactionType == "sell":
                return self.premium - liveUtils.getQuote(self.symbol, client)
            elif self.premium and self.transactionType == "buy":
                return liveUtils.getQuote(self.symbol, client) - self.premium
            else:
                return 0
        except Exception as e:
            Utils.logger.info("exception occurred", e)
            return self.premium

    def flush(self):
        self.Strike = None
        self.exp_date = None
        self.premium = 0
        self.symbol = None
        self.currentAdjustmentLevel = 0
        self.realizedProfit = 0
        self.hedge = None

    def reExecute(self, client):
        """
        when the current leg hits SL we do an adjustment in the leg to a farther strike
        :param client:
        :param priceDict:
        :param tokenData:
        :return:
        """
        if self.getLegUnRealizedProfit(client) < - SLMap[self.currentAdjustmentLevel] * self.premium:
            self.realizedProfit += self.getLegUnRealizedProfit(client)
            initialStrike = self.Strike
            Utils.logger.info(self.type + " leg adjustment at ", datetime.now())
            if self.currentAdjustmentLevel == Utils.noOfAdjustment:
                self.exit(client)
                self.premium = 0
                self.currentAdjustmentLevel += 1
                # self.hedge.realizedProfit += self.hedge.getLegUnRealizedProfit(client)
                # self.hedge.premium = 0
                return int(initialStrike)
            else:
                liveUtils.placeOrder(client, self.symbol, getOppTransaction(self.transactionType),
                                     liveUtils.getQuote(self.symbol, client))
                self.setStrike(adjustmentPercent * self.premium, None, client)
                # self.setHedge(priceDict, 20, tokenData)
                self.currentAdjustmentLevel += 1
                return int(initialStrike)
        return 0

    def reEnter(self, straddleCentre, client):
        """
        when the spot price comes back to the intial straddle or strangle price we do a reentry.
        :return:
        """
        if straddleCentre:
            Utils.logger.info(self.type + " leg rematch at ", datetime.now())
            self.realizedProfit += self.getLegUnRealizedProfit(client)
            liveUtils.placeOrder(client, self.symbol, getOppTransaction(self.transactionType),
                                     liveUtils.getQuote(self.symbol, client))
            symbol = index + self.exp_date + str(straddleCentre) + self.type
            self.premium = 0
            self.setLegPars(symbol, client)
            # self.setHedge(priceDict, 20, tokenData)
            self.currentAdjustmentLevel -= 1
            return 0

    def shiftIn(self, client):
        Utils.logger.info("shifting in ", self.type)
        self.realizedProfit += self.getLegUnRealizedProfit(client)
        liveUtils.placeOrder(client, self.symbol, getOppTransaction(self.transactionType),
                             liveUtils.getQuote(self.symbol, client))
        symbol = Utils.index + self.exp_date + str(int(self.Strike) - Utils.shiftAmount * self.shift) + self.type
        self.setLegPars(symbol, client)

    def setHedge(self, hedgeDist, tokenData, client, users):
        transactionType = "buy" if self.transactionType == "sell" else "sell"
        self.hedge = LEG(self.type, transactionType) if not self.hedge else self.hedge
        self.hedge.type = self.type
        self.hedge.exp_date = self.exp_date
        if hedgeDist > 10:
            hedgestrike = str(round((int(self.Strike) + hedgeDist * self.shift) / 100) * 100)
        else:
            hedgestrike = str(int(self.Strike) + hedgeDist * self.shift)
        symbol = index + self.exp_date + hedgestrike + self.type
        Utils.logger.info("hedge", end=" ")
        self.hedge.setLegPars(symbol, client)

    def updatePremium(self, client):
        self.realizedProfit += self.getLegUnRealizedProfit(client)
        self.premium = liveUtils.getQuote(self.symbol, client)
        if self.hedge:
            self.hedge.updatePremium(client)

    def exit(self, client):
        if not self.premium:
            return
        Utils.logger.info("exiting leg")
        liveUtils.placeOrder(client, self.symbol, getOppTransaction(self.transactionType), liveUtils.getQuote(self.symbol, client))
        if self.hedge:
            self.hedge.exit(client)
