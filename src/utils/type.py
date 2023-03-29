class E2NodeCommon():
    def __init__(self, e2NodeId="", plmnId="", ranName="", ranFuncId: int = 0, ricRequestorId: int = 0):
        self.e2NodeId       = e2NodeId
        self.plmnId         = plmnId
        self.ranName        = ranName
        self.ranFuncId      = ranFuncId
        self.ricRequestorId = ricRequestorId

class RRMPolicy():
    def __init__(self, plmnId="", sst="", sd="", maxPRB: int = 100, minPRB: int = 100, dedPRB: int = 0):
        self.plmnId = plmnId
        self.sst    = sst
        self.sd     = sd
        self.maxPRB = maxPRB
        self.minPRB = minPRB
        self.dedPRB = dedPRB