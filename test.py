import time

from PriceStream import PriceStream
from main import runStrategy

import Utils
from datetime import datetime

priceDictList = [
    {'addons': [], 'BANKNIFTY': 49094.6, 'BANKNIFTY05JUN24C49100': 100, 'BANKNIFTY05JUN24P49100': 100, 'BANKNIFTY05JUN24C49200': 25, 'BANKNIFTY05JUN24P49000': 25},
    {'addons': [], 'BANKNIFTY': 49150.6, 'BANKNIFTY05JUN24C49100': 135, 'BANKNIFTY05JUN24P49100': 70, 'BANKNIFTY05JUN24C49200': 25, 'BANKNIFTY05JUN24P49000': 25},
    {'addons': [], 'BANKNIFTY': 49300.6, 'BANKNIFTY05JUN24C49100': 100, 'BANKNIFTY05JUN24P49100': 100, 'BANKNIFTY05JUN24C49200': 55, 'BANKNIFTY05JUN24P49000': 25, 'BANKNIFTY05JUN24P49300': 100},
                 ]
if __name__ == '__main__':
    Utils.logger.info("Starting the program")
    for priceDict in priceDictList:
        runStrategy(priceDict)
        current_time = datetime.now()
        # sleep_time = 60 - current_time.second - (current_time.microsecond / 1000000.0)
        # time.sleep(sleep_time)
        if current_time.strftime("%H:%M:%S") > "20:30:00":
            break