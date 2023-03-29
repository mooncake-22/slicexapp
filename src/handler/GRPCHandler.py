import grpc
from typing import List
from ..utils.protobuf import rc_pb2
from ..utils.protobuf import rc_pb2_grpc
from ..utils import type

class GRPCHandler(object):
    def __init__(self, ip = "", port = ""):
        channel   = grpc.insecure_channel(ip + ":" + port)
        self.stub = rc_pb2_grpc.MsgCommStub(channel)

    def send_control_req(self, e2NodeCommon: type.E2NodeCommon, rrmPolicyList: List[type.RRMPolicy]):
        """
        This function helps to send the gRPC request with protocol buffer parameters.
        """
        RicControlGrpcReq = rc_pb2.RicControlGrpcReq(
            e2NodeID = e2NodeCommon.e2NodeId,
            plmnID   = e2NodeCommon.plmnId,
            ranName  = e2NodeCommon.ranName,

            RICE2APHeaderData = rc_pb2.RICE2APHeader(
                RanFuncId      = e2NodeCommon.ranFuncId,
                RICRequestorID = e2NodeCommon.ricRequestorId
            ),

            RICControlHeaderData = rc_pb2.RICControlHeader( 
                ControlStyle    = 2,
                ControlActionId = 6
            ),

            RICControlMessageData = self.packRicControlMessage(rrmPolicyList)
        )
        print(RicControlGrpcReq)
        try:
            resp = self.stub.SendRICControlReqServiceGrpc(RicControlGrpcReq)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.OK:
                print("GRPCHandler.send_control_req:: Successfully send the gRPC request to server")
                return True
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                print("GRPCHandler.send_control_req:: Failed to send the gRPC request to server due to server unavailable")
                return False
            else:
                print(f"GRPCHandler.send_control_req:: Received unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                return False
         
    
    def packRicControlMessage(self, rrmPolicyList: List[type.RRMPolicy]):
        """
        This function helps to pack the rrmPolicylist into RICControlMessage in protocol buffer definition.
        """
        RICControlMessageData = rc_pb2.RICControlMessage()

        for v in rrmPolicyList:
            policy = rc_pb2.Policy(minPRB = v.minPRB, maxPRB = v.maxPRB, dedPRB = v.dedPRB)
            member = rc_pb2.Member(plmnId = v.plmnId, sst = v.sst, sd = v.sd)
            policy.member.append(member)
            RICControlMessageData.policy.append(policy)
    
        return RICControlMessageData




