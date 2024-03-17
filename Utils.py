index = "BANKEX"
indexExchange = "BSE"
fnoExchange = "BFO"

initialPremiumMap = {"MIDCPNIFTY": 25, "FINNIFTY": 40, "BANKNIFTY": 100, "NIFTY": 60, "SENSEX": 100, "BANKEX": 100}
mtmSLMap = {"MIDCPNIFTY": 10, "FINNIFTY": 30, "BANKNIFTY": 60, "NIFTY": 30, "SENSEX": 70, "BANKEX": 60}
strikeDifferenceMap = {"MIDCPNIFTY": 25, "FINNIFTY": 50, "BANKNIFTY": 100, "NIFTY": 50, "SENSEX": 100, "BANKEX": 100}
indexTokenMap = {"MIDCPNIFTY": "NIFTY MID SELECT", "FINNIFTY": "NIFTY FIN SERVICE", "BANKNIFTY": "BANKNIFTY", "NIFTY": "NIFTY", "SENSEX": "SENSEX", "BANKEX": "BANKEX"}
lotSizeMap = {"MIDCPNIFTY": 75, "FINNIFTY": 40, "BANKNIFTY": 15, "NIFTY": 50, "SENSEX": 10, "BANKEX": 15}

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
