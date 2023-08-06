"""
Type annotations for secretsmanager service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_secretsmanager/type_defs/)

Usage::

    ```python
    from mypy_boto3_secretsmanager.type_defs import CancelRotateSecretRequestRequestTypeDef

    data: CancelRotateSecretRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import FilterNameStringTypeType, SortOrderTypeType, StatusTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CancelRotateSecretRequestRequestTypeDef",
    "CancelRotateSecretResponseTypeDef",
    "ReplicaRegionTypeTypeDef",
    "TagTypeDef",
    "ReplicationStatusTypeTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteResourcePolicyResponseTypeDef",
    "DeleteSecretRequestRequestTypeDef",
    "DeleteSecretResponseTypeDef",
    "DescribeSecretRequestRequestTypeDef",
    "RotationRulesTypeTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FilterTypeDef",
    "GetRandomPasswordRequestRequestTypeDef",
    "GetRandomPasswordResponseTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetSecretValueRequestRequestTypeDef",
    "GetSecretValueResponseTypeDef",
    "ListSecretVersionIdsRequestRequestTypeDef",
    "SecretVersionsListEntryTypeDef",
    "PaginatorConfigTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "PutSecretValueRequestRequestTypeDef",
    "PutSecretValueResponseTypeDef",
    "RemoveRegionsFromReplicationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreSecretRequestRequestTypeDef",
    "RestoreSecretResponseTypeDef",
    "RotateSecretResponseTypeDef",
    "StopReplicationToReplicaRequestRequestTypeDef",
    "StopReplicationToReplicaResponseTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateSecretRequestRequestTypeDef",
    "UpdateSecretResponseTypeDef",
    "UpdateSecretVersionStageRequestRequestTypeDef",
    "UpdateSecretVersionStageResponseTypeDef",
    "ValidateResourcePolicyRequestRequestTypeDef",
    "ValidationErrorsEntryTypeDef",
    "ReplicateSecretToRegionsRequestRequestTypeDef",
    "CreateSecretRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateSecretResponseTypeDef",
    "RemoveRegionsFromReplicationResponseTypeDef",
    "ReplicateSecretToRegionsResponseTypeDef",
    "DescribeSecretResponseTypeDef",
    "RotateSecretRequestRequestTypeDef",
    "SecretListEntryTypeDef",
    "ListSecretsRequestListSecretsPaginateTypeDef",
    "ListSecretsRequestRequestTypeDef",
    "ListSecretVersionIdsResponseTypeDef",
    "ValidateResourcePolicyResponseTypeDef",
    "ListSecretsResponseTypeDef",
)

CancelRotateSecretRequestRequestTypeDef = TypedDict(
    "CancelRotateSecretRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)

CancelRotateSecretResponseTypeDef = TypedDict(
    "CancelRotateSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReplicaRegionTypeTypeDef = TypedDict(
    "ReplicaRegionTypeTypeDef",
    {
        "Region": str,
        "KmsKeyId": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ReplicationStatusTypeTypeDef = TypedDict(
    "ReplicationStatusTypeTypeDef",
    {
        "Region": str,
        "KmsKeyId": str,
        "Status": StatusTypeType,
        "StatusMessage": str,
        "LastAccessedDate": datetime,
    },
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)

DeleteResourcePolicyResponseTypeDef = TypedDict(
    "DeleteResourcePolicyResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteSecretRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSecretRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)
_OptionalDeleteSecretRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSecretRequestRequestTypeDef",
    {
        "RecoveryWindowInDays": int,
        "ForceDeleteWithoutRecovery": bool,
    },
    total=False,
)


class DeleteSecretRequestRequestTypeDef(
    _RequiredDeleteSecretRequestRequestTypeDef, _OptionalDeleteSecretRequestRequestTypeDef
):
    pass


DeleteSecretResponseTypeDef = TypedDict(
    "DeleteSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "DeletionDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSecretRequestRequestTypeDef = TypedDict(
    "DescribeSecretRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)

RotationRulesTypeTypeDef = TypedDict(
    "RotationRulesTypeTypeDef",
    {
        "AutomaticallyAfterDays": int,
        "Duration": str,
        "ScheduleExpression": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Key": FilterNameStringTypeType,
        "Values": Sequence[str],
    },
    total=False,
)

GetRandomPasswordRequestRequestTypeDef = TypedDict(
    "GetRandomPasswordRequestRequestTypeDef",
    {
        "PasswordLength": int,
        "ExcludeCharacters": str,
        "ExcludeNumbers": bool,
        "ExcludePunctuation": bool,
        "ExcludeUppercase": bool,
        "ExcludeLowercase": bool,
        "IncludeSpace": bool,
        "RequireEachIncludedType": bool,
    },
    total=False,
)

GetRandomPasswordResponseTypeDef = TypedDict(
    "GetRandomPasswordResponseTypeDef",
    {
        "RandomPassword": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResourcePolicyRequestRequestTypeDef = TypedDict(
    "GetResourcePolicyRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "ResourcePolicy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetSecretValueRequestRequestTypeDef = TypedDict(
    "_RequiredGetSecretValueRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)
_OptionalGetSecretValueRequestRequestTypeDef = TypedDict(
    "_OptionalGetSecretValueRequestRequestTypeDef",
    {
        "VersionId": str,
        "VersionStage": str,
    },
    total=False,
)


class GetSecretValueRequestRequestTypeDef(
    _RequiredGetSecretValueRequestRequestTypeDef, _OptionalGetSecretValueRequestRequestTypeDef
):
    pass


GetSecretValueResponseTypeDef = TypedDict(
    "GetSecretValueResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "SecretBinary": bytes,
        "SecretString": str,
        "VersionStages": List[str],
        "CreatedDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListSecretVersionIdsRequestRequestTypeDef = TypedDict(
    "_RequiredListSecretVersionIdsRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)
_OptionalListSecretVersionIdsRequestRequestTypeDef = TypedDict(
    "_OptionalListSecretVersionIdsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "IncludeDeprecated": bool,
    },
    total=False,
)


class ListSecretVersionIdsRequestRequestTypeDef(
    _RequiredListSecretVersionIdsRequestRequestTypeDef,
    _OptionalListSecretVersionIdsRequestRequestTypeDef,
):
    pass


SecretVersionsListEntryTypeDef = TypedDict(
    "SecretVersionsListEntryTypeDef",
    {
        "VersionId": str,
        "VersionStages": List[str],
        "LastAccessedDate": datetime,
        "CreatedDate": datetime,
        "KmsKeyIds": List[str],
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutResourcePolicyRequestRequestTypeDef",
    {
        "SecretId": str,
        "ResourcePolicy": str,
    },
)
_OptionalPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutResourcePolicyRequestRequestTypeDef",
    {
        "BlockPublicPolicy": bool,
    },
    total=False,
)


class PutResourcePolicyRequestRequestTypeDef(
    _RequiredPutResourcePolicyRequestRequestTypeDef, _OptionalPutResourcePolicyRequestRequestTypeDef
):
    pass


PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutSecretValueRequestRequestTypeDef = TypedDict(
    "_RequiredPutSecretValueRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)
_OptionalPutSecretValueRequestRequestTypeDef = TypedDict(
    "_OptionalPutSecretValueRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "SecretBinary": Union[str, bytes, IO[Any], StreamingBody],
        "SecretString": str,
        "VersionStages": Sequence[str],
    },
    total=False,
)


class PutSecretValueRequestRequestTypeDef(
    _RequiredPutSecretValueRequestRequestTypeDef, _OptionalPutSecretValueRequestRequestTypeDef
):
    pass


PutSecretValueResponseTypeDef = TypedDict(
    "PutSecretValueResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "VersionStages": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveRegionsFromReplicationRequestRequestTypeDef = TypedDict(
    "RemoveRegionsFromReplicationRequestRequestTypeDef",
    {
        "SecretId": str,
        "RemoveReplicaRegions": Sequence[str],
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

RestoreSecretRequestRequestTypeDef = TypedDict(
    "RestoreSecretRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)

RestoreSecretResponseTypeDef = TypedDict(
    "RestoreSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RotateSecretResponseTypeDef = TypedDict(
    "RotateSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopReplicationToReplicaRequestRequestTypeDef = TypedDict(
    "StopReplicationToReplicaRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)

StopReplicationToReplicaResponseTypeDef = TypedDict(
    "StopReplicationToReplicaResponseTypeDef",
    {
        "ARN": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "SecretId": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateSecretRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSecretRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)
_OptionalUpdateSecretRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSecretRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Description": str,
        "KmsKeyId": str,
        "SecretBinary": Union[str, bytes, IO[Any], StreamingBody],
        "SecretString": str,
    },
    total=False,
)


class UpdateSecretRequestRequestTypeDef(
    _RequiredUpdateSecretRequestRequestTypeDef, _OptionalUpdateSecretRequestRequestTypeDef
):
    pass


UpdateSecretResponseTypeDef = TypedDict(
    "UpdateSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateSecretVersionStageRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSecretVersionStageRequestRequestTypeDef",
    {
        "SecretId": str,
        "VersionStage": str,
    },
)
_OptionalUpdateSecretVersionStageRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSecretVersionStageRequestRequestTypeDef",
    {
        "RemoveFromVersionId": str,
        "MoveToVersionId": str,
    },
    total=False,
)


class UpdateSecretVersionStageRequestRequestTypeDef(
    _RequiredUpdateSecretVersionStageRequestRequestTypeDef,
    _OptionalUpdateSecretVersionStageRequestRequestTypeDef,
):
    pass


UpdateSecretVersionStageResponseTypeDef = TypedDict(
    "UpdateSecretVersionStageResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredValidateResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredValidateResourcePolicyRequestRequestTypeDef",
    {
        "ResourcePolicy": str,
    },
)
_OptionalValidateResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalValidateResourcePolicyRequestRequestTypeDef",
    {
        "SecretId": str,
    },
    total=False,
)


class ValidateResourcePolicyRequestRequestTypeDef(
    _RequiredValidateResourcePolicyRequestRequestTypeDef,
    _OptionalValidateResourcePolicyRequestRequestTypeDef,
):
    pass


ValidationErrorsEntryTypeDef = TypedDict(
    "ValidationErrorsEntryTypeDef",
    {
        "CheckName": str,
        "ErrorMessage": str,
    },
)

_RequiredReplicateSecretToRegionsRequestRequestTypeDef = TypedDict(
    "_RequiredReplicateSecretToRegionsRequestRequestTypeDef",
    {
        "SecretId": str,
        "AddReplicaRegions": Sequence[ReplicaRegionTypeTypeDef],
    },
)
_OptionalReplicateSecretToRegionsRequestRequestTypeDef = TypedDict(
    "_OptionalReplicateSecretToRegionsRequestRequestTypeDef",
    {
        "ForceOverwriteReplicaSecret": bool,
    },
    total=False,
)


class ReplicateSecretToRegionsRequestRequestTypeDef(
    _RequiredReplicateSecretToRegionsRequestRequestTypeDef,
    _OptionalReplicateSecretToRegionsRequestRequestTypeDef,
):
    pass


_RequiredCreateSecretRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSecretRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateSecretRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSecretRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Description": str,
        "KmsKeyId": str,
        "SecretBinary": Union[str, bytes, IO[Any], StreamingBody],
        "SecretString": str,
        "Tags": Sequence[TagTypeDef],
        "AddReplicaRegions": Sequence[ReplicaRegionTypeTypeDef],
        "ForceOverwriteReplicaSecret": bool,
    },
    total=False,
)


class CreateSecretRequestRequestTypeDef(
    _RequiredCreateSecretRequestRequestTypeDef, _OptionalCreateSecretRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "SecretId": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateSecretResponseTypeDef = TypedDict(
    "CreateSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "ReplicationStatus": List[ReplicationStatusTypeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveRegionsFromReplicationResponseTypeDef = TypedDict(
    "RemoveRegionsFromReplicationResponseTypeDef",
    {
        "ARN": str,
        "ReplicationStatus": List[ReplicationStatusTypeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReplicateSecretToRegionsResponseTypeDef = TypedDict(
    "ReplicateSecretToRegionsResponseTypeDef",
    {
        "ARN": str,
        "ReplicationStatus": List[ReplicationStatusTypeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSecretResponseTypeDef = TypedDict(
    "DescribeSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "Description": str,
        "KmsKeyId": str,
        "RotationEnabled": bool,
        "RotationLambdaARN": str,
        "RotationRules": RotationRulesTypeTypeDef,
        "LastRotatedDate": datetime,
        "LastChangedDate": datetime,
        "LastAccessedDate": datetime,
        "DeletedDate": datetime,
        "NextRotationDate": datetime,
        "Tags": List[TagTypeDef],
        "VersionIdsToStages": Dict[str, List[str]],
        "OwningService": str,
        "CreatedDate": datetime,
        "PrimaryRegion": str,
        "ReplicationStatus": List[ReplicationStatusTypeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredRotateSecretRequestRequestTypeDef = TypedDict(
    "_RequiredRotateSecretRequestRequestTypeDef",
    {
        "SecretId": str,
    },
)
_OptionalRotateSecretRequestRequestTypeDef = TypedDict(
    "_OptionalRotateSecretRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "RotationLambdaARN": str,
        "RotationRules": RotationRulesTypeTypeDef,
        "RotateImmediately": bool,
    },
    total=False,
)


class RotateSecretRequestRequestTypeDef(
    _RequiredRotateSecretRequestRequestTypeDef, _OptionalRotateSecretRequestRequestTypeDef
):
    pass


SecretListEntryTypeDef = TypedDict(
    "SecretListEntryTypeDef",
    {
        "ARN": str,
        "Name": str,
        "Description": str,
        "KmsKeyId": str,
        "RotationEnabled": bool,
        "RotationLambdaARN": str,
        "RotationRules": RotationRulesTypeTypeDef,
        "LastRotatedDate": datetime,
        "LastChangedDate": datetime,
        "LastAccessedDate": datetime,
        "DeletedDate": datetime,
        "NextRotationDate": datetime,
        "Tags": List[TagTypeDef],
        "SecretVersionsToStages": Dict[str, List[str]],
        "OwningService": str,
        "CreatedDate": datetime,
        "PrimaryRegion": str,
    },
)

ListSecretsRequestListSecretsPaginateTypeDef = TypedDict(
    "ListSecretsRequestListSecretsPaginateTypeDef",
    {
        "IncludePlannedDeletion": bool,
        "Filters": Sequence[FilterTypeDef],
        "SortOrder": SortOrderTypeType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSecretsRequestRequestTypeDef = TypedDict(
    "ListSecretsRequestRequestTypeDef",
    {
        "IncludePlannedDeletion": bool,
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
        "SortOrder": SortOrderTypeType,
    },
    total=False,
)

ListSecretVersionIdsResponseTypeDef = TypedDict(
    "ListSecretVersionIdsResponseTypeDef",
    {
        "Versions": List[SecretVersionsListEntryTypeDef],
        "NextToken": str,
        "ARN": str,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ValidateResourcePolicyResponseTypeDef = TypedDict(
    "ValidateResourcePolicyResponseTypeDef",
    {
        "PolicyValidationPassed": bool,
        "ValidationErrors": List[ValidationErrorsEntryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSecretsResponseTypeDef = TypedDict(
    "ListSecretsResponseTypeDef",
    {
        "SecretList": List[SecretListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
