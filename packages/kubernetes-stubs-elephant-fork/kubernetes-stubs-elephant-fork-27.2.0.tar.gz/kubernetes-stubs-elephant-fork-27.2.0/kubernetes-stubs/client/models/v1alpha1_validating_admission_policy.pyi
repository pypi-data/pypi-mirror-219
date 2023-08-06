import datetime
import typing

import kubernetes.client

class V1alpha1ValidatingAdmissionPolicy:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1alpha1ValidatingAdmissionPolicySpec]
    status: typing.Optional[kubernetes.client.V1alpha1ValidatingAdmissionPolicyStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1alpha1ValidatingAdmissionPolicySpec] = ..., status: typing.Optional[kubernetes.client.V1alpha1ValidatingAdmissionPolicyStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ValidatingAdmissionPolicyDict:
        ...
class V1alpha1ValidatingAdmissionPolicyDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1alpha1ValidatingAdmissionPolicySpecDict]
    status: typing.Optional[kubernetes.client.V1alpha1ValidatingAdmissionPolicyStatusDict]
