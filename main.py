import asyncio
import time

import liveUtils
from PriceStream import PriceStream

import Utils
from Users import User
from runLive import Live
from datetime import datetime
from pyIB_APIS import IB_APIS

runLive = Live()


def runStrategy(client, priceDict):
    currentTime = datetime.now().strftime("%H:%M:%S")
    runLive.callback_method(client, currentTime, priceDict)


def main():
    # fath = User("fathima")
    Utils.logger.info("Starting the program")
    client = IB_APIS("http://localhost:21000")
    priceStream = PriceStream()
    priceStream.connect()
    time.sleep(5)
    while True:
        # current_time = datetime.now()
        # sleep_time = 60 - current_time.second - (current_time.microsecond / 1000000.0)
        # time.sleep(sleep_time)
        runStrategy(client, priceStream.priceDict)
        current_time = datetime.now()
        sleep_time = 60 - current_time.second - (current_time.microsecond / 1000000.0)
        time.sleep(sleep_time)
        if current_time.strftime("%H:%M:%S") > "24:30:00":
            break


if __name__ == '__main__':
    main()
