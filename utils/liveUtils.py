import calendar
import threading
import time
from datetime import date

from user.Users import users
from utils import Utils


def getQuote(symbol, stxoSymbol, priceDict):
    # return 20
    tryNo = 0
    while tryNo <= 5:
        try:
            users[0].client.IB_Subscribe(Utils.fnoExchange, stxoSymbol, "")
            if symbol not in priceDict["addons"]:
                priceDict["addons"].append(symbol)
            time.sleep(0.1)
            # Utils.logger.debug("strategy_"+str(self.strategyNo)+" - "+"fetching quote for {} for {}th try".format(symbol, tryNo))
            ltp = users[0].client.IB_LTP(Utils.fnoExchange, stxoSymbol, "")
            Utils.logger.debug("strategy_" + " - " + "quote fetched with ltp " + str(ltp))
            # OR Quotes API can be accessed without completing login by passing session_token, sid, and server_id
            if ltp == 0:
                Utils.logger.debug("strategy_" + " - " + "get quote attempt failed " + str(ltp))
                users[0].client.IB_Subscribe(Utils.fnoExchange, stxoSymbol, "")
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


def placeOrder(instrument_symbol, transaction_type, premium, strategyNo):
    Utils.logger.info("strategy_" + str(strategyNo) + " - " + "placing {} order for {} at {}".format(transaction_type,
                                                                                                     instrument_symbol,
                                                                                                     premium))
    task = [(user.placeAndConfirmOrder, ("", instrument_symbol, transaction_type, premium, Utils.lotSize, strategyNo)) for user in users]
    execute_in_parallel(task)


def execute_in_parallel(funcs_and_args):
    # Define a function to be executed in each thread
    def execute_func(func, args):
        return func(*args)

    results = []
    for func, args in funcs_and_args:
        thread = threading.Thread(target=execute_func, args=(func, args))
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
        0] + strike if Utils.index not in ["SENSEX", "BANKEX"] else Utils.index + exp_date + strike + type