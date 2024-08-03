import time

import pyotp
from NorenRestApiPy.NorenApi import NorenApi
#from neo_api_client import NeoAPI

from user import userDetails
from utils import Utils, Constants
from ioUtils.pyIB_APIS import IB_APIS


def fetchDetails(id):
    return userDetails.users[id]


class User:
    def __init__(self, Id):
        self.id = Id
        self.userDetails = fetchDetails(Id)
        self.client = self.login()

    def login(self):
        if self.userDetails["broker"] == "shoonya":
            api = NorenApi(host='https://api.shoonya.com/NorenWClientTP/',
                                  websocket='wss://api.shoonya.com/NorenWSTP/')
            ret = api.login(userid=self.userDetails["userid"], password=self.userDetails["password"],
                      twoFA=pyotp.TOTP(self.userDetails["2fa"]).now(), vendor_code=self.userDetails["vendorCode"],
                      api_secret=self.userDetails["secret"], imei=self.userDetails["imei"])
            return api
        elif self.userDetails["broker"] == "kotakNeo":
            client = NeoAPI(consumer_key=self.userDetails["consumer_key"],
                            consumer_secret=self.userDetails["consumer_secret"],
                            environment='Prod')
            client.login(mobilenumber=self.userDetails["mobilenumber"], password=self.userDetails["password"])
            client.session_2fa(self.userDetails["mpin"])
            return client
        elif self.userDetails["broker"] == "stxo":
            client = IB_APIS("http://localhost:21000")
            return client

    def placeOrder(self, instrument_token, instrument_symbol, transaction_type, strategyNo):
        quantity = str(Constants.lotQuantityMap[Utils.parameters[strategyNo]["index"]] * Utils.parameters[strategyNo]["lotSize"])
        result = None
        try:
            order_id = None
            if self.userDetails["broker"] == "kotakNeo":
                exch_segment = "bse_fo" if Utils.parameters[strategyNo]["index"] in ["BANKEX", "SENSEX"] else "nse_fo"
                transaction_type = transaction_type[0].upper()
                result = self.client.place_order(exchange_segment=exch_segment, product="NRML", price="",
                                                   order_type="MKT", quantity=quantity, validity="DAY",
                                                   trading_symbol=instrument_symbol,
                                                   transaction_type=transaction_type)
                order_id = result["nOrdNo"]
            elif self.userDetails["broker"] == "shoonya":
                transaction_type = transaction_type[0].upper()
                result = self.client.place_order(buy_or_sell=transaction_type, product_type='M',
                                                   exchange='NFO', tradingsymbol= instrument_token,
                                                   quantity= Utils.parameters[strategyNo]["lotSize"], discloseqty=0, price_type='MKT',  #price=200.00, trigger_price=199.50,
                                                   retention='DAY', remarks='my_order_001')
                order_id = result["norenordno"]
            Constants.logger.debug("order placed for user {} with order id {}".format(self.id, order_id))
            return order_id
        except Exception as e:
            Constants.logger.debug("error while placing order for user {}. error - {}".format(self.id, result))

    def confirmOrderStatus(self, orderid):
        tryNo = 0
        while tryNo <= 10:
            try:
                if self.userDetails["broker"] == "kotakNeo":
                    if self.client.order_history(orderid)["data"]["data"][0]["ordSt"] in ["complete", "rejected"]:
                        Constants.logger.debug("order confirmed for user {} with order id {}".format(self.id, orderid))
                        break
                    else:
                        time.sleep(0.05)
                if self.userDetails["broker"] == "shoonya":
                    if self.client.single_order_history(orderid)[0]["status"] in ["COMPLETE", "REJECTED"]:
                        Constants.logger.debug("order confirmed for user {} with order id {}".format(self.id, orderid))
                        break
                    else:
                        time.sleep(0.05)
            except Exception as e:
                Constants.logger.debug("error while confirming order for user {}. error - {}".format(self.id, e))
                tryNo += 1

    def placeAndConfirmOrder(self, instrument_token, instrument_symbol, transaction_type, premium, quantity,
                             strategyNo):
        if self.userDetails["broker"] == "stxo":
            self.placeAndConfirmOrderStxo(instrument_token, instrument_symbol, transaction_type, premium, quantity,
                                          strategyNo)
            return
        if strategyNo not in self.userDetails["strategies"]:
            return
        orderId = self.placeOrder(instrument_token, instrument_symbol, transaction_type, strategyNo)
        self.confirmOrderStatus(orderId)

    def placeAndConfirmOrderStxo(self, instrument_token, instrument_symbol, transaction_type, premium, quantity,
                                 strategyNo):
        transaction_type = "LE" if transaction_type == "buy" else "SE"
        tryNo = 0
        orderID = None
        while tryNo < 5:
            orderID = self.client.IB_MappedOrderAdv(SignalID=0,
                                                    StrategyTag=Utils.parameters[strategyNo]["strategyTag"],
                                                    SourceSymbol=instrument_symbol,
                                                    TransactionType=transaction_type,
                                                    OrderType="MARKET",
                                                    ProductType="NRML",
                                                    Price="",
                                                    TriggerPrice="",
                                                    Quantity=Utils.parameters[strategyNo]["lotSize"],
                                                    ProfitValue="",
                                                    StoplossValue="",
                                                    SLTrailingValue="",
                                                    SignalLTP=0,
                                                    OptionsType="")
            Constants.logger.debug(
                "strategy_" + str(strategyNo) + " - " + "order placed with orderID {} and tryNo {}".format(orderID,
                                                                                                           tryNo))
            if orderID:
                break
            else:
                tryNo += 1
        tryNo = 0
        while tryNo <= 10:
            try:
                statuses = self.client.IB_OrderStatus(orderID)
                done = True
                for status in statuses.split(","):
                    if status not in ["completed", "rejected"]:
                        done = False
                        # Constants.logger.warn("strategy_" + str(strategyNo) + " - " + "order not completed with status" + statuses)
                        time.sleep(0.05)
                        break
                if done:
                    Constants.logger.info("strategy_" + str(strategyNo) + " - " + "order completed for all users")
                    break
            except Exception as e:
                Constants.logger.error(e)
                time.sleep(1)
                continue
        if not done:
            Constants.logger.error("strategy_" + str(strategyNo) + " - " + "order not completed for all users, status - {}".format(statuses))


users = [User("stxo")]
