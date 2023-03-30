import rc_pb2 as rc
import rc_pb2_grpc as rcGrpc
import grpc 

if __name__ == "__main__":
    member = rc.Member(plmnId="311048",sst="01",sd="020304")
    rrmPolicy = rc.RrmPolicy(minPRB = 25, maxPRB = 85, dedPRB = 15)
    rrmPolicy.member.append(member)
    RICControlRequest=rc.RICControlRequest_RRMPolicy(
        ranName = "gnb_311_048_00000001",
        ranFuncId = 1
    )
    RICControlRequest.rrmPolicy.append(rrmPolicy)

    ip = "service-ricxapp-rc-grpc-server.ricxapp.svc.cluster.local"
    port= "7777"
    channel = grpc.insecure_channel(ip+":"+port)
    stub = rcGrpc.MsgCommStub(channel)
    resp = stub.SendRICControlReqServiceGrpc(RICControlRequest)
