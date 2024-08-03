from core.strategy import Strategy
from utils import liveUtils
priceDict = {"MIDCPNIFTY05AUG24C12700": 45.2,"MIDCPNIFTY05AUG24C13200": 2.45, "MIDCPNIFTY05AUG24P12100": 3.6, "MIDCPNIFTY05AUG24P12300": 5.75}
if __name__ == '__main__':
    strategy = Strategy("sell", 13)
    strategy.started = True
    strategy.straddle.strikeStack.append(12600)
    strategy.straddle.mean.append(12500)
    strategy.straddle.ce.setLegPars("MIDCPNIFTY05AUG24C12700", priceDict)
    strategy.straddle.ce.setHedge(5, priceDict)
    strategy.straddle.pe.currentAdjustmentLevel = 1
    strategy.straddle.ce.realizedProfit = -8.25
    strategy.straddle.pe.setLegPars("MIDCPNIFTY05AUG24P12300", priceDict)
    strategy.straddle.pe.setHedge(2, priceDict)
    strategy.straddle.pe.realizedProfit = 4.4
    liveUtils.dumpObject(strategy, "strategy_" + str(strategy.strategyNo))
