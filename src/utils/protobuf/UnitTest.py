import rc_pb2 as rc
import rc_pb2_grpc as rcGrpc
import grpc 

if __name__ == "__main__":
    member = rc.Member(plmnId="311048",sst="01",sd="020304")
    policy = rc.Policy(minPRB = 25, maxPRB = 85, dedPRB = 15)
    policy.member.append(member)
    RICControlMessageData=rc.RICControlMessage()
    RICControlMessageData.policy.append(policy)

    RicControlGrpcReq = rc.RicControlGrpcReq(
                e2NodeID="00000001",
                plmnID="13f184",
                ranName="gnb_311_048_00000001",
                RICE2APHeaderData=rc.RICE2APHeader(
                    RanFuncId=300,
                    RICRequestorID=2
                ),
                RICControlHeaderData=rc.RICControlHeader(
                    ControlStyle=2,
                    ControlActionId=6
                ),
                RICControlMessageData=RICControlMessageData
    )

    ip = "service-ricxapp-rc-grpc-server.ricxapp.svc.cluster.local"
    port= "7777"
    channel = grpc.insecure_channel(ip+":"+port)
    stub = rcGrpc.MsgCommStub(channel)
    resp = stub.SendRICControlReqServiceGrpc(RicControlGrpcReq)
