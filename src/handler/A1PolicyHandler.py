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

import json
from ricxappframe.xapp_frame import RMRXapp, rmr
from ..utils.constants import Constants
from ._BaseHandler import _BaseHandler


class A1PolicyHandler(_BaseHandler):

    def __init__(self, rmr_xapp: RMRXapp, msgtype):
        """
        ex: 
        policyId: 
        - example: 76bc6b34-3be6-44fe-8367-a790d503ec6f

        sliceId: 
        - rule: sliceId[policyId] = plmnId-sst-sd
        - example: 331f01-002-00000001

        policy: 
        - rule: policy[policyId] = payload
        - example:
        """
        super().__init__(rmr_xapp, msgtype)
        self.policyId = []
        self.sliceId  = {}
        self.policy   = {} 

    def request_handler(self, rmr_xapp, summary, sbuf):
        self._rmr_xapp.rmr_free(sbuf)
        try:
            req = json.loads(summary[rmr.RMR_MS_PAYLOAD])  # input should be a json encoded as bytes
            self.logger.debug("A1PolicyHandler.resp_handler:: Handler processing request")
        except (json.decoder.JSONDecodeError, KeyError):
            self.logger.error("A1PolicyManager.resp_handler:: Handler failed to parse request")
            return
        
        self.logger.info("A1PolicyHandler.resp_handler:: Handler processed request: {}".format(req))
        if self.verifyPolicy(req):
            self.logger.debug("A1PolicyHandler.resp_handler:: Request verification success: {}".format(req))
        else:
            self.logger.error("A1PolicyHandler.resp_handler:: Request verification failed: {}".format(req))
            return
        
        self.logger.info("A1PolicyHandler.resp_handler:: Handler handle policy payload")
        if self.handlePolicy(req):
            self.logger.debug("A1PolicyHandler.resp_handler:: Policy payload handled successfully")
            resp = self.buildSuccessPolicyResp(req)
        else:
            self.logger.error("A1PolicyHandler.resp_handler:: Policy payload handled failed")
            resp = self.buildErrorPolicyResp(req)
        
        self._rmr_xapp.rmr_send(json.dumps(resp).encode(), Constants.A1_POLICY_RESP)
        self.logger.info("A1PolicyHandler.resp_handler:: Response sent: {}".format(resp))

    def verifyPolicy(self, req: dict):
        for i in ["policy_type_id", "operation", "policy_instance_id"]:
            if i not in req:
                return False
        return True
    
    def extractSliceId(self, req: dict):
        member = req["payload"]["Member"]
        return member["PlmnId"]+"-"+member["Sst"]+"-"+member["Sd"]

    def buildSuccessPolicyResp(self, req: dict):
        req["handler_id"] = self._rmr_xapp.config["name"]
        del req["operation"]
        req["status"] = "OK"
        return req
    
    def buildErrorPolicyResp(self, req: dict):
        req["handler_id"] = self._rmr_xapp.config["name"]
        del req["operation"]
        req["status"] = "ERROR"
        return req

    def getNumPolicy(self):
        return len(self.policy)
    
    def getPolicy(self):
        return self.policy

    def createPolicy(self, req: dict):
        # Make sure each sliceId is only shown one time.
        id = req["policy_instance_id"]
        sliceId = self.extractSliceId(req)
        if sliceId in self.policy:
            self.logger.error("A1PolicyHandler.createPolicy:: Failed to create the policy for policy_instance_id: {} due to the sliceId: {} has already exist".format(id, sliceId))
            return False
        
        # Make sure policy instance id is new to be added.
        if id not in self.policyId:
            self.policyId.append(id)
            self.sliceId[id]     = sliceId
            self.policy[sliceId] = req["payload"]
            self.logger.debug("A1PolicyHandler.createPolicy:: Successfully create the policy for policy_instance_id: {}".format(id))
            return True
        else:
            self.logger.error("A1PolicyHandler.createPolicy:: Failed to create the policy for policy_instance_id: {}".format(id))
            return False
        
    def updatePolicy(self, req: dict):
        # Make sure sliceId will not changed through policy update.
        id = req["policy_instance_id"]
        sliceId = self.extractSliceId(req)
        if sliceId != self.sliceId[id]:
            self.logger.error("A1PolicyHandler.updatePolicy:: Failed to update the policy due to sliceId changed: {} -> {}".format(id, sliceId))
            return False
        
        if id in self.policyId:
            self.policy[sliceId] = req["payload"]
            self.logger.debug("A1PolicyHandler.updatePolicy:: Successfully update the policy for policy_instance_id: {}".format(id))
            return True
        else:
            self.logger.error("A1PolicyHandler.updatePolicy:: Failed to update the policy for policy_instance_id: {}".format(id))
            return False

    def deletePolicy(self,req: dict):
        id = req["policy_instance_id"]
        if id in self.policyId:
            self.policyId.remove(id)
            sliceId = self.sliceId.pop(id)
            self.policy.pop(sliceId)
            self.logger.debug("A1PolicyHandler.deletePolicy:: Successfully delete the policy for policy_instance_id: {}".format(id))
            return True
        else:
            self.logger.error("A1PolicyHandler.deletePolicy:: Failed to delete the policy for policy_instance_id: {}".format(id))
            return False

    def handlePolicy(self, req: dict):
        op = req["operation"]
        result = False

        if op == "CREATE":
            result = self.createPolicy(req)
        elif op == "UPDATE":
            result = self.updatePolicy(req)
        elif op == "DELETE":
            result = self.deletePolicy(req)
        else:
            self.logger.error("A1PolicyHandler.handlePolicy:: Receive undefined operation: {}".format(op))
        
        return result
