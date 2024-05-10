import multiprocessing

import Utils
from runLive import Live
from datetime import datetime
from pyIB_APIS import IB_APIS


def runStrategy(strategyNo, client):
    runLive = Live(strategyNo)
    currentTime = datetime.now().strftime("%H:%M:%S")
    lastMin = None
    while "00:15:00" <= currentTime <= "15:30:00":
        if currentTime[3:5] != lastMin and currentTime >= Utils.startTime:
            runLive.callback_method(client, currentTime)
            lastMin = currentTime[3:5]
        currentTime = datetime.now().strftime("%H:%M:%S")
        if runLive.mtmhit:
            break


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    Utils.logger.info("Starting the program")
    client = IB_APIS("http://localhost:21000")
    client.IB_Subscribe(Utils.indexExchange, Utils.indexToken, "")
    for i in range(4):
        pool.apply_async(runStrategy(i, client))

