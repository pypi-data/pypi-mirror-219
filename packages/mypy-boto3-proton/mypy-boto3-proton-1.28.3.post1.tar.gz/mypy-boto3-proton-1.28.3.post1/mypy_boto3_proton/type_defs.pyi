"""
Type annotations for proton service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/type_defs/)

Usage::

    ```python
    from mypy_boto3_proton.type_defs import AcceptEnvironmentAccountConnectionInputRequestTypeDef

    data: AcceptEnvironmentAccountConnectionInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    BlockerStatusType,
    ComponentDeploymentUpdateTypeType,
    DeploymentStatusType,
    DeploymentTargetResourceTypeType,
    DeploymentUpdateTypeType,
    EnvironmentAccountConnectionRequesterAccountTypeType,
    EnvironmentAccountConnectionStatusType,
    ListServiceInstancesFilterByType,
    ListServiceInstancesSortByType,
    ProvisionedResourceEngineType,
    RepositoryProviderType,
    RepositorySyncStatusType,
    ResourceDeploymentStatusType,
    ResourceSyncStatusType,
    ServiceStatusType,
    SortOrderType,
    SyncTypeType,
    TemplateTypeType,
    TemplateVersionStatusType,
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
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    "EnvironmentAccountConnectionOutputTypeDef",
    "RepositoryBranchOutputTypeDef",
    "CancelComponentDeploymentInputRequestTypeDef",
    "ComponentOutputTypeDef",
    "CancelEnvironmentDeploymentInputRequestTypeDef",
    "CancelServiceInstanceDeploymentInputRequestTypeDef",
    "ServiceInstanceOutputTypeDef",
    "CancelServicePipelineDeploymentInputRequestTypeDef",
    "ServicePipelineOutputTypeDef",
    "CompatibleEnvironmentTemplateInputTypeDef",
    "CompatibleEnvironmentTemplateOutputTypeDef",
    "ComponentStateOutputTypeDef",
    "ComponentSummaryOutputTypeDef",
    "ResourceCountsSummaryOutputTypeDef",
    "TagTypeDef",
    "RepositoryBranchInputTypeDef",
    "EnvironmentTemplateOutputTypeDef",
    "EnvironmentTemplateVersionOutputTypeDef",
    "RepositoryOutputTypeDef",
    "CreateServiceSyncConfigInputRequestTypeDef",
    "ServiceSyncConfigOutputTypeDef",
    "ServiceTemplateOutputTypeDef",
    "CreateTemplateSyncConfigInputRequestTypeDef",
    "TemplateSyncConfigOutputTypeDef",
    "DeleteComponentInputRequestTypeDef",
    "DeleteDeploymentInputRequestTypeDef",
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DeleteEnvironmentTemplateInputRequestTypeDef",
    "DeleteEnvironmentTemplateVersionInputRequestTypeDef",
    "DeleteRepositoryInputRequestTypeDef",
    "DeleteServiceInputRequestTypeDef",
    "DeleteServiceSyncConfigInputRequestTypeDef",
    "DeleteServiceTemplateInputRequestTypeDef",
    "DeleteServiceTemplateVersionInputRequestTypeDef",
    "DeleteTemplateSyncConfigInputRequestTypeDef",
    "EnvironmentStateOutputTypeDef",
    "ServiceInstanceStateOutputTypeDef",
    "ServicePipelineStateOutputTypeDef",
    "DeploymentSummaryOutputTypeDef",
    "EnvironmentAccountConnectionSummaryOutputTypeDef",
    "EnvironmentSummaryOutputTypeDef",
    "EnvironmentTemplateFilterTypeDef",
    "EnvironmentTemplateSummaryOutputTypeDef",
    "EnvironmentTemplateVersionSummaryOutputTypeDef",
    "WaiterConfigTypeDef",
    "GetComponentInputRequestTypeDef",
    "GetDeploymentInputRequestTypeDef",
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "GetEnvironmentTemplateInputRequestTypeDef",
    "GetEnvironmentTemplateVersionInputRequestTypeDef",
    "GetRepositoryInputRequestTypeDef",
    "GetRepositorySyncStatusInputRequestTypeDef",
    "GetServiceInputRequestTypeDef",
    "GetServiceInstanceInputRequestTypeDef",
    "GetServiceInstanceSyncStatusInputRequestTypeDef",
    "RevisionOutputTypeDef",
    "GetServiceSyncBlockerSummaryInputRequestTypeDef",
    "GetServiceSyncConfigInputRequestTypeDef",
    "GetServiceTemplateInputRequestTypeDef",
    "GetServiceTemplateVersionInputRequestTypeDef",
    "GetTemplateSyncConfigInputRequestTypeDef",
    "GetTemplateSyncStatusInputRequestTypeDef",
    "ListComponentOutputsInputListComponentOutputsPaginateTypeDef",
    "ListComponentOutputsInputRequestTypeDef",
    "OutputOutputTypeDef",
    "ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef",
    "ListComponentProvisionedResourcesInputRequestTypeDef",
    "ProvisionedResourceOutputTypeDef",
    "ListComponentsInputListComponentsPaginateTypeDef",
    "ListComponentsInputRequestTypeDef",
    "ListDeploymentsInputListDeploymentsPaginateTypeDef",
    "ListDeploymentsInputRequestTypeDef",
    "ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    "ListEnvironmentAccountConnectionsInputRequestTypeDef",
    "ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    "ListEnvironmentOutputsInputRequestTypeDef",
    "ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    "ListEnvironmentProvisionedResourcesInputRequestTypeDef",
    "ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    "ListEnvironmentTemplateVersionsInputRequestTypeDef",
    "ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef",
    "ListEnvironmentTemplatesInputRequestTypeDef",
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    "ListRepositoriesInputRequestTypeDef",
    "RepositorySummaryOutputTypeDef",
    "ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    "ListRepositorySyncDefinitionsInputRequestTypeDef",
    "RepositorySyncDefinitionOutputTypeDef",
    "ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    "ListServiceInstanceOutputsInputRequestTypeDef",
    "ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    "ListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    "ListServiceInstancesFilterTypeDef",
    "ServiceInstanceSummaryOutputTypeDef",
    "ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    "ListServicePipelineOutputsInputRequestTypeDef",
    "ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    "ListServicePipelineProvisionedResourcesInputRequestTypeDef",
    "ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    "ListServiceTemplateVersionsInputRequestTypeDef",
    "ServiceTemplateVersionSummaryOutputTypeDef",
    "ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef",
    "ListServiceTemplatesInputRequestTypeDef",
    "ServiceTemplateSummaryOutputTypeDef",
    "ListServicesInputListServicesPaginateTypeDef",
    "ListServicesInputRequestTypeDef",
    "ServiceSummaryOutputTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "TagOutputTypeDef",
    "OutputTypeDef",
    "PaginatorConfigTypeDef",
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    "RepositorySyncEventOutputTypeDef",
    "ResourceSyncEventOutputTypeDef",
    "ResponseMetadataTypeDef",
    "S3ObjectSourceTypeDef",
    "SyncBlockerContextOutputTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateComponentInputRequestTypeDef",
    "UpdateEnvironmentAccountConnectionInputRequestTypeDef",
    "UpdateEnvironmentTemplateInputRequestTypeDef",
    "UpdateEnvironmentTemplateVersionInputRequestTypeDef",
    "UpdateServiceInputRequestTypeDef",
    "UpdateServiceInstanceInputRequestTypeDef",
    "UpdateServicePipelineInputRequestTypeDef",
    "UpdateServiceSyncBlockerInputRequestTypeDef",
    "UpdateServiceSyncConfigInputRequestTypeDef",
    "UpdateServiceTemplateInputRequestTypeDef",
    "UpdateTemplateSyncConfigInputRequestTypeDef",
    "AcceptEnvironmentAccountConnectionOutputOutputTypeDef",
    "CreateEnvironmentAccountConnectionOutputOutputTypeDef",
    "DeleteEnvironmentAccountConnectionOutputOutputTypeDef",
    "GetEnvironmentAccountConnectionOutputOutputTypeDef",
    "RejectEnvironmentAccountConnectionOutputOutputTypeDef",
    "UpdateEnvironmentAccountConnectionOutputOutputTypeDef",
    "AccountSettingsOutputTypeDef",
    "EnvironmentOutputTypeDef",
    "CancelComponentDeploymentOutputOutputTypeDef",
    "CreateComponentOutputOutputTypeDef",
    "DeleteComponentOutputOutputTypeDef",
    "GetComponentOutputOutputTypeDef",
    "UpdateComponentOutputOutputTypeDef",
    "CancelServiceInstanceDeploymentOutputOutputTypeDef",
    "CreateServiceInstanceOutputOutputTypeDef",
    "GetServiceInstanceOutputOutputTypeDef",
    "UpdateServiceInstanceOutputOutputTypeDef",
    "CancelServicePipelineDeploymentOutputOutputTypeDef",
    "ServiceOutputTypeDef",
    "UpdateServicePipelineOutputOutputTypeDef",
    "UpdateServiceTemplateVersionInputRequestTypeDef",
    "ServiceTemplateVersionOutputTypeDef",
    "ListComponentsOutputOutputTypeDef",
    "CountsSummaryOutputTypeDef",
    "CreateComponentInputRequestTypeDef",
    "CreateEnvironmentAccountConnectionInputRequestTypeDef",
    "CreateEnvironmentTemplateInputRequestTypeDef",
    "CreateRepositoryInputRequestTypeDef",
    "CreateServiceInputRequestTypeDef",
    "CreateServiceInstanceInputRequestTypeDef",
    "CreateServiceTemplateInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "UpdateAccountSettingsInputRequestTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "CreateEnvironmentTemplateOutputOutputTypeDef",
    "DeleteEnvironmentTemplateOutputOutputTypeDef",
    "GetEnvironmentTemplateOutputOutputTypeDef",
    "UpdateEnvironmentTemplateOutputOutputTypeDef",
    "CreateEnvironmentTemplateVersionOutputOutputTypeDef",
    "DeleteEnvironmentTemplateVersionOutputOutputTypeDef",
    "GetEnvironmentTemplateVersionOutputOutputTypeDef",
    "UpdateEnvironmentTemplateVersionOutputOutputTypeDef",
    "CreateRepositoryOutputOutputTypeDef",
    "DeleteRepositoryOutputOutputTypeDef",
    "GetRepositoryOutputOutputTypeDef",
    "CreateServiceSyncConfigOutputOutputTypeDef",
    "DeleteServiceSyncConfigOutputOutputTypeDef",
    "GetServiceSyncConfigOutputOutputTypeDef",
    "UpdateServiceSyncConfigOutputOutputTypeDef",
    "CreateServiceTemplateOutputOutputTypeDef",
    "DeleteServiceTemplateOutputOutputTypeDef",
    "GetServiceTemplateOutputOutputTypeDef",
    "UpdateServiceTemplateOutputOutputTypeDef",
    "CreateTemplateSyncConfigOutputOutputTypeDef",
    "DeleteTemplateSyncConfigOutputOutputTypeDef",
    "GetTemplateSyncConfigOutputOutputTypeDef",
    "UpdateTemplateSyncConfigOutputOutputTypeDef",
    "DeploymentStateOutputTypeDef",
    "ListDeploymentsOutputOutputTypeDef",
    "ListEnvironmentAccountConnectionsOutputOutputTypeDef",
    "ListEnvironmentsOutputOutputTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListEnvironmentTemplatesOutputOutputTypeDef",
    "ListEnvironmentTemplateVersionsOutputOutputTypeDef",
    "GetComponentInputComponentDeletedWaitTypeDef",
    "GetComponentInputComponentDeployedWaitTypeDef",
    "GetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    "GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    "GetServiceInputServiceCreatedWaitTypeDef",
    "GetServiceInputServiceDeletedWaitTypeDef",
    "GetServiceInputServicePipelineDeployedWaitTypeDef",
    "GetServiceInputServiceUpdatedWaitTypeDef",
    "GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    "GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    "ListComponentOutputsOutputOutputTypeDef",
    "ListEnvironmentOutputsOutputOutputTypeDef",
    "ListServiceInstanceOutputsOutputOutputTypeDef",
    "ListServicePipelineOutputsOutputOutputTypeDef",
    "ListComponentProvisionedResourcesOutputOutputTypeDef",
    "ListEnvironmentProvisionedResourcesOutputOutputTypeDef",
    "ListServiceInstanceProvisionedResourcesOutputOutputTypeDef",
    "ListServicePipelineProvisionedResourcesOutputOutputTypeDef",
    "ListRepositoriesOutputOutputTypeDef",
    "ListRepositorySyncDefinitionsOutputOutputTypeDef",
    "ListServiceInstancesInputListServiceInstancesPaginateTypeDef",
    "ListServiceInstancesInputRequestTypeDef",
    "ListServiceInstancesOutputOutputTypeDef",
    "ListServiceTemplateVersionsOutputOutputTypeDef",
    "ListServiceTemplatesOutputOutputTypeDef",
    "ListServicesOutputOutputTypeDef",
    "ListTagsForResourceOutputOutputTypeDef",
    "NotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    "RepositorySyncAttemptOutputTypeDef",
    "ResourceSyncAttemptOutputTypeDef",
    "TemplateVersionSourceInputTypeDef",
    "SyncBlockerOutputTypeDef",
    "GetAccountSettingsOutputOutputTypeDef",
    "UpdateAccountSettingsOutputOutputTypeDef",
    "CancelEnvironmentDeploymentOutputOutputTypeDef",
    "CreateEnvironmentOutputOutputTypeDef",
    "DeleteEnvironmentOutputOutputTypeDef",
    "GetEnvironmentOutputOutputTypeDef",
    "UpdateEnvironmentOutputOutputTypeDef",
    "CreateServiceOutputOutputTypeDef",
    "DeleteServiceOutputOutputTypeDef",
    "GetServiceOutputOutputTypeDef",
    "UpdateServiceOutputOutputTypeDef",
    "CreateServiceTemplateVersionOutputOutputTypeDef",
    "DeleteServiceTemplateVersionOutputOutputTypeDef",
    "GetServiceTemplateVersionOutputOutputTypeDef",
    "UpdateServiceTemplateVersionOutputOutputTypeDef",
    "GetResourcesSummaryOutputOutputTypeDef",
    "DeploymentOutputTypeDef",
    "GetRepositorySyncStatusOutputOutputTypeDef",
    "GetServiceInstanceSyncStatusOutputOutputTypeDef",
    "GetTemplateSyncStatusOutputOutputTypeDef",
    "CreateEnvironmentTemplateVersionInputRequestTypeDef",
    "CreateServiceTemplateVersionInputRequestTypeDef",
    "ServiceSyncBlockerSummaryOutputTypeDef",
    "UpdateServiceSyncBlockerOutputOutputTypeDef",
    "DeleteDeploymentOutputOutputTypeDef",
    "GetDeploymentOutputOutputTypeDef",
    "GetServiceSyncBlockerSummaryOutputOutputTypeDef",
)

AcceptEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

EnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "EnvironmentAccountConnectionOutputTypeDef",
    {
        "arn": str,
        "codebuildRoleArn": str,
        "componentRoleArn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
    },
)

RepositoryBranchOutputTypeDef = TypedDict(
    "RepositoryBranchOutputTypeDef",
    {
        "arn": str,
        "branch": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

CancelComponentDeploymentInputRequestTypeDef = TypedDict(
    "CancelComponentDeploymentInputRequestTypeDef",
    {
        "componentName": str,
    },
)

ComponentOutputTypeDef = TypedDict(
    "ComponentOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "description": str,
        "environmentName": str,
        "lastAttemptedDeploymentId": str,
        "lastClientRequestToken": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "lastModifiedAt": datetime,
        "lastSucceededDeploymentId": str,
        "name": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSpec": str,
    },
)

CancelEnvironmentDeploymentInputRequestTypeDef = TypedDict(
    "CancelEnvironmentDeploymentInputRequestTypeDef",
    {
        "environmentName": str,
    },
)

CancelServiceInstanceDeploymentInputRequestTypeDef = TypedDict(
    "CancelServiceInstanceDeploymentInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)

ServiceInstanceOutputTypeDef = TypedDict(
    "ServiceInstanceOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "environmentName": str,
        "lastAttemptedDeploymentId": str,
        "lastClientRequestToken": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "lastSucceededDeploymentId": str,
        "name": str,
        "serviceName": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

CancelServicePipelineDeploymentInputRequestTypeDef = TypedDict(
    "CancelServicePipelineDeploymentInputRequestTypeDef",
    {
        "serviceName": str,
    },
)

ServicePipelineOutputTypeDef = TypedDict(
    "ServicePipelineOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "lastAttemptedDeploymentId": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "lastSucceededDeploymentId": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

CompatibleEnvironmentTemplateInputTypeDef = TypedDict(
    "CompatibleEnvironmentTemplateInputTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

CompatibleEnvironmentTemplateOutputTypeDef = TypedDict(
    "CompatibleEnvironmentTemplateOutputTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

ComponentStateOutputTypeDef = TypedDict(
    "ComponentStateOutputTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSpec": str,
        "templateFile": str,
    },
)

ComponentSummaryOutputTypeDef = TypedDict(
    "ComponentSummaryOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "environmentName": str,
        "lastAttemptedDeploymentId": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "lastModifiedAt": datetime,
        "lastSucceededDeploymentId": str,
        "name": str,
        "serviceInstanceName": str,
        "serviceName": str,
    },
)

ResourceCountsSummaryOutputTypeDef = TypedDict(
    "ResourceCountsSummaryOutputTypeDef",
    {
        "behindMajor": int,
        "behindMinor": int,
        "failed": int,
        "total": int,
        "upToDate": int,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

RepositoryBranchInputTypeDef = TypedDict(
    "RepositoryBranchInputTypeDef",
    {
        "branch": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

EnvironmentTemplateOutputTypeDef = TypedDict(
    "EnvironmentTemplateOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "lastModifiedAt": datetime,
        "name": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
)

EnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "EnvironmentTemplateVersionOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "recommendedMinorVersion": str,
        "schema": str,
        "status": TemplateVersionStatusType,
        "statusMessage": str,
        "templateName": str,
    },
)

RepositoryOutputTypeDef = TypedDict(
    "RepositoryOutputTypeDef",
    {
        "arn": str,
        "connectionArn": str,
        "encryptionKey": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

CreateServiceSyncConfigInputRequestTypeDef = TypedDict(
    "CreateServiceSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "filePath": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "serviceName": str,
    },
)

ServiceSyncConfigOutputTypeDef = TypedDict(
    "ServiceSyncConfigOutputTypeDef",
    {
        "branch": str,
        "filePath": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "serviceName": str,
    },
)

ServiceTemplateOutputTypeDef = TypedDict(
    "ServiceTemplateOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "lastModifiedAt": datetime,
        "name": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
)

_RequiredCreateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_RequiredCreateTemplateSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalCreateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_OptionalCreateTemplateSyncConfigInputRequestTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)

class CreateTemplateSyncConfigInputRequestTypeDef(
    _RequiredCreateTemplateSyncConfigInputRequestTypeDef,
    _OptionalCreateTemplateSyncConfigInputRequestTypeDef,
):
    pass

TemplateSyncConfigOutputTypeDef = TypedDict(
    "TemplateSyncConfigOutputTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "subdirectory": str,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)

DeleteComponentInputRequestTypeDef = TypedDict(
    "DeleteComponentInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteDeploymentInputRequestTypeDef = TypedDict(
    "DeleteDeploymentInputRequestTypeDef",
    {
        "id": str,
    },
)

DeleteEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

DeleteEnvironmentInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

DeleteRepositoryInputRequestTypeDef = TypedDict(
    "DeleteRepositoryInputRequestTypeDef",
    {
        "name": str,
        "provider": RepositoryProviderType,
    },
)

DeleteServiceInputRequestTypeDef = TypedDict(
    "DeleteServiceInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteServiceSyncConfigInputRequestTypeDef = TypedDict(
    "DeleteServiceSyncConfigInputRequestTypeDef",
    {
        "serviceName": str,
    },
)

DeleteServiceTemplateInputRequestTypeDef = TypedDict(
    "DeleteServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "DeleteServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

DeleteTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "DeleteTemplateSyncConfigInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)

EnvironmentStateOutputTypeDef = TypedDict(
    "EnvironmentStateOutputTypeDef",
    {
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

ServiceInstanceStateOutputTypeDef = TypedDict(
    "ServiceInstanceStateOutputTypeDef",
    {
        "lastSuccessfulComponentDeploymentIds": List[str],
        "lastSuccessfulEnvironmentDeploymentId": str,
        "lastSuccessfulServicePipelineDeploymentId": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

ServicePipelineStateOutputTypeDef = TypedDict(
    "ServicePipelineStateOutputTypeDef",
    {
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

DeploymentSummaryOutputTypeDef = TypedDict(
    "DeploymentSummaryOutputTypeDef",
    {
        "arn": str,
        "completedAt": datetime,
        "componentName": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "id": str,
        "lastAttemptedDeploymentId": str,
        "lastModifiedAt": datetime,
        "lastSucceededDeploymentId": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "targetArn": str,
        "targetResourceCreatedAt": datetime,
        "targetResourceType": DeploymentTargetResourceTypeType,
    },
)

EnvironmentAccountConnectionSummaryOutputTypeDef = TypedDict(
    "EnvironmentAccountConnectionSummaryOutputTypeDef",
    {
        "arn": str,
        "componentRoleArn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
    },
)

EnvironmentSummaryOutputTypeDef = TypedDict(
    "EnvironmentSummaryOutputTypeDef",
    {
        "arn": str,
        "componentRoleArn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "environmentAccountId": str,
        "lastAttemptedDeploymentId": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "lastSucceededDeploymentId": str,
        "name": str,
        "protonServiceRoleArn": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

EnvironmentTemplateFilterTypeDef = TypedDict(
    "EnvironmentTemplateFilterTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

EnvironmentTemplateSummaryOutputTypeDef = TypedDict(
    "EnvironmentTemplateSummaryOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "displayName": str,
        "lastModifiedAt": datetime,
        "name": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
)

EnvironmentTemplateVersionSummaryOutputTypeDef = TypedDict(
    "EnvironmentTemplateVersionSummaryOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "recommendedMinorVersion": str,
        "status": TemplateVersionStatusType,
        "statusMessage": str,
        "templateName": str,
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

GetComponentInputRequestTypeDef = TypedDict(
    "GetComponentInputRequestTypeDef",
    {
        "name": str,
    },
)

_RequiredGetDeploymentInputRequestTypeDef = TypedDict(
    "_RequiredGetDeploymentInputRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalGetDeploymentInputRequestTypeDef = TypedDict(
    "_OptionalGetDeploymentInputRequestTypeDef",
    {
        "componentName": str,
        "environmentName": str,
        "serviceInstanceName": str,
        "serviceName": str,
    },
    total=False,
)

class GetDeploymentInputRequestTypeDef(
    _RequiredGetDeploymentInputRequestTypeDef, _OptionalGetDeploymentInputRequestTypeDef
):
    pass

GetEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

GetEnvironmentInputRequestTypeDef = TypedDict(
    "GetEnvironmentInputRequestTypeDef",
    {
        "name": str,
    },
)

GetEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "GetEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

GetEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "GetEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

GetRepositoryInputRequestTypeDef = TypedDict(
    "GetRepositoryInputRequestTypeDef",
    {
        "name": str,
        "provider": RepositoryProviderType,
    },
)

GetRepositorySyncStatusInputRequestTypeDef = TypedDict(
    "GetRepositorySyncStatusInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": SyncTypeType,
    },
)

GetServiceInputRequestTypeDef = TypedDict(
    "GetServiceInputRequestTypeDef",
    {
        "name": str,
    },
)

GetServiceInstanceInputRequestTypeDef = TypedDict(
    "GetServiceInstanceInputRequestTypeDef",
    {
        "name": str,
        "serviceName": str,
    },
)

GetServiceInstanceSyncStatusInputRequestTypeDef = TypedDict(
    "GetServiceInstanceSyncStatusInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)

RevisionOutputTypeDef = TypedDict(
    "RevisionOutputTypeDef",
    {
        "branch": str,
        "directory": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "sha": str,
    },
)

_RequiredGetServiceSyncBlockerSummaryInputRequestTypeDef = TypedDict(
    "_RequiredGetServiceSyncBlockerSummaryInputRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalGetServiceSyncBlockerSummaryInputRequestTypeDef = TypedDict(
    "_OptionalGetServiceSyncBlockerSummaryInputRequestTypeDef",
    {
        "serviceInstanceName": str,
    },
    total=False,
)

class GetServiceSyncBlockerSummaryInputRequestTypeDef(
    _RequiredGetServiceSyncBlockerSummaryInputRequestTypeDef,
    _OptionalGetServiceSyncBlockerSummaryInputRequestTypeDef,
):
    pass

GetServiceSyncConfigInputRequestTypeDef = TypedDict(
    "GetServiceSyncConfigInputRequestTypeDef",
    {
        "serviceName": str,
    },
)

GetServiceTemplateInputRequestTypeDef = TypedDict(
    "GetServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

GetServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "GetServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

GetTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "GetTemplateSyncConfigInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)

GetTemplateSyncStatusInputRequestTypeDef = TypedDict(
    "GetTemplateSyncStatusInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
        "templateVersion": str,
    },
)

_RequiredListComponentOutputsInputListComponentOutputsPaginateTypeDef = TypedDict(
    "_RequiredListComponentOutputsInputListComponentOutputsPaginateTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentOutputsInputListComponentOutputsPaginateTypeDef = TypedDict(
    "_OptionalListComponentOutputsInputListComponentOutputsPaginateTypeDef",
    {
        "deploymentId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListComponentOutputsInputListComponentOutputsPaginateTypeDef(
    _RequiredListComponentOutputsInputListComponentOutputsPaginateTypeDef,
    _OptionalListComponentOutputsInputListComponentOutputsPaginateTypeDef,
):
    pass

_RequiredListComponentOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListComponentOutputsInputRequestTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListComponentOutputsInputRequestTypeDef",
    {
        "deploymentId": str,
        "nextToken": str,
    },
    total=False,
)

class ListComponentOutputsInputRequestTypeDef(
    _RequiredListComponentOutputsInputRequestTypeDef,
    _OptionalListComponentOutputsInputRequestTypeDef,
):
    pass

OutputOutputTypeDef = TypedDict(
    "OutputOutputTypeDef",
    {
        "key": str,
        "valueString": str,
    },
)

_RequiredListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef(
    _RequiredListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef,
    _OptionalListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef,
):
    pass

_RequiredListComponentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListComponentProvisionedResourcesInputRequestTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListComponentProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListComponentProvisionedResourcesInputRequestTypeDef(
    _RequiredListComponentProvisionedResourcesInputRequestTypeDef,
    _OptionalListComponentProvisionedResourcesInputRequestTypeDef,
):
    pass

ProvisionedResourceOutputTypeDef = TypedDict(
    "ProvisionedResourceOutputTypeDef",
    {
        "identifier": str,
        "name": str,
        "provisioningEngine": ProvisionedResourceEngineType,
    },
)

ListComponentsInputListComponentsPaginateTypeDef = TypedDict(
    "ListComponentsInputListComponentsPaginateTypeDef",
    {
        "environmentName": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListComponentsInputRequestTypeDef = TypedDict(
    "ListComponentsInputRequestTypeDef",
    {
        "environmentName": str,
        "maxResults": int,
        "nextToken": str,
        "serviceInstanceName": str,
        "serviceName": str,
    },
    total=False,
)

ListDeploymentsInputListDeploymentsPaginateTypeDef = TypedDict(
    "ListDeploymentsInputListDeploymentsPaginateTypeDef",
    {
        "componentName": str,
        "environmentName": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDeploymentsInputRequestTypeDef = TypedDict(
    "ListDeploymentsInputRequestTypeDef",
    {
        "componentName": str,
        "environmentName": str,
        "maxResults": int,
        "nextToken": str,
        "serviceInstanceName": str,
        "serviceName": str,
    },
    total=False,
)

_RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    {
        "requestedBy": EnvironmentAccountConnectionRequesterAccountTypeType,
    },
)
_OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    {
        "environmentName": str,
        "statuses": Sequence[EnvironmentAccountConnectionStatusType],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef(
    _RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef,
    _OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef,
):
    pass

_RequiredListEnvironmentAccountConnectionsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentAccountConnectionsInputRequestTypeDef",
    {
        "requestedBy": EnvironmentAccountConnectionRequesterAccountTypeType,
    },
)
_OptionalListEnvironmentAccountConnectionsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentAccountConnectionsInputRequestTypeDef",
    {
        "environmentName": str,
        "maxResults": int,
        "nextToken": str,
        "statuses": Sequence[EnvironmentAccountConnectionStatusType],
    },
    total=False,
)

class ListEnvironmentAccountConnectionsInputRequestTypeDef(
    _RequiredListEnvironmentAccountConnectionsInputRequestTypeDef,
    _OptionalListEnvironmentAccountConnectionsInputRequestTypeDef,
):
    pass

_RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    {
        "deploymentId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef(
    _RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef,
    _OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef,
):
    pass

_RequiredListEnvironmentOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentOutputsInputRequestTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentOutputsInputRequestTypeDef",
    {
        "deploymentId": str,
        "nextToken": str,
    },
    total=False,
)

class ListEnvironmentOutputsInputRequestTypeDef(
    _RequiredListEnvironmentOutputsInputRequestTypeDef,
    _OptionalListEnvironmentOutputsInputRequestTypeDef,
):
    pass

_RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef(
    _RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef,
    _OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef,
):
    pass

_RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListEnvironmentProvisionedResourcesInputRequestTypeDef(
    _RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef,
    _OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef,
):
    pass

_RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    {
        "majorVersion": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef(
    _RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef,
    _OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef,
):
    pass

_RequiredListEnvironmentTemplateVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentTemplateVersionsInputRequestTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListEnvironmentTemplateVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentTemplateVersionsInputRequestTypeDef",
    {
        "majorVersion": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListEnvironmentTemplateVersionsInputRequestTypeDef(
    _RequiredListEnvironmentTemplateVersionsInputRequestTypeDef,
    _OptionalListEnvironmentTemplateVersionsInputRequestTypeDef,
):
    pass

ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef = TypedDict(
    "ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEnvironmentTemplatesInputRequestTypeDef = TypedDict(
    "ListEnvironmentTemplatesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListRepositoriesInputListRepositoriesPaginateTypeDef = TypedDict(
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListRepositoriesInputRequestTypeDef = TypedDict(
    "ListRepositoriesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

RepositorySummaryOutputTypeDef = TypedDict(
    "RepositorySummaryOutputTypeDef",
    {
        "arn": str,
        "connectionArn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

_RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef = TypedDict(
    "_RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    {
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": SyncTypeType,
    },
)
_OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef = TypedDict(
    "_OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef(
    _RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef,
    _OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef,
):
    pass

_RequiredListRepositorySyncDefinitionsInputRequestTypeDef = TypedDict(
    "_RequiredListRepositorySyncDefinitionsInputRequestTypeDef",
    {
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": SyncTypeType,
    },
)
_OptionalListRepositorySyncDefinitionsInputRequestTypeDef = TypedDict(
    "_OptionalListRepositorySyncDefinitionsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListRepositorySyncDefinitionsInputRequestTypeDef(
    _RequiredListRepositorySyncDefinitionsInputRequestTypeDef,
    _OptionalListRepositorySyncDefinitionsInputRequestTypeDef,
):
    pass

RepositorySyncDefinitionOutputTypeDef = TypedDict(
    "RepositorySyncDefinitionOutputTypeDef",
    {
        "branch": str,
        "directory": str,
        "parent": str,
        "target": str,
    },
)

_RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef = TypedDict(
    "_RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef = TypedDict(
    "_OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    {
        "deploymentId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef(
    _RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef,
    _OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef,
):
    pass

_RequiredListServiceInstanceOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListServiceInstanceOutputsInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListServiceInstanceOutputsInputRequestTypeDef",
    {
        "deploymentId": str,
        "nextToken": str,
    },
    total=False,
)

class ListServiceInstanceOutputsInputRequestTypeDef(
    _RequiredListServiceInstanceOutputsInputRequestTypeDef,
    _OptionalListServiceInstanceOutputsInputRequestTypeDef,
):
    pass

_RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef(
    _RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef,
    _OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef,
):
    pass

_RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListServiceInstanceProvisionedResourcesInputRequestTypeDef(
    _RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef,
    _OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef,
):
    pass

ListServiceInstancesFilterTypeDef = TypedDict(
    "ListServiceInstancesFilterTypeDef",
    {
        "key": ListServiceInstancesFilterByType,
        "value": str,
    },
    total=False,
)

ServiceInstanceSummaryOutputTypeDef = TypedDict(
    "ServiceInstanceSummaryOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "environmentName": str,
        "lastAttemptedDeploymentId": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "lastSucceededDeploymentId": str,
        "name": str,
        "serviceName": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

_RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef = TypedDict(
    "_RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef = TypedDict(
    "_OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    {
        "deploymentId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef(
    _RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef,
    _OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef,
):
    pass

_RequiredListServicePipelineOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListServicePipelineOutputsInputRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListServicePipelineOutputsInputRequestTypeDef",
    {
        "deploymentId": str,
        "nextToken": str,
    },
    total=False,
)

class ListServicePipelineOutputsInputRequestTypeDef(
    _RequiredListServicePipelineOutputsInputRequestTypeDef,
    _OptionalListServicePipelineOutputsInputRequestTypeDef,
):
    pass

_RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef(
    _RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef,
    _OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef,
):
    pass

_RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListServicePipelineProvisionedResourcesInputRequestTypeDef(
    _RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef,
    _OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef,
):
    pass

_RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    {
        "majorVersion": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef(
    _RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef,
    _OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef,
):
    pass

_RequiredListServiceTemplateVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListServiceTemplateVersionsInputRequestTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListServiceTemplateVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListServiceTemplateVersionsInputRequestTypeDef",
    {
        "majorVersion": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListServiceTemplateVersionsInputRequestTypeDef(
    _RequiredListServiceTemplateVersionsInputRequestTypeDef,
    _OptionalListServiceTemplateVersionsInputRequestTypeDef,
):
    pass

ServiceTemplateVersionSummaryOutputTypeDef = TypedDict(
    "ServiceTemplateVersionSummaryOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "recommendedMinorVersion": str,
        "status": TemplateVersionStatusType,
        "statusMessage": str,
        "templateName": str,
    },
)

ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef = TypedDict(
    "ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListServiceTemplatesInputRequestTypeDef = TypedDict(
    "ListServiceTemplatesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ServiceTemplateSummaryOutputTypeDef = TypedDict(
    "ServiceTemplateSummaryOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "displayName": str,
        "lastModifiedAt": datetime,
        "name": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
)

ListServicesInputListServicesPaginateTypeDef = TypedDict(
    "ListServicesInputListServicesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListServicesInputRequestTypeDef = TypedDict(
    "ListServicesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ServiceSummaryOutputTypeDef = TypedDict(
    "ServiceSummaryOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "lastModifiedAt": datetime,
        "name": str,
        "status": ServiceStatusType,
        "statusMessage": str,
        "templateName": str,
    },
)

_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef,
):
    pass

_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "key": str,
        "value": str,
    },
)

OutputTypeDef = TypedDict(
    "OutputTypeDef",
    {
        "key": str,
        "valueString": str,
    },
    total=False,
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

RejectEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

RepositorySyncEventOutputTypeDef = TypedDict(
    "RepositorySyncEventOutputTypeDef",
    {
        "event": str,
        "externalId": str,
        "time": datetime,
        "type": str,
    },
)

ResourceSyncEventOutputTypeDef = TypedDict(
    "ResourceSyncEventOutputTypeDef",
    {
        "event": str,
        "externalId": str,
        "time": datetime,
        "type": str,
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

S3ObjectSourceTypeDef = TypedDict(
    "S3ObjectSourceTypeDef",
    {
        "bucket": str,
        "key": str,
    },
)

SyncBlockerContextOutputTypeDef = TypedDict(
    "SyncBlockerContextOutputTypeDef",
    {
        "key": str,
        "value": str,
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateComponentInputRequestTypeDef = TypedDict(
    "_RequiredUpdateComponentInputRequestTypeDef",
    {
        "deploymentType": ComponentDeploymentUpdateTypeType,
        "name": str,
    },
)
_OptionalUpdateComponentInputRequestTypeDef = TypedDict(
    "_OptionalUpdateComponentInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSpec": str,
        "templateFile": str,
    },
    total=False,
)

class UpdateComponentInputRequestTypeDef(
    _RequiredUpdateComponentInputRequestTypeDef, _OptionalUpdateComponentInputRequestTypeDef
):
    pass

_RequiredUpdateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "codebuildRoleArn": str,
        "componentRoleArn": str,
        "roleArn": str,
    },
    total=False,
)

class UpdateEnvironmentAccountConnectionInputRequestTypeDef(
    _RequiredUpdateEnvironmentAccountConnectionInputRequestTypeDef,
    _OptionalUpdateEnvironmentAccountConnectionInputRequestTypeDef,
):
    pass

_RequiredUpdateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
    },
    total=False,
)

class UpdateEnvironmentTemplateInputRequestTypeDef(
    _RequiredUpdateEnvironmentTemplateInputRequestTypeDef,
    _OptionalUpdateEnvironmentTemplateInputRequestTypeDef,
):
    pass

_RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "description": str,
        "status": TemplateVersionStatusType,
    },
    total=False,
)

class UpdateEnvironmentTemplateVersionInputRequestTypeDef(
    _RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef,
    _OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef,
):
    pass

_RequiredUpdateServiceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateServiceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceInputRequestTypeDef",
    {
        "description": str,
        "spec": str,
    },
    total=False,
)

class UpdateServiceInputRequestTypeDef(
    _RequiredUpdateServiceInputRequestTypeDef, _OptionalUpdateServiceInputRequestTypeDef
):
    pass

_RequiredUpdateServiceInstanceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceInstanceInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "name": str,
        "serviceName": str,
    },
)
_OptionalUpdateServiceInstanceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceInstanceInputRequestTypeDef",
    {
        "clientToken": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)

class UpdateServiceInstanceInputRequestTypeDef(
    _RequiredUpdateServiceInstanceInputRequestTypeDef,
    _OptionalUpdateServiceInstanceInputRequestTypeDef,
):
    pass

_RequiredUpdateServicePipelineInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServicePipelineInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "serviceName": str,
        "spec": str,
    },
)
_OptionalUpdateServicePipelineInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServicePipelineInputRequestTypeDef",
    {
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)

class UpdateServicePipelineInputRequestTypeDef(
    _RequiredUpdateServicePipelineInputRequestTypeDef,
    _OptionalUpdateServicePipelineInputRequestTypeDef,
):
    pass

UpdateServiceSyncBlockerInputRequestTypeDef = TypedDict(
    "UpdateServiceSyncBlockerInputRequestTypeDef",
    {
        "id": str,
        "resolvedReason": str,
    },
)

UpdateServiceSyncConfigInputRequestTypeDef = TypedDict(
    "UpdateServiceSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "filePath": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "serviceName": str,
    },
)

_RequiredUpdateServiceTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateServiceTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
    },
    total=False,
)

class UpdateServiceTemplateInputRequestTypeDef(
    _RequiredUpdateServiceTemplateInputRequestTypeDef,
    _OptionalUpdateServiceTemplateInputRequestTypeDef,
):
    pass

_RequiredUpdateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplateSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalUpdateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplateSyncConfigInputRequestTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)

class UpdateTemplateSyncConfigInputRequestTypeDef(
    _RequiredUpdateTemplateSyncConfigInputRequestTypeDef,
    _OptionalUpdateTemplateSyncConfigInputRequestTypeDef,
):
    pass

AcceptEnvironmentAccountConnectionOutputOutputTypeDef = TypedDict(
    "AcceptEnvironmentAccountConnectionOutputOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEnvironmentAccountConnectionOutputOutputTypeDef = TypedDict(
    "CreateEnvironmentAccountConnectionOutputOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentAccountConnectionOutputOutputTypeDef = TypedDict(
    "DeleteEnvironmentAccountConnectionOutputOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEnvironmentAccountConnectionOutputOutputTypeDef = TypedDict(
    "GetEnvironmentAccountConnectionOutputOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RejectEnvironmentAccountConnectionOutputOutputTypeDef = TypedDict(
    "RejectEnvironmentAccountConnectionOutputOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEnvironmentAccountConnectionOutputOutputTypeDef = TypedDict(
    "UpdateEnvironmentAccountConnectionOutputOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AccountSettingsOutputTypeDef = TypedDict(
    "AccountSettingsOutputTypeDef",
    {
        "pipelineCodebuildRoleArn": str,
        "pipelineProvisioningRepository": RepositoryBranchOutputTypeDef,
        "pipelineServiceRoleArn": str,
    },
)

EnvironmentOutputTypeDef = TypedDict(
    "EnvironmentOutputTypeDef",
    {
        "arn": str,
        "codebuildRoleArn": str,
        "componentRoleArn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "environmentAccountId": str,
        "lastAttemptedDeploymentId": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "lastSucceededDeploymentId": str,
        "name": str,
        "protonServiceRoleArn": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "provisioningRepository": RepositoryBranchOutputTypeDef,
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)

CancelComponentDeploymentOutputOutputTypeDef = TypedDict(
    "CancelComponentDeploymentOutputOutputTypeDef",
    {
        "component": ComponentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateComponentOutputOutputTypeDef = TypedDict(
    "CreateComponentOutputOutputTypeDef",
    {
        "component": ComponentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteComponentOutputOutputTypeDef = TypedDict(
    "DeleteComponentOutputOutputTypeDef",
    {
        "component": ComponentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetComponentOutputOutputTypeDef = TypedDict(
    "GetComponentOutputOutputTypeDef",
    {
        "component": ComponentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateComponentOutputOutputTypeDef = TypedDict(
    "UpdateComponentOutputOutputTypeDef",
    {
        "component": ComponentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelServiceInstanceDeploymentOutputOutputTypeDef = TypedDict(
    "CancelServiceInstanceDeploymentOutputOutputTypeDef",
    {
        "serviceInstance": ServiceInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateServiceInstanceOutputOutputTypeDef = TypedDict(
    "CreateServiceInstanceOutputOutputTypeDef",
    {
        "serviceInstance": ServiceInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceInstanceOutputOutputTypeDef = TypedDict(
    "GetServiceInstanceOutputOutputTypeDef",
    {
        "serviceInstance": ServiceInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServiceInstanceOutputOutputTypeDef = TypedDict(
    "UpdateServiceInstanceOutputOutputTypeDef",
    {
        "serviceInstance": ServiceInstanceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelServicePipelineDeploymentOutputOutputTypeDef = TypedDict(
    "CancelServicePipelineDeploymentOutputOutputTypeDef",
    {
        "pipeline": ServicePipelineOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ServiceOutputTypeDef = TypedDict(
    "ServiceOutputTypeDef",
    {
        "arn": str,
        "branchName": str,
        "createdAt": datetime,
        "description": str,
        "lastModifiedAt": datetime,
        "name": str,
        "pipeline": ServicePipelineOutputTypeDef,
        "repositoryConnectionArn": str,
        "repositoryId": str,
        "spec": str,
        "status": ServiceStatusType,
        "statusMessage": str,
        "templateName": str,
    },
)

UpdateServicePipelineOutputOutputTypeDef = TypedDict(
    "UpdateServicePipelineOutputOutputTypeDef",
    {
        "pipeline": ServicePipelineOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalUpdateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceTemplateVersionInputRequestTypeDef",
    {
        "compatibleEnvironmentTemplates": Sequence[CompatibleEnvironmentTemplateInputTypeDef],
        "description": str,
        "status": TemplateVersionStatusType,
        "supportedComponentSources": Sequence[Literal["DIRECTLY_DEFINED"]],
    },
    total=False,
)

class UpdateServiceTemplateVersionInputRequestTypeDef(
    _RequiredUpdateServiceTemplateVersionInputRequestTypeDef,
    _OptionalUpdateServiceTemplateVersionInputRequestTypeDef,
):
    pass

ServiceTemplateVersionOutputTypeDef = TypedDict(
    "ServiceTemplateVersionOutputTypeDef",
    {
        "arn": str,
        "compatibleEnvironmentTemplates": List[CompatibleEnvironmentTemplateOutputTypeDef],
        "createdAt": datetime,
        "description": str,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "recommendedMinorVersion": str,
        "schema": str,
        "status": TemplateVersionStatusType,
        "statusMessage": str,
        "supportedComponentSources": List[Literal["DIRECTLY_DEFINED"]],
        "templateName": str,
    },
)

ListComponentsOutputOutputTypeDef = TypedDict(
    "ListComponentsOutputOutputTypeDef",
    {
        "components": List[ComponentSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CountsSummaryOutputTypeDef = TypedDict(
    "CountsSummaryOutputTypeDef",
    {
        "components": ResourceCountsSummaryOutputTypeDef,
        "environmentTemplates": ResourceCountsSummaryOutputTypeDef,
        "environments": ResourceCountsSummaryOutputTypeDef,
        "pipelines": ResourceCountsSummaryOutputTypeDef,
        "serviceInstances": ResourceCountsSummaryOutputTypeDef,
        "serviceTemplates": ResourceCountsSummaryOutputTypeDef,
        "services": ResourceCountsSummaryOutputTypeDef,
    },
)

_RequiredCreateComponentInputRequestTypeDef = TypedDict(
    "_RequiredCreateComponentInputRequestTypeDef",
    {
        "manifest": str,
        "name": str,
        "templateFile": str,
    },
)
_OptionalCreateComponentInputRequestTypeDef = TypedDict(
    "_OptionalCreateComponentInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "environmentName": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSpec": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateComponentInputRequestTypeDef(
    _RequiredCreateComponentInputRequestTypeDef, _OptionalCreateComponentInputRequestTypeDef
):
    pass

_RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "environmentName": str,
        "managementAccountId": str,
    },
)
_OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "clientToken": str,
        "codebuildRoleArn": str,
        "componentRoleArn": str,
        "roleArn": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEnvironmentAccountConnectionInputRequestTypeDef(
    _RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef,
    _OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef,
):
    pass

_RequiredCreateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEnvironmentTemplateInputRequestTypeDef(
    _RequiredCreateEnvironmentTemplateInputRequestTypeDef,
    _OptionalCreateEnvironmentTemplateInputRequestTypeDef,
):
    pass

_RequiredCreateRepositoryInputRequestTypeDef = TypedDict(
    "_RequiredCreateRepositoryInputRequestTypeDef",
    {
        "connectionArn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)
_OptionalCreateRepositoryInputRequestTypeDef = TypedDict(
    "_OptionalCreateRepositoryInputRequestTypeDef",
    {
        "encryptionKey": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateRepositoryInputRequestTypeDef(
    _RequiredCreateRepositoryInputRequestTypeDef, _OptionalCreateRepositoryInputRequestTypeDef
):
    pass

_RequiredCreateServiceInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceInputRequestTypeDef",
    {
        "name": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateName": str,
    },
)
_OptionalCreateServiceInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceInputRequestTypeDef",
    {
        "branchName": str,
        "description": str,
        "repositoryConnectionArn": str,
        "repositoryId": str,
        "tags": Sequence[TagTypeDef],
        "templateMinorVersion": str,
    },
    total=False,
)

class CreateServiceInputRequestTypeDef(
    _RequiredCreateServiceInputRequestTypeDef, _OptionalCreateServiceInputRequestTypeDef
):
    pass

_RequiredCreateServiceInstanceInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceInstanceInputRequestTypeDef",
    {
        "name": str,
        "serviceName": str,
        "spec": str,
    },
)
_OptionalCreateServiceInstanceInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceInstanceInputRequestTypeDef",
    {
        "clientToken": str,
        "tags": Sequence[TagTypeDef],
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)

class CreateServiceInstanceInputRequestTypeDef(
    _RequiredCreateServiceInstanceInputRequestTypeDef,
    _OptionalCreateServiceInstanceInputRequestTypeDef,
):
    pass

_RequiredCreateServiceTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateServiceTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateServiceTemplateInputRequestTypeDef(
    _RequiredCreateServiceTemplateInputRequestTypeDef,
    _OptionalCreateServiceTemplateInputRequestTypeDef,
):
    pass

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentInputRequestTypeDef",
    {
        "name": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateName": str,
    },
)
_OptionalCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentInputRequestTypeDef",
    {
        "codebuildRoleArn": str,
        "componentRoleArn": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "protonServiceRoleArn": str,
        "provisioningRepository": RepositoryBranchInputTypeDef,
        "tags": Sequence[TagTypeDef],
        "templateMinorVersion": str,
    },
    total=False,
)

class CreateEnvironmentInputRequestTypeDef(
    _RequiredCreateEnvironmentInputRequestTypeDef, _OptionalCreateEnvironmentInputRequestTypeDef
):
    pass

UpdateAccountSettingsInputRequestTypeDef = TypedDict(
    "UpdateAccountSettingsInputRequestTypeDef",
    {
        "deletePipelineProvisioningRepository": bool,
        "pipelineCodebuildRoleArn": str,
        "pipelineProvisioningRepository": RepositoryBranchInputTypeDef,
        "pipelineServiceRoleArn": str,
    },
    total=False,
)

_RequiredUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "name": str,
    },
)
_OptionalUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentInputRequestTypeDef",
    {
        "codebuildRoleArn": str,
        "componentRoleArn": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "protonServiceRoleArn": str,
        "provisioningRepository": RepositoryBranchInputTypeDef,
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)

class UpdateEnvironmentInputRequestTypeDef(
    _RequiredUpdateEnvironmentInputRequestTypeDef, _OptionalUpdateEnvironmentInputRequestTypeDef
):
    pass

CreateEnvironmentTemplateOutputOutputTypeDef = TypedDict(
    "CreateEnvironmentTemplateOutputOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentTemplateOutputOutputTypeDef = TypedDict(
    "DeleteEnvironmentTemplateOutputOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEnvironmentTemplateOutputOutputTypeDef = TypedDict(
    "GetEnvironmentTemplateOutputOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEnvironmentTemplateOutputOutputTypeDef = TypedDict(
    "UpdateEnvironmentTemplateOutputOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEnvironmentTemplateVersionOutputOutputTypeDef = TypedDict(
    "CreateEnvironmentTemplateVersionOutputOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentTemplateVersionOutputOutputTypeDef = TypedDict(
    "DeleteEnvironmentTemplateVersionOutputOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEnvironmentTemplateVersionOutputOutputTypeDef = TypedDict(
    "GetEnvironmentTemplateVersionOutputOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEnvironmentTemplateVersionOutputOutputTypeDef = TypedDict(
    "UpdateEnvironmentTemplateVersionOutputOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateRepositoryOutputOutputTypeDef = TypedDict(
    "CreateRepositoryOutputOutputTypeDef",
    {
        "repository": RepositoryOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteRepositoryOutputOutputTypeDef = TypedDict(
    "DeleteRepositoryOutputOutputTypeDef",
    {
        "repository": RepositoryOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRepositoryOutputOutputTypeDef = TypedDict(
    "GetRepositoryOutputOutputTypeDef",
    {
        "repository": RepositoryOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateServiceSyncConfigOutputOutputTypeDef = TypedDict(
    "CreateServiceSyncConfigOutputOutputTypeDef",
    {
        "serviceSyncConfig": ServiceSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteServiceSyncConfigOutputOutputTypeDef = TypedDict(
    "DeleteServiceSyncConfigOutputOutputTypeDef",
    {
        "serviceSyncConfig": ServiceSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceSyncConfigOutputOutputTypeDef = TypedDict(
    "GetServiceSyncConfigOutputOutputTypeDef",
    {
        "serviceSyncConfig": ServiceSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServiceSyncConfigOutputOutputTypeDef = TypedDict(
    "UpdateServiceSyncConfigOutputOutputTypeDef",
    {
        "serviceSyncConfig": ServiceSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateServiceTemplateOutputOutputTypeDef = TypedDict(
    "CreateServiceTemplateOutputOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteServiceTemplateOutputOutputTypeDef = TypedDict(
    "DeleteServiceTemplateOutputOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceTemplateOutputOutputTypeDef = TypedDict(
    "GetServiceTemplateOutputOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServiceTemplateOutputOutputTypeDef = TypedDict(
    "UpdateServiceTemplateOutputOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateTemplateSyncConfigOutputOutputTypeDef = TypedDict(
    "CreateTemplateSyncConfigOutputOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteTemplateSyncConfigOutputOutputTypeDef = TypedDict(
    "DeleteTemplateSyncConfigOutputOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTemplateSyncConfigOutputOutputTypeDef = TypedDict(
    "GetTemplateSyncConfigOutputOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateTemplateSyncConfigOutputOutputTypeDef = TypedDict(
    "UpdateTemplateSyncConfigOutputOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeploymentStateOutputTypeDef = TypedDict(
    "DeploymentStateOutputTypeDef",
    {
        "component": ComponentStateOutputTypeDef,
        "environment": EnvironmentStateOutputTypeDef,
        "serviceInstance": ServiceInstanceStateOutputTypeDef,
        "servicePipeline": ServicePipelineStateOutputTypeDef,
    },
)

ListDeploymentsOutputOutputTypeDef = TypedDict(
    "ListDeploymentsOutputOutputTypeDef",
    {
        "deployments": List[DeploymentSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentAccountConnectionsOutputOutputTypeDef = TypedDict(
    "ListEnvironmentAccountConnectionsOutputOutputTypeDef",
    {
        "environmentAccountConnections": List[EnvironmentAccountConnectionSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentsOutputOutputTypeDef = TypedDict(
    "ListEnvironmentsOutputOutputTypeDef",
    {
        "environments": List[EnvironmentSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentsInputListEnvironmentsPaginateTypeDef = TypedDict(
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    {
        "environmentTemplates": Sequence[EnvironmentTemplateFilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEnvironmentsInputRequestTypeDef = TypedDict(
    "ListEnvironmentsInputRequestTypeDef",
    {
        "environmentTemplates": Sequence[EnvironmentTemplateFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListEnvironmentTemplatesOutputOutputTypeDef = TypedDict(
    "ListEnvironmentTemplatesOutputOutputTypeDef",
    {
        "nextToken": str,
        "templates": List[EnvironmentTemplateSummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentTemplateVersionsOutputOutputTypeDef = TypedDict(
    "ListEnvironmentTemplateVersionsOutputOutputTypeDef",
    {
        "nextToken": str,
        "templateVersions": List[EnvironmentTemplateVersionSummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetComponentInputComponentDeletedWaitTypeDef = TypedDict(
    "_RequiredGetComponentInputComponentDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetComponentInputComponentDeletedWaitTypeDef = TypedDict(
    "_OptionalGetComponentInputComponentDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetComponentInputComponentDeletedWaitTypeDef(
    _RequiredGetComponentInputComponentDeletedWaitTypeDef,
    _OptionalGetComponentInputComponentDeletedWaitTypeDef,
):
    pass

_RequiredGetComponentInputComponentDeployedWaitTypeDef = TypedDict(
    "_RequiredGetComponentInputComponentDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetComponentInputComponentDeployedWaitTypeDef = TypedDict(
    "_OptionalGetComponentInputComponentDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetComponentInputComponentDeployedWaitTypeDef(
    _RequiredGetComponentInputComponentDeployedWaitTypeDef,
    _OptionalGetComponentInputComponentDeployedWaitTypeDef,
):
    pass

_RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef = TypedDict(
    "_RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef = TypedDict(
    "_OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetEnvironmentInputEnvironmentDeployedWaitTypeDef(
    _RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef,
    _OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef,
):
    pass

_RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef(
    _RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef,
    _OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef,
):
    pass

_RequiredGetServiceInputServiceCreatedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceCreatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceCreatedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServiceCreatedWaitTypeDef(
    _RequiredGetServiceInputServiceCreatedWaitTypeDef,
    _OptionalGetServiceInputServiceCreatedWaitTypeDef,
):
    pass

_RequiredGetServiceInputServiceDeletedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceDeletedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServiceDeletedWaitTypeDef(
    _RequiredGetServiceInputServiceDeletedWaitTypeDef,
    _OptionalGetServiceInputServiceDeletedWaitTypeDef,
):
    pass

_RequiredGetServiceInputServicePipelineDeployedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServicePipelineDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServicePipelineDeployedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServicePipelineDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServicePipelineDeployedWaitTypeDef(
    _RequiredGetServiceInputServicePipelineDeployedWaitTypeDef,
    _OptionalGetServiceInputServicePipelineDeployedWaitTypeDef,
):
    pass

_RequiredGetServiceInputServiceUpdatedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceUpdatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceUpdatedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceUpdatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServiceUpdatedWaitTypeDef(
    _RequiredGetServiceInputServiceUpdatedWaitTypeDef,
    _OptionalGetServiceInputServiceUpdatedWaitTypeDef,
):
    pass

_RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    {
        "name": str,
        "serviceName": str,
    },
)
_OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef(
    _RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef,
    _OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef,
):
    pass

_RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef(
    _RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef,
    _OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef,
):
    pass

ListComponentOutputsOutputOutputTypeDef = TypedDict(
    "ListComponentOutputsOutputOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentOutputsOutputOutputTypeDef = TypedDict(
    "ListEnvironmentOutputsOutputOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServiceInstanceOutputsOutputOutputTypeDef = TypedDict(
    "ListServiceInstanceOutputsOutputOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServicePipelineOutputsOutputOutputTypeDef = TypedDict(
    "ListServicePipelineOutputsOutputOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListComponentProvisionedResourcesOutputOutputTypeDef = TypedDict(
    "ListComponentProvisionedResourcesOutputOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentProvisionedResourcesOutputOutputTypeDef = TypedDict(
    "ListEnvironmentProvisionedResourcesOutputOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServiceInstanceProvisionedResourcesOutputOutputTypeDef = TypedDict(
    "ListServiceInstanceProvisionedResourcesOutputOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServicePipelineProvisionedResourcesOutputOutputTypeDef = TypedDict(
    "ListServicePipelineProvisionedResourcesOutputOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRepositoriesOutputOutputTypeDef = TypedDict(
    "ListRepositoriesOutputOutputTypeDef",
    {
        "nextToken": str,
        "repositories": List[RepositorySummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRepositorySyncDefinitionsOutputOutputTypeDef = TypedDict(
    "ListRepositorySyncDefinitionsOutputOutputTypeDef",
    {
        "nextToken": str,
        "syncDefinitions": List[RepositorySyncDefinitionOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServiceInstancesInputListServiceInstancesPaginateTypeDef = TypedDict(
    "ListServiceInstancesInputListServiceInstancesPaginateTypeDef",
    {
        "filters": Sequence[ListServiceInstancesFilterTypeDef],
        "serviceName": str,
        "sortBy": ListServiceInstancesSortByType,
        "sortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListServiceInstancesInputRequestTypeDef = TypedDict(
    "ListServiceInstancesInputRequestTypeDef",
    {
        "filters": Sequence[ListServiceInstancesFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
        "serviceName": str,
        "sortBy": ListServiceInstancesSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

ListServiceInstancesOutputOutputTypeDef = TypedDict(
    "ListServiceInstancesOutputOutputTypeDef",
    {
        "nextToken": str,
        "serviceInstances": List[ServiceInstanceSummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServiceTemplateVersionsOutputOutputTypeDef = TypedDict(
    "ListServiceTemplateVersionsOutputOutputTypeDef",
    {
        "nextToken": str,
        "templateVersions": List[ServiceTemplateVersionSummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServiceTemplatesOutputOutputTypeDef = TypedDict(
    "ListServiceTemplatesOutputOutputTypeDef",
    {
        "nextToken": str,
        "templates": List[ServiceTemplateSummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServicesOutputOutputTypeDef = TypedDict(
    "ListServicesOutputOutputTypeDef",
    {
        "nextToken": str,
        "services": List[ServiceSummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceOutputOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputOutputTypeDef",
    {
        "nextToken": str,
        "tags": List[TagOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef = TypedDict(
    "_RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef = TypedDict(
    "_OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    {
        "deploymentId": str,
        "outputs": Sequence[OutputTypeDef],
        "status": ResourceDeploymentStatusType,
        "statusMessage": str,
    },
    total=False,
)

class NotifyResourceDeploymentStatusChangeInputRequestTypeDef(
    _RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef,
    _OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef,
):
    pass

RepositorySyncAttemptOutputTypeDef = TypedDict(
    "RepositorySyncAttemptOutputTypeDef",
    {
        "events": List[RepositorySyncEventOutputTypeDef],
        "startedAt": datetime,
        "status": RepositorySyncStatusType,
    },
)

ResourceSyncAttemptOutputTypeDef = TypedDict(
    "ResourceSyncAttemptOutputTypeDef",
    {
        "events": List[ResourceSyncEventOutputTypeDef],
        "initialRevision": RevisionOutputTypeDef,
        "startedAt": datetime,
        "status": ResourceSyncStatusType,
        "target": str,
        "targetRevision": RevisionOutputTypeDef,
    },
)

TemplateVersionSourceInputTypeDef = TypedDict(
    "TemplateVersionSourceInputTypeDef",
    {
        "s3": S3ObjectSourceTypeDef,
    },
    total=False,
)

SyncBlockerOutputTypeDef = TypedDict(
    "SyncBlockerOutputTypeDef",
    {
        "contexts": List[SyncBlockerContextOutputTypeDef],
        "createdAt": datetime,
        "createdReason": str,
        "id": str,
        "resolvedAt": datetime,
        "resolvedReason": str,
        "status": BlockerStatusType,
        "type": Literal["AUTOMATED"],
    },
)

GetAccountSettingsOutputOutputTypeDef = TypedDict(
    "GetAccountSettingsOutputOutputTypeDef",
    {
        "accountSettings": AccountSettingsOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateAccountSettingsOutputOutputTypeDef = TypedDict(
    "UpdateAccountSettingsOutputOutputTypeDef",
    {
        "accountSettings": AccountSettingsOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelEnvironmentDeploymentOutputOutputTypeDef = TypedDict(
    "CancelEnvironmentDeploymentOutputOutputTypeDef",
    {
        "environment": EnvironmentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEnvironmentOutputOutputTypeDef = TypedDict(
    "CreateEnvironmentOutputOutputTypeDef",
    {
        "environment": EnvironmentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentOutputOutputTypeDef = TypedDict(
    "DeleteEnvironmentOutputOutputTypeDef",
    {
        "environment": EnvironmentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEnvironmentOutputOutputTypeDef = TypedDict(
    "GetEnvironmentOutputOutputTypeDef",
    {
        "environment": EnvironmentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEnvironmentOutputOutputTypeDef = TypedDict(
    "UpdateEnvironmentOutputOutputTypeDef",
    {
        "environment": EnvironmentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateServiceOutputOutputTypeDef = TypedDict(
    "CreateServiceOutputOutputTypeDef",
    {
        "service": ServiceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteServiceOutputOutputTypeDef = TypedDict(
    "DeleteServiceOutputOutputTypeDef",
    {
        "service": ServiceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceOutputOutputTypeDef = TypedDict(
    "GetServiceOutputOutputTypeDef",
    {
        "service": ServiceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServiceOutputOutputTypeDef = TypedDict(
    "UpdateServiceOutputOutputTypeDef",
    {
        "service": ServiceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateServiceTemplateVersionOutputOutputTypeDef = TypedDict(
    "CreateServiceTemplateVersionOutputOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteServiceTemplateVersionOutputOutputTypeDef = TypedDict(
    "DeleteServiceTemplateVersionOutputOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceTemplateVersionOutputOutputTypeDef = TypedDict(
    "GetServiceTemplateVersionOutputOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServiceTemplateVersionOutputOutputTypeDef = TypedDict(
    "UpdateServiceTemplateVersionOutputOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResourcesSummaryOutputOutputTypeDef = TypedDict(
    "GetResourcesSummaryOutputOutputTypeDef",
    {
        "counts": CountsSummaryOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeploymentOutputTypeDef = TypedDict(
    "DeploymentOutputTypeDef",
    {
        "arn": str,
        "completedAt": datetime,
        "componentName": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "deploymentStatusMessage": str,
        "environmentName": str,
        "id": str,
        "initialState": DeploymentStateOutputTypeDef,
        "lastAttemptedDeploymentId": str,
        "lastModifiedAt": datetime,
        "lastSucceededDeploymentId": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "targetArn": str,
        "targetResourceCreatedAt": datetime,
        "targetResourceType": DeploymentTargetResourceTypeType,
        "targetState": DeploymentStateOutputTypeDef,
    },
)

GetRepositorySyncStatusOutputOutputTypeDef = TypedDict(
    "GetRepositorySyncStatusOutputOutputTypeDef",
    {
        "latestSync": RepositorySyncAttemptOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceInstanceSyncStatusOutputOutputTypeDef = TypedDict(
    "GetServiceInstanceSyncStatusOutputOutputTypeDef",
    {
        "desiredState": RevisionOutputTypeDef,
        "latestSuccessfulSync": ResourceSyncAttemptOutputTypeDef,
        "latestSync": ResourceSyncAttemptOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTemplateSyncStatusOutputOutputTypeDef = TypedDict(
    "GetTemplateSyncStatusOutputOutputTypeDef",
    {
        "desiredState": RevisionOutputTypeDef,
        "latestSuccessfulSync": ResourceSyncAttemptOutputTypeDef,
        "latestSync": ResourceSyncAttemptOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "source": TemplateVersionSourceInputTypeDef,
        "templateName": str,
    },
)
_OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "majorVersion": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEnvironmentTemplateVersionInputRequestTypeDef(
    _RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef,
    _OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef,
):
    pass

_RequiredCreateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceTemplateVersionInputRequestTypeDef",
    {
        "compatibleEnvironmentTemplates": Sequence[CompatibleEnvironmentTemplateInputTypeDef],
        "source": TemplateVersionSourceInputTypeDef,
        "templateName": str,
    },
)
_OptionalCreateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceTemplateVersionInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "majorVersion": str,
        "supportedComponentSources": Sequence[Literal["DIRECTLY_DEFINED"]],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateServiceTemplateVersionInputRequestTypeDef(
    _RequiredCreateServiceTemplateVersionInputRequestTypeDef,
    _OptionalCreateServiceTemplateVersionInputRequestTypeDef,
):
    pass

ServiceSyncBlockerSummaryOutputTypeDef = TypedDict(
    "ServiceSyncBlockerSummaryOutputTypeDef",
    {
        "latestBlockers": List[SyncBlockerOutputTypeDef],
        "serviceInstanceName": str,
        "serviceName": str,
    },
)

UpdateServiceSyncBlockerOutputOutputTypeDef = TypedDict(
    "UpdateServiceSyncBlockerOutputOutputTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSyncBlocker": SyncBlockerOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteDeploymentOutputOutputTypeDef = TypedDict(
    "DeleteDeploymentOutputOutputTypeDef",
    {
        "deployment": DeploymentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDeploymentOutputOutputTypeDef = TypedDict(
    "GetDeploymentOutputOutputTypeDef",
    {
        "deployment": DeploymentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceSyncBlockerSummaryOutputOutputTypeDef = TypedDict(
    "GetServiceSyncBlockerSummaryOutputOutputTypeDef",
    {
        "serviceSyncBlockerSummary": ServiceSyncBlockerSummaryOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
