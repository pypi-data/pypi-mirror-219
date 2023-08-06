from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from . import objects_pb2 as _objects_pb2
from . import session_status_pb2 as _session_status_pb2
from . import sort_direction_pb2 as _sort_direction_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SessionRawEnumField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SESSION_RAW_ENUM_FIELD_UNSPECIFIED: _ClassVar[SessionRawEnumField]
    SESSION_RAW_ENUM_FIELD_SESSION_ID: _ClassVar[SessionRawEnumField]
    SESSION_RAW_ENUM_FIELD_STATUS: _ClassVar[SessionRawEnumField]
    SESSION_RAW_ENUM_FIELD_PARTITION_IDS: _ClassVar[SessionRawEnumField]
    SESSION_RAW_ENUM_FIELD_OPTIONS: _ClassVar[SessionRawEnumField]
    SESSION_RAW_ENUM_FIELD_CREATED_AT: _ClassVar[SessionRawEnumField]
    SESSION_RAW_ENUM_FIELD_CANCELLED_AT: _ClassVar[SessionRawEnumField]
    SESSION_RAW_ENUM_FIELD_DURATION: _ClassVar[SessionRawEnumField]

class TaskOptionEnumField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TASK_OPTION_ENUM_FIELD_UNSPECIFIED: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_MAX_DURATION: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_MAX_RETRIES: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_PRIORITY: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_PARTITION_ID: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_APPLICATION_NAME: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_APPLICATION_VERSION: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_APPLICATION_NAMESPACE: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_APPLICATION_SERVICE: _ClassVar[TaskOptionEnumField]
    TASK_OPTION_ENUM_FIELD_ENGINE_TYPE: _ClassVar[TaskOptionEnumField]
SESSION_RAW_ENUM_FIELD_UNSPECIFIED: SessionRawEnumField
SESSION_RAW_ENUM_FIELD_SESSION_ID: SessionRawEnumField
SESSION_RAW_ENUM_FIELD_STATUS: SessionRawEnumField
SESSION_RAW_ENUM_FIELD_PARTITION_IDS: SessionRawEnumField
SESSION_RAW_ENUM_FIELD_OPTIONS: SessionRawEnumField
SESSION_RAW_ENUM_FIELD_CREATED_AT: SessionRawEnumField
SESSION_RAW_ENUM_FIELD_CANCELLED_AT: SessionRawEnumField
SESSION_RAW_ENUM_FIELD_DURATION: SessionRawEnumField
TASK_OPTION_ENUM_FIELD_UNSPECIFIED: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_MAX_DURATION: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_MAX_RETRIES: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_PRIORITY: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_PARTITION_ID: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_APPLICATION_NAME: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_APPLICATION_VERSION: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_APPLICATION_NAMESPACE: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_APPLICATION_SERVICE: TaskOptionEnumField
TASK_OPTION_ENUM_FIELD_ENGINE_TYPE: TaskOptionEnumField

class SessionRaw(_message.Message):
    __slots__ = ["session_id", "status", "partition_ids", "options", "created_at", "cancelled_at", "duration"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PARTITION_IDS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CANCELLED_AT_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    status: _session_status_pb2.SessionStatus
    partition_ids: _containers.RepeatedScalarFieldContainer[str]
    options: _objects_pb2.TaskOptions
    created_at: _timestamp_pb2.Timestamp
    cancelled_at: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    def __init__(self, session_id: _Optional[str] = ..., status: _Optional[_Union[_session_status_pb2.SessionStatus, str]] = ..., partition_ids: _Optional[_Iterable[str]] = ..., options: _Optional[_Union[_objects_pb2.TaskOptions, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., cancelled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class SessionRawField(_message.Message):
    __slots__ = ["field"]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    field: SessionRawEnumField
    def __init__(self, field: _Optional[_Union[SessionRawEnumField, str]] = ...) -> None: ...

class TaskOptionField(_message.Message):
    __slots__ = ["field"]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    field: TaskOptionEnumField
    def __init__(self, field: _Optional[_Union[TaskOptionEnumField, str]] = ...) -> None: ...

class TaskOptionGenericField(_message.Message):
    __slots__ = ["field"]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    field: str
    def __init__(self, field: _Optional[str] = ...) -> None: ...

class SessionField(_message.Message):
    __slots__ = ["session_raw_field", "task_option_field", "task_option_generic_field"]
    SESSION_RAW_FIELD_FIELD_NUMBER: _ClassVar[int]
    TASK_OPTION_FIELD_FIELD_NUMBER: _ClassVar[int]
    TASK_OPTION_GENERIC_FIELD_FIELD_NUMBER: _ClassVar[int]
    session_raw_field: SessionRawField
    task_option_field: TaskOptionField
    task_option_generic_field: TaskOptionGenericField
    def __init__(self, session_raw_field: _Optional[_Union[SessionRawField, _Mapping]] = ..., task_option_field: _Optional[_Union[TaskOptionField, _Mapping]] = ..., task_option_generic_field: _Optional[_Union[TaskOptionGenericField, _Mapping]] = ...) -> None: ...

class ListSessionsRequest(_message.Message):
    __slots__ = ["page", "page_size", "filter", "sort", "with_task_options"]
    class Filter(_message.Message):
        __slots__ = ["application_name", "application_version", "session_id", "created_after", "created_before", "cancelled_after", "cancelled_before", "status"]
        APPLICATION_NAME_FIELD_NUMBER: _ClassVar[int]
        APPLICATION_VERSION_FIELD_NUMBER: _ClassVar[int]
        SESSION_ID_FIELD_NUMBER: _ClassVar[int]
        CREATED_AFTER_FIELD_NUMBER: _ClassVar[int]
        CREATED_BEFORE_FIELD_NUMBER: _ClassVar[int]
        CANCELLED_AFTER_FIELD_NUMBER: _ClassVar[int]
        CANCELLED_BEFORE_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        application_name: str
        application_version: str
        session_id: str
        created_after: _timestamp_pb2.Timestamp
        created_before: _timestamp_pb2.Timestamp
        cancelled_after: _timestamp_pb2.Timestamp
        cancelled_before: _timestamp_pb2.Timestamp
        status: _session_status_pb2.SessionStatus
        def __init__(self, application_name: _Optional[str] = ..., application_version: _Optional[str] = ..., session_id: _Optional[str] = ..., created_after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_before: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., cancelled_after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., cancelled_before: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_session_status_pb2.SessionStatus, str]] = ...) -> None: ...
    class Sort(_message.Message):
        __slots__ = ["field", "direction"]
        FIELD_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        field: SessionField
        direction: _sort_direction_pb2.SortDirection
        def __init__(self, field: _Optional[_Union[SessionField, _Mapping]] = ..., direction: _Optional[_Union[_sort_direction_pb2.SortDirection, str]] = ...) -> None: ...
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    WITH_TASK_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    filter: ListSessionsRequest.Filter
    sort: ListSessionsRequest.Sort
    with_task_options: bool
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., filter: _Optional[_Union[ListSessionsRequest.Filter, _Mapping]] = ..., sort: _Optional[_Union[ListSessionsRequest.Sort, _Mapping]] = ..., with_task_options: bool = ...) -> None: ...

class ListSessionsResponse(_message.Message):
    __slots__ = ["sessions", "page", "page_size", "total"]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    sessions: _containers.RepeatedCompositeFieldContainer[SessionRaw]
    page: int
    page_size: int
    total: int
    def __init__(self, sessions: _Optional[_Iterable[_Union[SessionRaw, _Mapping]]] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class GetSessionRequest(_message.Message):
    __slots__ = ["session_id"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class GetSessionResponse(_message.Message):
    __slots__ = ["session"]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    session: SessionRaw
    def __init__(self, session: _Optional[_Union[SessionRaw, _Mapping]] = ...) -> None: ...

class CancelSessionRequest(_message.Message):
    __slots__ = ["session_id"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class CancelSessionResponse(_message.Message):
    __slots__ = ["session"]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    session: SessionRaw
    def __init__(self, session: _Optional[_Union[SessionRaw, _Mapping]] = ...) -> None: ...

class CountTasksByStatusRequest(_message.Message):
    __slots__ = ["session_id"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class CountTasksByStatusResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _containers.RepeatedCompositeFieldContainer[_objects_pb2.StatusCount]
    def __init__(self, status: _Optional[_Iterable[_Union[_objects_pb2.StatusCount, _Mapping]]] = ...) -> None: ...
