import Utils
from runLive import Live
from datetime import datetime
from pyIB_APIS import IB_APIS


if __name__ == '__main__':
    Utils.logger.info("Starting the program")
    client = IB_APIS("http://localhost:21000")
    client.IB_Subscribe(Utils.indexExchange, Utils.indexToken, "")
    runLive = Live()
    currentTime = datetime.now().strftime("%H:%M:%S")
    lastMin = None
    while "09:15:00" <= currentTime <= "15:30:00":
        if currentTime[3:5] != lastMin and currentTime >= "09:44:00":
            runLive.callback_method(client, currentTime)
            lastMin = currentTime[3:5]
        if runLive.mtmhit:
            break

