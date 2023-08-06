import datetime
import typing

import kubernetes.client

class V1alpha2ResourceClaim:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha2ResourceClaimSpec
    status: typing.Optional[kubernetes.client.V1alpha2ResourceClaimStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha2ResourceClaimSpec, status: typing.Optional[kubernetes.client.V1alpha2ResourceClaimStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2ResourceClaimDict:
        ...
class V1alpha2ResourceClaimDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha2ResourceClaimSpecDict
    status: typing.Optional[kubernetes.client.V1alpha2ResourceClaimStatusDict]
