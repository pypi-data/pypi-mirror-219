import datetime
import typing

import kubernetes.client

class V1alpha1ParentReference:
    group: typing.Optional[str]
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    resource: typing.Optional[str]
    uid: typing.Optional[str]
    
    def __init__(self, *, group: typing.Optional[str] = ..., name: typing.Optional[str] = ..., namespace: typing.Optional[str] = ..., resource: typing.Optional[str] = ..., uid: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ParentReferenceDict:
        ...
class V1alpha1ParentReferenceDict(typing.TypedDict, total=False):
    group: typing.Optional[str]
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    resource: typing.Optional[str]
    uid: typing.Optional[str]
