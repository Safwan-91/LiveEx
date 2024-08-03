from utils import Constants

isMonthly = False
intradayIndex = "BANKEX"
intradayExpDate = "24805"
positionalExpDate = "24807"

parameters = [
    {
        "SLMap": {0: 0.3, 1: 1, 2: 1},
        "adjustmentPercent": 0.3,
        "initialPremiumMultiplier": 0.0025,
        "mtmStopLoss": 0.00165,
        "index": intradayIndex,
        "lotSize": 1,
        "expDate": intradayExpDate,
        "indexExchange": "BSE" if intradayIndex in ["SENSEX", "BANKEX"] else "NSE",
        "fnoExchange": "BFO" if intradayIndex in ["SENSEX", "BANKEX"] else "NFO",
        "strikeDifference": Constants.strikeDiffMap[intradayIndex],
        "noOfAdjustment": 1,
        "oneSideFullHitFlag": True,
        "daysBeforeExpiry": 2,
        "adjustmentShift": True,
        "shiftAmount": 0.00005,
        "startTime": "09:45:00",
        "hedgeDist": 20,
        "overNightHedgeDist": 5,
        "isPositional": False,
        "strategyTag": "OPTIONSPLAYINTRADAY1MIN0945SL1"}
#     },
# {
#         "SLMap": {0: 0.3, 1: 1, 2: 1},
#         "adjustmentPercent": 0.3,
#         "initialPremiumMultiplier": 0.0025,
#         "mtmStopLoss": 0.00165,
#         "index": intradayIndex,
#         "lotSize": 1,
#         "expDate": intradayExpDate,
#         "indexExchange": "BSE" if intradayIndex in ["SENSEX", "BANKEX"] else "NSE",
#         "fnoExchange": "BFO" if intradayIndex in ["SENSEX", "BANKEX"] else "NFO",
#         "strikeDifference": Constants.strikeDiffMap[intradayIndex],
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": True,
#         "shiftAmount": 0.00005,
#         "startTime": "09:45:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAYINTRADAY1MIN0945SL2"
#     },
# {
#         "SLMap": {0: 0.3, 1: 1, 2: 1},
#         "adjustmentPercent": 0.3,
#         "initialPremiumMultiplier": 0.0025,
#         "mtmStopLoss": 0.00165,
#         "index": intradayIndex,
#         "lotSize": 1,
#         "expDate": intradayExpDate,
#         "indexExchange": "BSE" if intradayIndex in ["SENSEX", "BANKEX"] else "NSE",
#         "fnoExchange": "BFO" if intradayIndex in ["SENSEX", "BANKEX"] else "NFO",
#         "strikeDifference": Constants.strikeDiffMap[intradayIndex],
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": True,
#         "shiftAmount": 0.00005,
#         "startTime": "09:45:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAYINTRADAY1MIN1015SL1"
#     },
# {
#         "SLMap": {0: 0.3, 1: 1, 2: 1},
#         "adjustmentPercent": 0.3,
#         "initialPremiumMultiplier": 0.0025,
#         "mtmStopLoss": 0.00165,
#         "index": intradayIndex,
#         "lotSize": 1,
#         "expDate": intradayExpDate,
#         "indexExchange": "BSE" if intradayIndex in ["SENSEX", "BANKEX"] else "NSE",
#         "fnoExchange": "BFO" if intradayIndex in ["SENSEX", "BANKEX"] else "NFO",
#         "strikeDifference": Constants.strikeDiffMap[intradayIndex],
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": True,
#         "shiftAmount": 0.00005,
#         "startTime": "09:45:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAYINTRADAY1MIN1015SL2"
#     },
# {
#         "SLMap": {0: 0.3, 1: 1, 2: 1},
#         "adjustmentPercent": 0.3,
#         "initialPremiumMultiplier": 0.0025,
#         "mtmStopLoss": 0.00165,
#         "index": intradayIndex,
#         "lotSize": 1,
#         "expDate": intradayExpDate,
#         "indexExchange": "BSE" if intradayIndex in ["SENSEX", "BANKEX"] else "NSE",
#         "fnoExchange": "BFO" if intradayIndex in ["SENSEX", "BANKEX"] else "NFO",
#         "strikeDifference": Constants.strikeDiffMap[intradayIndex],
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": True,
#         "shiftAmount": 0.00005,
#         "startTime": "09:45:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAYINTRADAY1MIN1045SL1"
#     },
# {
#         "SLMap": {0: 0.3, 1: 1, 2: 1},
#         "adjustmentPercent": 0.3,
#         "initialPremiumMultiplier": 0.0025,
#         "mtmStopLoss": 0.00165,
#         "index": intradayIndex,
#         "lotSize": 1,
#         "expDate": intradayExpDate,
#         "indexExchange": "BSE" if intradayIndex in ["SENSEX", "BANKEX"] else "NSE",
#         "fnoExchange": "BFO" if intradayIndex in ["SENSEX", "BANKEX"] else "NFO",
#         "strikeDifference": Constants.strikeDiffMap[intradayIndex],
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": True,
#         "shiftAmount": 0.00005,
#         "startTime": "09:45:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAYINTRADAY1MIN1045SL2"
#     },
#     {
#         "SLMap": {0: 0.2, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.01,
#         "mtmStopLoss": 0.004,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": positionalExpDate,
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 6,
#         "adjustmentShift": True,
#         "shiftAmount": 0.0002,
#         "startTime": "09:44:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": True,
#         "strategyTag": "OPTIONSPLAYPOSITIONAL"
#     },
#     {
#         "SLMap": {0: 0.2, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.01,
#         "mtmStopLoss": 0.004,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": positionalExpDate,
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 6,
#         "adjustmentShift": True,
#         "shiftAmount": 0.0002,
#         "startTime": "14:30:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": True,
#         "strategyTag": "OPTIONSPLAYPOSITIONAL"
#     },
#     {
#         "SLMap": {0: 0.2, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.01,
#         "mtmStopLoss": 0.004,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": positionalExpDate,
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 5,
#         "adjustmentShift": True,
#         "shiftAmount": 0.00015,
#         "startTime": "09:45:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": True,
#         "strategyTag": "OPTIONSPLAYPOSITIONAL"
#     },
#     {
#         "SLMap": {0: 0.2, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.01,
#         "mtmStopLoss": 0.004,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": positionalExpDate,
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 5,
#         "adjustmentShift": True,
#         "shiftAmount": 0.00015,
#         "startTime": "14:30:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": True,
#         "strategyTag": "OPTIONSPLAYPOSITIONAL"
#     },
#     {
#         "SLMap": {0: 0.2, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.005,
#         "mtmStopLoss": 0.004,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": positionalExpDate,
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 2,
#         "adjustmentShift": True,
#         "shiftAmount": 0.0001,
#         "startTime": "09:45:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": True,
#         "strategyTag": "OPTIONSPLAYPOSITIONAL"
#     },
#     {
#         "SLMap": {0: 0.2, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.005,
#         "mtmStopLoss": 0.004,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": positionalExpDate,
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 2,
#         "adjustmentShift": True,
#         "shiftAmount": 0.0001,
#         "startTime": "14:30:00",
#         "hedgeDist": 20,
#         "overNightHedgeDist": 5,
#         "isPositional": True,
#         "strategyTag": "OPTIONSPLAYPOSITIONAL"
#     }
]

# parameters = [
#     {
#         "SLMap": {0: 0.4, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.003,
#         "mtmStopLoss": 0.02,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": "24724",
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": False,
#         "shiftAmount": 0.0003,
#         "startTime": "13:00:00",
#         "hedgeDist": 10,
#         "overNightHedgeDist": 4,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAY1PM"
#     },
# {
#         "SLMap": {0: 0.5, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.003,
#         "mtmStopLoss": 0.02,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": "24724",
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": False,
#         "shiftAmount": 0.0003,
#         "startTime": "13:30:00",
#         "hedgeDist": 8,
#         "overNightHedgeDist": 4,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAY1PM"
#     },
# {
#         "SLMap": {0: 0.6, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.003,
#         "mtmStopLoss": 0.02,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": "24724",
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": False,
#         "shiftAmount": 0.0003,
#         "startTime": "13:59:00",
#         "hedgeDist": 6,
#         "overNightHedgeDist": 4,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAY1PM"
#     },
# {
#         "SLMap": {0: 0.6, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.003,
#         "mtmStopLoss": 0.02,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": "24724",
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": False,
#         "shiftAmount": 0.0003,
#         "startTime": "14:29:00",
#         "hedgeDist": 5,
#         "overNightHedgeDist": 4,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAY1PM"
#     },
# {
#         "SLMap": {0: 100, 1: 1, 2: 1},
#         "adjustmentPercent": 0.2,
#         "initialPremiumMultiplier": 0.003,
#         "mtmStopLoss": 0.02,
#         "index": "BANKNIFTY",
#         "lotSize": 2,
#         "expDate": "24724",
#         "indexExchange": "NSE",
#         "fnoExchange": "NFO",
#         "strikeDifference": 100,
#         "noOfAdjustment": 1,
#         "oneSideFullHitFlag": True,
#         "daysBeforeExpiry": 0,
#         "adjustmentShift": False,
#         "shiftAmount": 0.0003,
#         "startTime": "14:59:00",
#         "hedgeDist": 5,
#         "overNightHedgeDist": 4,
#         "isPositional": False,
#         "strategyTag": "OPTIONSPLAY1PM"
#     },
# ]
