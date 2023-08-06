"""
Type annotations for dms service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dms.client import DatabaseMigrationServiceClient

    session = Session()
    client: DatabaseMigrationServiceClient = session.client("dms")
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .literals import (
    DmsSslModeValueType,
    MigrationTypeValueType,
    ReloadOptionValueType,
    ReplicationEndpointTypeValueType,
    StartReplicationTaskTypeValueType,
)
from .paginator import (
    DescribeCertificatesPaginator,
    DescribeConnectionsPaginator,
    DescribeEndpointsPaginator,
    DescribeEndpointTypesPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeOrderableReplicationInstancesPaginator,
    DescribeReplicationInstancesPaginator,
    DescribeReplicationSubnetGroupsPaginator,
    DescribeReplicationTaskAssessmentResultsPaginator,
    DescribeReplicationTasksPaginator,
    DescribeSchemasPaginator,
    DescribeTableStatisticsPaginator,
)
from .type_defs import (
    ApplyPendingMaintenanceActionResponseOutputTypeDef,
    BatchStartRecommendationsResponseOutputTypeDef,
    CancelReplicationTaskAssessmentRunResponseOutputTypeDef,
    ComputeConfigTypeDef,
    CreateEndpointResponseOutputTypeDef,
    CreateEventSubscriptionResponseOutputTypeDef,
    CreateFleetAdvisorCollectorResponseOutputTypeDef,
    CreateReplicationConfigResponseOutputTypeDef,
    CreateReplicationInstanceResponseOutputTypeDef,
    CreateReplicationSubnetGroupResponseOutputTypeDef,
    CreateReplicationTaskResponseOutputTypeDef,
    DeleteCertificateResponseOutputTypeDef,
    DeleteConnectionResponseOutputTypeDef,
    DeleteEndpointResponseOutputTypeDef,
    DeleteEventSubscriptionResponseOutputTypeDef,
    DeleteFleetAdvisorDatabasesResponseOutputTypeDef,
    DeleteReplicationConfigResponseOutputTypeDef,
    DeleteReplicationInstanceResponseOutputTypeDef,
    DeleteReplicationTaskAssessmentRunResponseOutputTypeDef,
    DeleteReplicationTaskResponseOutputTypeDef,
    DescribeAccountAttributesResponseOutputTypeDef,
    DescribeApplicableIndividualAssessmentsResponseOutputTypeDef,
    DescribeCertificatesResponseOutputTypeDef,
    DescribeConnectionsResponseOutputTypeDef,
    DescribeEndpointSettingsResponseOutputTypeDef,
    DescribeEndpointsResponseOutputTypeDef,
    DescribeEndpointTypesResponseOutputTypeDef,
    DescribeEventCategoriesResponseOutputTypeDef,
    DescribeEventsResponseOutputTypeDef,
    DescribeEventSubscriptionsResponseOutputTypeDef,
    DescribeFleetAdvisorCollectorsResponseOutputTypeDef,
    DescribeFleetAdvisorDatabasesResponseOutputTypeDef,
    DescribeFleetAdvisorLsaAnalysisResponseOutputTypeDef,
    DescribeFleetAdvisorSchemaObjectSummaryResponseOutputTypeDef,
    DescribeFleetAdvisorSchemasResponseOutputTypeDef,
    DescribeOrderableReplicationInstancesResponseOutputTypeDef,
    DescribePendingMaintenanceActionsResponseOutputTypeDef,
    DescribeRecommendationLimitationsResponseOutputTypeDef,
    DescribeRecommendationsResponseOutputTypeDef,
    DescribeRefreshSchemasStatusResponseOutputTypeDef,
    DescribeReplicationConfigsResponseOutputTypeDef,
    DescribeReplicationInstancesResponseOutputTypeDef,
    DescribeReplicationInstanceTaskLogsResponseOutputTypeDef,
    DescribeReplicationsResponseOutputTypeDef,
    DescribeReplicationSubnetGroupsResponseOutputTypeDef,
    DescribeReplicationTableStatisticsResponseOutputTypeDef,
    DescribeReplicationTaskAssessmentResultsResponseOutputTypeDef,
    DescribeReplicationTaskAssessmentRunsResponseOutputTypeDef,
    DescribeReplicationTaskIndividualAssessmentsResponseOutputTypeDef,
    DescribeReplicationTasksResponseOutputTypeDef,
    DescribeSchemasResponseOutputTypeDef,
    DescribeTableStatisticsResponseOutputTypeDef,
    DmsTransferSettingsTypeDef,
    DocDbSettingsTypeDef,
    DynamoDbSettingsTypeDef,
    ElasticsearchSettingsTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterTypeDef,
    GcpMySQLSettingsTypeDef,
    IBMDb2SettingsTypeDef,
    ImportCertificateResponseOutputTypeDef,
    KafkaSettingsTypeDef,
    KinesisSettingsTypeDef,
    ListTagsForResourceResponseOutputTypeDef,
    MicrosoftSQLServerSettingsTypeDef,
    ModifyEndpointResponseOutputTypeDef,
    ModifyEventSubscriptionResponseOutputTypeDef,
    ModifyReplicationConfigResponseOutputTypeDef,
    ModifyReplicationInstanceResponseOutputTypeDef,
    ModifyReplicationSubnetGroupResponseOutputTypeDef,
    ModifyReplicationTaskResponseOutputTypeDef,
    MongoDbSettingsTypeDef,
    MoveReplicationTaskResponseOutputTypeDef,
    MySQLSettingsTypeDef,
    NeptuneSettingsTypeDef,
    OracleSettingsTypeDef,
    PostgreSQLSettingsTypeDef,
    RebootReplicationInstanceResponseOutputTypeDef,
    RecommendationSettingsTypeDef,
    RedisSettingsTypeDef,
    RedshiftSettingsTypeDef,
    RefreshSchemasResponseOutputTypeDef,
    ReloadReplicationTablesResponseOutputTypeDef,
    ReloadTablesResponseOutputTypeDef,
    RunFleetAdvisorLsaAnalysisResponseOutputTypeDef,
    S3SettingsTypeDef,
    StartRecommendationsRequestEntryTypeDef,
    StartReplicationResponseOutputTypeDef,
    StartReplicationTaskAssessmentResponseOutputTypeDef,
    StartReplicationTaskAssessmentRunResponseOutputTypeDef,
    StartReplicationTaskResponseOutputTypeDef,
    StopReplicationResponseOutputTypeDef,
    StopReplicationTaskResponseOutputTypeDef,
    SybaseSettingsTypeDef,
    TableToReloadTypeDef,
    TagTypeDef,
    TestConnectionResponseOutputTypeDef,
    TimestreamSettingsTypeDef,
    UpdateSubscriptionsToEventBridgeResponseOutputTypeDef,
)
from .waiter import (
    EndpointDeletedWaiter,
    ReplicationInstanceAvailableWaiter,
    ReplicationInstanceDeletedWaiter,
    ReplicationTaskDeletedWaiter,
    ReplicationTaskReadyWaiter,
    ReplicationTaskRunningWaiter,
    ReplicationTaskStoppedWaiter,
    TestConnectionSucceedsWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DatabaseMigrationServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CollectorNotFoundFault: Type[BotocoreClientError]
    InsufficientResourceCapacityFault: Type[BotocoreClientError]
    InvalidCertificateFault: Type[BotocoreClientError]
    InvalidOperationFault: Type[BotocoreClientError]
    InvalidResourceStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    KMSAccessDeniedFault: Type[BotocoreClientError]
    KMSDisabledFault: Type[BotocoreClientError]
    KMSFault: Type[BotocoreClientError]
    KMSInvalidStateFault: Type[BotocoreClientError]
    KMSKeyNotAccessibleFault: Type[BotocoreClientError]
    KMSNotFoundFault: Type[BotocoreClientError]
    KMSThrottlingFault: Type[BotocoreClientError]
    ReplicationSubnetGroupDoesNotCoverEnoughAZs: Type[BotocoreClientError]
    ResourceAlreadyExistsFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    ResourceQuotaExceededFault: Type[BotocoreClientError]
    S3AccessDeniedFault: Type[BotocoreClientError]
    S3ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    StorageQuotaExceededFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    UpgradeDependencyFailureFault: Type[BotocoreClientError]


class DatabaseMigrationServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DatabaseMigrationServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#exceptions)
        """

    def add_tags_to_resource(
        self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds metadata tags to an DMS resource, including replication instance, endpoint,
        subnet group, and migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.add_tags_to_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#add_tags_to_resource)
        """

    def apply_pending_maintenance_action(
        self, *, ReplicationInstanceArn: str, ApplyAction: str, OptInType: str
    ) -> ApplyPendingMaintenanceActionResponseOutputTypeDef:
        """
        Applies a pending maintenance action to a resource (for example, to a
        replication instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.apply_pending_maintenance_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#apply_pending_maintenance_action)
        """

    def batch_start_recommendations(
        self, *, Data: Sequence[StartRecommendationsRequestEntryTypeDef] = ...
    ) -> BatchStartRecommendationsResponseOutputTypeDef:
        """
        Starts the analysis of up to 20 source databases to recommend target engines for
        each source database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.batch_start_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#batch_start_recommendations)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#can_paginate)
        """

    def cancel_replication_task_assessment_run(
        self, *, ReplicationTaskAssessmentRunArn: str
    ) -> CancelReplicationTaskAssessmentRunResponseOutputTypeDef:
        """
        Cancels a single premigration assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.cancel_replication_task_assessment_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#cancel_replication_task_assessment_run)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#close)
        """

    def create_endpoint(
        self,
        *,
        EndpointIdentifier: str,
        EndpointType: ReplicationEndpointTypeValueType,
        EngineName: str,
        Username: str = ...,
        Password: str = ...,
        ServerName: str = ...,
        Port: int = ...,
        DatabaseName: str = ...,
        ExtraConnectionAttributes: str = ...,
        KmsKeyId: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        CertificateArn: str = ...,
        SslMode: DmsSslModeValueType = ...,
        ServiceAccessRoleArn: str = ...,
        ExternalTableDefinition: str = ...,
        DynamoDbSettings: DynamoDbSettingsTypeDef = ...,
        S3Settings: S3SettingsTypeDef = ...,
        DmsTransferSettings: DmsTransferSettingsTypeDef = ...,
        MongoDbSettings: MongoDbSettingsTypeDef = ...,
        KinesisSettings: KinesisSettingsTypeDef = ...,
        KafkaSettings: KafkaSettingsTypeDef = ...,
        ElasticsearchSettings: ElasticsearchSettingsTypeDef = ...,
        NeptuneSettings: NeptuneSettingsTypeDef = ...,
        RedshiftSettings: RedshiftSettingsTypeDef = ...,
        PostgreSQLSettings: PostgreSQLSettingsTypeDef = ...,
        MySQLSettings: MySQLSettingsTypeDef = ...,
        OracleSettings: OracleSettingsTypeDef = ...,
        SybaseSettings: SybaseSettingsTypeDef = ...,
        MicrosoftSQLServerSettings: MicrosoftSQLServerSettingsTypeDef = ...,
        IBMDb2Settings: IBMDb2SettingsTypeDef = ...,
        ResourceIdentifier: str = ...,
        DocDbSettings: DocDbSettingsTypeDef = ...,
        RedisSettings: RedisSettingsTypeDef = ...,
        GcpMySQLSettings: GcpMySQLSettingsTypeDef = ...,
        TimestreamSettings: TimestreamSettingsTypeDef = ...
    ) -> CreateEndpointResponseOutputTypeDef:
        """
        Creates an endpoint using the provided settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.create_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_endpoint)
        """

    def create_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        SourceIds: Sequence[str] = ...,
        Enabled: bool = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateEventSubscriptionResponseOutputTypeDef:
        """
        Creates an DMS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.create_event_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_event_subscription)
        """

    def create_fleet_advisor_collector(
        self,
        *,
        CollectorName: str,
        ServiceAccessRoleArn: str,
        S3BucketName: str,
        Description: str = ...
    ) -> CreateFleetAdvisorCollectorResponseOutputTypeDef:
        """
        Creates a Fleet Advisor collector using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.create_fleet_advisor_collector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_fleet_advisor_collector)
        """

    def create_replication_config(
        self,
        *,
        ReplicationConfigIdentifier: str,
        SourceEndpointArn: str,
        TargetEndpointArn: str,
        ComputeConfig: ComputeConfigTypeDef,
        ReplicationType: MigrationTypeValueType,
        TableMappings: str,
        ReplicationSettings: str = ...,
        SupplementalSettings: str = ...,
        ResourceIdentifier: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateReplicationConfigResponseOutputTypeDef:
        """
        Creates a configuration that you can later provide to configure and start an DMS
        Serverless replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.create_replication_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_config)
        """

    def create_replication_instance(
        self,
        *,
        ReplicationInstanceIdentifier: str,
        ReplicationInstanceClass: str,
        AllocatedStorage: int = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        AvailabilityZone: str = ...,
        ReplicationSubnetGroupIdentifier: str = ...,
        PreferredMaintenanceWindow: str = ...,
        MultiAZ: bool = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
        KmsKeyId: str = ...,
        PubliclyAccessible: bool = ...,
        DnsNameServers: str = ...,
        ResourceIdentifier: str = ...,
        NetworkType: str = ...
    ) -> CreateReplicationInstanceResponseOutputTypeDef:
        """
        Creates the replication instance using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.create_replication_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_instance)
        """

    def create_replication_subnet_group(
        self,
        *,
        ReplicationSubnetGroupIdentifier: str,
        ReplicationSubnetGroupDescription: str,
        SubnetIds: Sequence[str],
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateReplicationSubnetGroupResponseOutputTypeDef:
        """
        Creates a replication subnet group given a list of the subnet IDs in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.create_replication_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_subnet_group)
        """

    def create_replication_task(
        self,
        *,
        ReplicationTaskIdentifier: str,
        SourceEndpointArn: str,
        TargetEndpointArn: str,
        ReplicationInstanceArn: str,
        MigrationType: MigrationTypeValueType,
        TableMappings: str,
        ReplicationTaskSettings: str = ...,
        CdcStartTime: Union[datetime, str] = ...,
        CdcStartPosition: str = ...,
        CdcStopPosition: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        TaskData: str = ...,
        ResourceIdentifier: str = ...
    ) -> CreateReplicationTaskResponseOutputTypeDef:
        """
        Creates a replication task using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.create_replication_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_task)
        """

    def delete_certificate(self, *, CertificateArn: str) -> DeleteCertificateResponseOutputTypeDef:
        """
        Deletes the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_certificate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_certificate)
        """

    def delete_connection(
        self, *, EndpointArn: str, ReplicationInstanceArn: str
    ) -> DeleteConnectionResponseOutputTypeDef:
        """
        Deletes the connection between a replication instance and an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_connection)
        """

    def delete_endpoint(self, *, EndpointArn: str) -> DeleteEndpointResponseOutputTypeDef:
        """
        Deletes the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_endpoint)
        """

    def delete_event_subscription(
        self, *, SubscriptionName: str
    ) -> DeleteEventSubscriptionResponseOutputTypeDef:
        """
        Deletes an DMS event subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_event_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_event_subscription)
        """

    def delete_fleet_advisor_collector(
        self, *, CollectorReferencedId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Fleet Advisor collector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_fleet_advisor_collector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_fleet_advisor_collector)
        """

    def delete_fleet_advisor_databases(
        self, *, DatabaseIds: Sequence[str]
    ) -> DeleteFleetAdvisorDatabasesResponseOutputTypeDef:
        """
        Deletes the specified Fleet Advisor collector databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_fleet_advisor_databases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_fleet_advisor_databases)
        """

    def delete_replication_config(
        self, *, ReplicationConfigArn: str
    ) -> DeleteReplicationConfigResponseOutputTypeDef:
        """
        Deletes an DMS Serverless replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_replication_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_config)
        """

    def delete_replication_instance(
        self, *, ReplicationInstanceArn: str
    ) -> DeleteReplicationInstanceResponseOutputTypeDef:
        """
        Deletes the specified replication instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_replication_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_instance)
        """

    def delete_replication_subnet_group(
        self, *, ReplicationSubnetGroupIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_replication_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_subnet_group)
        """

    def delete_replication_task(
        self, *, ReplicationTaskArn: str
    ) -> DeleteReplicationTaskResponseOutputTypeDef:
        """
        Deletes the specified replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_replication_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_task)
        """

    def delete_replication_task_assessment_run(
        self, *, ReplicationTaskAssessmentRunArn: str
    ) -> DeleteReplicationTaskAssessmentRunResponseOutputTypeDef:
        """
        Deletes the record of a single premigration assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.delete_replication_task_assessment_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_task_assessment_run)
        """

    def describe_account_attributes(self) -> DescribeAccountAttributesResponseOutputTypeDef:
        """
        Lists all of the DMS attributes for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_account_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_account_attributes)
        """

    def describe_applicable_individual_assessments(
        self,
        *,
        ReplicationTaskArn: str = ...,
        ReplicationInstanceArn: str = ...,
        SourceEngineName: str = ...,
        TargetEngineName: str = ...,
        MigrationType: MigrationTypeValueType = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeApplicableIndividualAssessmentsResponseOutputTypeDef:
        """
        Provides a list of individual assessments that you can specify for a new
        premigration assessment run, given one or more parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_applicable_individual_assessments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_applicable_individual_assessments)
        """

    def describe_certificates(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeCertificatesResponseOutputTypeDef:
        """
        Provides a description of the certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_certificates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_certificates)
        """

    def describe_connections(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeConnectionsResponseOutputTypeDef:
        """
        Describes the status of the connections that have been made between the
        replication instance and an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_connections)
        """

    def describe_endpoint_settings(
        self, *, EngineName: str, MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeEndpointSettingsResponseOutputTypeDef:
        """
        Returns information about the possible endpoint settings available when you
        create an endpoint for a specific database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_endpoint_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_endpoint_settings)
        """

    def describe_endpoint_types(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeEndpointTypesResponseOutputTypeDef:
        """
        Returns information about the type of endpoints available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_endpoint_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_endpoint_types)
        """

    def describe_endpoints(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeEndpointsResponseOutputTypeDef:
        """
        Returns information about the endpoints for your account in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_endpoints)
        """

    def describe_event_categories(
        self, *, SourceType: str = ..., Filters: Sequence[FilterTypeDef] = ...
    ) -> DescribeEventCategoriesResponseOutputTypeDef:
        """
        Lists categories for all event source types, or, if specified, for a specified
        source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_event_categories)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_event_categories)
        """

    def describe_event_subscriptions(
        self,
        *,
        SubscriptionName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeEventSubscriptionsResponseOutputTypeDef:
        """
        Lists all the event subscriptions for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_event_subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_event_subscriptions)
        """

    def describe_events(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: Literal["replication-instance"] = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        EventCategories: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeEventsResponseOutputTypeDef:
        """
        Lists events for a given source identifier and source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_events)
        """

    def describe_fleet_advisor_collectors(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeFleetAdvisorCollectorsResponseOutputTypeDef:
        """
        Returns a list of the Fleet Advisor collectors in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_fleet_advisor_collectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_collectors)
        """

    def describe_fleet_advisor_databases(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeFleetAdvisorDatabasesResponseOutputTypeDef:
        """
        Returns a list of Fleet Advisor databases in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_fleet_advisor_databases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_databases)
        """

    def describe_fleet_advisor_lsa_analysis(
        self, *, MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeFleetAdvisorLsaAnalysisResponseOutputTypeDef:
        """
        Provides descriptions of large-scale assessment (LSA) analyses produced by your
        Fleet Advisor collectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_fleet_advisor_lsa_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_lsa_analysis)
        """

    def describe_fleet_advisor_schema_object_summary(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeFleetAdvisorSchemaObjectSummaryResponseOutputTypeDef:
        """
        Provides descriptions of the schemas discovered by your Fleet Advisor
        collectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_fleet_advisor_schema_object_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_schema_object_summary)
        """

    def describe_fleet_advisor_schemas(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeFleetAdvisorSchemasResponseOutputTypeDef:
        """
        Returns a list of schemas detected by Fleet Advisor Collectors in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_fleet_advisor_schemas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_schemas)
        """

    def describe_orderable_replication_instances(
        self, *, MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeOrderableReplicationInstancesResponseOutputTypeDef:
        """
        Returns information about the replication instance types that can be created in
        the specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_orderable_replication_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_orderable_replication_instances)
        """

    def describe_pending_maintenance_actions(
        self,
        *,
        ReplicationInstanceArn: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> DescribePendingMaintenanceActionsResponseOutputTypeDef:
        """
        For internal use only See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribePendingMaintenanceActions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_pending_maintenance_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_pending_maintenance_actions)
        """

    def describe_recommendation_limitations(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeRecommendationLimitationsResponseOutputTypeDef:
        """
        Returns a paginated list of limitations for recommendations of target Amazon Web
        Services engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_recommendation_limitations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_recommendation_limitations)
        """

    def describe_recommendations(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeRecommendationsResponseOutputTypeDef:
        """
        Returns a paginated list of target engine recommendations for your source
        databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_recommendations)
        """

    def describe_refresh_schemas_status(
        self, *, EndpointArn: str
    ) -> DescribeRefreshSchemasStatusResponseOutputTypeDef:
        """
        Returns the status of the RefreshSchemas operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_refresh_schemas_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_refresh_schemas_status)
        """

    def describe_replication_configs(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationConfigsResponseOutputTypeDef:
        """
        Returns one or more existing DMS Serverless replication configurations as a list
        of structures.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_configs)
        """

    def describe_replication_instance_task_logs(
        self, *, ReplicationInstanceArn: str, MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationInstanceTaskLogsResponseOutputTypeDef:
        """
        Returns information about the task logs for the specified task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_instance_task_logs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_instance_task_logs)
        """

    def describe_replication_instances(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationInstancesResponseOutputTypeDef:
        """
        Returns information about replication instances for your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_instances)
        """

    def describe_replication_subnet_groups(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationSubnetGroupsResponseOutputTypeDef:
        """
        Returns information about the replication subnet groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_subnet_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_subnet_groups)
        """

    def describe_replication_table_statistics(
        self,
        *,
        ReplicationConfigArn: str,
        MaxRecords: int = ...,
        Marker: str = ...,
        Filters: Sequence[FilterTypeDef] = ...
    ) -> DescribeReplicationTableStatisticsResponseOutputTypeDef:
        """
        Returns table and schema statistics for one or more provisioned replications
        that use a given DMS Serverless replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_table_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_table_statistics)
        """

    def describe_replication_task_assessment_results(
        self, *, ReplicationTaskArn: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationTaskAssessmentResultsResponseOutputTypeDef:
        """
        Returns the task assessment results from the Amazon S3 bucket that DMS creates
        in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_task_assessment_results)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_task_assessment_results)
        """

    def describe_replication_task_assessment_runs(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationTaskAssessmentRunsResponseOutputTypeDef:
        """
        Returns a paginated list of premigration assessment runs based on filter
        settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_task_assessment_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_task_assessment_runs)
        """

    def describe_replication_task_individual_assessments(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationTaskIndividualAssessmentsResponseOutputTypeDef:
        """
        Returns a paginated list of individual assessments based on filter settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_task_individual_assessments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_task_individual_assessments)
        """

    def describe_replication_tasks(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WithoutSettings: bool = ...
    ) -> DescribeReplicationTasksResponseOutputTypeDef:
        """
        Returns information about replication tasks for your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replication_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_tasks)
        """

    def describe_replications(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeReplicationsResponseOutputTypeDef:
        """
        Provides details on replication progress by returning status information for one
        or more provisioned DMS Serverless replications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_replications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replications)
        """

    def describe_schemas(
        self, *, EndpointArn: str, MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeSchemasResponseOutputTypeDef:
        """
        Returns information about the schema for the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_schemas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_schemas)
        """

    def describe_table_statistics(
        self,
        *,
        ReplicationTaskArn: str,
        MaxRecords: int = ...,
        Marker: str = ...,
        Filters: Sequence[FilterTypeDef] = ...
    ) -> DescribeTableStatisticsResponseOutputTypeDef:
        """
        Returns table statistics on the database migration task, including table name,
        rows inserted, rows updated, and rows deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.describe_table_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_table_statistics)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#generate_presigned_url)
        """

    def import_certificate(
        self,
        *,
        CertificateIdentifier: str,
        CertificatePem: str = ...,
        CertificateWallet: Union[str, bytes, IO[Any], StreamingBody] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> ImportCertificateResponseOutputTypeDef:
        """
        Uploads the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.import_certificate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#import_certificate)
        """

    def list_tags_for_resource(
        self, *, ResourceArn: str = ..., ResourceArnList: Sequence[str] = ...
    ) -> ListTagsForResourceResponseOutputTypeDef:
        """
        Lists all metadata tags attached to an DMS resource, including replication
        instance, endpoint, subnet group, and migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#list_tags_for_resource)
        """

    def modify_endpoint(
        self,
        *,
        EndpointArn: str,
        EndpointIdentifier: str = ...,
        EndpointType: ReplicationEndpointTypeValueType = ...,
        EngineName: str = ...,
        Username: str = ...,
        Password: str = ...,
        ServerName: str = ...,
        Port: int = ...,
        DatabaseName: str = ...,
        ExtraConnectionAttributes: str = ...,
        CertificateArn: str = ...,
        SslMode: DmsSslModeValueType = ...,
        ServiceAccessRoleArn: str = ...,
        ExternalTableDefinition: str = ...,
        DynamoDbSettings: DynamoDbSettingsTypeDef = ...,
        S3Settings: S3SettingsTypeDef = ...,
        DmsTransferSettings: DmsTransferSettingsTypeDef = ...,
        MongoDbSettings: MongoDbSettingsTypeDef = ...,
        KinesisSettings: KinesisSettingsTypeDef = ...,
        KafkaSettings: KafkaSettingsTypeDef = ...,
        ElasticsearchSettings: ElasticsearchSettingsTypeDef = ...,
        NeptuneSettings: NeptuneSettingsTypeDef = ...,
        RedshiftSettings: RedshiftSettingsTypeDef = ...,
        PostgreSQLSettings: PostgreSQLSettingsTypeDef = ...,
        MySQLSettings: MySQLSettingsTypeDef = ...,
        OracleSettings: OracleSettingsTypeDef = ...,
        SybaseSettings: SybaseSettingsTypeDef = ...,
        MicrosoftSQLServerSettings: MicrosoftSQLServerSettingsTypeDef = ...,
        IBMDb2Settings: IBMDb2SettingsTypeDef = ...,
        DocDbSettings: DocDbSettingsTypeDef = ...,
        RedisSettings: RedisSettingsTypeDef = ...,
        ExactSettings: bool = ...,
        GcpMySQLSettings: GcpMySQLSettingsTypeDef = ...,
        TimestreamSettings: TimestreamSettingsTypeDef = ...
    ) -> ModifyEndpointResponseOutputTypeDef:
        """
        Modifies the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.modify_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_endpoint)
        """

    def modify_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str = ...,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        Enabled: bool = ...
    ) -> ModifyEventSubscriptionResponseOutputTypeDef:
        """
        Modifies an existing DMS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.modify_event_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_event_subscription)
        """

    def modify_replication_config(
        self,
        *,
        ReplicationConfigArn: str,
        ReplicationConfigIdentifier: str = ...,
        ReplicationType: MigrationTypeValueType = ...,
        TableMappings: str = ...,
        ReplicationSettings: str = ...,
        SupplementalSettings: str = ...,
        ComputeConfig: ComputeConfigTypeDef = ...,
        SourceEndpointArn: str = ...,
        TargetEndpointArn: str = ...
    ) -> ModifyReplicationConfigResponseOutputTypeDef:
        """
        Modifies an existing DMS Serverless replication configuration that you can use
        to start a replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.modify_replication_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_config)
        """

    def modify_replication_instance(
        self,
        *,
        ReplicationInstanceArn: str,
        AllocatedStorage: int = ...,
        ApplyImmediately: bool = ...,
        ReplicationInstanceClass: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        PreferredMaintenanceWindow: str = ...,
        MultiAZ: bool = ...,
        EngineVersion: str = ...,
        AllowMajorVersionUpgrade: bool = ...,
        AutoMinorVersionUpgrade: bool = ...,
        ReplicationInstanceIdentifier: str = ...,
        NetworkType: str = ...
    ) -> ModifyReplicationInstanceResponseOutputTypeDef:
        """
        Modifies the replication instance to apply new settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.modify_replication_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_instance)
        """

    def modify_replication_subnet_group(
        self,
        *,
        ReplicationSubnetGroupIdentifier: str,
        SubnetIds: Sequence[str],
        ReplicationSubnetGroupDescription: str = ...
    ) -> ModifyReplicationSubnetGroupResponseOutputTypeDef:
        """
        Modifies the settings for the specified replication subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.modify_replication_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_subnet_group)
        """

    def modify_replication_task(
        self,
        *,
        ReplicationTaskArn: str,
        ReplicationTaskIdentifier: str = ...,
        MigrationType: MigrationTypeValueType = ...,
        TableMappings: str = ...,
        ReplicationTaskSettings: str = ...,
        CdcStartTime: Union[datetime, str] = ...,
        CdcStartPosition: str = ...,
        CdcStopPosition: str = ...,
        TaskData: str = ...
    ) -> ModifyReplicationTaskResponseOutputTypeDef:
        """
        Modifies the specified replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.modify_replication_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_task)
        """

    def move_replication_task(
        self, *, ReplicationTaskArn: str, TargetReplicationInstanceArn: str
    ) -> MoveReplicationTaskResponseOutputTypeDef:
        """
        Moves a replication task from its current replication instance to a different
        target replication instance using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.move_replication_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#move_replication_task)
        """

    def reboot_replication_instance(
        self,
        *,
        ReplicationInstanceArn: str,
        ForceFailover: bool = ...,
        ForcePlannedFailover: bool = ...
    ) -> RebootReplicationInstanceResponseOutputTypeDef:
        """
        Reboots a replication instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.reboot_replication_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#reboot_replication_instance)
        """

    def refresh_schemas(
        self, *, EndpointArn: str, ReplicationInstanceArn: str
    ) -> RefreshSchemasResponseOutputTypeDef:
        """
        Populates the schema for the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.refresh_schemas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#refresh_schemas)
        """

    def reload_replication_tables(
        self,
        *,
        ReplicationConfigArn: str,
        TablesToReload: Sequence[TableToReloadTypeDef],
        ReloadOption: ReloadOptionValueType = ...
    ) -> ReloadReplicationTablesResponseOutputTypeDef:
        """
        Reloads the target database table with the source data for a given DMS
        Serverless replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.reload_replication_tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#reload_replication_tables)
        """

    def reload_tables(
        self,
        *,
        ReplicationTaskArn: str,
        TablesToReload: Sequence[TableToReloadTypeDef],
        ReloadOption: ReloadOptionValueType = ...
    ) -> ReloadTablesResponseOutputTypeDef:
        """
        Reloads the target database table with the source data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.reload_tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#reload_tables)
        """

    def remove_tags_from_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Removes metadata tags from an DMS resource, including replication instance,
        endpoint, subnet group, and migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.remove_tags_from_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#remove_tags_from_resource)
        """

    def run_fleet_advisor_lsa_analysis(self) -> RunFleetAdvisorLsaAnalysisResponseOutputTypeDef:
        """
        Runs large-scale assessment (LSA) analysis on every Fleet Advisor collector in
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.run_fleet_advisor_lsa_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#run_fleet_advisor_lsa_analysis)
        """

    def start_recommendations(
        self, *, DatabaseId: str, Settings: RecommendationSettingsTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts the analysis of your source database to provide recommendations of target
        engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.start_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_recommendations)
        """

    def start_replication(
        self,
        *,
        ReplicationConfigArn: str,
        StartReplicationType: str,
        CdcStartTime: Union[datetime, str] = ...,
        CdcStartPosition: str = ...,
        CdcStopPosition: str = ...
    ) -> StartReplicationResponseOutputTypeDef:
        """
        For a given DMS Serverless replication configuration, DMS connects to the source
        endpoint and collects the metadata to analyze the replication workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.start_replication)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication)
        """

    def start_replication_task(
        self,
        *,
        ReplicationTaskArn: str,
        StartReplicationTaskType: StartReplicationTaskTypeValueType,
        CdcStartTime: Union[datetime, str] = ...,
        CdcStartPosition: str = ...,
        CdcStopPosition: str = ...
    ) -> StartReplicationTaskResponseOutputTypeDef:
        """
        Starts the replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.start_replication_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication_task)
        """

    def start_replication_task_assessment(
        self, *, ReplicationTaskArn: str
    ) -> StartReplicationTaskAssessmentResponseOutputTypeDef:
        """
        Starts the replication task assessment for unsupported data types in the source
        database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.start_replication_task_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication_task_assessment)
        """

    def start_replication_task_assessment_run(
        self,
        *,
        ReplicationTaskArn: str,
        ServiceAccessRoleArn: str,
        ResultLocationBucket: str,
        AssessmentRunName: str,
        ResultLocationFolder: str = ...,
        ResultEncryptionMode: str = ...,
        ResultKmsKeyArn: str = ...,
        IncludeOnly: Sequence[str] = ...,
        Exclude: Sequence[str] = ...
    ) -> StartReplicationTaskAssessmentRunResponseOutputTypeDef:
        """
        Starts a new premigration assessment run for one or more individual assessments
        of a migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.start_replication_task_assessment_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication_task_assessment_run)
        """

    def stop_replication(
        self, *, ReplicationConfigArn: str
    ) -> StopReplicationResponseOutputTypeDef:
        """
        For a given DMS Serverless replication configuration, DMS stops any and all
        ongoing DMS Serverless replications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.stop_replication)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#stop_replication)
        """

    def stop_replication_task(
        self, *, ReplicationTaskArn: str
    ) -> StopReplicationTaskResponseOutputTypeDef:
        """
        Stops the replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.stop_replication_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#stop_replication_task)
        """

    def test_connection(
        self, *, ReplicationInstanceArn: str, EndpointArn: str
    ) -> TestConnectionResponseOutputTypeDef:
        """
        Tests the connection between the replication instance and the endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.test_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#test_connection)
        """

    def update_subscriptions_to_event_bridge(
        self, *, ForceMove: bool = ...
    ) -> UpdateSubscriptionsToEventBridgeResponseOutputTypeDef:
        """
        Migrates 10 active and enabled Amazon SNS subscriptions at a time and converts
        them to corresponding Amazon EventBridge rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.update_subscriptions_to_event_bridge)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#update_subscriptions_to_event_bridge)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_certificates"]
    ) -> DescribeCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_connections"]
    ) -> DescribeConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoint_types"]
    ) -> DescribeEndpointTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoints"]
    ) -> DescribeEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_replication_instances"]
    ) -> DescribeOrderableReplicationInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_instances"]
    ) -> DescribeReplicationInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_subnet_groups"]
    ) -> DescribeReplicationSubnetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_task_assessment_results"]
    ) -> DescribeReplicationTaskAssessmentResultsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_tasks"]
    ) -> DescribeReplicationTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_schemas"]
    ) -> DescribeSchemasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_table_statistics"]
    ) -> DescribeTableStatisticsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["endpoint_deleted"]) -> EndpointDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_instance_available"]
    ) -> ReplicationInstanceAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_instance_deleted"]
    ) -> ReplicationInstanceDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_deleted"]
    ) -> ReplicationTaskDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_ready"]
    ) -> ReplicationTaskReadyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_running"]
    ) -> ReplicationTaskRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_stopped"]
    ) -> ReplicationTaskStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["test_connection_succeeds"]
    ) -> TestConnectionSucceedsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """
