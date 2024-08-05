import calendar
import pickle
import threading
import time
from datetime import date

from user.Users import users
from utils import Utils, Constants


def getQuote(symbol, stxoSymbol, priceDict, strategyNo):
    # return 20
    tryNo = 0
    while tryNo <= 5:
        try:
            users[0].client.IB_Subscribe(Utils.parameters[strategyNo]["fnoExchange"], stxoSymbol, "")
            if symbol not in priceDict["addons"]:
                priceDict["addons"].append(symbol)
            time.sleep(0.1)
            # Constants.logger.debug("strategy_"+str(self.strategyNo)+" - "+"fetching quote for {} for {}th try".format(symbol, tryNo))
            ltp = users[0].client.IB_LTP(Utils.parameters[strategyNo]["fnoExchange"], stxoSymbol, "")
            Constants.logger.debug("strategy_" + " - " + "quote fetched with ltp " + str(ltp))
            # OR Quotes API can be accessed without completing login by passing session_token, sid, and server_id
            if ltp == 0:
                Constants.logger.debug("strategy_" + " - " + "get quote attempt failed " + str(ltp))
                users[0].client.IB_Subscribe(Utils.parameters[strategyNo]["fnoExchange"], stxoSymbol, "")
                tryNo += 1
                time.sleep(0.5)
                continue
            return float(ltp)
        except Exception as e:
            Constants.logger.error("Exception when calling get Quote api->quotes: %s\n" % e)
            tryNo += 1
            time.sleep(1)
            if tryNo == 5:
                return e


def placeOrder(shonyaSymbol, instrument_symbol, transaction_type, premium, strategyNo):
    Constants.logger.info(
        "strategy_" + str(strategyNo) + " - " + "placing {} order for {} at {}".format(transaction_type,
                                                                                       instrument_symbol,
                                                                                       premium))
    task = [(user.placeAndConfirmOrder,
             (shonyaSymbol, instrument_symbol, transaction_type, premium, Utils.parameters[strategyNo]["lotSize"],
              strategyNo)) for user in users]
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


def getShonyaSymbol(index, strike, exp_date, type):
    map = {"O": 10, "N": 11, "D": 12}
    if exp_date[-1].isnumeric():
        m = int(exp_date[2]) if exp_date[2] not in map else map[exp_date[2]]
        expDate = exp_date[-2:] + calendar.month_abbr[m].upper() + exp_date[:2]
    else:
        expDate = str(date.today().day) + exp_date[-3:] + exp_date[:2]
    return index + expDate + type[
        0] + strike if index not in ["SENSEX", "BANKEX"] else index + exp_date + strike + type


def dumpObject(obj, name):
    fileObj = open(Constants.positionalObjectsPath + "\\" + name + '.obj', 'wb')
    pickle.dump(obj, fileObj)
    fileObj.close()


def loadObject(name):
    dbfile = open(Constants.positionalObjectsPath + "\\" + name, 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db
