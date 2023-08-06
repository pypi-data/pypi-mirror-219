import datetime
import typing

import kubernetes.client

class V1alpha1ValidatingAdmissionPolicyStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    observed_generation: typing.Optional[int]
    type_checking: typing.Optional[kubernetes.client.V1alpha1TypeChecking]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., observed_generation: typing.Optional[int] = ..., type_checking: typing.Optional[kubernetes.client.V1alpha1TypeChecking] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ValidatingAdmissionPolicyStatusDict:
        ...
class V1alpha1ValidatingAdmissionPolicyStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    observedGeneration: typing.Optional[int]
    typeChecking: typing.Optional[kubernetes.client.V1alpha1TypeCheckingDict]
