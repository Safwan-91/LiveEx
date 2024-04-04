import calendar
import time
from datetime import datetime, timedelta

import Utils
import userDetails
from strategy import Strategy
import liveUtils


def formatDate(date):
    return date[-2:] + calendar.month_abbr[int(date[-5:-3])].upper() + date[2:4]


def getTokenDataDateFromat(date):
    map = {10: "O", 11: "N", 12: "D"}
    mid = map[date[5:7]] if date[5:7] in map else date[6:7]
    return date[2:4] + mid + date[-2:]


def getExpDate(tokenData):
    expDates = []
    if Utils.index == "CRUDEOIL":
        return "24FEB"
    elif Utils.index == "NIFTY":
        expDates = tokenData["symbol"][tokenData.instrumentName.str.startswith("NIFTY")].str[5:10].unique()
    elif Utils.index == "BANKNIFTY":
        expDates = tokenData["symbol"][tokenData.instrumentName.str.startswith("BANKNIFTY")].str[9:14].unique()
    elif Utils.index == "SENSEX":
        expDates = tokenData["symbol"][tokenData.symbol.str.startswith("SENSEX24")].str[6:11].unique()
    elif Utils.index == "FINNIFTY":
        expDates = tokenData["symbol"][tokenData.symbol.str.startswith("FINNIFTY")].str[8:13].unique()
    elif Utils.index == "MIDCPNIFTY":
        expDates = tokenData["symbol"][tokenData.symbol.str.startswith("MIDCPNIFTY")].str[10:15].unique()
    elif Utils.index == "BANKEX":
        expDates = tokenData["symbol"][tokenData.symbol.str.startswith("BANKEX")].str[6:11].unique()
    else:
        pass
    for i in range(7):
        date = getTokenDataDateFromat((datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"))
        if date in expDates:
            return date
    return datetime.now().strftime("%Y-%m-%d")[2:4] + calendar.month_abbr[
        int(datetime.now().strftime("%Y-%m-%d")[5:7])].upper()


def getQuote(client, tokens):
    inst_tokens = [{"instrument_token": str(Utils.indexToken), "exchange_segment": "nse_cm"}]
    for el in tokens:
        inst_tokens.append({"instrument_token": el, "exchange_segment": "nse_fo"})
    noOfTry = 0
    while noOfTry <= 5:
        # get LTP and Market Depth Data
        try:
            print("time before main quote call " + str(datetime.now()) + " try no ", noOfTry)
            ltp = client.quotes(instrument_tokens=inst_tokens, quote_type="ltp", isIndex=False)["message"]
            print("time after main quote call " + str(datetime.now()))
            if type(ltp) is not list:
                print(ltp)
                noOfTry += 1
                time.sleep(1)
                continue
            return ltp
        except Exception as e:
            print("Exception when calling get Quote api->quotes: %s\n" % e)
            noOfTry += 1
            time.sleep(1)


def getAllUsers():
    userList = []
    return userList


class Live:
    def __init__(self, indexToken, client):
        self.users = getAllUsers()
        self.mtmhit = None
        self.tokenData = liveUtils.loadTokenData()
        self.price = {}
        self.indexToken = str(indexToken)
        self.expDate = getExpDate(self.tokenData)
        self.currentDate = formatDate(datetime.now().strftime("%Y-%m-%d"))
        self.strategy = Strategy("sell")
        self.strategy.tokenData = self.tokenData
        self.hedge = False

    def callback_method(self, client):
        self.subscribeAllTokens(client)
        if not self.hedge and datetime.now().strftime("%H:%M") >= "09:44":
            time.sleep(10)
            self.buyHedge(client)
            self.hedge = True
            if datetime.now().strftime("%H:%M") == "09:44":
                return
        if not self.strategy.started and datetime.now().strftime("%H:%M:%S") >= "00:00:00":
            self.strategy.start(client, client.IB_LTP(Utils.indexExchange, Utils.indexToken, ""), self.users, self.expDate)
        elif self.currentDate == self.expDate and datetime.now().strftime("%H:%M:%S") >= "15:29:00":
            self.strategy.end(client, self.users)
        elif self.mtmhit or (self.strategy.started and (
                self.strategy.straddle.getProfit(client) < -Utils.mtmStopLoss)):
            if not self.mtmhit:
                self.mtmhit = (self.strategy.straddle.getProfit(client))
                self.strategy.end(client, self.users)
                print("mtm hit at " + datetime.now().strftime("%H:%M:%S") + " for ", self.mtmhit)
            return
        elif self.strategy.started:
            self.strategy.piyushAdjustment(client.IB_LTP(Utils.indexExchange, Utils.indexToken, ""), client, self.users)

    def subscribeAllTokens(self, client):
        client.IB_Subscribe(Utils.indexExchange, Utils.indexToken, "")
        spot = client.IB_LTP(Utils.indexExchange, Utils.indexToken, "")
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        for i in range(10):
            symbolce = Utils.index + self.expDate + str(int(atm) + i * Utils.strikeDifference) + "CE"
            symbolpe = Utils.index + self.expDate + str(int(atm) - i * Utils.strikeDifference) + "PE"
            client.IB_Subscribe(Utils.fnoExchange, symbolce, "")
            client.IB_Subscribe(Utils.fnoExchange, symbolpe, "")

    def buyHedge(self, client):
        spot = client.IB_LTP(Utils.indexExchange, Utils.indexToken, "")
        atm = (round(float(spot) / Utils.strikeDifference) * Utils.strikeDifference)
        symbolce = Utils.index + self.expDate + str(int(atm) + 20 * Utils.strikeDifference) + "CE"
        symbolpe = Utils.index + self.expDate + str(int(atm) - 20 * Utils.strikeDifference) + "PE"
        liveUtils.placeOrder(client, symbolce, symbolce, "buy", 0, 1)
        liveUtils.placeOrder(client, symbolpe, symbolpe, "buy", 0, 1)