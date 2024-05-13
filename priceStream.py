import Utils

class priceStream:
    def __init__(self):
        self.brokerObject = None
        self.priceDict = {}
        self.expDate = Utils.expDate
