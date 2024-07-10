import os

from core.strategy import Strategy
from utils import liveUtils, Utils, Constants


class Live:
    def __init__(self):
        self.mtmhit = None
        self.expDate = Utils.expDate
        self.strategy = [Strategy("sell", strategyNo) for strategyNo in range(6)]
        self.loadPositionalStrategies()
        self.hedge = False

    def callback_method(self, currentime, priceDict):

        Utils.logger.info("New minute formed, executing computation")
        Utils.logger.info("the current min closes are" + str(priceDict))

        self.start(priceDict[Utils.index], priceDict, currentime)

        self.checkMTMs(priceDict)

        self.piyushAdjustment(priceDict[Utils.index], currentime, priceDict)

        if currentime == "15:25:00":
            self.exitPositionalStrategies()

    def start(self, spot, priceDict, currentime):
        task = [(strategy.start, (spot, priceDict, currentime)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def checkMTMs(self, priceDict):
        task = [(strategy.checkmtmhit, (priceDict,)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def piyushAdjustment(self, spot, currentime, priceDict):
        task = [(strategy.piyushAdjustment, (spot, currentime, priceDict)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def loadPositionalStrategies(self):
        for file in os.listdir(Constants.positionalObjectsPath):
            strategy = liveUtils.loadObject(file)
            st

    def exitPositionalStrategies(self):
        pass
