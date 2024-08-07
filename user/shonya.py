from NorenRestApiPy.NorenApi import NorenApi
import pyotp


class Shonya(object):
    _root = {"login": "/QuickAuth", "fund": "/Limits", "position": "/PositionBook", "orderbook": "/OrderBook",
             "tradebook": "/TradeBook", "holding": "/Holdings",
             "order": '/PlaceOrder', "modifyorder": '/ModifyOrder', "cancelorder": '/CancelOrder',
             "exitorder": '/ExitSNOOrder', "singleorderhistory": '/SingleOrdHist',
             "searchscrip": '/SearchScrip', "scripinfo": '/GetSecurityInfo', "getquote": '/GetQuotes',
             "hist_data": "/TPSeries", "option": "/GetOptionChain"}

    # make the api call

    def __init__(self, client_id: str = None):
        if client_id == '1':
            self.uid = 'FA127352'
            self.pwd = 'Fifa@2026'
            self.factor2 = pyotp.TOTP('MHG22VYK4B2I56KS4X567N2UG7M363A3')
            self.imei = '60-45-CB-C5-A7-49'
            self.app_key = 'a2e650f7d642a160d3d428f6795c0b20'
            self.vc = 'FA127352_U'
        elif client_id == '2':
            self.uid = 'FA92112'
            self.pwd = 'Wafa@2020'
            self.factor2 = None
            self.imei = '60-45-CB-C5-A7-49'
            self.app_key = '3314839374e9c76e933188930cef5bdd'
            # self.wss = None
            self.vc = 'FA92112_U'
        elif client_id == '7':
            self.uid = 'FA145842'
            self.pwd = 'Messi@2020'
            self.factor2 = None
            self.imei = '60-45-CB-C5-A7-49'
            self.app_key = '0efcfe51b43b52add631312b732993c1'
            # self.wss = None
            self.vc = 'FA145842_U'
        else:
            self.uid = 'FA175005'
            self.pwd = 'Strangle@29'
            self.factor2 = pyotp.TOTP('3ZQ64ZJ3LPSX64AL4J4MI3QGUIU527L7')
            self.imei = '60-45-CB-C5-A7-49'
            self.app_key = 'fa33bde95e69245faf636528e259083f'
            # self.wss = None
            self.vc = 'FA175005_U'

    def login(self):

        api = None

        class ShoonyaApiPy(NorenApi):
            def __init__(self):
                NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
                                  websocket='wss://api.shoonya.com/NorenWSTP/')
                global api
                api = self

        # start of our program
        api = ShoonyaApiPy()

        ret = api.login(userid=self.uid, password=self.pwd, twoFA=self.factor2.now(), vendor_code=self.vc,
                        api_secret=self.app_key, imei=self.imei)

        if ret is not None:
            if ret['stat'] == 'Ok':
                self.api = api
                print("Logged In.")
                return self.api
            else:
                print(f"Unable to Login. Reason:{ret.text}")
                return
        else:
            print('login  error')
