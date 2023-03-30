from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
RIC_CONTROL_ACK: RICControlAckEnum
RIC_CONTROL_ACK_UNKWON: RICControlAckEnum
RIC_CONTROL_CELL_UNKWON: RICControlCellTypeEnum
RIC_CONTROL_EUTRAN_CELL: RICControlCellTypeEnum
RIC_CONTROL_NACK: RICControlAckEnum
RIC_CONTROL_NO_ACK: RICControlAckEnum
RIC_CONTROL_NR_CELL: RICControlCellTypeEnum

class Guami(_message.Message):
    __slots__ = ["aMFPointer", "aMFRegionID", "aMFSetID", "pLMNIdentity"]
    AMFPOINTER_FIELD_NUMBER: _ClassVar[int]
    AMFREGIONID_FIELD_NUMBER: _ClassVar[int]
    AMFSETID_FIELD_NUMBER: _ClassVar[int]
    PLMNIDENTITY_FIELD_NUMBER: _ClassVar[int]
    aMFPointer: str
    aMFRegionID: str
    aMFSetID: str
    pLMNIdentity: str
    def __init__(self, pLMNIdentity: _Optional[str] = ..., aMFRegionID: _Optional[str] = ..., aMFSetID: _Optional[str] = ..., aMFPointer: _Optional[str] = ...) -> None: ...

class Member(_message.Message):
    __slots__ = ["plmnId", "sd", "sst"]
    PLMNID_FIELD_NUMBER: _ClassVar[int]
    SD_FIELD_NUMBER: _ClassVar[int]
    SST_FIELD_NUMBER: _ClassVar[int]
    plmnId: str
    sd: str
    sst: str
    def __init__(self, plmnId: _Optional[str] = ..., sst: _Optional[str] = ..., sd: _Optional[str] = ...) -> None: ...

class RICControlHeader(_message.Message):
    __slots__ = ["ControlActionId", "ControlStyle", "UEID"]
    CONTROLACTIONID_FIELD_NUMBER: _ClassVar[int]
    CONTROLSTYLE_FIELD_NUMBER: _ClassVar[int]
    ControlActionId: int
    ControlStyle: int
    UEID: UeId
    UEID_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, ControlStyle: _Optional[int] = ..., ControlActionId: _Optional[int] = ..., UEID: _Optional[_Union[UeId, _Mapping]] = ...) -> None: ...

class RICControlMessage(_message.Message):
    __slots__ = ["RICControlCellTypeVal", "TargetCellID"]
    RICCONTROLCELLTYPEVAL_FIELD_NUMBER: _ClassVar[int]
    RICControlCellTypeVal: RICControlCellTypeEnum
    TARGETCELLID_FIELD_NUMBER: _ClassVar[int]
    TargetCellID: str
    def __init__(self, RICControlCellTypeVal: _Optional[_Union[RICControlCellTypeEnum, str]] = ..., TargetCellID: _Optional[str] = ...) -> None: ...

class RICControlRequest_RRMPolicy(_message.Message):
    __slots__ = ["ranFuncId", "ranName", "rrmPolicy"]
    RANFUNCID_FIELD_NUMBER: _ClassVar[int]
    RANNAME_FIELD_NUMBER: _ClassVar[int]
    RRMPOLICY_FIELD_NUMBER: _ClassVar[int]
    ranFuncId: int
    ranName: str
    rrmPolicy: _containers.RepeatedCompositeFieldContainer[RrmPolicy]
    def __init__(self, ranName: _Optional[str] = ..., ranFuncId: _Optional[int] = ..., rrmPolicy: _Optional[_Iterable[_Union[RrmPolicy, _Mapping]]] = ...) -> None: ...

class RICE2APHeader(_message.Message):
    __slots__ = ["RICRequestorID", "RanFuncId"]
    RANFUNCID_FIELD_NUMBER: _ClassVar[int]
    RICREQUESTORID_FIELD_NUMBER: _ClassVar[int]
    RICRequestorID: int
    RanFuncId: int
    def __init__(self, RanFuncId: _Optional[int] = ..., RICRequestorID: _Optional[int] = ...) -> None: ...

class RicControlGrpcReq(_message.Message):
    __slots__ = ["RICControlAckReqVal", "RICControlHeaderData", "RICControlMessageData", "RICE2APHeaderData", "e2NodeID", "plmnID", "ranName"]
    E2NODEID_FIELD_NUMBER: _ClassVar[int]
    PLMNID_FIELD_NUMBER: _ClassVar[int]
    RANNAME_FIELD_NUMBER: _ClassVar[int]
    RICCONTROLACKREQVAL_FIELD_NUMBER: _ClassVar[int]
    RICCONTROLHEADERDATA_FIELD_NUMBER: _ClassVar[int]
    RICCONTROLMESSAGEDATA_FIELD_NUMBER: _ClassVar[int]
    RICControlAckReqVal: RICControlAckEnum
    RICControlHeaderData: RICControlHeader
    RICControlMessageData: RICControlMessage
    RICE2APHEADERDATA_FIELD_NUMBER: _ClassVar[int]
    RICE2APHeaderData: RICE2APHeader
    e2NodeID: str
    plmnID: str
    ranName: str
    def __init__(self, e2NodeID: _Optional[str] = ..., plmnID: _Optional[str] = ..., ranName: _Optional[str] = ..., RICE2APHeaderData: _Optional[_Union[RICE2APHeader, _Mapping]] = ..., RICControlHeaderData: _Optional[_Union[RICControlHeader, _Mapping]] = ..., RICControlMessageData: _Optional[_Union[RICControlMessage, _Mapping]] = ..., RICControlAckReqVal: _Optional[_Union[RICControlAckEnum, str]] = ...) -> None: ...

class RicControlGrpcRsp(_message.Message):
    __slots__ = ["description", "rspCode"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RSPCODE_FIELD_NUMBER: _ClassVar[int]
    description: str
    rspCode: int
    def __init__(self, rspCode: _Optional[int] = ..., description: _Optional[str] = ...) -> None: ...

class RrmPolicy(_message.Message):
    __slots__ = ["dedPRB", "maxPRB", "member", "minPRB"]
    DEDPRB_FIELD_NUMBER: _ClassVar[int]
    MAXPRB_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    MINPRB_FIELD_NUMBER: _ClassVar[int]
    dedPRB: int
    maxPRB: int
    member: _containers.RepeatedCompositeFieldContainer[Member]
    minPRB: int
    def __init__(self, member: _Optional[_Iterable[_Union[Member, _Mapping]]] = ..., minPRB: _Optional[int] = ..., maxPRB: _Optional[int] = ..., dedPRB: _Optional[int] = ...) -> None: ...

class UeId(_message.Message):
    __slots__ = ["GnbUEID"]
    GNBUEID_FIELD_NUMBER: _ClassVar[int]
    GnbUEID: gNBUEID
    def __init__(self, GnbUEID: _Optional[_Union[gNBUEID, _Mapping]] = ...) -> None: ...

class gNBUEID(_message.Message):
    __slots__ = ["amfUENGAPID", "gNBCUCPUEE1APID", "gNBCUUEF1APID", "guami"]
    AMFUENGAPID_FIELD_NUMBER: _ClassVar[int]
    GNBCUCPUEE1APID_FIELD_NUMBER: _ClassVar[int]
    GNBCUUEF1APID_FIELD_NUMBER: _ClassVar[int]
    GUAMI_FIELD_NUMBER: _ClassVar[int]
    amfUENGAPID: int
    gNBCUCPUEE1APID: _containers.RepeatedScalarFieldContainer[int]
    gNBCUUEF1APID: _containers.RepeatedScalarFieldContainer[int]
    guami: Guami
    def __init__(self, amfUENGAPID: _Optional[int] = ..., guami: _Optional[_Union[Guami, _Mapping]] = ..., gNBCUUEF1APID: _Optional[_Iterable[int]] = ..., gNBCUCPUEE1APID: _Optional[_Iterable[int]] = ...) -> None: ...

class RICControlCellTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RICControlAckEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
