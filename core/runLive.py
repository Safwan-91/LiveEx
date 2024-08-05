import os
from datetime import datetime

from core.strategy import Strategy
from utils import liveUtils, Utils, Constants


class Live:
    def __init__(self):
        self.positionalObjectsSaved = False
        self.mtmhit = None
        self.strategy = [Strategy("sell", strategyNo) for strategyNo in range(len(Utils.parameters))]
        self.positionalStrategiesLoaded = False
        self.hedge = False

    def callback_method(self, currentime, priceDict):

        Constants.logger.info("New minute formed, executing computation")
        Constants.logger.info("the current min closes are" + str(priceDict))

        if not self.positionalStrategiesLoaded:
            self.loadPositionalStrategies(priceDict)

        self.start(priceDict, currentime)

        self.checkMTMs(priceDict)

        self.piyushAdjustment(currentime, priceDict)

        if currentime[:5] == Constants.positionalEndTime:
            self.overNightHedge(priceDict)

    def start(self, priceDict, currentime):
        task = [(strategy.start, (priceDict, currentime)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def checkMTMs(self, priceDict):
        task = [(strategy.checkmtmhit, (priceDict,)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def piyushAdjustment(self,currentime, priceDict):
        task = [(strategy.piyushAdjustment, (currentime, priceDict)) for strategy in self.strategy]
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
        task = [(strategy.buyOverNightHedge, (priceDict,)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)
        for strategy in self.strategy:
            if strategy.started and strategy.getPar("isPositional") and datetime.now().strftime("%d") != strategy.getPar("expDate")[-2:] and not self.positionalObjectsSaved:
                liveUtils.dumpObject(strategy, "strategy_"+str(strategy.strategyNo))
        self.positionalObjectsSaved = True

