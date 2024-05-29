import asyncio
import time

import liveUtils
from PriceStream import PriceStream

import Utils
from runLive import Live
from datetime import datetime
from pyIB_APIS import IB_APIS

live_instances = {}
def runStrategy(strategyNo, client, priceDict):
    if strategyNo not in live_instances:
        live_instances[strategyNo] = Live(strategyNo)

    runLive = live_instances[strategyNo]
    currentTime = datetime.now().strftime("%H:%M:%S")
    if "00:15:00" <= currentTime <= "24:30:00":
        if runLive.mtmhit:
            return
        runLive.callback_method(client, currentTime, priceDict)


def main():
    Utils.logger.info("Starting the program")
    client = IB_APIS("http://localhost:21000")
    priceStream = PriceStream()
    priceStream.connect()
    time.sleep(5)
    while True:
        current_time = datetime.now()
        sleep_time = 60 - current_time.second - (current_time.microsecond / 1000000.0)
        time.sleep(sleep_time)
        tasks = [(runStrategy, (i, client, priceStream.priceDict)) for i in
                 range(4)]
        liveUtils.execute_in_parallel(tasks)



if __name__ == '__main__':
    main()
