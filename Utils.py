import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

index = "FINNIFTY"
expDate = "24514"
indexExchange = "NSE"
fnoExchange = "NFO"

startTime = ["00:04:00", "00:04:00", "00:04:00", "10:44:00"]
adjSL = [1,2,1,2]
strategyTag = ["OPTIONSPLAY945SL1", "OPTIONSPLAY945SL2", "OPTIONSPLAY1045SL1", "OPTIONSPLAY1045SL2"]

executor = ThreadPoolExecutor()

logPath = "C:/Users/Safwan PC/Desktop/logs/"
formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=logPath+datetime.now().strftime('%Y-%m-%d')+'.log', level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(console_handler)

initialPremiumMap = {"MIDCPNIFTY": 25, "FINNIFTY": 40, "BANKNIFTY": 110, "NIFTY": 50, "SENSEX": 163, "BANKEX": 125}
mtmSLMap = {"MIDCPNIFTY": 10, "FINNIFTY": 25, "BANKNIFTY": 70, "NIFTY": 30, "SENSEX": 100, "BANKEX": 80}
strikeDifferenceMap = {"MIDCPNIFTY": 25, "FINNIFTY": 50, "BANKNIFTY": 100, "NIFTY": 50, "SENSEX": 100, "BANKEX": 100}
indexTokenMap = {"MIDCPNIFTY": "NIFTY MID SELECT", "FINNIFTY": "Nifty Fin Service", "BANKNIFTY": "BANKNIFTY", "NIFTY": "NIFTY", "SENSEX": "SENSEX", "BANKEX": "BANKEX"}
lotSizeMap = {"MIDCPNIFTY": 1, "FINNIFTY": 3, "BANKNIFTY": 3, "NIFTY": 4, "SENSEX": 3, "BANKEX": 3}
shiftAmountMap = {"MIDCPNIFTY": 1, "FINNIFTY": 1, "BANKNIFTY": 2, "NIFTY": 1, "SENSEX": 2, "BANKEX": 2}

adjustmentShift = "True"
shiftAmount = shiftAmountMap[index] if adjSL == 1 else shiftAmountMap[index] + 1
indexToken = indexTokenMap[index]
lotSize = lotSizeMap[index]
SLMap = {0: [0.3, 0.3, 0.3, 0.3], 1: adjSL, 2: 0}
adjustmentPercent = 0.3
initialPremium = initialPremiumMap[index]
mtmStopLoss = mtmSLMap[index]
strikeDifference = strikeDifferenceMap[index]
noOfAdjustment = 1
oneSideFullHitFlag = True

