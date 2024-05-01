import time
import asyncio

import Utils


def getQuote(symbol, client):
    tryNo = 0
    while tryNo <= 5:
        try:
            Utils.logger.info("fetching quote for {} for {}th try".format(symbol, tryNo))
            ltp = client.IB_LTP(Utils.fnoExchange, symbol, "")
            Utils.logger.info("quote fetched with ltp "+str(ltp))
            # OR Quotes API can be accessed without completing login by passing session_token, sid, and server_id
            if ltp == 0:
                Utils.logger.info("get quote attempt failed ", ltp)
                client.IB_Subscribe(Utils.fnoExchange, symbol, "")
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


def placeOrder(client, instrument_symbol, transaction_type, premium):
    Utils.logger.info("placing {} order for {} at {}".format(transaction_type, instrument_symbol, premium))
    transaction_type = "LE" if transaction_type == "buy" else "SE"
    orderID = client.IB_MappedOrderAdv(SignalID=0,
                                       StrategyTag="OPTIONSPLAYPYSAF",
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
    Utils.logger.info("order placed with orderID " + str(orderID))
    while True:
        try:
            statuses = client.IB_OrderStatus(orderID)
            done = True
            for status in statuses.split(","):
                if status != "completed":
                    done = False
                    Utils.logger.warn("order not completed with status" + statuses)
                    time.sleep(0.1)
            if done:
                Utils.logger.info("order completed for all users")
                break
        except Exception as e:
            Utils.logger.error(e)
            time.sleep(1)
            continue
    # for user in users:
    #     user.order(instrument_token, instrument_symbol, transaction_type, premium, quantity)


async def execute_in_parallel(func_list, self_instance):
    tasks = []

    # Define a function to be executed in each task
    async def execute_func(func):
        await func(self_instance)

    # Create and schedule a task for each function in the func_list
    for func in func_list:
        task = asyncio.create_task(execute_func(func))
        tasks.append(task)

    # Wait for all tasks to finish
    await asyncio.gather(*tasks)
