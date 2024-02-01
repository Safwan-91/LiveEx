import liveUtils
from runLive import Live
from datetime import datetime


if __name__ == '__main__':
    client = liveUtils.login()
    runLive = Live(client)
    while "09:28:00" <= datetime.now().strftime("%H:%M:%S") <= "15:29:00":
        runLive.callback_method(client)

