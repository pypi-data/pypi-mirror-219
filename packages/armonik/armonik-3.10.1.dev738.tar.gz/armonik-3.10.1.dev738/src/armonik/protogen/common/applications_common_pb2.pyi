from . import objects_pb2 as _objects_pb2
from . import sort_direction_pb2 as _sort_direction_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationRawEnumField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    APPLICATION_RAW_ENUM_FIELD_UNSPECIFIED: _ClassVar[ApplicationRawEnumField]
    APPLICATION_RAW_ENUM_FIELD_NAME: _ClassVar[ApplicationRawEnumField]
    APPLICATION_RAW_ENUM_FIELD_VERSION: _ClassVar[ApplicationRawEnumField]
    APPLICATION_RAW_ENUM_FIELD_NAMESPACE: _ClassVar[ApplicationRawEnumField]
    APPLICATION_RAW_ENUM_FIELD_SERVICE: _ClassVar[ApplicationRawEnumField]
APPLICATION_RAW_ENUM_FIELD_UNSPECIFIED: ApplicationRawEnumField
APPLICATION_RAW_ENUM_FIELD_NAME: ApplicationRawEnumField
APPLICATION_RAW_ENUM_FIELD_VERSION: ApplicationRawEnumField
APPLICATION_RAW_ENUM_FIELD_NAMESPACE: ApplicationRawEnumField
APPLICATION_RAW_ENUM_FIELD_SERVICE: ApplicationRawEnumField

class ApplicationRaw(_message.Message):
    __slots__ = ["name", "version", "namespace", "service"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    namespace: str
    service: str
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., namespace: _Optional[str] = ..., service: _Optional[str] = ...) -> None: ...

class ApplicationRawField(_message.Message):
    __slots__ = ["field"]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    field: ApplicationRawEnumField
    def __init__(self, field: _Optional[_Union[ApplicationRawEnumField, str]] = ...) -> None: ...

class ApplicationField(_message.Message):
    __slots__ = ["application_field"]
    APPLICATION_FIELD_FIELD_NUMBER: _ClassVar[int]
    application_field: ApplicationRawField
    def __init__(self, application_field: _Optional[_Union[ApplicationRawField, _Mapping]] = ...) -> None: ...

class ListApplicationsRequest(_message.Message):
    __slots__ = ["page", "page_size", "filter", "sort"]
    class Filter(_message.Message):
        __slots__ = ["name", "version", "namespace", "service"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        NAMESPACE_FIELD_NUMBER: _ClassVar[int]
        SERVICE_FIELD_NUMBER: _ClassVar[int]
        name: str
        version: str
        namespace: str
        service: str
        def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., namespace: _Optional[str] = ..., service: _Optional[str] = ...) -> None: ...
    class Sort(_message.Message):
        __slots__ = ["fields", "direction"]
        FIELDS_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        fields: _containers.RepeatedCompositeFieldContainer[ApplicationField]
        direction: _sort_direction_pb2.SortDirection
        def __init__(self, fields: _Optional[_Iterable[_Union[ApplicationField, _Mapping]]] = ..., direction: _Optional[_Union[_sort_direction_pb2.SortDirection, str]] = ...) -> None: ...
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    filter: ListApplicationsRequest.Filter
    sort: ListApplicationsRequest.Sort
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., filter: _Optional[_Union[ListApplicationsRequest.Filter, _Mapping]] = ..., sort: _Optional[_Union[ListApplicationsRequest.Sort, _Mapping]] = ...) -> None: ...

class ListApplicationsResponse(_message.Message):
    __slots__ = ["applications", "page", "page_size", "total"]
    APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    applications: _containers.RepeatedCompositeFieldContainer[ApplicationRaw]
    page: int
    page_size: int
    total: int
    def __init__(self, applications: _Optional[_Iterable[_Union[ApplicationRaw, _Mapping]]] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class CountTasksByStatusRequest(_message.Message):
    __slots__ = ["name", "version"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class CountTasksByStatusResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _containers.RepeatedCompositeFieldContainer[_objects_pb2.StatusCount]
    def __init__(self, status: _Optional[_Iterable[_Union[_objects_pb2.StatusCount, _Mapping]]] = ...) -> None: ...
