import logging
from datetime import datetime

logPath = "C:/Users/Safwan PC/Desktop/logs/"
formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=logPath+datetime.now().strftime('%Y-%m-%d')+'.log', level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(console_handler)

lotQuantityMap = {"MIDCPNIFTY": 10, "FINNIFTY": 40, "BANKNIFTY": 15, "NIFTY": 25, "SENSEX": 10, "BANKEX": 15}
positionalObjectsPath = "C:\Users\Safwan PC\PycharmProjects\LiveExe\positionalObjects"
