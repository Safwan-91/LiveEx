import time

from PriceStream import PriceStream

import Utils
from runLive import Live
from datetime import datetime

runLive = Live()


def runStrategy(priceDict):
    currentTime = datetime.now().strftime("%H:%M:%S")
    runLive.callback_method(currentTime, priceDict)


def main():
    Utils.logger.info("Starting the program")
    priceStream = PriceStream()
    priceStream.connect()
    time.sleep(10)
    while True:
        # current_time = datetime.now()
        # sleep_time = 60 - current_time.second - (current_time.microsecond / 1000000.0)
        # time.sleep(sleep_time)
        runStrategy(priceStream.priceDict)
        current_time = datetime.now()
        sleep_time = 60 - current_time.second - (current_time.microsecond / 1000000.0)
        time.sleep(sleep_time)
        if current_time.strftime("%H:%M:%S") > "24:30:00":
            break


if __name__ == '__main__':
    main()
