import os
from datetime import datetime

from core.strategy import Strategy
from utils import liveUtils, Utils, Constants


class Live:
    def __init__(self):
        self.mtmhit = None
        self.expDate = Utils.expDate
        self.strategy = [Strategy("sell", strategyNo) for strategyNo in range(6)]
        self.positionalStrategiesLoaded = False
        self.hedge = False

    def callback_method(self, currentime, priceDict):

        Constants.logger.info("New minute formed, executing computation")
        Constants.logger.info("the current min closes are" + str(priceDict))

        if not self.positionalStrategiesLoaded:
            self.loadPositionalStrategies(priceDict)

        self.start(priceDict[Utils.index], priceDict, currentime)

        self.checkMTMs(priceDict)

        self.piyushAdjustment(priceDict[Utils.index], currentime, priceDict)

        if currentime == "15:25:00":
            self.overNightHedge(priceDict)

    def start(self, spot, priceDict, currentime):
        task = [(strategy.start, (spot, priceDict, currentime)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def checkMTMs(self, priceDict):
        task = [(strategy.checkmtmhit, (priceDict,)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def piyushAdjustment(self, spot, currentime, priceDict):
        task = [(strategy.piyushAdjustment, (spot, currentime, priceDict)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def loadPositionalStrategies(self, priceDict):
        for file in os.listdir(Constants.positionalObjectsPath):
            strategy = liveUtils.loadObject(file)
            self.strategy.append(strategy)
            symbols = strategy.straddle.getAllSymbols()
            for symbol in symbols:
                priceDict["addons"].append(symbol)
        self.positionalStrategiesLoaded = True

    def overNightHedge(self, priceDict):
        if datetime.now().strftime("%d") != Utils.expDate[2]:
            return
        task = [(strategy.buyOverNightHedge, (priceDict,)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

