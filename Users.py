from NorenRestApiPy.NorenApi import NorenApi
from neo_api_client import NeoAPI
from datetime import datetime

import Utils
import userDetails


def fetchDetails(id):
    return userDetails.users[id]


class User:
    def __init__(self, Id):
        self.userDetails = fetchDetails(Id)
        self.client = self.login()

    def login(self):
        if self.userDetails["broker"] == "shoonya":
            api = NorenApi(host='https://api.shoonya.com/NorenWClientTP/',
                                    websocket='wss://api.shoonya.com/NorenWSTP/')
            api.login(userid=self.userDetails["userid"], password=self.userDetails["password"], twoFA=input("enter shoonya otp "), vendor_code=self.userDetails["vendorCode"], api_secret=self.userDetails["secret"], imei=self.userDetails["imei"])
            return api
        elif self.userDetails["broker"] == "kotakNeo":
            client = NeoAPI(consumer_key=self.userDetails["consumer_key"], consumer_secret=self.userDetails["consumer_secret"],
                            environment='Prod', on_message=None, on_error=None, on_close=None, on_open=None)
            client.login(mobilenumber=self.userDetails["mobilenumber"], password=self.userDetails["password"])
            client.configuration.edit_sid = "sid"
            client.configuration.edit_token = "token"
            # client.session_2fa(input())
            return client

    def order(self, instrument_token, instrument_symbol, transaction_type, premium, quantity):
        print("time before order ", datetime.now())
        try:
            if self.userDetails["broker"] == "kotakNeo":
                order_id = self.client.place_order(exchange_segment="bse_fo", product="NRML", price="", order_type="MKT", quantity=quantity, validity="DAY", trading_symbol="",
                           transaction_type="", amo="", disclosed_quantity="", market_protection="", pf="", trigger_price="",
                           tag="")
                print(transaction_type + " : " + str(instrument_symbol) + " at " + str(premium))
                return order_id
            elif self.userDetails["broker"] == "shoonya":
                transaction_type = transaction_type[0].upper()
                # order_id = self.client.place_order(buy_or_sell=transaction_type, product_type='M',
                #         exchange='NFO', tradingsymbol=instrument_symbol,
                #         quantity= Utils.lotSize, discloseqty=0, price_type='MKT', #price=200.00, trigger_price=199.50,
                #         retention='DAY', remarks='my_order_001')["norenordno"]
                # flag = True
                # while flag:
                #     for el in self.client.get_order_book():
                #         if el["norenordno"] == order_id:
                #             if el["norenordno"] != "Open":
                #                 flag = False
                #                 break
                #             break
            print(transaction_type + " : " + str(instrument_symbol) + " at " + str(premium))
            print("time after order ", datetime.now())
        except Exception as e:
            print("Exception when calling OrderApi->place_order: %s\n" % e)