import datetime
import typing

import kubernetes.client

class V1alpha2ResourceClaimStatus:
    allocation: typing.Optional[kubernetes.client.V1alpha2AllocationResult]
    deallocation_requested: typing.Optional[bool]
    driver_name: typing.Optional[str]
    reserved_for: typing.Optional[list[kubernetes.client.V1alpha2ResourceClaimConsumerReference]]
    
    def __init__(self, *, allocation: typing.Optional[kubernetes.client.V1alpha2AllocationResult] = ..., deallocation_requested: typing.Optional[bool] = ..., driver_name: typing.Optional[str] = ..., reserved_for: typing.Optional[list[kubernetes.client.V1alpha2ResourceClaimConsumerReference]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2ResourceClaimStatusDict:
        ...
class V1alpha2ResourceClaimStatusDict(typing.TypedDict, total=False):
    allocation: typing.Optional[kubernetes.client.V1alpha2AllocationResultDict]
    deallocationRequested: typing.Optional[bool]
    driverName: typing.Optional[str]
    reservedFor: typing.Optional[list[kubernetes.client.V1alpha2ResourceClaimConsumerReferenceDict]]
