import calendar
import threading
from datetime import date

from utils import liveUtils, Utils, Constants


def getOppTransaction(transactionType):
    return "sell" if transactionType == "buy" else "buy"


class LEG:

    def __init__(self, type, transactionType, strategyNo):
        self.type = type
        self.transactionType = transactionType
        self.Strike = None
        self.exp_date = Utils.parameters[strategyNo]["expDate"]
        self.symbol = None
        self.premium = None
        self.currentAdjustmentLevel = 0
        self.realizedProfit = 0
        self.shift = Utils.parameters[strategyNo]["strikeDifference"] if type == "CE" else -Utils.parameters[strategyNo]["strikeDifference"]
        self.hedge = None
        self.strategyNo = strategyNo

    def setStrike(self, premiumTarget, atm, priceDict):
        """
        fetches the strike which has premium closest to premium target.
        """
        Constants.logger.info(
            "strategy_" + str(self.strategyNo) + " - " + "fetching strike for {} side with premium {}".format(self.type,
                                                                                                              premiumTarget))
        intialStrike = atm if atm else int(self.Strike)
        newStrike = intialStrike
        while abs(intialStrike - newStrike) <= 8000:
            symbol = self.getShonyaSymbol(str(newStrike))
            premium = 0
            try:
                premium = priceDict[symbol] if symbol in priceDict else liveUtils.getQuote(symbol, self.getSymbol(str(newStrike)), priceDict, self.strategyNo)
            except Exception as e:
                Constants.logger.error(e)
            if premium < premiumTarget:
                self.premium = premium
                Constants.logger.info(
                    "strategy_" + str(self.strategyNo) + " - " + "{} fetched with premium {}".format(symbol, premium))
                self.setLegPars(symbol, priceDict)
                return symbol
            newStrike = newStrike + self.shift

    def setLegPars(self, symbol, priceDict):
        if self.symbol:
            liveUtils.placeOrder(self.getShonyaSymbol(), self.getSymbol(), getOppTransaction(self.transactionType),
                                 priceDict[self.symbol], self.strategyNo)
        self.Strike = symbol[-5:] if self.getPar("index") not in ["SENSEX", "BANKEX"] else symbol[-7:-2]
        if self.transactionType == "sell" and not self.symbol:
            self.setHedge(self.getPar("hedgeDist"), priceDict)
        self.symbol = symbol
        self.premium = priceDict[symbol] if symbol in priceDict else liveUtils.getQuote(symbol, self.getSymbol(), priceDict)
        liveUtils.placeOrder(self.getShonyaSymbol(), self.getSymbol(), self.transactionType, self.premium, self.strategyNo)
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " +
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
            Constants.logger.error("strategy_" + str(self.strategyNo) + " - " + "exception occurred while getting price from priceDict {}".format(e))
            return self.premium

    def flush(self):
        self.Strike = None
        self.exp_date = None
        self.premium = 0
        self.symbol = None
        self.currentAdjustmentLevel = 0
        self.realizedProfit = 0
        self.hedge = None

    def reExecute(self, priceDict):
        """
        when the current leg hits SL we do an adjustment in the leg to a farther strike
        :param priceDict:
        :return:
        """
        if self.getLegUnRealizedProfit(priceDict) <= - self.getPar("SLMap")[self.currentAdjustmentLevel] * self.premium:
            self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
            initialStrike = self.Strike
            Constants.logger.info("strategy_" + str(
                self.strategyNo) + " - " + self.type + " leg adjustment occured, initiating order placement")
            if self.currentAdjustmentLevel == self.getPar("noOfAdjustment"):
                threading.Thread(target=self.exit, args=(priceDict,)).start()
                self.currentAdjustmentLevel += 1
                # self.hedge.realizedProfit += self.hedge.getLegUnRealizedProfit(client)
                # self.hedge.premium = 0
                return int(initialStrike)
            else:
                self.setStrike(self.getPar("adjustmentPercent") * self.premium, None, priceDict)
                # self.setHedge(priceDict, 20, tokenData)
                self.currentAdjustmentLevel += 1
                return int(initialStrike)
        return 0

    def reEnter(self, straddleCentre, priceDict):
        """
        when the spot price comes back to the intial straddle or strangle price we do a reentry.
        :return:
        """
        if straddleCentre:
            Constants.logger.info(
                "strategy_" + str(self.strategyNo) + " - " + self.type + " leg rematch occured, initiating rematch ")
            self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
            symbol = self.getShonyaSymbol(str(straddleCentre))
            self.premium = 0
            self.setLegPars(symbol, priceDict)
            # self.setHedge(priceDict, 20, tokenData)
            self.currentAdjustmentLevel -= 1
            return 0

    def shiftIn(self, priceDict):
        shiftAmount = round(self.getPar("shiftAmount")*priceDict[self.getPar("index")]) * self.shift
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "shifting in initialized for " + self.type)
        self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
        symbol = self.getShonyaSymbol(str(int(self.Strike) - shiftAmount))
        self.setLegPars(symbol, priceDict)

    def setHedge(self, hedgeDist, priceDict):
        if not self.premium:
            return
        transactionType = "buy" if self.transactionType == "sell" else "sell"
        self.hedge = LEG(self.type, transactionType, self.strategyNo) if not self.hedge else self.hedge
        self.hedge.type = self.type
        self.hedge.exp_date = self.exp_date
        symbol = self.getShonyaSymbol(distFromStrike=hedgeDist)
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "moving hedge to distance {}".format(hedgeDist))
        self.hedge.realizedProfit += self.hedge.getLegUnRealizedProfit(priceDict)
        self.hedge.setLegPars(symbol, priceDict)

    def updatePremium(self, priceDict):
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "updating premium for " + self.symbol)
        self.realizedProfit += self.getLegUnRealizedProfit(priceDict)
        self.premium = priceDict[self.symbol]
        # if self.hedge:
        #     self.hedge.updatePremium(priceDict)

    def exit(self, priceDict):
        if not self.premium:
            return
        Constants.logger.info("strategy_" + str(self.strategyNo) + " - " + "exiting leg")
        liveUtils.placeOrder(self.getShonyaSymbol(), self.getSymbol(), getOppTransaction(self.transactionType),
                             priceDict[self.symbol], self.strategyNo)
        self.premium = 0
        if self.hedge:
            self.hedge.exit(priceDict)

    def getShonyaSymbol(self, strike=None, distFromStrike=None):
        if not strike:
            strike = self.Strike if not distFromStrike else str(int(self.Strike)+distFromStrike*self.shift)
        map = {"O": 10, "N": 11, "D": 12}
        if self.exp_date[2].isnumeric():
            m = int(self.exp_date[2]) if self.exp_date[2] not in map else map[self.exp_date[2]]
            expDate = self.exp_date[-2:] + calendar.month_abbr[m].upper() + self.exp_date[:2]
        else:
            expDate = str(date.today().day) + self.exp_date[-3:] + self.exp_date[:2]
        return self.getPar("index") + expDate + self.type[
            0] + strike if self.getPar("index") not in ["SENSEX", "BANKEX"] else self.getPar("index") + self.exp_date + strike + self.type

    def getSymbol(self, strike=None):
        if not strike:
            strike = self.Strike
        if Utils.isMonthly and self.getPar("isPositional"):
            return self.getPar("index") + self.getPar("expDate")[:2] + calendar.month_name[Constants.monthMap[int(self.getPar("expDate")[2])]][:3].upper() + strike + self.type
        return self.getPar("index") + self.exp_date + strike + self.type
    
    def getPar(self, parameter):
        return Utils.parameters[self.strategyNo][parameter]
