import Utils
import liveUtils
from runLive import Live
from datetime import datetime
from Users import User
from pyIB_APIS import IB_APIS


if __name__ == '__main__':
    client = IB_APIS("http://localhost:21000")
    client.IB_Subscribe("NSE", Utils.indexToken, "")
    runLive = Live(Utils.indexToken, client)
    currMin = None
    while "09:15:00" <= datetime.now().strftime("%H:%M:%S") <= "15:30:00":
        if datetime.now().strftime("%M") != currMin and datetime.now().strftime("%H:%M:%S") >= "09:45:00":
            runLive.callback_method(client)
            currMin = datetime.now().strftime("%M")
        if runLive.mtmhit:
            break

