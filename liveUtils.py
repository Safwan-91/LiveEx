import pickle
import time
from datetime import datetime
from urllib.request import urlopen
import time as tm

import pandas as pd

import Utils


def getQuote(symbol, client):
    tryNo = 0
    while tryNo <= 5:
        try:
            # print("time before quote call " + str(datetime.now()) + " try no ", tryNo)
            ltp = client.IB_LTP(Utils.fnoExchange, symbol, "")
            # print("time after quote call ", datetime.now())
            # OR Quotes API can be accessed without completing login by passing session_token, sid, and server_id
            if ltp == 0:
                print("get quote attempt failed ", ltp)
                client.IB_Subscribe(Utils.fnoExchange, symbol, "")
                tryNo += 1
                time.sleep(0.5)
                continue
            return float(ltp)
        except Exception as e:
            print("Exception when calling get Quote api->quotes: %s\n" % e)
            tryNo += 1
            time.sleep(1)
            if tryNo == 5:
                return e


def loadTokenData():
    url = "https://lapi.kotaksecurities.com/wso2-scripmaster/v1/prod/" + datetime.now().strftime('%Y-%m-%d') + "/transformed/"+Utils.indexExchange.lower()+"_fo.csv"
    response = urlopen(url)
    inst = pd.read_csv(response, sep=",")
    column_mapping = {'pSymbolName': 'instrumentName', 'pTrdSymbol': 'symbol', 'pSymbol': 'token'}
    inst.rename(columns=column_mapping, inplace=True)
    inst["expiry"] = inst.symbol.str[9:14]
    return inst


def dump(obj, name):
    fileObj = open(name + '.obj', 'wb')
    pickle.dump(obj, fileObj)
    fileObj.close()


def load(name):
    dbfile = open(name + '.obj', 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db


def placeOrder(client, instrument_token, instrument_symbol, transaction_type, premium, quantity):
    print("time before order call " + str(datetime.now()))
    transaction_type = "LE" if transaction_type == "buy" else "SE"
    orderID = client.IB_MappedOrderAdv(SignalID=0,
                               StrategyTag="OPTIONSPLAYPYSAF",
                               SourceSymbol=instrument_token,
                               TransactionType=transaction_type,
                               OrderType="MARKET",
                               ProductType="NRML",
                               Price="",
                               TriggerPrice="",
                               Quantity=Utils.lotSize,
                               ProfitValue="",
                               StoplossValue="",
                               SLTrailingValue="",
                               SignalLTP=0,
                               OptionsType="")
    while (client.IB_IsOrderCompleted(orderID))!="true":
        continue
    print(transaction_type + " : " + str(instrument_token) + " at " + str(premium))
    print("time before order call " + str(datetime.now()))
    # for user in users:
    #     user.order(instrument_token, instrument_symbol, transaction_type, premium, quantity)
