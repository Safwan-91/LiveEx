import time

import asyncio

import Utils
from strategy import Strategy
import liveUtils


class Live:
    def __init__(self):
        self.mtmhit = None
        self.expDate = Utils.expDate
        self.strategy = [Strategy("sell", strategyNo) for strategyNo in range(1)]
        self.hedge = False

    def callback_method(self, client, currentime, priceDict):

        Utils.logger.info("New minute formed, executing computation")
        Utils.logger.info("the current min closes are" + str(priceDict))

        self.start(client, priceDict[Utils.index], priceDict, currentime)

        self.checkMTMs(client, priceDict)

        self.piyushAdjustment(priceDict[Utils.index], client, currentime, priceDict)

    def start(self, client, spot, priceDict, currentime):
        task = [(strategy.start, (client, spot, priceDict, currentime)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def checkMTMs(self, client, priceDict):
        task = [(strategy.checkmtmhit, (client, priceDict)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)

    def piyushAdjustment(self, spot, client, currentime, priceDict):
        task = [(strategy.piyushAdjustment, (spot, client, currentime, priceDict)) for strategy in self.strategy]
        liveUtils.execute_in_parallel(task)
