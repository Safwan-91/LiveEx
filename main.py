import Utils
import liveUtils
from runLive import Live
from datetime import datetime
from Users import User
from pyIB_APIS import IB_APIS


if __name__ == '__main__':
    client = IB_APIS("http://localhost:21000")
    client.IB_Subscribe("NSE", Utils.index, "")
    runLive = Live(Utils.indexToken)
    currMin = None
    while "00:00:00" <= datetime.now().strftime("%H:%M:%S") <= "24:29:00":
        if datetime.now().strftime("%M") != currMin:# and datetime.now().strftime("%H:%M:%S") >= "09:45:00":
            runLive.callback_method(client)
            currMin = datetime.now().strftime("%M")
        if runLive.mtmhit:
            break

