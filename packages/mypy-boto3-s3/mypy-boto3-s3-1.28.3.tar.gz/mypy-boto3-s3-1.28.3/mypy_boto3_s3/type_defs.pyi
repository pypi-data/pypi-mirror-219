"""
Type annotations for s3 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3/type_defs/)

Usage::

    ```python
    from mypy_boto3_s3.type_defs import AbortIncompleteMultipartUploadTypeDef

    data: AbortIncompleteMultipartUploadTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Callable, Dict, List, Mapping, Sequence, Union

from boto3.s3.transfer import TransferConfig
from botocore.client import BaseClient
from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ArchiveStatusType,
    BucketAccelerateStatusType,
    BucketCannedACLType,
    BucketLocationConstraintType,
    BucketLogsPermissionType,
    BucketVersioningStatusType,
    ChecksumAlgorithmType,
    CompressionTypeType,
    DeleteMarkerReplicationStatusType,
    EventType,
    ExistingObjectReplicationStatusType,
    ExpirationStatusType,
    FileHeaderInfoType,
    FilterRuleNameType,
    IntelligentTieringAccessTierType,
    IntelligentTieringStatusType,
    InventoryFormatType,
    InventoryFrequencyType,
    InventoryIncludedObjectVersionsType,
    InventoryOptionalFieldType,
    JSONTypeType,
    MetadataDirectiveType,
    MetricsStatusType,
    MFADeleteStatusType,
    MFADeleteType,
    ObjectAttributesType,
    ObjectCannedACLType,
    ObjectLockLegalHoldStatusType,
    ObjectLockModeType,
    ObjectLockRetentionModeType,
    ObjectOwnershipType,
    ObjectStorageClassType,
    PayerType,
    PermissionType,
    ProtocolType,
    QuoteFieldsType,
    ReplicaModificationsStatusType,
    ReplicationRuleStatusType,
    ReplicationStatusType,
    ReplicationTimeStatusType,
    ServerSideEncryptionType,
    SseKmsEncryptedObjectsStatusType,
    StorageClassType,
    TaggingDirectiveType,
    TierType,
    TransitionStorageClassType,
    TypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AbortIncompleteMultipartUploadTypeDef",
    "AbortMultipartUploadOutputTypeDef",
    "AbortMultipartUploadRequestMultipartUploadAbortTypeDef",
    "AbortMultipartUploadRequestRequestTypeDef",
    "AccelerateConfigurationTypeDef",
    "OwnerTypeDef",
    "AccessControlTranslationTypeDef",
    "TagTypeDef",
    "AnalyticsS3BucketDestinationTypeDef",
    "CopySourceTypeDef",
    "BucketDownloadFileRequestTypeDef",
    "BucketDownloadFileobjRequestTypeDef",
    "BucketTypeDef",
    "BucketUploadFileRequestTypeDef",
    "BucketUploadFileobjRequestTypeDef",
    "CORSRuleTypeDef",
    "CSVInputTypeDef",
    "CSVOutputTypeDef",
    "ChecksumTypeDef",
    "ClientDownloadFileRequestTypeDef",
    "ClientDownloadFileobjRequestTypeDef",
    "ClientGeneratePresignedPostRequestTypeDef",
    "ClientUploadFileRequestTypeDef",
    "ClientUploadFileobjRequestTypeDef",
    "CloudFunctionConfigurationTypeDef",
    "CommonPrefixTypeDef",
    "CompleteMultipartUploadOutputTypeDef",
    "CompletedPartTypeDef",
    "ConditionTypeDef",
    "CopyObjectResultTypeDef",
    "CopyObjectRequestObjectCopyFromTypeDef",
    "CopyObjectRequestObjectSummaryCopyFromTypeDef",
    "CopyPartResultTypeDef",
    "CreateBucketConfigurationTypeDef",
    "CreateBucketOutputTypeDef",
    "CreateMultipartUploadOutputTypeDef",
    "CreateMultipartUploadRequestObjectInitiateMultipartUploadTypeDef",
    "CreateMultipartUploadRequestObjectSummaryInitiateMultipartUploadTypeDef",
    "CreateMultipartUploadRequestRequestTypeDef",
    "DefaultRetentionTypeDef",
    "DeleteBucketAnalyticsConfigurationRequestRequestTypeDef",
    "DeleteBucketCorsRequestBucketCorsDeleteTypeDef",
    "DeleteBucketCorsRequestRequestTypeDef",
    "DeleteBucketEncryptionRequestRequestTypeDef",
    "DeleteBucketIntelligentTieringConfigurationRequestRequestTypeDef",
    "DeleteBucketInventoryConfigurationRequestRequestTypeDef",
    "DeleteBucketLifecycleRequestBucketLifecycleConfigurationDeleteTypeDef",
    "DeleteBucketLifecycleRequestBucketLifecycleDeleteTypeDef",
    "DeleteBucketLifecycleRequestRequestTypeDef",
    "DeleteBucketMetricsConfigurationRequestRequestTypeDef",
    "DeleteBucketOwnershipControlsRequestRequestTypeDef",
    "DeleteBucketPolicyRequestBucketPolicyDeleteTypeDef",
    "DeleteBucketPolicyRequestRequestTypeDef",
    "DeleteBucketReplicationRequestRequestTypeDef",
    "DeleteBucketRequestBucketDeleteTypeDef",
    "DeleteBucketRequestRequestTypeDef",
    "DeleteBucketTaggingRequestBucketTaggingDeleteTypeDef",
    "DeleteBucketTaggingRequestRequestTypeDef",
    "DeleteBucketWebsiteRequestBucketWebsiteDeleteTypeDef",
    "DeleteBucketWebsiteRequestRequestTypeDef",
    "DeleteMarkerReplicationTypeDef",
    "DeleteObjectOutputTypeDef",
    "DeleteObjectRequestObjectDeleteTypeDef",
    "DeleteObjectRequestObjectSummaryDeleteTypeDef",
    "DeleteObjectRequestObjectVersionDeleteTypeDef",
    "DeleteObjectRequestRequestTypeDef",
    "DeleteObjectTaggingOutputTypeDef",
    "DeleteObjectTaggingRequestRequestTypeDef",
    "DeletedObjectTypeDef",
    "ErrorTypeDef",
    "DeletePublicAccessBlockRequestRequestTypeDef",
    "ObjectIdentifierTypeDef",
    "EncryptionConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionTypeDef",
    "ErrorDocumentResponseMetadataTypeDef",
    "ErrorDocumentTypeDef",
    "ExistingObjectReplicationTypeDef",
    "FilterRuleTypeDef",
    "GetBucketAccelerateConfigurationOutputTypeDef",
    "GetBucketAccelerateConfigurationRequestRequestTypeDef",
    "GetBucketAclRequestRequestTypeDef",
    "GetBucketAnalyticsConfigurationRequestRequestTypeDef",
    "GetBucketCorsRequestRequestTypeDef",
    "GetBucketEncryptionRequestRequestTypeDef",
    "GetBucketIntelligentTieringConfigurationRequestRequestTypeDef",
    "GetBucketInventoryConfigurationRequestRequestTypeDef",
    "GetBucketLifecycleConfigurationRequestRequestTypeDef",
    "GetBucketLifecycleRequestRequestTypeDef",
    "GetBucketLocationOutputTypeDef",
    "GetBucketLocationRequestRequestTypeDef",
    "GetBucketLoggingRequestRequestTypeDef",
    "GetBucketMetricsConfigurationRequestRequestTypeDef",
    "GetBucketNotificationConfigurationRequestRequestTypeDef",
    "GetBucketOwnershipControlsRequestRequestTypeDef",
    "GetBucketPolicyOutputTypeDef",
    "GetBucketPolicyRequestRequestTypeDef",
    "PolicyStatusTypeDef",
    "GetBucketPolicyStatusRequestRequestTypeDef",
    "GetBucketReplicationRequestRequestTypeDef",
    "GetBucketRequestPaymentOutputTypeDef",
    "GetBucketRequestPaymentRequestRequestTypeDef",
    "GetBucketTaggingRequestRequestTypeDef",
    "GetBucketVersioningOutputTypeDef",
    "GetBucketVersioningRequestRequestTypeDef",
    "IndexDocumentTypeDef",
    "RedirectAllRequestsToTypeDef",
    "GetBucketWebsiteRequestRequestTypeDef",
    "GetObjectAclRequestRequestTypeDef",
    "ObjectPartTypeDef",
    "GetObjectAttributesRequestRequestTypeDef",
    "ObjectLockLegalHoldTypeDef",
    "GetObjectLegalHoldRequestRequestTypeDef",
    "GetObjectLockConfigurationRequestRequestTypeDef",
    "GetObjectOutputTypeDef",
    "GetObjectRequestObjectGetTypeDef",
    "GetObjectRequestObjectSummaryGetTypeDef",
    "GetObjectRequestObjectVersionGetTypeDef",
    "GetObjectRequestRequestTypeDef",
    "ObjectLockRetentionTypeDef",
    "GetObjectRetentionRequestRequestTypeDef",
    "GetObjectTaggingRequestRequestTypeDef",
    "GetObjectTorrentOutputTypeDef",
    "GetObjectTorrentRequestRequestTypeDef",
    "PublicAccessBlockConfigurationTypeDef",
    "GetPublicAccessBlockRequestRequestTypeDef",
    "GlacierJobParametersTypeDef",
    "GranteeTypeDef",
    "WaiterConfigTypeDef",
    "HeadBucketRequestRequestTypeDef",
    "HeadObjectOutputTypeDef",
    "HeadObjectRequestObjectVersionHeadTypeDef",
    "HeadObjectRequestRequestTypeDef",
    "IndexDocumentResponseMetadataTypeDef",
    "InitiatorResponseMetadataTypeDef",
    "InitiatorTypeDef",
    "JSONInputTypeDef",
    "TieringTypeDef",
    "InventoryFilterTypeDef",
    "InventoryScheduleTypeDef",
    "SSEKMSTypeDef",
    "JSONOutputTypeDef",
    "LifecycleExpirationTypeDef",
    "NoncurrentVersionExpirationTypeDef",
    "NoncurrentVersionTransitionTypeDef",
    "TransitionTypeDef",
    "ListBucketAnalyticsConfigurationsRequestRequestTypeDef",
    "ListBucketIntelligentTieringConfigurationsRequestRequestTypeDef",
    "ListBucketInventoryConfigurationsRequestRequestTypeDef",
    "ListBucketMetricsConfigurationsRequestRequestTypeDef",
    "ListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef",
    "ListMultipartUploadsRequestRequestTypeDef",
    "ListObjectVersionsRequestListObjectVersionsPaginateTypeDef",
    "ListObjectVersionsRequestRequestTypeDef",
    "ListObjectsRequestListObjectsPaginateTypeDef",
    "ListObjectsRequestRequestTypeDef",
    "ListObjectsV2RequestListObjectsV2PaginateTypeDef",
    "ListObjectsV2RequestRequestTypeDef",
    "PartTypeDef",
    "ListPartsRequestListPartsPaginateTypeDef",
    "ListPartsRequestRequestTypeDef",
    "MetadataEntryTypeDef",
    "ReplicationTimeValueTypeDef",
    "QueueConfigurationDeprecatedTypeDef",
    "TopicConfigurationDeprecatedTypeDef",
    "ObjectDownloadFileRequestTypeDef",
    "ObjectDownloadFileobjRequestTypeDef",
    "RestoreStatusTypeDef",
    "ObjectUploadFileRequestTypeDef",
    "ObjectUploadFileobjRequestTypeDef",
    "OwnerResponseMetadataTypeDef",
    "OwnershipControlsRuleTypeDef",
    "PaginatorConfigTypeDef",
    "ProgressTypeDef",
    "PutBucketPolicyRequestBucketPolicyPutTypeDef",
    "PutBucketPolicyRequestRequestTypeDef",
    "RequestPaymentConfigurationTypeDef",
    "PutBucketVersioningRequestBucketVersioningEnableTypeDef",
    "VersioningConfigurationTypeDef",
    "PutBucketVersioningRequestBucketVersioningSuspendTypeDef",
    "PutObjectAclOutputTypeDef",
    "PutObjectLegalHoldOutputTypeDef",
    "PutObjectLockConfigurationOutputTypeDef",
    "PutObjectOutputTypeDef",
    "PutObjectRequestBucketPutObjectTypeDef",
    "PutObjectRequestObjectPutTypeDef",
    "PutObjectRequestObjectSummaryPutTypeDef",
    "PutObjectRequestRequestTypeDef",
    "PutObjectRetentionOutputTypeDef",
    "PutObjectTaggingOutputTypeDef",
    "RecordsEventTypeDef",
    "RedirectAllRequestsToResponseMetadataTypeDef",
    "RedirectTypeDef",
    "ReplicaModificationsTypeDef",
    "RequestProgressTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreObjectOutputTypeDef",
    "RestoreStatusResponseMetadataTypeDef",
    "ScanRangeTypeDef",
    "ServerSideEncryptionByDefaultTypeDef",
    "SseKmsEncryptedObjectsTypeDef",
    "StatsTypeDef",
    "UploadPartOutputTypeDef",
    "UploadPartRequestMultipartUploadPartUploadTypeDef",
    "UploadPartRequestRequestTypeDef",
    "WriteGetObjectResponseRequestRequestTypeDef",
    "PutBucketAccelerateConfigurationRequestRequestTypeDef",
    "DeleteMarkerEntryTypeDef",
    "AnalyticsAndOperatorTypeDef",
    "GetBucketTaggingOutputTypeDef",
    "GetObjectTaggingOutputTypeDef",
    "IntelligentTieringAndOperatorTypeDef",
    "LifecycleRuleAndOperatorTypeDef",
    "MetricsAndOperatorTypeDef",
    "ReplicationRuleAndOperatorTypeDef",
    "TaggingTypeDef",
    "AnalyticsExportDestinationTypeDef",
    "BucketCopyRequestTypeDef",
    "ClientCopyRequestTypeDef",
    "CopyObjectRequestRequestTypeDef",
    "ObjectCopyRequestTypeDef",
    "UploadPartCopyRequestMultipartUploadPartCopyFromTypeDef",
    "UploadPartCopyRequestRequestTypeDef",
    "ListBucketsOutputTypeDef",
    "CORSConfigurationTypeDef",
    "GetBucketCorsOutputTypeDef",
    "CompletedMultipartUploadTypeDef",
    "CopyObjectOutputTypeDef",
    "UploadPartCopyOutputTypeDef",
    "CreateBucketRequestBucketCreateTypeDef",
    "CreateBucketRequestRequestTypeDef",
    "CreateBucketRequestServiceResourceCreateBucketTypeDef",
    "ObjectLockRuleTypeDef",
    "DeleteObjectsOutputTypeDef",
    "DeleteTypeDef",
    "S3KeyFilterTypeDef",
    "GetBucketPolicyStatusOutputTypeDef",
    "GetObjectAttributesPartsTypeDef",
    "GetObjectLegalHoldOutputTypeDef",
    "PutObjectLegalHoldRequestRequestTypeDef",
    "GetObjectRetentionOutputTypeDef",
    "PutObjectRetentionRequestRequestTypeDef",
    "GetPublicAccessBlockOutputTypeDef",
    "PutPublicAccessBlockRequestRequestTypeDef",
    "GrantTypeDef",
    "TargetGrantTypeDef",
    "HeadBucketRequestBucketExistsWaitTypeDef",
    "HeadBucketRequestBucketNotExistsWaitTypeDef",
    "HeadObjectRequestObjectExistsWaitTypeDef",
    "HeadObjectRequestObjectNotExistsWaitTypeDef",
    "MultipartUploadTypeDef",
    "InputSerializationTypeDef",
    "InventoryEncryptionTypeDef",
    "OutputSerializationTypeDef",
    "RuleTypeDef",
    "ListPartsOutputTypeDef",
    "MetricsTypeDef",
    "ReplicationTimeTypeDef",
    "NotificationConfigurationDeprecatedResponseMetadataTypeDef",
    "NotificationConfigurationDeprecatedTypeDef",
    "ObjectTypeDef",
    "ObjectVersionTypeDef",
    "OwnershipControlsTypeDef",
    "ProgressEventTypeDef",
    "PutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef",
    "PutBucketRequestPaymentRequestRequestTypeDef",
    "PutBucketVersioningRequestBucketVersioningPutTypeDef",
    "PutBucketVersioningRequestRequestTypeDef",
    "RoutingRuleTypeDef",
    "ServerSideEncryptionRuleTypeDef",
    "SourceSelectionCriteriaTypeDef",
    "StatsEventTypeDef",
    "AnalyticsFilterTypeDef",
    "IntelligentTieringFilterTypeDef",
    "LifecycleRuleFilterTypeDef",
    "MetricsFilterTypeDef",
    "ReplicationRuleFilterTypeDef",
    "PutBucketTaggingRequestBucketTaggingPutTypeDef",
    "PutBucketTaggingRequestRequestTypeDef",
    "PutObjectTaggingRequestRequestTypeDef",
    "StorageClassAnalysisDataExportTypeDef",
    "PutBucketCorsRequestBucketCorsPutTypeDef",
    "PutBucketCorsRequestRequestTypeDef",
    "CompleteMultipartUploadRequestMultipartUploadCompleteTypeDef",
    "CompleteMultipartUploadRequestRequestTypeDef",
    "ObjectLockConfigurationTypeDef",
    "DeleteObjectsRequestBucketDeleteObjectsTypeDef",
    "DeleteObjectsRequestRequestTypeDef",
    "NotificationConfigurationFilterTypeDef",
    "GetObjectAttributesOutputTypeDef",
    "AccessControlPolicyTypeDef",
    "GetBucketAclOutputTypeDef",
    "GetObjectAclOutputTypeDef",
    "S3LocationTypeDef",
    "LoggingEnabledResponseMetadataTypeDef",
    "LoggingEnabledTypeDef",
    "ListMultipartUploadsOutputTypeDef",
    "InventoryS3BucketDestinationTypeDef",
    "SelectObjectContentRequestRequestTypeDef",
    "SelectParametersTypeDef",
    "GetBucketLifecycleOutputTypeDef",
    "LifecycleConfigurationTypeDef",
    "DestinationTypeDef",
    "PutBucketNotificationRequestRequestTypeDef",
    "ListObjectsOutputTypeDef",
    "ListObjectsV2OutputTypeDef",
    "ListObjectVersionsOutputTypeDef",
    "GetBucketOwnershipControlsOutputTypeDef",
    "PutBucketOwnershipControlsRequestRequestTypeDef",
    "GetBucketWebsiteOutputTypeDef",
    "WebsiteConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "SelectObjectContentEventStreamTypeDef",
    "IntelligentTieringConfigurationTypeDef",
    "LifecycleRuleTypeDef",
    "MetricsConfigurationTypeDef",
    "StorageClassAnalysisTypeDef",
    "GetObjectLockConfigurationOutputTypeDef",
    "PutObjectLockConfigurationRequestRequestTypeDef",
    "LambdaFunctionConfigurationTypeDef",
    "QueueConfigurationTypeDef",
    "TopicConfigurationTypeDef",
    "PutBucketAclRequestBucketAclPutTypeDef",
    "PutBucketAclRequestRequestTypeDef",
    "PutObjectAclRequestObjectAclPutTypeDef",
    "PutObjectAclRequestRequestTypeDef",
    "OutputLocationTypeDef",
    "BucketLoggingStatusTypeDef",
    "GetBucketLoggingOutputTypeDef",
    "InventoryDestinationTypeDef",
    "PutBucketLifecycleRequestBucketLifecyclePutTypeDef",
    "PutBucketLifecycleRequestRequestTypeDef",
    "ReplicationRuleTypeDef",
    "PutBucketWebsiteRequestBucketWebsitePutTypeDef",
    "PutBucketWebsiteRequestRequestTypeDef",
    "GetBucketEncryptionOutputTypeDef",
    "PutBucketEncryptionRequestRequestTypeDef",
    "SelectObjectContentOutputTypeDef",
    "GetBucketIntelligentTieringConfigurationOutputTypeDef",
    "ListBucketIntelligentTieringConfigurationsOutputTypeDef",
    "PutBucketIntelligentTieringConfigurationRequestRequestTypeDef",
    "BucketLifecycleConfigurationTypeDef",
    "GetBucketLifecycleConfigurationOutputTypeDef",
    "GetBucketMetricsConfigurationOutputTypeDef",
    "ListBucketMetricsConfigurationsOutputTypeDef",
    "PutBucketMetricsConfigurationRequestRequestTypeDef",
    "AnalyticsConfigurationTypeDef",
    "NotificationConfigurationResponseMetadataTypeDef",
    "NotificationConfigurationTypeDef",
    "RestoreRequestTypeDef",
    "PutBucketLoggingRequestBucketLoggingPutTypeDef",
    "PutBucketLoggingRequestRequestTypeDef",
    "InventoryConfigurationTypeDef",
    "ReplicationConfigurationTypeDef",
    "PutBucketLifecycleConfigurationRequestBucketLifecycleConfigurationPutTypeDef",
    "PutBucketLifecycleConfigurationRequestRequestTypeDef",
    "GetBucketAnalyticsConfigurationOutputTypeDef",
    "ListBucketAnalyticsConfigurationsOutputTypeDef",
    "PutBucketAnalyticsConfigurationRequestRequestTypeDef",
    "PutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef",
    "PutBucketNotificationConfigurationRequestRequestTypeDef",
    "RestoreObjectRequestObjectRestoreObjectTypeDef",
    "RestoreObjectRequestObjectSummaryRestoreObjectTypeDef",
    "RestoreObjectRequestRequestTypeDef",
    "GetBucketInventoryConfigurationOutputTypeDef",
    "ListBucketInventoryConfigurationsOutputTypeDef",
    "PutBucketInventoryConfigurationRequestRequestTypeDef",
    "GetBucketReplicationOutputTypeDef",
    "PutBucketReplicationRequestRequestTypeDef",
)

AbortIncompleteMultipartUploadTypeDef = TypedDict(
    "AbortIncompleteMultipartUploadTypeDef",
    {
        "DaysAfterInitiation": int,
    },
)

AbortMultipartUploadOutputTypeDef = TypedDict(
    "AbortMultipartUploadOutputTypeDef",
    {
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AbortMultipartUploadRequestMultipartUploadAbortTypeDef = TypedDict(
    "AbortMultipartUploadRequestMultipartUploadAbortTypeDef",
    {
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredAbortMultipartUploadRequestRequestTypeDef = TypedDict(
    "_RequiredAbortMultipartUploadRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "UploadId": str,
    },
)
_OptionalAbortMultipartUploadRequestRequestTypeDef = TypedDict(
    "_OptionalAbortMultipartUploadRequestRequestTypeDef",
    {
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class AbortMultipartUploadRequestRequestTypeDef(
    _RequiredAbortMultipartUploadRequestRequestTypeDef,
    _OptionalAbortMultipartUploadRequestRequestTypeDef,
):
    pass

AccelerateConfigurationTypeDef = TypedDict(
    "AccelerateConfigurationTypeDef",
    {
        "Status": BucketAccelerateStatusType,
    },
    total=False,
)

OwnerTypeDef = TypedDict(
    "OwnerTypeDef",
    {
        "DisplayName": str,
        "ID": str,
    },
)

AccessControlTranslationTypeDef = TypedDict(
    "AccessControlTranslationTypeDef",
    {
        "Owner": Literal["Destination"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

AnalyticsS3BucketDestinationTypeDef = TypedDict(
    "AnalyticsS3BucketDestinationTypeDef",
    {
        "Format": Literal["CSV"],
        "BucketAccountId": str,
        "Bucket": str,
        "Prefix": str,
    },
)

_RequiredCopySourceTypeDef = TypedDict(
    "_RequiredCopySourceTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalCopySourceTypeDef = TypedDict(
    "_OptionalCopySourceTypeDef",
    {
        "VersionId": str,
    },
    total=False,
)

class CopySourceTypeDef(_RequiredCopySourceTypeDef, _OptionalCopySourceTypeDef):
    pass

_RequiredBucketDownloadFileRequestTypeDef = TypedDict(
    "_RequiredBucketDownloadFileRequestTypeDef",
    {
        "Key": str,
        "Filename": str,
    },
)
_OptionalBucketDownloadFileRequestTypeDef = TypedDict(
    "_OptionalBucketDownloadFileRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class BucketDownloadFileRequestTypeDef(
    _RequiredBucketDownloadFileRequestTypeDef, _OptionalBucketDownloadFileRequestTypeDef
):
    pass

_RequiredBucketDownloadFileobjRequestTypeDef = TypedDict(
    "_RequiredBucketDownloadFileobjRequestTypeDef",
    {
        "Key": str,
        "Fileobj": Union[IO[Any], StreamingBody],
    },
)
_OptionalBucketDownloadFileobjRequestTypeDef = TypedDict(
    "_OptionalBucketDownloadFileobjRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class BucketDownloadFileobjRequestTypeDef(
    _RequiredBucketDownloadFileobjRequestTypeDef, _OptionalBucketDownloadFileobjRequestTypeDef
):
    pass

BucketTypeDef = TypedDict(
    "BucketTypeDef",
    {
        "Name": str,
        "CreationDate": datetime,
    },
)

_RequiredBucketUploadFileRequestTypeDef = TypedDict(
    "_RequiredBucketUploadFileRequestTypeDef",
    {
        "Filename": str,
        "Key": str,
    },
)
_OptionalBucketUploadFileRequestTypeDef = TypedDict(
    "_OptionalBucketUploadFileRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class BucketUploadFileRequestTypeDef(
    _RequiredBucketUploadFileRequestTypeDef, _OptionalBucketUploadFileRequestTypeDef
):
    pass

_RequiredBucketUploadFileobjRequestTypeDef = TypedDict(
    "_RequiredBucketUploadFileobjRequestTypeDef",
    {
        "Fileobj": Union[IO[Any], StreamingBody],
        "Key": str,
    },
)
_OptionalBucketUploadFileobjRequestTypeDef = TypedDict(
    "_OptionalBucketUploadFileobjRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class BucketUploadFileobjRequestTypeDef(
    _RequiredBucketUploadFileobjRequestTypeDef, _OptionalBucketUploadFileobjRequestTypeDef
):
    pass

CORSRuleTypeDef = TypedDict(
    "CORSRuleTypeDef",
    {
        "ID": str,
        "AllowedHeaders": List[str],
        "AllowedMethods": List[str],
        "AllowedOrigins": List[str],
        "ExposeHeaders": List[str],
        "MaxAgeSeconds": int,
    },
)

CSVInputTypeDef = TypedDict(
    "CSVInputTypeDef",
    {
        "FileHeaderInfo": FileHeaderInfoType,
        "Comments": str,
        "QuoteEscapeCharacter": str,
        "RecordDelimiter": str,
        "FieldDelimiter": str,
        "QuoteCharacter": str,
        "AllowQuotedRecordDelimiter": bool,
    },
    total=False,
)

CSVOutputTypeDef = TypedDict(
    "CSVOutputTypeDef",
    {
        "QuoteFields": QuoteFieldsType,
        "QuoteEscapeCharacter": str,
        "RecordDelimiter": str,
        "FieldDelimiter": str,
        "QuoteCharacter": str,
    },
    total=False,
)

ChecksumTypeDef = TypedDict(
    "ChecksumTypeDef",
    {
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
    },
)

_RequiredClientDownloadFileRequestTypeDef = TypedDict(
    "_RequiredClientDownloadFileRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "Filename": str,
    },
)
_OptionalClientDownloadFileRequestTypeDef = TypedDict(
    "_OptionalClientDownloadFileRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ClientDownloadFileRequestTypeDef(
    _RequiredClientDownloadFileRequestTypeDef, _OptionalClientDownloadFileRequestTypeDef
):
    pass

_RequiredClientDownloadFileobjRequestTypeDef = TypedDict(
    "_RequiredClientDownloadFileobjRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "Fileobj": Union[IO[Any], StreamingBody],
    },
)
_OptionalClientDownloadFileobjRequestTypeDef = TypedDict(
    "_OptionalClientDownloadFileobjRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ClientDownloadFileobjRequestTypeDef(
    _RequiredClientDownloadFileobjRequestTypeDef, _OptionalClientDownloadFileobjRequestTypeDef
):
    pass

_RequiredClientGeneratePresignedPostRequestTypeDef = TypedDict(
    "_RequiredClientGeneratePresignedPostRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalClientGeneratePresignedPostRequestTypeDef = TypedDict(
    "_OptionalClientGeneratePresignedPostRequestTypeDef",
    {
        "Fields": Dict[str, Any],
        "Conditions": Union[List[Any], Dict[str, Any]],
        "ExpiresIn": int,
    },
    total=False,
)

class ClientGeneratePresignedPostRequestTypeDef(
    _RequiredClientGeneratePresignedPostRequestTypeDef,
    _OptionalClientGeneratePresignedPostRequestTypeDef,
):
    pass

_RequiredClientUploadFileRequestTypeDef = TypedDict(
    "_RequiredClientUploadFileRequestTypeDef",
    {
        "Filename": str,
        "Bucket": str,
        "Key": str,
    },
)
_OptionalClientUploadFileRequestTypeDef = TypedDict(
    "_OptionalClientUploadFileRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ClientUploadFileRequestTypeDef(
    _RequiredClientUploadFileRequestTypeDef, _OptionalClientUploadFileRequestTypeDef
):
    pass

_RequiredClientUploadFileobjRequestTypeDef = TypedDict(
    "_RequiredClientUploadFileobjRequestTypeDef",
    {
        "Fileobj": Union[IO[Any], StreamingBody],
        "Bucket": str,
        "Key": str,
    },
)
_OptionalClientUploadFileobjRequestTypeDef = TypedDict(
    "_OptionalClientUploadFileobjRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ClientUploadFileobjRequestTypeDef(
    _RequiredClientUploadFileobjRequestTypeDef, _OptionalClientUploadFileobjRequestTypeDef
):
    pass

CloudFunctionConfigurationTypeDef = TypedDict(
    "CloudFunctionConfigurationTypeDef",
    {
        "Id": str,
        "Event": EventType,
        "Events": List[EventType],
        "CloudFunction": str,
        "InvocationRole": str,
    },
)

CommonPrefixTypeDef = TypedDict(
    "CommonPrefixTypeDef",
    {
        "Prefix": str,
    },
)

CompleteMultipartUploadOutputTypeDef = TypedDict(
    "CompleteMultipartUploadOutputTypeDef",
    {
        "Location": str,
        "Bucket": str,
        "Key": str,
        "Expiration": str,
        "ETag": str,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "ServerSideEncryption": ServerSideEncryptionType,
        "VersionId": str,
        "SSEKMSKeyId": str,
        "BucketKeyEnabled": bool,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CompletedPartTypeDef = TypedDict(
    "CompletedPartTypeDef",
    {
        "ETag": str,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "PartNumber": int,
    },
    total=False,
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "HttpErrorCodeReturnedEquals": str,
        "KeyPrefixEquals": str,
    },
)

CopyObjectResultTypeDef = TypedDict(
    "CopyObjectResultTypeDef",
    {
        "ETag": str,
        "LastModified": datetime,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
    },
)

_RequiredCopyObjectRequestObjectCopyFromTypeDef = TypedDict(
    "_RequiredCopyObjectRequestObjectCopyFromTypeDef",
    {
        "CopySource": str,
    },
)
_OptionalCopyObjectRequestObjectCopyFromTypeDef = TypedDict(
    "_OptionalCopyObjectRequestObjectCopyFromTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "CacheControl": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "CopySourceIfMatch": str,
        "CopySourceIfModifiedSince": Union[datetime, str],
        "CopySourceIfNoneMatch": str,
        "CopySourceIfUnmodifiedSince": Union[datetime, str],
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "MetadataDirective": MetadataDirectiveType,
        "TaggingDirective": TaggingDirectiveType,
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "CopySourceSSECustomerAlgorithm": str,
        "CopySourceSSECustomerKey": str,
        "CopySourceSSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
        "ExpectedSourceBucketOwner": str,
    },
    total=False,
)

class CopyObjectRequestObjectCopyFromTypeDef(
    _RequiredCopyObjectRequestObjectCopyFromTypeDef, _OptionalCopyObjectRequestObjectCopyFromTypeDef
):
    pass

_RequiredCopyObjectRequestObjectSummaryCopyFromTypeDef = TypedDict(
    "_RequiredCopyObjectRequestObjectSummaryCopyFromTypeDef",
    {
        "CopySource": str,
    },
)
_OptionalCopyObjectRequestObjectSummaryCopyFromTypeDef = TypedDict(
    "_OptionalCopyObjectRequestObjectSummaryCopyFromTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "CacheControl": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "CopySourceIfMatch": str,
        "CopySourceIfModifiedSince": Union[datetime, str],
        "CopySourceIfNoneMatch": str,
        "CopySourceIfUnmodifiedSince": Union[datetime, str],
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "MetadataDirective": MetadataDirectiveType,
        "TaggingDirective": TaggingDirectiveType,
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "CopySourceSSECustomerAlgorithm": str,
        "CopySourceSSECustomerKey": str,
        "CopySourceSSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
        "ExpectedSourceBucketOwner": str,
    },
    total=False,
)

class CopyObjectRequestObjectSummaryCopyFromTypeDef(
    _RequiredCopyObjectRequestObjectSummaryCopyFromTypeDef,
    _OptionalCopyObjectRequestObjectSummaryCopyFromTypeDef,
):
    pass

CopyPartResultTypeDef = TypedDict(
    "CopyPartResultTypeDef",
    {
        "ETag": str,
        "LastModified": datetime,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
    },
)

CreateBucketConfigurationTypeDef = TypedDict(
    "CreateBucketConfigurationTypeDef",
    {
        "LocationConstraint": BucketLocationConstraintType,
    },
    total=False,
)

CreateBucketOutputTypeDef = TypedDict(
    "CreateBucketOutputTypeDef",
    {
        "Location": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMultipartUploadOutputTypeDef = TypedDict(
    "CreateMultipartUploadOutputTypeDef",
    {
        "AbortDate": datetime,
        "AbortRuleId": str,
        "Bucket": str,
        "Key": str,
        "UploadId": str,
        "ServerSideEncryption": ServerSideEncryptionType,
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestCharged": Literal["requester"],
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMultipartUploadRequestObjectInitiateMultipartUploadTypeDef = TypedDict(
    "CreateMultipartUploadRequestObjectInitiateMultipartUploadTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
    },
    total=False,
)

CreateMultipartUploadRequestObjectSummaryInitiateMultipartUploadTypeDef = TypedDict(
    "CreateMultipartUploadRequestObjectSummaryInitiateMultipartUploadTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
    },
    total=False,
)

_RequiredCreateMultipartUploadRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMultipartUploadRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalCreateMultipartUploadRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMultipartUploadRequestRequestTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
    },
    total=False,
)

class CreateMultipartUploadRequestRequestTypeDef(
    _RequiredCreateMultipartUploadRequestRequestTypeDef,
    _OptionalCreateMultipartUploadRequestRequestTypeDef,
):
    pass

DefaultRetentionTypeDef = TypedDict(
    "DefaultRetentionTypeDef",
    {
        "Mode": ObjectLockRetentionModeType,
        "Days": int,
        "Years": int,
    },
)

_RequiredDeleteBucketAnalyticsConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketAnalyticsConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)
_OptionalDeleteBucketAnalyticsConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketAnalyticsConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketAnalyticsConfigurationRequestRequestTypeDef(
    _RequiredDeleteBucketAnalyticsConfigurationRequestRequestTypeDef,
    _OptionalDeleteBucketAnalyticsConfigurationRequestRequestTypeDef,
):
    pass

DeleteBucketCorsRequestBucketCorsDeleteTypeDef = TypedDict(
    "DeleteBucketCorsRequestBucketCorsDeleteTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredDeleteBucketCorsRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketCorsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketCorsRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketCorsRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketCorsRequestRequestTypeDef(
    _RequiredDeleteBucketCorsRequestRequestTypeDef, _OptionalDeleteBucketCorsRequestRequestTypeDef
):
    pass

_RequiredDeleteBucketEncryptionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketEncryptionRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketEncryptionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketEncryptionRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketEncryptionRequestRequestTypeDef(
    _RequiredDeleteBucketEncryptionRequestRequestTypeDef,
    _OptionalDeleteBucketEncryptionRequestRequestTypeDef,
):
    pass

DeleteBucketIntelligentTieringConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteBucketIntelligentTieringConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)

_RequiredDeleteBucketInventoryConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketInventoryConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)
_OptionalDeleteBucketInventoryConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketInventoryConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketInventoryConfigurationRequestRequestTypeDef(
    _RequiredDeleteBucketInventoryConfigurationRequestRequestTypeDef,
    _OptionalDeleteBucketInventoryConfigurationRequestRequestTypeDef,
):
    pass

DeleteBucketLifecycleRequestBucketLifecycleConfigurationDeleteTypeDef = TypedDict(
    "DeleteBucketLifecycleRequestBucketLifecycleConfigurationDeleteTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

DeleteBucketLifecycleRequestBucketLifecycleDeleteTypeDef = TypedDict(
    "DeleteBucketLifecycleRequestBucketLifecycleDeleteTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredDeleteBucketLifecycleRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketLifecycleRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketLifecycleRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketLifecycleRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketLifecycleRequestRequestTypeDef(
    _RequiredDeleteBucketLifecycleRequestRequestTypeDef,
    _OptionalDeleteBucketLifecycleRequestRequestTypeDef,
):
    pass

_RequiredDeleteBucketMetricsConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketMetricsConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)
_OptionalDeleteBucketMetricsConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketMetricsConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketMetricsConfigurationRequestRequestTypeDef(
    _RequiredDeleteBucketMetricsConfigurationRequestRequestTypeDef,
    _OptionalDeleteBucketMetricsConfigurationRequestRequestTypeDef,
):
    pass

_RequiredDeleteBucketOwnershipControlsRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketOwnershipControlsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketOwnershipControlsRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketOwnershipControlsRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketOwnershipControlsRequestRequestTypeDef(
    _RequiredDeleteBucketOwnershipControlsRequestRequestTypeDef,
    _OptionalDeleteBucketOwnershipControlsRequestRequestTypeDef,
):
    pass

DeleteBucketPolicyRequestBucketPolicyDeleteTypeDef = TypedDict(
    "DeleteBucketPolicyRequestBucketPolicyDeleteTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredDeleteBucketPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketPolicyRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketPolicyRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketPolicyRequestRequestTypeDef(
    _RequiredDeleteBucketPolicyRequestRequestTypeDef,
    _OptionalDeleteBucketPolicyRequestRequestTypeDef,
):
    pass

_RequiredDeleteBucketReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketReplicationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketReplicationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketReplicationRequestRequestTypeDef(
    _RequiredDeleteBucketReplicationRequestRequestTypeDef,
    _OptionalDeleteBucketReplicationRequestRequestTypeDef,
):
    pass

DeleteBucketRequestBucketDeleteTypeDef = TypedDict(
    "DeleteBucketRequestBucketDeleteTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredDeleteBucketRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketRequestRequestTypeDef(
    _RequiredDeleteBucketRequestRequestTypeDef, _OptionalDeleteBucketRequestRequestTypeDef
):
    pass

DeleteBucketTaggingRequestBucketTaggingDeleteTypeDef = TypedDict(
    "DeleteBucketTaggingRequestBucketTaggingDeleteTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredDeleteBucketTaggingRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketTaggingRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketTaggingRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketTaggingRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketTaggingRequestRequestTypeDef(
    _RequiredDeleteBucketTaggingRequestRequestTypeDef,
    _OptionalDeleteBucketTaggingRequestRequestTypeDef,
):
    pass

DeleteBucketWebsiteRequestBucketWebsiteDeleteTypeDef = TypedDict(
    "DeleteBucketWebsiteRequestBucketWebsiteDeleteTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredDeleteBucketWebsiteRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBucketWebsiteRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeleteBucketWebsiteRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBucketWebsiteRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteBucketWebsiteRequestRequestTypeDef(
    _RequiredDeleteBucketWebsiteRequestRequestTypeDef,
    _OptionalDeleteBucketWebsiteRequestRequestTypeDef,
):
    pass

DeleteMarkerReplicationTypeDef = TypedDict(
    "DeleteMarkerReplicationTypeDef",
    {
        "Status": DeleteMarkerReplicationStatusType,
    },
)

DeleteObjectOutputTypeDef = TypedDict(
    "DeleteObjectOutputTypeDef",
    {
        "DeleteMarker": bool,
        "VersionId": str,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteObjectRequestObjectDeleteTypeDef = TypedDict(
    "DeleteObjectRequestObjectDeleteTypeDef",
    {
        "MFA": str,
        "VersionId": str,
        "RequestPayer": Literal["requester"],
        "BypassGovernanceRetention": bool,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

DeleteObjectRequestObjectSummaryDeleteTypeDef = TypedDict(
    "DeleteObjectRequestObjectSummaryDeleteTypeDef",
    {
        "MFA": str,
        "VersionId": str,
        "RequestPayer": Literal["requester"],
        "BypassGovernanceRetention": bool,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

DeleteObjectRequestObjectVersionDeleteTypeDef = TypedDict(
    "DeleteObjectRequestObjectVersionDeleteTypeDef",
    {
        "MFA": str,
        "RequestPayer": Literal["requester"],
        "BypassGovernanceRetention": bool,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredDeleteObjectRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteObjectRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalDeleteObjectRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteObjectRequestRequestTypeDef",
    {
        "MFA": str,
        "VersionId": str,
        "RequestPayer": Literal["requester"],
        "BypassGovernanceRetention": bool,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteObjectRequestRequestTypeDef(
    _RequiredDeleteObjectRequestRequestTypeDef, _OptionalDeleteObjectRequestRequestTypeDef
):
    pass

DeleteObjectTaggingOutputTypeDef = TypedDict(
    "DeleteObjectTaggingOutputTypeDef",
    {
        "VersionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteObjectTaggingRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteObjectTaggingRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalDeleteObjectTaggingRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteObjectTaggingRequestRequestTypeDef",
    {
        "VersionId": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeleteObjectTaggingRequestRequestTypeDef(
    _RequiredDeleteObjectTaggingRequestRequestTypeDef,
    _OptionalDeleteObjectTaggingRequestRequestTypeDef,
):
    pass

DeletedObjectTypeDef = TypedDict(
    "DeletedObjectTypeDef",
    {
        "Key": str,
        "VersionId": str,
        "DeleteMarker": bool,
        "DeleteMarkerVersionId": str,
    },
)

ErrorTypeDef = TypedDict(
    "ErrorTypeDef",
    {
        "Key": str,
        "VersionId": str,
        "Code": str,
        "Message": str,
    },
)

_RequiredDeletePublicAccessBlockRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePublicAccessBlockRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalDeletePublicAccessBlockRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePublicAccessBlockRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class DeletePublicAccessBlockRequestRequestTypeDef(
    _RequiredDeletePublicAccessBlockRequestRequestTypeDef,
    _OptionalDeletePublicAccessBlockRequestRequestTypeDef,
):
    pass

_RequiredObjectIdentifierTypeDef = TypedDict(
    "_RequiredObjectIdentifierTypeDef",
    {
        "Key": str,
    },
)
_OptionalObjectIdentifierTypeDef = TypedDict(
    "_OptionalObjectIdentifierTypeDef",
    {
        "VersionId": str,
    },
    total=False,
)

class ObjectIdentifierTypeDef(_RequiredObjectIdentifierTypeDef, _OptionalObjectIdentifierTypeDef):
    pass

EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "ReplicaKmsKeyID": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEncryptionTypeDef = TypedDict(
    "_RequiredEncryptionTypeDef",
    {
        "EncryptionType": ServerSideEncryptionType,
    },
)
_OptionalEncryptionTypeDef = TypedDict(
    "_OptionalEncryptionTypeDef",
    {
        "KMSKeyId": str,
        "KMSContext": str,
    },
    total=False,
)

class EncryptionTypeDef(_RequiredEncryptionTypeDef, _OptionalEncryptionTypeDef):
    pass

ErrorDocumentResponseMetadataTypeDef = TypedDict(
    "ErrorDocumentResponseMetadataTypeDef",
    {
        "Key": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ErrorDocumentTypeDef = TypedDict(
    "ErrorDocumentTypeDef",
    {
        "Key": str,
    },
)

ExistingObjectReplicationTypeDef = TypedDict(
    "ExistingObjectReplicationTypeDef",
    {
        "Status": ExistingObjectReplicationStatusType,
    },
)

FilterRuleTypeDef = TypedDict(
    "FilterRuleTypeDef",
    {
        "Name": FilterRuleNameType,
        "Value": str,
    },
)

GetBucketAccelerateConfigurationOutputTypeDef = TypedDict(
    "GetBucketAccelerateConfigurationOutputTypeDef",
    {
        "Status": BucketAccelerateStatusType,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetBucketAccelerateConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketAccelerateConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketAccelerateConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketAccelerateConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
        "RequestPayer": Literal["requester"],
    },
    total=False,
)

class GetBucketAccelerateConfigurationRequestRequestTypeDef(
    _RequiredGetBucketAccelerateConfigurationRequestRequestTypeDef,
    _OptionalGetBucketAccelerateConfigurationRequestRequestTypeDef,
):
    pass

_RequiredGetBucketAclRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketAclRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketAclRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketAclRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketAclRequestRequestTypeDef(
    _RequiredGetBucketAclRequestRequestTypeDef, _OptionalGetBucketAclRequestRequestTypeDef
):
    pass

_RequiredGetBucketAnalyticsConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketAnalyticsConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)
_OptionalGetBucketAnalyticsConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketAnalyticsConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketAnalyticsConfigurationRequestRequestTypeDef(
    _RequiredGetBucketAnalyticsConfigurationRequestRequestTypeDef,
    _OptionalGetBucketAnalyticsConfigurationRequestRequestTypeDef,
):
    pass

_RequiredGetBucketCorsRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketCorsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketCorsRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketCorsRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketCorsRequestRequestTypeDef(
    _RequiredGetBucketCorsRequestRequestTypeDef, _OptionalGetBucketCorsRequestRequestTypeDef
):
    pass

_RequiredGetBucketEncryptionRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketEncryptionRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketEncryptionRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketEncryptionRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketEncryptionRequestRequestTypeDef(
    _RequiredGetBucketEncryptionRequestRequestTypeDef,
    _OptionalGetBucketEncryptionRequestRequestTypeDef,
):
    pass

GetBucketIntelligentTieringConfigurationRequestRequestTypeDef = TypedDict(
    "GetBucketIntelligentTieringConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)

_RequiredGetBucketInventoryConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketInventoryConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)
_OptionalGetBucketInventoryConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketInventoryConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketInventoryConfigurationRequestRequestTypeDef(
    _RequiredGetBucketInventoryConfigurationRequestRequestTypeDef,
    _OptionalGetBucketInventoryConfigurationRequestRequestTypeDef,
):
    pass

_RequiredGetBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketLifecycleConfigurationRequestRequestTypeDef(
    _RequiredGetBucketLifecycleConfigurationRequestRequestTypeDef,
    _OptionalGetBucketLifecycleConfigurationRequestRequestTypeDef,
):
    pass

_RequiredGetBucketLifecycleRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketLifecycleRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketLifecycleRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketLifecycleRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketLifecycleRequestRequestTypeDef(
    _RequiredGetBucketLifecycleRequestRequestTypeDef,
    _OptionalGetBucketLifecycleRequestRequestTypeDef,
):
    pass

GetBucketLocationOutputTypeDef = TypedDict(
    "GetBucketLocationOutputTypeDef",
    {
        "LocationConstraint": BucketLocationConstraintType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetBucketLocationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketLocationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketLocationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketLocationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketLocationRequestRequestTypeDef(
    _RequiredGetBucketLocationRequestRequestTypeDef, _OptionalGetBucketLocationRequestRequestTypeDef
):
    pass

_RequiredGetBucketLoggingRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketLoggingRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketLoggingRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketLoggingRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketLoggingRequestRequestTypeDef(
    _RequiredGetBucketLoggingRequestRequestTypeDef, _OptionalGetBucketLoggingRequestRequestTypeDef
):
    pass

_RequiredGetBucketMetricsConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketMetricsConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
    },
)
_OptionalGetBucketMetricsConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketMetricsConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketMetricsConfigurationRequestRequestTypeDef(
    _RequiredGetBucketMetricsConfigurationRequestRequestTypeDef,
    _OptionalGetBucketMetricsConfigurationRequestRequestTypeDef,
):
    pass

_RequiredGetBucketNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketNotificationConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketNotificationConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketNotificationConfigurationRequestRequestTypeDef(
    _RequiredGetBucketNotificationConfigurationRequestRequestTypeDef,
    _OptionalGetBucketNotificationConfigurationRequestRequestTypeDef,
):
    pass

_RequiredGetBucketOwnershipControlsRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketOwnershipControlsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketOwnershipControlsRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketOwnershipControlsRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketOwnershipControlsRequestRequestTypeDef(
    _RequiredGetBucketOwnershipControlsRequestRequestTypeDef,
    _OptionalGetBucketOwnershipControlsRequestRequestTypeDef,
):
    pass

GetBucketPolicyOutputTypeDef = TypedDict(
    "GetBucketPolicyOutputTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetBucketPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketPolicyRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketPolicyRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketPolicyRequestRequestTypeDef(
    _RequiredGetBucketPolicyRequestRequestTypeDef, _OptionalGetBucketPolicyRequestRequestTypeDef
):
    pass

PolicyStatusTypeDef = TypedDict(
    "PolicyStatusTypeDef",
    {
        "IsPublic": bool,
    },
)

_RequiredGetBucketPolicyStatusRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketPolicyStatusRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketPolicyStatusRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketPolicyStatusRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketPolicyStatusRequestRequestTypeDef(
    _RequiredGetBucketPolicyStatusRequestRequestTypeDef,
    _OptionalGetBucketPolicyStatusRequestRequestTypeDef,
):
    pass

_RequiredGetBucketReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketReplicationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketReplicationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketReplicationRequestRequestTypeDef(
    _RequiredGetBucketReplicationRequestRequestTypeDef,
    _OptionalGetBucketReplicationRequestRequestTypeDef,
):
    pass

GetBucketRequestPaymentOutputTypeDef = TypedDict(
    "GetBucketRequestPaymentOutputTypeDef",
    {
        "Payer": PayerType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetBucketRequestPaymentRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketRequestPaymentRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketRequestPaymentRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketRequestPaymentRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketRequestPaymentRequestRequestTypeDef(
    _RequiredGetBucketRequestPaymentRequestRequestTypeDef,
    _OptionalGetBucketRequestPaymentRequestRequestTypeDef,
):
    pass

_RequiredGetBucketTaggingRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketTaggingRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketTaggingRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketTaggingRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketTaggingRequestRequestTypeDef(
    _RequiredGetBucketTaggingRequestRequestTypeDef, _OptionalGetBucketTaggingRequestRequestTypeDef
):
    pass

GetBucketVersioningOutputTypeDef = TypedDict(
    "GetBucketVersioningOutputTypeDef",
    {
        "Status": BucketVersioningStatusType,
        "MFADelete": MFADeleteStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetBucketVersioningRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketVersioningRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketVersioningRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketVersioningRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketVersioningRequestRequestTypeDef(
    _RequiredGetBucketVersioningRequestRequestTypeDef,
    _OptionalGetBucketVersioningRequestRequestTypeDef,
):
    pass

IndexDocumentTypeDef = TypedDict(
    "IndexDocumentTypeDef",
    {
        "Suffix": str,
    },
)

RedirectAllRequestsToTypeDef = TypedDict(
    "RedirectAllRequestsToTypeDef",
    {
        "HostName": str,
        "Protocol": ProtocolType,
    },
)

_RequiredGetBucketWebsiteRequestRequestTypeDef = TypedDict(
    "_RequiredGetBucketWebsiteRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetBucketWebsiteRequestRequestTypeDef = TypedDict(
    "_OptionalGetBucketWebsiteRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetBucketWebsiteRequestRequestTypeDef(
    _RequiredGetBucketWebsiteRequestRequestTypeDef, _OptionalGetBucketWebsiteRequestRequestTypeDef
):
    pass

_RequiredGetObjectAclRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectAclRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalGetObjectAclRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectAclRequestRequestTypeDef",
    {
        "VersionId": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetObjectAclRequestRequestTypeDef(
    _RequiredGetObjectAclRequestRequestTypeDef, _OptionalGetObjectAclRequestRequestTypeDef
):
    pass

ObjectPartTypeDef = TypedDict(
    "ObjectPartTypeDef",
    {
        "PartNumber": int,
        "Size": int,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
    },
)

_RequiredGetObjectAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectAttributesRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "ObjectAttributes": Sequence[ObjectAttributesType],
    },
)
_OptionalGetObjectAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectAttributesRequestRequestTypeDef",
    {
        "VersionId": str,
        "MaxParts": int,
        "PartNumberMarker": int,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetObjectAttributesRequestRequestTypeDef(
    _RequiredGetObjectAttributesRequestRequestTypeDef,
    _OptionalGetObjectAttributesRequestRequestTypeDef,
):
    pass

ObjectLockLegalHoldTypeDef = TypedDict(
    "ObjectLockLegalHoldTypeDef",
    {
        "Status": ObjectLockLegalHoldStatusType,
    },
)

_RequiredGetObjectLegalHoldRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectLegalHoldRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalGetObjectLegalHoldRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectLegalHoldRequestRequestTypeDef",
    {
        "VersionId": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetObjectLegalHoldRequestRequestTypeDef(
    _RequiredGetObjectLegalHoldRequestRequestTypeDef,
    _OptionalGetObjectLegalHoldRequestRequestTypeDef,
):
    pass

_RequiredGetObjectLockConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectLockConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetObjectLockConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectLockConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetObjectLockConfigurationRequestRequestTypeDef(
    _RequiredGetObjectLockConfigurationRequestRequestTypeDef,
    _OptionalGetObjectLockConfigurationRequestRequestTypeDef,
):
    pass

GetObjectOutputTypeDef = TypedDict(
    "GetObjectOutputTypeDef",
    {
        "Body": StreamingBody,
        "DeleteMarker": bool,
        "AcceptRanges": str,
        "Expiration": str,
        "Restore": str,
        "LastModified": datetime,
        "ContentLength": int,
        "ETag": str,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "MissingMeta": int,
        "VersionId": str,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentRange": str,
        "ContentType": str,
        "Expires": datetime,
        "WebsiteRedirectLocation": str,
        "ServerSideEncryption": ServerSideEncryptionType,
        "Metadata": Dict[str, str],
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "BucketKeyEnabled": bool,
        "StorageClass": StorageClassType,
        "RequestCharged": Literal["requester"],
        "ReplicationStatus": ReplicationStatusType,
        "PartsCount": int,
        "TagCount": int,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": datetime,
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetObjectRequestObjectGetTypeDef = TypedDict(
    "GetObjectRequestObjectGetTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "ResponseCacheControl": str,
        "ResponseContentDisposition": str,
        "ResponseContentEncoding": str,
        "ResponseContentLanguage": str,
        "ResponseContentType": str,
        "ResponseExpires": Union[datetime, str],
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
    },
    total=False,
)

GetObjectRequestObjectSummaryGetTypeDef = TypedDict(
    "GetObjectRequestObjectSummaryGetTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "ResponseCacheControl": str,
        "ResponseContentDisposition": str,
        "ResponseContentEncoding": str,
        "ResponseContentLanguage": str,
        "ResponseContentType": str,
        "ResponseExpires": Union[datetime, str],
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
    },
    total=False,
)

GetObjectRequestObjectVersionGetTypeDef = TypedDict(
    "GetObjectRequestObjectVersionGetTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "ResponseCacheControl": str,
        "ResponseContentDisposition": str,
        "ResponseContentEncoding": str,
        "ResponseContentLanguage": str,
        "ResponseContentType": str,
        "ResponseExpires": Union[datetime, str],
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
    },
    total=False,
)

_RequiredGetObjectRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalGetObjectRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectRequestRequestTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "ResponseCacheControl": str,
        "ResponseContentDisposition": str,
        "ResponseContentEncoding": str,
        "ResponseContentLanguage": str,
        "ResponseContentType": str,
        "ResponseExpires": Union[datetime, str],
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
    },
    total=False,
)

class GetObjectRequestRequestTypeDef(
    _RequiredGetObjectRequestRequestTypeDef, _OptionalGetObjectRequestRequestTypeDef
):
    pass

ObjectLockRetentionTypeDef = TypedDict(
    "ObjectLockRetentionTypeDef",
    {
        "Mode": ObjectLockRetentionModeType,
        "RetainUntilDate": datetime,
    },
)

_RequiredGetObjectRetentionRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectRetentionRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalGetObjectRetentionRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectRetentionRequestRequestTypeDef",
    {
        "VersionId": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetObjectRetentionRequestRequestTypeDef(
    _RequiredGetObjectRetentionRequestRequestTypeDef,
    _OptionalGetObjectRetentionRequestRequestTypeDef,
):
    pass

_RequiredGetObjectTaggingRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectTaggingRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalGetObjectTaggingRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectTaggingRequestRequestTypeDef",
    {
        "VersionId": str,
        "ExpectedBucketOwner": str,
        "RequestPayer": Literal["requester"],
    },
    total=False,
)

class GetObjectTaggingRequestRequestTypeDef(
    _RequiredGetObjectTaggingRequestRequestTypeDef, _OptionalGetObjectTaggingRequestRequestTypeDef
):
    pass

GetObjectTorrentOutputTypeDef = TypedDict(
    "GetObjectTorrentOutputTypeDef",
    {
        "Body": StreamingBody,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetObjectTorrentRequestRequestTypeDef = TypedDict(
    "_RequiredGetObjectTorrentRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalGetObjectTorrentRequestRequestTypeDef = TypedDict(
    "_OptionalGetObjectTorrentRequestRequestTypeDef",
    {
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetObjectTorrentRequestRequestTypeDef(
    _RequiredGetObjectTorrentRequestRequestTypeDef, _OptionalGetObjectTorrentRequestRequestTypeDef
):
    pass

PublicAccessBlockConfigurationTypeDef = TypedDict(
    "PublicAccessBlockConfigurationTypeDef",
    {
        "BlockPublicAcls": bool,
        "IgnorePublicAcls": bool,
        "BlockPublicPolicy": bool,
        "RestrictPublicBuckets": bool,
    },
)

_RequiredGetPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "_RequiredGetPublicAccessBlockRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalGetPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "_OptionalGetPublicAccessBlockRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class GetPublicAccessBlockRequestRequestTypeDef(
    _RequiredGetPublicAccessBlockRequestRequestTypeDef,
    _OptionalGetPublicAccessBlockRequestRequestTypeDef,
):
    pass

GlacierJobParametersTypeDef = TypedDict(
    "GlacierJobParametersTypeDef",
    {
        "Tier": TierType,
    },
)

GranteeTypeDef = TypedDict(
    "GranteeTypeDef",
    {
        "DisplayName": str,
        "EmailAddress": str,
        "ID": str,
        "Type": TypeType,
        "URI": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

_RequiredHeadBucketRequestRequestTypeDef = TypedDict(
    "_RequiredHeadBucketRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalHeadBucketRequestRequestTypeDef = TypedDict(
    "_OptionalHeadBucketRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class HeadBucketRequestRequestTypeDef(
    _RequiredHeadBucketRequestRequestTypeDef, _OptionalHeadBucketRequestRequestTypeDef
):
    pass

HeadObjectOutputTypeDef = TypedDict(
    "HeadObjectOutputTypeDef",
    {
        "DeleteMarker": bool,
        "AcceptRanges": str,
        "Expiration": str,
        "Restore": str,
        "ArchiveStatus": ArchiveStatusType,
        "LastModified": datetime,
        "ContentLength": int,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "ETag": str,
        "MissingMeta": int,
        "VersionId": str,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "Expires": datetime,
        "WebsiteRedirectLocation": str,
        "ServerSideEncryption": ServerSideEncryptionType,
        "Metadata": Dict[str, str],
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "BucketKeyEnabled": bool,
        "StorageClass": StorageClassType,
        "RequestCharged": Literal["requester"],
        "ReplicationStatus": ReplicationStatusType,
        "PartsCount": int,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": datetime,
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HeadObjectRequestObjectVersionHeadTypeDef = TypedDict(
    "HeadObjectRequestObjectVersionHeadTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
    },
    total=False,
)

_RequiredHeadObjectRequestRequestTypeDef = TypedDict(
    "_RequiredHeadObjectRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalHeadObjectRequestRequestTypeDef = TypedDict(
    "_OptionalHeadObjectRequestRequestTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
    },
    total=False,
)

class HeadObjectRequestRequestTypeDef(
    _RequiredHeadObjectRequestRequestTypeDef, _OptionalHeadObjectRequestRequestTypeDef
):
    pass

IndexDocumentResponseMetadataTypeDef = TypedDict(
    "IndexDocumentResponseMetadataTypeDef",
    {
        "Suffix": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InitiatorResponseMetadataTypeDef = TypedDict(
    "InitiatorResponseMetadataTypeDef",
    {
        "ID": str,
        "DisplayName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InitiatorTypeDef = TypedDict(
    "InitiatorTypeDef",
    {
        "ID": str,
        "DisplayName": str,
    },
)

JSONInputTypeDef = TypedDict(
    "JSONInputTypeDef",
    {
        "Type": JSONTypeType,
    },
    total=False,
)

TieringTypeDef = TypedDict(
    "TieringTypeDef",
    {
        "Days": int,
        "AccessTier": IntelligentTieringAccessTierType,
    },
)

InventoryFilterTypeDef = TypedDict(
    "InventoryFilterTypeDef",
    {
        "Prefix": str,
    },
)

InventoryScheduleTypeDef = TypedDict(
    "InventoryScheduleTypeDef",
    {
        "Frequency": InventoryFrequencyType,
    },
)

SSEKMSTypeDef = TypedDict(
    "SSEKMSTypeDef",
    {
        "KeyId": str,
    },
)

JSONOutputTypeDef = TypedDict(
    "JSONOutputTypeDef",
    {
        "RecordDelimiter": str,
    },
    total=False,
)

LifecycleExpirationTypeDef = TypedDict(
    "LifecycleExpirationTypeDef",
    {
        "Date": datetime,
        "Days": int,
        "ExpiredObjectDeleteMarker": bool,
    },
)

NoncurrentVersionExpirationTypeDef = TypedDict(
    "NoncurrentVersionExpirationTypeDef",
    {
        "NoncurrentDays": int,
        "NewerNoncurrentVersions": int,
    },
)

NoncurrentVersionTransitionTypeDef = TypedDict(
    "NoncurrentVersionTransitionTypeDef",
    {
        "NoncurrentDays": int,
        "StorageClass": TransitionStorageClassType,
        "NewerNoncurrentVersions": int,
    },
)

TransitionTypeDef = TypedDict(
    "TransitionTypeDef",
    {
        "Date": datetime,
        "Days": int,
        "StorageClass": TransitionStorageClassType,
    },
)

_RequiredListBucketAnalyticsConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListBucketAnalyticsConfigurationsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListBucketAnalyticsConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListBucketAnalyticsConfigurationsRequestRequestTypeDef",
    {
        "ContinuationToken": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class ListBucketAnalyticsConfigurationsRequestRequestTypeDef(
    _RequiredListBucketAnalyticsConfigurationsRequestRequestTypeDef,
    _OptionalListBucketAnalyticsConfigurationsRequestRequestTypeDef,
):
    pass

_RequiredListBucketIntelligentTieringConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListBucketIntelligentTieringConfigurationsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListBucketIntelligentTieringConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListBucketIntelligentTieringConfigurationsRequestRequestTypeDef",
    {
        "ContinuationToken": str,
    },
    total=False,
)

class ListBucketIntelligentTieringConfigurationsRequestRequestTypeDef(
    _RequiredListBucketIntelligentTieringConfigurationsRequestRequestTypeDef,
    _OptionalListBucketIntelligentTieringConfigurationsRequestRequestTypeDef,
):
    pass

_RequiredListBucketInventoryConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListBucketInventoryConfigurationsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListBucketInventoryConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListBucketInventoryConfigurationsRequestRequestTypeDef",
    {
        "ContinuationToken": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class ListBucketInventoryConfigurationsRequestRequestTypeDef(
    _RequiredListBucketInventoryConfigurationsRequestRequestTypeDef,
    _OptionalListBucketInventoryConfigurationsRequestRequestTypeDef,
):
    pass

_RequiredListBucketMetricsConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListBucketMetricsConfigurationsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListBucketMetricsConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListBucketMetricsConfigurationsRequestRequestTypeDef",
    {
        "ContinuationToken": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class ListBucketMetricsConfigurationsRequestRequestTypeDef(
    _RequiredListBucketMetricsConfigurationsRequestRequestTypeDef,
    _OptionalListBucketMetricsConfigurationsRequestRequestTypeDef,
):
    pass

_RequiredListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef = TypedDict(
    "_RequiredListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef = TypedDict(
    "_OptionalListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "Prefix": str,
        "ExpectedBucketOwner": str,
        "RequestPayer": Literal["requester"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef(
    _RequiredListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef,
    _OptionalListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef,
):
    pass

_RequiredListMultipartUploadsRequestRequestTypeDef = TypedDict(
    "_RequiredListMultipartUploadsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListMultipartUploadsRequestRequestTypeDef = TypedDict(
    "_OptionalListMultipartUploadsRequestRequestTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "KeyMarker": str,
        "MaxUploads": int,
        "Prefix": str,
        "UploadIdMarker": str,
        "ExpectedBucketOwner": str,
        "RequestPayer": Literal["requester"],
    },
    total=False,
)

class ListMultipartUploadsRequestRequestTypeDef(
    _RequiredListMultipartUploadsRequestRequestTypeDef,
    _OptionalListMultipartUploadsRequestRequestTypeDef,
):
    pass

_RequiredListObjectVersionsRequestListObjectVersionsPaginateTypeDef = TypedDict(
    "_RequiredListObjectVersionsRequestListObjectVersionsPaginateTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListObjectVersionsRequestListObjectVersionsPaginateTypeDef = TypedDict(
    "_OptionalListObjectVersionsRequestListObjectVersionsPaginateTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "Prefix": str,
        "ExpectedBucketOwner": str,
        "RequestPayer": Literal["requester"],
        "OptionalObjectAttributes": Sequence[Literal["RestoreStatus"]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListObjectVersionsRequestListObjectVersionsPaginateTypeDef(
    _RequiredListObjectVersionsRequestListObjectVersionsPaginateTypeDef,
    _OptionalListObjectVersionsRequestListObjectVersionsPaginateTypeDef,
):
    pass

_RequiredListObjectVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListObjectVersionsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListObjectVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListObjectVersionsRequestRequestTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "KeyMarker": str,
        "MaxKeys": int,
        "Prefix": str,
        "VersionIdMarker": str,
        "ExpectedBucketOwner": str,
        "RequestPayer": Literal["requester"],
        "OptionalObjectAttributes": Sequence[Literal["RestoreStatus"]],
    },
    total=False,
)

class ListObjectVersionsRequestRequestTypeDef(
    _RequiredListObjectVersionsRequestRequestTypeDef,
    _OptionalListObjectVersionsRequestRequestTypeDef,
):
    pass

_RequiredListObjectsRequestListObjectsPaginateTypeDef = TypedDict(
    "_RequiredListObjectsRequestListObjectsPaginateTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListObjectsRequestListObjectsPaginateTypeDef = TypedDict(
    "_OptionalListObjectsRequestListObjectsPaginateTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "Prefix": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "OptionalObjectAttributes": Sequence[Literal["RestoreStatus"]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListObjectsRequestListObjectsPaginateTypeDef(
    _RequiredListObjectsRequestListObjectsPaginateTypeDef,
    _OptionalListObjectsRequestListObjectsPaginateTypeDef,
):
    pass

_RequiredListObjectsRequestRequestTypeDef = TypedDict(
    "_RequiredListObjectsRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListObjectsRequestRequestTypeDef = TypedDict(
    "_OptionalListObjectsRequestRequestTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "Marker": str,
        "MaxKeys": int,
        "Prefix": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "OptionalObjectAttributes": Sequence[Literal["RestoreStatus"]],
    },
    total=False,
)

class ListObjectsRequestRequestTypeDef(
    _RequiredListObjectsRequestRequestTypeDef, _OptionalListObjectsRequestRequestTypeDef
):
    pass

_RequiredListObjectsV2RequestListObjectsV2PaginateTypeDef = TypedDict(
    "_RequiredListObjectsV2RequestListObjectsV2PaginateTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListObjectsV2RequestListObjectsV2PaginateTypeDef = TypedDict(
    "_OptionalListObjectsV2RequestListObjectsV2PaginateTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "Prefix": str,
        "FetchOwner": bool,
        "StartAfter": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "OptionalObjectAttributes": Sequence[Literal["RestoreStatus"]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListObjectsV2RequestListObjectsV2PaginateTypeDef(
    _RequiredListObjectsV2RequestListObjectsV2PaginateTypeDef,
    _OptionalListObjectsV2RequestListObjectsV2PaginateTypeDef,
):
    pass

_RequiredListObjectsV2RequestRequestTypeDef = TypedDict(
    "_RequiredListObjectsV2RequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalListObjectsV2RequestRequestTypeDef = TypedDict(
    "_OptionalListObjectsV2RequestRequestTypeDef",
    {
        "Delimiter": str,
        "EncodingType": Literal["url"],
        "MaxKeys": int,
        "Prefix": str,
        "ContinuationToken": str,
        "FetchOwner": bool,
        "StartAfter": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "OptionalObjectAttributes": Sequence[Literal["RestoreStatus"]],
    },
    total=False,
)

class ListObjectsV2RequestRequestTypeDef(
    _RequiredListObjectsV2RequestRequestTypeDef, _OptionalListObjectsV2RequestRequestTypeDef
):
    pass

PartTypeDef = TypedDict(
    "PartTypeDef",
    {
        "PartNumber": int,
        "LastModified": datetime,
        "ETag": str,
        "Size": int,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
    },
)

_RequiredListPartsRequestListPartsPaginateTypeDef = TypedDict(
    "_RequiredListPartsRequestListPartsPaginateTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "UploadId": str,
    },
)
_OptionalListPartsRequestListPartsPaginateTypeDef = TypedDict(
    "_OptionalListPartsRequestListPartsPaginateTypeDef",
    {
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListPartsRequestListPartsPaginateTypeDef(
    _RequiredListPartsRequestListPartsPaginateTypeDef,
    _OptionalListPartsRequestListPartsPaginateTypeDef,
):
    pass

_RequiredListPartsRequestRequestTypeDef = TypedDict(
    "_RequiredListPartsRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "UploadId": str,
    },
)
_OptionalListPartsRequestRequestTypeDef = TypedDict(
    "_OptionalListPartsRequestRequestTypeDef",
    {
        "MaxParts": int,
        "PartNumberMarker": int,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
    },
    total=False,
)

class ListPartsRequestRequestTypeDef(
    _RequiredListPartsRequestRequestTypeDef, _OptionalListPartsRequestRequestTypeDef
):
    pass

MetadataEntryTypeDef = TypedDict(
    "MetadataEntryTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

ReplicationTimeValueTypeDef = TypedDict(
    "ReplicationTimeValueTypeDef",
    {
        "Minutes": int,
    },
)

QueueConfigurationDeprecatedTypeDef = TypedDict(
    "QueueConfigurationDeprecatedTypeDef",
    {
        "Id": str,
        "Event": EventType,
        "Events": List[EventType],
        "Queue": str,
    },
)

TopicConfigurationDeprecatedTypeDef = TypedDict(
    "TopicConfigurationDeprecatedTypeDef",
    {
        "Id": str,
        "Events": List[EventType],
        "Event": EventType,
        "Topic": str,
    },
)

_RequiredObjectDownloadFileRequestTypeDef = TypedDict(
    "_RequiredObjectDownloadFileRequestTypeDef",
    {
        "Filename": str,
    },
)
_OptionalObjectDownloadFileRequestTypeDef = TypedDict(
    "_OptionalObjectDownloadFileRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ObjectDownloadFileRequestTypeDef(
    _RequiredObjectDownloadFileRequestTypeDef, _OptionalObjectDownloadFileRequestTypeDef
):
    pass

_RequiredObjectDownloadFileobjRequestTypeDef = TypedDict(
    "_RequiredObjectDownloadFileobjRequestTypeDef",
    {
        "Fileobj": Union[IO[Any], StreamingBody],
    },
)
_OptionalObjectDownloadFileobjRequestTypeDef = TypedDict(
    "_OptionalObjectDownloadFileobjRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ObjectDownloadFileobjRequestTypeDef(
    _RequiredObjectDownloadFileobjRequestTypeDef, _OptionalObjectDownloadFileobjRequestTypeDef
):
    pass

RestoreStatusTypeDef = TypedDict(
    "RestoreStatusTypeDef",
    {
        "IsRestoreInProgress": bool,
        "RestoreExpiryDate": datetime,
    },
)

_RequiredObjectUploadFileRequestTypeDef = TypedDict(
    "_RequiredObjectUploadFileRequestTypeDef",
    {
        "Filename": str,
    },
)
_OptionalObjectUploadFileRequestTypeDef = TypedDict(
    "_OptionalObjectUploadFileRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ObjectUploadFileRequestTypeDef(
    _RequiredObjectUploadFileRequestTypeDef, _OptionalObjectUploadFileRequestTypeDef
):
    pass

_RequiredObjectUploadFileobjRequestTypeDef = TypedDict(
    "_RequiredObjectUploadFileobjRequestTypeDef",
    {
        "Fileobj": Union[IO[Any], StreamingBody],
    },
)
_OptionalObjectUploadFileobjRequestTypeDef = TypedDict(
    "_OptionalObjectUploadFileobjRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "Config": TransferConfig,
    },
    total=False,
)

class ObjectUploadFileobjRequestTypeDef(
    _RequiredObjectUploadFileobjRequestTypeDef, _OptionalObjectUploadFileobjRequestTypeDef
):
    pass

OwnerResponseMetadataTypeDef = TypedDict(
    "OwnerResponseMetadataTypeDef",
    {
        "DisplayName": str,
        "ID": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

OwnershipControlsRuleTypeDef = TypedDict(
    "OwnershipControlsRuleTypeDef",
    {
        "ObjectOwnership": ObjectOwnershipType,
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

ProgressTypeDef = TypedDict(
    "ProgressTypeDef",
    {
        "BytesScanned": int,
        "BytesProcessed": int,
        "BytesReturned": int,
    },
)

_RequiredPutBucketPolicyRequestBucketPolicyPutTypeDef = TypedDict(
    "_RequiredPutBucketPolicyRequestBucketPolicyPutTypeDef",
    {
        "Policy": str,
    },
)
_OptionalPutBucketPolicyRequestBucketPolicyPutTypeDef = TypedDict(
    "_OptionalPutBucketPolicyRequestBucketPolicyPutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ConfirmRemoveSelfBucketAccess": bool,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketPolicyRequestBucketPolicyPutTypeDef(
    _RequiredPutBucketPolicyRequestBucketPolicyPutTypeDef,
    _OptionalPutBucketPolicyRequestBucketPolicyPutTypeDef,
):
    pass

_RequiredPutBucketPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketPolicyRequestRequestTypeDef",
    {
        "Bucket": str,
        "Policy": str,
    },
)
_OptionalPutBucketPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketPolicyRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ConfirmRemoveSelfBucketAccess": bool,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketPolicyRequestRequestTypeDef(
    _RequiredPutBucketPolicyRequestRequestTypeDef, _OptionalPutBucketPolicyRequestRequestTypeDef
):
    pass

RequestPaymentConfigurationTypeDef = TypedDict(
    "RequestPaymentConfigurationTypeDef",
    {
        "Payer": PayerType,
    },
)

PutBucketVersioningRequestBucketVersioningEnableTypeDef = TypedDict(
    "PutBucketVersioningRequestBucketVersioningEnableTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "MFA": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

VersioningConfigurationTypeDef = TypedDict(
    "VersioningConfigurationTypeDef",
    {
        "MFADelete": MFADeleteType,
        "Status": BucketVersioningStatusType,
    },
    total=False,
)

PutBucketVersioningRequestBucketVersioningSuspendTypeDef = TypedDict(
    "PutBucketVersioningRequestBucketVersioningSuspendTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "MFA": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

PutObjectAclOutputTypeDef = TypedDict(
    "PutObjectAclOutputTypeDef",
    {
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutObjectLegalHoldOutputTypeDef = TypedDict(
    "PutObjectLegalHoldOutputTypeDef",
    {
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutObjectLockConfigurationOutputTypeDef = TypedDict(
    "PutObjectLockConfigurationOutputTypeDef",
    {
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutObjectOutputTypeDef = TypedDict(
    "PutObjectOutputTypeDef",
    {
        "Expiration": str,
        "ETag": str,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "ServerSideEncryption": ServerSideEncryptionType,
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutObjectRequestBucketPutObjectTypeDef = TypedDict(
    "_RequiredPutObjectRequestBucketPutObjectTypeDef",
    {
        "Key": str,
    },
)
_OptionalPutObjectRequestBucketPutObjectTypeDef = TypedDict(
    "_OptionalPutObjectRequestBucketPutObjectTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentLength": int,
        "ContentMD5": str,
        "ContentType": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutObjectRequestBucketPutObjectTypeDef(
    _RequiredPutObjectRequestBucketPutObjectTypeDef, _OptionalPutObjectRequestBucketPutObjectTypeDef
):
    pass

PutObjectRequestObjectPutTypeDef = TypedDict(
    "PutObjectRequestObjectPutTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentLength": int,
        "ContentMD5": str,
        "ContentType": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

PutObjectRequestObjectSummaryPutTypeDef = TypedDict(
    "PutObjectRequestObjectSummaryPutTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentLength": int,
        "ContentMD5": str,
        "ContentType": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredPutObjectRequestRequestTypeDef = TypedDict(
    "_RequiredPutObjectRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalPutObjectRequestRequestTypeDef = TypedDict(
    "_OptionalPutObjectRequestRequestTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentLength": int,
        "ContentMD5": str,
        "ContentType": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutObjectRequestRequestTypeDef(
    _RequiredPutObjectRequestRequestTypeDef, _OptionalPutObjectRequestRequestTypeDef
):
    pass

PutObjectRetentionOutputTypeDef = TypedDict(
    "PutObjectRetentionOutputTypeDef",
    {
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutObjectTaggingOutputTypeDef = TypedDict(
    "PutObjectTaggingOutputTypeDef",
    {
        "VersionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecordsEventTypeDef = TypedDict(
    "RecordsEventTypeDef",
    {
        "Payload": bytes,
    },
)

RedirectAllRequestsToResponseMetadataTypeDef = TypedDict(
    "RedirectAllRequestsToResponseMetadataTypeDef",
    {
        "HostName": str,
        "Protocol": ProtocolType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RedirectTypeDef = TypedDict(
    "RedirectTypeDef",
    {
        "HostName": str,
        "HttpRedirectCode": str,
        "Protocol": ProtocolType,
        "ReplaceKeyPrefixWith": str,
        "ReplaceKeyWith": str,
    },
)

ReplicaModificationsTypeDef = TypedDict(
    "ReplicaModificationsTypeDef",
    {
        "Status": ReplicaModificationsStatusType,
    },
)

RequestProgressTypeDef = TypedDict(
    "RequestProgressTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
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

RestoreObjectOutputTypeDef = TypedDict(
    "RestoreObjectOutputTypeDef",
    {
        "RequestCharged": Literal["requester"],
        "RestoreOutputPath": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RestoreStatusResponseMetadataTypeDef = TypedDict(
    "RestoreStatusResponseMetadataTypeDef",
    {
        "IsRestoreInProgress": bool,
        "RestoreExpiryDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ScanRangeTypeDef = TypedDict(
    "ScanRangeTypeDef",
    {
        "Start": int,
        "End": int,
    },
    total=False,
)

ServerSideEncryptionByDefaultTypeDef = TypedDict(
    "ServerSideEncryptionByDefaultTypeDef",
    {
        "SSEAlgorithm": ServerSideEncryptionType,
        "KMSMasterKeyID": str,
    },
)

SseKmsEncryptedObjectsTypeDef = TypedDict(
    "SseKmsEncryptedObjectsTypeDef",
    {
        "Status": SseKmsEncryptedObjectsStatusType,
    },
)

StatsTypeDef = TypedDict(
    "StatsTypeDef",
    {
        "BytesScanned": int,
        "BytesProcessed": int,
        "BytesReturned": int,
    },
)

UploadPartOutputTypeDef = TypedDict(
    "UploadPartOutputTypeDef",
    {
        "ServerSideEncryption": ServerSideEncryptionType,
        "ETag": str,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "BucketKeyEnabled": bool,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UploadPartRequestMultipartUploadPartUploadTypeDef = TypedDict(
    "UploadPartRequestMultipartUploadPartUploadTypeDef",
    {
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "ContentLength": int,
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredUploadPartRequestRequestTypeDef = TypedDict(
    "_RequiredUploadPartRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "PartNumber": int,
        "UploadId": str,
    },
)
_OptionalUploadPartRequestRequestTypeDef = TypedDict(
    "_OptionalUploadPartRequestRequestTypeDef",
    {
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "ContentLength": int,
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class UploadPartRequestRequestTypeDef(
    _RequiredUploadPartRequestRequestTypeDef, _OptionalUploadPartRequestRequestTypeDef
):
    pass

_RequiredWriteGetObjectResponseRequestRequestTypeDef = TypedDict(
    "_RequiredWriteGetObjectResponseRequestRequestTypeDef",
    {
        "RequestRoute": str,
        "RequestToken": str,
    },
)
_OptionalWriteGetObjectResponseRequestRequestTypeDef = TypedDict(
    "_OptionalWriteGetObjectResponseRequestRequestTypeDef",
    {
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "StatusCode": int,
        "ErrorCode": str,
        "ErrorMessage": str,
        "AcceptRanges": str,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentLength": int,
        "ContentRange": str,
        "ContentType": str,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "DeleteMarker": bool,
        "ETag": str,
        "Expires": Union[datetime, str],
        "Expiration": str,
        "LastModified": Union[datetime, str],
        "MissingMeta": int,
        "Metadata": Mapping[str, str],
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "PartsCount": int,
        "ReplicationStatus": ReplicationStatusType,
        "RequestCharged": Literal["requester"],
        "Restore": str,
        "ServerSideEncryption": ServerSideEncryptionType,
        "SSECustomerAlgorithm": str,
        "SSEKMSKeyId": str,
        "SSECustomerKeyMD5": str,
        "StorageClass": StorageClassType,
        "TagCount": int,
        "VersionId": str,
        "BucketKeyEnabled": bool,
    },
    total=False,
)

class WriteGetObjectResponseRequestRequestTypeDef(
    _RequiredWriteGetObjectResponseRequestRequestTypeDef,
    _OptionalWriteGetObjectResponseRequestRequestTypeDef,
):
    pass

_RequiredPutBucketAccelerateConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketAccelerateConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "AccelerateConfiguration": AccelerateConfigurationTypeDef,
    },
)
_OptionalPutBucketAccelerateConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketAccelerateConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
    },
    total=False,
)

class PutBucketAccelerateConfigurationRequestRequestTypeDef(
    _RequiredPutBucketAccelerateConfigurationRequestRequestTypeDef,
    _OptionalPutBucketAccelerateConfigurationRequestRequestTypeDef,
):
    pass

DeleteMarkerEntryTypeDef = TypedDict(
    "DeleteMarkerEntryTypeDef",
    {
        "Owner": OwnerTypeDef,
        "Key": str,
        "VersionId": str,
        "IsLatest": bool,
        "LastModified": datetime,
    },
)

AnalyticsAndOperatorTypeDef = TypedDict(
    "AnalyticsAndOperatorTypeDef",
    {
        "Prefix": str,
        "Tags": List[TagTypeDef],
    },
)

GetBucketTaggingOutputTypeDef = TypedDict(
    "GetBucketTaggingOutputTypeDef",
    {
        "TagSet": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetObjectTaggingOutputTypeDef = TypedDict(
    "GetObjectTaggingOutputTypeDef",
    {
        "VersionId": str,
        "TagSet": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

IntelligentTieringAndOperatorTypeDef = TypedDict(
    "IntelligentTieringAndOperatorTypeDef",
    {
        "Prefix": str,
        "Tags": List[TagTypeDef],
    },
)

LifecycleRuleAndOperatorTypeDef = TypedDict(
    "LifecycleRuleAndOperatorTypeDef",
    {
        "Prefix": str,
        "Tags": List[TagTypeDef],
        "ObjectSizeGreaterThan": int,
        "ObjectSizeLessThan": int,
    },
)

MetricsAndOperatorTypeDef = TypedDict(
    "MetricsAndOperatorTypeDef",
    {
        "Prefix": str,
        "Tags": List[TagTypeDef],
        "AccessPointArn": str,
    },
)

ReplicationRuleAndOperatorTypeDef = TypedDict(
    "ReplicationRuleAndOperatorTypeDef",
    {
        "Prefix": str,
        "Tags": List[TagTypeDef],
    },
)

TaggingTypeDef = TypedDict(
    "TaggingTypeDef",
    {
        "TagSet": Sequence[TagTypeDef],
    },
)

AnalyticsExportDestinationTypeDef = TypedDict(
    "AnalyticsExportDestinationTypeDef",
    {
        "S3BucketDestination": AnalyticsS3BucketDestinationTypeDef,
    },
)

_RequiredBucketCopyRequestTypeDef = TypedDict(
    "_RequiredBucketCopyRequestTypeDef",
    {
        "CopySource": CopySourceTypeDef,
        "Key": str,
    },
)
_OptionalBucketCopyRequestTypeDef = TypedDict(
    "_OptionalBucketCopyRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "SourceClient": BaseClient,
        "Config": TransferConfig,
    },
    total=False,
)

class BucketCopyRequestTypeDef(
    _RequiredBucketCopyRequestTypeDef, _OptionalBucketCopyRequestTypeDef
):
    pass

_RequiredClientCopyRequestTypeDef = TypedDict(
    "_RequiredClientCopyRequestTypeDef",
    {
        "CopySource": CopySourceTypeDef,
        "Bucket": str,
        "Key": str,
    },
)
_OptionalClientCopyRequestTypeDef = TypedDict(
    "_OptionalClientCopyRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "SourceClient": BaseClient,
        "Config": TransferConfig,
    },
    total=False,
)

class ClientCopyRequestTypeDef(
    _RequiredClientCopyRequestTypeDef, _OptionalClientCopyRequestTypeDef
):
    pass

_RequiredCopyObjectRequestRequestTypeDef = TypedDict(
    "_RequiredCopyObjectRequestRequestTypeDef",
    {
        "Bucket": str,
        "CopySource": Union[str, CopySourceTypeDef],
        "Key": str,
    },
)
_OptionalCopyObjectRequestRequestTypeDef = TypedDict(
    "_OptionalCopyObjectRequestRequestTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "CacheControl": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "CopySourceIfMatch": str,
        "CopySourceIfModifiedSince": Union[datetime, str],
        "CopySourceIfNoneMatch": str,
        "CopySourceIfUnmodifiedSince": Union[datetime, str],
        "Expires": Union[datetime, str],
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWriteACP": str,
        "Metadata": Mapping[str, str],
        "MetadataDirective": MetadataDirectiveType,
        "TaggingDirective": TaggingDirectiveType,
        "ServerSideEncryption": ServerSideEncryptionType,
        "StorageClass": StorageClassType,
        "WebsiteRedirectLocation": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "CopySourceSSECustomerAlgorithm": str,
        "CopySourceSSECustomerKey": str,
        "CopySourceSSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "Tagging": str,
        "ObjectLockMode": ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "ObjectLockLegalHoldStatus": ObjectLockLegalHoldStatusType,
        "ExpectedBucketOwner": str,
        "ExpectedSourceBucketOwner": str,
    },
    total=False,
)

class CopyObjectRequestRequestTypeDef(
    _RequiredCopyObjectRequestRequestTypeDef, _OptionalCopyObjectRequestRequestTypeDef
):
    pass

_RequiredObjectCopyRequestTypeDef = TypedDict(
    "_RequiredObjectCopyRequestTypeDef",
    {
        "CopySource": CopySourceTypeDef,
    },
)
_OptionalObjectCopyRequestTypeDef = TypedDict(
    "_OptionalObjectCopyRequestTypeDef",
    {
        "ExtraArgs": Dict[str, Any],
        "Callback": Callable[..., Any],
        "SourceClient": BaseClient,
        "Config": TransferConfig,
    },
    total=False,
)

class ObjectCopyRequestTypeDef(
    _RequiredObjectCopyRequestTypeDef, _OptionalObjectCopyRequestTypeDef
):
    pass

_RequiredUploadPartCopyRequestMultipartUploadPartCopyFromTypeDef = TypedDict(
    "_RequiredUploadPartCopyRequestMultipartUploadPartCopyFromTypeDef",
    {
        "CopySource": Union[str, CopySourceTypeDef],
    },
)
_OptionalUploadPartCopyRequestMultipartUploadPartCopyFromTypeDef = TypedDict(
    "_OptionalUploadPartCopyRequestMultipartUploadPartCopyFromTypeDef",
    {
        "CopySourceIfMatch": str,
        "CopySourceIfModifiedSince": Union[datetime, str],
        "CopySourceIfNoneMatch": str,
        "CopySourceIfUnmodifiedSince": Union[datetime, str],
        "CopySourceRange": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "CopySourceSSECustomerAlgorithm": str,
        "CopySourceSSECustomerKey": str,
        "CopySourceSSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "ExpectedSourceBucketOwner": str,
    },
    total=False,
)

class UploadPartCopyRequestMultipartUploadPartCopyFromTypeDef(
    _RequiredUploadPartCopyRequestMultipartUploadPartCopyFromTypeDef,
    _OptionalUploadPartCopyRequestMultipartUploadPartCopyFromTypeDef,
):
    pass

_RequiredUploadPartCopyRequestRequestTypeDef = TypedDict(
    "_RequiredUploadPartCopyRequestRequestTypeDef",
    {
        "Bucket": str,
        "CopySource": Union[str, CopySourceTypeDef],
        "Key": str,
        "PartNumber": int,
        "UploadId": str,
    },
)
_OptionalUploadPartCopyRequestRequestTypeDef = TypedDict(
    "_OptionalUploadPartCopyRequestRequestTypeDef",
    {
        "CopySourceIfMatch": str,
        "CopySourceIfModifiedSince": Union[datetime, str],
        "CopySourceIfNoneMatch": str,
        "CopySourceIfUnmodifiedSince": Union[datetime, str],
        "CopySourceRange": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "CopySourceSSECustomerAlgorithm": str,
        "CopySourceSSECustomerKey": str,
        "CopySourceSSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "ExpectedSourceBucketOwner": str,
    },
    total=False,
)

class UploadPartCopyRequestRequestTypeDef(
    _RequiredUploadPartCopyRequestRequestTypeDef, _OptionalUploadPartCopyRequestRequestTypeDef
):
    pass

ListBucketsOutputTypeDef = TypedDict(
    "ListBucketsOutputTypeDef",
    {
        "Buckets": List[BucketTypeDef],
        "Owner": OwnerTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CORSConfigurationTypeDef = TypedDict(
    "CORSConfigurationTypeDef",
    {
        "CORSRules": Sequence[CORSRuleTypeDef],
    },
)

GetBucketCorsOutputTypeDef = TypedDict(
    "GetBucketCorsOutputTypeDef",
    {
        "CORSRules": List[CORSRuleTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CompletedMultipartUploadTypeDef = TypedDict(
    "CompletedMultipartUploadTypeDef",
    {
        "Parts": Sequence[CompletedPartTypeDef],
    },
    total=False,
)

CopyObjectOutputTypeDef = TypedDict(
    "CopyObjectOutputTypeDef",
    {
        "CopyObjectResult": CopyObjectResultTypeDef,
        "Expiration": str,
        "CopySourceVersionId": str,
        "VersionId": str,
        "ServerSideEncryption": ServerSideEncryptionType,
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "BucketKeyEnabled": bool,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UploadPartCopyOutputTypeDef = TypedDict(
    "UploadPartCopyOutputTypeDef",
    {
        "CopySourceVersionId": str,
        "CopyPartResult": CopyPartResultTypeDef,
        "ServerSideEncryption": ServerSideEncryptionType,
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "BucketKeyEnabled": bool,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateBucketRequestBucketCreateTypeDef = TypedDict(
    "CreateBucketRequestBucketCreateTypeDef",
    {
        "ACL": BucketCannedACLType,
        "CreateBucketConfiguration": CreateBucketConfigurationTypeDef,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "ObjectLockEnabledForBucket": bool,
        "ObjectOwnership": ObjectOwnershipType,
    },
    total=False,
)

_RequiredCreateBucketRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBucketRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalCreateBucketRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBucketRequestRequestTypeDef",
    {
        "ACL": BucketCannedACLType,
        "CreateBucketConfiguration": CreateBucketConfigurationTypeDef,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "ObjectLockEnabledForBucket": bool,
        "ObjectOwnership": ObjectOwnershipType,
    },
    total=False,
)

class CreateBucketRequestRequestTypeDef(
    _RequiredCreateBucketRequestRequestTypeDef, _OptionalCreateBucketRequestRequestTypeDef
):
    pass

_RequiredCreateBucketRequestServiceResourceCreateBucketTypeDef = TypedDict(
    "_RequiredCreateBucketRequestServiceResourceCreateBucketTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalCreateBucketRequestServiceResourceCreateBucketTypeDef = TypedDict(
    "_OptionalCreateBucketRequestServiceResourceCreateBucketTypeDef",
    {
        "ACL": BucketCannedACLType,
        "CreateBucketConfiguration": CreateBucketConfigurationTypeDef,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "ObjectLockEnabledForBucket": bool,
        "ObjectOwnership": ObjectOwnershipType,
    },
    total=False,
)

class CreateBucketRequestServiceResourceCreateBucketTypeDef(
    _RequiredCreateBucketRequestServiceResourceCreateBucketTypeDef,
    _OptionalCreateBucketRequestServiceResourceCreateBucketTypeDef,
):
    pass

ObjectLockRuleTypeDef = TypedDict(
    "ObjectLockRuleTypeDef",
    {
        "DefaultRetention": DefaultRetentionTypeDef,
    },
)

DeleteObjectsOutputTypeDef = TypedDict(
    "DeleteObjectsOutputTypeDef",
    {
        "Deleted": List[DeletedObjectTypeDef],
        "RequestCharged": Literal["requester"],
        "Errors": List[ErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteTypeDef = TypedDict(
    "_RequiredDeleteTypeDef",
    {
        "Objects": Sequence[ObjectIdentifierTypeDef],
    },
)
_OptionalDeleteTypeDef = TypedDict(
    "_OptionalDeleteTypeDef",
    {
        "Quiet": bool,
    },
    total=False,
)

class DeleteTypeDef(_RequiredDeleteTypeDef, _OptionalDeleteTypeDef):
    pass

S3KeyFilterTypeDef = TypedDict(
    "S3KeyFilterTypeDef",
    {
        "FilterRules": List[FilterRuleTypeDef],
    },
)

GetBucketPolicyStatusOutputTypeDef = TypedDict(
    "GetBucketPolicyStatusOutputTypeDef",
    {
        "PolicyStatus": PolicyStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetObjectAttributesPartsTypeDef = TypedDict(
    "GetObjectAttributesPartsTypeDef",
    {
        "TotalPartsCount": int,
        "PartNumberMarker": int,
        "NextPartNumberMarker": int,
        "MaxParts": int,
        "IsTruncated": bool,
        "Parts": List[ObjectPartTypeDef],
    },
)

GetObjectLegalHoldOutputTypeDef = TypedDict(
    "GetObjectLegalHoldOutputTypeDef",
    {
        "LegalHold": ObjectLockLegalHoldTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutObjectLegalHoldRequestRequestTypeDef = TypedDict(
    "_RequiredPutObjectLegalHoldRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalPutObjectLegalHoldRequestRequestTypeDef = TypedDict(
    "_OptionalPutObjectLegalHoldRequestRequestTypeDef",
    {
        "LegalHold": ObjectLockLegalHoldTypeDef,
        "RequestPayer": Literal["requester"],
        "VersionId": str,
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutObjectLegalHoldRequestRequestTypeDef(
    _RequiredPutObjectLegalHoldRequestRequestTypeDef,
    _OptionalPutObjectLegalHoldRequestRequestTypeDef,
):
    pass

GetObjectRetentionOutputTypeDef = TypedDict(
    "GetObjectRetentionOutputTypeDef",
    {
        "Retention": ObjectLockRetentionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutObjectRetentionRequestRequestTypeDef = TypedDict(
    "_RequiredPutObjectRetentionRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalPutObjectRetentionRequestRequestTypeDef = TypedDict(
    "_OptionalPutObjectRetentionRequestRequestTypeDef",
    {
        "Retention": ObjectLockRetentionTypeDef,
        "RequestPayer": Literal["requester"],
        "VersionId": str,
        "BypassGovernanceRetention": bool,
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutObjectRetentionRequestRequestTypeDef(
    _RequiredPutObjectRetentionRequestRequestTypeDef,
    _OptionalPutObjectRetentionRequestRequestTypeDef,
):
    pass

GetPublicAccessBlockOutputTypeDef = TypedDict(
    "GetPublicAccessBlockOutputTypeDef",
    {
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "_RequiredPutPublicAccessBlockRequestRequestTypeDef",
    {
        "Bucket": str,
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
    },
)
_OptionalPutPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "_OptionalPutPublicAccessBlockRequestRequestTypeDef",
    {
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutPublicAccessBlockRequestRequestTypeDef(
    _RequiredPutPublicAccessBlockRequestRequestTypeDef,
    _OptionalPutPublicAccessBlockRequestRequestTypeDef,
):
    pass

GrantTypeDef = TypedDict(
    "GrantTypeDef",
    {
        "Grantee": GranteeTypeDef,
        "Permission": PermissionType,
    },
)

TargetGrantTypeDef = TypedDict(
    "TargetGrantTypeDef",
    {
        "Grantee": GranteeTypeDef,
        "Permission": BucketLogsPermissionType,
    },
)

_RequiredHeadBucketRequestBucketExistsWaitTypeDef = TypedDict(
    "_RequiredHeadBucketRequestBucketExistsWaitTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalHeadBucketRequestBucketExistsWaitTypeDef = TypedDict(
    "_OptionalHeadBucketRequestBucketExistsWaitTypeDef",
    {
        "ExpectedBucketOwner": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class HeadBucketRequestBucketExistsWaitTypeDef(
    _RequiredHeadBucketRequestBucketExistsWaitTypeDef,
    _OptionalHeadBucketRequestBucketExistsWaitTypeDef,
):
    pass

_RequiredHeadBucketRequestBucketNotExistsWaitTypeDef = TypedDict(
    "_RequiredHeadBucketRequestBucketNotExistsWaitTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalHeadBucketRequestBucketNotExistsWaitTypeDef = TypedDict(
    "_OptionalHeadBucketRequestBucketNotExistsWaitTypeDef",
    {
        "ExpectedBucketOwner": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class HeadBucketRequestBucketNotExistsWaitTypeDef(
    _RequiredHeadBucketRequestBucketNotExistsWaitTypeDef,
    _OptionalHeadBucketRequestBucketNotExistsWaitTypeDef,
):
    pass

_RequiredHeadObjectRequestObjectExistsWaitTypeDef = TypedDict(
    "_RequiredHeadObjectRequestObjectExistsWaitTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalHeadObjectRequestObjectExistsWaitTypeDef = TypedDict(
    "_OptionalHeadObjectRequestObjectExistsWaitTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class HeadObjectRequestObjectExistsWaitTypeDef(
    _RequiredHeadObjectRequestObjectExistsWaitTypeDef,
    _OptionalHeadObjectRequestObjectExistsWaitTypeDef,
):
    pass

_RequiredHeadObjectRequestObjectNotExistsWaitTypeDef = TypedDict(
    "_RequiredHeadObjectRequestObjectNotExistsWaitTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalHeadObjectRequestObjectNotExistsWaitTypeDef = TypedDict(
    "_OptionalHeadObjectRequestObjectNotExistsWaitTypeDef",
    {
        "IfMatch": str,
        "IfModifiedSince": Union[datetime, str],
        "IfNoneMatch": str,
        "IfUnmodifiedSince": Union[datetime, str],
        "Range": str,
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestPayer": Literal["requester"],
        "PartNumber": int,
        "ExpectedBucketOwner": str,
        "ChecksumMode": Literal["ENABLED"],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class HeadObjectRequestObjectNotExistsWaitTypeDef(
    _RequiredHeadObjectRequestObjectNotExistsWaitTypeDef,
    _OptionalHeadObjectRequestObjectNotExistsWaitTypeDef,
):
    pass

MultipartUploadTypeDef = TypedDict(
    "MultipartUploadTypeDef",
    {
        "UploadId": str,
        "Key": str,
        "Initiated": datetime,
        "StorageClass": StorageClassType,
        "Owner": OwnerTypeDef,
        "Initiator": InitiatorTypeDef,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
    },
)

InputSerializationTypeDef = TypedDict(
    "InputSerializationTypeDef",
    {
        "CSV": CSVInputTypeDef,
        "CompressionType": CompressionTypeType,
        "JSON": JSONInputTypeDef,
        "Parquet": Mapping[str, Any],
    },
    total=False,
)

InventoryEncryptionTypeDef = TypedDict(
    "InventoryEncryptionTypeDef",
    {
        "SSES3": Dict[str, Any],
        "SSEKMS": SSEKMSTypeDef,
    },
)

OutputSerializationTypeDef = TypedDict(
    "OutputSerializationTypeDef",
    {
        "CSV": CSVOutputTypeDef,
        "JSON": JSONOutputTypeDef,
    },
    total=False,
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "Expiration": LifecycleExpirationTypeDef,
        "ID": str,
        "Prefix": str,
        "Status": ExpirationStatusType,
        "Transition": TransitionTypeDef,
        "NoncurrentVersionTransition": NoncurrentVersionTransitionTypeDef,
        "NoncurrentVersionExpiration": NoncurrentVersionExpirationTypeDef,
        "AbortIncompleteMultipartUpload": AbortIncompleteMultipartUploadTypeDef,
    },
)

ListPartsOutputTypeDef = TypedDict(
    "ListPartsOutputTypeDef",
    {
        "AbortDate": datetime,
        "AbortRuleId": str,
        "Bucket": str,
        "Key": str,
        "UploadId": str,
        "PartNumberMarker": int,
        "NextPartNumberMarker": int,
        "MaxParts": int,
        "IsTruncated": bool,
        "Parts": List[PartTypeDef],
        "Initiator": InitiatorTypeDef,
        "Owner": OwnerTypeDef,
        "StorageClass": StorageClassType,
        "RequestCharged": Literal["requester"],
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MetricsTypeDef = TypedDict(
    "MetricsTypeDef",
    {
        "Status": MetricsStatusType,
        "EventThreshold": ReplicationTimeValueTypeDef,
    },
)

ReplicationTimeTypeDef = TypedDict(
    "ReplicationTimeTypeDef",
    {
        "Status": ReplicationTimeStatusType,
        "Time": ReplicationTimeValueTypeDef,
    },
)

NotificationConfigurationDeprecatedResponseMetadataTypeDef = TypedDict(
    "NotificationConfigurationDeprecatedResponseMetadataTypeDef",
    {
        "TopicConfiguration": TopicConfigurationDeprecatedTypeDef,
        "QueueConfiguration": QueueConfigurationDeprecatedTypeDef,
        "CloudFunctionConfiguration": CloudFunctionConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NotificationConfigurationDeprecatedTypeDef = TypedDict(
    "NotificationConfigurationDeprecatedTypeDef",
    {
        "TopicConfiguration": TopicConfigurationDeprecatedTypeDef,
        "QueueConfiguration": QueueConfigurationDeprecatedTypeDef,
        "CloudFunctionConfiguration": CloudFunctionConfigurationTypeDef,
    },
    total=False,
)

ObjectTypeDef = TypedDict(
    "ObjectTypeDef",
    {
        "Key": str,
        "LastModified": datetime,
        "ETag": str,
        "ChecksumAlgorithm": List[ChecksumAlgorithmType],
        "Size": int,
        "StorageClass": ObjectStorageClassType,
        "Owner": OwnerTypeDef,
        "RestoreStatus": RestoreStatusTypeDef,
    },
)

ObjectVersionTypeDef = TypedDict(
    "ObjectVersionTypeDef",
    {
        "ETag": str,
        "ChecksumAlgorithm": List[ChecksumAlgorithmType],
        "Size": int,
        "StorageClass": Literal["STANDARD"],
        "Key": str,
        "VersionId": str,
        "IsLatest": bool,
        "LastModified": datetime,
        "Owner": OwnerTypeDef,
        "RestoreStatus": RestoreStatusTypeDef,
    },
)

OwnershipControlsTypeDef = TypedDict(
    "OwnershipControlsTypeDef",
    {
        "Rules": List[OwnershipControlsRuleTypeDef],
    },
)

ProgressEventTypeDef = TypedDict(
    "ProgressEventTypeDef",
    {
        "Details": ProgressTypeDef,
    },
)

_RequiredPutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef = TypedDict(
    "_RequiredPutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef",
    {
        "RequestPaymentConfiguration": RequestPaymentConfigurationTypeDef,
    },
)
_OptionalPutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef = TypedDict(
    "_OptionalPutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef(
    _RequiredPutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef,
    _OptionalPutBucketRequestPaymentRequestBucketRequestPaymentPutTypeDef,
):
    pass

_RequiredPutBucketRequestPaymentRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketRequestPaymentRequestRequestTypeDef",
    {
        "Bucket": str,
        "RequestPaymentConfiguration": RequestPaymentConfigurationTypeDef,
    },
)
_OptionalPutBucketRequestPaymentRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketRequestPaymentRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketRequestPaymentRequestRequestTypeDef(
    _RequiredPutBucketRequestPaymentRequestRequestTypeDef,
    _OptionalPutBucketRequestPaymentRequestRequestTypeDef,
):
    pass

_RequiredPutBucketVersioningRequestBucketVersioningPutTypeDef = TypedDict(
    "_RequiredPutBucketVersioningRequestBucketVersioningPutTypeDef",
    {
        "VersioningConfiguration": VersioningConfigurationTypeDef,
    },
)
_OptionalPutBucketVersioningRequestBucketVersioningPutTypeDef = TypedDict(
    "_OptionalPutBucketVersioningRequestBucketVersioningPutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "MFA": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketVersioningRequestBucketVersioningPutTypeDef(
    _RequiredPutBucketVersioningRequestBucketVersioningPutTypeDef,
    _OptionalPutBucketVersioningRequestBucketVersioningPutTypeDef,
):
    pass

_RequiredPutBucketVersioningRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketVersioningRequestRequestTypeDef",
    {
        "Bucket": str,
        "VersioningConfiguration": VersioningConfigurationTypeDef,
    },
)
_OptionalPutBucketVersioningRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketVersioningRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "MFA": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketVersioningRequestRequestTypeDef(
    _RequiredPutBucketVersioningRequestRequestTypeDef,
    _OptionalPutBucketVersioningRequestRequestTypeDef,
):
    pass

RoutingRuleTypeDef = TypedDict(
    "RoutingRuleTypeDef",
    {
        "Condition": ConditionTypeDef,
        "Redirect": RedirectTypeDef,
    },
)

ServerSideEncryptionRuleTypeDef = TypedDict(
    "ServerSideEncryptionRuleTypeDef",
    {
        "ApplyServerSideEncryptionByDefault": ServerSideEncryptionByDefaultTypeDef,
        "BucketKeyEnabled": bool,
    },
)

SourceSelectionCriteriaTypeDef = TypedDict(
    "SourceSelectionCriteriaTypeDef",
    {
        "SseKmsEncryptedObjects": SseKmsEncryptedObjectsTypeDef,
        "ReplicaModifications": ReplicaModificationsTypeDef,
    },
)

StatsEventTypeDef = TypedDict(
    "StatsEventTypeDef",
    {
        "Details": StatsTypeDef,
    },
)

AnalyticsFilterTypeDef = TypedDict(
    "AnalyticsFilterTypeDef",
    {
        "Prefix": str,
        "Tag": TagTypeDef,
        "And": AnalyticsAndOperatorTypeDef,
    },
)

IntelligentTieringFilterTypeDef = TypedDict(
    "IntelligentTieringFilterTypeDef",
    {
        "Prefix": str,
        "Tag": TagTypeDef,
        "And": IntelligentTieringAndOperatorTypeDef,
    },
)

LifecycleRuleFilterTypeDef = TypedDict(
    "LifecycleRuleFilterTypeDef",
    {
        "Prefix": str,
        "Tag": TagTypeDef,
        "ObjectSizeGreaterThan": int,
        "ObjectSizeLessThan": int,
        "And": LifecycleRuleAndOperatorTypeDef,
    },
)

MetricsFilterTypeDef = TypedDict(
    "MetricsFilterTypeDef",
    {
        "Prefix": str,
        "Tag": TagTypeDef,
        "AccessPointArn": str,
        "And": MetricsAndOperatorTypeDef,
    },
)

ReplicationRuleFilterTypeDef = TypedDict(
    "ReplicationRuleFilterTypeDef",
    {
        "Prefix": str,
        "Tag": TagTypeDef,
        "And": ReplicationRuleAndOperatorTypeDef,
    },
)

_RequiredPutBucketTaggingRequestBucketTaggingPutTypeDef = TypedDict(
    "_RequiredPutBucketTaggingRequestBucketTaggingPutTypeDef",
    {
        "Tagging": TaggingTypeDef,
    },
)
_OptionalPutBucketTaggingRequestBucketTaggingPutTypeDef = TypedDict(
    "_OptionalPutBucketTaggingRequestBucketTaggingPutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketTaggingRequestBucketTaggingPutTypeDef(
    _RequiredPutBucketTaggingRequestBucketTaggingPutTypeDef,
    _OptionalPutBucketTaggingRequestBucketTaggingPutTypeDef,
):
    pass

_RequiredPutBucketTaggingRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketTaggingRequestRequestTypeDef",
    {
        "Bucket": str,
        "Tagging": TaggingTypeDef,
    },
)
_OptionalPutBucketTaggingRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketTaggingRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketTaggingRequestRequestTypeDef(
    _RequiredPutBucketTaggingRequestRequestTypeDef, _OptionalPutBucketTaggingRequestRequestTypeDef
):
    pass

_RequiredPutObjectTaggingRequestRequestTypeDef = TypedDict(
    "_RequiredPutObjectTaggingRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "Tagging": TaggingTypeDef,
    },
)
_OptionalPutObjectTaggingRequestRequestTypeDef = TypedDict(
    "_OptionalPutObjectTaggingRequestRequestTypeDef",
    {
        "VersionId": str,
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
        "RequestPayer": Literal["requester"],
    },
    total=False,
)

class PutObjectTaggingRequestRequestTypeDef(
    _RequiredPutObjectTaggingRequestRequestTypeDef, _OptionalPutObjectTaggingRequestRequestTypeDef
):
    pass

StorageClassAnalysisDataExportTypeDef = TypedDict(
    "StorageClassAnalysisDataExportTypeDef",
    {
        "OutputSchemaVersion": Literal["V_1"],
        "Destination": AnalyticsExportDestinationTypeDef,
    },
)

_RequiredPutBucketCorsRequestBucketCorsPutTypeDef = TypedDict(
    "_RequiredPutBucketCorsRequestBucketCorsPutTypeDef",
    {
        "CORSConfiguration": CORSConfigurationTypeDef,
    },
)
_OptionalPutBucketCorsRequestBucketCorsPutTypeDef = TypedDict(
    "_OptionalPutBucketCorsRequestBucketCorsPutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketCorsRequestBucketCorsPutTypeDef(
    _RequiredPutBucketCorsRequestBucketCorsPutTypeDef,
    _OptionalPutBucketCorsRequestBucketCorsPutTypeDef,
):
    pass

_RequiredPutBucketCorsRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketCorsRequestRequestTypeDef",
    {
        "Bucket": str,
        "CORSConfiguration": CORSConfigurationTypeDef,
    },
)
_OptionalPutBucketCorsRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketCorsRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketCorsRequestRequestTypeDef(
    _RequiredPutBucketCorsRequestRequestTypeDef, _OptionalPutBucketCorsRequestRequestTypeDef
):
    pass

CompleteMultipartUploadRequestMultipartUploadCompleteTypeDef = TypedDict(
    "CompleteMultipartUploadRequestMultipartUploadCompleteTypeDef",
    {
        "MultipartUpload": CompletedMultipartUploadTypeDef,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
    },
    total=False,
)

_RequiredCompleteMultipartUploadRequestRequestTypeDef = TypedDict(
    "_RequiredCompleteMultipartUploadRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "UploadId": str,
    },
)
_OptionalCompleteMultipartUploadRequestRequestTypeDef = TypedDict(
    "_OptionalCompleteMultipartUploadRequestRequestTypeDef",
    {
        "MultipartUpload": CompletedMultipartUploadTypeDef,
        "ChecksumCRC32": str,
        "ChecksumCRC32C": str,
        "ChecksumSHA1": str,
        "ChecksumSHA256": str,
        "RequestPayer": Literal["requester"],
        "ExpectedBucketOwner": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
    },
    total=False,
)

class CompleteMultipartUploadRequestRequestTypeDef(
    _RequiredCompleteMultipartUploadRequestRequestTypeDef,
    _OptionalCompleteMultipartUploadRequestRequestTypeDef,
):
    pass

ObjectLockConfigurationTypeDef = TypedDict(
    "ObjectLockConfigurationTypeDef",
    {
        "ObjectLockEnabled": Literal["Enabled"],
        "Rule": ObjectLockRuleTypeDef,
    },
)

_RequiredDeleteObjectsRequestBucketDeleteObjectsTypeDef = TypedDict(
    "_RequiredDeleteObjectsRequestBucketDeleteObjectsTypeDef",
    {
        "Delete": DeleteTypeDef,
    },
)
_OptionalDeleteObjectsRequestBucketDeleteObjectsTypeDef = TypedDict(
    "_OptionalDeleteObjectsRequestBucketDeleteObjectsTypeDef",
    {
        "MFA": str,
        "RequestPayer": Literal["requester"],
        "BypassGovernanceRetention": bool,
        "ExpectedBucketOwner": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
    },
    total=False,
)

class DeleteObjectsRequestBucketDeleteObjectsTypeDef(
    _RequiredDeleteObjectsRequestBucketDeleteObjectsTypeDef,
    _OptionalDeleteObjectsRequestBucketDeleteObjectsTypeDef,
):
    pass

_RequiredDeleteObjectsRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteObjectsRequestRequestTypeDef",
    {
        "Bucket": str,
        "Delete": DeleteTypeDef,
    },
)
_OptionalDeleteObjectsRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteObjectsRequestRequestTypeDef",
    {
        "MFA": str,
        "RequestPayer": Literal["requester"],
        "BypassGovernanceRetention": bool,
        "ExpectedBucketOwner": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
    },
    total=False,
)

class DeleteObjectsRequestRequestTypeDef(
    _RequiredDeleteObjectsRequestRequestTypeDef, _OptionalDeleteObjectsRequestRequestTypeDef
):
    pass

NotificationConfigurationFilterTypeDef = TypedDict(
    "NotificationConfigurationFilterTypeDef",
    {
        "Key": S3KeyFilterTypeDef,
    },
)

GetObjectAttributesOutputTypeDef = TypedDict(
    "GetObjectAttributesOutputTypeDef",
    {
        "DeleteMarker": bool,
        "LastModified": datetime,
        "VersionId": str,
        "RequestCharged": Literal["requester"],
        "ETag": str,
        "Checksum": ChecksumTypeDef,
        "ObjectParts": GetObjectAttributesPartsTypeDef,
        "StorageClass": StorageClassType,
        "ObjectSize": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AccessControlPolicyTypeDef = TypedDict(
    "AccessControlPolicyTypeDef",
    {
        "Grants": Sequence[GrantTypeDef],
        "Owner": OwnerTypeDef,
    },
    total=False,
)

GetBucketAclOutputTypeDef = TypedDict(
    "GetBucketAclOutputTypeDef",
    {
        "Owner": OwnerTypeDef,
        "Grants": List[GrantTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetObjectAclOutputTypeDef = TypedDict(
    "GetObjectAclOutputTypeDef",
    {
        "Owner": OwnerTypeDef,
        "Grants": List[GrantTypeDef],
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredS3LocationTypeDef = TypedDict(
    "_RequiredS3LocationTypeDef",
    {
        "BucketName": str,
        "Prefix": str,
    },
)
_OptionalS3LocationTypeDef = TypedDict(
    "_OptionalS3LocationTypeDef",
    {
        "Encryption": EncryptionTypeDef,
        "CannedACL": ObjectCannedACLType,
        "AccessControlList": Sequence[GrantTypeDef],
        "Tagging": TaggingTypeDef,
        "UserMetadata": Sequence[MetadataEntryTypeDef],
        "StorageClass": StorageClassType,
    },
    total=False,
)

class S3LocationTypeDef(_RequiredS3LocationTypeDef, _OptionalS3LocationTypeDef):
    pass

LoggingEnabledResponseMetadataTypeDef = TypedDict(
    "LoggingEnabledResponseMetadataTypeDef",
    {
        "TargetBucket": str,
        "TargetGrants": List[TargetGrantTypeDef],
        "TargetPrefix": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LoggingEnabledTypeDef = TypedDict(
    "LoggingEnabledTypeDef",
    {
        "TargetBucket": str,
        "TargetGrants": List[TargetGrantTypeDef],
        "TargetPrefix": str,
    },
)

ListMultipartUploadsOutputTypeDef = TypedDict(
    "ListMultipartUploadsOutputTypeDef",
    {
        "Bucket": str,
        "KeyMarker": str,
        "UploadIdMarker": str,
        "NextKeyMarker": str,
        "Prefix": str,
        "Delimiter": str,
        "NextUploadIdMarker": str,
        "MaxUploads": int,
        "IsTruncated": bool,
        "Uploads": List[MultipartUploadTypeDef],
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InventoryS3BucketDestinationTypeDef = TypedDict(
    "InventoryS3BucketDestinationTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "Format": InventoryFormatType,
        "Prefix": str,
        "Encryption": InventoryEncryptionTypeDef,
    },
)

_RequiredSelectObjectContentRequestRequestTypeDef = TypedDict(
    "_RequiredSelectObjectContentRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "Expression": str,
        "ExpressionType": Literal["SQL"],
        "InputSerialization": InputSerializationTypeDef,
        "OutputSerialization": OutputSerializationTypeDef,
    },
)
_OptionalSelectObjectContentRequestRequestTypeDef = TypedDict(
    "_OptionalSelectObjectContentRequestRequestTypeDef",
    {
        "SSECustomerAlgorithm": str,
        "SSECustomerKey": str,
        "SSECustomerKeyMD5": str,
        "RequestProgress": RequestProgressTypeDef,
        "ScanRange": ScanRangeTypeDef,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class SelectObjectContentRequestRequestTypeDef(
    _RequiredSelectObjectContentRequestRequestTypeDef,
    _OptionalSelectObjectContentRequestRequestTypeDef,
):
    pass

SelectParametersTypeDef = TypedDict(
    "SelectParametersTypeDef",
    {
        "InputSerialization": InputSerializationTypeDef,
        "ExpressionType": Literal["SQL"],
        "Expression": str,
        "OutputSerialization": OutputSerializationTypeDef,
    },
)

GetBucketLifecycleOutputTypeDef = TypedDict(
    "GetBucketLifecycleOutputTypeDef",
    {
        "Rules": List[RuleTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LifecycleConfigurationTypeDef = TypedDict(
    "LifecycleConfigurationTypeDef",
    {
        "Rules": Sequence[RuleTypeDef],
    },
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "Bucket": str,
        "Account": str,
        "StorageClass": StorageClassType,
        "AccessControlTranslation": AccessControlTranslationTypeDef,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "ReplicationTime": ReplicationTimeTypeDef,
        "Metrics": MetricsTypeDef,
    },
)

_RequiredPutBucketNotificationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketNotificationRequestRequestTypeDef",
    {
        "Bucket": str,
        "NotificationConfiguration": NotificationConfigurationDeprecatedTypeDef,
    },
)
_OptionalPutBucketNotificationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketNotificationRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketNotificationRequestRequestTypeDef(
    _RequiredPutBucketNotificationRequestRequestTypeDef,
    _OptionalPutBucketNotificationRequestRequestTypeDef,
):
    pass

ListObjectsOutputTypeDef = TypedDict(
    "ListObjectsOutputTypeDef",
    {
        "IsTruncated": bool,
        "Marker": str,
        "NextMarker": str,
        "Contents": List[ObjectTypeDef],
        "Name": str,
        "Prefix": str,
        "Delimiter": str,
        "MaxKeys": int,
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListObjectsV2OutputTypeDef = TypedDict(
    "ListObjectsV2OutputTypeDef",
    {
        "IsTruncated": bool,
        "Contents": List[ObjectTypeDef],
        "Name": str,
        "Prefix": str,
        "Delimiter": str,
        "MaxKeys": int,
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
        "KeyCount": int,
        "ContinuationToken": str,
        "NextContinuationToken": str,
        "StartAfter": str,
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListObjectVersionsOutputTypeDef = TypedDict(
    "ListObjectVersionsOutputTypeDef",
    {
        "IsTruncated": bool,
        "KeyMarker": str,
        "VersionIdMarker": str,
        "NextKeyMarker": str,
        "NextVersionIdMarker": str,
        "Versions": List[ObjectVersionTypeDef],
        "DeleteMarkers": List[DeleteMarkerEntryTypeDef],
        "Name": str,
        "Prefix": str,
        "Delimiter": str,
        "MaxKeys": int,
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
        "RequestCharged": Literal["requester"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetBucketOwnershipControlsOutputTypeDef = TypedDict(
    "GetBucketOwnershipControlsOutputTypeDef",
    {
        "OwnershipControls": OwnershipControlsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutBucketOwnershipControlsRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketOwnershipControlsRequestRequestTypeDef",
    {
        "Bucket": str,
        "OwnershipControls": OwnershipControlsTypeDef,
    },
)
_OptionalPutBucketOwnershipControlsRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketOwnershipControlsRequestRequestTypeDef",
    {
        "ContentMD5": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketOwnershipControlsRequestRequestTypeDef(
    _RequiredPutBucketOwnershipControlsRequestRequestTypeDef,
    _OptionalPutBucketOwnershipControlsRequestRequestTypeDef,
):
    pass

GetBucketWebsiteOutputTypeDef = TypedDict(
    "GetBucketWebsiteOutputTypeDef",
    {
        "RedirectAllRequestsTo": RedirectAllRequestsToTypeDef,
        "IndexDocument": IndexDocumentTypeDef,
        "ErrorDocument": ErrorDocumentTypeDef,
        "RoutingRules": List[RoutingRuleTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

WebsiteConfigurationTypeDef = TypedDict(
    "WebsiteConfigurationTypeDef",
    {
        "ErrorDocument": ErrorDocumentTypeDef,
        "IndexDocument": IndexDocumentTypeDef,
        "RedirectAllRequestsTo": RedirectAllRequestsToTypeDef,
        "RoutingRules": Sequence[RoutingRuleTypeDef],
    },
    total=False,
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "Rules": List[ServerSideEncryptionRuleTypeDef],
    },
)

SelectObjectContentEventStreamTypeDef = TypedDict(
    "SelectObjectContentEventStreamTypeDef",
    {
        "Records": RecordsEventTypeDef,
        "Stats": StatsEventTypeDef,
        "Progress": ProgressEventTypeDef,
        "Cont": Dict[str, Any],
        "End": Dict[str, Any],
    },
)

IntelligentTieringConfigurationTypeDef = TypedDict(
    "IntelligentTieringConfigurationTypeDef",
    {
        "Id": str,
        "Filter": IntelligentTieringFilterTypeDef,
        "Status": IntelligentTieringStatusType,
        "Tierings": List[TieringTypeDef],
    },
)

LifecycleRuleTypeDef = TypedDict(
    "LifecycleRuleTypeDef",
    {
        "Expiration": LifecycleExpirationTypeDef,
        "ID": str,
        "Prefix": str,
        "Filter": LifecycleRuleFilterTypeDef,
        "Status": ExpirationStatusType,
        "Transitions": List[TransitionTypeDef],
        "NoncurrentVersionTransitions": List[NoncurrentVersionTransitionTypeDef],
        "NoncurrentVersionExpiration": NoncurrentVersionExpirationTypeDef,
        "AbortIncompleteMultipartUpload": AbortIncompleteMultipartUploadTypeDef,
    },
)

MetricsConfigurationTypeDef = TypedDict(
    "MetricsConfigurationTypeDef",
    {
        "Id": str,
        "Filter": MetricsFilterTypeDef,
    },
)

StorageClassAnalysisTypeDef = TypedDict(
    "StorageClassAnalysisTypeDef",
    {
        "DataExport": StorageClassAnalysisDataExportTypeDef,
    },
)

GetObjectLockConfigurationOutputTypeDef = TypedDict(
    "GetObjectLockConfigurationOutputTypeDef",
    {
        "ObjectLockConfiguration": ObjectLockConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutObjectLockConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutObjectLockConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalPutObjectLockConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutObjectLockConfigurationRequestRequestTypeDef",
    {
        "ObjectLockConfiguration": ObjectLockConfigurationTypeDef,
        "RequestPayer": Literal["requester"],
        "Token": str,
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutObjectLockConfigurationRequestRequestTypeDef(
    _RequiredPutObjectLockConfigurationRequestRequestTypeDef,
    _OptionalPutObjectLockConfigurationRequestRequestTypeDef,
):
    pass

LambdaFunctionConfigurationTypeDef = TypedDict(
    "LambdaFunctionConfigurationTypeDef",
    {
        "Id": str,
        "LambdaFunctionArn": str,
        "Events": List[EventType],
        "Filter": NotificationConfigurationFilterTypeDef,
    },
)

QueueConfigurationTypeDef = TypedDict(
    "QueueConfigurationTypeDef",
    {
        "Id": str,
        "QueueArn": str,
        "Events": List[EventType],
        "Filter": NotificationConfigurationFilterTypeDef,
    },
)

TopicConfigurationTypeDef = TypedDict(
    "TopicConfigurationTypeDef",
    {
        "Id": str,
        "TopicArn": str,
        "Events": List[EventType],
        "Filter": NotificationConfigurationFilterTypeDef,
    },
)

PutBucketAclRequestBucketAclPutTypeDef = TypedDict(
    "PutBucketAclRequestBucketAclPutTypeDef",
    {
        "ACL": BucketCannedACLType,
        "AccessControlPolicy": AccessControlPolicyTypeDef,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredPutBucketAclRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketAclRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalPutBucketAclRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketAclRequestRequestTypeDef",
    {
        "ACL": BucketCannedACLType,
        "AccessControlPolicy": AccessControlPolicyTypeDef,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketAclRequestRequestTypeDef(
    _RequiredPutBucketAclRequestRequestTypeDef, _OptionalPutBucketAclRequestRequestTypeDef
):
    pass

PutObjectAclRequestObjectAclPutTypeDef = TypedDict(
    "PutObjectAclRequestObjectAclPutTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "AccessControlPolicy": AccessControlPolicyTypeDef,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "RequestPayer": Literal["requester"],
        "VersionId": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredPutObjectAclRequestRequestTypeDef = TypedDict(
    "_RequiredPutObjectAclRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalPutObjectAclRequestRequestTypeDef = TypedDict(
    "_OptionalPutObjectAclRequestRequestTypeDef",
    {
        "ACL": ObjectCannedACLType,
        "AccessControlPolicy": AccessControlPolicyTypeDef,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "RequestPayer": Literal["requester"],
        "VersionId": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutObjectAclRequestRequestTypeDef(
    _RequiredPutObjectAclRequestRequestTypeDef, _OptionalPutObjectAclRequestRequestTypeDef
):
    pass

OutputLocationTypeDef = TypedDict(
    "OutputLocationTypeDef",
    {
        "S3": S3LocationTypeDef,
    },
    total=False,
)

BucketLoggingStatusTypeDef = TypedDict(
    "BucketLoggingStatusTypeDef",
    {
        "LoggingEnabled": LoggingEnabledTypeDef,
    },
    total=False,
)

GetBucketLoggingOutputTypeDef = TypedDict(
    "GetBucketLoggingOutputTypeDef",
    {
        "LoggingEnabled": LoggingEnabledTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InventoryDestinationTypeDef = TypedDict(
    "InventoryDestinationTypeDef",
    {
        "S3BucketDestination": InventoryS3BucketDestinationTypeDef,
    },
)

PutBucketLifecycleRequestBucketLifecyclePutTypeDef = TypedDict(
    "PutBucketLifecycleRequestBucketLifecyclePutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "LifecycleConfiguration": LifecycleConfigurationTypeDef,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredPutBucketLifecycleRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketLifecycleRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalPutBucketLifecycleRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketLifecycleRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "LifecycleConfiguration": LifecycleConfigurationTypeDef,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketLifecycleRequestRequestTypeDef(
    _RequiredPutBucketLifecycleRequestRequestTypeDef,
    _OptionalPutBucketLifecycleRequestRequestTypeDef,
):
    pass

ReplicationRuleTypeDef = TypedDict(
    "ReplicationRuleTypeDef",
    {
        "ID": str,
        "Priority": int,
        "Prefix": str,
        "Filter": ReplicationRuleFilterTypeDef,
        "Status": ReplicationRuleStatusType,
        "SourceSelectionCriteria": SourceSelectionCriteriaTypeDef,
        "ExistingObjectReplication": ExistingObjectReplicationTypeDef,
        "Destination": DestinationTypeDef,
        "DeleteMarkerReplication": DeleteMarkerReplicationTypeDef,
    },
)

_RequiredPutBucketWebsiteRequestBucketWebsitePutTypeDef = TypedDict(
    "_RequiredPutBucketWebsiteRequestBucketWebsitePutTypeDef",
    {
        "WebsiteConfiguration": WebsiteConfigurationTypeDef,
    },
)
_OptionalPutBucketWebsiteRequestBucketWebsitePutTypeDef = TypedDict(
    "_OptionalPutBucketWebsiteRequestBucketWebsitePutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketWebsiteRequestBucketWebsitePutTypeDef(
    _RequiredPutBucketWebsiteRequestBucketWebsitePutTypeDef,
    _OptionalPutBucketWebsiteRequestBucketWebsitePutTypeDef,
):
    pass

_RequiredPutBucketWebsiteRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketWebsiteRequestRequestTypeDef",
    {
        "Bucket": str,
        "WebsiteConfiguration": WebsiteConfigurationTypeDef,
    },
)
_OptionalPutBucketWebsiteRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketWebsiteRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketWebsiteRequestRequestTypeDef(
    _RequiredPutBucketWebsiteRequestRequestTypeDef, _OptionalPutBucketWebsiteRequestRequestTypeDef
):
    pass

GetBucketEncryptionOutputTypeDef = TypedDict(
    "GetBucketEncryptionOutputTypeDef",
    {
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutBucketEncryptionRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketEncryptionRequestRequestTypeDef",
    {
        "Bucket": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
    },
)
_OptionalPutBucketEncryptionRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketEncryptionRequestRequestTypeDef",
    {
        "ContentMD5": str,
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketEncryptionRequestRequestTypeDef(
    _RequiredPutBucketEncryptionRequestRequestTypeDef,
    _OptionalPutBucketEncryptionRequestRequestTypeDef,
):
    pass

SelectObjectContentOutputTypeDef = TypedDict(
    "SelectObjectContentOutputTypeDef",
    {
        "Payload": "EventStream[SelectObjectContentEventStreamTypeDef]",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetBucketIntelligentTieringConfigurationOutputTypeDef = TypedDict(
    "GetBucketIntelligentTieringConfigurationOutputTypeDef",
    {
        "IntelligentTieringConfiguration": IntelligentTieringConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBucketIntelligentTieringConfigurationsOutputTypeDef = TypedDict(
    "ListBucketIntelligentTieringConfigurationsOutputTypeDef",
    {
        "IsTruncated": bool,
        "ContinuationToken": str,
        "NextContinuationToken": str,
        "IntelligentTieringConfigurationList": List[IntelligentTieringConfigurationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutBucketIntelligentTieringConfigurationRequestRequestTypeDef = TypedDict(
    "PutBucketIntelligentTieringConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
        "IntelligentTieringConfiguration": IntelligentTieringConfigurationTypeDef,
    },
)

BucketLifecycleConfigurationTypeDef = TypedDict(
    "BucketLifecycleConfigurationTypeDef",
    {
        "Rules": Sequence[LifecycleRuleTypeDef],
    },
)

GetBucketLifecycleConfigurationOutputTypeDef = TypedDict(
    "GetBucketLifecycleConfigurationOutputTypeDef",
    {
        "Rules": List[LifecycleRuleTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetBucketMetricsConfigurationOutputTypeDef = TypedDict(
    "GetBucketMetricsConfigurationOutputTypeDef",
    {
        "MetricsConfiguration": MetricsConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBucketMetricsConfigurationsOutputTypeDef = TypedDict(
    "ListBucketMetricsConfigurationsOutputTypeDef",
    {
        "IsTruncated": bool,
        "ContinuationToken": str,
        "NextContinuationToken": str,
        "MetricsConfigurationList": List[MetricsConfigurationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutBucketMetricsConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketMetricsConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
        "MetricsConfiguration": MetricsConfigurationTypeDef,
    },
)
_OptionalPutBucketMetricsConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketMetricsConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketMetricsConfigurationRequestRequestTypeDef(
    _RequiredPutBucketMetricsConfigurationRequestRequestTypeDef,
    _OptionalPutBucketMetricsConfigurationRequestRequestTypeDef,
):
    pass

AnalyticsConfigurationTypeDef = TypedDict(
    "AnalyticsConfigurationTypeDef",
    {
        "Id": str,
        "Filter": AnalyticsFilterTypeDef,
        "StorageClassAnalysis": StorageClassAnalysisTypeDef,
    },
)

NotificationConfigurationResponseMetadataTypeDef = TypedDict(
    "NotificationConfigurationResponseMetadataTypeDef",
    {
        "TopicConfigurations": List[TopicConfigurationTypeDef],
        "QueueConfigurations": List[QueueConfigurationTypeDef],
        "LambdaFunctionConfigurations": List[LambdaFunctionConfigurationTypeDef],
        "EventBridgeConfiguration": Dict[str, Any],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "TopicConfigurations": Sequence[TopicConfigurationTypeDef],
        "QueueConfigurations": Sequence[QueueConfigurationTypeDef],
        "LambdaFunctionConfigurations": Sequence[LambdaFunctionConfigurationTypeDef],
        "EventBridgeConfiguration": Mapping[str, Any],
    },
    total=False,
)

RestoreRequestTypeDef = TypedDict(
    "RestoreRequestTypeDef",
    {
        "Days": int,
        "GlacierJobParameters": GlacierJobParametersTypeDef,
        "Type": Literal["SELECT"],
        "Tier": TierType,
        "Description": str,
        "SelectParameters": SelectParametersTypeDef,
        "OutputLocation": OutputLocationTypeDef,
    },
    total=False,
)

_RequiredPutBucketLoggingRequestBucketLoggingPutTypeDef = TypedDict(
    "_RequiredPutBucketLoggingRequestBucketLoggingPutTypeDef",
    {
        "BucketLoggingStatus": BucketLoggingStatusTypeDef,
    },
)
_OptionalPutBucketLoggingRequestBucketLoggingPutTypeDef = TypedDict(
    "_OptionalPutBucketLoggingRequestBucketLoggingPutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketLoggingRequestBucketLoggingPutTypeDef(
    _RequiredPutBucketLoggingRequestBucketLoggingPutTypeDef,
    _OptionalPutBucketLoggingRequestBucketLoggingPutTypeDef,
):
    pass

_RequiredPutBucketLoggingRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketLoggingRequestRequestTypeDef",
    {
        "Bucket": str,
        "BucketLoggingStatus": BucketLoggingStatusTypeDef,
    },
)
_OptionalPutBucketLoggingRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketLoggingRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketLoggingRequestRequestTypeDef(
    _RequiredPutBucketLoggingRequestRequestTypeDef, _OptionalPutBucketLoggingRequestRequestTypeDef
):
    pass

InventoryConfigurationTypeDef = TypedDict(
    "InventoryConfigurationTypeDef",
    {
        "Destination": InventoryDestinationTypeDef,
        "IsEnabled": bool,
        "Filter": InventoryFilterTypeDef,
        "Id": str,
        "IncludedObjectVersions": InventoryIncludedObjectVersionsType,
        "OptionalFields": List[InventoryOptionalFieldType],
        "Schedule": InventoryScheduleTypeDef,
    },
)

ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef",
    {
        "Role": str,
        "Rules": List[ReplicationRuleTypeDef],
    },
)

PutBucketLifecycleConfigurationRequestBucketLifecycleConfigurationPutTypeDef = TypedDict(
    "PutBucketLifecycleConfigurationRequestBucketLifecycleConfigurationPutTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "LifecycleConfiguration": BucketLifecycleConfigurationTypeDef,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredPutBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalPutBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "LifecycleConfiguration": BucketLifecycleConfigurationTypeDef,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketLifecycleConfigurationRequestRequestTypeDef(
    _RequiredPutBucketLifecycleConfigurationRequestRequestTypeDef,
    _OptionalPutBucketLifecycleConfigurationRequestRequestTypeDef,
):
    pass

GetBucketAnalyticsConfigurationOutputTypeDef = TypedDict(
    "GetBucketAnalyticsConfigurationOutputTypeDef",
    {
        "AnalyticsConfiguration": AnalyticsConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBucketAnalyticsConfigurationsOutputTypeDef = TypedDict(
    "ListBucketAnalyticsConfigurationsOutputTypeDef",
    {
        "IsTruncated": bool,
        "ContinuationToken": str,
        "NextContinuationToken": str,
        "AnalyticsConfigurationList": List[AnalyticsConfigurationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutBucketAnalyticsConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketAnalyticsConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
        "AnalyticsConfiguration": AnalyticsConfigurationTypeDef,
    },
)
_OptionalPutBucketAnalyticsConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketAnalyticsConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketAnalyticsConfigurationRequestRequestTypeDef(
    _RequiredPutBucketAnalyticsConfigurationRequestRequestTypeDef,
    _OptionalPutBucketAnalyticsConfigurationRequestRequestTypeDef,
):
    pass

_RequiredPutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef = TypedDict(
    "_RequiredPutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef",
    {
        "NotificationConfiguration": NotificationConfigurationTypeDef,
    },
)
_OptionalPutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef = TypedDict(
    "_OptionalPutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef",
    {
        "ExpectedBucketOwner": str,
        "SkipDestinationValidation": bool,
    },
    total=False,
)

class PutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef(
    _RequiredPutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef,
    _OptionalPutBucketNotificationConfigurationRequestBucketNotificationPutTypeDef,
):
    pass

_RequiredPutBucketNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketNotificationConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
    },
)
_OptionalPutBucketNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketNotificationConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
        "SkipDestinationValidation": bool,
    },
    total=False,
)

class PutBucketNotificationConfigurationRequestRequestTypeDef(
    _RequiredPutBucketNotificationConfigurationRequestRequestTypeDef,
    _OptionalPutBucketNotificationConfigurationRequestRequestTypeDef,
):
    pass

RestoreObjectRequestObjectRestoreObjectTypeDef = TypedDict(
    "RestoreObjectRequestObjectRestoreObjectTypeDef",
    {
        "VersionId": str,
        "RestoreRequest": RestoreRequestTypeDef,
        "RequestPayer": Literal["requester"],
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

RestoreObjectRequestObjectSummaryRestoreObjectTypeDef = TypedDict(
    "RestoreObjectRequestObjectSummaryRestoreObjectTypeDef",
    {
        "VersionId": str,
        "RestoreRequest": RestoreRequestTypeDef,
        "RequestPayer": Literal["requester"],
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

_RequiredRestoreObjectRequestRequestTypeDef = TypedDict(
    "_RequiredRestoreObjectRequestRequestTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalRestoreObjectRequestRequestTypeDef = TypedDict(
    "_OptionalRestoreObjectRequestRequestTypeDef",
    {
        "VersionId": str,
        "RestoreRequest": RestoreRequestTypeDef,
        "RequestPayer": Literal["requester"],
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class RestoreObjectRequestRequestTypeDef(
    _RequiredRestoreObjectRequestRequestTypeDef, _OptionalRestoreObjectRequestRequestTypeDef
):
    pass

GetBucketInventoryConfigurationOutputTypeDef = TypedDict(
    "GetBucketInventoryConfigurationOutputTypeDef",
    {
        "InventoryConfiguration": InventoryConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBucketInventoryConfigurationsOutputTypeDef = TypedDict(
    "ListBucketInventoryConfigurationsOutputTypeDef",
    {
        "ContinuationToken": str,
        "InventoryConfigurationList": List[InventoryConfigurationTypeDef],
        "IsTruncated": bool,
        "NextContinuationToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutBucketInventoryConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketInventoryConfigurationRequestRequestTypeDef",
    {
        "Bucket": str,
        "Id": str,
        "InventoryConfiguration": InventoryConfigurationTypeDef,
    },
)
_OptionalPutBucketInventoryConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketInventoryConfigurationRequestRequestTypeDef",
    {
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketInventoryConfigurationRequestRequestTypeDef(
    _RequiredPutBucketInventoryConfigurationRequestRequestTypeDef,
    _OptionalPutBucketInventoryConfigurationRequestRequestTypeDef,
):
    pass

GetBucketReplicationOutputTypeDef = TypedDict(
    "GetBucketReplicationOutputTypeDef",
    {
        "ReplicationConfiguration": ReplicationConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPutBucketReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketReplicationRequestRequestTypeDef",
    {
        "Bucket": str,
        "ReplicationConfiguration": ReplicationConfigurationTypeDef,
    },
)
_OptionalPutBucketReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketReplicationRequestRequestTypeDef",
    {
        "ChecksumAlgorithm": ChecksumAlgorithmType,
        "Token": str,
        "ExpectedBucketOwner": str,
    },
    total=False,
)

class PutBucketReplicationRequestRequestTypeDef(
    _RequiredPutBucketReplicationRequestRequestTypeDef,
    _OptionalPutBucketReplicationRequestRequestTypeDef,
):
    pass
