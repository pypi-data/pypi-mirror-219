import datetime
import typing

import kubernetes.client

class V1alpha2PodSchedulingContextStatus:
    resource_claims: typing.Optional[list[kubernetes.client.V1alpha2ResourceClaimSchedulingStatus]]
    
    def __init__(self, *, resource_claims: typing.Optional[list[kubernetes.client.V1alpha2ResourceClaimSchedulingStatus]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2PodSchedulingContextStatusDict:
        ...
class V1alpha2PodSchedulingContextStatusDict(typing.TypedDict, total=False):
    resourceClaims: typing.Optional[list[kubernetes.client.V1alpha2ResourceClaimSchedulingStatusDict]]
