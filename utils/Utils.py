import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

index = "BANKNIFTY"
expDate = "24717"
indexExchange = "NSE"
fnoExchange = "NFO"
hedgeDist = 20

startTime = ["09:44:00", "09:44:00", "10:44:00", "10:44:00", "10:14:00", "10:14:00"]
adjSL = [1, 2, 1, 2, 1, 2]
strategyTag = ["OPTIONSPLAY945SL1", "OPTIONSPLAY945SL2", "OPTIONSPLAY1045SL1", "OPTIONSPLAY1045SL2", "OPTIONSPLAY1015SL1", "OPTIONSPLAY1015SL2"]

initialPremiumMap = {"MIDCPNIFTY": 25, "FINNIFTY": 40, "BANKNIFTY": 110, "NIFTY": 50, "SENSEX": 163, "BANKEX": 125}
mtmSLMap = {"MIDCPNIFTY": 10, "FINNIFTY": 25, "BANKNIFTY": 70, "NIFTY": 30, "SENSEX": 100, "BANKEX": 80}
strikeDifferenceMap = {"MIDCPNIFTY": 25, "FINNIFTY": 50, "BANKNIFTY": 100, "NIFTY": 50, "SENSEX": 100, "BANKEX": 100}
indexTokenMap = {"MIDCPNIFTY": "26074", "FINNIFTY": "26037", "BANKNIFTY": "26009", "NIFTY": "26000", "SENSEX": "1", "BANKEX": "12"}
lotSizeMap = {"MIDCPNIFTY": 1, "FINNIFTY": 3, "BANKNIFTY": 3, "NIFTY": 4, "SENSEX": 3, "BANKEX": 3}
shiftAmountMap = {"MIDCPNIFTY": 1, "FINNIFTY": 1, "BANKNIFTY": 2, "NIFTY": 1, "SENSEX": 2, "BANKEX": 2}

parameters = [
    {"SLMap": {0: 0.2, 1: 1, 2: 1},
     "adjustmentPercent": 0.2,
     "initialPremiumMultiplier": 0.0025,
     "mtmStopLoss": 0.002,
     "index": "NIFTY",
     "expDate": "24717",
     "indexExchange": "NSE",
     "fnoExchange": "NFO",
     "strikeDifference": 50,
     "noOfAdjustment": 1,
     "oneSideFullHitFlag": True,
     "daysBeforeExpiry": 0,
     "adjustmentShift": True,
     "shiftAmount": 0.0002,
     "startTime": "09:44:00",
     "hedgeDist": 20,
     "overNightHedgeDist": 6,
     "isPositional": True
     },
]

