import threading
import time
from Utils import executor

import Utils


def getQuote(symbol, client):
    return 20
    tryNo = 0
    while tryNo <= 5:
        try:
            Utils.logger.debug("strategy_"+str(self.strategyNo)+" - "+"fetching quote for {} for {}th try".format(symbol, tryNo))
            ltp = client.IB_LTP(Utils.fnoExchange, symbol, "")
            Utils.logger.debug("strategy_"+str(self.strategyNo)+" - "+"quote fetched with ltp " + str(ltp))
            # OR Quotes API can be accessed without completing login by passing session_token, sid, and server_id
            # if ltp == 0:
            #     Utils.logger.debug("strategy_"+str(self.strategyNo)+" - "+"get quote attempt failed "+ str(ltp))
            #     client.IB_Subscribe(Utils.fnoExchange, symbol, "")
            #     tryNo += 1
            #     time.sleep(0.5)
            #     continue
            return float(ltp)
        except Exception as e:
            Utils.logger.error("Exception when calling get Quote api->quotes: %s\n" % e)
            tryNo += 1
            time.sleep(1)
            if tryNo == 5:
                return e


def placeOrder(client, instrument_symbol, transaction_type, premium, stratrgyNo):
    Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"placing {} order for {} at {}".format(transaction_type, instrument_symbol, premium))
    return
    transaction_type = "LE" if transaction_type == "buy" else "SE"
    orderID = client.IB_MappedOrderAdv(SignalID=0,
                                       StrategyTag=Utils.strategyTag[stratrgyNo],
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
    Utils.logger.debug("strategy_"+str(self.strategyNo)+" - "+"order placed with orderID " + str(orderID))
    while True:
        try:
            statuses = client.IB_OrderStatus(orderID)
            done = True
            for status in statuses.split(","):
                if status != "completed":
                    done = False
                    Utils.logger.warn("order not completed with status" + statuses)
                    time.sleep(0.05)
                    break
            if done:
                Utils.logger.info("strategy_"+str(self.strategyNo)+" - "+"order completed for all users")
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
        # Pass parameters to sub_task
        results.append(executor.submit(execute_func, func))

    # Wait for all sub-tasks to complete
    for future in results:
        future.result()
    return results
