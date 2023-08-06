import datetime
import typing

import kubernetes.client

class V1alpha2ResourceClaimConsumerReference:
    api_group: typing.Optional[str]
    name: str
    resource: str
    uid: str
    
    def __init__(self, *, api_group: typing.Optional[str] = ..., name: str, resource: str, uid: str) -> None:
        ...
    def to_dict(self) -> V1alpha2ResourceClaimConsumerReferenceDict:
        ...
class V1alpha2ResourceClaimConsumerReferenceDict(typing.TypedDict, total=False):
    apiGroup: typing.Optional[str]
    name: str
    resource: str
    uid: str
