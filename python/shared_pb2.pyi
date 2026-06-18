from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TriggerSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_SOURCE_UNSPECIFIED: _ClassVar[TriggerSource]
    TRIGGER_SOURCE_CRON: _ClassVar[TriggerSource]
    TRIGGER_SOURCE_WEBHOOK: _ClassVar[TriggerSource]
    TRIGGER_SOURCE_UI: _ClassVar[TriggerSource]
    TRIGGER_SOURCE_CLI: _ClassVar[TriggerSource]

class RegistrationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REGISTRATION_STATUS_UNSPECIFIED: _ClassVar[RegistrationStatus]
    REGISTRATION_STATUS_SUCCESSFUL: _ClassVar[RegistrationStatus]
    REGISTRATION_STATUS_FAILED: _ClassVar[RegistrationStatus]

class TriggerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_STATUS_UNSPECIFIED: _ClassVar[TriggerStatus]
    TRIGGER_STATUS_ACCEPTED: _ClassVar[TriggerStatus]
    TRIGGER_STATUS_REJECTED: _ClassVar[TriggerStatus]

class ExecutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXECUTION_STATUS_UNSPECIFIED: _ClassVar[ExecutionStatus]
    EXECUTION_STATUS_SUCCESSFUL: _ClassVar[ExecutionStatus]
    EXECUTION_STATUS_FAILED: _ClassVar[ExecutionStatus]

class BackoffStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BACKOFF_STRATEGY_UNSPECIFIED: _ClassVar[BackoffStrategy]
    BACKOFF_STRATEGY_LINEAR: _ClassVar[BackoffStrategy]
    BACKOFF_STRATEGY_EXPONENTIAL: _ClassVar[BackoffStrategy]
TRIGGER_SOURCE_UNSPECIFIED: TriggerSource
TRIGGER_SOURCE_CRON: TriggerSource
TRIGGER_SOURCE_WEBHOOK: TriggerSource
TRIGGER_SOURCE_UI: TriggerSource
TRIGGER_SOURCE_CLI: TriggerSource
REGISTRATION_STATUS_UNSPECIFIED: RegistrationStatus
REGISTRATION_STATUS_SUCCESSFUL: RegistrationStatus
REGISTRATION_STATUS_FAILED: RegistrationStatus
TRIGGER_STATUS_UNSPECIFIED: TriggerStatus
TRIGGER_STATUS_ACCEPTED: TriggerStatus
TRIGGER_STATUS_REJECTED: TriggerStatus
EXECUTION_STATUS_UNSPECIFIED: ExecutionStatus
EXECUTION_STATUS_SUCCESSFUL: ExecutionStatus
EXECUTION_STATUS_FAILED: ExecutionStatus
BACKOFF_STRATEGY_UNSPECIFIED: BackoffStrategy
BACKOFF_STRATEGY_LINEAR: BackoffStrategy
BACKOFF_STRATEGY_EXPONENTIAL: BackoffStrategy

class DataFunctionSettings(_message.Message):
    __slots__ = ("ttl", "timeout")
    TTL_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    ttl: int
    timeout: int
    def __init__(self, ttl: _Optional[int] = ..., timeout: _Optional[int] = ...) -> None: ...

class TaskExecutionSettings(_message.Message):
    __slots__ = ("executionTimeout", "retryCount", "backoffStrategy", "deadline")
    EXECUTIONTIMEOUT_FIELD_NUMBER: _ClassVar[int]
    RETRYCOUNT_FIELD_NUMBER: _ClassVar[int]
    BACKOFFSTRATEGY_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    executionTimeout: int
    retryCount: int
    backoffStrategy: BackoffStrategy
    deadline: int
    def __init__(self, executionTimeout: _Optional[int] = ..., retryCount: _Optional[int] = ..., backoffStrategy: _Optional[_Union[BackoffStrategy, str]] = ..., deadline: _Optional[int] = ...) -> None: ...

class RequiredPastResult(_message.Message):
    __slots__ = ("taskName", "executionParams", "taskResult")
    TASKNAME_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONPARAMS_FIELD_NUMBER: _ClassVar[int]
    TASKRESULT_FIELD_NUMBER: _ClassVar[int]
    taskName: str
    executionParams: str
    taskResult: str
    def __init__(self, taskName: _Optional[str] = ..., executionParams: _Optional[str] = ..., taskResult: _Optional[str] = ...) -> None: ...

class WorkflowExecutionSettings(_message.Message):
    __slots__ = ("priorityQueue", "concurrencyLimit")
    PRIORITYQUEUE_FIELD_NUMBER: _ClassVar[int]
    CONCURRENCYLIMIT_FIELD_NUMBER: _ClassVar[int]
    priorityQueue: _containers.RepeatedScalarFieldContainer[str]
    concurrencyLimit: int
    def __init__(self, priorityQueue: _Optional[_Iterable[str]] = ..., concurrencyLimit: _Optional[int] = ...) -> None: ...

class ComputeMetrics(_message.Message):
    __slots__ = ("cpuSeconds", "memoryGiBSeconds")
    CPUSECONDS_FIELD_NUMBER: _ClassVar[int]
    MEMORYGIBSECONDS_FIELD_NUMBER: _ClassVar[int]
    cpuSeconds: float
    memoryGiBSeconds: float
    def __init__(self, cpuSeconds: _Optional[float] = ..., memoryGiBSeconds: _Optional[float] = ...) -> None: ...
