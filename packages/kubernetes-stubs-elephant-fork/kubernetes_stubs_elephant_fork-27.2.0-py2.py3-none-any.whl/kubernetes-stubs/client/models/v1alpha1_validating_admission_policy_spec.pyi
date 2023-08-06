import datetime
import typing

import kubernetes.client

class V1alpha1ValidatingAdmissionPolicySpec:
    audit_annotations: typing.Optional[list[kubernetes.client.V1alpha1AuditAnnotation]]
    failure_policy: typing.Optional[str]
    match_conditions: typing.Optional[list[kubernetes.client.V1alpha1MatchCondition]]
    match_constraints: typing.Optional[kubernetes.client.V1alpha1MatchResources]
    param_kind: typing.Optional[kubernetes.client.V1alpha1ParamKind]
    validations: typing.Optional[list[kubernetes.client.V1alpha1Validation]]
    
    def __init__(self, *, audit_annotations: typing.Optional[list[kubernetes.client.V1alpha1AuditAnnotation]] = ..., failure_policy: typing.Optional[str] = ..., match_conditions: typing.Optional[list[kubernetes.client.V1alpha1MatchCondition]] = ..., match_constraints: typing.Optional[kubernetes.client.V1alpha1MatchResources] = ..., param_kind: typing.Optional[kubernetes.client.V1alpha1ParamKind] = ..., validations: typing.Optional[list[kubernetes.client.V1alpha1Validation]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ValidatingAdmissionPolicySpecDict:
        ...
class V1alpha1ValidatingAdmissionPolicySpecDict(typing.TypedDict, total=False):
    auditAnnotations: typing.Optional[list[kubernetes.client.V1alpha1AuditAnnotationDict]]
    failurePolicy: typing.Optional[str]
    matchConditions: typing.Optional[list[kubernetes.client.V1alpha1MatchConditionDict]]
    matchConstraints: typing.Optional[kubernetes.client.V1alpha1MatchResourcesDict]
    paramKind: typing.Optional[kubernetes.client.V1alpha1ParamKindDict]
    validations: typing.Optional[list[kubernetes.client.V1alpha1ValidationDict]]
