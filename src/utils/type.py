class E2NodeCommon():
    def __init__(self, ranName="", ranFuncId: int = 0):
        self.ranName        = ranName
        self.ranFuncId      = ranFuncId

class RRMPolicy():
    def __init__(self, plmnId="", sst="", sd="", maxPRB: int = 100, minPRB: int = 100, dedPRB: int = 0):
        self.plmnId = plmnId
        self.sst    = sst
        self.sd     = sd
        self.maxPRB = maxPRB
        self.minPRB = minPRB
        self.dedPRB = dedPRB