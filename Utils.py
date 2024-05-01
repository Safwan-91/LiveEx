import logging
from datetime import datetime

logPath = "C:/Users/Administrator/Desktop/logs"
formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=logPath+datetime.now().strftime('%Y-%m-%d')+'.log', level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(console_handler)

index = "NIFTY"
expDate = "24502"
indexExchange = "NSE"
fnoExchange = "NFO"
adjustmentShift = "True"

initialPremiumMap = {"MIDCPNIFTY": 25, "FINNIFTY": 40, "BANKNIFTY": 100, "NIFTY": 50, "SENSEX": 163, "BANKEX": 115}
mtmSLMap = {"MIDCPNIFTY": 10, "FINNIFTY": 30, "BANKNIFTY": 80, "NIFTY": 40, "SENSEX": 130, "BANKEX": 90}
strikeDifferenceMap = {"MIDCPNIFTY": 25, "FINNIFTY": 50, "BANKNIFTY": 100, "NIFTY": 50, "SENSEX": 100, "BANKEX": 100}
indexTokenMap = {"MIDCPNIFTY": "NIFTY MID SELECT", "FINNIFTY": "NIFTY FIN SERVICE", "BANKNIFTY": "BANKNIFTY", "NIFTY": "NIFTY", "SENSEX": "SENSEX", "BANKEX": "BANKEX"}
lotSizeMap = {"MIDCPNIFTY": 1, "FINNIFTY": 3, "BANKNIFTY": 3, "NIFTY": 2, "SENSEX": 3, "BANKEX": 3}
shiftAmountMap = {"MIDCPNIFTY": 1, "FINNIFTY": 1, "BANKNIFTY": 2, "NIFTY": 1, "SENSEX": 2, "BANKEX": 2}

shiftAmount = shiftAmountMap[index]
indexToken = indexTokenMap[index]
lotSize = lotSizeMap[index]
SLMap = {0: 0.3, 1: 1, 2: 0}
adjustmentPercent = 0.3
initialPremium = initialPremiumMap[index]
mtmStopLoss = mtmSLMap[index]
path = "C:\\Users\\Safwan PC\\banknifty_new\\"
strikeDifference = strikeDifferenceMap[index]
noOfAdjustment = 1
oneSideFullHitFlag = True
