import datetime
import typing

import kubernetes.client

class V1alpha2ResourceClaimSchedulingStatus:
    name: typing.Optional[str]
    unsuitable_nodes: typing.Optional[list[str]]
    
    def __init__(self, *, name: typing.Optional[str] = ..., unsuitable_nodes: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2ResourceClaimSchedulingStatusDict:
        ...
class V1alpha2ResourceClaimSchedulingStatusDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
    unsuitableNodes: typing.Optional[list[str]]
