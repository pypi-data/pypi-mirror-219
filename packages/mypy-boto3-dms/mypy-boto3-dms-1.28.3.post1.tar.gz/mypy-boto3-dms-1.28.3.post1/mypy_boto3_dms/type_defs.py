"""
Type annotations for dms service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/type_defs/)

Usage::

    ```python
    from mypy_boto3_dms.type_defs import AccountQuotaOutputTypeDef

    data: AccountQuotaOutputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AuthMechanismValueType,
    AuthTypeValueType,
    CannedAclForObjectsValueType,
    CharLengthSemanticsType,
    CollectorStatusType,
    CompressionTypeValueType,
    DatabaseModeType,
    DataFormatValueType,
    DatePartitionDelimiterValueType,
    DatePartitionSequenceValueType,
    DmsSslModeValueType,
    EncodingTypeValueType,
    EncryptionModeValueType,
    EndpointSettingTypeValueType,
    KafkaSaslMechanismType,
    KafkaSecurityProtocolType,
    KafkaSslEndpointIdentificationAlgorithmType,
    LongVarcharMappingTypeType,
    MessageFormatValueType,
    MigrationTypeValueType,
    NestingLevelValueType,
    ParquetVersionValueType,
    PluginNameValueType,
    RedisAuthTypeValueType,
    RefreshSchemasStatusTypeValueType,
    ReleaseStatusValuesType,
    ReloadOptionValueType,
    ReplicationEndpointTypeValueType,
    SafeguardPolicyType,
    SslSecurityProtocolValueType,
    StartReplicationTaskTypeValueType,
    TargetDbTypeType,
    TlogAccessModeType,
    VersionStatusType,
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
    "AccountQuotaOutputTypeDef",
    "TagTypeDef",
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    "AvailabilityZoneOutputTypeDef",
    "BatchStartRecommendationsErrorEntryOutputTypeDef",
    "CancelReplicationTaskAssessmentRunMessageRequestTypeDef",
    "CertificateOutputTypeDef",
    "CollectorHealthCheckOutputTypeDef",
    "InventoryDataOutputTypeDef",
    "CollectorShortInfoResponseOutputTypeDef",
    "ComputeConfigOutputTypeDef",
    "ComputeConfigTypeDef",
    "ConnectionOutputTypeDef",
    "DmsTransferSettingsTypeDef",
    "DocDbSettingsTypeDef",
    "DynamoDbSettingsTypeDef",
    "ElasticsearchSettingsTypeDef",
    "GcpMySQLSettingsTypeDef",
    "IBMDb2SettingsTypeDef",
    "KafkaSettingsTypeDef",
    "KinesisSettingsTypeDef",
    "MicrosoftSQLServerSettingsTypeDef",
    "MongoDbSettingsTypeDef",
    "MySQLSettingsTypeDef",
    "NeptuneSettingsTypeDef",
    "OracleSettingsTypeDef",
    "PostgreSQLSettingsTypeDef",
    "RedisSettingsTypeDef",
    "RedshiftSettingsTypeDef",
    "S3SettingsTypeDef",
    "SybaseSettingsTypeDef",
    "TimestreamSettingsTypeDef",
    "EventSubscriptionOutputTypeDef",
    "CreateFleetAdvisorCollectorRequestRequestTypeDef",
    "CreateFleetAdvisorCollectorResponseOutputTypeDef",
    "DatabaseInstanceSoftwareDetailsResponseOutputTypeDef",
    "ServerShortInfoResponseOutputTypeDef",
    "DatabaseShortInfoResponseOutputTypeDef",
    "DeleteCertificateMessageRequestTypeDef",
    "DeleteCollectorRequestRequestTypeDef",
    "DeleteConnectionMessageRequestTypeDef",
    "DeleteEndpointMessageRequestTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "DeleteFleetAdvisorDatabasesRequestRequestTypeDef",
    "DeleteFleetAdvisorDatabasesResponseOutputTypeDef",
    "DeleteReplicationConfigMessageRequestTypeDef",
    "DeleteReplicationInstanceMessageRequestTypeDef",
    "DeleteReplicationSubnetGroupMessageRequestTypeDef",
    "DeleteReplicationTaskAssessmentRunMessageRequestTypeDef",
    "DeleteReplicationTaskMessageRequestTypeDef",
    "DescribeApplicableIndividualAssessmentsMessageRequestTypeDef",
    "DescribeApplicableIndividualAssessmentsResponseOutputTypeDef",
    "FilterTypeDef",
    "WaiterConfigTypeDef",
    "DescribeEndpointSettingsMessageRequestTypeDef",
    "EndpointSettingOutputTypeDef",
    "SupportedEndpointTypeOutputTypeDef",
    "EventCategoryGroupOutputTypeDef",
    "EventOutputTypeDef",
    "DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef",
    "FleetAdvisorLsaAnalysisResponseOutputTypeDef",
    "FleetAdvisorSchemaObjectResponseOutputTypeDef",
    "DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef",
    "DescribeOrderableReplicationInstancesMessageRequestTypeDef",
    "OrderableReplicationInstanceOutputTypeDef",
    "LimitationOutputTypeDef",
    "DescribeRefreshSchemasStatusMessageRequestTypeDef",
    "RefreshSchemasStatusOutputTypeDef",
    "DescribeReplicationInstanceTaskLogsMessageRequestTypeDef",
    "ReplicationInstanceTaskLogOutputTypeDef",
    "TableStatisticsOutputTypeDef",
    "DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef",
    "DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef",
    "ReplicationTaskAssessmentResultOutputTypeDef",
    "ReplicationTaskIndividualAssessmentOutputTypeDef",
    "DescribeSchemasMessageDescribeSchemasPaginateTypeDef",
    "DescribeSchemasMessageRequestTypeDef",
    "DescribeSchemasResponseOutputTypeDef",
    "DmsTransferSettingsOutputTypeDef",
    "DocDbSettingsOutputTypeDef",
    "DynamoDbSettingsOutputTypeDef",
    "ElasticsearchSettingsOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GcpMySQLSettingsOutputTypeDef",
    "IBMDb2SettingsOutputTypeDef",
    "KafkaSettingsOutputTypeDef",
    "KinesisSettingsOutputTypeDef",
    "MicrosoftSQLServerSettingsOutputTypeDef",
    "MongoDbSettingsOutputTypeDef",
    "MySQLSettingsOutputTypeDef",
    "NeptuneSettingsOutputTypeDef",
    "OracleSettingsOutputTypeDef",
    "PostgreSQLSettingsOutputTypeDef",
    "RedisSettingsOutputTypeDef",
    "RedshiftSettingsOutputTypeDef",
    "S3SettingsOutputTypeDef",
    "SybaseSettingsOutputTypeDef",
    "TimestreamSettingsOutputTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "TagOutputTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "ModifyReplicationInstanceMessageRequestTypeDef",
    "ModifyReplicationSubnetGroupMessageRequestTypeDef",
    "ModifyReplicationTaskMessageRequestTypeDef",
    "MoveReplicationTaskMessageRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PendingMaintenanceActionOutputTypeDef",
    "ProvisionDataOutputTypeDef",
    "RdsConfigurationOutputTypeDef",
    "RdsRequirementsOutputTypeDef",
    "RebootReplicationInstanceMessageRequestTypeDef",
    "RecommendationSettingsOutputTypeDef",
    "RecommendationSettingsTypeDef",
    "RefreshSchemasMessageRequestTypeDef",
    "TableToReloadTypeDef",
    "ReloadReplicationTablesResponseOutputTypeDef",
    "ReloadTablesResponseOutputTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "ReplicationPendingModifiedValuesOutputTypeDef",
    "VpcSecurityGroupMembershipOutputTypeDef",
    "ReplicationStatsOutputTypeDef",
    "ReplicationTaskAssessmentRunProgressOutputTypeDef",
    "ReplicationTaskStatsOutputTypeDef",
    "ResponseMetadataTypeDef",
    "RunFleetAdvisorLsaAnalysisResponseOutputTypeDef",
    "SchemaShortInfoResponseOutputTypeDef",
    "StartReplicationMessageRequestTypeDef",
    "StartReplicationTaskAssessmentMessageRequestTypeDef",
    "StartReplicationTaskAssessmentRunMessageRequestTypeDef",
    "StartReplicationTaskMessageRequestTypeDef",
    "StopReplicationMessageRequestTypeDef",
    "StopReplicationTaskMessageRequestTypeDef",
    "TestConnectionMessageRequestTypeDef",
    "UpdateSubscriptionsToEventBridgeMessageRequestTypeDef",
    "UpdateSubscriptionsToEventBridgeResponseOutputTypeDef",
    "DescribeAccountAttributesResponseOutputTypeDef",
    "AddTagsToResourceMessageRequestTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "CreateReplicationInstanceMessageRequestTypeDef",
    "CreateReplicationSubnetGroupMessageRequestTypeDef",
    "CreateReplicationTaskMessageRequestTypeDef",
    "ImportCertificateMessageRequestTypeDef",
    "SubnetOutputTypeDef",
    "BatchStartRecommendationsResponseOutputTypeDef",
    "DeleteCertificateResponseOutputTypeDef",
    "DescribeCertificatesResponseOutputTypeDef",
    "ImportCertificateResponseOutputTypeDef",
    "CollectorResponseOutputTypeDef",
    "ReplicationConfigOutputTypeDef",
    "CreateReplicationConfigMessageRequestTypeDef",
    "ModifyReplicationConfigMessageRequestTypeDef",
    "DeleteConnectionResponseOutputTypeDef",
    "DescribeConnectionsResponseOutputTypeDef",
    "TestConnectionResponseOutputTypeDef",
    "CreateEndpointMessageRequestTypeDef",
    "ModifyEndpointMessageRequestTypeDef",
    "CreateEventSubscriptionResponseOutputTypeDef",
    "DeleteEventSubscriptionResponseOutputTypeDef",
    "DescribeEventSubscriptionsResponseOutputTypeDef",
    "ModifyEventSubscriptionResponseOutputTypeDef",
    "DatabaseResponseOutputTypeDef",
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    "DescribeCertificatesMessageRequestTypeDef",
    "DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef",
    "DescribeConnectionsMessageRequestTypeDef",
    "DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef",
    "DescribeEndpointTypesMessageRequestTypeDef",
    "DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef",
    "DescribeEndpointsMessageRequestTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeFleetAdvisorCollectorsRequestRequestTypeDef",
    "DescribeFleetAdvisorDatabasesRequestRequestTypeDef",
    "DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef",
    "DescribeFleetAdvisorSchemasRequestRequestTypeDef",
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    "DescribeRecommendationLimitationsRequestRequestTypeDef",
    "DescribeRecommendationsRequestRequestTypeDef",
    "DescribeReplicationConfigsMessageRequestTypeDef",
    "DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef",
    "DescribeReplicationInstancesMessageRequestTypeDef",
    "DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef",
    "DescribeReplicationSubnetGroupsMessageRequestTypeDef",
    "DescribeReplicationTableStatisticsMessageRequestTypeDef",
    "DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef",
    "DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef",
    "DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef",
    "DescribeReplicationTasksMessageRequestTypeDef",
    "DescribeReplicationsMessageRequestTypeDef",
    "DescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef",
    "DescribeTableStatisticsMessageRequestTypeDef",
    "DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef",
    "DescribeEndpointsMessageEndpointDeletedWaitTypeDef",
    "DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef",
    "DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef",
    "DescribeEndpointSettingsResponseOutputTypeDef",
    "DescribeEndpointTypesResponseOutputTypeDef",
    "DescribeEventCategoriesResponseOutputTypeDef",
    "DescribeEventsResponseOutputTypeDef",
    "DescribeFleetAdvisorLsaAnalysisResponseOutputTypeDef",
    "DescribeFleetAdvisorSchemaObjectSummaryResponseOutputTypeDef",
    "DescribeOrderableReplicationInstancesResponseOutputTypeDef",
    "DescribeRecommendationLimitationsResponseOutputTypeDef",
    "DescribeRefreshSchemasStatusResponseOutputTypeDef",
    "RefreshSchemasResponseOutputTypeDef",
    "DescribeReplicationInstanceTaskLogsResponseOutputTypeDef",
    "DescribeReplicationTableStatisticsResponseOutputTypeDef",
    "DescribeTableStatisticsResponseOutputTypeDef",
    "DescribeReplicationTaskAssessmentResultsResponseOutputTypeDef",
    "DescribeReplicationTaskIndividualAssessmentsResponseOutputTypeDef",
    "EndpointOutputTypeDef",
    "ListTagsForResourceResponseOutputTypeDef",
    "ResourcePendingMaintenanceActionsOutputTypeDef",
    "RdsRecommendationOutputTypeDef",
    "StartRecommendationsRequestEntryTypeDef",
    "StartRecommendationsRequestRequestTypeDef",
    "ReloadReplicationTablesMessageRequestTypeDef",
    "ReloadTablesMessageRequestTypeDef",
    "ReplicationOutputTypeDef",
    "ReplicationTaskAssessmentRunOutputTypeDef",
    "ReplicationTaskOutputTypeDef",
    "SchemaResponseOutputTypeDef",
    "ReplicationSubnetGroupOutputTypeDef",
    "DescribeFleetAdvisorCollectorsResponseOutputTypeDef",
    "CreateReplicationConfigResponseOutputTypeDef",
    "DeleteReplicationConfigResponseOutputTypeDef",
    "DescribeReplicationConfigsResponseOutputTypeDef",
    "ModifyReplicationConfigResponseOutputTypeDef",
    "DescribeFleetAdvisorDatabasesResponseOutputTypeDef",
    "CreateEndpointResponseOutputTypeDef",
    "DeleteEndpointResponseOutputTypeDef",
    "DescribeEndpointsResponseOutputTypeDef",
    "ModifyEndpointResponseOutputTypeDef",
    "ApplyPendingMaintenanceActionResponseOutputTypeDef",
    "DescribePendingMaintenanceActionsResponseOutputTypeDef",
    "RecommendationDataOutputTypeDef",
    "BatchStartRecommendationsRequestRequestTypeDef",
    "DescribeReplicationsResponseOutputTypeDef",
    "StartReplicationResponseOutputTypeDef",
    "StopReplicationResponseOutputTypeDef",
    "CancelReplicationTaskAssessmentRunResponseOutputTypeDef",
    "DeleteReplicationTaskAssessmentRunResponseOutputTypeDef",
    "DescribeReplicationTaskAssessmentRunsResponseOutputTypeDef",
    "StartReplicationTaskAssessmentRunResponseOutputTypeDef",
    "CreateReplicationTaskResponseOutputTypeDef",
    "DeleteReplicationTaskResponseOutputTypeDef",
    "DescribeReplicationTasksResponseOutputTypeDef",
    "ModifyReplicationTaskResponseOutputTypeDef",
    "MoveReplicationTaskResponseOutputTypeDef",
    "StartReplicationTaskAssessmentResponseOutputTypeDef",
    "StartReplicationTaskResponseOutputTypeDef",
    "StopReplicationTaskResponseOutputTypeDef",
    "DescribeFleetAdvisorSchemasResponseOutputTypeDef",
    "CreateReplicationSubnetGroupResponseOutputTypeDef",
    "DescribeReplicationSubnetGroupsResponseOutputTypeDef",
    "ModifyReplicationSubnetGroupResponseOutputTypeDef",
    "ReplicationInstanceOutputTypeDef",
    "RecommendationOutputTypeDef",
    "CreateReplicationInstanceResponseOutputTypeDef",
    "DeleteReplicationInstanceResponseOutputTypeDef",
    "DescribeReplicationInstancesResponseOutputTypeDef",
    "ModifyReplicationInstanceResponseOutputTypeDef",
    "RebootReplicationInstanceResponseOutputTypeDef",
    "DescribeRecommendationsResponseOutputTypeDef",
)

AccountQuotaOutputTypeDef = TypedDict(
    "AccountQuotaOutputTypeDef",
    {
        "AccountQuotaName": str,
        "Used": int,
        "Max": int,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
        "ResourceArn": str,
    },
    total=False,
)

ApplyPendingMaintenanceActionMessageRequestTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
        "ApplyAction": str,
        "OptInType": str,
    },
)

AvailabilityZoneOutputTypeDef = TypedDict(
    "AvailabilityZoneOutputTypeDef",
    {
        "Name": str,
    },
)

BatchStartRecommendationsErrorEntryOutputTypeDef = TypedDict(
    "BatchStartRecommendationsErrorEntryOutputTypeDef",
    {
        "DatabaseId": str,
        "Message": str,
        "Code": str,
    },
)

CancelReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "CancelReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ReplicationTaskAssessmentRunArn": str,
    },
)

CertificateOutputTypeDef = TypedDict(
    "CertificateOutputTypeDef",
    {
        "CertificateIdentifier": str,
        "CertificateCreationDate": datetime,
        "CertificatePem": str,
        "CertificateWallet": bytes,
        "CertificateArn": str,
        "CertificateOwner": str,
        "ValidFromDate": datetime,
        "ValidToDate": datetime,
        "SigningAlgorithm": str,
        "KeyLength": int,
    },
)

CollectorHealthCheckOutputTypeDef = TypedDict(
    "CollectorHealthCheckOutputTypeDef",
    {
        "CollectorStatus": CollectorStatusType,
        "LocalCollectorS3Access": bool,
        "WebCollectorS3Access": bool,
        "WebCollectorGrantedRoleBasedAccess": bool,
    },
)

InventoryDataOutputTypeDef = TypedDict(
    "InventoryDataOutputTypeDef",
    {
        "NumberOfDatabases": int,
        "NumberOfSchemas": int,
    },
)

CollectorShortInfoResponseOutputTypeDef = TypedDict(
    "CollectorShortInfoResponseOutputTypeDef",
    {
        "CollectorReferencedId": str,
        "CollectorName": str,
    },
)

ComputeConfigOutputTypeDef = TypedDict(
    "ComputeConfigOutputTypeDef",
    {
        "AvailabilityZone": str,
        "DnsNameServers": str,
        "KmsKeyId": str,
        "MaxCapacityUnits": int,
        "MinCapacityUnits": int,
        "MultiAZ": bool,
        "PreferredMaintenanceWindow": str,
        "ReplicationSubnetGroupId": str,
        "VpcSecurityGroupIds": List[str],
    },
)

ComputeConfigTypeDef = TypedDict(
    "ComputeConfigTypeDef",
    {
        "AvailabilityZone": str,
        "DnsNameServers": str,
        "KmsKeyId": str,
        "MaxCapacityUnits": int,
        "MinCapacityUnits": int,
        "MultiAZ": bool,
        "PreferredMaintenanceWindow": str,
        "ReplicationSubnetGroupId": str,
        "VpcSecurityGroupIds": Sequence[str],
    },
    total=False,
)

ConnectionOutputTypeDef = TypedDict(
    "ConnectionOutputTypeDef",
    {
        "ReplicationInstanceArn": str,
        "EndpointArn": str,
        "Status": str,
        "LastFailureMessage": str,
        "EndpointIdentifier": str,
        "ReplicationInstanceIdentifier": str,
    },
)

DmsTransferSettingsTypeDef = TypedDict(
    "DmsTransferSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "BucketName": str,
    },
    total=False,
)

DocDbSettingsTypeDef = TypedDict(
    "DocDbSettingsTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "NestingLevel": NestingLevelValueType,
        "ExtractDocId": bool,
        "DocsToInvestigate": int,
        "KmsKeyId": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "UseUpdateLookUp": bool,
        "ReplicateShardCollections": bool,
    },
    total=False,
)

DynamoDbSettingsTypeDef = TypedDict(
    "DynamoDbSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
    },
)

_RequiredElasticsearchSettingsTypeDef = TypedDict(
    "_RequiredElasticsearchSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "EndpointUri": str,
    },
)
_OptionalElasticsearchSettingsTypeDef = TypedDict(
    "_OptionalElasticsearchSettingsTypeDef",
    {
        "FullLoadErrorPercentage": int,
        "ErrorRetryDuration": int,
        "UseNewMappingType": bool,
    },
    total=False,
)


class ElasticsearchSettingsTypeDef(
    _RequiredElasticsearchSettingsTypeDef, _OptionalElasticsearchSettingsTypeDef
):
    pass


GcpMySQLSettingsTypeDef = TypedDict(
    "GcpMySQLSettingsTypeDef",
    {
        "AfterConnectScript": str,
        "CleanSourceMetadataOnMismatch": bool,
        "DatabaseName": str,
        "EventsPollInterval": int,
        "TargetDbType": TargetDbTypeType,
        "MaxFileSize": int,
        "ParallelLoadThreads": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "ServerTimezone": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

IBMDb2SettingsTypeDef = TypedDict(
    "IBMDb2SettingsTypeDef",
    {
        "DatabaseName": str,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "SetDataCaptureChanges": bool,
        "CurrentLsn": str,
        "MaxKBytesPerRead": int,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

KafkaSettingsTypeDef = TypedDict(
    "KafkaSettingsTypeDef",
    {
        "Broker": str,
        "Topic": str,
        "MessageFormat": MessageFormatValueType,
        "IncludeTransactionDetails": bool,
        "IncludePartitionValue": bool,
        "PartitionIncludeSchemaTable": bool,
        "IncludeTableAlterOperations": bool,
        "IncludeControlDetails": bool,
        "MessageMaxBytes": int,
        "IncludeNullAndEmpty": bool,
        "SecurityProtocol": KafkaSecurityProtocolType,
        "SslClientCertificateArn": str,
        "SslClientKeyArn": str,
        "SslClientKeyPassword": str,
        "SslCaCertificateArn": str,
        "SaslUsername": str,
        "SaslPassword": str,
        "NoHexPrefix": bool,
        "SaslMechanism": KafkaSaslMechanismType,
        "SslEndpointIdentificationAlgorithm": KafkaSslEndpointIdentificationAlgorithmType,
    },
    total=False,
)

KinesisSettingsTypeDef = TypedDict(
    "KinesisSettingsTypeDef",
    {
        "StreamArn": str,
        "MessageFormat": MessageFormatValueType,
        "ServiceAccessRoleArn": str,
        "IncludeTransactionDetails": bool,
        "IncludePartitionValue": bool,
        "PartitionIncludeSchemaTable": bool,
        "IncludeTableAlterOperations": bool,
        "IncludeControlDetails": bool,
        "IncludeNullAndEmpty": bool,
        "NoHexPrefix": bool,
    },
    total=False,
)

MicrosoftSQLServerSettingsTypeDef = TypedDict(
    "MicrosoftSQLServerSettingsTypeDef",
    {
        "Port": int,
        "BcpPacketSize": int,
        "DatabaseName": str,
        "ControlTablesFileGroup": str,
        "Password": str,
        "QuerySingleAlwaysOnNode": bool,
        "ReadBackupOnly": bool,
        "SafeguardPolicy": SafeguardPolicyType,
        "ServerName": str,
        "Username": str,
        "UseBcpFullLoad": bool,
        "UseThirdPartyBackupDevice": bool,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "TrimSpaceInChar": bool,
        "TlogAccessMode": TlogAccessModeType,
        "ForceLobLookup": bool,
    },
    total=False,
)

MongoDbSettingsTypeDef = TypedDict(
    "MongoDbSettingsTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "AuthType": AuthTypeValueType,
        "AuthMechanism": AuthMechanismValueType,
        "NestingLevel": NestingLevelValueType,
        "ExtractDocId": str,
        "DocsToInvestigate": str,
        "AuthSource": str,
        "KmsKeyId": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "UseUpdateLookUp": bool,
        "ReplicateShardCollections": bool,
    },
    total=False,
)

MySQLSettingsTypeDef = TypedDict(
    "MySQLSettingsTypeDef",
    {
        "AfterConnectScript": str,
        "CleanSourceMetadataOnMismatch": bool,
        "DatabaseName": str,
        "EventsPollInterval": int,
        "TargetDbType": TargetDbTypeType,
        "MaxFileSize": int,
        "ParallelLoadThreads": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "ServerTimezone": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

_RequiredNeptuneSettingsTypeDef = TypedDict(
    "_RequiredNeptuneSettingsTypeDef",
    {
        "S3BucketName": str,
        "S3BucketFolder": str,
    },
)
_OptionalNeptuneSettingsTypeDef = TypedDict(
    "_OptionalNeptuneSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "ErrorRetryDuration": int,
        "MaxFileSize": int,
        "MaxRetryCount": int,
        "IamAuthEnabled": bool,
    },
    total=False,
)


class NeptuneSettingsTypeDef(_RequiredNeptuneSettingsTypeDef, _OptionalNeptuneSettingsTypeDef):
    pass


OracleSettingsTypeDef = TypedDict(
    "OracleSettingsTypeDef",
    {
        "AddSupplementalLogging": bool,
        "ArchivedLogDestId": int,
        "AdditionalArchivedLogDestId": int,
        "ExtraArchivedLogDestIds": Sequence[int],
        "AllowSelectNestedTables": bool,
        "ParallelAsmReadThreads": int,
        "ReadAheadBlocks": int,
        "AccessAlternateDirectly": bool,
        "UseAlternateFolderForOnline": bool,
        "OraclePathPrefix": str,
        "UsePathPrefix": str,
        "ReplacePathPrefix": bool,
        "EnableHomogenousTablespace": bool,
        "DirectPathNoLog": bool,
        "ArchivedLogsOnly": bool,
        "AsmPassword": str,
        "AsmServer": str,
        "AsmUser": str,
        "CharLengthSemantics": CharLengthSemanticsType,
        "DatabaseName": str,
        "DirectPathParallelLoad": bool,
        "FailTasksOnLobTruncation": bool,
        "NumberDatatypeScale": int,
        "Password": str,
        "Port": int,
        "ReadTableSpaceName": bool,
        "RetryInterval": int,
        "SecurityDbEncryption": str,
        "SecurityDbEncryptionName": str,
        "ServerName": str,
        "SpatialDataOptionToGeoJsonFunctionName": str,
        "StandbyDelayTime": int,
        "Username": str,
        "UseBFile": bool,
        "UseDirectPathFullLoad": bool,
        "UseLogminerReader": bool,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "SecretsManagerOracleAsmAccessRoleArn": str,
        "SecretsManagerOracleAsmSecretId": str,
        "TrimSpaceInChar": bool,
        "ConvertTimestampWithZoneToUTC": bool,
        "OpenTransactionWindow": int,
    },
    total=False,
)

PostgreSQLSettingsTypeDef = TypedDict(
    "PostgreSQLSettingsTypeDef",
    {
        "AfterConnectScript": str,
        "CaptureDdls": bool,
        "MaxFileSize": int,
        "DatabaseName": str,
        "DdlArtifactsSchema": str,
        "ExecuteTimeout": int,
        "FailTasksOnLobTruncation": bool,
        "HeartbeatEnable": bool,
        "HeartbeatSchema": str,
        "HeartbeatFrequency": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "Username": str,
        "SlotName": str,
        "PluginName": PluginNameValueType,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "TrimSpaceInChar": bool,
        "MapBooleanAsBoolean": bool,
        "MapJsonbAsClob": bool,
        "MapLongVarcharAs": LongVarcharMappingTypeType,
        "DatabaseMode": DatabaseModeType,
        "BabelfishDatabaseName": str,
    },
    total=False,
)

_RequiredRedisSettingsTypeDef = TypedDict(
    "_RequiredRedisSettingsTypeDef",
    {
        "ServerName": str,
        "Port": int,
    },
)
_OptionalRedisSettingsTypeDef = TypedDict(
    "_OptionalRedisSettingsTypeDef",
    {
        "SslSecurityProtocol": SslSecurityProtocolValueType,
        "AuthType": RedisAuthTypeValueType,
        "AuthUserName": str,
        "AuthPassword": str,
        "SslCaCertificateArn": str,
    },
    total=False,
)


class RedisSettingsTypeDef(_RequiredRedisSettingsTypeDef, _OptionalRedisSettingsTypeDef):
    pass


RedshiftSettingsTypeDef = TypedDict(
    "RedshiftSettingsTypeDef",
    {
        "AcceptAnyDate": bool,
        "AfterConnectScript": str,
        "BucketFolder": str,
        "BucketName": str,
        "CaseSensitiveNames": bool,
        "CompUpdate": bool,
        "ConnectionTimeout": int,
        "DatabaseName": str,
        "DateFormat": str,
        "EmptyAsNull": bool,
        "EncryptionMode": EncryptionModeValueType,
        "ExplicitIds": bool,
        "FileTransferUploadStreams": int,
        "LoadTimeout": int,
        "MaxFileSize": int,
        "Password": str,
        "Port": int,
        "RemoveQuotes": bool,
        "ReplaceInvalidChars": str,
        "ReplaceChars": str,
        "ServerName": str,
        "ServiceAccessRoleArn": str,
        "ServerSideEncryptionKmsKeyId": str,
        "TimeFormat": str,
        "TrimBlanks": bool,
        "TruncateColumns": bool,
        "Username": str,
        "WriteBufferSize": int,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "MapBooleanAsBoolean": bool,
    },
    total=False,
)

S3SettingsTypeDef = TypedDict(
    "S3SettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "CsvRowDelimiter": str,
        "CsvDelimiter": str,
        "BucketFolder": str,
        "BucketName": str,
        "CompressionType": CompressionTypeValueType,
        "EncryptionMode": EncryptionModeValueType,
        "ServerSideEncryptionKmsKeyId": str,
        "DataFormat": DataFormatValueType,
        "EncodingType": EncodingTypeValueType,
        "DictPageSizeLimit": int,
        "RowGroupLength": int,
        "DataPageSize": int,
        "ParquetVersion": ParquetVersionValueType,
        "EnableStatistics": bool,
        "IncludeOpForFullLoad": bool,
        "CdcInsertsOnly": bool,
        "TimestampColumnName": str,
        "ParquetTimestampInMillisecond": bool,
        "CdcInsertsAndUpdates": bool,
        "DatePartitionEnabled": bool,
        "DatePartitionSequence": DatePartitionSequenceValueType,
        "DatePartitionDelimiter": DatePartitionDelimiterValueType,
        "UseCsvNoSupValue": bool,
        "CsvNoSupValue": str,
        "PreserveTransactions": bool,
        "CdcPath": str,
        "UseTaskStartTimeForFullLoadTimestamp": bool,
        "CannedAclForObjects": CannedAclForObjectsValueType,
        "AddColumnName": bool,
        "CdcMaxBatchInterval": int,
        "CdcMinFileSize": int,
        "CsvNullValue": str,
        "IgnoreHeaderRows": int,
        "MaxFileSize": int,
        "Rfc4180": bool,
        "DatePartitionTimezone": str,
        "AddTrailingPaddingCharacter": bool,
        "ExpectedBucketOwner": str,
        "GlueCatalogGeneration": bool,
    },
    total=False,
)

SybaseSettingsTypeDef = TypedDict(
    "SybaseSettingsTypeDef",
    {
        "DatabaseName": str,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

_RequiredTimestreamSettingsTypeDef = TypedDict(
    "_RequiredTimestreamSettingsTypeDef",
    {
        "DatabaseName": str,
        "MemoryDuration": int,
        "MagneticDuration": int,
    },
)
_OptionalTimestreamSettingsTypeDef = TypedDict(
    "_OptionalTimestreamSettingsTypeDef",
    {
        "CdcInsertsAndUpdates": bool,
        "EnableMagneticStoreWrites": bool,
    },
    total=False,
)


class TimestreamSettingsTypeDef(
    _RequiredTimestreamSettingsTypeDef, _OptionalTimestreamSettingsTypeDef
):
    pass


EventSubscriptionOutputTypeDef = TypedDict(
    "EventSubscriptionOutputTypeDef",
    {
        "CustomerAwsId": str,
        "CustSubscriptionId": str,
        "SnsTopicArn": str,
        "Status": str,
        "SubscriptionCreationTime": str,
        "SourceType": str,
        "SourceIdsList": List[str],
        "EventCategoriesList": List[str],
        "Enabled": bool,
    },
)

_RequiredCreateFleetAdvisorCollectorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFleetAdvisorCollectorRequestRequestTypeDef",
    {
        "CollectorName": str,
        "ServiceAccessRoleArn": str,
        "S3BucketName": str,
    },
)
_OptionalCreateFleetAdvisorCollectorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFleetAdvisorCollectorRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class CreateFleetAdvisorCollectorRequestRequestTypeDef(
    _RequiredCreateFleetAdvisorCollectorRequestRequestTypeDef,
    _OptionalCreateFleetAdvisorCollectorRequestRequestTypeDef,
):
    pass


CreateFleetAdvisorCollectorResponseOutputTypeDef = TypedDict(
    "CreateFleetAdvisorCollectorResponseOutputTypeDef",
    {
        "CollectorReferencedId": str,
        "CollectorName": str,
        "Description": str,
        "ServiceAccessRoleArn": str,
        "S3BucketName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatabaseInstanceSoftwareDetailsResponseOutputTypeDef = TypedDict(
    "DatabaseInstanceSoftwareDetailsResponseOutputTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "EngineEdition": str,
        "ServicePack": str,
        "SupportLevel": str,
        "OsArchitecture": int,
        "Tooltip": str,
    },
)

ServerShortInfoResponseOutputTypeDef = TypedDict(
    "ServerShortInfoResponseOutputTypeDef",
    {
        "ServerId": str,
        "IpAddress": str,
        "ServerName": str,
    },
)

DatabaseShortInfoResponseOutputTypeDef = TypedDict(
    "DatabaseShortInfoResponseOutputTypeDef",
    {
        "DatabaseId": str,
        "DatabaseName": str,
        "DatabaseIpAddress": str,
        "DatabaseEngine": str,
    },
)

DeleteCertificateMessageRequestTypeDef = TypedDict(
    "DeleteCertificateMessageRequestTypeDef",
    {
        "CertificateArn": str,
    },
)

DeleteCollectorRequestRequestTypeDef = TypedDict(
    "DeleteCollectorRequestRequestTypeDef",
    {
        "CollectorReferencedId": str,
    },
)

DeleteConnectionMessageRequestTypeDef = TypedDict(
    "DeleteConnectionMessageRequestTypeDef",
    {
        "EndpointArn": str,
        "ReplicationInstanceArn": str,
    },
)

DeleteEndpointMessageRequestTypeDef = TypedDict(
    "DeleteEndpointMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

DeleteEventSubscriptionMessageRequestTypeDef = TypedDict(
    "DeleteEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)

DeleteFleetAdvisorDatabasesRequestRequestTypeDef = TypedDict(
    "DeleteFleetAdvisorDatabasesRequestRequestTypeDef",
    {
        "DatabaseIds": Sequence[str],
    },
)

DeleteFleetAdvisorDatabasesResponseOutputTypeDef = TypedDict(
    "DeleteFleetAdvisorDatabasesResponseOutputTypeDef",
    {
        "DatabaseIds": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationConfigMessageRequestTypeDef = TypedDict(
    "DeleteReplicationConfigMessageRequestTypeDef",
    {
        "ReplicationConfigArn": str,
    },
)

DeleteReplicationInstanceMessageRequestTypeDef = TypedDict(
    "DeleteReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)

DeleteReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "DeleteReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
    },
)

DeleteReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "DeleteReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ReplicationTaskAssessmentRunArn": str,
    },
)

DeleteReplicationTaskMessageRequestTypeDef = TypedDict(
    "DeleteReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)

DescribeApplicableIndividualAssessmentsMessageRequestTypeDef = TypedDict(
    "DescribeApplicableIndividualAssessmentsMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "ReplicationInstanceArn": str,
        "SourceEngineName": str,
        "TargetEngineName": str,
        "MigrationType": MigrationTypeValueType,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeApplicableIndividualAssessmentsResponseOutputTypeDef = TypedDict(
    "DescribeApplicableIndividualAssessmentsResponseOutputTypeDef",
    {
        "IndividualAssessmentNames": List[str],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
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

_RequiredDescribeEndpointSettingsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeEndpointSettingsMessageRequestTypeDef",
    {
        "EngineName": str,
    },
)
_OptionalDescribeEndpointSettingsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeEndpointSettingsMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeEndpointSettingsMessageRequestTypeDef(
    _RequiredDescribeEndpointSettingsMessageRequestTypeDef,
    _OptionalDescribeEndpointSettingsMessageRequestTypeDef,
):
    pass


EndpointSettingOutputTypeDef = TypedDict(
    "EndpointSettingOutputTypeDef",
    {
        "Name": str,
        "Type": EndpointSettingTypeValueType,
        "EnumValues": List[str],
        "Sensitive": bool,
        "Units": str,
        "Applicability": str,
        "IntValueMin": int,
        "IntValueMax": int,
        "DefaultValue": str,
    },
)

SupportedEndpointTypeOutputTypeDef = TypedDict(
    "SupportedEndpointTypeOutputTypeDef",
    {
        "EngineName": str,
        "SupportsCDC": bool,
        "EndpointType": ReplicationEndpointTypeValueType,
        "ReplicationInstanceEngineMinimumVersion": str,
        "EngineDisplayName": str,
    },
)

EventCategoryGroupOutputTypeDef = TypedDict(
    "EventCategoryGroupOutputTypeDef",
    {
        "SourceType": str,
        "EventCategories": List[str],
    },
)

EventOutputTypeDef = TypedDict(
    "EventOutputTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal["replication-instance"],
        "Message": str,
        "EventCategories": List[str],
        "Date": datetime,
    },
)

DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef",
    {
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

FleetAdvisorLsaAnalysisResponseOutputTypeDef = TypedDict(
    "FleetAdvisorLsaAnalysisResponseOutputTypeDef",
    {
        "LsaAnalysisId": str,
        "Status": str,
    },
)

FleetAdvisorSchemaObjectResponseOutputTypeDef = TypedDict(
    "FleetAdvisorSchemaObjectResponseOutputTypeDef",
    {
        "SchemaId": str,
        "ObjectType": str,
        "NumberOfObjects": int,
        "CodeLineCount": int,
        "CodeSize": int,
    },
)

DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef = TypedDict(
    "DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeOrderableReplicationInstancesMessageRequestTypeDef = TypedDict(
    "DescribeOrderableReplicationInstancesMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

OrderableReplicationInstanceOutputTypeDef = TypedDict(
    "OrderableReplicationInstanceOutputTypeDef",
    {
        "EngineVersion": str,
        "ReplicationInstanceClass": str,
        "StorageType": str,
        "MinAllocatedStorage": int,
        "MaxAllocatedStorage": int,
        "DefaultAllocatedStorage": int,
        "IncludedAllocatedStorage": int,
        "AvailabilityZones": List[str],
        "ReleaseStatus": ReleaseStatusValuesType,
    },
)

LimitationOutputTypeDef = TypedDict(
    "LimitationOutputTypeDef",
    {
        "DatabaseId": str,
        "EngineName": str,
        "Name": str,
        "Description": str,
        "Impact": str,
        "Type": str,
    },
)

DescribeRefreshSchemasStatusMessageRequestTypeDef = TypedDict(
    "DescribeRefreshSchemasStatusMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

RefreshSchemasStatusOutputTypeDef = TypedDict(
    "RefreshSchemasStatusOutputTypeDef",
    {
        "EndpointArn": str,
        "ReplicationInstanceArn": str,
        "Status": RefreshSchemasStatusTypeValueType,
        "LastRefreshDate": datetime,
        "LastFailureMessage": str,
    },
)

_RequiredDescribeReplicationInstanceTaskLogsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeReplicationInstanceTaskLogsMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)
_OptionalDescribeReplicationInstanceTaskLogsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeReplicationInstanceTaskLogsMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeReplicationInstanceTaskLogsMessageRequestTypeDef(
    _RequiredDescribeReplicationInstanceTaskLogsMessageRequestTypeDef,
    _OptionalDescribeReplicationInstanceTaskLogsMessageRequestTypeDef,
):
    pass


ReplicationInstanceTaskLogOutputTypeDef = TypedDict(
    "ReplicationInstanceTaskLogOutputTypeDef",
    {
        "ReplicationTaskName": str,
        "ReplicationTaskArn": str,
        "ReplicationInstanceTaskLogSize": int,
    },
)

TableStatisticsOutputTypeDef = TypedDict(
    "TableStatisticsOutputTypeDef",
    {
        "SchemaName": str,
        "TableName": str,
        "Inserts": int,
        "Deletes": int,
        "Updates": int,
        "Ddls": int,
        "AppliedInserts": int,
        "AppliedDeletes": int,
        "AppliedUpdates": int,
        "AppliedDdls": int,
        "FullLoadRows": int,
        "FullLoadCondtnlChkFailedRows": int,
        "FullLoadErrorRows": int,
        "FullLoadStartTime": datetime,
        "FullLoadEndTime": datetime,
        "FullLoadReloaded": bool,
        "LastUpdateTime": datetime,
        "TableState": str,
        "ValidationPendingRecords": int,
        "ValidationFailedRecords": int,
        "ValidationSuspendedRecords": int,
        "ValidationState": str,
        "ValidationStateDetails": str,
    },
)

DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef",
    {
        "ReplicationTaskArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

ReplicationTaskAssessmentResultOutputTypeDef = TypedDict(
    "ReplicationTaskAssessmentResultOutputTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "ReplicationTaskArn": str,
        "ReplicationTaskLastAssessmentDate": datetime,
        "AssessmentStatus": str,
        "AssessmentResultsFile": str,
        "AssessmentResults": str,
        "S3ObjectUrl": str,
    },
)

ReplicationTaskIndividualAssessmentOutputTypeDef = TypedDict(
    "ReplicationTaskIndividualAssessmentOutputTypeDef",
    {
        "ReplicationTaskIndividualAssessmentArn": str,
        "ReplicationTaskAssessmentRunArn": str,
        "IndividualAssessmentName": str,
        "Status": str,
        "ReplicationTaskIndividualAssessmentStartDate": datetime,
    },
)

_RequiredDescribeSchemasMessageDescribeSchemasPaginateTypeDef = TypedDict(
    "_RequiredDescribeSchemasMessageDescribeSchemasPaginateTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalDescribeSchemasMessageDescribeSchemasPaginateTypeDef = TypedDict(
    "_OptionalDescribeSchemasMessageDescribeSchemasPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class DescribeSchemasMessageDescribeSchemasPaginateTypeDef(
    _RequiredDescribeSchemasMessageDescribeSchemasPaginateTypeDef,
    _OptionalDescribeSchemasMessageDescribeSchemasPaginateTypeDef,
):
    pass


_RequiredDescribeSchemasMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeSchemasMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalDescribeSchemasMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeSchemasMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeSchemasMessageRequestTypeDef(
    _RequiredDescribeSchemasMessageRequestTypeDef, _OptionalDescribeSchemasMessageRequestTypeDef
):
    pass


DescribeSchemasResponseOutputTypeDef = TypedDict(
    "DescribeSchemasResponseOutputTypeDef",
    {
        "Marker": str,
        "Schemas": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DmsTransferSettingsOutputTypeDef = TypedDict(
    "DmsTransferSettingsOutputTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "BucketName": str,
    },
)

DocDbSettingsOutputTypeDef = TypedDict(
    "DocDbSettingsOutputTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "NestingLevel": NestingLevelValueType,
        "ExtractDocId": bool,
        "DocsToInvestigate": int,
        "KmsKeyId": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "UseUpdateLookUp": bool,
        "ReplicateShardCollections": bool,
    },
)

DynamoDbSettingsOutputTypeDef = TypedDict(
    "DynamoDbSettingsOutputTypeDef",
    {
        "ServiceAccessRoleArn": str,
    },
)

ElasticsearchSettingsOutputTypeDef = TypedDict(
    "ElasticsearchSettingsOutputTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "EndpointUri": str,
        "FullLoadErrorPercentage": int,
        "ErrorRetryDuration": int,
        "UseNewMappingType": bool,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GcpMySQLSettingsOutputTypeDef = TypedDict(
    "GcpMySQLSettingsOutputTypeDef",
    {
        "AfterConnectScript": str,
        "CleanSourceMetadataOnMismatch": bool,
        "DatabaseName": str,
        "EventsPollInterval": int,
        "TargetDbType": TargetDbTypeType,
        "MaxFileSize": int,
        "ParallelLoadThreads": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "ServerTimezone": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
)

IBMDb2SettingsOutputTypeDef = TypedDict(
    "IBMDb2SettingsOutputTypeDef",
    {
        "DatabaseName": str,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "SetDataCaptureChanges": bool,
        "CurrentLsn": str,
        "MaxKBytesPerRead": int,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
)

KafkaSettingsOutputTypeDef = TypedDict(
    "KafkaSettingsOutputTypeDef",
    {
        "Broker": str,
        "Topic": str,
        "MessageFormat": MessageFormatValueType,
        "IncludeTransactionDetails": bool,
        "IncludePartitionValue": bool,
        "PartitionIncludeSchemaTable": bool,
        "IncludeTableAlterOperations": bool,
        "IncludeControlDetails": bool,
        "MessageMaxBytes": int,
        "IncludeNullAndEmpty": bool,
        "SecurityProtocol": KafkaSecurityProtocolType,
        "SslClientCertificateArn": str,
        "SslClientKeyArn": str,
        "SslClientKeyPassword": str,
        "SslCaCertificateArn": str,
        "SaslUsername": str,
        "SaslPassword": str,
        "NoHexPrefix": bool,
        "SaslMechanism": KafkaSaslMechanismType,
        "SslEndpointIdentificationAlgorithm": KafkaSslEndpointIdentificationAlgorithmType,
    },
)

KinesisSettingsOutputTypeDef = TypedDict(
    "KinesisSettingsOutputTypeDef",
    {
        "StreamArn": str,
        "MessageFormat": MessageFormatValueType,
        "ServiceAccessRoleArn": str,
        "IncludeTransactionDetails": bool,
        "IncludePartitionValue": bool,
        "PartitionIncludeSchemaTable": bool,
        "IncludeTableAlterOperations": bool,
        "IncludeControlDetails": bool,
        "IncludeNullAndEmpty": bool,
        "NoHexPrefix": bool,
    },
)

MicrosoftSQLServerSettingsOutputTypeDef = TypedDict(
    "MicrosoftSQLServerSettingsOutputTypeDef",
    {
        "Port": int,
        "BcpPacketSize": int,
        "DatabaseName": str,
        "ControlTablesFileGroup": str,
        "Password": str,
        "QuerySingleAlwaysOnNode": bool,
        "ReadBackupOnly": bool,
        "SafeguardPolicy": SafeguardPolicyType,
        "ServerName": str,
        "Username": str,
        "UseBcpFullLoad": bool,
        "UseThirdPartyBackupDevice": bool,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "TrimSpaceInChar": bool,
        "TlogAccessMode": TlogAccessModeType,
        "ForceLobLookup": bool,
    },
)

MongoDbSettingsOutputTypeDef = TypedDict(
    "MongoDbSettingsOutputTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "AuthType": AuthTypeValueType,
        "AuthMechanism": AuthMechanismValueType,
        "NestingLevel": NestingLevelValueType,
        "ExtractDocId": str,
        "DocsToInvestigate": str,
        "AuthSource": str,
        "KmsKeyId": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "UseUpdateLookUp": bool,
        "ReplicateShardCollections": bool,
    },
)

MySQLSettingsOutputTypeDef = TypedDict(
    "MySQLSettingsOutputTypeDef",
    {
        "AfterConnectScript": str,
        "CleanSourceMetadataOnMismatch": bool,
        "DatabaseName": str,
        "EventsPollInterval": int,
        "TargetDbType": TargetDbTypeType,
        "MaxFileSize": int,
        "ParallelLoadThreads": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "ServerTimezone": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
)

NeptuneSettingsOutputTypeDef = TypedDict(
    "NeptuneSettingsOutputTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "S3BucketName": str,
        "S3BucketFolder": str,
        "ErrorRetryDuration": int,
        "MaxFileSize": int,
        "MaxRetryCount": int,
        "IamAuthEnabled": bool,
    },
)

OracleSettingsOutputTypeDef = TypedDict(
    "OracleSettingsOutputTypeDef",
    {
        "AddSupplementalLogging": bool,
        "ArchivedLogDestId": int,
        "AdditionalArchivedLogDestId": int,
        "ExtraArchivedLogDestIds": List[int],
        "AllowSelectNestedTables": bool,
        "ParallelAsmReadThreads": int,
        "ReadAheadBlocks": int,
        "AccessAlternateDirectly": bool,
        "UseAlternateFolderForOnline": bool,
        "OraclePathPrefix": str,
        "UsePathPrefix": str,
        "ReplacePathPrefix": bool,
        "EnableHomogenousTablespace": bool,
        "DirectPathNoLog": bool,
        "ArchivedLogsOnly": bool,
        "AsmPassword": str,
        "AsmServer": str,
        "AsmUser": str,
        "CharLengthSemantics": CharLengthSemanticsType,
        "DatabaseName": str,
        "DirectPathParallelLoad": bool,
        "FailTasksOnLobTruncation": bool,
        "NumberDatatypeScale": int,
        "Password": str,
        "Port": int,
        "ReadTableSpaceName": bool,
        "RetryInterval": int,
        "SecurityDbEncryption": str,
        "SecurityDbEncryptionName": str,
        "ServerName": str,
        "SpatialDataOptionToGeoJsonFunctionName": str,
        "StandbyDelayTime": int,
        "Username": str,
        "UseBFile": bool,
        "UseDirectPathFullLoad": bool,
        "UseLogminerReader": bool,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "SecretsManagerOracleAsmAccessRoleArn": str,
        "SecretsManagerOracleAsmSecretId": str,
        "TrimSpaceInChar": bool,
        "ConvertTimestampWithZoneToUTC": bool,
        "OpenTransactionWindow": int,
    },
)

PostgreSQLSettingsOutputTypeDef = TypedDict(
    "PostgreSQLSettingsOutputTypeDef",
    {
        "AfterConnectScript": str,
        "CaptureDdls": bool,
        "MaxFileSize": int,
        "DatabaseName": str,
        "DdlArtifactsSchema": str,
        "ExecuteTimeout": int,
        "FailTasksOnLobTruncation": bool,
        "HeartbeatEnable": bool,
        "HeartbeatSchema": str,
        "HeartbeatFrequency": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "Username": str,
        "SlotName": str,
        "PluginName": PluginNameValueType,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "TrimSpaceInChar": bool,
        "MapBooleanAsBoolean": bool,
        "MapJsonbAsClob": bool,
        "MapLongVarcharAs": LongVarcharMappingTypeType,
        "DatabaseMode": DatabaseModeType,
        "BabelfishDatabaseName": str,
    },
)

RedisSettingsOutputTypeDef = TypedDict(
    "RedisSettingsOutputTypeDef",
    {
        "ServerName": str,
        "Port": int,
        "SslSecurityProtocol": SslSecurityProtocolValueType,
        "AuthType": RedisAuthTypeValueType,
        "AuthUserName": str,
        "AuthPassword": str,
        "SslCaCertificateArn": str,
    },
)

RedshiftSettingsOutputTypeDef = TypedDict(
    "RedshiftSettingsOutputTypeDef",
    {
        "AcceptAnyDate": bool,
        "AfterConnectScript": str,
        "BucketFolder": str,
        "BucketName": str,
        "CaseSensitiveNames": bool,
        "CompUpdate": bool,
        "ConnectionTimeout": int,
        "DatabaseName": str,
        "DateFormat": str,
        "EmptyAsNull": bool,
        "EncryptionMode": EncryptionModeValueType,
        "ExplicitIds": bool,
        "FileTransferUploadStreams": int,
        "LoadTimeout": int,
        "MaxFileSize": int,
        "Password": str,
        "Port": int,
        "RemoveQuotes": bool,
        "ReplaceInvalidChars": str,
        "ReplaceChars": str,
        "ServerName": str,
        "ServiceAccessRoleArn": str,
        "ServerSideEncryptionKmsKeyId": str,
        "TimeFormat": str,
        "TrimBlanks": bool,
        "TruncateColumns": bool,
        "Username": str,
        "WriteBufferSize": int,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "MapBooleanAsBoolean": bool,
    },
)

S3SettingsOutputTypeDef = TypedDict(
    "S3SettingsOutputTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "CsvRowDelimiter": str,
        "CsvDelimiter": str,
        "BucketFolder": str,
        "BucketName": str,
        "CompressionType": CompressionTypeValueType,
        "EncryptionMode": EncryptionModeValueType,
        "ServerSideEncryptionKmsKeyId": str,
        "DataFormat": DataFormatValueType,
        "EncodingType": EncodingTypeValueType,
        "DictPageSizeLimit": int,
        "RowGroupLength": int,
        "DataPageSize": int,
        "ParquetVersion": ParquetVersionValueType,
        "EnableStatistics": bool,
        "IncludeOpForFullLoad": bool,
        "CdcInsertsOnly": bool,
        "TimestampColumnName": str,
        "ParquetTimestampInMillisecond": bool,
        "CdcInsertsAndUpdates": bool,
        "DatePartitionEnabled": bool,
        "DatePartitionSequence": DatePartitionSequenceValueType,
        "DatePartitionDelimiter": DatePartitionDelimiterValueType,
        "UseCsvNoSupValue": bool,
        "CsvNoSupValue": str,
        "PreserveTransactions": bool,
        "CdcPath": str,
        "UseTaskStartTimeForFullLoadTimestamp": bool,
        "CannedAclForObjects": CannedAclForObjectsValueType,
        "AddColumnName": bool,
        "CdcMaxBatchInterval": int,
        "CdcMinFileSize": int,
        "CsvNullValue": str,
        "IgnoreHeaderRows": int,
        "MaxFileSize": int,
        "Rfc4180": bool,
        "DatePartitionTimezone": str,
        "AddTrailingPaddingCharacter": bool,
        "ExpectedBucketOwner": str,
        "GlueCatalogGeneration": bool,
    },
)

SybaseSettingsOutputTypeDef = TypedDict(
    "SybaseSettingsOutputTypeDef",
    {
        "DatabaseName": str,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
)

TimestreamSettingsOutputTypeDef = TypedDict(
    "TimestreamSettingsOutputTypeDef",
    {
        "DatabaseName": str,
        "MemoryDuration": int,
        "MagneticDuration": int,
        "CdcInsertsAndUpdates": bool,
        "EnableMagneticStoreWrites": bool,
    },
)

ListTagsForResourceMessageRequestTypeDef = TypedDict(
    "ListTagsForResourceMessageRequestTypeDef",
    {
        "ResourceArn": str,
        "ResourceArnList": Sequence[str],
    },
    total=False,
)

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "Key": str,
        "Value": str,
        "ResourceArn": str,
    },
)

_RequiredModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)
_OptionalModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SnsTopicArn": str,
        "SourceType": str,
        "EventCategories": Sequence[str],
        "Enabled": bool,
    },
    total=False,
)


class ModifyEventSubscriptionMessageRequestTypeDef(
    _RequiredModifyEventSubscriptionMessageRequestTypeDef,
    _OptionalModifyEventSubscriptionMessageRequestTypeDef,
):
    pass


_RequiredModifyReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredModifyReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)
_OptionalModifyReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalModifyReplicationInstanceMessageRequestTypeDef",
    {
        "AllocatedStorage": int,
        "ApplyImmediately": bool,
        "ReplicationInstanceClass": str,
        "VpcSecurityGroupIds": Sequence[str],
        "PreferredMaintenanceWindow": str,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AllowMajorVersionUpgrade": bool,
        "AutoMinorVersionUpgrade": bool,
        "ReplicationInstanceIdentifier": str,
        "NetworkType": str,
    },
    total=False,
)


class ModifyReplicationInstanceMessageRequestTypeDef(
    _RequiredModifyReplicationInstanceMessageRequestTypeDef,
    _OptionalModifyReplicationInstanceMessageRequestTypeDef,
):
    pass


_RequiredModifyReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredModifyReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalModifyReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalModifyReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupDescription": str,
    },
    total=False,
)


class ModifyReplicationSubnetGroupMessageRequestTypeDef(
    _RequiredModifyReplicationSubnetGroupMessageRequestTypeDef,
    _OptionalModifyReplicationSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredModifyReplicationTaskMessageRequestTypeDef = TypedDict(
    "_RequiredModifyReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)
_OptionalModifyReplicationTaskMessageRequestTypeDef = TypedDict(
    "_OptionalModifyReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "MigrationType": MigrationTypeValueType,
        "TableMappings": str,
        "ReplicationTaskSettings": str,
        "CdcStartTime": Union[datetime, str],
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "TaskData": str,
    },
    total=False,
)


class ModifyReplicationTaskMessageRequestTypeDef(
    _RequiredModifyReplicationTaskMessageRequestTypeDef,
    _OptionalModifyReplicationTaskMessageRequestTypeDef,
):
    pass


MoveReplicationTaskMessageRequestTypeDef = TypedDict(
    "MoveReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "TargetReplicationInstanceArn": str,
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

PendingMaintenanceActionOutputTypeDef = TypedDict(
    "PendingMaintenanceActionOutputTypeDef",
    {
        "Action": str,
        "AutoAppliedAfterDate": datetime,
        "ForcedApplyDate": datetime,
        "OptInStatus": str,
        "CurrentApplyDate": datetime,
        "Description": str,
    },
)

ProvisionDataOutputTypeDef = TypedDict(
    "ProvisionDataOutputTypeDef",
    {
        "ProvisionState": str,
        "ProvisionedCapacityUnits": int,
        "DateProvisioned": datetime,
        "IsNewProvisioningAvailable": bool,
        "DateNewProvisioningDataAvailable": datetime,
        "ReasonForNewProvisioningData": str,
    },
)

RdsConfigurationOutputTypeDef = TypedDict(
    "RdsConfigurationOutputTypeDef",
    {
        "EngineEdition": str,
        "InstanceType": str,
        "InstanceVcpu": float,
        "InstanceMemory": float,
        "StorageType": str,
        "StorageSize": int,
        "StorageIops": int,
        "DeploymentOption": str,
        "EngineVersion": str,
    },
)

RdsRequirementsOutputTypeDef = TypedDict(
    "RdsRequirementsOutputTypeDef",
    {
        "EngineEdition": str,
        "InstanceVcpu": float,
        "InstanceMemory": float,
        "StorageSize": int,
        "StorageIops": int,
        "DeploymentOption": str,
        "EngineVersion": str,
    },
)

_RequiredRebootReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredRebootReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)
_OptionalRebootReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalRebootReplicationInstanceMessageRequestTypeDef",
    {
        "ForceFailover": bool,
        "ForcePlannedFailover": bool,
    },
    total=False,
)


class RebootReplicationInstanceMessageRequestTypeDef(
    _RequiredRebootReplicationInstanceMessageRequestTypeDef,
    _OptionalRebootReplicationInstanceMessageRequestTypeDef,
):
    pass


RecommendationSettingsOutputTypeDef = TypedDict(
    "RecommendationSettingsOutputTypeDef",
    {
        "InstanceSizingType": str,
        "WorkloadType": str,
    },
)

RecommendationSettingsTypeDef = TypedDict(
    "RecommendationSettingsTypeDef",
    {
        "InstanceSizingType": str,
        "WorkloadType": str,
    },
)

RefreshSchemasMessageRequestTypeDef = TypedDict(
    "RefreshSchemasMessageRequestTypeDef",
    {
        "EndpointArn": str,
        "ReplicationInstanceArn": str,
    },
)

TableToReloadTypeDef = TypedDict(
    "TableToReloadTypeDef",
    {
        "SchemaName": str,
        "TableName": str,
    },
)

ReloadReplicationTablesResponseOutputTypeDef = TypedDict(
    "ReloadReplicationTablesResponseOutputTypeDef",
    {
        "ReplicationConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReloadTablesResponseOutputTypeDef = TypedDict(
    "ReloadTablesResponseOutputTypeDef",
    {
        "ReplicationTaskArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveTagsFromResourceMessageRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceMessageRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

ReplicationPendingModifiedValuesOutputTypeDef = TypedDict(
    "ReplicationPendingModifiedValuesOutputTypeDef",
    {
        "ReplicationInstanceClass": str,
        "AllocatedStorage": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "NetworkType": str,
    },
)

VpcSecurityGroupMembershipOutputTypeDef = TypedDict(
    "VpcSecurityGroupMembershipOutputTypeDef",
    {
        "VpcSecurityGroupId": str,
        "Status": str,
    },
)

ReplicationStatsOutputTypeDef = TypedDict(
    "ReplicationStatsOutputTypeDef",
    {
        "FullLoadProgressPercent": int,
        "ElapsedTimeMillis": int,
        "TablesLoaded": int,
        "TablesLoading": int,
        "TablesQueued": int,
        "TablesErrored": int,
        "FreshStartDate": datetime,
        "StartDate": datetime,
        "StopDate": datetime,
        "FullLoadStartDate": datetime,
        "FullLoadFinishDate": datetime,
    },
)

ReplicationTaskAssessmentRunProgressOutputTypeDef = TypedDict(
    "ReplicationTaskAssessmentRunProgressOutputTypeDef",
    {
        "IndividualAssessmentCount": int,
        "IndividualAssessmentCompletedCount": int,
    },
)

ReplicationTaskStatsOutputTypeDef = TypedDict(
    "ReplicationTaskStatsOutputTypeDef",
    {
        "FullLoadProgressPercent": int,
        "ElapsedTimeMillis": int,
        "TablesLoaded": int,
        "TablesLoading": int,
        "TablesQueued": int,
        "TablesErrored": int,
        "FreshStartDate": datetime,
        "StartDate": datetime,
        "StopDate": datetime,
        "FullLoadStartDate": datetime,
        "FullLoadFinishDate": datetime,
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

RunFleetAdvisorLsaAnalysisResponseOutputTypeDef = TypedDict(
    "RunFleetAdvisorLsaAnalysisResponseOutputTypeDef",
    {
        "LsaAnalysisId": str,
        "Status": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SchemaShortInfoResponseOutputTypeDef = TypedDict(
    "SchemaShortInfoResponseOutputTypeDef",
    {
        "SchemaId": str,
        "SchemaName": str,
        "DatabaseId": str,
        "DatabaseName": str,
        "DatabaseIpAddress": str,
    },
)

_RequiredStartReplicationMessageRequestTypeDef = TypedDict(
    "_RequiredStartReplicationMessageRequestTypeDef",
    {
        "ReplicationConfigArn": str,
        "StartReplicationType": str,
    },
)
_OptionalStartReplicationMessageRequestTypeDef = TypedDict(
    "_OptionalStartReplicationMessageRequestTypeDef",
    {
        "CdcStartTime": Union[datetime, str],
        "CdcStartPosition": str,
        "CdcStopPosition": str,
    },
    total=False,
)


class StartReplicationMessageRequestTypeDef(
    _RequiredStartReplicationMessageRequestTypeDef, _OptionalStartReplicationMessageRequestTypeDef
):
    pass


StartReplicationTaskAssessmentMessageRequestTypeDef = TypedDict(
    "StartReplicationTaskAssessmentMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)

_RequiredStartReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "_RequiredStartReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "ServiceAccessRoleArn": str,
        "ResultLocationBucket": str,
        "AssessmentRunName": str,
    },
)
_OptionalStartReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "_OptionalStartReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ResultLocationFolder": str,
        "ResultEncryptionMode": str,
        "ResultKmsKeyArn": str,
        "IncludeOnly": Sequence[str],
        "Exclude": Sequence[str],
    },
    total=False,
)


class StartReplicationTaskAssessmentRunMessageRequestTypeDef(
    _RequiredStartReplicationTaskAssessmentRunMessageRequestTypeDef,
    _OptionalStartReplicationTaskAssessmentRunMessageRequestTypeDef,
):
    pass


_RequiredStartReplicationTaskMessageRequestTypeDef = TypedDict(
    "_RequiredStartReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "StartReplicationTaskType": StartReplicationTaskTypeValueType,
    },
)
_OptionalStartReplicationTaskMessageRequestTypeDef = TypedDict(
    "_OptionalStartReplicationTaskMessageRequestTypeDef",
    {
        "CdcStartTime": Union[datetime, str],
        "CdcStartPosition": str,
        "CdcStopPosition": str,
    },
    total=False,
)


class StartReplicationTaskMessageRequestTypeDef(
    _RequiredStartReplicationTaskMessageRequestTypeDef,
    _OptionalStartReplicationTaskMessageRequestTypeDef,
):
    pass


StopReplicationMessageRequestTypeDef = TypedDict(
    "StopReplicationMessageRequestTypeDef",
    {
        "ReplicationConfigArn": str,
    },
)

StopReplicationTaskMessageRequestTypeDef = TypedDict(
    "StopReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)

TestConnectionMessageRequestTypeDef = TypedDict(
    "TestConnectionMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
        "EndpointArn": str,
    },
)

UpdateSubscriptionsToEventBridgeMessageRequestTypeDef = TypedDict(
    "UpdateSubscriptionsToEventBridgeMessageRequestTypeDef",
    {
        "ForceMove": bool,
    },
    total=False,
)

UpdateSubscriptionsToEventBridgeResponseOutputTypeDef = TypedDict(
    "UpdateSubscriptionsToEventBridgeResponseOutputTypeDef",
    {
        "Result": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeAccountAttributesResponseOutputTypeDef = TypedDict(
    "DescribeAccountAttributesResponseOutputTypeDef",
    {
        "AccountQuotas": List[AccountQuotaOutputTypeDef],
        "UniqueAccountIdentifier": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AddTagsToResourceMessageRequestTypeDef = TypedDict(
    "AddTagsToResourceMessageRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SnsTopicArn": str,
    },
)
_OptionalCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SourceType": str,
        "EventCategories": Sequence[str],
        "SourceIds": Sequence[str],
        "Enabled": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEventSubscriptionMessageRequestTypeDef(
    _RequiredCreateEventSubscriptionMessageRequestTypeDef,
    _OptionalCreateEventSubscriptionMessageRequestTypeDef,
):
    pass


_RequiredCreateReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceIdentifier": str,
        "ReplicationInstanceClass": str,
    },
)
_OptionalCreateReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationInstanceMessageRequestTypeDef",
    {
        "AllocatedStorage": int,
        "VpcSecurityGroupIds": Sequence[str],
        "AvailabilityZone": str,
        "ReplicationSubnetGroupIdentifier": str,
        "PreferredMaintenanceWindow": str,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "PubliclyAccessible": bool,
        "DnsNameServers": str,
        "ResourceIdentifier": str,
        "NetworkType": str,
    },
    total=False,
)


class CreateReplicationInstanceMessageRequestTypeDef(
    _RequiredCreateReplicationInstanceMessageRequestTypeDef,
    _OptionalCreateReplicationInstanceMessageRequestTypeDef,
):
    pass


_RequiredCreateReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
        "ReplicationSubnetGroupDescription": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationSubnetGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateReplicationSubnetGroupMessageRequestTypeDef(
    _RequiredCreateReplicationSubnetGroupMessageRequestTypeDef,
    _OptionalCreateReplicationSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateReplicationTaskMessageRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ReplicationInstanceArn": str,
        "MigrationType": MigrationTypeValueType,
        "TableMappings": str,
    },
)
_OptionalCreateReplicationTaskMessageRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskSettings": str,
        "CdcStartTime": Union[datetime, str],
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "Tags": Sequence[TagTypeDef],
        "TaskData": str,
        "ResourceIdentifier": str,
    },
    total=False,
)


class CreateReplicationTaskMessageRequestTypeDef(
    _RequiredCreateReplicationTaskMessageRequestTypeDef,
    _OptionalCreateReplicationTaskMessageRequestTypeDef,
):
    pass


_RequiredImportCertificateMessageRequestTypeDef = TypedDict(
    "_RequiredImportCertificateMessageRequestTypeDef",
    {
        "CertificateIdentifier": str,
    },
)
_OptionalImportCertificateMessageRequestTypeDef = TypedDict(
    "_OptionalImportCertificateMessageRequestTypeDef",
    {
        "CertificatePem": str,
        "CertificateWallet": Union[str, bytes, IO[Any], StreamingBody],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class ImportCertificateMessageRequestTypeDef(
    _RequiredImportCertificateMessageRequestTypeDef, _OptionalImportCertificateMessageRequestTypeDef
):
    pass


SubnetOutputTypeDef = TypedDict(
    "SubnetOutputTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AvailabilityZoneOutputTypeDef,
        "SubnetStatus": str,
    },
)

BatchStartRecommendationsResponseOutputTypeDef = TypedDict(
    "BatchStartRecommendationsResponseOutputTypeDef",
    {
        "ErrorEntries": List[BatchStartRecommendationsErrorEntryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteCertificateResponseOutputTypeDef = TypedDict(
    "DeleteCertificateResponseOutputTypeDef",
    {
        "Certificate": CertificateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCertificatesResponseOutputTypeDef = TypedDict(
    "DescribeCertificatesResponseOutputTypeDef",
    {
        "Marker": str,
        "Certificates": List[CertificateOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportCertificateResponseOutputTypeDef = TypedDict(
    "ImportCertificateResponseOutputTypeDef",
    {
        "Certificate": CertificateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CollectorResponseOutputTypeDef = TypedDict(
    "CollectorResponseOutputTypeDef",
    {
        "CollectorReferencedId": str,
        "CollectorName": str,
        "CollectorVersion": str,
        "VersionStatus": VersionStatusType,
        "Description": str,
        "S3BucketName": str,
        "ServiceAccessRoleArn": str,
        "CollectorHealthCheck": CollectorHealthCheckOutputTypeDef,
        "LastDataReceived": str,
        "RegisteredDate": str,
        "CreatedDate": str,
        "ModifiedDate": str,
        "InventoryData": InventoryDataOutputTypeDef,
    },
)

ReplicationConfigOutputTypeDef = TypedDict(
    "ReplicationConfigOutputTypeDef",
    {
        "ReplicationConfigIdentifier": str,
        "ReplicationConfigArn": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ReplicationType": MigrationTypeValueType,
        "ComputeConfig": ComputeConfigOutputTypeDef,
        "ReplicationSettings": str,
        "SupplementalSettings": str,
        "TableMappings": str,
        "ReplicationConfigCreateTime": datetime,
        "ReplicationConfigUpdateTime": datetime,
    },
)

_RequiredCreateReplicationConfigMessageRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationConfigMessageRequestTypeDef",
    {
        "ReplicationConfigIdentifier": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ComputeConfig": ComputeConfigTypeDef,
        "ReplicationType": MigrationTypeValueType,
        "TableMappings": str,
    },
)
_OptionalCreateReplicationConfigMessageRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationConfigMessageRequestTypeDef",
    {
        "ReplicationSettings": str,
        "SupplementalSettings": str,
        "ResourceIdentifier": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateReplicationConfigMessageRequestTypeDef(
    _RequiredCreateReplicationConfigMessageRequestTypeDef,
    _OptionalCreateReplicationConfigMessageRequestTypeDef,
):
    pass


_RequiredModifyReplicationConfigMessageRequestTypeDef = TypedDict(
    "_RequiredModifyReplicationConfigMessageRequestTypeDef",
    {
        "ReplicationConfigArn": str,
    },
)
_OptionalModifyReplicationConfigMessageRequestTypeDef = TypedDict(
    "_OptionalModifyReplicationConfigMessageRequestTypeDef",
    {
        "ReplicationConfigIdentifier": str,
        "ReplicationType": MigrationTypeValueType,
        "TableMappings": str,
        "ReplicationSettings": str,
        "SupplementalSettings": str,
        "ComputeConfig": ComputeConfigTypeDef,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
    },
    total=False,
)


class ModifyReplicationConfigMessageRequestTypeDef(
    _RequiredModifyReplicationConfigMessageRequestTypeDef,
    _OptionalModifyReplicationConfigMessageRequestTypeDef,
):
    pass


DeleteConnectionResponseOutputTypeDef = TypedDict(
    "DeleteConnectionResponseOutputTypeDef",
    {
        "Connection": ConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeConnectionsResponseOutputTypeDef = TypedDict(
    "DescribeConnectionsResponseOutputTypeDef",
    {
        "Marker": str,
        "Connections": List[ConnectionOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TestConnectionResponseOutputTypeDef = TypedDict(
    "TestConnectionResponseOutputTypeDef",
    {
        "Connection": ConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointMessageRequestTypeDef",
    {
        "EndpointIdentifier": str,
        "EndpointType": ReplicationEndpointTypeValueType,
        "EngineName": str,
    },
)
_OptionalCreateEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointMessageRequestTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "ExtraConnectionAttributes": str,
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
        "CertificateArn": str,
        "SslMode": DmsSslModeValueType,
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "DynamoDbSettings": DynamoDbSettingsTypeDef,
        "S3Settings": S3SettingsTypeDef,
        "DmsTransferSettings": DmsTransferSettingsTypeDef,
        "MongoDbSettings": MongoDbSettingsTypeDef,
        "KinesisSettings": KinesisSettingsTypeDef,
        "KafkaSettings": KafkaSettingsTypeDef,
        "ElasticsearchSettings": ElasticsearchSettingsTypeDef,
        "NeptuneSettings": NeptuneSettingsTypeDef,
        "RedshiftSettings": RedshiftSettingsTypeDef,
        "PostgreSQLSettings": PostgreSQLSettingsTypeDef,
        "MySQLSettings": MySQLSettingsTypeDef,
        "OracleSettings": OracleSettingsTypeDef,
        "SybaseSettings": SybaseSettingsTypeDef,
        "MicrosoftSQLServerSettings": MicrosoftSQLServerSettingsTypeDef,
        "IBMDb2Settings": IBMDb2SettingsTypeDef,
        "ResourceIdentifier": str,
        "DocDbSettings": DocDbSettingsTypeDef,
        "RedisSettings": RedisSettingsTypeDef,
        "GcpMySQLSettings": GcpMySQLSettingsTypeDef,
        "TimestreamSettings": TimestreamSettingsTypeDef,
    },
    total=False,
)


class CreateEndpointMessageRequestTypeDef(
    _RequiredCreateEndpointMessageRequestTypeDef, _OptionalCreateEndpointMessageRequestTypeDef
):
    pass


_RequiredModifyEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEndpointMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalModifyEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEndpointMessageRequestTypeDef",
    {
        "EndpointIdentifier": str,
        "EndpointType": ReplicationEndpointTypeValueType,
        "EngineName": str,
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "ExtraConnectionAttributes": str,
        "CertificateArn": str,
        "SslMode": DmsSslModeValueType,
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "DynamoDbSettings": DynamoDbSettingsTypeDef,
        "S3Settings": S3SettingsTypeDef,
        "DmsTransferSettings": DmsTransferSettingsTypeDef,
        "MongoDbSettings": MongoDbSettingsTypeDef,
        "KinesisSettings": KinesisSettingsTypeDef,
        "KafkaSettings": KafkaSettingsTypeDef,
        "ElasticsearchSettings": ElasticsearchSettingsTypeDef,
        "NeptuneSettings": NeptuneSettingsTypeDef,
        "RedshiftSettings": RedshiftSettingsTypeDef,
        "PostgreSQLSettings": PostgreSQLSettingsTypeDef,
        "MySQLSettings": MySQLSettingsTypeDef,
        "OracleSettings": OracleSettingsTypeDef,
        "SybaseSettings": SybaseSettingsTypeDef,
        "MicrosoftSQLServerSettings": MicrosoftSQLServerSettingsTypeDef,
        "IBMDb2Settings": IBMDb2SettingsTypeDef,
        "DocDbSettings": DocDbSettingsTypeDef,
        "RedisSettings": RedisSettingsTypeDef,
        "ExactSettings": bool,
        "GcpMySQLSettings": GcpMySQLSettingsTypeDef,
        "TimestreamSettings": TimestreamSettingsTypeDef,
    },
    total=False,
)


class ModifyEndpointMessageRequestTypeDef(
    _RequiredModifyEndpointMessageRequestTypeDef, _OptionalModifyEndpointMessageRequestTypeDef
):
    pass


CreateEventSubscriptionResponseOutputTypeDef = TypedDict(
    "CreateEventSubscriptionResponseOutputTypeDef",
    {
        "EventSubscription": EventSubscriptionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEventSubscriptionResponseOutputTypeDef = TypedDict(
    "DeleteEventSubscriptionResponseOutputTypeDef",
    {
        "EventSubscription": EventSubscriptionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventSubscriptionsResponseOutputTypeDef = TypedDict(
    "DescribeEventSubscriptionsResponseOutputTypeDef",
    {
        "Marker": str,
        "EventSubscriptionsList": List[EventSubscriptionOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyEventSubscriptionResponseOutputTypeDef = TypedDict(
    "ModifyEventSubscriptionResponseOutputTypeDef",
    {
        "EventSubscription": EventSubscriptionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatabaseResponseOutputTypeDef = TypedDict(
    "DatabaseResponseOutputTypeDef",
    {
        "DatabaseId": str,
        "DatabaseName": str,
        "IpAddress": str,
        "NumberOfSchemas": int,
        "Server": ServerShortInfoResponseOutputTypeDef,
        "SoftwareDetails": DatabaseInstanceSoftwareDetailsResponseOutputTypeDef,
        "Collectors": List[CollectorShortInfoResponseOutputTypeDef],
    },
)

DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef = TypedDict(
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeCertificatesMessageRequestTypeDef = TypedDict(
    "DescribeCertificatesMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef = TypedDict(
    "DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeConnectionsMessageRequestTypeDef = TypedDict(
    "DescribeConnectionsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef = TypedDict(
    "DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEndpointTypesMessageRequestTypeDef = TypedDict(
    "DescribeEndpointTypesMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef = TypedDict(
    "DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEndpointsMessageRequestTypeDef = TypedDict(
    "DescribeEndpointsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEventCategoriesMessageRequestTypeDef = TypedDict(
    "DescribeEventCategoriesMessageRequestTypeDef",
    {
        "SourceType": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEventSubscriptionsMessageRequestTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEventsMessageDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal["replication-instance"],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEventsMessageRequestTypeDef = TypedDict(
    "DescribeEventsMessageRequestTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal["replication-instance"],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeFleetAdvisorCollectorsRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorCollectorsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFleetAdvisorDatabasesRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorDatabasesRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFleetAdvisorSchemasRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemasRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribePendingMaintenanceActionsMessageRequestTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribeRecommendationLimitationsRequestRequestTypeDef = TypedDict(
    "DescribeRecommendationLimitationsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeRecommendationsRequestRequestTypeDef = TypedDict(
    "DescribeRecommendationsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeReplicationConfigsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationConfigsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationInstancesMessageRequestTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef = TypedDict(
    "DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationSubnetGroupsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationSubnetGroupsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeReplicationTableStatisticsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeReplicationTableStatisticsMessageRequestTypeDef",
    {
        "ReplicationConfigArn": str,
    },
)
_OptionalDescribeReplicationTableStatisticsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeReplicationTableStatisticsMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class DescribeReplicationTableStatisticsMessageRequestTypeDef(
    _RequiredDescribeReplicationTableStatisticsMessageRequestTypeDef,
    _OptionalDescribeReplicationTableStatisticsMessageRequestTypeDef,
):
    pass


DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef = TypedDict(
    "DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "WithoutSettings": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationTasksMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTasksMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
    },
    total=False,
)

DescribeReplicationsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef = TypedDict(
    "_RequiredDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)
_OptionalDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef = TypedDict(
    "_OptionalDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class DescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef(
    _RequiredDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef,
    _OptionalDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef,
):
    pass


_RequiredDescribeTableStatisticsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeTableStatisticsMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)
_OptionalDescribeTableStatisticsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeTableStatisticsMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class DescribeTableStatisticsMessageRequestTypeDef(
    _RequiredDescribeTableStatisticsMessageRequestTypeDef,
    _OptionalDescribeTableStatisticsMessageRequestTypeDef,
):
    pass


DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef = TypedDict(
    "DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeEndpointsMessageEndpointDeletedWaitTypeDef = TypedDict(
    "DescribeEndpointsMessageEndpointDeletedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeEndpointSettingsResponseOutputTypeDef = TypedDict(
    "DescribeEndpointSettingsResponseOutputTypeDef",
    {
        "Marker": str,
        "EndpointSettings": List[EndpointSettingOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEndpointTypesResponseOutputTypeDef = TypedDict(
    "DescribeEndpointTypesResponseOutputTypeDef",
    {
        "Marker": str,
        "SupportedEndpointTypes": List[SupportedEndpointTypeOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventCategoriesResponseOutputTypeDef = TypedDict(
    "DescribeEventCategoriesResponseOutputTypeDef",
    {
        "EventCategoryGroupList": List[EventCategoryGroupOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventsResponseOutputTypeDef = TypedDict(
    "DescribeEventsResponseOutputTypeDef",
    {
        "Marker": str,
        "Events": List[EventOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorLsaAnalysisResponseOutputTypeDef = TypedDict(
    "DescribeFleetAdvisorLsaAnalysisResponseOutputTypeDef",
    {
        "Analysis": List[FleetAdvisorLsaAnalysisResponseOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorSchemaObjectSummaryResponseOutputTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemaObjectSummaryResponseOutputTypeDef",
    {
        "FleetAdvisorSchemaObjects": List[FleetAdvisorSchemaObjectResponseOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOrderableReplicationInstancesResponseOutputTypeDef = TypedDict(
    "DescribeOrderableReplicationInstancesResponseOutputTypeDef",
    {
        "OrderableReplicationInstances": List[OrderableReplicationInstanceOutputTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecommendationLimitationsResponseOutputTypeDef = TypedDict(
    "DescribeRecommendationLimitationsResponseOutputTypeDef",
    {
        "NextToken": str,
        "Limitations": List[LimitationOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRefreshSchemasStatusResponseOutputTypeDef = TypedDict(
    "DescribeRefreshSchemasStatusResponseOutputTypeDef",
    {
        "RefreshSchemasStatus": RefreshSchemasStatusOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RefreshSchemasResponseOutputTypeDef = TypedDict(
    "RefreshSchemasResponseOutputTypeDef",
    {
        "RefreshSchemasStatus": RefreshSchemasStatusOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationInstanceTaskLogsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationInstanceTaskLogsResponseOutputTypeDef",
    {
        "ReplicationInstanceArn": str,
        "ReplicationInstanceTaskLogs": List[ReplicationInstanceTaskLogOutputTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTableStatisticsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationTableStatisticsResponseOutputTypeDef",
    {
        "ReplicationConfigArn": str,
        "Marker": str,
        "ReplicationTableStatistics": List[TableStatisticsOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTableStatisticsResponseOutputTypeDef = TypedDict(
    "DescribeTableStatisticsResponseOutputTypeDef",
    {
        "ReplicationTaskArn": str,
        "TableStatistics": List[TableStatisticsOutputTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTaskAssessmentResultsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentResultsResponseOutputTypeDef",
    {
        "Marker": str,
        "BucketName": str,
        "ReplicationTaskAssessmentResults": List[ReplicationTaskAssessmentResultOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTaskIndividualAssessmentsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationTaskIndividualAssessmentsResponseOutputTypeDef",
    {
        "Marker": str,
        "ReplicationTaskIndividualAssessments": List[
            ReplicationTaskIndividualAssessmentOutputTypeDef
        ],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EndpointOutputTypeDef = TypedDict(
    "EndpointOutputTypeDef",
    {
        "EndpointIdentifier": str,
        "EndpointType": ReplicationEndpointTypeValueType,
        "EngineName": str,
        "EngineDisplayName": str,
        "Username": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "ExtraConnectionAttributes": str,
        "Status": str,
        "KmsKeyId": str,
        "EndpointArn": str,
        "CertificateArn": str,
        "SslMode": DmsSslModeValueType,
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "ExternalId": str,
        "DynamoDbSettings": DynamoDbSettingsOutputTypeDef,
        "S3Settings": S3SettingsOutputTypeDef,
        "DmsTransferSettings": DmsTransferSettingsOutputTypeDef,
        "MongoDbSettings": MongoDbSettingsOutputTypeDef,
        "KinesisSettings": KinesisSettingsOutputTypeDef,
        "KafkaSettings": KafkaSettingsOutputTypeDef,
        "ElasticsearchSettings": ElasticsearchSettingsOutputTypeDef,
        "NeptuneSettings": NeptuneSettingsOutputTypeDef,
        "RedshiftSettings": RedshiftSettingsOutputTypeDef,
        "PostgreSQLSettings": PostgreSQLSettingsOutputTypeDef,
        "MySQLSettings": MySQLSettingsOutputTypeDef,
        "OracleSettings": OracleSettingsOutputTypeDef,
        "SybaseSettings": SybaseSettingsOutputTypeDef,
        "MicrosoftSQLServerSettings": MicrosoftSQLServerSettingsOutputTypeDef,
        "IBMDb2Settings": IBMDb2SettingsOutputTypeDef,
        "DocDbSettings": DocDbSettingsOutputTypeDef,
        "RedisSettings": RedisSettingsOutputTypeDef,
        "GcpMySQLSettings": GcpMySQLSettingsOutputTypeDef,
        "TimestreamSettings": TimestreamSettingsOutputTypeDef,
    },
)

ListTagsForResourceResponseOutputTypeDef = TypedDict(
    "ListTagsForResourceResponseOutputTypeDef",
    {
        "TagList": List[TagOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourcePendingMaintenanceActionsOutputTypeDef = TypedDict(
    "ResourcePendingMaintenanceActionsOutputTypeDef",
    {
        "ResourceIdentifier": str,
        "PendingMaintenanceActionDetails": List[PendingMaintenanceActionOutputTypeDef],
    },
)

RdsRecommendationOutputTypeDef = TypedDict(
    "RdsRecommendationOutputTypeDef",
    {
        "RequirementsToTarget": RdsRequirementsOutputTypeDef,
        "TargetConfiguration": RdsConfigurationOutputTypeDef,
    },
)

StartRecommendationsRequestEntryTypeDef = TypedDict(
    "StartRecommendationsRequestEntryTypeDef",
    {
        "DatabaseId": str,
        "Settings": RecommendationSettingsTypeDef,
    },
)

StartRecommendationsRequestRequestTypeDef = TypedDict(
    "StartRecommendationsRequestRequestTypeDef",
    {
        "DatabaseId": str,
        "Settings": RecommendationSettingsTypeDef,
    },
)

_RequiredReloadReplicationTablesMessageRequestTypeDef = TypedDict(
    "_RequiredReloadReplicationTablesMessageRequestTypeDef",
    {
        "ReplicationConfigArn": str,
        "TablesToReload": Sequence[TableToReloadTypeDef],
    },
)
_OptionalReloadReplicationTablesMessageRequestTypeDef = TypedDict(
    "_OptionalReloadReplicationTablesMessageRequestTypeDef",
    {
        "ReloadOption": ReloadOptionValueType,
    },
    total=False,
)


class ReloadReplicationTablesMessageRequestTypeDef(
    _RequiredReloadReplicationTablesMessageRequestTypeDef,
    _OptionalReloadReplicationTablesMessageRequestTypeDef,
):
    pass


_RequiredReloadTablesMessageRequestTypeDef = TypedDict(
    "_RequiredReloadTablesMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "TablesToReload": Sequence[TableToReloadTypeDef],
    },
)
_OptionalReloadTablesMessageRequestTypeDef = TypedDict(
    "_OptionalReloadTablesMessageRequestTypeDef",
    {
        "ReloadOption": ReloadOptionValueType,
    },
    total=False,
)


class ReloadTablesMessageRequestTypeDef(
    _RequiredReloadTablesMessageRequestTypeDef, _OptionalReloadTablesMessageRequestTypeDef
):
    pass


ReplicationOutputTypeDef = TypedDict(
    "ReplicationOutputTypeDef",
    {
        "ReplicationConfigIdentifier": str,
        "ReplicationConfigArn": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ReplicationType": MigrationTypeValueType,
        "Status": str,
        "ProvisionData": ProvisionDataOutputTypeDef,
        "StopReason": str,
        "FailureMessages": List[str],
        "ReplicationStats": ReplicationStatsOutputTypeDef,
        "StartReplicationType": str,
        "CdcStartTime": datetime,
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "RecoveryCheckpoint": str,
        "ReplicationCreateTime": datetime,
        "ReplicationUpdateTime": datetime,
        "ReplicationLastStopTime": datetime,
    },
)

ReplicationTaskAssessmentRunOutputTypeDef = TypedDict(
    "ReplicationTaskAssessmentRunOutputTypeDef",
    {
        "ReplicationTaskAssessmentRunArn": str,
        "ReplicationTaskArn": str,
        "Status": str,
        "ReplicationTaskAssessmentRunCreationDate": datetime,
        "AssessmentProgress": ReplicationTaskAssessmentRunProgressOutputTypeDef,
        "LastFailureMessage": str,
        "ServiceAccessRoleArn": str,
        "ResultLocationBucket": str,
        "ResultLocationFolder": str,
        "ResultEncryptionMode": str,
        "ResultKmsKeyArn": str,
        "AssessmentRunName": str,
    },
)

ReplicationTaskOutputTypeDef = TypedDict(
    "ReplicationTaskOutputTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ReplicationInstanceArn": str,
        "MigrationType": MigrationTypeValueType,
        "TableMappings": str,
        "ReplicationTaskSettings": str,
        "Status": str,
        "LastFailureMessage": str,
        "StopReason": str,
        "ReplicationTaskCreationDate": datetime,
        "ReplicationTaskStartDate": datetime,
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "RecoveryCheckpoint": str,
        "ReplicationTaskArn": str,
        "ReplicationTaskStats": ReplicationTaskStatsOutputTypeDef,
        "TaskData": str,
        "TargetReplicationInstanceArn": str,
    },
)

SchemaResponseOutputTypeDef = TypedDict(
    "SchemaResponseOutputTypeDef",
    {
        "CodeLineCount": int,
        "CodeSize": int,
        "Complexity": str,
        "Server": ServerShortInfoResponseOutputTypeDef,
        "DatabaseInstance": DatabaseShortInfoResponseOutputTypeDef,
        "SchemaId": str,
        "SchemaName": str,
        "OriginalSchema": SchemaShortInfoResponseOutputTypeDef,
        "Similarity": float,
    },
)

ReplicationSubnetGroupOutputTypeDef = TypedDict(
    "ReplicationSubnetGroupOutputTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
        "ReplicationSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[SubnetOutputTypeDef],
        "SupportedNetworkTypes": List[str],
    },
)

DescribeFleetAdvisorCollectorsResponseOutputTypeDef = TypedDict(
    "DescribeFleetAdvisorCollectorsResponseOutputTypeDef",
    {
        "Collectors": List[CollectorResponseOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateReplicationConfigResponseOutputTypeDef = TypedDict(
    "CreateReplicationConfigResponseOutputTypeDef",
    {
        "ReplicationConfig": ReplicationConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationConfigResponseOutputTypeDef = TypedDict(
    "DeleteReplicationConfigResponseOutputTypeDef",
    {
        "ReplicationConfig": ReplicationConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationConfigsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationConfigsResponseOutputTypeDef",
    {
        "Marker": str,
        "ReplicationConfigs": List[ReplicationConfigOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReplicationConfigResponseOutputTypeDef = TypedDict(
    "ModifyReplicationConfigResponseOutputTypeDef",
    {
        "ReplicationConfig": ReplicationConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorDatabasesResponseOutputTypeDef = TypedDict(
    "DescribeFleetAdvisorDatabasesResponseOutputTypeDef",
    {
        "Databases": List[DatabaseResponseOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEndpointResponseOutputTypeDef = TypedDict(
    "CreateEndpointResponseOutputTypeDef",
    {
        "Endpoint": EndpointOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEndpointResponseOutputTypeDef = TypedDict(
    "DeleteEndpointResponseOutputTypeDef",
    {
        "Endpoint": EndpointOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEndpointsResponseOutputTypeDef = TypedDict(
    "DescribeEndpointsResponseOutputTypeDef",
    {
        "Marker": str,
        "Endpoints": List[EndpointOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyEndpointResponseOutputTypeDef = TypedDict(
    "ModifyEndpointResponseOutputTypeDef",
    {
        "Endpoint": EndpointOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ApplyPendingMaintenanceActionResponseOutputTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionResponseOutputTypeDef",
    {
        "ResourcePendingMaintenanceActions": ResourcePendingMaintenanceActionsOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePendingMaintenanceActionsResponseOutputTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsResponseOutputTypeDef",
    {
        "PendingMaintenanceActions": List[ResourcePendingMaintenanceActionsOutputTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommendationDataOutputTypeDef = TypedDict(
    "RecommendationDataOutputTypeDef",
    {
        "RdsEngine": RdsRecommendationOutputTypeDef,
    },
)

BatchStartRecommendationsRequestRequestTypeDef = TypedDict(
    "BatchStartRecommendationsRequestRequestTypeDef",
    {
        "Data": Sequence[StartRecommendationsRequestEntryTypeDef],
    },
    total=False,
)

DescribeReplicationsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationsResponseOutputTypeDef",
    {
        "Marker": str,
        "Replications": List[ReplicationOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartReplicationResponseOutputTypeDef = TypedDict(
    "StartReplicationResponseOutputTypeDef",
    {
        "Replication": ReplicationOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopReplicationResponseOutputTypeDef = TypedDict(
    "StopReplicationResponseOutputTypeDef",
    {
        "Replication": ReplicationOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelReplicationTaskAssessmentRunResponseOutputTypeDef = TypedDict(
    "CancelReplicationTaskAssessmentRunResponseOutputTypeDef",
    {
        "ReplicationTaskAssessmentRun": ReplicationTaskAssessmentRunOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationTaskAssessmentRunResponseOutputTypeDef = TypedDict(
    "DeleteReplicationTaskAssessmentRunResponseOutputTypeDef",
    {
        "ReplicationTaskAssessmentRun": ReplicationTaskAssessmentRunOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTaskAssessmentRunsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentRunsResponseOutputTypeDef",
    {
        "Marker": str,
        "ReplicationTaskAssessmentRuns": List[ReplicationTaskAssessmentRunOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartReplicationTaskAssessmentRunResponseOutputTypeDef = TypedDict(
    "StartReplicationTaskAssessmentRunResponseOutputTypeDef",
    {
        "ReplicationTaskAssessmentRun": ReplicationTaskAssessmentRunOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateReplicationTaskResponseOutputTypeDef = TypedDict(
    "CreateReplicationTaskResponseOutputTypeDef",
    {
        "ReplicationTask": ReplicationTaskOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationTaskResponseOutputTypeDef = TypedDict(
    "DeleteReplicationTaskResponseOutputTypeDef",
    {
        "ReplicationTask": ReplicationTaskOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTasksResponseOutputTypeDef = TypedDict(
    "DescribeReplicationTasksResponseOutputTypeDef",
    {
        "Marker": str,
        "ReplicationTasks": List[ReplicationTaskOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReplicationTaskResponseOutputTypeDef = TypedDict(
    "ModifyReplicationTaskResponseOutputTypeDef",
    {
        "ReplicationTask": ReplicationTaskOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MoveReplicationTaskResponseOutputTypeDef = TypedDict(
    "MoveReplicationTaskResponseOutputTypeDef",
    {
        "ReplicationTask": ReplicationTaskOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartReplicationTaskAssessmentResponseOutputTypeDef = TypedDict(
    "StartReplicationTaskAssessmentResponseOutputTypeDef",
    {
        "ReplicationTask": ReplicationTaskOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartReplicationTaskResponseOutputTypeDef = TypedDict(
    "StartReplicationTaskResponseOutputTypeDef",
    {
        "ReplicationTask": ReplicationTaskOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopReplicationTaskResponseOutputTypeDef = TypedDict(
    "StopReplicationTaskResponseOutputTypeDef",
    {
        "ReplicationTask": ReplicationTaskOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorSchemasResponseOutputTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemasResponseOutputTypeDef",
    {
        "FleetAdvisorSchemas": List[SchemaResponseOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateReplicationSubnetGroupResponseOutputTypeDef = TypedDict(
    "CreateReplicationSubnetGroupResponseOutputTypeDef",
    {
        "ReplicationSubnetGroup": ReplicationSubnetGroupOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationSubnetGroupsResponseOutputTypeDef = TypedDict(
    "DescribeReplicationSubnetGroupsResponseOutputTypeDef",
    {
        "Marker": str,
        "ReplicationSubnetGroups": List[ReplicationSubnetGroupOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReplicationSubnetGroupResponseOutputTypeDef = TypedDict(
    "ModifyReplicationSubnetGroupResponseOutputTypeDef",
    {
        "ReplicationSubnetGroup": ReplicationSubnetGroupOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReplicationInstanceOutputTypeDef = TypedDict(
    "ReplicationInstanceOutputTypeDef",
    {
        "ReplicationInstanceIdentifier": str,
        "ReplicationInstanceClass": str,
        "ReplicationInstanceStatus": str,
        "AllocatedStorage": int,
        "InstanceCreateTime": datetime,
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipOutputTypeDef],
        "AvailabilityZone": str,
        "ReplicationSubnetGroup": ReplicationSubnetGroupOutputTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": ReplicationPendingModifiedValuesOutputTypeDef,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "KmsKeyId": str,
        "ReplicationInstanceArn": str,
        "ReplicationInstancePublicIpAddress": str,
        "ReplicationInstancePrivateIpAddress": str,
        "ReplicationInstancePublicIpAddresses": List[str],
        "ReplicationInstancePrivateIpAddresses": List[str],
        "ReplicationInstanceIpv6Addresses": List[str],
        "PubliclyAccessible": bool,
        "SecondaryAvailabilityZone": str,
        "FreeUntil": datetime,
        "DnsNameServers": str,
        "NetworkType": str,
    },
)

RecommendationOutputTypeDef = TypedDict(
    "RecommendationOutputTypeDef",
    {
        "DatabaseId": str,
        "EngineName": str,
        "CreatedDate": str,
        "Status": str,
        "Preferred": bool,
        "Settings": RecommendationSettingsOutputTypeDef,
        "Data": RecommendationDataOutputTypeDef,
    },
)

CreateReplicationInstanceResponseOutputTypeDef = TypedDict(
    "CreateReplicationInstanceResponseOutputTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationInstanceResponseOutputTypeDef = TypedDict(
    "DeleteReplicationInstanceResponseOutputTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationInstancesResponseOutputTypeDef = TypedDict(
    "DescribeReplicationInstancesResponseOutputTypeDef",
    {
        "Marker": str,
        "ReplicationInstances": List[ReplicationInstanceOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReplicationInstanceResponseOutputTypeDef = TypedDict(
    "ModifyReplicationInstanceResponseOutputTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RebootReplicationInstanceResponseOutputTypeDef = TypedDict(
    "RebootReplicationInstanceResponseOutputTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecommendationsResponseOutputTypeDef = TypedDict(
    "DescribeRecommendationsResponseOutputTypeDef",
    {
        "NextToken": str,
        "Recommendations": List[RecommendationOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
