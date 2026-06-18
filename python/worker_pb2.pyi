import shared_pb2 as _shared_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecuteDataFunctionRequest(_message.Message):
    __slots__ = ("executionParameters", "workflowRunId", "uri")
    EXECUTIONPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    WORKFLOWRUNID_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    executionParameters: str
    workflowRunId: str
    uri: str
    def __init__(self, executionParameters: _Optional[str] = ..., workflowRunId: _Optional[str] = ..., uri: _Optional[str] = ...) -> None: ...

class ExecuteDataFunctionResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: _shared_pb2.ExecutionStatus
    message: str
    def __init__(self, status: _Optional[_Union[_shared_pb2.ExecutionStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class ExecuteWorkflowSegmentRequest(_message.Message):
    __slots__ = ("workflowRunId", "executionParameters", "dataUri", "tasks")
    WORKFLOWRUNID_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    DATAURI_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    workflowRunId: str
    executionParameters: str
    dataUri: str
    tasks: _containers.RepeatedCompositeFieldContainer[WorkflowTask]
    def __init__(self, workflowRunId: _Optional[str] = ..., executionParameters: _Optional[str] = ..., dataUri: _Optional[str] = ..., tasks: _Optional[_Iterable[_Union[WorkflowTask, _Mapping]]] = ...) -> None: ...

class ExecuteWorkflowSegmentResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: _shared_pb2.ExecutionStatus
    message: str
    def __init__(self, status: _Optional[_Union[_shared_pb2.ExecutionStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class WorkflowTask(_message.Message):
    __slots__ = ("taskName", "parameters")
    TASKNAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    taskName: str
    parameters: str
    def __init__(self, taskName: _Optional[str] = ..., parameters: _Optional[str] = ...) -> None: ...

class HeartbeatRequest(_message.Message):
    __slots__ = ("workerId",)
    WORKERID_FIELD_NUMBER: _ClassVar[int]
    workerId: str
    def __init__(self, workerId: _Optional[str] = ...) -> None: ...

class HeartbeatResponse(_message.Message):
    __slots__ = ("alive",)
    ALIVE_FIELD_NUMBER: _ClassVar[int]
    alive: bool
    def __init__(self, alive: bool = ...) -> None: ...
