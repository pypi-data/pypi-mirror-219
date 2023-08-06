"""
Type annotations for proton service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_proton.client import ProtonClient

    session = Session()
    client: ProtonClient = session.client("proton")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ComponentDeploymentUpdateTypeType,
    DeploymentUpdateTypeType,
    EnvironmentAccountConnectionRequesterAccountTypeType,
    EnvironmentAccountConnectionStatusType,
    ListServiceInstancesSortByType,
    RepositoryProviderType,
    ResourceDeploymentStatusType,
    SortOrderType,
    SyncTypeType,
    TemplateTypeType,
    TemplateVersionStatusType,
)
from .paginator import (
    ListComponentOutputsPaginator,
    ListComponentProvisionedResourcesPaginator,
    ListComponentsPaginator,
    ListDeploymentsPaginator,
    ListEnvironmentAccountConnectionsPaginator,
    ListEnvironmentOutputsPaginator,
    ListEnvironmentProvisionedResourcesPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentTemplatesPaginator,
    ListEnvironmentTemplateVersionsPaginator,
    ListRepositoriesPaginator,
    ListRepositorySyncDefinitionsPaginator,
    ListServiceInstanceOutputsPaginator,
    ListServiceInstanceProvisionedResourcesPaginator,
    ListServiceInstancesPaginator,
    ListServicePipelineOutputsPaginator,
    ListServicePipelineProvisionedResourcesPaginator,
    ListServicesPaginator,
    ListServiceTemplatesPaginator,
    ListServiceTemplateVersionsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AcceptEnvironmentAccountConnectionOutputOutputTypeDef,
    CancelComponentDeploymentOutputOutputTypeDef,
    CancelEnvironmentDeploymentOutputOutputTypeDef,
    CancelServiceInstanceDeploymentOutputOutputTypeDef,
    CancelServicePipelineDeploymentOutputOutputTypeDef,
    CompatibleEnvironmentTemplateInputTypeDef,
    CreateComponentOutputOutputTypeDef,
    CreateEnvironmentAccountConnectionOutputOutputTypeDef,
    CreateEnvironmentOutputOutputTypeDef,
    CreateEnvironmentTemplateOutputOutputTypeDef,
    CreateEnvironmentTemplateVersionOutputOutputTypeDef,
    CreateRepositoryOutputOutputTypeDef,
    CreateServiceInstanceOutputOutputTypeDef,
    CreateServiceOutputOutputTypeDef,
    CreateServiceSyncConfigOutputOutputTypeDef,
    CreateServiceTemplateOutputOutputTypeDef,
    CreateServiceTemplateVersionOutputOutputTypeDef,
    CreateTemplateSyncConfigOutputOutputTypeDef,
    DeleteComponentOutputOutputTypeDef,
    DeleteDeploymentOutputOutputTypeDef,
    DeleteEnvironmentAccountConnectionOutputOutputTypeDef,
    DeleteEnvironmentOutputOutputTypeDef,
    DeleteEnvironmentTemplateOutputOutputTypeDef,
    DeleteEnvironmentTemplateVersionOutputOutputTypeDef,
    DeleteRepositoryOutputOutputTypeDef,
    DeleteServiceOutputOutputTypeDef,
    DeleteServiceSyncConfigOutputOutputTypeDef,
    DeleteServiceTemplateOutputOutputTypeDef,
    DeleteServiceTemplateVersionOutputOutputTypeDef,
    DeleteTemplateSyncConfigOutputOutputTypeDef,
    EnvironmentTemplateFilterTypeDef,
    GetAccountSettingsOutputOutputTypeDef,
    GetComponentOutputOutputTypeDef,
    GetDeploymentOutputOutputTypeDef,
    GetEnvironmentAccountConnectionOutputOutputTypeDef,
    GetEnvironmentOutputOutputTypeDef,
    GetEnvironmentTemplateOutputOutputTypeDef,
    GetEnvironmentTemplateVersionOutputOutputTypeDef,
    GetRepositoryOutputOutputTypeDef,
    GetRepositorySyncStatusOutputOutputTypeDef,
    GetResourcesSummaryOutputOutputTypeDef,
    GetServiceInstanceOutputOutputTypeDef,
    GetServiceInstanceSyncStatusOutputOutputTypeDef,
    GetServiceOutputOutputTypeDef,
    GetServiceSyncBlockerSummaryOutputOutputTypeDef,
    GetServiceSyncConfigOutputOutputTypeDef,
    GetServiceTemplateOutputOutputTypeDef,
    GetServiceTemplateVersionOutputOutputTypeDef,
    GetTemplateSyncConfigOutputOutputTypeDef,
    GetTemplateSyncStatusOutputOutputTypeDef,
    ListComponentOutputsOutputOutputTypeDef,
    ListComponentProvisionedResourcesOutputOutputTypeDef,
    ListComponentsOutputOutputTypeDef,
    ListDeploymentsOutputOutputTypeDef,
    ListEnvironmentAccountConnectionsOutputOutputTypeDef,
    ListEnvironmentOutputsOutputOutputTypeDef,
    ListEnvironmentProvisionedResourcesOutputOutputTypeDef,
    ListEnvironmentsOutputOutputTypeDef,
    ListEnvironmentTemplatesOutputOutputTypeDef,
    ListEnvironmentTemplateVersionsOutputOutputTypeDef,
    ListRepositoriesOutputOutputTypeDef,
    ListRepositorySyncDefinitionsOutputOutputTypeDef,
    ListServiceInstanceOutputsOutputOutputTypeDef,
    ListServiceInstanceProvisionedResourcesOutputOutputTypeDef,
    ListServiceInstancesFilterTypeDef,
    ListServiceInstancesOutputOutputTypeDef,
    ListServicePipelineOutputsOutputOutputTypeDef,
    ListServicePipelineProvisionedResourcesOutputOutputTypeDef,
    ListServicesOutputOutputTypeDef,
    ListServiceTemplatesOutputOutputTypeDef,
    ListServiceTemplateVersionsOutputOutputTypeDef,
    ListTagsForResourceOutputOutputTypeDef,
    OutputTypeDef,
    RejectEnvironmentAccountConnectionOutputOutputTypeDef,
    RepositoryBranchInputTypeDef,
    TagTypeDef,
    TemplateVersionSourceInputTypeDef,
    UpdateAccountSettingsOutputOutputTypeDef,
    UpdateComponentOutputOutputTypeDef,
    UpdateEnvironmentAccountConnectionOutputOutputTypeDef,
    UpdateEnvironmentOutputOutputTypeDef,
    UpdateEnvironmentTemplateOutputOutputTypeDef,
    UpdateEnvironmentTemplateVersionOutputOutputTypeDef,
    UpdateServiceInstanceOutputOutputTypeDef,
    UpdateServiceOutputOutputTypeDef,
    UpdateServicePipelineOutputOutputTypeDef,
    UpdateServiceSyncBlockerOutputOutputTypeDef,
    UpdateServiceSyncConfigOutputOutputTypeDef,
    UpdateServiceTemplateOutputOutputTypeDef,
    UpdateServiceTemplateVersionOutputOutputTypeDef,
    UpdateTemplateSyncConfigOutputOutputTypeDef,
)
from .waiter import (
    ComponentDeletedWaiter,
    ComponentDeployedWaiter,
    EnvironmentDeployedWaiter,
    EnvironmentTemplateVersionRegisteredWaiter,
    ServiceCreatedWaiter,
    ServiceDeletedWaiter,
    ServiceInstanceDeployedWaiter,
    ServicePipelineDeployedWaiter,
    ServiceTemplateVersionRegisteredWaiter,
    ServiceUpdatedWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ProtonClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ProtonClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ProtonClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#exceptions)
        """

    def accept_environment_account_connection(
        self, *, id: str
    ) -> AcceptEnvironmentAccountConnectionOutputOutputTypeDef:
        """
        In a management account, an environment account connection request is accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.accept_environment_account_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#accept_environment_account_connection)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#can_paginate)
        """

    def cancel_component_deployment(
        self, *, componentName: str
    ) -> CancelComponentDeploymentOutputOutputTypeDef:
        """
        Attempts to cancel a component deployment (for a component that is in the
        `IN_PROGRESS` deployment status).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.cancel_component_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#cancel_component_deployment)
        """

    def cancel_environment_deployment(
        self, *, environmentName: str
    ) -> CancelEnvironmentDeploymentOutputOutputTypeDef:
        """
        Attempts to cancel an environment deployment on an  UpdateEnvironment action, if
        the deployment is `IN_PROGRESS`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.cancel_environment_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#cancel_environment_deployment)
        """

    def cancel_service_instance_deployment(
        self, *, serviceInstanceName: str, serviceName: str
    ) -> CancelServiceInstanceDeploymentOutputOutputTypeDef:
        """
        Attempts to cancel a service instance deployment on an  UpdateServiceInstance
        action, if the deployment is `IN_PROGRESS`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.cancel_service_instance_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#cancel_service_instance_deployment)
        """

    def cancel_service_pipeline_deployment(
        self, *, serviceName: str
    ) -> CancelServicePipelineDeploymentOutputOutputTypeDef:
        """
        Attempts to cancel a service pipeline deployment on an  UpdateServicePipeline
        action, if the deployment is `IN_PROGRESS`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.cancel_service_pipeline_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#cancel_service_pipeline_deployment)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#close)
        """

    def create_component(
        self,
        *,
        manifest: str,
        name: str,
        templateFile: str,
        clientToken: str = ...,
        description: str = ...,
        environmentName: str = ...,
        serviceInstanceName: str = ...,
        serviceName: str = ...,
        serviceSpec: str = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateComponentOutputOutputTypeDef:
        """
        Create an Proton component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_component)
        """

    def create_environment(
        self,
        *,
        name: str,
        spec: str,
        templateMajorVersion: str,
        templateName: str,
        codebuildRoleArn: str = ...,
        componentRoleArn: str = ...,
        description: str = ...,
        environmentAccountConnectionId: str = ...,
        protonServiceRoleArn: str = ...,
        provisioningRepository: RepositoryBranchInputTypeDef = ...,
        tags: Sequence[TagTypeDef] = ...,
        templateMinorVersion: str = ...
    ) -> CreateEnvironmentOutputOutputTypeDef:
        """
        Deploy a new environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_environment)
        """

    def create_environment_account_connection(
        self,
        *,
        environmentName: str,
        managementAccountId: str,
        clientToken: str = ...,
        codebuildRoleArn: str = ...,
        componentRoleArn: str = ...,
        roleArn: str = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateEnvironmentAccountConnectionOutputOutputTypeDef:
        """
        Create an environment account connection in an environment account so that
        environment infrastructure resources can be provisioned in the environment
        account from a management account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment_account_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_environment_account_connection)
        """

    def create_environment_template(
        self,
        *,
        name: str,
        description: str = ...,
        displayName: str = ...,
        encryptionKey: str = ...,
        provisioning: Literal["CUSTOMER_MANAGED"] = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateEnvironmentTemplateOutputOutputTypeDef:
        """
        Create an environment template for Proton.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_environment_template)
        """

    def create_environment_template_version(
        self,
        *,
        source: TemplateVersionSourceInputTypeDef,
        templateName: str,
        clientToken: str = ...,
        description: str = ...,
        majorVersion: str = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateEnvironmentTemplateVersionOutputOutputTypeDef:
        """
        Create a new major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_environment_template_version)
        """

    def create_repository(
        self,
        *,
        connectionArn: str,
        name: str,
        provider: RepositoryProviderType,
        encryptionKey: str = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateRepositoryOutputOutputTypeDef:
        """
        Create and register a link to a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_repository)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_repository)
        """

    def create_service(
        self,
        *,
        name: str,
        spec: str,
        templateMajorVersion: str,
        templateName: str,
        branchName: str = ...,
        description: str = ...,
        repositoryConnectionArn: str = ...,
        repositoryId: str = ...,
        tags: Sequence[TagTypeDef] = ...,
        templateMinorVersion: str = ...
    ) -> CreateServiceOutputOutputTypeDef:
        """
        Create an Proton service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_service)
        """

    def create_service_instance(
        self,
        *,
        name: str,
        serviceName: str,
        spec: str,
        clientToken: str = ...,
        tags: Sequence[TagTypeDef] = ...,
        templateMajorVersion: str = ...,
        templateMinorVersion: str = ...
    ) -> CreateServiceInstanceOutputOutputTypeDef:
        """
        Create a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_service_instance)
        """

    def create_service_sync_config(
        self,
        *,
        branch: str,
        filePath: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        serviceName: str
    ) -> CreateServiceSyncConfigOutputOutputTypeDef:
        """
        Create the Proton Ops configuration file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_service_sync_config)
        """

    def create_service_template(
        self,
        *,
        name: str,
        description: str = ...,
        displayName: str = ...,
        encryptionKey: str = ...,
        pipelineProvisioning: Literal["CUSTOMER_MANAGED"] = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateServiceTemplateOutputOutputTypeDef:
        """
        Create a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_service_template)
        """

    def create_service_template_version(
        self,
        *,
        compatibleEnvironmentTemplates: Sequence[CompatibleEnvironmentTemplateInputTypeDef],
        source: TemplateVersionSourceInputTypeDef,
        templateName: str,
        clientToken: str = ...,
        description: str = ...,
        majorVersion: str = ...,
        supportedComponentSources: Sequence[Literal["DIRECTLY_DEFINED"]] = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateServiceTemplateVersionOutputOutputTypeDef:
        """
        Create a new major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_service_template_version)
        """

    def create_template_sync_config(
        self,
        *,
        branch: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        templateName: str,
        templateType: TemplateTypeType,
        subdirectory: str = ...
    ) -> CreateTemplateSyncConfigOutputOutputTypeDef:
        """
        Set up a template to create new template versions automatically by tracking a
        linked repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_template_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#create_template_sync_config)
        """

    def delete_component(self, *, name: str) -> DeleteComponentOutputOutputTypeDef:
        """
        Delete an Proton component resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_component)
        """

    def delete_deployment(self, *, id: str) -> DeleteDeploymentOutputOutputTypeDef:
        """
        Delete the deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_deployment)
        """

    def delete_environment(self, *, name: str) -> DeleteEnvironmentOutputOutputTypeDef:
        """
        Delete an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_environment)
        """

    def delete_environment_account_connection(
        self, *, id: str
    ) -> DeleteEnvironmentAccountConnectionOutputOutputTypeDef:
        """
        In an environment account, delete an environment account connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment_account_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_environment_account_connection)
        """

    def delete_environment_template(
        self, *, name: str
    ) -> DeleteEnvironmentTemplateOutputOutputTypeDef:
        """
        If no other major or minor versions of an environment template exist, delete the
        environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_environment_template)
        """

    def delete_environment_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> DeleteEnvironmentTemplateVersionOutputOutputTypeDef:
        """
        If no other minor versions of an environment template exist, delete a major
        version of the environment template if it's not the `Recommended` version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_environment_template_version)
        """

    def delete_repository(
        self, *, name: str, provider: RepositoryProviderType
    ) -> DeleteRepositoryOutputOutputTypeDef:
        """
        De-register and unlink your repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_repository)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_repository)
        """

    def delete_service(self, *, name: str) -> DeleteServiceOutputOutputTypeDef:
        """
        Delete a service, with its instances and pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_service)
        """

    def delete_service_sync_config(
        self, *, serviceName: str
    ) -> DeleteServiceSyncConfigOutputOutputTypeDef:
        """
        Delete the Proton Ops file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_service_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_service_sync_config)
        """

    def delete_service_template(self, *, name: str) -> DeleteServiceTemplateOutputOutputTypeDef:
        """
        If no other major or minor versions of the service template exist, delete the
        service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_service_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_service_template)
        """

    def delete_service_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> DeleteServiceTemplateVersionOutputOutputTypeDef:
        """
        If no other minor versions of a service template exist, delete a major version
        of the service template if it's not the `Recommended` version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_service_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_service_template_version)
        """

    def delete_template_sync_config(
        self, *, templateName: str, templateType: TemplateTypeType
    ) -> DeleteTemplateSyncConfigOutputOutputTypeDef:
        """
        Delete a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_template_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#delete_template_sync_config)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#generate_presigned_url)
        """

    def get_account_settings(self) -> GetAccountSettingsOutputOutputTypeDef:
        """
        Get detail data for Proton account-wide settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_account_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_account_settings)
        """

    def get_component(self, *, name: str) -> GetComponentOutputOutputTypeDef:
        """
        Get detailed data for a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_component)
        """

    def get_deployment(
        self,
        *,
        id: str,
        componentName: str = ...,
        environmentName: str = ...,
        serviceInstanceName: str = ...,
        serviceName: str = ...
    ) -> GetDeploymentOutputOutputTypeDef:
        """
        Get detailed data for a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_deployment)
        """

    def get_environment(self, *, name: str) -> GetEnvironmentOutputOutputTypeDef:
        """
        Get detailed data for an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_environment)
        """

    def get_environment_account_connection(
        self, *, id: str
    ) -> GetEnvironmentAccountConnectionOutputOutputTypeDef:
        """
        In an environment account, get the detailed data for an environment account
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment_account_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_environment_account_connection)
        """

    def get_environment_template(self, *, name: str) -> GetEnvironmentTemplateOutputOutputTypeDef:
        """
        Get detailed data for an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_environment_template)
        """

    def get_environment_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> GetEnvironmentTemplateVersionOutputOutputTypeDef:
        """
        Get detailed data for a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_environment_template_version)
        """

    def get_repository(
        self, *, name: str, provider: RepositoryProviderType
    ) -> GetRepositoryOutputOutputTypeDef:
        """
        Get detail data for a linked repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_repository)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_repository)
        """

    def get_repository_sync_status(
        self,
        *,
        branch: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        syncType: SyncTypeType
    ) -> GetRepositorySyncStatusOutputOutputTypeDef:
        """
        Get the sync status of a repository used for Proton template sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_repository_sync_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_repository_sync_status)
        """

    def get_resources_summary(self) -> GetResourcesSummaryOutputOutputTypeDef:
        """
        Get counts of Proton resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_resources_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_resources_summary)
        """

    def get_service(self, *, name: str) -> GetServiceOutputOutputTypeDef:
        """
        Get detailed data for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_service)
        """

    def get_service_instance(
        self, *, name: str, serviceName: str
    ) -> GetServiceInstanceOutputOutputTypeDef:
        """
        Get detailed data for a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_service_instance)
        """

    def get_service_instance_sync_status(
        self, *, serviceInstanceName: str, serviceName: str
    ) -> GetServiceInstanceSyncStatusOutputOutputTypeDef:
        """
        Get the status of the synced service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_instance_sync_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_service_instance_sync_status)
        """

    def get_service_sync_blocker_summary(
        self, *, serviceName: str, serviceInstanceName: str = ...
    ) -> GetServiceSyncBlockerSummaryOutputOutputTypeDef:
        """
        Get detailed data for the service sync blocker summary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_sync_blocker_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_service_sync_blocker_summary)
        """

    def get_service_sync_config(
        self, *, serviceName: str
    ) -> GetServiceSyncConfigOutputOutputTypeDef:
        """
        Get detailed information for the service sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_service_sync_config)
        """

    def get_service_template(self, *, name: str) -> GetServiceTemplateOutputOutputTypeDef:
        """
        Get detailed data for a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_service_template)
        """

    def get_service_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> GetServiceTemplateVersionOutputOutputTypeDef:
        """
        Get detailed data for a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_service_template_version)
        """

    def get_template_sync_config(
        self, *, templateName: str, templateType: TemplateTypeType
    ) -> GetTemplateSyncConfigOutputOutputTypeDef:
        """
        Get detail data for a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_template_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_template_sync_config)
        """

    def get_template_sync_status(
        self, *, templateName: str, templateType: TemplateTypeType, templateVersion: str
    ) -> GetTemplateSyncStatusOutputOutputTypeDef:
        """
        Get the status of a template sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_template_sync_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_template_sync_status)
        """

    def list_component_outputs(
        self, *, componentName: str, deploymentId: str = ..., nextToken: str = ...
    ) -> ListComponentOutputsOutputOutputTypeDef:
        """
        Get a list of component Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_component_outputs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_component_outputs)
        """

    def list_component_provisioned_resources(
        self, *, componentName: str, nextToken: str = ...
    ) -> ListComponentProvisionedResourcesOutputOutputTypeDef:
        """
        List provisioned resources for a component with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_component_provisioned_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_component_provisioned_resources)
        """

    def list_components(
        self,
        *,
        environmentName: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        serviceInstanceName: str = ...,
        serviceName: str = ...
    ) -> ListComponentsOutputOutputTypeDef:
        """
        List components with summary data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_components)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_components)
        """

    def list_deployments(
        self,
        *,
        componentName: str = ...,
        environmentName: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        serviceInstanceName: str = ...,
        serviceName: str = ...
    ) -> ListDeploymentsOutputOutputTypeDef:
        """
        List deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_deployments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_deployments)
        """

    def list_environment_account_connections(
        self,
        *,
        requestedBy: EnvironmentAccountConnectionRequesterAccountTypeType,
        environmentName: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        statuses: Sequence[EnvironmentAccountConnectionStatusType] = ...
    ) -> ListEnvironmentAccountConnectionsOutputOutputTypeDef:
        """
        View a list of environment account connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_account_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_environment_account_connections)
        """

    def list_environment_outputs(
        self, *, environmentName: str, deploymentId: str = ..., nextToken: str = ...
    ) -> ListEnvironmentOutputsOutputOutputTypeDef:
        """
        List the infrastructure as code outputs for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_outputs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_environment_outputs)
        """

    def list_environment_provisioned_resources(
        self, *, environmentName: str, nextToken: str = ...
    ) -> ListEnvironmentProvisionedResourcesOutputOutputTypeDef:
        """
        List the provisioned resources for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_provisioned_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_environment_provisioned_resources)
        """

    def list_environment_template_versions(
        self,
        *,
        templateName: str,
        majorVersion: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListEnvironmentTemplateVersionsOutputOutputTypeDef:
        """
        List major or minor versions of an environment template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_template_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_environment_template_versions)
        """

    def list_environment_templates(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListEnvironmentTemplatesOutputOutputTypeDef:
        """
        List environment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_environment_templates)
        """

    def list_environments(
        self,
        *,
        environmentTemplates: Sequence[EnvironmentTemplateFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListEnvironmentsOutputOutputTypeDef:
        """
        List environments with detail data summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_environments)
        """

    def list_repositories(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListRepositoriesOutputOutputTypeDef:
        """
        List linked repositories with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_repositories)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_repositories)
        """

    def list_repository_sync_definitions(
        self,
        *,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        syncType: SyncTypeType,
        nextToken: str = ...
    ) -> ListRepositorySyncDefinitionsOutputOutputTypeDef:
        """
        List repository sync definitions with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_repository_sync_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_repository_sync_definitions)
        """

    def list_service_instance_outputs(
        self,
        *,
        serviceInstanceName: str,
        serviceName: str,
        deploymentId: str = ...,
        nextToken: str = ...
    ) -> ListServiceInstanceOutputsOutputOutputTypeDef:
        """
        Get a list service of instance Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_instance_outputs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_service_instance_outputs)
        """

    def list_service_instance_provisioned_resources(
        self, *, serviceInstanceName: str, serviceName: str, nextToken: str = ...
    ) -> ListServiceInstanceProvisionedResourcesOutputOutputTypeDef:
        """
        List provisioned resources for a service instance with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_instance_provisioned_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_service_instance_provisioned_resources)
        """

    def list_service_instances(
        self,
        *,
        filters: Sequence[ListServiceInstancesFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        serviceName: str = ...,
        sortBy: ListServiceInstancesSortByType = ...,
        sortOrder: SortOrderType = ...
    ) -> ListServiceInstancesOutputOutputTypeDef:
        """
        List service instances with summary data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_service_instances)
        """

    def list_service_pipeline_outputs(
        self, *, serviceName: str, deploymentId: str = ..., nextToken: str = ...
    ) -> ListServicePipelineOutputsOutputOutputTypeDef:
        """
        Get a list of service pipeline Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_pipeline_outputs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_service_pipeline_outputs)
        """

    def list_service_pipeline_provisioned_resources(
        self, *, serviceName: str, nextToken: str = ...
    ) -> ListServicePipelineProvisionedResourcesOutputOutputTypeDef:
        """
        List provisioned resources for a service and pipeline with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_pipeline_provisioned_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_service_pipeline_provisioned_resources)
        """

    def list_service_template_versions(
        self,
        *,
        templateName: str,
        majorVersion: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListServiceTemplateVersionsOutputOutputTypeDef:
        """
        List major or minor versions of a service template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_template_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_service_template_versions)
        """

    def list_service_templates(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListServiceTemplatesOutputOutputTypeDef:
        """
        List service templates with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_service_templates)
        """

    def list_services(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListServicesOutputOutputTypeDef:
        """
        List services with summaries of detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_services)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_services)
        """

    def list_tags_for_resource(
        self, *, resourceArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListTagsForResourceOutputOutputTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#list_tags_for_resource)
        """

    def notify_resource_deployment_status_change(
        self,
        *,
        resourceArn: str,
        deploymentId: str = ...,
        outputs: Sequence[OutputTypeDef] = ...,
        status: ResourceDeploymentStatusType = ...,
        statusMessage: str = ...
    ) -> Dict[str, Any]:
        """
        Notify Proton of status changes to a provisioned resource when you use self-
        managed provisioning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.notify_resource_deployment_status_change)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#notify_resource_deployment_status_change)
        """

    def reject_environment_account_connection(
        self, *, id: str
    ) -> RejectEnvironmentAccountConnectionOutputOutputTypeDef:
        """
        In a management account, reject an environment account connection from another
        environment account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.reject_environment_account_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#reject_environment_account_connection)
        """

    def tag_resource(self, *, resourceArn: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove a customer tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#untag_resource)
        """

    def update_account_settings(
        self,
        *,
        deletePipelineProvisioningRepository: bool = ...,
        pipelineCodebuildRoleArn: str = ...,
        pipelineProvisioningRepository: RepositoryBranchInputTypeDef = ...,
        pipelineServiceRoleArn: str = ...
    ) -> UpdateAccountSettingsOutputOutputTypeDef:
        """
        Update Proton settings that are used for multiple services in the Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_account_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_account_settings)
        """

    def update_component(
        self,
        *,
        deploymentType: ComponentDeploymentUpdateTypeType,
        name: str,
        clientToken: str = ...,
        description: str = ...,
        serviceInstanceName: str = ...,
        serviceName: str = ...,
        serviceSpec: str = ...,
        templateFile: str = ...
    ) -> UpdateComponentOutputOutputTypeDef:
        """
        Update a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_component)
        """

    def update_environment(
        self,
        *,
        deploymentType: DeploymentUpdateTypeType,
        name: str,
        codebuildRoleArn: str = ...,
        componentRoleArn: str = ...,
        description: str = ...,
        environmentAccountConnectionId: str = ...,
        protonServiceRoleArn: str = ...,
        provisioningRepository: RepositoryBranchInputTypeDef = ...,
        spec: str = ...,
        templateMajorVersion: str = ...,
        templateMinorVersion: str = ...
    ) -> UpdateEnvironmentOutputOutputTypeDef:
        """
        Update an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_environment)
        """

    def update_environment_account_connection(
        self,
        *,
        id: str,
        codebuildRoleArn: str = ...,
        componentRoleArn: str = ...,
        roleArn: str = ...
    ) -> UpdateEnvironmentAccountConnectionOutputOutputTypeDef:
        """
        In an environment account, update an environment account connection to use a new
        IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment_account_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_environment_account_connection)
        """

    def update_environment_template(
        self, *, name: str, description: str = ..., displayName: str = ...
    ) -> UpdateEnvironmentTemplateOutputOutputTypeDef:
        """
        Update an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_environment_template)
        """

    def update_environment_template_version(
        self,
        *,
        majorVersion: str,
        minorVersion: str,
        templateName: str,
        description: str = ...,
        status: TemplateVersionStatusType = ...
    ) -> UpdateEnvironmentTemplateVersionOutputOutputTypeDef:
        """
        Update a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_environment_template_version)
        """

    def update_service(
        self, *, name: str, description: str = ..., spec: str = ...
    ) -> UpdateServiceOutputOutputTypeDef:
        """
        Edit a service description or use a spec to add and delete service instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_service)
        """

    def update_service_instance(
        self,
        *,
        deploymentType: DeploymentUpdateTypeType,
        name: str,
        serviceName: str,
        clientToken: str = ...,
        spec: str = ...,
        templateMajorVersion: str = ...,
        templateMinorVersion: str = ...
    ) -> UpdateServiceInstanceOutputOutputTypeDef:
        """
        Update a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_service_instance)
        """

    def update_service_pipeline(
        self,
        *,
        deploymentType: DeploymentUpdateTypeType,
        serviceName: str,
        spec: str,
        templateMajorVersion: str = ...,
        templateMinorVersion: str = ...
    ) -> UpdateServicePipelineOutputOutputTypeDef:
        """
        Update the service pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_service_pipeline)
        """

    def update_service_sync_blocker(
        self, *, id: str, resolvedReason: str
    ) -> UpdateServiceSyncBlockerOutputOutputTypeDef:
        """
        Update the service sync blocker by resolving it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_sync_blocker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_service_sync_blocker)
        """

    def update_service_sync_config(
        self,
        *,
        branch: str,
        filePath: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        serviceName: str
    ) -> UpdateServiceSyncConfigOutputOutputTypeDef:
        """
        Update the Proton Ops config file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_service_sync_config)
        """

    def update_service_template(
        self, *, name: str, description: str = ..., displayName: str = ...
    ) -> UpdateServiceTemplateOutputOutputTypeDef:
        """
        Update a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_service_template)
        """

    def update_service_template_version(
        self,
        *,
        majorVersion: str,
        minorVersion: str,
        templateName: str,
        compatibleEnvironmentTemplates: Sequence[CompatibleEnvironmentTemplateInputTypeDef] = ...,
        description: str = ...,
        status: TemplateVersionStatusType = ...,
        supportedComponentSources: Sequence[Literal["DIRECTLY_DEFINED"]] = ...
    ) -> UpdateServiceTemplateVersionOutputOutputTypeDef:
        """
        Update a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_template_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_service_template_version)
        """

    def update_template_sync_config(
        self,
        *,
        branch: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        templateName: str,
        templateType: TemplateTypeType,
        subdirectory: str = ...
    ) -> UpdateTemplateSyncConfigOutputOutputTypeDef:
        """
        Update template sync configuration parameters, except for the `templateName` and
        `templateType`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_template_sync_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#update_template_sync_config)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_component_outputs"]
    ) -> ListComponentOutputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_component_provisioned_resources"]
    ) -> ListComponentProvisionedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_account_connections"]
    ) -> ListEnvironmentAccountConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_outputs"]
    ) -> ListEnvironmentOutputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_provisioned_resources"]
    ) -> ListEnvironmentProvisionedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_template_versions"]
    ) -> ListEnvironmentTemplateVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_templates"]
    ) -> ListEnvironmentTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repository_sync_definitions"]
    ) -> ListRepositorySyncDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instance_outputs"]
    ) -> ListServiceInstanceOutputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instance_provisioned_resources"]
    ) -> ListServiceInstanceProvisionedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instances"]
    ) -> ListServiceInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_pipeline_outputs"]
    ) -> ListServicePipelineOutputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_pipeline_provisioned_resources"]
    ) -> ListServicePipelineProvisionedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_template_versions"]
    ) -> ListServiceTemplateVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_templates"]
    ) -> ListServiceTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["component_deleted"]) -> ComponentDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["component_deployed"]) -> ComponentDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["environment_deployed"]) -> EnvironmentDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["environment_template_version_registered"]
    ) -> EnvironmentTemplateVersionRegisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["service_created"]) -> ServiceCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["service_deleted"]) -> ServiceDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["service_instance_deployed"]
    ) -> ServiceInstanceDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["service_pipeline_deployed"]
    ) -> ServicePipelineDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["service_template_version_registered"]
    ) -> ServiceTemplateVersionRegisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["service_updated"]) -> ServiceUpdatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/client/#get_waiter)
        """
