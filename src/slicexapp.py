# ==================================================================================
#
#       Copyright (c) 2020 Samsung Electronics Co., Ltd. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ==================================================================================

from os import getenv
from ricxappframe.xapp_frame import RMRXapp, rmr

from .utils.constants import Constants
from .utils.type import RRMPolicy, E2NodeCommon
from .manager import *
from .handler import *

import schedule
import random
import json

class SliceXapp:

    def __init__(self):
        fake_sdl = getenv("USE_FAKE_SDL", False)
        self._rmr_xapp = RMRXapp(self._default_handler,
                                 config_handler=self._handle_config_change,
                                 rmr_port=4560,
                                 post_init=self._post_init,
                                 use_fake_sdl=bool(fake_sdl))
        self._rmr_xapp.logger.mdclog_format_init()

        self._rmr_xapp.logger.info("SliceXapp.__init__:: Invoke to initialize gRPC Control Request")
        self.grpc = GRPCHandler(Constants.RCXAPP_GRPC_SERVER_IP, Constants.RCXAPP_GRPC_SERVER_PORT)

    def _post_init(self, rmr_xapp):
        """
        Function that runs when xapp initialization is complete
        """
        a1_mgr = A1PolicyManager(rmr_xapp)
        a1_mgr.startup()

    def _handle_config_change(self, rmr_xapp, config):
        """
        Function that runs at start and on every configuration file change.
        """
        rmr_xapp.logger.info("SliceXapp.handle_config_change:: config: {}".format(config))
        rmr_xapp.config = config  # No mutex required due to GIL

    def _default_handler(self, rmr_xapp, summary, sbuf):
        """
        Function that processes messages for which no handler is defined
        """
        rmr_xapp.logger.info("SliceXapp.default_handler called for msg type = " +
                                   str(summary[rmr.RMR_MS_MSG_TYPE]))
        rmr_xapp.rmr_free(sbuf)

    def createHandlers(self):
        """
        Function that creates all the handlers for RMR Messages
        """
        self._rmr_xapp.logger.info("In createHandlers()")
        HealthCheckHandler(self._rmr_xapp, Constants.RIC_HEALTH_CHECK_REQ)
        self.a1Policy = A1PolicyHandler(self._rmr_xapp, Constants.A1_POLICY_REQ)

    def start(self, thread=True):
        """
        This is a convenience function that allows this xapp to run in Docker
        for "real" (no thread, real SDL), but also easily modified for unit testing
        (e.g., use_fake_sdl). The defaults for this function are for the Dockerized xapp.
        """
        self._rmr_xapp.logger.info("In start()")
        self.createHandlers()
        self._rmr_xapp.run(thread)
        self.entry()

    def stop(self):
        """
        can only be called if thread=True when started
        TODO: could we register a signal handler for Docker SIGTERM that calls this?
        """
        self._rmr_xapp.stop()

    def sendControlRequest(self):
        pass

    def getE2NodeInfo(self):
        e2NodeInfo = E2NodeCommon(
            ranName        = "gnb_311_048_00000001",
            ranFuncId      = 300
        )
        return e2NodeInfo

    def readData(self, numSlice=0):
        DRBUEThpDl = []
        for _ in range(numSlice):
            DRBUEThpDl.append(1000*random.random())

        return DRBUEThpDl

    def predict(self):
        """
        Read the data, calculate the PRB for each slice 
        """
        numSlice = self.a1Policy.getNumPolicy()
        policyList = self.a1Policy.getPolicy()

        self._rmr_xapp.logger.info("There are {} slice defined by A1 policy".format(numSlice))

        if numSlice == 0:
            self._rmr_xapp.logger.info("Skip PRB allocation due to no slice defined by A1 policy")
            return

        DrbUeThpDl = self.readData(numSlice)
        DedicatePrbRatio = []
    
        for i in range(len(DrbUeThpDl)):
            if i != len(DrbUeThpDl)-1:
                val = int((DrbUeThpDl[i]/sum(DrbUeThpDl))*100)
            else:
                val = 100 - sum(DedicatePrbRatio)
        
            DedicatePrbRatio.append(val)
        
        for i in range(len(DedicatePrbRatio)):
            self._rmr_xapp.logger.info("Slice {SliceId}: DedicatedPRBRatio = {DedicatPRBRatio}%"
                                       .format(SliceId=i+1, DedicatPRBRatio=DedicatePrbRatio[i]))
        
        v = 0
        rrmPolicyList = []
        for i in policyList:
            rrmPolicy = RRMPolicy(
                plmnId = policyList[i]["Member"]["PlmnId"],
                sst    = policyList[i]["Member"]["Sst"],
                sd     = policyList[i]["Member"]["Sd"],
                maxPRB = 100,
                minPRB = DedicatePrbRatio[v],
                dedPRB = DedicatePrbRatio[v]
            )
            v = v + 1
            rrmPolicyList.append(rrmPolicy)
        
        e2NodeInfo = self.getE2NodeInfo()
        self.grpc.send_control_req(e2NodeInfo, rrmPolicyList)

    def entry(self):
        """
        After xApp initialization finished, it enters this function. 
        This function is a loop, continuously check the A1 flag, entering the prediction
        for RRMPolicy if A1 flag is True, otherwise do nothing.
        """
        schedule.every(1).seconds.do(self.predict)
        while True:
            schedule.run_pending()