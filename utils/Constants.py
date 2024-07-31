import logging
from datetime import datetime

logPath = "C:/Users/Safwan PC/Desktop/logs/"
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
lotSizeMap = {"MIDCPNIFTY": 1, "FINNIFTY": 3, "BANKNIFTY": 3, "NIFTY": 4, "SENSEX": 3, "BANKEX": 3}
positionalObjectsPath = r"C:\Users\Safwan PC\PycharmProjects\LiveExe2\positionalObjects"
positionalEndTime = "15:25"
monthMap = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, "O": 10, "N": 11, "D": 12}
