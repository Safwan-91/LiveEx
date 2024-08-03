import logging
from datetime import datetime

logPath = "C:/Users/thanseef/Desktop/logs/"
formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=logPath + datetime.now().strftime('%Y-%m-%d') + '.log', level=logging.DEBUG,
                    format=formatter)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(console_handler)

lotQuantityMap = {"MIDCPNIFTY": 10, "FINNIFTY": 40, "BANKNIFTY": 15, "NIFTY": 25, "SENSEX": 10, "BANKEX": 15}
indexTokenMap = {"MIDCPNIFTY": "26074", "FINNIFTY": "26037", "BANKNIFTY": "26009", "NIFTY": "26000", "SENSEX": "1",
                 "BANKEX": "12"}
strikeDiffMap = {"MIDCPNIFTY": 25, "FINNIFTY": 50, "BANKNIFTY": 100, "NIFTY": 50, "SENSEX": 100, "BANKEX": 100}
tokenIndexMap = {"26074": "MIDCPNIFTY", "26037": "FINNIFTY", "26009": "BANKNIFTY", "26000": "NIFTY", "1": "SENSEX",
                 "12": "BANKEX"}

positionalObjectsPath = r"C:\Users\thanseef\PycharmProjects\LiveEx_prod\positionalObjects"
positionalEndTime = "15:25"
monthMap = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, "O": 10, "N": 11, "D": 12}
