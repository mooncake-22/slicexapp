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
        RicControlGrpcReq = rc_pb2.RICControlRequest_RRMPolicy(
            ranName   = e2NodeCommon.ranName
        )

        for v in rrmPolicyList:
            rrmPolicy = rc_pb2.RrmPolicy(
                minPRB = v.minPRB,
                maxPRB = v.maxPRB,
                dedPRB = v.dedPRB
            )

            member = rc_pb2.Member(
                plmnId = v.plmnId,
                sst = v.sst,
                sd = v.sd
            )

            rrmPolicy.member.append(member)
            
            RicControlGrpcReq.rrmPolicy.append(rrmPolicy)

        print(RicControlGrpcReq)

        try:
            resp = self.stub.SendRRMPolicyServiceGrpc(RicControlGrpcReq)
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
