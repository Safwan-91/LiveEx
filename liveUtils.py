import calendar
import threading
import time
from datetime import date

from Utils import executor

import Utils


def getQuote(symbol, stxoSymbol, client, priceDict):
    # return 20
    tryNo = 0
    while tryNo <= 5:
        try:
            client.IB_Subscribe(Utils.fnoExchange, stxoSymbol, "")
            if symbol not in priceDict["addons"]:
                priceDict["addons"].append(symbol)
            time.sleep(0.1)
            # Utils.logger.debug("strategy_"+str(self.strategyNo)+" - "+"fetching quote for {} for {}th try".format(symbol, tryNo))
            ltp = client.IB_LTP(Utils.fnoExchange, stxoSymbol, "")
            Utils.logger.debug("strategy_" + " - " + "quote fetched with ltp " + str(ltp))
            # OR Quotes API can be accessed without completing login by passing session_token, sid, and server_id
            if ltp == 0:
                Utils.logger.debug("strategy_" + " - " + "get quote attempt failed " + str(ltp))
                client.IB_Subscribe(Utils.fnoExchange, stxoSymbol, "")
                tryNo += 1
                time.sleep(0.5)
                continue
            return float(ltp)
        except Exception as e:
            Utils.logger.error("Exception when calling get Quote api->quotes: %s\n" % e)
            tryNo += 1
            time.sleep(1)
            if tryNo == 5:
                return e


def placeOrder(client, instrument_symbol, transaction_type, premium, strategyNo):
    Utils.logger.info("strategy_" + str(strategyNo) + " - " + "placing {} order for {} at {}".format(transaction_type,
                                                                                                     instrument_symbol,
                                                                                                     premium))
    return
    transaction_type = "LE" if transaction_type == "buy" else "SE"
    tryNo = 0
    orderID = None
    while tryNo < 5:
        orderID = client.IB_MappedOrderAdv(SignalID=0,
                                       StrategyTag=Utils.strategyTag[strategyNo],
                                       SourceSymbol=instrument_symbol,
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
        Utils.logger.debug("strategy_" + str(strategyNo) + " - " + "order placed with orderID {} and tryNo {}".format(orderID, tryNo))
        if orderID:
            break
        else:
            tryNo+=1

    while True:
        try:
            statuses = client.IB_OrderStatus(orderID)
            done = True
            for status in statuses.split(","):
                if status != "completed":
                    done = False
                    Utils.logger.warn("strategy_" + str(strategyNo) + " - " + "order not completed with status" + statuses)
                    time.sleep(0.05)
                    break
            if done:
                Utils.logger.info("strategy_" + str(strategyNo) + " - " + "order completed for all users")
                break
        except Exception as e:
            Utils.logger.error(e)
            time.sleep(1)
            continue
    # for user in users:
    #     user.order(instrument_token, instrument_symbol, transaction_type, premium, quantity)


def execute_in_parallel(func_list, *args):
    # Define a function to be executed in each thread
    def execute_func(func):
        return func(*args)

    results = []
    for func in func_list:
        thread = threading.Thread(target=execute_func, args=(func,))
        results.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in results:
        thread.join()


def getShonyaSymbol(strike, exp_date, type):

    map = {"O": 10, "N": 11, "D": 12}
    if exp_date[-1].isnumeric():
        m = int(exp_date[2]) if exp_date[2] not in map else map[exp_date[2]]
        expDate = exp_date[-2:] + calendar.month_abbr[m].upper() + exp_date[:2]
    else:
        expDate = str(date.today().day) + Utils.expDate[-3:] + Utils.expDate[:2]
    return Utils.index + expDate + type[
        0] + strike if Utils.index not in ["SENSEX","BANKEX"] else Utils.index + exp_date + strike + type