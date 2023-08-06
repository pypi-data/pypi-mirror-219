import datetime
import typing

import kubernetes.client

class V1alpha2ResourceHandle:
    data: typing.Optional[str]
    driver_name: typing.Optional[str]
    
    def __init__(self, *, data: typing.Optional[str] = ..., driver_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2ResourceHandleDict:
        ...
class V1alpha2ResourceHandleDict(typing.TypedDict, total=False):
    data: typing.Optional[str]
    driverName: typing.Optional[str]
