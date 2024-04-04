import calendar
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
        self.premium = None
        self.token = None
        self.currentAdjustmentLevel = 0
        self.realizedProfit = 0
        self.noOfAdjustments = 1
        self.shift = strikeDifference if type == "CE" else -strikeDifference
        self.hedge = None

    def getStrike(self, premiumTarget, atm, tokenData, client):
        """
        fetches the strike which has premium closest to premium target.
        :param priceDict:
        :param premiumTarget: always less than self.premium.
        :param bankNiftyData:
        :param time:
        :return: symbol eg. BANKNIFTY29NOV40000CE
        """
        intialStrike = atm if atm else int(self.Strike)
        newStrike = intialStrike
        while abs(intialStrike - newStrike) <= 8000:
            symbol = index + self.exp_date + str(newStrike) + self.type
            premium = 0
            try:
                premium = liveUtils.getQuote(symbol, client)
            except Exception as e:
                print(e)
            if premium < premiumTarget:
                self.premium = premium
                return symbol
            newStrike = newStrike + self.shift

    def setLegPars(self, symbol, tokenData, client, users):
        self.Strike = symbol[-7:-2]
        # if self.transactionType == "sell" and not self.token:
        #     self.setHedge(20, tokenData, client, users)
        self.token = symbol
        if not self.premium:
            self.premium = liveUtils.getQuote(self.token, client)
        liveUtils.placeOrder(client, self.token, self.getSymbol(), self.transactionType, self.premium, 1)
        print(self.type + " parameters set with strike {} and premium {}".format(self.Strike, self.premium), )

    def getLegProfit(self, client):
        if self.hedge:
            return self.realizedProfit + self.getLegUnRealizedProfit(client) + self.hedge.getLegProfit(client)
        else:
            return self.realizedProfit + self.getLegUnRealizedProfit(client)

    def getLegUnRealizedProfit(self, client):
        try:
            if self.premium and self.transactionType == "sell":
                return self.premium - liveUtils.getQuote(self.token, client)
            elif self.premium and self.transactionType == "buy":
                return liveUtils.getQuote(self.token, client) - self.premium
            else:
                return 0
        except Exception as e:
            print("exception occurred", e)
            return self.premium

    def flush(self):
        self.Strike = None
        self.exp_date = None
        self.premium = 0
        self.token = None
        self.currentAdjustmentLevel = 0
        self.realizedProfit = 0
        self.hedge = None

    def reExecute(self, tokenData, client, users):
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
            print(self.type + " leg adjustment at ", datetime.now())
            if self.currentAdjustmentLevel == self.noOfAdjustments:
                self.exit(client, users)
                self.premium = 0
                self.currentAdjustmentLevel += 1
                # self.hedge.realizedProfit += self.hedge.getLegUnRealizedProfit(client)
                # self.hedge.premium = 0
                return int(initialStrike)
            else:
                liveUtils.placeOrder(client, self.token, self.getSymbol(), getOppTransaction(self.transactionType),
                                     liveUtils.getQuote(self.token, client), 1)
                symbol = self.getStrike(adjustmentPercent * self.premium, None, tokenData, client)
                self.setLegPars(symbol, tokenData, client, users)
                # self.setHedge(priceDict, 20, tokenData)
                self.currentAdjustmentLevel += 1
                return int(initialStrike)
        return 0

    def reEnter(self, straddleCentre, tokenData, client, users):
        """
        when the spot price comes back to the intial straddle or strangle price we do a reentry.
        :param time:
        :param straddleCentre:
        :param bankNiftyData:
        :return:
        """
        if straddleCentre:
            print(self.type + " leg rematch at ", datetime.now())
            self.realizedProfit += self.getLegUnRealizedProfit(client)
            liveUtils.placeOrder(client, self.token, self.getSymbol(), getOppTransaction(self.transactionType),
                                     liveUtils.getQuote(self.token, client), 1)
            symbol = index + self.exp_date + str(straddleCentre) + self.type
            self.premium = 0
            self.setLegPars(symbol, tokenData, client, users)
            # self.setHedge(priceDict, 20, tokenData)
            self.currentAdjustmentLevel -= 1
            return 0

    def shiftIn(self, client, tokenData, users):
        print("shifting in ", self.type)
        self.realizedProfit += self.getLegUnRealizedProfit(client)
        liveUtils.placeOrder(client, self.token, self.getSymbol(), getOppTransaction(self.transactionType),
                             liveUtils.getQuote(self.token, client), 1)
        symbol = Utils.index + self.exp_date + str(int(self.Strike) - Utils.shiftAmount * self.shift) + self.type
        self.setLegPars(symbol, tokenData, client, users)

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
        print("hedge", end=" ")
        self.hedge.setLegPars(symbol, tokenData, client, users)

    def updatePremium(self, client):
        self.realizedProfit += self.getLegUnRealizedProfit(client)
        self.premium = liveUtils.getQuote(self.token, client)
        if self.hedge:
            self.hedge.updatePremium(client)

    def exit(self, client, users):
        if not self.premium:
            return
        print("exiting leg")
        liveUtils.placeOrder(client, self.token, self.getSymbol(), getOppTransaction(self.transactionType), liveUtils.getQuote(self.token, client), 1)
        if self.hedge:
            self.hedge.exit(client, users)

    def getSymbol(self):
        map = {"O": 10, "N": 11, "D": 12}
        if self.exp_date[2].isnumeric():
            m = int(self.exp_date[2]) if self.exp_date[2] not in map else map[self.exp_date[2]]
            expDate = self.exp_date[-2:]+calendar.month_abbr[m].upper()+self.exp_date[:2]
        else:
            expDate = self.exp_date
        return Utils.index+expDate+self.type[0]+self.Strike if Utils.index != "SENSEX" else Utils.index+expDate+self.Strike+self.type
