import multiprocessing
import time

from PriceStream import PriceStream

import Utils
from runLive import Live
from datetime import datetime
from pyIB_APIS import IB_APIS


def runStrategy(strategyNo, client, priceDict):
    runLive = Live(strategyNo)
    currentTime = datetime.now().strftime("%H:%M:%S")
    lastMin = None
    while "00:15:00" <= currentTime <= "15:30:00":
        if currentTime[3:5] != lastMin and currentTime >= Utils.startTime[strategyNo]:
            runLive.callback_method(client, currentTime, priceDict)
            lastMin = currentTime[3:5]
        currentTime = datetime.now().strftime("%H:%M:%S")
        if runLive.mtmhit:
            break


if __name__ == '__main__':
    Utils.logger.info("Starting the program")
    client = IB_APIS("http://localhost:21000")
    priceStream = PriceStream()
    priceStream.connect()
    time.sleep(5)
    processes = []
    for i in range(4):
        processes.append(multiprocessing.Process(target=runStrategy, args=(i, client, priceStream.priceDict)))
        processes[i].start()
    for process in processes:
        process.join()
