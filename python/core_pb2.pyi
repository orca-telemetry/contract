from google.protobuf import timestamp_pb2 as _timestamp_pb2
import shared_pb2 as _shared_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Comparator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMPARATOR_UNSPECIFIED: _ClassVar[Comparator]
    EQ: _ClassVar[Comparator]
    NEQ: _ClassVar[Comparator]
    GT: _ClassVar[Comparator]
    GTE: _ClassVar[Comparator]
    LT: _ClassVar[Comparator]
    LTE: _ClassVar[Comparator]
    IN: _ClassVar[Comparator]
    NOT_IN: _ClassVar[Comparator]
    EXISTS: _ClassVar[Comparator]
    NOT_EXISTS: _ClassVar[Comparator]
    CONTAINS: _ClassVar[Comparator]
    PREFIX: _ClassVar[Comparator]

class DataSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_SOURCE_UNSPECIFIED: _ClassVar[DataSource]
    RESULT: _ClassVar[DataSource]
    EXECUTION_PARAMETERS: _ClassVar[DataSource]

class SortDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_DIRECTION_UNSPECIFIED: _ClassVar[SortDirection]
    ASC: _ClassVar[SortDirection]
    DESC: _ClassVar[SortDirection]
COMPARATOR_UNSPECIFIED: Comparator
EQ: Comparator
NEQ: Comparator
GT: Comparator
GTE: Comparator
LT: Comparator
LTE: Comparator
IN: Comparator
NOT_IN: Comparator
EXISTS: Comparator
NOT_EXISTS: Comparator
CONTAINS: Comparator
PREFIX: Comparator
DATA_SOURCE_UNSPECIFIED: DataSource
RESULT: DataSource
EXECUTION_PARAMETERS: DataSource
SORT_DIRECTION_UNSPECIFIED: SortDirection
ASC: SortDirection
DESC: SortDirection

class DataFunction(_message.Message):
    __slots__ = ("name", "hash", "inputModel", "outputModel", "settings")
    NAME_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    INPUTMODEL_FIELD_NUMBER: _ClassVar[int]
    OUTPUTMODEL_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    hash: str
    inputModel: bytes
    outputModel: bytes
    settings: _shared_pb2.DataFunctionSettings
    def __init__(self, name: _Optional[str] = ..., hash: _Optional[str] = ..., inputModel: _Optional[bytes] = ..., outputModel: _Optional[bytes] = ..., settings: _Optional[_Union[_shared_pb2.DataFunctionSettings, _Mapping]] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ("taskHash", "name", "description", "executionSettings", "inputModel", "outputModel", "requiredDataFunctions")
    TASKHASH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONSETTINGS_FIELD_NUMBER: _ClassVar[int]
    INPUTMODEL_FIELD_NUMBER: _ClassVar[int]
    OUTPUTMODEL_FIELD_NUMBER: _ClassVar[int]
    REQUIREDDATAFUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    taskHash: str
    name: str
    description: str
    executionSettings: _shared_pb2.TaskExecutionSettings
    inputModel: bytes
    outputModel: bytes
    requiredDataFunctions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, taskHash: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., executionSettings: _Optional[_Union[_shared_pb2.TaskExecutionSettings, _Mapping]] = ..., inputModel: _Optional[bytes] = ..., outputModel: _Optional[bytes] = ..., requiredDataFunctions: _Optional[_Iterable[str]] = ...) -> None: ...

class WorkflowEdge(_message.Message):
    __slots__ = ("fromTaskName", "fromTaskHash", "fromTaskWorker", "toTaskName", "toTaskHash", "toTaskWorker")
    FROMTASKNAME_FIELD_NUMBER: _ClassVar[int]
    FROMTASKHASH_FIELD_NUMBER: _ClassVar[int]
    FROMTASKWORKER_FIELD_NUMBER: _ClassVar[int]
    TOTASKNAME_FIELD_NUMBER: _ClassVar[int]
    TOTASKHASH_FIELD_NUMBER: _ClassVar[int]
    TOTASKWORKER_FIELD_NUMBER: _ClassVar[int]
    fromTaskName: str
    fromTaskHash: str
    fromTaskWorker: str
    toTaskName: str
    toTaskHash: str
    toTaskWorker: str
    def __init__(self, fromTaskName: _Optional[str] = ..., fromTaskHash: _Optional[str] = ..., fromTaskWorker: _Optional[str] = ..., toTaskName: _Optional[str] = ..., toTaskHash: _Optional[str] = ..., toTaskWorker: _Optional[str] = ...) -> None: ...

class Workflow(_message.Message):
    __slots__ = ("workflowName", "description", "workflowHash", "edges", "executionSettings", "inputModel", "haltOnFailure")
    WORKFLOWNAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    WORKFLOWHASH_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONSETTINGS_FIELD_NUMBER: _ClassVar[int]
    INPUTMODEL_FIELD_NUMBER: _ClassVar[int]
    HALTONFAILURE_FIELD_NUMBER: _ClassVar[int]
    workflowName: str
    description: str
    workflowHash: str
    edges: _containers.RepeatedCompositeFieldContainer[WorkflowEdge]
    executionSettings: _shared_pb2.WorkflowExecutionSettings
    inputModel: bytes
    haltOnFailure: bool
    def __init__(self, workflowName: _Optional[str] = ..., description: _Optional[str] = ..., workflowHash: _Optional[str] = ..., edges: _Optional[_Iterable[_Union[WorkflowEdge, _Mapping]]] = ..., executionSettings: _Optional[_Union[_shared_pb2.WorkflowExecutionSettings, _Mapping]] = ..., inputModel: _Optional[bytes] = ..., haltOnFailure: bool = ...) -> None: ...

class RegisterWorkerRequest(_message.Message):
    __slots__ = ("public_key",)
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    public_key: bytes
    def __init__(self, public_key: _Optional[bytes] = ...) -> None: ...

class RegisterWorkerResponse(_message.Message):
    __slots__ = ("worker_id", "nonce_id")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    NONCE_ID_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    nonce_id: str
    def __init__(self, worker_id: _Optional[str] = ..., nonce_id: _Optional[str] = ...) -> None: ...

class GetNonceRequest(_message.Message):
    __slots__ = ("worker_id",)
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    def __init__(self, worker_id: _Optional[str] = ...) -> None: ...

class GetNonceResponse(_message.Message):
    __slots__ = ("challenge",)
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    challenge: bytes
    def __init__(self, challenge: _Optional[bytes] = ...) -> None: ...

class CheckNonceRequest(_message.Message):
    __slots__ = ("signed_challenge", "worker_id", "nonce_id")
    SIGNED_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    NONCE_ID_FIELD_NUMBER: _ClassVar[int]
    signed_challenge: bytes
    worker_id: str
    nonce_id: str
    def __init__(self, signed_challenge: _Optional[bytes] = ..., worker_id: _Optional[str] = ..., nonce_id: _Optional[str] = ...) -> None: ...

class CheckNonceResponse(_message.Message):
    __slots__ = ("expires_at", "access_key")
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    expires_at: _timestamp_pb2.Timestamp
    access_key: bytes
    def __init__(self, expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., access_key: _Optional[bytes] = ...) -> None: ...

class RegisterWorkerSnapshotRequest(_message.Message):
    __slots__ = ("gitCommitHash", "dataFunctions", "tasks", "workflows")
    GITCOMMITHASH_FIELD_NUMBER: _ClassVar[int]
    DATAFUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    gitCommitHash: str
    dataFunctions: _containers.RepeatedCompositeFieldContainer[DataFunction]
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    workflows: _containers.RepeatedCompositeFieldContainer[Workflow]
    def __init__(self, gitCommitHash: _Optional[str] = ..., dataFunctions: _Optional[_Iterable[_Union[DataFunction, _Mapping]]] = ..., tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ..., workflows: _Optional[_Iterable[_Union[Workflow, _Mapping]]] = ...) -> None: ...

class RegisterWorkerSnapshotResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RegisterServingRequest(_message.Message):
    __slots__ = ("connectionUrl", "isServing")
    CONNECTIONURL_FIELD_NUMBER: _ClassVar[int]
    ISSERVING_FIELD_NUMBER: _ClassVar[int]
    connectionUrl: str
    isServing: bool
    def __init__(self, connectionUrl: _Optional[str] = ..., isServing: bool = ...) -> None: ...

class RegisterServingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TriggerWorkflowRequest(_message.Message):
    __slots__ = ("workflowName", "logicalDate", "executionParameters", "triggerSource")
    WORKFLOWNAME_FIELD_NUMBER: _ClassVar[int]
    LOGICALDATE_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    TRIGGERSOURCE_FIELD_NUMBER: _ClassVar[int]
    workflowName: str
    logicalDate: _timestamp_pb2.Timestamp
    executionParameters: str
    triggerSource: _shared_pb2.TriggerSource
    def __init__(self, workflowName: _Optional[str] = ..., logicalDate: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., executionParameters: _Optional[str] = ..., triggerSource: _Optional[_Union[_shared_pb2.TriggerSource, str]] = ...) -> None: ...

class TriggerWorkflowResponse(_message.Message):
    __slots__ = ("workflowRunId", "status", "message")
    WORKFLOWRUNID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    workflowRunId: str
    status: _shared_pb2.TriggerStatus
    message: str
    def __init__(self, workflowRunId: _Optional[str] = ..., status: _Optional[_Union[_shared_pb2.TriggerStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class RegisterDataFunctionCompletionRequest(_message.Message):
    __slots__ = ("workflowRunId", "status", "message")
    WORKFLOWRUNID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    workflowRunId: str
    status: _shared_pb2.ExecutionStatus
    message: str
    def __init__(self, workflowRunId: _Optional[str] = ..., status: _Optional[_Union[_shared_pb2.ExecutionStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class RegisterDataFunctionCompletionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RegisterTaskResultRequest(_message.Message):
    __slots__ = ("workflowRunId", "taskName", "result", "status", "message", "computeMetrics")
    WORKFLOWRUNID_FIELD_NUMBER: _ClassVar[int]
    TASKNAME_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    COMPUTEMETRICS_FIELD_NUMBER: _ClassVar[int]
    workflowRunId: str
    taskName: str
    result: str
    status: _shared_pb2.ExecutionStatus
    message: str
    computeMetrics: _shared_pb2.ComputeMetrics
    def __init__(self, workflowRunId: _Optional[str] = ..., taskName: _Optional[str] = ..., result: _Optional[str] = ..., status: _Optional[_Union[_shared_pb2.ExecutionStatus, str]] = ..., message: _Optional[str] = ..., computeMetrics: _Optional[_Union[_shared_pb2.ComputeMetrics, _Mapping]] = ...) -> None: ...

class RegisterTaskResultResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExposeStateRequest(_message.Message):
    __slots__ = ("gitCommitHash", "timestamp", "codebase")
    GITCOMMITHASH_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CODEBASE_FIELD_NUMBER: _ClassVar[int]
    gitCommitHash: str
    timestamp: _timestamp_pb2.Timestamp
    codebase: str
    def __init__(self, gitCommitHash: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., codebase: _Optional[str] = ...) -> None: ...

class ExposeStateResponse(_message.Message):
    __slots__ = ("tasks", "workflows", "dataFunctions")
    TASKS_FIELD_NUMBER: _ClassVar[int]
    WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    DATAFUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    workflows: _containers.RepeatedCompositeFieldContainer[Workflow]
    dataFunctions: _containers.RepeatedCompositeFieldContainer[DataFunction]
    def __init__(self, tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ..., workflows: _Optional[_Iterable[_Union[Workflow, _Mapping]]] = ..., dataFunctions: _Optional[_Iterable[_Union[DataFunction, _Mapping]]] = ...) -> None: ...

class QueryTaskRequest(_message.Message):
    __slots__ = ("name", "execution_parameter_filters", "result_filters", "order_by", "result_fields", "page_size", "page_token")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_PARAMETER_FILTERS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FILTERS_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    name: str
    execution_parameter_filters: _containers.RepeatedCompositeFieldContainer[FilterGroup]
    result_filters: _containers.RepeatedCompositeFieldContainer[FilterGroup]
    order_by: _containers.RepeatedCompositeFieldContainer[OrderByStatement]
    result_fields: _containers.RepeatedScalarFieldContainer[str]
    page_size: int
    page_token: str
    def __init__(self, name: _Optional[str] = ..., execution_parameter_filters: _Optional[_Iterable[_Union[FilterGroup, _Mapping]]] = ..., result_filters: _Optional[_Iterable[_Union[FilterGroup, _Mapping]]] = ..., order_by: _Optional[_Iterable[_Union[OrderByStatement, _Mapping]]] = ..., result_fields: _Optional[_Iterable[str]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class QueryTaskResponse(_message.Message):
    __slots__ = ("results", "next_page_token")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[TaskResult]
    next_page_token: str
    def __init__(self, results: _Optional[_Iterable[_Union[TaskResult, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class TaskResult(_message.Message):
    __slots__ = ("name", "execution_parameters", "result")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    name: str
    execution_parameters: str
    result: str
    def __init__(self, name: _Optional[str] = ..., execution_parameters: _Optional[str] = ..., result: _Optional[str] = ...) -> None: ...

class FilterGroup(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.RepeatedCompositeFieldContainer[LeafFilter]
    def __init__(self, filters: _Optional[_Iterable[_Union[LeafFilter, _Mapping]]] = ...) -> None: ...

class LeafFilter(_message.Message):
    __slots__ = ("key", "comparator", "value", "values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    COMPARATOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    key: str
    comparator: Comparator
    value: str
    values: StringList
    def __init__(self, key: _Optional[str] = ..., comparator: _Optional[_Union[Comparator, str]] = ..., value: _Optional[str] = ..., values: _Optional[_Union[StringList, _Mapping]] = ...) -> None: ...

class StringList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class OrderByStatement(_message.Message):
    __slots__ = ("key", "source", "direction")
    KEY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    key: str
    source: DataSource
    direction: SortDirection
    def __init__(self, key: _Optional[str] = ..., source: _Optional[_Union[DataSource, str]] = ..., direction: _Optional[_Union[SortDirection, str]] = ...) -> None: ...
