"""
Type annotations for sagemaker service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker.type_defs import ActionSourceTypeDef

    data: ActionSourceTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionStatusType,
    AggregationTransformationValueType,
    AlgorithmSortByType,
    AlgorithmStatusType,
    AppImageConfigSortKeyType,
    AppInstanceTypeType,
    AppNetworkAccessTypeType,
    AppSecurityGroupManagementType,
    AppStatusType,
    AppTypeType,
    ArtifactSourceIdTypeType,
    AssemblyTypeType,
    AssociationEdgeTypeType,
    AsyncNotificationTopicTypesType,
    AthenaResultCompressionTypeType,
    AthenaResultFormatType,
    AuthModeType,
    AutoMLAlgorithmType,
    AutoMLChannelTypeType,
    AutoMLJobObjectiveTypeType,
    AutoMLJobSecondaryStatusType,
    AutoMLJobStatusType,
    AutoMLMetricEnumType,
    AutoMLMetricExtendedEnumType,
    AutoMLModeType,
    AutoMLProblemTypeConfigNameType,
    AutoMLProcessingUnitType,
    AutoMLS3DataTypeType,
    AutoMLSortByType,
    AutoMLSortOrderType,
    AwsManagedHumanLoopRequestSourceType,
    BatchStrategyType,
    BooleanOperatorType,
    CandidateSortByType,
    CandidateStatusType,
    CandidateStepTypeType,
    CapacitySizeTypeType,
    CaptureModeType,
    CaptureStatusType,
    ClarifyFeatureTypeType,
    ClarifyTextGranularityType,
    ClarifyTextLanguageType,
    CodeRepositorySortByType,
    CodeRepositorySortOrderType,
    CompilationJobStatusType,
    CompleteOnConvergenceType,
    CompressionTypeType,
    ConditionOutcomeType,
    ContainerModeType,
    ContentClassifierType,
    DataDistributionTypeType,
    DetailedAlgorithmStatusType,
    DetailedModelPackageStatusType,
    DeviceDeploymentStatusType,
    DeviceSubsetTypeType,
    DirectInternetAccessType,
    DirectionType,
    DomainStatusType,
    EdgePackagingJobStatusType,
    EdgePresetDeploymentStatusType,
    EndpointConfigSortKeyType,
    EndpointSortKeyType,
    EndpointStatusType,
    ExecutionRoleIdentityConfigType,
    ExecutionStatusType,
    FailureHandlingPolicyType,
    FeatureGroupSortByType,
    FeatureGroupSortOrderType,
    FeatureGroupStatusType,
    FeatureStatusType,
    FeatureTypeType,
    FileSystemAccessModeType,
    FileSystemTypeType,
    FillingTypeType,
    FlowDefinitionStatusType,
    FrameworkType,
    HubContentSortByType,
    HubContentStatusType,
    HubContentTypeType,
    HubSortByType,
    HubStatusType,
    HumanTaskUiStatusType,
    HyperParameterScalingTypeType,
    HyperParameterTuningJobObjectiveTypeType,
    HyperParameterTuningJobSortByOptionsType,
    HyperParameterTuningJobStatusType,
    HyperParameterTuningJobStrategyTypeType,
    HyperParameterTuningJobWarmStartTypeType,
    ImageSortByType,
    ImageSortOrderType,
    ImageStatusType,
    ImageVersionSortByType,
    ImageVersionSortOrderType,
    ImageVersionStatusType,
    InferenceExecutionModeType,
    InferenceExperimentStatusType,
    InferenceExperimentStopDesiredStateType,
    InputModeType,
    InstanceTypeType,
    JobTypeType,
    JoinSourceType,
    LabelingJobStatusType,
    LastUpdateStatusValueType,
    LineageTypeType,
    ListCompilationJobsSortByType,
    ListDeviceFleetsSortByType,
    ListEdgeDeploymentPlansSortByType,
    ListEdgePackagingJobsSortByType,
    ListInferenceRecommendationsJobsSortByType,
    ListWorkforcesSortByOptionsType,
    ListWorkteamsSortByOptionsType,
    MetricSetSourceType,
    ModelApprovalStatusType,
    ModelCacheSettingType,
    ModelCardExportJobSortByType,
    ModelCardExportJobSortOrderType,
    ModelCardExportJobStatusType,
    ModelCardProcessingStatusType,
    ModelCardSortByType,
    ModelCardSortOrderType,
    ModelCardStatusType,
    ModelCompressionTypeType,
    ModelMetadataFilterTypeType,
    ModelPackageGroupSortByType,
    ModelPackageGroupStatusType,
    ModelPackageSortByType,
    ModelPackageStatusType,
    ModelPackageTypeType,
    ModelSortKeyType,
    ModelVariantActionType,
    ModelVariantStatusType,
    MonitoringAlertHistorySortKeyType,
    MonitoringAlertStatusType,
    MonitoringExecutionSortKeyType,
    MonitoringJobDefinitionSortKeyType,
    MonitoringProblemTypeType,
    MonitoringScheduleSortKeyType,
    MonitoringTypeType,
    NotebookInstanceAcceleratorTypeType,
    NotebookInstanceLifecycleConfigSortKeyType,
    NotebookInstanceLifecycleConfigSortOrderType,
    NotebookInstanceSortKeyType,
    NotebookInstanceSortOrderType,
    NotebookInstanceStatusType,
    NotebookOutputOptionType,
    ObjectiveStatusType,
    OfflineStoreStatusValueType,
    OperatorType,
    OrderKeyType,
    OutputCompressionTypeType,
    ParameterTypeType,
    PipelineExecutionStatusType,
    ProblemTypeType,
    ProcessingInstanceTypeType,
    ProcessingJobStatusType,
    ProcessingS3CompressionTypeType,
    ProcessingS3DataDistributionTypeType,
    ProcessingS3DataTypeType,
    ProcessingS3InputModeType,
    ProcessingS3UploadModeType,
    ProcessorType,
    ProductionVariantAcceleratorTypeType,
    ProductionVariantInstanceTypeType,
    ProfilingStatusType,
    ProjectSortByType,
    ProjectSortOrderType,
    ProjectStatusType,
    RecommendationJobStatusType,
    RecommendationJobSupportedEndpointTypeType,
    RecommendationJobTypeType,
    RecommendationStatusType,
    RecordWrapperType,
    RedshiftResultCompressionTypeType,
    RedshiftResultFormatType,
    RepositoryAccessModeType,
    ResourceTypeType,
    RetentionTypeType,
    RootAccessType,
    RStudioServerProAccessStatusType,
    RStudioServerProUserGroupType,
    RuleEvaluationStatusType,
    S3DataDistributionType,
    S3DataTypeType,
    S3ModelDataTypeType,
    SagemakerServicecatalogStatusType,
    ScheduleStatusType,
    SearchSortOrderType,
    SecondaryStatusType,
    SortActionsByType,
    SortAssociationsByType,
    SortByType,
    SortContextsByType,
    SortExperimentsByType,
    SortInferenceExperimentsByType,
    SortLineageGroupsByType,
    SortOrderType,
    SortPipelineExecutionsByType,
    SortPipelinesByType,
    SortTrialComponentsByType,
    SortTrialsByType,
    SpaceSortKeyType,
    SpaceStatusType,
    SplitTypeType,
    StageStatusType,
    StepStatusType,
    StudioLifecycleConfigAppTypeType,
    StudioLifecycleConfigSortKeyType,
    TableFormatType,
    TargetDeviceType,
    TargetPlatformAcceleratorType,
    TargetPlatformArchType,
    TargetPlatformOsType,
    TrafficRoutingConfigTypeType,
    TrainingInputModeType,
    TrainingInstanceTypeType,
    TrainingJobEarlyStoppingTypeType,
    TrainingJobSortByOptionsType,
    TrainingJobStatusType,
    TrainingRepositoryAccessModeType,
    TransformInstanceTypeType,
    TransformJobStatusType,
    TrialComponentPrimaryStatusType,
    TtlDurationUnitType,
    UserProfileSortKeyType,
    UserProfileStatusType,
    VariantPropertyTypeType,
    VariantStatusType,
    VendorGuidanceType,
    WarmPoolResourceStatusType,
    WorkforceStatusType,
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
    "ActionSourceTypeDef",
    "AddAssociationRequestRequestTypeDef",
    "AddAssociationResponseTypeDef",
    "TagTypeDef",
    "AgentVersionTypeDef",
    "AlarmTypeDef",
    "MetricDefinitionTypeDef",
    "AlgorithmStatusItemTypeDef",
    "AlgorithmSummaryTypeDef",
    "AnnotationConsolidationConfigTypeDef",
    "AppDetailsTypeDef",
    "AppSpecificationTypeDef",
    "ArtifactSourceTypeTypeDef",
    "AssociateTrialComponentRequestRequestTypeDef",
    "AssociateTrialComponentResponseTypeDef",
    "AsyncInferenceClientConfigTypeDef",
    "AsyncInferenceNotificationConfigTypeDef",
    "AthenaDatasetDefinitionTypeDef",
    "AutoMLAlgorithmConfigTypeDef",
    "AutoMLCandidateStepTypeDef",
    "AutoMLContainerDefinitionTypeDef",
    "FinalAutoMLJobObjectiveMetricTypeDef",
    "AutoMLS3DataSourceTypeDef",
    "AutoMLDataSplitConfigTypeDef",
    "AutoMLJobArtifactsTypeDef",
    "AutoMLJobCompletionCriteriaTypeDef",
    "AutoMLJobObjectiveTypeDef",
    "AutoMLJobStepMetadataTypeDef",
    "AutoMLPartialFailureReasonTypeDef",
    "AutoMLOutputDataConfigTypeDef",
    "TabularResolvedAttributesTypeDef",
    "VpcConfigTypeDef",
    "AutoParameterTypeDef",
    "AutotuneTypeDef",
    "BatchDataCaptureConfigTypeDef",
    "BatchDescribeModelPackageErrorTypeDef",
    "BatchDescribeModelPackageInputRequestTypeDef",
    "BestObjectiveNotImprovingTypeDef",
    "MetricsSourceTypeDef",
    "CacheHitResultTypeDef",
    "OutputParameterTypeDef",
    "CandidateArtifactLocationsTypeDef",
    "MetricDatumTypeDef",
    "ModelRegisterSettingsTypeDef",
    "TimeSeriesForecastingSettingsTypeDef",
    "WorkspaceSettingsTypeDef",
    "CapacitySizeTypeDef",
    "CaptureContentTypeHeaderTypeDef",
    "CaptureOptionTypeDef",
    "CategoricalParameterRangeSpecificationTypeDef",
    "CategoricalParameterRangeTypeDef",
    "CategoricalParameterTypeDef",
    "ChannelSpecificationTypeDef",
    "ShuffleConfigTypeDef",
    "CheckpointConfigTypeDef",
    "ClarifyCheckStepMetadataTypeDef",
    "ClarifyInferenceConfigTypeDef",
    "ClarifyShapBaselineConfigTypeDef",
    "ClarifyTextConfigTypeDef",
    "GitConfigTypeDef",
    "CodeRepositoryTypeDef",
    "CognitoConfigTypeDef",
    "CognitoMemberDefinitionTypeDef",
    "CollectionConfigurationTypeDef",
    "CompilationJobSummaryTypeDef",
    "ConditionStepMetadataTypeDef",
    "MultiModelConfigTypeDef",
    "ContextSourceTypeDef",
    "ContinuousParameterRangeSpecificationTypeDef",
    "ContinuousParameterRangeTypeDef",
    "ConvergenceDetectedTypeDef",
    "MetadataPropertiesTypeDef",
    "CreateActionResponseTypeDef",
    "CreateAlgorithmOutputTypeDef",
    "CreateAppImageConfigResponseTypeDef",
    "ResourceSpecTypeDef",
    "CreateAppResponseTypeDef",
    "CreateArtifactResponseTypeDef",
    "ModelDeployConfigTypeDef",
    "CreateAutoMLJobResponseTypeDef",
    "CreateAutoMLJobV2ResponseTypeDef",
    "CreateCodeRepositoryOutputTypeDef",
    "InputConfigTypeDef",
    "NeoVpcConfigTypeDef",
    "StoppingConditionTypeDef",
    "CreateCompilationJobResponseTypeDef",
    "CreateContextResponseTypeDef",
    "DataQualityAppSpecificationTypeDef",
    "MonitoringStoppingConditionTypeDef",
    "CreateDataQualityJobDefinitionResponseTypeDef",
    "EdgeOutputConfigTypeDef",
    "CreateDomainResponseTypeDef",
    "EdgeDeploymentModelConfigTypeDef",
    "CreateEdgeDeploymentPlanResponseTypeDef",
    "CreateEndpointConfigOutputTypeDef",
    "CreateEndpointOutputTypeDef",
    "CreateExperimentResponseTypeDef",
    "FeatureDefinitionTypeDef",
    "CreateFeatureGroupResponseTypeDef",
    "FlowDefinitionOutputConfigTypeDef",
    "HumanLoopRequestSourceTypeDef",
    "CreateFlowDefinitionResponseTypeDef",
    "HubS3StorageConfigTypeDef",
    "CreateHubResponseTypeDef",
    "UiTemplateTypeDef",
    "CreateHumanTaskUiResponseTypeDef",
    "CreateHyperParameterTuningJobResponseTypeDef",
    "CreateImageResponseTypeDef",
    "CreateImageVersionRequestRequestTypeDef",
    "CreateImageVersionResponseTypeDef",
    "InferenceExperimentScheduleTypeDef",
    "CreateInferenceExperimentResponseTypeDef",
    "CreateInferenceRecommendationsJobResponseTypeDef",
    "LabelingJobOutputConfigTypeDef",
    "LabelingJobStoppingConditionsTypeDef",
    "CreateLabelingJobResponseTypeDef",
    "ModelBiasAppSpecificationTypeDef",
    "CreateModelBiasJobDefinitionResponseTypeDef",
    "ModelCardExportOutputConfigTypeDef",
    "CreateModelCardExportJobResponseTypeDef",
    "ModelCardSecurityConfigTypeDef",
    "CreateModelCardResponseTypeDef",
    "ModelExplainabilityAppSpecificationTypeDef",
    "CreateModelExplainabilityJobDefinitionResponseTypeDef",
    "InferenceExecutionConfigTypeDef",
    "CreateModelOutputTypeDef",
    "CreateModelPackageGroupOutputTypeDef",
    "CreateModelPackageOutputTypeDef",
    "ModelQualityAppSpecificationTypeDef",
    "CreateModelQualityJobDefinitionResponseTypeDef",
    "CreateMonitoringScheduleResponseTypeDef",
    "InstanceMetadataServiceConfigurationTypeDef",
    "NotebookInstanceLifecycleHookTypeDef",
    "CreateNotebookInstanceLifecycleConfigOutputTypeDef",
    "CreateNotebookInstanceOutputTypeDef",
    "ParallelismConfigurationTypeDef",
    "PipelineDefinitionS3LocationTypeDef",
    "CreatePipelineResponseTypeDef",
    "CreatePresignedDomainUrlRequestRequestTypeDef",
    "CreatePresignedDomainUrlResponseTypeDef",
    "CreatePresignedNotebookInstanceUrlInputRequestTypeDef",
    "CreatePresignedNotebookInstanceUrlOutputTypeDef",
    "ExperimentConfigTypeDef",
    "ProcessingStoppingConditionTypeDef",
    "CreateProcessingJobResponseTypeDef",
    "CreateProjectOutputTypeDef",
    "CreateSpaceResponseTypeDef",
    "CreateStudioLifecycleConfigResponseTypeDef",
    "DebugRuleConfigurationTypeDef",
    "OutputDataConfigTypeDef",
    "ProfilerConfigTypeDef",
    "ProfilerRuleConfigurationTypeDef",
    "RetryStrategyTypeDef",
    "TensorBoardOutputConfigTypeDef",
    "CreateTrainingJobResponseTypeDef",
    "DataProcessingTypeDef",
    "ModelClientConfigTypeDef",
    "TransformOutputTypeDef",
    "TransformResourcesTypeDef",
    "CreateTransformJobResponseTypeDef",
    "TrialComponentArtifactTypeDef",
    "TrialComponentParameterValueTypeDef",
    "TrialComponentStatusTypeDef",
    "CreateTrialComponentResponseTypeDef",
    "CreateTrialResponseTypeDef",
    "CreateUserProfileResponseTypeDef",
    "OidcConfigTypeDef",
    "SourceIpConfigTypeDef",
    "WorkforceVpcConfigRequestTypeDef",
    "CreateWorkforceResponseTypeDef",
    "NotificationConfigurationTypeDef",
    "CreateWorkteamResponseTypeDef",
    "CustomImageTypeDef",
    "DataCaptureConfigSummaryTypeDef",
    "DataCatalogConfigTypeDef",
    "MonitoringConstraintsResourceTypeDef",
    "MonitoringStatisticsResourceTypeDef",
    "EndpointInputTypeDef",
    "FileSystemDataSourceTypeDef",
    "S3DataSourceTypeDef",
    "RedshiftDatasetDefinitionTypeDef",
    "DebugRuleEvaluationStatusTypeDef",
    "DeleteActionRequestRequestTypeDef",
    "DeleteActionResponseTypeDef",
    "DeleteAlgorithmInputRequestTypeDef",
    "DeleteAppImageConfigRequestRequestTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteArtifactResponseTypeDef",
    "DeleteAssociationRequestRequestTypeDef",
    "DeleteAssociationResponseTypeDef",
    "DeleteCodeRepositoryInputRequestTypeDef",
    "DeleteContextRequestRequestTypeDef",
    "DeleteContextResponseTypeDef",
    "DeleteDataQualityJobDefinitionRequestRequestTypeDef",
    "DeleteDeviceFleetRequestRequestTypeDef",
    "RetentionPolicyTypeDef",
    "DeleteEdgeDeploymentPlanRequestRequestTypeDef",
    "DeleteEdgeDeploymentStageRequestRequestTypeDef",
    "DeleteEndpointConfigInputRequestTypeDef",
    "DeleteEndpointInputRequestTypeDef",
    "DeleteExperimentRequestRequestTypeDef",
    "DeleteExperimentResponseTypeDef",
    "DeleteFeatureGroupRequestRequestTypeDef",
    "DeleteFlowDefinitionRequestRequestTypeDef",
    "DeleteHubContentRequestRequestTypeDef",
    "DeleteHubRequestRequestTypeDef",
    "DeleteHumanTaskUiRequestRequestTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteImageVersionRequestRequestTypeDef",
    "DeleteInferenceExperimentRequestRequestTypeDef",
    "DeleteInferenceExperimentResponseTypeDef",
    "DeleteModelBiasJobDefinitionRequestRequestTypeDef",
    "DeleteModelCardRequestRequestTypeDef",
    "DeleteModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "DeleteModelInputRequestTypeDef",
    "DeleteModelPackageGroupInputRequestTypeDef",
    "DeleteModelPackageGroupPolicyInputRequestTypeDef",
    "DeleteModelPackageInputRequestTypeDef",
    "DeleteModelQualityJobDefinitionRequestRequestTypeDef",
    "DeleteMonitoringScheduleRequestRequestTypeDef",
    "DeleteNotebookInstanceInputRequestTypeDef",
    "DeleteNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "DeletePipelineResponseTypeDef",
    "DeleteProjectInputRequestTypeDef",
    "DeleteSpaceRequestRequestTypeDef",
    "DeleteStudioLifecycleConfigRequestRequestTypeDef",
    "DeleteTagsInputRequestTypeDef",
    "DeleteTrialComponentRequestRequestTypeDef",
    "DeleteTrialComponentResponseTypeDef",
    "DeleteTrialRequestRequestTypeDef",
    "DeleteTrialResponseTypeDef",
    "DeleteUserProfileRequestRequestTypeDef",
    "DeleteWorkforceRequestRequestTypeDef",
    "DeleteWorkteamRequestRequestTypeDef",
    "DeleteWorkteamResponseTypeDef",
    "DeployedImageTypeDef",
    "RealTimeInferenceRecommendationTypeDef",
    "DeviceSelectionConfigTypeDef",
    "EdgeDeploymentConfigTypeDef",
    "EdgeDeploymentStatusTypeDef",
    "DeregisterDevicesRequestRequestTypeDef",
    "DescribeActionRequestRequestTypeDef",
    "DescribeAlgorithmInputRequestTypeDef",
    "DescribeAppImageConfigRequestRequestTypeDef",
    "DescribeAppRequestRequestTypeDef",
    "DescribeArtifactRequestRequestTypeDef",
    "DescribeAutoMLJobRequestRequestTypeDef",
    "ModelDeployResultTypeDef",
    "DescribeAutoMLJobV2RequestRequestTypeDef",
    "DescribeCodeRepositoryInputRequestTypeDef",
    "DescribeCompilationJobRequestRequestTypeDef",
    "ModelArtifactsTypeDef",
    "ModelDigestsTypeDef",
    "DescribeContextRequestRequestTypeDef",
    "DescribeDataQualityJobDefinitionRequestRequestTypeDef",
    "DescribeDeviceFleetRequestRequestTypeDef",
    "DescribeDeviceRequestRequestTypeDef",
    "EdgeModelTypeDef",
    "DescribeDomainRequestRequestTypeDef",
    "DescribeEdgeDeploymentPlanRequestRequestTypeDef",
    "DescribeEdgePackagingJobRequestRequestTypeDef",
    "EdgePresetDeploymentOutputTypeDef",
    "DescribeEndpointConfigInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeEndpointInputRequestTypeDef",
    "DescribeExperimentRequestRequestTypeDef",
    "ExperimentSourceTypeDef",
    "DescribeFeatureGroupRequestRequestTypeDef",
    "LastUpdateStatusTypeDef",
    "OfflineStoreStatusTypeDef",
    "DescribeFeatureMetadataRequestRequestTypeDef",
    "FeatureParameterTypeDef",
    "DescribeFlowDefinitionRequestRequestTypeDef",
    "DescribeHubContentRequestRequestTypeDef",
    "HubContentDependencyTypeDef",
    "DescribeHubRequestRequestTypeDef",
    "DescribeHumanTaskUiRequestRequestTypeDef",
    "UiTemplateInfoTypeDef",
    "DescribeHyperParameterTuningJobRequestRequestTypeDef",
    "HyperParameterTuningJobCompletionDetailsTypeDef",
    "HyperParameterTuningJobConsumedResourcesTypeDef",
    "ObjectiveStatusCountersTypeDef",
    "TrainingJobStatusCountersTypeDef",
    "DescribeImageRequestRequestTypeDef",
    "DescribeImageResponseTypeDef",
    "DescribeImageVersionRequestRequestTypeDef",
    "DescribeImageVersionResponseTypeDef",
    "DescribeInferenceExperimentRequestRequestTypeDef",
    "EndpointMetadataTypeDef",
    "DescribeInferenceRecommendationsJobRequestRequestTypeDef",
    "DescribeLabelingJobRequestRequestTypeDef",
    "LabelCountersTypeDef",
    "LabelingJobOutputTypeDef",
    "DescribeLineageGroupRequestRequestTypeDef",
    "DescribeModelBiasJobDefinitionRequestRequestTypeDef",
    "DescribeModelCardExportJobRequestRequestTypeDef",
    "ModelCardExportArtifactsTypeDef",
    "DescribeModelCardRequestRequestTypeDef",
    "DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "DescribeModelInputRequestTypeDef",
    "DescribeModelPackageGroupInputRequestTypeDef",
    "DescribeModelPackageInputRequestTypeDef",
    "DescribeModelQualityJobDefinitionRequestRequestTypeDef",
    "DescribeMonitoringScheduleRequestRequestTypeDef",
    "MonitoringExecutionSummaryTypeDef",
    "DescribeNotebookInstanceInputRequestTypeDef",
    "DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "DescribePipelineDefinitionForExecutionRequestRequestTypeDef",
    "DescribePipelineDefinitionForExecutionResponseTypeDef",
    "DescribePipelineExecutionRequestRequestTypeDef",
    "PipelineExperimentConfigTypeDef",
    "DescribePipelineRequestRequestTypeDef",
    "DescribeProcessingJobRequestRequestTypeDef",
    "DescribeProjectInputRequestTypeDef",
    "ServiceCatalogProvisionedProductDetailsTypeDef",
    "DescribeSpaceRequestRequestTypeDef",
    "DescribeStudioLifecycleConfigRequestRequestTypeDef",
    "DescribeStudioLifecycleConfigResponseTypeDef",
    "DescribeSubscribedWorkteamRequestRequestTypeDef",
    "SubscribedWorkteamTypeDef",
    "DescribeTrainingJobRequestRequestTypeDef",
    "MetricDataTypeDef",
    "ProfilerRuleEvaluationStatusTypeDef",
    "SecondaryStatusTransitionTypeDef",
    "WarmPoolStatusTypeDef",
    "DescribeTransformJobRequestRequestTypeDef",
    "DescribeTrialComponentRequestRequestTypeDef",
    "TrialComponentMetricSummaryTypeDef",
    "TrialComponentSourceTypeDef",
    "DescribeTrialRequestRequestTypeDef",
    "TrialSourceTypeDef",
    "DescribeUserProfileRequestRequestTypeDef",
    "DescribeWorkforceRequestRequestTypeDef",
    "DescribeWorkteamRequestRequestTypeDef",
    "ProductionVariantServerlessUpdateConfigTypeDef",
    "DeviceDeploymentSummaryTypeDef",
    "DeviceFleetSummaryTypeDef",
    "DeviceStatsTypeDef",
    "EdgeModelSummaryTypeDef",
    "DeviceTypeDef",
    "DisassociateTrialComponentRequestRequestTypeDef",
    "DisassociateTrialComponentResponseTypeDef",
    "DomainDetailsTypeDef",
    "FileSourceTypeDef",
    "EMRStepMetadataTypeDef",
    "EdgeDeploymentPlanSummaryTypeDef",
    "EdgeModelStatTypeDef",
    "EdgePackagingJobSummaryTypeDef",
    "EdgeTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointConfigSummaryTypeDef",
    "EndpointInfoTypeDef",
    "ProductionVariantServerlessConfigTypeDef",
    "InferenceMetricsTypeDef",
    "EndpointSummaryTypeDef",
    "EnvironmentParameterTypeDef",
    "FailStepMetadataTypeDef",
    "FileSystemConfigTypeDef",
    "FilterTypeDef",
    "FinalHyperParameterTuningJobObjectiveMetricTypeDef",
    "FlowDefinitionSummaryTypeDef",
    "GetDeviceFleetReportRequestRequestTypeDef",
    "GetLineageGroupPolicyRequestRequestTypeDef",
    "GetLineageGroupPolicyResponseTypeDef",
    "GetModelPackageGroupPolicyInputRequestTypeDef",
    "GetModelPackageGroupPolicyOutputTypeDef",
    "GetSagemakerServicecatalogPortfolioStatusOutputTypeDef",
    "PropertyNameSuggestionTypeDef",
    "GitConfigForUpdateTypeDef",
    "HubContentInfoTypeDef",
    "HubInfoTypeDef",
    "HumanLoopActivationConditionsConfigTypeDef",
    "UiConfigTypeDef",
    "HumanTaskUiSummaryTypeDef",
    "HyperParameterTuningJobObjectiveTypeDef",
    "HyperParameterTuningInstanceConfigTypeDef",
    "ResourceLimitsTypeDef",
    "HyperbandStrategyConfigTypeDef",
    "ParentHyperParameterTuningJobTypeDef",
    "IamIdentityTypeDef",
    "RepositoryAuthConfigTypeDef",
    "ImageTypeDef",
    "ImageVersionTypeDef",
    "ImportHubContentResponseTypeDef",
    "RecommendationMetricsTypeDef",
    "InferenceRecommendationsJobTypeDef",
    "InstanceGroupTypeDef",
    "IntegerParameterRangeSpecificationTypeDef",
    "IntegerParameterRangeTypeDef",
    "KernelSpecTypeDef",
    "LabelCountersForWorkteamTypeDef",
    "LabelingJobDataAttributesTypeDef",
    "LabelingJobS3DataSourceTypeDef",
    "LabelingJobSnsDataSourceTypeDef",
    "LineageGroupSummaryTypeDef",
    "ListActionsRequestListActionsPaginateTypeDef",
    "ListActionsRequestRequestTypeDef",
    "ListAlgorithmsInputListAlgorithmsPaginateTypeDef",
    "ListAlgorithmsInputRequestTypeDef",
    "ListAliasesRequestListAliasesPaginateTypeDef",
    "ListAliasesRequestRequestTypeDef",
    "ListAliasesResponseTypeDef",
    "ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef",
    "ListAppImageConfigsRequestRequestTypeDef",
    "ListAppsRequestListAppsPaginateTypeDef",
    "ListAppsRequestRequestTypeDef",
    "ListArtifactsRequestListArtifactsPaginateTypeDef",
    "ListArtifactsRequestRequestTypeDef",
    "ListAssociationsRequestListAssociationsPaginateTypeDef",
    "ListAssociationsRequestRequestTypeDef",
    "ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef",
    "ListAutoMLJobsRequestRequestTypeDef",
    "ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef",
    "ListCandidatesForAutoMLJobRequestRequestTypeDef",
    "ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef",
    "ListCodeRepositoriesInputRequestTypeDef",
    "ListCompilationJobsRequestListCompilationJobsPaginateTypeDef",
    "ListCompilationJobsRequestRequestTypeDef",
    "ListContextsRequestListContextsPaginateTypeDef",
    "ListContextsRequestRequestTypeDef",
    "ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef",
    "ListDataQualityJobDefinitionsRequestRequestTypeDef",
    "MonitoringJobDefinitionSummaryTypeDef",
    "ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef",
    "ListDeviceFleetsRequestRequestTypeDef",
    "ListDevicesRequestListDevicesPaginateTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef",
    "ListEdgeDeploymentPlansRequestRequestTypeDef",
    "ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef",
    "ListEdgePackagingJobsRequestRequestTypeDef",
    "ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef",
    "ListEndpointConfigsInputRequestTypeDef",
    "ListEndpointsInputListEndpointsPaginateTypeDef",
    "ListEndpointsInputRequestTypeDef",
    "ListExperimentsRequestListExperimentsPaginateTypeDef",
    "ListExperimentsRequestRequestTypeDef",
    "ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef",
    "ListFeatureGroupsRequestRequestTypeDef",
    "ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef",
    "ListFlowDefinitionsRequestRequestTypeDef",
    "ListHubContentVersionsRequestRequestTypeDef",
    "ListHubContentsRequestRequestTypeDef",
    "ListHubsRequestRequestTypeDef",
    "ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef",
    "ListHumanTaskUisRequestRequestTypeDef",
    "ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef",
    "ListHyperParameterTuningJobsRequestRequestTypeDef",
    "ListImageVersionsRequestListImageVersionsPaginateTypeDef",
    "ListImageVersionsRequestRequestTypeDef",
    "ListImagesRequestListImagesPaginateTypeDef",
    "ListImagesRequestRequestTypeDef",
    "ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef",
    "ListInferenceExperimentsRequestRequestTypeDef",
    "ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef",
    "ListInferenceRecommendationsJobStepsRequestRequestTypeDef",
    "ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef",
    "ListInferenceRecommendationsJobsRequestRequestTypeDef",
    "ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef",
    "ListLabelingJobsForWorkteamRequestRequestTypeDef",
    "ListLabelingJobsRequestListLabelingJobsPaginateTypeDef",
    "ListLabelingJobsRequestRequestTypeDef",
    "ListLineageGroupsRequestListLineageGroupsPaginateTypeDef",
    "ListLineageGroupsRequestRequestTypeDef",
    "ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef",
    "ListModelBiasJobDefinitionsRequestRequestTypeDef",
    "ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef",
    "ListModelCardExportJobsRequestRequestTypeDef",
    "ModelCardExportJobSummaryTypeDef",
    "ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef",
    "ListModelCardVersionsRequestRequestTypeDef",
    "ModelCardVersionSummaryTypeDef",
    "ListModelCardsRequestListModelCardsPaginateTypeDef",
    "ListModelCardsRequestRequestTypeDef",
    "ModelCardSummaryTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestRequestTypeDef",
    "ModelMetadataSummaryTypeDef",
    "ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef",
    "ListModelPackageGroupsInputRequestTypeDef",
    "ModelPackageGroupSummaryTypeDef",
    "ListModelPackagesInputListModelPackagesPaginateTypeDef",
    "ListModelPackagesInputRequestTypeDef",
    "ModelPackageSummaryTypeDef",
    "ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef",
    "ListModelQualityJobDefinitionsRequestRequestTypeDef",
    "ListModelsInputListModelsPaginateTypeDef",
    "ListModelsInputRequestTypeDef",
    "ModelSummaryTypeDef",
    "ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef",
    "ListMonitoringAlertHistoryRequestRequestTypeDef",
    "MonitoringAlertHistorySummaryTypeDef",
    "ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef",
    "ListMonitoringAlertsRequestRequestTypeDef",
    "ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef",
    "ListMonitoringExecutionsRequestRequestTypeDef",
    "ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef",
    "ListMonitoringSchedulesRequestRequestTypeDef",
    "MonitoringScheduleSummaryTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputRequestTypeDef",
    "NotebookInstanceLifecycleConfigSummaryTypeDef",
    "ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef",
    "ListNotebookInstancesInputRequestTypeDef",
    "NotebookInstanceSummaryTypeDef",
    "ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef",
    "ListPipelineExecutionStepsRequestRequestTypeDef",
    "ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef",
    "ListPipelineExecutionsRequestRequestTypeDef",
    "PipelineExecutionSummaryTypeDef",
    "ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef",
    "ListPipelineParametersForExecutionRequestRequestTypeDef",
    "ParameterTypeDef",
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "PipelineSummaryTypeDef",
    "ListProcessingJobsRequestListProcessingJobsPaginateTypeDef",
    "ListProcessingJobsRequestRequestTypeDef",
    "ProcessingJobSummaryTypeDef",
    "ListProjectsInputRequestTypeDef",
    "ProjectSummaryTypeDef",
    "ListSpacesRequestListSpacesPaginateTypeDef",
    "ListSpacesRequestRequestTypeDef",
    "SpaceDetailsTypeDef",
    "ListStageDevicesRequestListStageDevicesPaginateTypeDef",
    "ListStageDevicesRequestRequestTypeDef",
    "ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef",
    "ListStudioLifecycleConfigsRequestRequestTypeDef",
    "StudioLifecycleConfigDetailsTypeDef",
    "ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef",
    "ListSubscribedWorkteamsRequestRequestTypeDef",
    "ListTagsInputListTagsPaginateTypeDef",
    "ListTagsInputRequestTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef",
    "ListTrainingJobsRequestListTrainingJobsPaginateTypeDef",
    "ListTrainingJobsRequestRequestTypeDef",
    "ListTransformJobsRequestListTransformJobsPaginateTypeDef",
    "ListTransformJobsRequestRequestTypeDef",
    "TransformJobSummaryTypeDef",
    "ListTrialComponentsRequestListTrialComponentsPaginateTypeDef",
    "ListTrialComponentsRequestRequestTypeDef",
    "ListTrialsRequestListTrialsPaginateTypeDef",
    "ListTrialsRequestRequestTypeDef",
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
    "ListUserProfilesRequestRequestTypeDef",
    "UserProfileDetailsTypeDef",
    "ListWorkforcesRequestListWorkforcesPaginateTypeDef",
    "ListWorkforcesRequestRequestTypeDef",
    "ListWorkteamsRequestListWorkteamsPaginateTypeDef",
    "ListWorkteamsRequestRequestTypeDef",
    "OidcMemberDefinitionTypeDef",
    "MonitoringGroundTruthS3InputTypeDef",
    "ModelDashboardEndpointTypeDef",
    "ModelDashboardIndicatorActionTypeDef",
    "S3ModelDataSourceTypeDef",
    "RealTimeInferenceConfigTypeDef",
    "ModelInputTypeDef",
    "ModelLatencyThresholdTypeDef",
    "ModelMetadataFilterTypeDef",
    "ModelPackageStatusItemTypeDef",
    "ModelStepMetadataTypeDef",
    "MonitoringAppSpecificationTypeDef",
    "MonitoringClusterConfigTypeDef",
    "MonitoringCsvDatasetFormatTypeDef",
    "MonitoringJsonDatasetFormatTypeDef",
    "MonitoringS3OutputTypeDef",
    "ScheduleConfigTypeDef",
    "S3StorageConfigTypeDef",
    "OidcConfigForResponseTypeDef",
    "OnlineStoreSecurityConfigTypeDef",
    "TtlDurationTypeDef",
    "TargetPlatformTypeDef",
    "PaginatorConfigTypeDef",
    "ParentTypeDef",
    "ProductionVariantStatusTypeDef",
    "PhaseTypeDef",
    "ProcessingJobStepMetadataTypeDef",
    "QualityCheckStepMetadataTypeDef",
    "RegisterModelStepMetadataTypeDef",
    "TrainingJobStepMetadataTypeDef",
    "TransformJobStepMetadataTypeDef",
    "TuningJobStepMetaDataTypeDef",
    "SelectiveExecutionResultTypeDef",
    "ProcessingClusterConfigTypeDef",
    "ProcessingFeatureStoreOutputTypeDef",
    "ProcessingS3InputTypeDef",
    "ProcessingS3OutputTypeDef",
    "ProductionVariantCoreDumpConfigTypeDef",
    "ProfilerConfigForUpdateTypeDef",
    "PropertyNameQueryTypeDef",
    "ProvisioningParameterTypeDef",
    "USDTypeDef",
    "PutModelPackageGroupPolicyInputRequestTypeDef",
    "PutModelPackageGroupPolicyOutputTypeDef",
    "QueryFiltersTypeDef",
    "VertexTypeDef",
    "RStudioServerProAppSettingsTypeDef",
    "RecommendationJobCompiledOutputConfigTypeDef",
    "RecommendationJobPayloadConfigTypeDef",
    "RecommendationJobResourceLimitTypeDef",
    "RecommendationJobVpcConfigTypeDef",
    "RenderableTaskTypeDef",
    "RenderingErrorTypeDef",
    "ResourceConfigForUpdateTypeDef",
    "ResponseMetadataTypeDef",
    "RetryPipelineExecutionResponseTypeDef",
    "SearchRequestRequestTypeDef",
    "SearchRequestSearchPaginateTypeDef",
    "SelectedStepTypeDef",
    "SendPipelineExecutionStepFailureRequestRequestTypeDef",
    "SendPipelineExecutionStepFailureResponseTypeDef",
    "SendPipelineExecutionStepSuccessResponseTypeDef",
    "ShadowModelVariantConfigTypeDef",
    "SharingSettingsTypeDef",
    "SourceAlgorithmTypeDef",
    "StartEdgeDeploymentStageRequestRequestTypeDef",
    "StartInferenceExperimentRequestRequestTypeDef",
    "StartInferenceExperimentResponseTypeDef",
    "StartMonitoringScheduleRequestRequestTypeDef",
    "StartNotebookInstanceInputRequestTypeDef",
    "StartPipelineExecutionResponseTypeDef",
    "StopAutoMLJobRequestRequestTypeDef",
    "StopCompilationJobRequestRequestTypeDef",
    "StopEdgeDeploymentStageRequestRequestTypeDef",
    "StopEdgePackagingJobRequestRequestTypeDef",
    "StopHyperParameterTuningJobRequestRequestTypeDef",
    "StopInferenceExperimentResponseTypeDef",
    "StopInferenceRecommendationsJobRequestRequestTypeDef",
    "StopLabelingJobRequestRequestTypeDef",
    "StopMonitoringScheduleRequestRequestTypeDef",
    "StopNotebookInstanceInputRequestTypeDef",
    "StopPipelineExecutionRequestRequestTypeDef",
    "StopPipelineExecutionResponseTypeDef",
    "StopProcessingJobRequestRequestTypeDef",
    "StopTrainingJobRequestRequestTypeDef",
    "StopTransformJobRequestRequestTypeDef",
    "TimeSeriesConfigTypeDef",
    "TimeSeriesTransformationsTypeDef",
    "TrainingRepositoryAuthConfigTypeDef",
    "TransformS3DataSourceTypeDef",
    "UpdateActionRequestRequestTypeDef",
    "UpdateActionResponseTypeDef",
    "UpdateAppImageConfigResponseTypeDef",
    "UpdateArtifactRequestRequestTypeDef",
    "UpdateArtifactResponseTypeDef",
    "UpdateCodeRepositoryOutputTypeDef",
    "UpdateContextRequestRequestTypeDef",
    "UpdateContextResponseTypeDef",
    "UpdateDomainResponseTypeDef",
    "VariantPropertyTypeDef",
    "UpdateEndpointOutputTypeDef",
    "UpdateEndpointWeightsAndCapacitiesOutputTypeDef",
    "UpdateExperimentRequestRequestTypeDef",
    "UpdateExperimentResponseTypeDef",
    "UpdateFeatureGroupResponseTypeDef",
    "UpdateHubRequestRequestTypeDef",
    "UpdateHubResponseTypeDef",
    "UpdateImageRequestRequestTypeDef",
    "UpdateImageResponseTypeDef",
    "UpdateImageVersionRequestRequestTypeDef",
    "UpdateImageVersionResponseTypeDef",
    "UpdateInferenceExperimentResponseTypeDef",
    "UpdateModelCardRequestRequestTypeDef",
    "UpdateModelCardResponseTypeDef",
    "UpdateModelPackageOutputTypeDef",
    "UpdateMonitoringAlertRequestRequestTypeDef",
    "UpdateMonitoringAlertResponseTypeDef",
    "UpdateMonitoringScheduleResponseTypeDef",
    "UpdatePipelineExecutionResponseTypeDef",
    "UpdatePipelineResponseTypeDef",
    "UpdateProjectOutputTypeDef",
    "UpdateSpaceResponseTypeDef",
    "UpdateTrainingJobResponseTypeDef",
    "UpdateTrialComponentResponseTypeDef",
    "UpdateTrialRequestRequestTypeDef",
    "UpdateTrialResponseTypeDef",
    "UpdateUserProfileResponseTypeDef",
    "WorkforceVpcConfigResponseTypeDef",
    "ActionSummaryTypeDef",
    "AddTagsInputRequestTypeDef",
    "AddTagsOutputTypeDef",
    "CreateExperimentRequestRequestTypeDef",
    "CreateImageRequestRequestTypeDef",
    "CreateModelPackageGroupInputRequestTypeDef",
    "CreateStudioLifecycleConfigRequestRequestTypeDef",
    "ImportHubContentRequestRequestTypeDef",
    "ListTagsOutputTypeDef",
    "AutoRollbackConfigTypeDef",
    "HyperParameterAlgorithmSpecificationTypeDef",
    "AlgorithmStatusDetailsTypeDef",
    "ListAlgorithmsOutputTypeDef",
    "ListAppsResponseTypeDef",
    "ArtifactSourceTypeDef",
    "AsyncInferenceOutputConfigTypeDef",
    "AutoMLCandidateGenerationConfigTypeDef",
    "CandidateGenerationConfigTypeDef",
    "AutoMLDataSourceTypeDef",
    "ImageClassificationJobConfigTypeDef",
    "TextClassificationJobConfigTypeDef",
    "ResolvedAttributesTypeDef",
    "AutoMLJobSummaryTypeDef",
    "AutoMLProblemTypeResolvedAttributesTypeDef",
    "AutoMLSecurityConfigTypeDef",
    "LabelingJobResourceConfigTypeDef",
    "MonitoringNetworkConfigTypeDef",
    "NetworkConfigTypeDef",
    "BiasTypeDef",
    "DriftCheckModelDataQualityTypeDef",
    "DriftCheckModelQualityTypeDef",
    "ExplainabilityTypeDef",
    "ModelDataQualityTypeDef",
    "ModelQualityTypeDef",
    "CallbackStepMetadataTypeDef",
    "LambdaStepMetadataTypeDef",
    "SendPipelineExecutionStepSuccessRequestRequestTypeDef",
    "CandidatePropertiesTypeDef",
    "CanvasAppSettingsTypeDef",
    "RollingUpdatePolicyTypeDef",
    "TrafficRoutingConfigTypeDef",
    "InferenceExperimentDataStorageConfigTypeDef",
    "DataCaptureConfigTypeDef",
    "EnvironmentParameterRangesTypeDef",
    "ClarifyShapConfigTypeDef",
    "CodeRepositorySummaryTypeDef",
    "CreateCodeRepositoryInputRequestTypeDef",
    "DescribeCodeRepositoryOutputTypeDef",
    "DebugHookConfigTypeDef",
    "ListCompilationJobsResponseTypeDef",
    "ContextSummaryTypeDef",
    "CreateContextRequestRequestTypeDef",
    "TuningJobCompletionCriteriaTypeDef",
    "CreateActionRequestRequestTypeDef",
    "CreateTrialRequestRequestTypeDef",
    "CreateAppRequestRequestTypeDef",
    "DescribeAppResponseTypeDef",
    "JupyterServerAppSettingsTypeDef",
    "RStudioServerProDomainSettingsForUpdateTypeDef",
    "RStudioServerProDomainSettingsTypeDef",
    "TensorBoardAppSettingsTypeDef",
    "CreateDeviceFleetRequestRequestTypeDef",
    "CreateEdgePackagingJobRequestRequestTypeDef",
    "DescribeDeviceFleetResponseTypeDef",
    "UpdateDeviceFleetRequestRequestTypeDef",
    "CreateHubRequestRequestTypeDef",
    "DescribeHubResponseTypeDef",
    "CreateHumanTaskUiRequestRequestTypeDef",
    "InferenceExperimentSummaryTypeDef",
    "CreateModelCardExportJobRequestRequestTypeDef",
    "CreateModelCardRequestRequestTypeDef",
    "CreateNotebookInstanceInputRequestTypeDef",
    "DescribeNotebookInstanceOutputTypeDef",
    "UpdateNotebookInstanceInputRequestTypeDef",
    "CreateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "DescribeNotebookInstanceLifecycleConfigOutputTypeDef",
    "UpdateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "RetryPipelineExecutionRequestRequestTypeDef",
    "UpdatePipelineExecutionRequestRequestTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "CreateTrialComponentRequestRequestTypeDef",
    "UpdateTrialComponentRequestRequestTypeDef",
    "CreateWorkforceRequestRequestTypeDef",
    "UpdateWorkforceRequestRequestTypeDef",
    "KernelGatewayAppSettingsTypeDef",
    "RSessionAppSettingsTypeDef",
    "ModelBiasBaselineConfigTypeDef",
    "ModelExplainabilityBaselineConfigTypeDef",
    "ModelQualityBaselineConfigTypeDef",
    "DataQualityBaselineConfigTypeDef",
    "MonitoringBaselineConfigTypeDef",
    "DataSourceTypeDef",
    "DatasetDefinitionTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeploymentRecommendationTypeDef",
    "DeploymentStageTypeDef",
    "DeploymentStageStatusSummaryTypeDef",
    "DescribeDeviceResponseTypeDef",
    "DescribeEdgePackagingJobResponseTypeDef",
    "DescribeEndpointInputEndpointDeletedWaitTypeDef",
    "DescribeEndpointInputEndpointInServiceWaitTypeDef",
    "DescribeImageRequestImageCreatedWaitTypeDef",
    "DescribeImageRequestImageDeletedWaitTypeDef",
    "DescribeImageRequestImageUpdatedWaitTypeDef",
    "DescribeImageVersionRequestImageVersionCreatedWaitTypeDef",
    "DescribeImageVersionRequestImageVersionDeletedWaitTypeDef",
    "DescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef",
    "DescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef",
    "DescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef",
    "DescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef",
    "DescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef",
    "DescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef",
    "ExperimentSummaryTypeDef",
    "FeatureGroupSummaryTypeDef",
    "DescribeFeatureMetadataResponseTypeDef",
    "FeatureMetadataTypeDef",
    "UpdateFeatureMetadataRequestRequestTypeDef",
    "DescribeHubContentResponseTypeDef",
    "DescribeHumanTaskUiResponseTypeDef",
    "DescribeModelCardExportJobResponseTypeDef",
    "ListMonitoringExecutionsResponseTypeDef",
    "DescribeSubscribedWorkteamResponseTypeDef",
    "ListSubscribedWorkteamsResponseTypeDef",
    "TrainingJobSummaryTypeDef",
    "TrialSummaryTypeDef",
    "DesiredWeightAndCapacityTypeDef",
    "ListStageDevicesResponseTypeDef",
    "ListDeviceFleetsResponseTypeDef",
    "DeviceSummaryTypeDef",
    "RegisterDevicesRequestRequestTypeDef",
    "UpdateDevicesRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "DriftCheckBiasTypeDef",
    "DriftCheckExplainabilityTypeDef",
    "ListEdgeDeploymentPlansResponseTypeDef",
    "GetDeviceFleetReportResponseTypeDef",
    "ListEdgePackagingJobsResponseTypeDef",
    "ListEndpointConfigsOutputTypeDef",
    "EndpointOutputConfigurationTypeDef",
    "EndpointPerformanceTypeDef",
    "ListEndpointsOutputTypeDef",
    "ModelConfigurationTypeDef",
    "NestedFiltersTypeDef",
    "HyperParameterTrainingJobSummaryTypeDef",
    "ListFlowDefinitionsResponseTypeDef",
    "GetSearchSuggestionsResponseTypeDef",
    "UpdateCodeRepositoryInputRequestTypeDef",
    "ListHubContentVersionsResponseTypeDef",
    "ListHubContentsResponseTypeDef",
    "ListHubsResponseTypeDef",
    "HumanLoopActivationConfigTypeDef",
    "ListHumanTaskUisResponseTypeDef",
    "HyperParameterTuningResourceConfigTypeDef",
    "HyperParameterTuningJobSummaryTypeDef",
    "HyperParameterTuningJobStrategyConfigTypeDef",
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    "UserContextTypeDef",
    "ImageConfigTypeDef",
    "ListImagesResponseTypeDef",
    "ListImageVersionsResponseTypeDef",
    "ListInferenceRecommendationsJobsResponseTypeDef",
    "ResourceConfigTypeDef",
    "ParameterRangeTypeDef",
    "ParameterRangesTypeDef",
    "KernelGatewayImageConfigTypeDef",
    "LabelingJobForWorkteamSummaryTypeDef",
    "LabelingJobDataSourceTypeDef",
    "ListLineageGroupsResponseTypeDef",
    "ListDataQualityJobDefinitionsResponseTypeDef",
    "ListModelBiasJobDefinitionsResponseTypeDef",
    "ListModelExplainabilityJobDefinitionsResponseTypeDef",
    "ListModelQualityJobDefinitionsResponseTypeDef",
    "ListModelCardExportJobsResponseTypeDef",
    "ListModelCardVersionsResponseTypeDef",
    "ListModelCardsResponseTypeDef",
    "ListModelMetadataResponseTypeDef",
    "ListModelPackageGroupsOutputTypeDef",
    "ListModelPackagesOutputTypeDef",
    "ListModelsOutputTypeDef",
    "ListMonitoringAlertHistoryResponseTypeDef",
    "ListMonitoringSchedulesResponseTypeDef",
    "ListNotebookInstanceLifecycleConfigsOutputTypeDef",
    "ListNotebookInstancesOutputTypeDef",
    "ListPipelineExecutionsResponseTypeDef",
    "ListPipelineParametersForExecutionResponseTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListProcessingJobsResponseTypeDef",
    "ListProjectsOutputTypeDef",
    "ListSpacesResponseTypeDef",
    "ListStudioLifecycleConfigsResponseTypeDef",
    "ListTransformJobsResponseTypeDef",
    "ListUserProfilesResponseTypeDef",
    "MemberDefinitionTypeDef",
    "MonitoringAlertActionsTypeDef",
    "ModelDataSourceTypeDef",
    "ModelInfrastructureConfigTypeDef",
    "ModelPackageContainerDefinitionTypeDef",
    "RecommendationJobStoppingConditionsTypeDef",
    "ModelMetadataSearchExpressionTypeDef",
    "ModelPackageStatusDetailsTypeDef",
    "MonitoringResourcesTypeDef",
    "MonitoringDatasetFormatTypeDef",
    "MonitoringOutputTypeDef",
    "OfflineStoreConfigTypeDef",
    "OnlineStoreConfigTypeDef",
    "OnlineStoreConfigUpdateTypeDef",
    "OutputConfigTypeDef",
    "PendingProductionVariantSummaryTypeDef",
    "ProductionVariantSummaryTypeDef",
    "TrafficPatternTypeDef",
    "ProcessingResourcesTypeDef",
    "ProcessingOutputTypeDef",
    "ProductionVariantTypeDef",
    "SuggestionQueryTypeDef",
    "ServiceCatalogProvisioningDetailsTypeDef",
    "ServiceCatalogProvisioningUpdateDetailsTypeDef",
    "PublicWorkforceTaskPriceTypeDef",
    "QueryLineageRequestRequestTypeDef",
    "QueryLineageResponseTypeDef",
    "RecommendationJobOutputConfigTypeDef",
    "RecommendationJobContainerConfigTypeDef",
    "RenderUiTemplateRequestRequestTypeDef",
    "RenderUiTemplateResponseTypeDef",
    "UpdateTrainingJobRequestRequestTypeDef",
    "SelectiveExecutionConfigTypeDef",
    "ShadowModeConfigTypeDef",
    "SourceAlgorithmSpecificationTypeDef",
    "TimeSeriesForecastingJobConfigTypeDef",
    "TrainingImageConfigTypeDef",
    "TransformDataSourceTypeDef",
    "WorkforceTypeDef",
    "ListActionsResponseTypeDef",
    "ArtifactSummaryTypeDef",
    "CreateArtifactRequestRequestTypeDef",
    "DeleteArtifactRequestRequestTypeDef",
    "AsyncInferenceConfigTypeDef",
    "TabularJobConfigTypeDef",
    "AutoMLChannelTypeDef",
    "AutoMLJobChannelTypeDef",
    "ListAutoMLJobsResponseTypeDef",
    "AutoMLResolvedAttributesTypeDef",
    "AutoMLJobConfigTypeDef",
    "LabelingJobAlgorithmsConfigTypeDef",
    "ModelMetricsTypeDef",
    "PipelineExecutionStepMetadataTypeDef",
    "AutoMLCandidateTypeDef",
    "BlueGreenUpdatePolicyTypeDef",
    "EndpointInputConfigurationTypeDef",
    "ClarifyExplainerConfigTypeDef",
    "ListCodeRepositoriesOutputTypeDef",
    "ListContextsResponseTypeDef",
    "DomainSettingsForUpdateTypeDef",
    "DomainSettingsTypeDef",
    "ListInferenceExperimentsResponseTypeDef",
    "DefaultSpaceSettingsTypeDef",
    "SpaceSettingsTypeDef",
    "UserSettingsTypeDef",
    "ChannelTypeDef",
    "ProcessingInputTypeDef",
    "CreateEdgeDeploymentPlanRequestRequestTypeDef",
    "CreateEdgeDeploymentStageRequestRequestTypeDef",
    "DescribeEdgeDeploymentPlanResponseTypeDef",
    "ListExperimentsResponseTypeDef",
    "ListFeatureGroupsResponseTypeDef",
    "ListTrainingJobsResponseTypeDef",
    "ListTrialsResponseTypeDef",
    "UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef",
    "ListDevicesResponseTypeDef",
    "DriftCheckBaselinesTypeDef",
    "InferenceRecommendationTypeDef",
    "RecommendationJobInferenceBenchmarkTypeDef",
    "SearchExpressionTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobResponseTypeDef",
    "ListHyperParameterTuningJobsResponseTypeDef",
    "AssociationSummaryTypeDef",
    "DescribeActionResponseTypeDef",
    "DescribeArtifactResponseTypeDef",
    "DescribeContextResponseTypeDef",
    "DescribeExperimentResponseTypeDef",
    "DescribeLineageGroupResponseTypeDef",
    "DescribeModelCardResponseTypeDef",
    "DescribeModelPackageGroupOutputTypeDef",
    "DescribePipelineResponseTypeDef",
    "DescribeTrialComponentResponseTypeDef",
    "DescribeTrialResponseTypeDef",
    "ExperimentTypeDef",
    "ModelCardTypeDef",
    "ModelDashboardModelCardTypeDef",
    "ModelPackageGroupTypeDef",
    "PipelineTypeDef",
    "TrialComponentSimpleSummaryTypeDef",
    "TrialComponentSummaryTypeDef",
    "HyperParameterSpecificationTypeDef",
    "HyperParameterTuningJobConfigTypeDef",
    "AppImageConfigDetailsTypeDef",
    "CreateAppImageConfigRequestRequestTypeDef",
    "DescribeAppImageConfigResponseTypeDef",
    "UpdateAppImageConfigRequestRequestTypeDef",
    "ListLabelingJobsForWorkteamResponseTypeDef",
    "LabelingJobInputConfigTypeDef",
    "CreateWorkteamRequestRequestTypeDef",
    "UpdateWorkteamRequestRequestTypeDef",
    "WorkteamTypeDef",
    "MonitoringAlertSummaryTypeDef",
    "ContainerDefinitionTypeDef",
    "ModelVariantConfigSummaryTypeDef",
    "ModelVariantConfigTypeDef",
    "AdditionalInferenceSpecificationDefinitionTypeDef",
    "InferenceSpecificationTypeDef",
    "ListModelMetadataRequestListModelMetadataPaginateTypeDef",
    "ListModelMetadataRequestRequestTypeDef",
    "BatchTransformInputTypeDef",
    "MonitoringOutputConfigTypeDef",
    "CreateFeatureGroupRequestRequestTypeDef",
    "DescribeFeatureGroupResponseTypeDef",
    "FeatureGroupTypeDef",
    "UpdateFeatureGroupRequestRequestTypeDef",
    "CreateCompilationJobRequestRequestTypeDef",
    "DescribeCompilationJobResponseTypeDef",
    "PendingDeploymentSummaryTypeDef",
    "ProcessingOutputConfigTypeDef",
    "GetSearchSuggestionsRequestRequestTypeDef",
    "CreateProjectInputRequestTypeDef",
    "DescribeProjectOutputTypeDef",
    "ProjectTypeDef",
    "UpdateProjectInputRequestTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanTaskConfigTypeDef",
    "DescribePipelineExecutionResponseTypeDef",
    "PipelineExecutionTypeDef",
    "StartPipelineExecutionRequestRequestTypeDef",
    "AlgorithmSpecificationTypeDef",
    "TransformInputTypeDef",
    "DescribeWorkforceResponseTypeDef",
    "ListWorkforcesResponseTypeDef",
    "UpdateWorkforceResponseTypeDef",
    "ListArtifactsResponseTypeDef",
    "AutoMLProblemTypeConfigTypeDef",
    "CreateAutoMLJobRequestRequestTypeDef",
    "PipelineExecutionStepTypeDef",
    "DescribeAutoMLJobResponseTypeDef",
    "ListCandidatesForAutoMLJobResponseTypeDef",
    "DeploymentConfigTypeDef",
    "RecommendationJobInputConfigTypeDef",
    "ExplainerConfigTypeDef",
    "CreateSpaceRequestRequestTypeDef",
    "DescribeSpaceResponseTypeDef",
    "UpdateSpaceRequestRequestTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateUserProfileRequestRequestTypeDef",
    "DescribeDomainResponseTypeDef",
    "DescribeUserProfileResponseTypeDef",
    "UpdateDomainRequestRequestTypeDef",
    "UpdateUserProfileRequestRequestTypeDef",
    "HyperParameterTrainingJobDefinitionTypeDef",
    "TrainingJobDefinitionTypeDef",
    "InferenceRecommendationsJobStepTypeDef",
    "ListAssociationsResponseTypeDef",
    "TrialTypeDef",
    "ListTrialComponentsResponseTypeDef",
    "TrainingSpecificationTypeDef",
    "ListAppImageConfigsResponseTypeDef",
    "LabelingJobSummaryTypeDef",
    "DescribeWorkteamResponseTypeDef",
    "ListWorkteamsResponseTypeDef",
    "UpdateWorkteamResponseTypeDef",
    "ListMonitoringAlertsResponseTypeDef",
    "CreateModelInputRequestTypeDef",
    "DescribeModelOutputTypeDef",
    "ModelTypeDef",
    "DescribeInferenceExperimentResponseTypeDef",
    "CreateInferenceExperimentRequestRequestTypeDef",
    "StopInferenceExperimentRequestRequestTypeDef",
    "UpdateInferenceExperimentRequestRequestTypeDef",
    "UpdateModelPackageInputRequestTypeDef",
    "BatchDescribeModelPackageSummaryTypeDef",
    "DataQualityJobInputTypeDef",
    "ModelBiasJobInputTypeDef",
    "ModelExplainabilityJobInputTypeDef",
    "ModelQualityJobInputTypeDef",
    "MonitoringInputTypeDef",
    "CreateProcessingJobRequestRequestTypeDef",
    "DescribeProcessingJobResponseTypeDef",
    "ProcessingJobTypeDef",
    "CreateFlowDefinitionRequestRequestTypeDef",
    "DescribeFlowDefinitionResponseTypeDef",
    "CreateLabelingJobRequestRequestTypeDef",
    "DescribeLabelingJobResponseTypeDef",
    "CreateTrainingJobRequestRequestTypeDef",
    "DescribeTrainingJobResponseTypeDef",
    "TrainingJobTypeDef",
    "CreateTransformJobRequestRequestTypeDef",
    "DescribeTransformJobResponseTypeDef",
    "TransformJobDefinitionTypeDef",
    "TransformJobTypeDef",
    "CreateAutoMLJobV2RequestRequestTypeDef",
    "DescribeAutoMLJobV2ResponseTypeDef",
    "ListPipelineExecutionStepsResponseTypeDef",
    "CreateEndpointInputRequestTypeDef",
    "UpdateEndpointInputRequestTypeDef",
    "CreateInferenceRecommendationsJobRequestRequestTypeDef",
    "DescribeInferenceRecommendationsJobResponseTypeDef",
    "CreateEndpointConfigInputRequestTypeDef",
    "DescribeEndpointConfigOutputTypeDef",
    "DescribeEndpointOutputTypeDef",
    "CreateHyperParameterTuningJobRequestRequestTypeDef",
    "DescribeHyperParameterTuningJobResponseTypeDef",
    "HyperParameterTuningJobSearchEntityTypeDef",
    "ListInferenceRecommendationsJobStepsResponseTypeDef",
    "ListLabelingJobsResponseTypeDef",
    "BatchDescribeModelPackageOutputTypeDef",
    "CreateDataQualityJobDefinitionRequestRequestTypeDef",
    "DescribeDataQualityJobDefinitionResponseTypeDef",
    "CreateModelBiasJobDefinitionRequestRequestTypeDef",
    "DescribeModelBiasJobDefinitionResponseTypeDef",
    "CreateModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "DescribeModelExplainabilityJobDefinitionResponseTypeDef",
    "CreateModelQualityJobDefinitionRequestRequestTypeDef",
    "DescribeModelQualityJobDefinitionResponseTypeDef",
    "MonitoringJobDefinitionTypeDef",
    "AlgorithmValidationProfileTypeDef",
    "ModelPackageValidationProfileTypeDef",
    "TrialComponentSourceDetailTypeDef",
    "MonitoringScheduleConfigTypeDef",
    "AlgorithmValidationSpecificationTypeDef",
    "ModelPackageValidationSpecificationTypeDef",
    "TrialComponentTypeDef",
    "CreateMonitoringScheduleRequestRequestTypeDef",
    "DescribeMonitoringScheduleResponseTypeDef",
    "ModelDashboardMonitoringScheduleTypeDef",
    "MonitoringScheduleTypeDef",
    "UpdateMonitoringScheduleRequestRequestTypeDef",
    "CreateAlgorithmInputRequestTypeDef",
    "DescribeAlgorithmOutputTypeDef",
    "CreateModelPackageInputRequestTypeDef",
    "DescribeModelPackageOutputTypeDef",
    "ModelPackageTypeDef",
    "ModelDashboardModelTypeDef",
    "EndpointTypeDef",
    "SearchRecordTypeDef",
    "SearchResponseTypeDef",
)

_RequiredActionSourceTypeDef = TypedDict(
    "_RequiredActionSourceTypeDef",
    {
        "SourceUri": str,
    },
)
_OptionalActionSourceTypeDef = TypedDict(
    "_OptionalActionSourceTypeDef",
    {
        "SourceType": str,
        "SourceId": str,
    },
    total=False,
)


class ActionSourceTypeDef(_RequiredActionSourceTypeDef, _OptionalActionSourceTypeDef):
    pass


_RequiredAddAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredAddAssociationRequestRequestTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
    },
)
_OptionalAddAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalAddAssociationRequestRequestTypeDef",
    {
        "AssociationType": AssociationEdgeTypeType,
    },
    total=False,
)


class AddAssociationRequestRequestTypeDef(
    _RequiredAddAssociationRequestRequestTypeDef, _OptionalAddAssociationRequestRequestTypeDef
):
    pass


AddAssociationResponseTypeDef = TypedDict(
    "AddAssociationResponseTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

AgentVersionTypeDef = TypedDict(
    "AgentVersionTypeDef",
    {
        "Version": str,
        "AgentCount": int,
    },
)

AlarmTypeDef = TypedDict(
    "AlarmTypeDef",
    {
        "AlarmName": str,
    },
    total=False,
)

MetricDefinitionTypeDef = TypedDict(
    "MetricDefinitionTypeDef",
    {
        "Name": str,
        "Regex": str,
    },
)

AlgorithmStatusItemTypeDef = TypedDict(
    "AlgorithmStatusItemTypeDef",
    {
        "Name": str,
        "Status": DetailedAlgorithmStatusType,
        "FailureReason": str,
    },
)

AlgorithmSummaryTypeDef = TypedDict(
    "AlgorithmSummaryTypeDef",
    {
        "AlgorithmName": str,
        "AlgorithmArn": str,
        "AlgorithmDescription": str,
        "CreationTime": datetime,
        "AlgorithmStatus": AlgorithmStatusType,
    },
)

AnnotationConsolidationConfigTypeDef = TypedDict(
    "AnnotationConsolidationConfigTypeDef",
    {
        "AnnotationConsolidationLambdaArn": str,
    },
)

AppDetailsTypeDef = TypedDict(
    "AppDetailsTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
        "AppType": AppTypeType,
        "AppName": str,
        "Status": AppStatusType,
        "CreationTime": datetime,
        "SpaceName": str,
    },
)

_RequiredAppSpecificationTypeDef = TypedDict(
    "_RequiredAppSpecificationTypeDef",
    {
        "ImageUri": str,
    },
)
_OptionalAppSpecificationTypeDef = TypedDict(
    "_OptionalAppSpecificationTypeDef",
    {
        "ContainerEntrypoint": Sequence[str],
        "ContainerArguments": Sequence[str],
    },
    total=False,
)


class AppSpecificationTypeDef(_RequiredAppSpecificationTypeDef, _OptionalAppSpecificationTypeDef):
    pass


ArtifactSourceTypeTypeDef = TypedDict(
    "ArtifactSourceTypeTypeDef",
    {
        "SourceIdType": ArtifactSourceIdTypeType,
        "Value": str,
    },
)

AssociateTrialComponentRequestRequestTypeDef = TypedDict(
    "AssociateTrialComponentRequestRequestTypeDef",
    {
        "TrialComponentName": str,
        "TrialName": str,
    },
)

AssociateTrialComponentResponseTypeDef = TypedDict(
    "AssociateTrialComponentResponseTypeDef",
    {
        "TrialComponentArn": str,
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AsyncInferenceClientConfigTypeDef = TypedDict(
    "AsyncInferenceClientConfigTypeDef",
    {
        "MaxConcurrentInvocationsPerInstance": int,
    },
    total=False,
)

AsyncInferenceNotificationConfigTypeDef = TypedDict(
    "AsyncInferenceNotificationConfigTypeDef",
    {
        "SuccessTopic": str,
        "ErrorTopic": str,
        "IncludeInferenceResponseIn": Sequence[AsyncNotificationTopicTypesType],
    },
    total=False,
)

_RequiredAthenaDatasetDefinitionTypeDef = TypedDict(
    "_RequiredAthenaDatasetDefinitionTypeDef",
    {
        "Catalog": str,
        "Database": str,
        "QueryString": str,
        "OutputS3Uri": str,
        "OutputFormat": AthenaResultFormatType,
    },
)
_OptionalAthenaDatasetDefinitionTypeDef = TypedDict(
    "_OptionalAthenaDatasetDefinitionTypeDef",
    {
        "WorkGroup": str,
        "KmsKeyId": str,
        "OutputCompression": AthenaResultCompressionTypeType,
    },
    total=False,
)


class AthenaDatasetDefinitionTypeDef(
    _RequiredAthenaDatasetDefinitionTypeDef, _OptionalAthenaDatasetDefinitionTypeDef
):
    pass


AutoMLAlgorithmConfigTypeDef = TypedDict(
    "AutoMLAlgorithmConfigTypeDef",
    {
        "AutoMLAlgorithms": Sequence[AutoMLAlgorithmType],
    },
)

AutoMLCandidateStepTypeDef = TypedDict(
    "AutoMLCandidateStepTypeDef",
    {
        "CandidateStepType": CandidateStepTypeType,
        "CandidateStepArn": str,
        "CandidateStepName": str,
    },
)

AutoMLContainerDefinitionTypeDef = TypedDict(
    "AutoMLContainerDefinitionTypeDef",
    {
        "Image": str,
        "ModelDataUrl": str,
        "Environment": Dict[str, str],
    },
)

FinalAutoMLJobObjectiveMetricTypeDef = TypedDict(
    "FinalAutoMLJobObjectiveMetricTypeDef",
    {
        "Type": AutoMLJobObjectiveTypeType,
        "MetricName": AutoMLMetricEnumType,
        "Value": float,
        "StandardMetricName": AutoMLMetricEnumType,
    },
)

AutoMLS3DataSourceTypeDef = TypedDict(
    "AutoMLS3DataSourceTypeDef",
    {
        "S3DataType": AutoMLS3DataTypeType,
        "S3Uri": str,
    },
)

AutoMLDataSplitConfigTypeDef = TypedDict(
    "AutoMLDataSplitConfigTypeDef",
    {
        "ValidationFraction": float,
    },
    total=False,
)

AutoMLJobArtifactsTypeDef = TypedDict(
    "AutoMLJobArtifactsTypeDef",
    {
        "CandidateDefinitionNotebookLocation": str,
        "DataExplorationNotebookLocation": str,
    },
)

AutoMLJobCompletionCriteriaTypeDef = TypedDict(
    "AutoMLJobCompletionCriteriaTypeDef",
    {
        "MaxCandidates": int,
        "MaxRuntimePerTrainingJobInSeconds": int,
        "MaxAutoMLJobRuntimeInSeconds": int,
    },
    total=False,
)

AutoMLJobObjectiveTypeDef = TypedDict(
    "AutoMLJobObjectiveTypeDef",
    {
        "MetricName": AutoMLMetricEnumType,
    },
)

AutoMLJobStepMetadataTypeDef = TypedDict(
    "AutoMLJobStepMetadataTypeDef",
    {
        "Arn": str,
    },
)

AutoMLPartialFailureReasonTypeDef = TypedDict(
    "AutoMLPartialFailureReasonTypeDef",
    {
        "PartialFailureMessage": str,
    },
)

_RequiredAutoMLOutputDataConfigTypeDef = TypedDict(
    "_RequiredAutoMLOutputDataConfigTypeDef",
    {
        "S3OutputPath": str,
    },
)
_OptionalAutoMLOutputDataConfigTypeDef = TypedDict(
    "_OptionalAutoMLOutputDataConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class AutoMLOutputDataConfigTypeDef(
    _RequiredAutoMLOutputDataConfigTypeDef, _OptionalAutoMLOutputDataConfigTypeDef
):
    pass


TabularResolvedAttributesTypeDef = TypedDict(
    "TabularResolvedAttributesTypeDef",
    {
        "ProblemType": ProblemTypeType,
    },
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "Subnets": Sequence[str],
    },
)

AutoParameterTypeDef = TypedDict(
    "AutoParameterTypeDef",
    {
        "Name": str,
        "ValueHint": str,
    },
)

AutotuneTypeDef = TypedDict(
    "AutotuneTypeDef",
    {
        "Mode": Literal["Enabled"],
    },
)

_RequiredBatchDataCaptureConfigTypeDef = TypedDict(
    "_RequiredBatchDataCaptureConfigTypeDef",
    {
        "DestinationS3Uri": str,
    },
)
_OptionalBatchDataCaptureConfigTypeDef = TypedDict(
    "_OptionalBatchDataCaptureConfigTypeDef",
    {
        "KmsKeyId": str,
        "GenerateInferenceId": bool,
    },
    total=False,
)


class BatchDataCaptureConfigTypeDef(
    _RequiredBatchDataCaptureConfigTypeDef, _OptionalBatchDataCaptureConfigTypeDef
):
    pass


BatchDescribeModelPackageErrorTypeDef = TypedDict(
    "BatchDescribeModelPackageErrorTypeDef",
    {
        "ErrorCode": str,
        "ErrorResponse": str,
    },
)

BatchDescribeModelPackageInputRequestTypeDef = TypedDict(
    "BatchDescribeModelPackageInputRequestTypeDef",
    {
        "ModelPackageArnList": Sequence[str],
    },
)

BestObjectiveNotImprovingTypeDef = TypedDict(
    "BestObjectiveNotImprovingTypeDef",
    {
        "MaxNumberOfTrainingJobsNotImproving": int,
    },
    total=False,
)

_RequiredMetricsSourceTypeDef = TypedDict(
    "_RequiredMetricsSourceTypeDef",
    {
        "ContentType": str,
        "S3Uri": str,
    },
)
_OptionalMetricsSourceTypeDef = TypedDict(
    "_OptionalMetricsSourceTypeDef",
    {
        "ContentDigest": str,
    },
    total=False,
)


class MetricsSourceTypeDef(_RequiredMetricsSourceTypeDef, _OptionalMetricsSourceTypeDef):
    pass


CacheHitResultTypeDef = TypedDict(
    "CacheHitResultTypeDef",
    {
        "SourcePipelineExecutionArn": str,
    },
)

OutputParameterTypeDef = TypedDict(
    "OutputParameterTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

CandidateArtifactLocationsTypeDef = TypedDict(
    "CandidateArtifactLocationsTypeDef",
    {
        "Explainability": str,
        "ModelInsights": str,
        "BacktestResults": str,
    },
)

MetricDatumTypeDef = TypedDict(
    "MetricDatumTypeDef",
    {
        "MetricName": AutoMLMetricEnumType,
        "Value": float,
        "Set": MetricSetSourceType,
        "StandardMetricName": AutoMLMetricExtendedEnumType,
    },
)

ModelRegisterSettingsTypeDef = TypedDict(
    "ModelRegisterSettingsTypeDef",
    {
        "Status": FeatureStatusType,
        "CrossAccountModelRegisterRoleArn": str,
    },
    total=False,
)

TimeSeriesForecastingSettingsTypeDef = TypedDict(
    "TimeSeriesForecastingSettingsTypeDef",
    {
        "Status": FeatureStatusType,
        "AmazonForecastRoleArn": str,
    },
    total=False,
)

WorkspaceSettingsTypeDef = TypedDict(
    "WorkspaceSettingsTypeDef",
    {
        "S3ArtifactPath": str,
        "S3KmsKeyId": str,
    },
    total=False,
)

CapacitySizeTypeDef = TypedDict(
    "CapacitySizeTypeDef",
    {
        "Type": CapacitySizeTypeType,
        "Value": int,
    },
)

CaptureContentTypeHeaderTypeDef = TypedDict(
    "CaptureContentTypeHeaderTypeDef",
    {
        "CsvContentTypes": Sequence[str],
        "JsonContentTypes": Sequence[str],
    },
    total=False,
)

CaptureOptionTypeDef = TypedDict(
    "CaptureOptionTypeDef",
    {
        "CaptureMode": CaptureModeType,
    },
)

CategoricalParameterRangeSpecificationTypeDef = TypedDict(
    "CategoricalParameterRangeSpecificationTypeDef",
    {
        "Values": Sequence[str],
    },
)

CategoricalParameterRangeTypeDef = TypedDict(
    "CategoricalParameterRangeTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

CategoricalParameterTypeDef = TypedDict(
    "CategoricalParameterTypeDef",
    {
        "Name": str,
        "Value": Sequence[str],
    },
)

_RequiredChannelSpecificationTypeDef = TypedDict(
    "_RequiredChannelSpecificationTypeDef",
    {
        "Name": str,
        "SupportedContentTypes": Sequence[str],
        "SupportedInputModes": Sequence[TrainingInputModeType],
    },
)
_OptionalChannelSpecificationTypeDef = TypedDict(
    "_OptionalChannelSpecificationTypeDef",
    {
        "Description": str,
        "IsRequired": bool,
        "SupportedCompressionTypes": Sequence[CompressionTypeType],
    },
    total=False,
)


class ChannelSpecificationTypeDef(
    _RequiredChannelSpecificationTypeDef, _OptionalChannelSpecificationTypeDef
):
    pass


ShuffleConfigTypeDef = TypedDict(
    "ShuffleConfigTypeDef",
    {
        "Seed": int,
    },
)

_RequiredCheckpointConfigTypeDef = TypedDict(
    "_RequiredCheckpointConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalCheckpointConfigTypeDef = TypedDict(
    "_OptionalCheckpointConfigTypeDef",
    {
        "LocalPath": str,
    },
    total=False,
)


class CheckpointConfigTypeDef(_RequiredCheckpointConfigTypeDef, _OptionalCheckpointConfigTypeDef):
    pass


ClarifyCheckStepMetadataTypeDef = TypedDict(
    "ClarifyCheckStepMetadataTypeDef",
    {
        "CheckType": str,
        "BaselineUsedForDriftCheckConstraints": str,
        "CalculatedBaselineConstraints": str,
        "ModelPackageGroupName": str,
        "ViolationReport": str,
        "CheckJobArn": str,
        "SkipCheck": bool,
        "RegisterNewBaseline": bool,
    },
)

ClarifyInferenceConfigTypeDef = TypedDict(
    "ClarifyInferenceConfigTypeDef",
    {
        "FeaturesAttribute": str,
        "ContentTemplate": str,
        "MaxRecordCount": int,
        "MaxPayloadInMB": int,
        "ProbabilityIndex": int,
        "LabelIndex": int,
        "ProbabilityAttribute": str,
        "LabelAttribute": str,
        "LabelHeaders": Sequence[str],
        "FeatureHeaders": Sequence[str],
        "FeatureTypes": Sequence[ClarifyFeatureTypeType],
    },
    total=False,
)

ClarifyShapBaselineConfigTypeDef = TypedDict(
    "ClarifyShapBaselineConfigTypeDef",
    {
        "MimeType": str,
        "ShapBaseline": str,
        "ShapBaselineUri": str,
    },
    total=False,
)

ClarifyTextConfigTypeDef = TypedDict(
    "ClarifyTextConfigTypeDef",
    {
        "Language": ClarifyTextLanguageType,
        "Granularity": ClarifyTextGranularityType,
    },
)

_RequiredGitConfigTypeDef = TypedDict(
    "_RequiredGitConfigTypeDef",
    {
        "RepositoryUrl": str,
    },
)
_OptionalGitConfigTypeDef = TypedDict(
    "_OptionalGitConfigTypeDef",
    {
        "Branch": str,
        "SecretArn": str,
    },
    total=False,
)


class GitConfigTypeDef(_RequiredGitConfigTypeDef, _OptionalGitConfigTypeDef):
    pass


CodeRepositoryTypeDef = TypedDict(
    "CodeRepositoryTypeDef",
    {
        "RepositoryUrl": str,
    },
)

CognitoConfigTypeDef = TypedDict(
    "CognitoConfigTypeDef",
    {
        "UserPool": str,
        "ClientId": str,
    },
)

CognitoMemberDefinitionTypeDef = TypedDict(
    "CognitoMemberDefinitionTypeDef",
    {
        "UserPool": str,
        "UserGroup": str,
        "ClientId": str,
    },
)

CollectionConfigurationTypeDef = TypedDict(
    "CollectionConfigurationTypeDef",
    {
        "CollectionName": str,
        "CollectionParameters": Mapping[str, str],
    },
    total=False,
)

CompilationJobSummaryTypeDef = TypedDict(
    "CompilationJobSummaryTypeDef",
    {
        "CompilationJobName": str,
        "CompilationJobArn": str,
        "CreationTime": datetime,
        "CompilationStartTime": datetime,
        "CompilationEndTime": datetime,
        "CompilationTargetDevice": TargetDeviceType,
        "CompilationTargetPlatformOs": TargetPlatformOsType,
        "CompilationTargetPlatformArch": TargetPlatformArchType,
        "CompilationTargetPlatformAccelerator": TargetPlatformAcceleratorType,
        "LastModifiedTime": datetime,
        "CompilationJobStatus": CompilationJobStatusType,
    },
)

ConditionStepMetadataTypeDef = TypedDict(
    "ConditionStepMetadataTypeDef",
    {
        "Outcome": ConditionOutcomeType,
    },
)

MultiModelConfigTypeDef = TypedDict(
    "MultiModelConfigTypeDef",
    {
        "ModelCacheSetting": ModelCacheSettingType,
    },
    total=False,
)

_RequiredContextSourceTypeDef = TypedDict(
    "_RequiredContextSourceTypeDef",
    {
        "SourceUri": str,
    },
)
_OptionalContextSourceTypeDef = TypedDict(
    "_OptionalContextSourceTypeDef",
    {
        "SourceType": str,
        "SourceId": str,
    },
    total=False,
)


class ContextSourceTypeDef(_RequiredContextSourceTypeDef, _OptionalContextSourceTypeDef):
    pass


ContinuousParameterRangeSpecificationTypeDef = TypedDict(
    "ContinuousParameterRangeSpecificationTypeDef",
    {
        "MinValue": str,
        "MaxValue": str,
    },
)

_RequiredContinuousParameterRangeTypeDef = TypedDict(
    "_RequiredContinuousParameterRangeTypeDef",
    {
        "Name": str,
        "MinValue": str,
        "MaxValue": str,
    },
)
_OptionalContinuousParameterRangeTypeDef = TypedDict(
    "_OptionalContinuousParameterRangeTypeDef",
    {
        "ScalingType": HyperParameterScalingTypeType,
    },
    total=False,
)


class ContinuousParameterRangeTypeDef(
    _RequiredContinuousParameterRangeTypeDef, _OptionalContinuousParameterRangeTypeDef
):
    pass


ConvergenceDetectedTypeDef = TypedDict(
    "ConvergenceDetectedTypeDef",
    {
        "CompleteOnConvergence": CompleteOnConvergenceType,
    },
    total=False,
)

MetadataPropertiesTypeDef = TypedDict(
    "MetadataPropertiesTypeDef",
    {
        "CommitId": str,
        "Repository": str,
        "GeneratedBy": str,
        "ProjectId": str,
    },
    total=False,
)

CreateActionResponseTypeDef = TypedDict(
    "CreateActionResponseTypeDef",
    {
        "ActionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAlgorithmOutputTypeDef = TypedDict(
    "CreateAlgorithmOutputTypeDef",
    {
        "AlgorithmArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAppImageConfigResponseTypeDef = TypedDict(
    "CreateAppImageConfigResponseTypeDef",
    {
        "AppImageConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourceSpecTypeDef = TypedDict(
    "ResourceSpecTypeDef",
    {
        "SageMakerImageArn": str,
        "SageMakerImageVersionArn": str,
        "InstanceType": AppInstanceTypeType,
        "LifecycleConfigArn": str,
    },
    total=False,
)

CreateAppResponseTypeDef = TypedDict(
    "CreateAppResponseTypeDef",
    {
        "AppArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateArtifactResponseTypeDef = TypedDict(
    "CreateArtifactResponseTypeDef",
    {
        "ArtifactArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelDeployConfigTypeDef = TypedDict(
    "ModelDeployConfigTypeDef",
    {
        "AutoGenerateEndpointName": bool,
        "EndpointName": str,
    },
    total=False,
)

CreateAutoMLJobResponseTypeDef = TypedDict(
    "CreateAutoMLJobResponseTypeDef",
    {
        "AutoMLJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAutoMLJobV2ResponseTypeDef = TypedDict(
    "CreateAutoMLJobV2ResponseTypeDef",
    {
        "AutoMLJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateCodeRepositoryOutputTypeDef = TypedDict(
    "CreateCodeRepositoryOutputTypeDef",
    {
        "CodeRepositoryArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredInputConfigTypeDef = TypedDict(
    "_RequiredInputConfigTypeDef",
    {
        "S3Uri": str,
        "DataInputConfig": str,
        "Framework": FrameworkType,
    },
)
_OptionalInputConfigTypeDef = TypedDict(
    "_OptionalInputConfigTypeDef",
    {
        "FrameworkVersion": str,
    },
    total=False,
)


class InputConfigTypeDef(_RequiredInputConfigTypeDef, _OptionalInputConfigTypeDef):
    pass


NeoVpcConfigTypeDef = TypedDict(
    "NeoVpcConfigTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "Subnets": Sequence[str],
    },
)

StoppingConditionTypeDef = TypedDict(
    "StoppingConditionTypeDef",
    {
        "MaxRuntimeInSeconds": int,
        "MaxWaitTimeInSeconds": int,
    },
    total=False,
)

CreateCompilationJobResponseTypeDef = TypedDict(
    "CreateCompilationJobResponseTypeDef",
    {
        "CompilationJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateContextResponseTypeDef = TypedDict(
    "CreateContextResponseTypeDef",
    {
        "ContextArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDataQualityAppSpecificationTypeDef = TypedDict(
    "_RequiredDataQualityAppSpecificationTypeDef",
    {
        "ImageUri": str,
    },
)
_OptionalDataQualityAppSpecificationTypeDef = TypedDict(
    "_OptionalDataQualityAppSpecificationTypeDef",
    {
        "ContainerEntrypoint": Sequence[str],
        "ContainerArguments": Sequence[str],
        "RecordPreprocessorSourceUri": str,
        "PostAnalyticsProcessorSourceUri": str,
        "Environment": Mapping[str, str],
    },
    total=False,
)


class DataQualityAppSpecificationTypeDef(
    _RequiredDataQualityAppSpecificationTypeDef, _OptionalDataQualityAppSpecificationTypeDef
):
    pass


MonitoringStoppingConditionTypeDef = TypedDict(
    "MonitoringStoppingConditionTypeDef",
    {
        "MaxRuntimeInSeconds": int,
    },
)

CreateDataQualityJobDefinitionResponseTypeDef = TypedDict(
    "CreateDataQualityJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEdgeOutputConfigTypeDef = TypedDict(
    "_RequiredEdgeOutputConfigTypeDef",
    {
        "S3OutputLocation": str,
    },
)
_OptionalEdgeOutputConfigTypeDef = TypedDict(
    "_OptionalEdgeOutputConfigTypeDef",
    {
        "KmsKeyId": str,
        "PresetDeploymentType": Literal["GreengrassV2Component"],
        "PresetDeploymentConfig": str,
    },
    total=False,
)


class EdgeOutputConfigTypeDef(_RequiredEdgeOutputConfigTypeDef, _OptionalEdgeOutputConfigTypeDef):
    pass


CreateDomainResponseTypeDef = TypedDict(
    "CreateDomainResponseTypeDef",
    {
        "DomainArn": str,
        "Url": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EdgeDeploymentModelConfigTypeDef = TypedDict(
    "EdgeDeploymentModelConfigTypeDef",
    {
        "ModelHandle": str,
        "EdgePackagingJobName": str,
    },
)

CreateEdgeDeploymentPlanResponseTypeDef = TypedDict(
    "CreateEdgeDeploymentPlanResponseTypeDef",
    {
        "EdgeDeploymentPlanArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEndpointConfigOutputTypeDef = TypedDict(
    "CreateEndpointConfigOutputTypeDef",
    {
        "EndpointConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEndpointOutputTypeDef = TypedDict(
    "CreateEndpointOutputTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateExperimentResponseTypeDef = TypedDict(
    "CreateExperimentResponseTypeDef",
    {
        "ExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FeatureDefinitionTypeDef = TypedDict(
    "FeatureDefinitionTypeDef",
    {
        "FeatureName": str,
        "FeatureType": FeatureTypeType,
    },
    total=False,
)

CreateFeatureGroupResponseTypeDef = TypedDict(
    "CreateFeatureGroupResponseTypeDef",
    {
        "FeatureGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredFlowDefinitionOutputConfigTypeDef = TypedDict(
    "_RequiredFlowDefinitionOutputConfigTypeDef",
    {
        "S3OutputPath": str,
    },
)
_OptionalFlowDefinitionOutputConfigTypeDef = TypedDict(
    "_OptionalFlowDefinitionOutputConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class FlowDefinitionOutputConfigTypeDef(
    _RequiredFlowDefinitionOutputConfigTypeDef, _OptionalFlowDefinitionOutputConfigTypeDef
):
    pass


HumanLoopRequestSourceTypeDef = TypedDict(
    "HumanLoopRequestSourceTypeDef",
    {
        "AwsManagedHumanLoopRequestSource": AwsManagedHumanLoopRequestSourceType,
    },
)

CreateFlowDefinitionResponseTypeDef = TypedDict(
    "CreateFlowDefinitionResponseTypeDef",
    {
        "FlowDefinitionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HubS3StorageConfigTypeDef = TypedDict(
    "HubS3StorageConfigTypeDef",
    {
        "S3OutputPath": str,
    },
    total=False,
)

CreateHubResponseTypeDef = TypedDict(
    "CreateHubResponseTypeDef",
    {
        "HubArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UiTemplateTypeDef = TypedDict(
    "UiTemplateTypeDef",
    {
        "Content": str,
    },
)

CreateHumanTaskUiResponseTypeDef = TypedDict(
    "CreateHumanTaskUiResponseTypeDef",
    {
        "HumanTaskUiArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateHyperParameterTuningJobResponseTypeDef = TypedDict(
    "CreateHyperParameterTuningJobResponseTypeDef",
    {
        "HyperParameterTuningJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateImageResponseTypeDef = TypedDict(
    "CreateImageResponseTypeDef",
    {
        "ImageArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateImageVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageVersionRequestRequestTypeDef",
    {
        "BaseImage": str,
        "ClientToken": str,
        "ImageName": str,
    },
)
_OptionalCreateImageVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageVersionRequestRequestTypeDef",
    {
        "Aliases": Sequence[str],
        "VendorGuidance": VendorGuidanceType,
        "JobType": JobTypeType,
        "MLFramework": str,
        "ProgrammingLang": str,
        "Processor": ProcessorType,
        "Horovod": bool,
        "ReleaseNotes": str,
    },
    total=False,
)


class CreateImageVersionRequestRequestTypeDef(
    _RequiredCreateImageVersionRequestRequestTypeDef,
    _OptionalCreateImageVersionRequestRequestTypeDef,
):
    pass


CreateImageVersionResponseTypeDef = TypedDict(
    "CreateImageVersionResponseTypeDef",
    {
        "ImageVersionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InferenceExperimentScheduleTypeDef = TypedDict(
    "InferenceExperimentScheduleTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
    total=False,
)

CreateInferenceExperimentResponseTypeDef = TypedDict(
    "CreateInferenceExperimentResponseTypeDef",
    {
        "InferenceExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateInferenceRecommendationsJobResponseTypeDef = TypedDict(
    "CreateInferenceRecommendationsJobResponseTypeDef",
    {
        "JobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredLabelingJobOutputConfigTypeDef = TypedDict(
    "_RequiredLabelingJobOutputConfigTypeDef",
    {
        "S3OutputPath": str,
    },
)
_OptionalLabelingJobOutputConfigTypeDef = TypedDict(
    "_OptionalLabelingJobOutputConfigTypeDef",
    {
        "KmsKeyId": str,
        "SnsTopicArn": str,
    },
    total=False,
)


class LabelingJobOutputConfigTypeDef(
    _RequiredLabelingJobOutputConfigTypeDef, _OptionalLabelingJobOutputConfigTypeDef
):
    pass


LabelingJobStoppingConditionsTypeDef = TypedDict(
    "LabelingJobStoppingConditionsTypeDef",
    {
        "MaxHumanLabeledObjectCount": int,
        "MaxPercentageOfInputDatasetLabeled": int,
    },
    total=False,
)

CreateLabelingJobResponseTypeDef = TypedDict(
    "CreateLabelingJobResponseTypeDef",
    {
        "LabelingJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredModelBiasAppSpecificationTypeDef = TypedDict(
    "_RequiredModelBiasAppSpecificationTypeDef",
    {
        "ImageUri": str,
        "ConfigUri": str,
    },
)
_OptionalModelBiasAppSpecificationTypeDef = TypedDict(
    "_OptionalModelBiasAppSpecificationTypeDef",
    {
        "Environment": Mapping[str, str],
    },
    total=False,
)


class ModelBiasAppSpecificationTypeDef(
    _RequiredModelBiasAppSpecificationTypeDef, _OptionalModelBiasAppSpecificationTypeDef
):
    pass


CreateModelBiasJobDefinitionResponseTypeDef = TypedDict(
    "CreateModelBiasJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelCardExportOutputConfigTypeDef = TypedDict(
    "ModelCardExportOutputConfigTypeDef",
    {
        "S3OutputPath": str,
    },
)

CreateModelCardExportJobResponseTypeDef = TypedDict(
    "CreateModelCardExportJobResponseTypeDef",
    {
        "ModelCardExportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelCardSecurityConfigTypeDef = TypedDict(
    "ModelCardSecurityConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

CreateModelCardResponseTypeDef = TypedDict(
    "CreateModelCardResponseTypeDef",
    {
        "ModelCardArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredModelExplainabilityAppSpecificationTypeDef = TypedDict(
    "_RequiredModelExplainabilityAppSpecificationTypeDef",
    {
        "ImageUri": str,
        "ConfigUri": str,
    },
)
_OptionalModelExplainabilityAppSpecificationTypeDef = TypedDict(
    "_OptionalModelExplainabilityAppSpecificationTypeDef",
    {
        "Environment": Mapping[str, str],
    },
    total=False,
)


class ModelExplainabilityAppSpecificationTypeDef(
    _RequiredModelExplainabilityAppSpecificationTypeDef,
    _OptionalModelExplainabilityAppSpecificationTypeDef,
):
    pass


CreateModelExplainabilityJobDefinitionResponseTypeDef = TypedDict(
    "CreateModelExplainabilityJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InferenceExecutionConfigTypeDef = TypedDict(
    "InferenceExecutionConfigTypeDef",
    {
        "Mode": InferenceExecutionModeType,
    },
)

CreateModelOutputTypeDef = TypedDict(
    "CreateModelOutputTypeDef",
    {
        "ModelArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateModelPackageGroupOutputTypeDef = TypedDict(
    "CreateModelPackageGroupOutputTypeDef",
    {
        "ModelPackageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateModelPackageOutputTypeDef = TypedDict(
    "CreateModelPackageOutputTypeDef",
    {
        "ModelPackageArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredModelQualityAppSpecificationTypeDef = TypedDict(
    "_RequiredModelQualityAppSpecificationTypeDef",
    {
        "ImageUri": str,
    },
)
_OptionalModelQualityAppSpecificationTypeDef = TypedDict(
    "_OptionalModelQualityAppSpecificationTypeDef",
    {
        "ContainerEntrypoint": Sequence[str],
        "ContainerArguments": Sequence[str],
        "RecordPreprocessorSourceUri": str,
        "PostAnalyticsProcessorSourceUri": str,
        "ProblemType": MonitoringProblemTypeType,
        "Environment": Mapping[str, str],
    },
    total=False,
)


class ModelQualityAppSpecificationTypeDef(
    _RequiredModelQualityAppSpecificationTypeDef, _OptionalModelQualityAppSpecificationTypeDef
):
    pass


CreateModelQualityJobDefinitionResponseTypeDef = TypedDict(
    "CreateModelQualityJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMonitoringScheduleResponseTypeDef = TypedDict(
    "CreateMonitoringScheduleResponseTypeDef",
    {
        "MonitoringScheduleArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InstanceMetadataServiceConfigurationTypeDef = TypedDict(
    "InstanceMetadataServiceConfigurationTypeDef",
    {
        "MinimumInstanceMetadataServiceVersion": str,
    },
)

NotebookInstanceLifecycleHookTypeDef = TypedDict(
    "NotebookInstanceLifecycleHookTypeDef",
    {
        "Content": str,
    },
    total=False,
)

CreateNotebookInstanceLifecycleConfigOutputTypeDef = TypedDict(
    "CreateNotebookInstanceLifecycleConfigOutputTypeDef",
    {
        "NotebookInstanceLifecycleConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateNotebookInstanceOutputTypeDef = TypedDict(
    "CreateNotebookInstanceOutputTypeDef",
    {
        "NotebookInstanceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ParallelismConfigurationTypeDef = TypedDict(
    "ParallelismConfigurationTypeDef",
    {
        "MaxParallelExecutionSteps": int,
    },
)

_RequiredPipelineDefinitionS3LocationTypeDef = TypedDict(
    "_RequiredPipelineDefinitionS3LocationTypeDef",
    {
        "Bucket": str,
        "ObjectKey": str,
    },
)
_OptionalPipelineDefinitionS3LocationTypeDef = TypedDict(
    "_OptionalPipelineDefinitionS3LocationTypeDef",
    {
        "VersionId": str,
    },
    total=False,
)


class PipelineDefinitionS3LocationTypeDef(
    _RequiredPipelineDefinitionS3LocationTypeDef, _OptionalPipelineDefinitionS3LocationTypeDef
):
    pass


CreatePipelineResponseTypeDef = TypedDict(
    "CreatePipelineResponseTypeDef",
    {
        "PipelineArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePresignedDomainUrlRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePresignedDomainUrlRequestRequestTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
    },
)
_OptionalCreatePresignedDomainUrlRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePresignedDomainUrlRequestRequestTypeDef",
    {
        "SessionExpirationDurationInSeconds": int,
        "ExpiresInSeconds": int,
        "SpaceName": str,
    },
    total=False,
)


class CreatePresignedDomainUrlRequestRequestTypeDef(
    _RequiredCreatePresignedDomainUrlRequestRequestTypeDef,
    _OptionalCreatePresignedDomainUrlRequestRequestTypeDef,
):
    pass


CreatePresignedDomainUrlResponseTypeDef = TypedDict(
    "CreatePresignedDomainUrlResponseTypeDef",
    {
        "AuthorizedUrl": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePresignedNotebookInstanceUrlInputRequestTypeDef = TypedDict(
    "_RequiredCreatePresignedNotebookInstanceUrlInputRequestTypeDef",
    {
        "NotebookInstanceName": str,
    },
)
_OptionalCreatePresignedNotebookInstanceUrlInputRequestTypeDef = TypedDict(
    "_OptionalCreatePresignedNotebookInstanceUrlInputRequestTypeDef",
    {
        "SessionExpirationDurationInSeconds": int,
    },
    total=False,
)


class CreatePresignedNotebookInstanceUrlInputRequestTypeDef(
    _RequiredCreatePresignedNotebookInstanceUrlInputRequestTypeDef,
    _OptionalCreatePresignedNotebookInstanceUrlInputRequestTypeDef,
):
    pass


CreatePresignedNotebookInstanceUrlOutputTypeDef = TypedDict(
    "CreatePresignedNotebookInstanceUrlOutputTypeDef",
    {
        "AuthorizedUrl": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExperimentConfigTypeDef = TypedDict(
    "ExperimentConfigTypeDef",
    {
        "ExperimentName": str,
        "TrialName": str,
        "TrialComponentDisplayName": str,
        "RunName": str,
    },
    total=False,
)

ProcessingStoppingConditionTypeDef = TypedDict(
    "ProcessingStoppingConditionTypeDef",
    {
        "MaxRuntimeInSeconds": int,
    },
)

CreateProcessingJobResponseTypeDef = TypedDict(
    "CreateProcessingJobResponseTypeDef",
    {
        "ProcessingJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateProjectOutputTypeDef = TypedDict(
    "CreateProjectOutputTypeDef",
    {
        "ProjectArn": str,
        "ProjectId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateSpaceResponseTypeDef = TypedDict(
    "CreateSpaceResponseTypeDef",
    {
        "SpaceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateStudioLifecycleConfigResponseTypeDef = TypedDict(
    "CreateStudioLifecycleConfigResponseTypeDef",
    {
        "StudioLifecycleConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDebugRuleConfigurationTypeDef = TypedDict(
    "_RequiredDebugRuleConfigurationTypeDef",
    {
        "RuleConfigurationName": str,
        "RuleEvaluatorImage": str,
    },
)
_OptionalDebugRuleConfigurationTypeDef = TypedDict(
    "_OptionalDebugRuleConfigurationTypeDef",
    {
        "LocalPath": str,
        "S3OutputPath": str,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
        "RuleParameters": Mapping[str, str],
    },
    total=False,
)


class DebugRuleConfigurationTypeDef(
    _RequiredDebugRuleConfigurationTypeDef, _OptionalDebugRuleConfigurationTypeDef
):
    pass


_RequiredOutputDataConfigTypeDef = TypedDict(
    "_RequiredOutputDataConfigTypeDef",
    {
        "S3OutputPath": str,
    },
)
_OptionalOutputDataConfigTypeDef = TypedDict(
    "_OptionalOutputDataConfigTypeDef",
    {
        "KmsKeyId": str,
        "CompressionType": OutputCompressionTypeType,
    },
    total=False,
)


class OutputDataConfigTypeDef(_RequiredOutputDataConfigTypeDef, _OptionalOutputDataConfigTypeDef):
    pass


ProfilerConfigTypeDef = TypedDict(
    "ProfilerConfigTypeDef",
    {
        "S3OutputPath": str,
        "ProfilingIntervalInMilliseconds": int,
        "ProfilingParameters": Mapping[str, str],
        "DisableProfiler": bool,
    },
    total=False,
)

_RequiredProfilerRuleConfigurationTypeDef = TypedDict(
    "_RequiredProfilerRuleConfigurationTypeDef",
    {
        "RuleConfigurationName": str,
        "RuleEvaluatorImage": str,
    },
)
_OptionalProfilerRuleConfigurationTypeDef = TypedDict(
    "_OptionalProfilerRuleConfigurationTypeDef",
    {
        "LocalPath": str,
        "S3OutputPath": str,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
        "RuleParameters": Mapping[str, str],
    },
    total=False,
)


class ProfilerRuleConfigurationTypeDef(
    _RequiredProfilerRuleConfigurationTypeDef, _OptionalProfilerRuleConfigurationTypeDef
):
    pass


RetryStrategyTypeDef = TypedDict(
    "RetryStrategyTypeDef",
    {
        "MaximumRetryAttempts": int,
    },
)

_RequiredTensorBoardOutputConfigTypeDef = TypedDict(
    "_RequiredTensorBoardOutputConfigTypeDef",
    {
        "S3OutputPath": str,
    },
)
_OptionalTensorBoardOutputConfigTypeDef = TypedDict(
    "_OptionalTensorBoardOutputConfigTypeDef",
    {
        "LocalPath": str,
    },
    total=False,
)


class TensorBoardOutputConfigTypeDef(
    _RequiredTensorBoardOutputConfigTypeDef, _OptionalTensorBoardOutputConfigTypeDef
):
    pass


CreateTrainingJobResponseTypeDef = TypedDict(
    "CreateTrainingJobResponseTypeDef",
    {
        "TrainingJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataProcessingTypeDef = TypedDict(
    "DataProcessingTypeDef",
    {
        "InputFilter": str,
        "OutputFilter": str,
        "JoinSource": JoinSourceType,
    },
    total=False,
)

ModelClientConfigTypeDef = TypedDict(
    "ModelClientConfigTypeDef",
    {
        "InvocationsTimeoutInSeconds": int,
        "InvocationsMaxRetries": int,
    },
    total=False,
)

_RequiredTransformOutputTypeDef = TypedDict(
    "_RequiredTransformOutputTypeDef",
    {
        "S3OutputPath": str,
    },
)
_OptionalTransformOutputTypeDef = TypedDict(
    "_OptionalTransformOutputTypeDef",
    {
        "Accept": str,
        "AssembleWith": AssemblyTypeType,
        "KmsKeyId": str,
    },
    total=False,
)


class TransformOutputTypeDef(_RequiredTransformOutputTypeDef, _OptionalTransformOutputTypeDef):
    pass


_RequiredTransformResourcesTypeDef = TypedDict(
    "_RequiredTransformResourcesTypeDef",
    {
        "InstanceType": TransformInstanceTypeType,
        "InstanceCount": int,
    },
)
_OptionalTransformResourcesTypeDef = TypedDict(
    "_OptionalTransformResourcesTypeDef",
    {
        "VolumeKmsKeyId": str,
    },
    total=False,
)


class TransformResourcesTypeDef(
    _RequiredTransformResourcesTypeDef, _OptionalTransformResourcesTypeDef
):
    pass


CreateTransformJobResponseTypeDef = TypedDict(
    "CreateTransformJobResponseTypeDef",
    {
        "TransformJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredTrialComponentArtifactTypeDef = TypedDict(
    "_RequiredTrialComponentArtifactTypeDef",
    {
        "Value": str,
    },
)
_OptionalTrialComponentArtifactTypeDef = TypedDict(
    "_OptionalTrialComponentArtifactTypeDef",
    {
        "MediaType": str,
    },
    total=False,
)


class TrialComponentArtifactTypeDef(
    _RequiredTrialComponentArtifactTypeDef, _OptionalTrialComponentArtifactTypeDef
):
    pass


TrialComponentParameterValueTypeDef = TypedDict(
    "TrialComponentParameterValueTypeDef",
    {
        "StringValue": str,
        "NumberValue": float,
    },
    total=False,
)

TrialComponentStatusTypeDef = TypedDict(
    "TrialComponentStatusTypeDef",
    {
        "PrimaryStatus": TrialComponentPrimaryStatusType,
        "Message": str,
    },
    total=False,
)

CreateTrialComponentResponseTypeDef = TypedDict(
    "CreateTrialComponentResponseTypeDef",
    {
        "TrialComponentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateTrialResponseTypeDef = TypedDict(
    "CreateTrialResponseTypeDef",
    {
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateUserProfileResponseTypeDef = TypedDict(
    "CreateUserProfileResponseTypeDef",
    {
        "UserProfileArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

OidcConfigTypeDef = TypedDict(
    "OidcConfigTypeDef",
    {
        "ClientId": str,
        "ClientSecret": str,
        "Issuer": str,
        "AuthorizationEndpoint": str,
        "TokenEndpoint": str,
        "UserInfoEndpoint": str,
        "LogoutEndpoint": str,
        "JwksUri": str,
    },
)

SourceIpConfigTypeDef = TypedDict(
    "SourceIpConfigTypeDef",
    {
        "Cidrs": Sequence[str],
    },
)

WorkforceVpcConfigRequestTypeDef = TypedDict(
    "WorkforceVpcConfigRequestTypeDef",
    {
        "VpcId": str,
        "SecurityGroupIds": Sequence[str],
        "Subnets": Sequence[str],
    },
    total=False,
)

CreateWorkforceResponseTypeDef = TypedDict(
    "CreateWorkforceResponseTypeDef",
    {
        "WorkforceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "NotificationTopicArn": str,
    },
    total=False,
)

CreateWorkteamResponseTypeDef = TypedDict(
    "CreateWorkteamResponseTypeDef",
    {
        "WorkteamArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCustomImageTypeDef = TypedDict(
    "_RequiredCustomImageTypeDef",
    {
        "ImageName": str,
        "AppImageConfigName": str,
    },
)
_OptionalCustomImageTypeDef = TypedDict(
    "_OptionalCustomImageTypeDef",
    {
        "ImageVersionNumber": int,
    },
    total=False,
)


class CustomImageTypeDef(_RequiredCustomImageTypeDef, _OptionalCustomImageTypeDef):
    pass


DataCaptureConfigSummaryTypeDef = TypedDict(
    "DataCaptureConfigSummaryTypeDef",
    {
        "EnableCapture": bool,
        "CaptureStatus": CaptureStatusType,
        "CurrentSamplingPercentage": int,
        "DestinationS3Uri": str,
        "KmsKeyId": str,
    },
)

DataCatalogConfigTypeDef = TypedDict(
    "DataCatalogConfigTypeDef",
    {
        "TableName": str,
        "Catalog": str,
        "Database": str,
    },
)

MonitoringConstraintsResourceTypeDef = TypedDict(
    "MonitoringConstraintsResourceTypeDef",
    {
        "S3Uri": str,
    },
    total=False,
)

MonitoringStatisticsResourceTypeDef = TypedDict(
    "MonitoringStatisticsResourceTypeDef",
    {
        "S3Uri": str,
    },
    total=False,
)

_RequiredEndpointInputTypeDef = TypedDict(
    "_RequiredEndpointInputTypeDef",
    {
        "EndpointName": str,
        "LocalPath": str,
    },
)
_OptionalEndpointInputTypeDef = TypedDict(
    "_OptionalEndpointInputTypeDef",
    {
        "S3InputMode": ProcessingS3InputModeType,
        "S3DataDistributionType": ProcessingS3DataDistributionTypeType,
        "FeaturesAttribute": str,
        "InferenceAttribute": str,
        "ProbabilityAttribute": str,
        "ProbabilityThresholdAttribute": float,
        "StartTimeOffset": str,
        "EndTimeOffset": str,
    },
    total=False,
)


class EndpointInputTypeDef(_RequiredEndpointInputTypeDef, _OptionalEndpointInputTypeDef):
    pass


FileSystemDataSourceTypeDef = TypedDict(
    "FileSystemDataSourceTypeDef",
    {
        "FileSystemId": str,
        "FileSystemAccessMode": FileSystemAccessModeType,
        "FileSystemType": FileSystemTypeType,
        "DirectoryPath": str,
    },
)

_RequiredS3DataSourceTypeDef = TypedDict(
    "_RequiredS3DataSourceTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
    },
)
_OptionalS3DataSourceTypeDef = TypedDict(
    "_OptionalS3DataSourceTypeDef",
    {
        "S3DataDistributionType": S3DataDistributionType,
        "AttributeNames": Sequence[str],
        "InstanceGroupNames": Sequence[str],
    },
    total=False,
)


class S3DataSourceTypeDef(_RequiredS3DataSourceTypeDef, _OptionalS3DataSourceTypeDef):
    pass


_RequiredRedshiftDatasetDefinitionTypeDef = TypedDict(
    "_RequiredRedshiftDatasetDefinitionTypeDef",
    {
        "ClusterId": str,
        "Database": str,
        "DbUser": str,
        "QueryString": str,
        "ClusterRoleArn": str,
        "OutputS3Uri": str,
        "OutputFormat": RedshiftResultFormatType,
    },
)
_OptionalRedshiftDatasetDefinitionTypeDef = TypedDict(
    "_OptionalRedshiftDatasetDefinitionTypeDef",
    {
        "KmsKeyId": str,
        "OutputCompression": RedshiftResultCompressionTypeType,
    },
    total=False,
)


class RedshiftDatasetDefinitionTypeDef(
    _RequiredRedshiftDatasetDefinitionTypeDef, _OptionalRedshiftDatasetDefinitionTypeDef
):
    pass


DebugRuleEvaluationStatusTypeDef = TypedDict(
    "DebugRuleEvaluationStatusTypeDef",
    {
        "RuleConfigurationName": str,
        "RuleEvaluationJobArn": str,
        "RuleEvaluationStatus": RuleEvaluationStatusType,
        "StatusDetails": str,
        "LastModifiedTime": datetime,
    },
)

DeleteActionRequestRequestTypeDef = TypedDict(
    "DeleteActionRequestRequestTypeDef",
    {
        "ActionName": str,
    },
)

DeleteActionResponseTypeDef = TypedDict(
    "DeleteActionResponseTypeDef",
    {
        "ActionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteAlgorithmInputRequestTypeDef = TypedDict(
    "DeleteAlgorithmInputRequestTypeDef",
    {
        "AlgorithmName": str,
    },
)

DeleteAppImageConfigRequestRequestTypeDef = TypedDict(
    "DeleteAppImageConfigRequestRequestTypeDef",
    {
        "AppImageConfigName": str,
    },
)

_RequiredDeleteAppRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAppRequestRequestTypeDef",
    {
        "DomainId": str,
        "AppType": AppTypeType,
        "AppName": str,
    },
)
_OptionalDeleteAppRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAppRequestRequestTypeDef",
    {
        "UserProfileName": str,
        "SpaceName": str,
    },
    total=False,
)


class DeleteAppRequestRequestTypeDef(
    _RequiredDeleteAppRequestRequestTypeDef, _OptionalDeleteAppRequestRequestTypeDef
):
    pass


DeleteArtifactResponseTypeDef = TypedDict(
    "DeleteArtifactResponseTypeDef",
    {
        "ArtifactArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteAssociationRequestRequestTypeDef = TypedDict(
    "DeleteAssociationRequestRequestTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
    },
)

DeleteAssociationResponseTypeDef = TypedDict(
    "DeleteAssociationResponseTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteCodeRepositoryInputRequestTypeDef = TypedDict(
    "DeleteCodeRepositoryInputRequestTypeDef",
    {
        "CodeRepositoryName": str,
    },
)

DeleteContextRequestRequestTypeDef = TypedDict(
    "DeleteContextRequestRequestTypeDef",
    {
        "ContextName": str,
    },
)

DeleteContextResponseTypeDef = TypedDict(
    "DeleteContextResponseTypeDef",
    {
        "ContextArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteDataQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteDataQualityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DeleteDeviceFleetRequestRequestTypeDef = TypedDict(
    "DeleteDeviceFleetRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
    },
)

RetentionPolicyTypeDef = TypedDict(
    "RetentionPolicyTypeDef",
    {
        "HomeEfsFileSystem": RetentionTypeType,
    },
    total=False,
)

DeleteEdgeDeploymentPlanRequestRequestTypeDef = TypedDict(
    "DeleteEdgeDeploymentPlanRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
    },
)

DeleteEdgeDeploymentStageRequestRequestTypeDef = TypedDict(
    "DeleteEdgeDeploymentStageRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
        "StageName": str,
    },
)

DeleteEndpointConfigInputRequestTypeDef = TypedDict(
    "DeleteEndpointConfigInputRequestTypeDef",
    {
        "EndpointConfigName": str,
    },
)

DeleteEndpointInputRequestTypeDef = TypedDict(
    "DeleteEndpointInputRequestTypeDef",
    {
        "EndpointName": str,
    },
)

DeleteExperimentRequestRequestTypeDef = TypedDict(
    "DeleteExperimentRequestRequestTypeDef",
    {
        "ExperimentName": str,
    },
)

DeleteExperimentResponseTypeDef = TypedDict(
    "DeleteExperimentResponseTypeDef",
    {
        "ExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteFeatureGroupRequestRequestTypeDef = TypedDict(
    "DeleteFeatureGroupRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
    },
)

DeleteFlowDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteFlowDefinitionRequestRequestTypeDef",
    {
        "FlowDefinitionName": str,
    },
)

DeleteHubContentRequestRequestTypeDef = TypedDict(
    "DeleteHubContentRequestRequestTypeDef",
    {
        "HubName": str,
        "HubContentType": HubContentTypeType,
        "HubContentName": str,
        "HubContentVersion": str,
    },
)

DeleteHubRequestRequestTypeDef = TypedDict(
    "DeleteHubRequestRequestTypeDef",
    {
        "HubName": str,
    },
)

DeleteHumanTaskUiRequestRequestTypeDef = TypedDict(
    "DeleteHumanTaskUiRequestRequestTypeDef",
    {
        "HumanTaskUiName": str,
    },
)

DeleteImageRequestRequestTypeDef = TypedDict(
    "DeleteImageRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)

_RequiredDeleteImageVersionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteImageVersionRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalDeleteImageVersionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteImageVersionRequestRequestTypeDef",
    {
        "Version": int,
        "Alias": str,
    },
    total=False,
)


class DeleteImageVersionRequestRequestTypeDef(
    _RequiredDeleteImageVersionRequestRequestTypeDef,
    _OptionalDeleteImageVersionRequestRequestTypeDef,
):
    pass


DeleteInferenceExperimentRequestRequestTypeDef = TypedDict(
    "DeleteInferenceExperimentRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteInferenceExperimentResponseTypeDef = TypedDict(
    "DeleteInferenceExperimentResponseTypeDef",
    {
        "InferenceExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteModelBiasJobDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteModelBiasJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DeleteModelCardRequestRequestTypeDef = TypedDict(
    "DeleteModelCardRequestRequestTypeDef",
    {
        "ModelCardName": str,
    },
)

DeleteModelExplainabilityJobDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteModelExplainabilityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DeleteModelInputRequestTypeDef = TypedDict(
    "DeleteModelInputRequestTypeDef",
    {
        "ModelName": str,
    },
)

DeleteModelPackageGroupInputRequestTypeDef = TypedDict(
    "DeleteModelPackageGroupInputRequestTypeDef",
    {
        "ModelPackageGroupName": str,
    },
)

DeleteModelPackageGroupPolicyInputRequestTypeDef = TypedDict(
    "DeleteModelPackageGroupPolicyInputRequestTypeDef",
    {
        "ModelPackageGroupName": str,
    },
)

DeleteModelPackageInputRequestTypeDef = TypedDict(
    "DeleteModelPackageInputRequestTypeDef",
    {
        "ModelPackageName": str,
    },
)

DeleteModelQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteModelQualityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DeleteMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "DeleteMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
    },
)

DeleteNotebookInstanceInputRequestTypeDef = TypedDict(
    "DeleteNotebookInstanceInputRequestTypeDef",
    {
        "NotebookInstanceName": str,
    },
)

DeleteNotebookInstanceLifecycleConfigInputRequestTypeDef = TypedDict(
    "DeleteNotebookInstanceLifecycleConfigInputRequestTypeDef",
    {
        "NotebookInstanceLifecycleConfigName": str,
    },
)

DeletePipelineRequestRequestTypeDef = TypedDict(
    "DeletePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
        "ClientRequestToken": str,
    },
)

DeletePipelineResponseTypeDef = TypedDict(
    "DeletePipelineResponseTypeDef",
    {
        "PipelineArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteProjectInputRequestTypeDef = TypedDict(
    "DeleteProjectInputRequestTypeDef",
    {
        "ProjectName": str,
    },
)

DeleteSpaceRequestRequestTypeDef = TypedDict(
    "DeleteSpaceRequestRequestTypeDef",
    {
        "DomainId": str,
        "SpaceName": str,
    },
)

DeleteStudioLifecycleConfigRequestRequestTypeDef = TypedDict(
    "DeleteStudioLifecycleConfigRequestRequestTypeDef",
    {
        "StudioLifecycleConfigName": str,
    },
)

DeleteTagsInputRequestTypeDef = TypedDict(
    "DeleteTagsInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

DeleteTrialComponentRequestRequestTypeDef = TypedDict(
    "DeleteTrialComponentRequestRequestTypeDef",
    {
        "TrialComponentName": str,
    },
)

DeleteTrialComponentResponseTypeDef = TypedDict(
    "DeleteTrialComponentResponseTypeDef",
    {
        "TrialComponentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteTrialRequestRequestTypeDef = TypedDict(
    "DeleteTrialRequestRequestTypeDef",
    {
        "TrialName": str,
    },
)

DeleteTrialResponseTypeDef = TypedDict(
    "DeleteTrialResponseTypeDef",
    {
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteUserProfileRequestRequestTypeDef = TypedDict(
    "DeleteUserProfileRequestRequestTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
    },
)

DeleteWorkforceRequestRequestTypeDef = TypedDict(
    "DeleteWorkforceRequestRequestTypeDef",
    {
        "WorkforceName": str,
    },
)

DeleteWorkteamRequestRequestTypeDef = TypedDict(
    "DeleteWorkteamRequestRequestTypeDef",
    {
        "WorkteamName": str,
    },
)

DeleteWorkteamResponseTypeDef = TypedDict(
    "DeleteWorkteamResponseTypeDef",
    {
        "Success": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeployedImageTypeDef = TypedDict(
    "DeployedImageTypeDef",
    {
        "SpecifiedImage": str,
        "ResolvedImage": str,
        "ResolutionTime": datetime,
    },
)

RealTimeInferenceRecommendationTypeDef = TypedDict(
    "RealTimeInferenceRecommendationTypeDef",
    {
        "RecommendationId": str,
        "InstanceType": ProductionVariantInstanceTypeType,
        "Environment": Dict[str, str],
    },
)

_RequiredDeviceSelectionConfigTypeDef = TypedDict(
    "_RequiredDeviceSelectionConfigTypeDef",
    {
        "DeviceSubsetType": DeviceSubsetTypeType,
    },
)
_OptionalDeviceSelectionConfigTypeDef = TypedDict(
    "_OptionalDeviceSelectionConfigTypeDef",
    {
        "Percentage": int,
        "DeviceNames": Sequence[str],
        "DeviceNameContains": str,
    },
    total=False,
)


class DeviceSelectionConfigTypeDef(
    _RequiredDeviceSelectionConfigTypeDef, _OptionalDeviceSelectionConfigTypeDef
):
    pass


EdgeDeploymentConfigTypeDef = TypedDict(
    "EdgeDeploymentConfigTypeDef",
    {
        "FailureHandlingPolicy": FailureHandlingPolicyType,
    },
)

EdgeDeploymentStatusTypeDef = TypedDict(
    "EdgeDeploymentStatusTypeDef",
    {
        "StageStatus": StageStatusType,
        "EdgeDeploymentSuccessInStage": int,
        "EdgeDeploymentPendingInStage": int,
        "EdgeDeploymentFailedInStage": int,
        "EdgeDeploymentStatusMessage": str,
        "EdgeDeploymentStageStartTime": datetime,
    },
)

DeregisterDevicesRequestRequestTypeDef = TypedDict(
    "DeregisterDevicesRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
        "DeviceNames": Sequence[str],
    },
)

DescribeActionRequestRequestTypeDef = TypedDict(
    "DescribeActionRequestRequestTypeDef",
    {
        "ActionName": str,
    },
)

DescribeAlgorithmInputRequestTypeDef = TypedDict(
    "DescribeAlgorithmInputRequestTypeDef",
    {
        "AlgorithmName": str,
    },
)

DescribeAppImageConfigRequestRequestTypeDef = TypedDict(
    "DescribeAppImageConfigRequestRequestTypeDef",
    {
        "AppImageConfigName": str,
    },
)

_RequiredDescribeAppRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAppRequestRequestTypeDef",
    {
        "DomainId": str,
        "AppType": AppTypeType,
        "AppName": str,
    },
)
_OptionalDescribeAppRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAppRequestRequestTypeDef",
    {
        "UserProfileName": str,
        "SpaceName": str,
    },
    total=False,
)


class DescribeAppRequestRequestTypeDef(
    _RequiredDescribeAppRequestRequestTypeDef, _OptionalDescribeAppRequestRequestTypeDef
):
    pass


DescribeArtifactRequestRequestTypeDef = TypedDict(
    "DescribeArtifactRequestRequestTypeDef",
    {
        "ArtifactArn": str,
    },
)

DescribeAutoMLJobRequestRequestTypeDef = TypedDict(
    "DescribeAutoMLJobRequestRequestTypeDef",
    {
        "AutoMLJobName": str,
    },
)

ModelDeployResultTypeDef = TypedDict(
    "ModelDeployResultTypeDef",
    {
        "EndpointName": str,
    },
)

DescribeAutoMLJobV2RequestRequestTypeDef = TypedDict(
    "DescribeAutoMLJobV2RequestRequestTypeDef",
    {
        "AutoMLJobName": str,
    },
)

DescribeCodeRepositoryInputRequestTypeDef = TypedDict(
    "DescribeCodeRepositoryInputRequestTypeDef",
    {
        "CodeRepositoryName": str,
    },
)

DescribeCompilationJobRequestRequestTypeDef = TypedDict(
    "DescribeCompilationJobRequestRequestTypeDef",
    {
        "CompilationJobName": str,
    },
)

ModelArtifactsTypeDef = TypedDict(
    "ModelArtifactsTypeDef",
    {
        "S3ModelArtifacts": str,
    },
)

ModelDigestsTypeDef = TypedDict(
    "ModelDigestsTypeDef",
    {
        "ArtifactDigest": str,
    },
)

DescribeContextRequestRequestTypeDef = TypedDict(
    "DescribeContextRequestRequestTypeDef",
    {
        "ContextName": str,
    },
)

DescribeDataQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeDataQualityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DescribeDeviceFleetRequestRequestTypeDef = TypedDict(
    "DescribeDeviceFleetRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
    },
)

_RequiredDescribeDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDeviceRequestRequestTypeDef",
    {
        "DeviceName": str,
        "DeviceFleetName": str,
    },
)
_OptionalDescribeDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDeviceRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class DescribeDeviceRequestRequestTypeDef(
    _RequiredDescribeDeviceRequestRequestTypeDef, _OptionalDescribeDeviceRequestRequestTypeDef
):
    pass


EdgeModelTypeDef = TypedDict(
    "EdgeModelTypeDef",
    {
        "ModelName": str,
        "ModelVersion": str,
        "LatestSampleTime": datetime,
        "LatestInference": datetime,
    },
)

DescribeDomainRequestRequestTypeDef = TypedDict(
    "DescribeDomainRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)

_RequiredDescribeEdgeDeploymentPlanRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEdgeDeploymentPlanRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
    },
)
_OptionalDescribeEdgeDeploymentPlanRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEdgeDeploymentPlanRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeEdgeDeploymentPlanRequestRequestTypeDef(
    _RequiredDescribeEdgeDeploymentPlanRequestRequestTypeDef,
    _OptionalDescribeEdgeDeploymentPlanRequestRequestTypeDef,
):
    pass


DescribeEdgePackagingJobRequestRequestTypeDef = TypedDict(
    "DescribeEdgePackagingJobRequestRequestTypeDef",
    {
        "EdgePackagingJobName": str,
    },
)

EdgePresetDeploymentOutputTypeDef = TypedDict(
    "EdgePresetDeploymentOutputTypeDef",
    {
        "Type": Literal["GreengrassV2Component"],
        "Artifact": str,
        "Status": EdgePresetDeploymentStatusType,
        "StatusMessage": str,
    },
)

DescribeEndpointConfigInputRequestTypeDef = TypedDict(
    "DescribeEndpointConfigInputRequestTypeDef",
    {
        "EndpointConfigName": str,
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

DescribeEndpointInputRequestTypeDef = TypedDict(
    "DescribeEndpointInputRequestTypeDef",
    {
        "EndpointName": str,
    },
)

DescribeExperimentRequestRequestTypeDef = TypedDict(
    "DescribeExperimentRequestRequestTypeDef",
    {
        "ExperimentName": str,
    },
)

ExperimentSourceTypeDef = TypedDict(
    "ExperimentSourceTypeDef",
    {
        "SourceArn": str,
        "SourceType": str,
    },
)

_RequiredDescribeFeatureGroupRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeFeatureGroupRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
    },
)
_OptionalDescribeFeatureGroupRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeFeatureGroupRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class DescribeFeatureGroupRequestRequestTypeDef(
    _RequiredDescribeFeatureGroupRequestRequestTypeDef,
    _OptionalDescribeFeatureGroupRequestRequestTypeDef,
):
    pass


LastUpdateStatusTypeDef = TypedDict(
    "LastUpdateStatusTypeDef",
    {
        "Status": LastUpdateStatusValueType,
        "FailureReason": str,
    },
)

OfflineStoreStatusTypeDef = TypedDict(
    "OfflineStoreStatusTypeDef",
    {
        "Status": OfflineStoreStatusValueType,
        "BlockedReason": str,
    },
)

DescribeFeatureMetadataRequestRequestTypeDef = TypedDict(
    "DescribeFeatureMetadataRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
        "FeatureName": str,
    },
)

FeatureParameterTypeDef = TypedDict(
    "FeatureParameterTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DescribeFlowDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeFlowDefinitionRequestRequestTypeDef",
    {
        "FlowDefinitionName": str,
    },
)

_RequiredDescribeHubContentRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeHubContentRequestRequestTypeDef",
    {
        "HubName": str,
        "HubContentType": HubContentTypeType,
        "HubContentName": str,
    },
)
_OptionalDescribeHubContentRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeHubContentRequestRequestTypeDef",
    {
        "HubContentVersion": str,
    },
    total=False,
)


class DescribeHubContentRequestRequestTypeDef(
    _RequiredDescribeHubContentRequestRequestTypeDef,
    _OptionalDescribeHubContentRequestRequestTypeDef,
):
    pass


HubContentDependencyTypeDef = TypedDict(
    "HubContentDependencyTypeDef",
    {
        "DependencyOriginPath": str,
        "DependencyCopyPath": str,
    },
)

DescribeHubRequestRequestTypeDef = TypedDict(
    "DescribeHubRequestRequestTypeDef",
    {
        "HubName": str,
    },
)

DescribeHumanTaskUiRequestRequestTypeDef = TypedDict(
    "DescribeHumanTaskUiRequestRequestTypeDef",
    {
        "HumanTaskUiName": str,
    },
)

UiTemplateInfoTypeDef = TypedDict(
    "UiTemplateInfoTypeDef",
    {
        "Url": str,
        "ContentSha256": str,
    },
)

DescribeHyperParameterTuningJobRequestRequestTypeDef = TypedDict(
    "DescribeHyperParameterTuningJobRequestRequestTypeDef",
    {
        "HyperParameterTuningJobName": str,
    },
)

HyperParameterTuningJobCompletionDetailsTypeDef = TypedDict(
    "HyperParameterTuningJobCompletionDetailsTypeDef",
    {
        "NumberOfTrainingJobsObjectiveNotImproving": int,
        "ConvergenceDetectedTime": datetime,
    },
)

HyperParameterTuningJobConsumedResourcesTypeDef = TypedDict(
    "HyperParameterTuningJobConsumedResourcesTypeDef",
    {
        "RuntimeInSeconds": int,
    },
)

ObjectiveStatusCountersTypeDef = TypedDict(
    "ObjectiveStatusCountersTypeDef",
    {
        "Succeeded": int,
        "Pending": int,
        "Failed": int,
    },
)

TrainingJobStatusCountersTypeDef = TypedDict(
    "TrainingJobStatusCountersTypeDef",
    {
        "Completed": int,
        "InProgress": int,
        "RetryableError": int,
        "NonRetryableError": int,
        "Stopped": int,
    },
)

DescribeImageRequestRequestTypeDef = TypedDict(
    "DescribeImageRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)

DescribeImageResponseTypeDef = TypedDict(
    "DescribeImageResponseTypeDef",
    {
        "CreationTime": datetime,
        "Description": str,
        "DisplayName": str,
        "FailureReason": str,
        "ImageArn": str,
        "ImageName": str,
        "ImageStatus": ImageStatusType,
        "LastModifiedTime": datetime,
        "RoleArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeImageVersionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImageVersionRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalDescribeImageVersionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImageVersionRequestRequestTypeDef",
    {
        "Version": int,
        "Alias": str,
    },
    total=False,
)


class DescribeImageVersionRequestRequestTypeDef(
    _RequiredDescribeImageVersionRequestRequestTypeDef,
    _OptionalDescribeImageVersionRequestRequestTypeDef,
):
    pass


DescribeImageVersionResponseTypeDef = TypedDict(
    "DescribeImageVersionResponseTypeDef",
    {
        "BaseImage": str,
        "ContainerImage": str,
        "CreationTime": datetime,
        "FailureReason": str,
        "ImageArn": str,
        "ImageVersionArn": str,
        "ImageVersionStatus": ImageVersionStatusType,
        "LastModifiedTime": datetime,
        "Version": int,
        "VendorGuidance": VendorGuidanceType,
        "JobType": JobTypeType,
        "MLFramework": str,
        "ProgrammingLang": str,
        "Processor": ProcessorType,
        "Horovod": bool,
        "ReleaseNotes": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeInferenceExperimentRequestRequestTypeDef = TypedDict(
    "DescribeInferenceExperimentRequestRequestTypeDef",
    {
        "Name": str,
    },
)

EndpointMetadataTypeDef = TypedDict(
    "EndpointMetadataTypeDef",
    {
        "EndpointName": str,
        "EndpointConfigName": str,
        "EndpointStatus": EndpointStatusType,
        "FailureReason": str,
    },
)

DescribeInferenceRecommendationsJobRequestRequestTypeDef = TypedDict(
    "DescribeInferenceRecommendationsJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
)

DescribeLabelingJobRequestRequestTypeDef = TypedDict(
    "DescribeLabelingJobRequestRequestTypeDef",
    {
        "LabelingJobName": str,
    },
)

LabelCountersTypeDef = TypedDict(
    "LabelCountersTypeDef",
    {
        "TotalLabeled": int,
        "HumanLabeled": int,
        "MachineLabeled": int,
        "FailedNonRetryableError": int,
        "Unlabeled": int,
    },
)

LabelingJobOutputTypeDef = TypedDict(
    "LabelingJobOutputTypeDef",
    {
        "OutputDatasetS3Uri": str,
        "FinalActiveLearningModelArn": str,
    },
)

DescribeLineageGroupRequestRequestTypeDef = TypedDict(
    "DescribeLineageGroupRequestRequestTypeDef",
    {
        "LineageGroupName": str,
    },
)

DescribeModelBiasJobDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeModelBiasJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DescribeModelCardExportJobRequestRequestTypeDef = TypedDict(
    "DescribeModelCardExportJobRequestRequestTypeDef",
    {
        "ModelCardExportJobArn": str,
    },
)

ModelCardExportArtifactsTypeDef = TypedDict(
    "ModelCardExportArtifactsTypeDef",
    {
        "S3ExportArtifacts": str,
    },
)

_RequiredDescribeModelCardRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeModelCardRequestRequestTypeDef",
    {
        "ModelCardName": str,
    },
)
_OptionalDescribeModelCardRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeModelCardRequestRequestTypeDef",
    {
        "ModelCardVersion": int,
    },
    total=False,
)


class DescribeModelCardRequestRequestTypeDef(
    _RequiredDescribeModelCardRequestRequestTypeDef, _OptionalDescribeModelCardRequestRequestTypeDef
):
    pass


DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DescribeModelInputRequestTypeDef = TypedDict(
    "DescribeModelInputRequestTypeDef",
    {
        "ModelName": str,
    },
)

DescribeModelPackageGroupInputRequestTypeDef = TypedDict(
    "DescribeModelPackageGroupInputRequestTypeDef",
    {
        "ModelPackageGroupName": str,
    },
)

DescribeModelPackageInputRequestTypeDef = TypedDict(
    "DescribeModelPackageInputRequestTypeDef",
    {
        "ModelPackageName": str,
    },
)

DescribeModelQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeModelQualityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

DescribeMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "DescribeMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
    },
)

MonitoringExecutionSummaryTypeDef = TypedDict(
    "MonitoringExecutionSummaryTypeDef",
    {
        "MonitoringScheduleName": str,
        "ScheduledTime": datetime,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringExecutionStatus": ExecutionStatusType,
        "ProcessingJobArn": str,
        "EndpointName": str,
        "FailureReason": str,
        "MonitoringJobDefinitionName": str,
        "MonitoringType": MonitoringTypeType,
    },
)

DescribeNotebookInstanceInputRequestTypeDef = TypedDict(
    "DescribeNotebookInstanceInputRequestTypeDef",
    {
        "NotebookInstanceName": str,
    },
)

DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef = TypedDict(
    "DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef",
    {
        "NotebookInstanceLifecycleConfigName": str,
    },
)

DescribePipelineDefinitionForExecutionRequestRequestTypeDef = TypedDict(
    "DescribePipelineDefinitionForExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
    },
)

DescribePipelineDefinitionForExecutionResponseTypeDef = TypedDict(
    "DescribePipelineDefinitionForExecutionResponseTypeDef",
    {
        "PipelineDefinition": str,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePipelineExecutionRequestRequestTypeDef = TypedDict(
    "DescribePipelineExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
    },
)

PipelineExperimentConfigTypeDef = TypedDict(
    "PipelineExperimentConfigTypeDef",
    {
        "ExperimentName": str,
        "TrialName": str,
    },
)

DescribePipelineRequestRequestTypeDef = TypedDict(
    "DescribePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

DescribeProcessingJobRequestRequestTypeDef = TypedDict(
    "DescribeProcessingJobRequestRequestTypeDef",
    {
        "ProcessingJobName": str,
    },
)

DescribeProjectInputRequestTypeDef = TypedDict(
    "DescribeProjectInputRequestTypeDef",
    {
        "ProjectName": str,
    },
)

ServiceCatalogProvisionedProductDetailsTypeDef = TypedDict(
    "ServiceCatalogProvisionedProductDetailsTypeDef",
    {
        "ProvisionedProductId": str,
        "ProvisionedProductStatusMessage": str,
    },
)

DescribeSpaceRequestRequestTypeDef = TypedDict(
    "DescribeSpaceRequestRequestTypeDef",
    {
        "DomainId": str,
        "SpaceName": str,
    },
)

DescribeStudioLifecycleConfigRequestRequestTypeDef = TypedDict(
    "DescribeStudioLifecycleConfigRequestRequestTypeDef",
    {
        "StudioLifecycleConfigName": str,
    },
)

DescribeStudioLifecycleConfigResponseTypeDef = TypedDict(
    "DescribeStudioLifecycleConfigResponseTypeDef",
    {
        "StudioLifecycleConfigArn": str,
        "StudioLifecycleConfigName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "StudioLifecycleConfigContent": str,
        "StudioLifecycleConfigAppType": StudioLifecycleConfigAppTypeType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSubscribedWorkteamRequestRequestTypeDef = TypedDict(
    "DescribeSubscribedWorkteamRequestRequestTypeDef",
    {
        "WorkteamArn": str,
    },
)

SubscribedWorkteamTypeDef = TypedDict(
    "SubscribedWorkteamTypeDef",
    {
        "WorkteamArn": str,
        "MarketplaceTitle": str,
        "SellerName": str,
        "MarketplaceDescription": str,
        "ListingId": str,
    },
)

DescribeTrainingJobRequestRequestTypeDef = TypedDict(
    "DescribeTrainingJobRequestRequestTypeDef",
    {
        "TrainingJobName": str,
    },
)

MetricDataTypeDef = TypedDict(
    "MetricDataTypeDef",
    {
        "MetricName": str,
        "Value": float,
        "Timestamp": datetime,
    },
)

ProfilerRuleEvaluationStatusTypeDef = TypedDict(
    "ProfilerRuleEvaluationStatusTypeDef",
    {
        "RuleConfigurationName": str,
        "RuleEvaluationJobArn": str,
        "RuleEvaluationStatus": RuleEvaluationStatusType,
        "StatusDetails": str,
        "LastModifiedTime": datetime,
    },
)

SecondaryStatusTransitionTypeDef = TypedDict(
    "SecondaryStatusTransitionTypeDef",
    {
        "Status": SecondaryStatusType,
        "StartTime": datetime,
        "EndTime": datetime,
        "StatusMessage": str,
    },
)

WarmPoolStatusTypeDef = TypedDict(
    "WarmPoolStatusTypeDef",
    {
        "Status": WarmPoolResourceStatusType,
        "ResourceRetainedBillableTimeInSeconds": int,
        "ReusedByJob": str,
    },
)

DescribeTransformJobRequestRequestTypeDef = TypedDict(
    "DescribeTransformJobRequestRequestTypeDef",
    {
        "TransformJobName": str,
    },
)

DescribeTrialComponentRequestRequestTypeDef = TypedDict(
    "DescribeTrialComponentRequestRequestTypeDef",
    {
        "TrialComponentName": str,
    },
)

TrialComponentMetricSummaryTypeDef = TypedDict(
    "TrialComponentMetricSummaryTypeDef",
    {
        "MetricName": str,
        "SourceArn": str,
        "TimeStamp": datetime,
        "Max": float,
        "Min": float,
        "Last": float,
        "Count": int,
        "Avg": float,
        "StdDev": float,
    },
)

TrialComponentSourceTypeDef = TypedDict(
    "TrialComponentSourceTypeDef",
    {
        "SourceArn": str,
        "SourceType": str,
    },
)

DescribeTrialRequestRequestTypeDef = TypedDict(
    "DescribeTrialRequestRequestTypeDef",
    {
        "TrialName": str,
    },
)

TrialSourceTypeDef = TypedDict(
    "TrialSourceTypeDef",
    {
        "SourceArn": str,
        "SourceType": str,
    },
)

DescribeUserProfileRequestRequestTypeDef = TypedDict(
    "DescribeUserProfileRequestRequestTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
    },
)

DescribeWorkforceRequestRequestTypeDef = TypedDict(
    "DescribeWorkforceRequestRequestTypeDef",
    {
        "WorkforceName": str,
    },
)

DescribeWorkteamRequestRequestTypeDef = TypedDict(
    "DescribeWorkteamRequestRequestTypeDef",
    {
        "WorkteamName": str,
    },
)

ProductionVariantServerlessUpdateConfigTypeDef = TypedDict(
    "ProductionVariantServerlessUpdateConfigTypeDef",
    {
        "MaxConcurrency": int,
        "ProvisionedConcurrency": int,
    },
    total=False,
)

DeviceDeploymentSummaryTypeDef = TypedDict(
    "DeviceDeploymentSummaryTypeDef",
    {
        "EdgeDeploymentPlanArn": str,
        "EdgeDeploymentPlanName": str,
        "StageName": str,
        "DeployedStageName": str,
        "DeviceFleetName": str,
        "DeviceName": str,
        "DeviceArn": str,
        "DeviceDeploymentStatus": DeviceDeploymentStatusType,
        "DeviceDeploymentStatusMessage": str,
        "Description": str,
        "DeploymentStartTime": datetime,
    },
)

DeviceFleetSummaryTypeDef = TypedDict(
    "DeviceFleetSummaryTypeDef",
    {
        "DeviceFleetArn": str,
        "DeviceFleetName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

DeviceStatsTypeDef = TypedDict(
    "DeviceStatsTypeDef",
    {
        "ConnectedDeviceCount": int,
        "RegisteredDeviceCount": int,
    },
)

EdgeModelSummaryTypeDef = TypedDict(
    "EdgeModelSummaryTypeDef",
    {
        "ModelName": str,
        "ModelVersion": str,
    },
)

_RequiredDeviceTypeDef = TypedDict(
    "_RequiredDeviceTypeDef",
    {
        "DeviceName": str,
    },
)
_OptionalDeviceTypeDef = TypedDict(
    "_OptionalDeviceTypeDef",
    {
        "Description": str,
        "IotThingName": str,
    },
    total=False,
)


class DeviceTypeDef(_RequiredDeviceTypeDef, _OptionalDeviceTypeDef):
    pass


DisassociateTrialComponentRequestRequestTypeDef = TypedDict(
    "DisassociateTrialComponentRequestRequestTypeDef",
    {
        "TrialComponentName": str,
        "TrialName": str,
    },
)

DisassociateTrialComponentResponseTypeDef = TypedDict(
    "DisassociateTrialComponentResponseTypeDef",
    {
        "TrialComponentArn": str,
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DomainDetailsTypeDef = TypedDict(
    "DomainDetailsTypeDef",
    {
        "DomainArn": str,
        "DomainId": str,
        "DomainName": str,
        "Status": DomainStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Url": str,
    },
)

_RequiredFileSourceTypeDef = TypedDict(
    "_RequiredFileSourceTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalFileSourceTypeDef = TypedDict(
    "_OptionalFileSourceTypeDef",
    {
        "ContentType": str,
        "ContentDigest": str,
    },
    total=False,
)


class FileSourceTypeDef(_RequiredFileSourceTypeDef, _OptionalFileSourceTypeDef):
    pass


EMRStepMetadataTypeDef = TypedDict(
    "EMRStepMetadataTypeDef",
    {
        "ClusterId": str,
        "StepId": str,
        "StepName": str,
        "LogFilePath": str,
    },
)

EdgeDeploymentPlanSummaryTypeDef = TypedDict(
    "EdgeDeploymentPlanSummaryTypeDef",
    {
        "EdgeDeploymentPlanArn": str,
        "EdgeDeploymentPlanName": str,
        "DeviceFleetName": str,
        "EdgeDeploymentSuccess": int,
        "EdgeDeploymentPending": int,
        "EdgeDeploymentFailed": int,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

EdgeModelStatTypeDef = TypedDict(
    "EdgeModelStatTypeDef",
    {
        "ModelName": str,
        "ModelVersion": str,
        "OfflineDeviceCount": int,
        "ConnectedDeviceCount": int,
        "ActiveDeviceCount": int,
        "SamplingDeviceCount": int,
    },
)

EdgePackagingJobSummaryTypeDef = TypedDict(
    "EdgePackagingJobSummaryTypeDef",
    {
        "EdgePackagingJobArn": str,
        "EdgePackagingJobName": str,
        "EdgePackagingJobStatus": EdgePackagingJobStatusType,
        "CompilationJobName": str,
        "ModelName": str,
        "ModelVersion": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

EdgeTypeDef = TypedDict(
    "EdgeTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "AssociationType": AssociationEdgeTypeType,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EndpointConfigSummaryTypeDef = TypedDict(
    "EndpointConfigSummaryTypeDef",
    {
        "EndpointConfigName": str,
        "EndpointConfigArn": str,
        "CreationTime": datetime,
    },
)

EndpointInfoTypeDef = TypedDict(
    "EndpointInfoTypeDef",
    {
        "EndpointName": str,
    },
)

_RequiredProductionVariantServerlessConfigTypeDef = TypedDict(
    "_RequiredProductionVariantServerlessConfigTypeDef",
    {
        "MemorySizeInMB": int,
        "MaxConcurrency": int,
    },
)
_OptionalProductionVariantServerlessConfigTypeDef = TypedDict(
    "_OptionalProductionVariantServerlessConfigTypeDef",
    {
        "ProvisionedConcurrency": int,
    },
    total=False,
)


class ProductionVariantServerlessConfigTypeDef(
    _RequiredProductionVariantServerlessConfigTypeDef,
    _OptionalProductionVariantServerlessConfigTypeDef,
):
    pass


InferenceMetricsTypeDef = TypedDict(
    "InferenceMetricsTypeDef",
    {
        "MaxInvocations": int,
        "ModelLatency": int,
    },
)

EndpointSummaryTypeDef = TypedDict(
    "EndpointSummaryTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "EndpointStatus": EndpointStatusType,
    },
)

EnvironmentParameterTypeDef = TypedDict(
    "EnvironmentParameterTypeDef",
    {
        "Key": str,
        "ValueType": str,
        "Value": str,
    },
)

FailStepMetadataTypeDef = TypedDict(
    "FailStepMetadataTypeDef",
    {
        "ErrorMessage": str,
    },
)

FileSystemConfigTypeDef = TypedDict(
    "FileSystemConfigTypeDef",
    {
        "MountPath": str,
        "DefaultUid": int,
        "DefaultGid": int,
    },
    total=False,
)

_RequiredFilterTypeDef = TypedDict(
    "_RequiredFilterTypeDef",
    {
        "Name": str,
    },
)
_OptionalFilterTypeDef = TypedDict(
    "_OptionalFilterTypeDef",
    {
        "Operator": OperatorType,
        "Value": str,
    },
    total=False,
)


class FilterTypeDef(_RequiredFilterTypeDef, _OptionalFilterTypeDef):
    pass


FinalHyperParameterTuningJobObjectiveMetricTypeDef = TypedDict(
    "FinalHyperParameterTuningJobObjectiveMetricTypeDef",
    {
        "Type": HyperParameterTuningJobObjectiveTypeType,
        "MetricName": str,
        "Value": float,
    },
)

FlowDefinitionSummaryTypeDef = TypedDict(
    "FlowDefinitionSummaryTypeDef",
    {
        "FlowDefinitionName": str,
        "FlowDefinitionArn": str,
        "FlowDefinitionStatus": FlowDefinitionStatusType,
        "CreationTime": datetime,
        "FailureReason": str,
    },
)

GetDeviceFleetReportRequestRequestTypeDef = TypedDict(
    "GetDeviceFleetReportRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
    },
)

GetLineageGroupPolicyRequestRequestTypeDef = TypedDict(
    "GetLineageGroupPolicyRequestRequestTypeDef",
    {
        "LineageGroupName": str,
    },
)

GetLineageGroupPolicyResponseTypeDef = TypedDict(
    "GetLineageGroupPolicyResponseTypeDef",
    {
        "LineageGroupArn": str,
        "ResourcePolicy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetModelPackageGroupPolicyInputRequestTypeDef = TypedDict(
    "GetModelPackageGroupPolicyInputRequestTypeDef",
    {
        "ModelPackageGroupName": str,
    },
)

GetModelPackageGroupPolicyOutputTypeDef = TypedDict(
    "GetModelPackageGroupPolicyOutputTypeDef",
    {
        "ResourcePolicy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSagemakerServicecatalogPortfolioStatusOutputTypeDef = TypedDict(
    "GetSagemakerServicecatalogPortfolioStatusOutputTypeDef",
    {
        "Status": SagemakerServicecatalogStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PropertyNameSuggestionTypeDef = TypedDict(
    "PropertyNameSuggestionTypeDef",
    {
        "PropertyName": str,
    },
)

GitConfigForUpdateTypeDef = TypedDict(
    "GitConfigForUpdateTypeDef",
    {
        "SecretArn": str,
    },
    total=False,
)

HubContentInfoTypeDef = TypedDict(
    "HubContentInfoTypeDef",
    {
        "HubContentName": str,
        "HubContentArn": str,
        "HubContentVersion": str,
        "HubContentType": HubContentTypeType,
        "DocumentSchemaVersion": str,
        "HubContentDisplayName": str,
        "HubContentDescription": str,
        "HubContentSearchKeywords": List[str],
        "HubContentStatus": HubContentStatusType,
        "CreationTime": datetime,
    },
)

HubInfoTypeDef = TypedDict(
    "HubInfoTypeDef",
    {
        "HubName": str,
        "HubArn": str,
        "HubDisplayName": str,
        "HubDescription": str,
        "HubSearchKeywords": List[str],
        "HubStatus": HubStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

HumanLoopActivationConditionsConfigTypeDef = TypedDict(
    "HumanLoopActivationConditionsConfigTypeDef",
    {
        "HumanLoopActivationConditions": str,
    },
)

UiConfigTypeDef = TypedDict(
    "UiConfigTypeDef",
    {
        "UiTemplateS3Uri": str,
        "HumanTaskUiArn": str,
    },
    total=False,
)

HumanTaskUiSummaryTypeDef = TypedDict(
    "HumanTaskUiSummaryTypeDef",
    {
        "HumanTaskUiName": str,
        "HumanTaskUiArn": str,
        "CreationTime": datetime,
    },
)

HyperParameterTuningJobObjectiveTypeDef = TypedDict(
    "HyperParameterTuningJobObjectiveTypeDef",
    {
        "Type": HyperParameterTuningJobObjectiveTypeType,
        "MetricName": str,
    },
)

HyperParameterTuningInstanceConfigTypeDef = TypedDict(
    "HyperParameterTuningInstanceConfigTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "VolumeSizeInGB": int,
    },
)

_RequiredResourceLimitsTypeDef = TypedDict(
    "_RequiredResourceLimitsTypeDef",
    {
        "MaxParallelTrainingJobs": int,
    },
)
_OptionalResourceLimitsTypeDef = TypedDict(
    "_OptionalResourceLimitsTypeDef",
    {
        "MaxNumberOfTrainingJobs": int,
        "MaxRuntimeInSeconds": int,
    },
    total=False,
)


class ResourceLimitsTypeDef(_RequiredResourceLimitsTypeDef, _OptionalResourceLimitsTypeDef):
    pass


HyperbandStrategyConfigTypeDef = TypedDict(
    "HyperbandStrategyConfigTypeDef",
    {
        "MinResource": int,
        "MaxResource": int,
    },
    total=False,
)

ParentHyperParameterTuningJobTypeDef = TypedDict(
    "ParentHyperParameterTuningJobTypeDef",
    {
        "HyperParameterTuningJobName": str,
    },
    total=False,
)

IamIdentityTypeDef = TypedDict(
    "IamIdentityTypeDef",
    {
        "Arn": str,
        "PrincipalId": str,
        "SourceIdentity": str,
    },
)

RepositoryAuthConfigTypeDef = TypedDict(
    "RepositoryAuthConfigTypeDef",
    {
        "RepositoryCredentialsProviderArn": str,
    },
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "CreationTime": datetime,
        "Description": str,
        "DisplayName": str,
        "FailureReason": str,
        "ImageArn": str,
        "ImageName": str,
        "ImageStatus": ImageStatusType,
        "LastModifiedTime": datetime,
    },
)

ImageVersionTypeDef = TypedDict(
    "ImageVersionTypeDef",
    {
        "CreationTime": datetime,
        "FailureReason": str,
        "ImageArn": str,
        "ImageVersionArn": str,
        "ImageVersionStatus": ImageVersionStatusType,
        "LastModifiedTime": datetime,
        "Version": int,
    },
)

ImportHubContentResponseTypeDef = TypedDict(
    "ImportHubContentResponseTypeDef",
    {
        "HubArn": str,
        "HubContentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommendationMetricsTypeDef = TypedDict(
    "RecommendationMetricsTypeDef",
    {
        "CostPerHour": float,
        "CostPerInference": float,
        "MaxInvocations": int,
        "ModelLatency": int,
        "CpuUtilization": float,
        "MemoryUtilization": float,
        "ModelSetupTime": int,
    },
)

InferenceRecommendationsJobTypeDef = TypedDict(
    "InferenceRecommendationsJobTypeDef",
    {
        "JobName": str,
        "JobDescription": str,
        "JobType": RecommendationJobTypeType,
        "JobArn": str,
        "Status": RecommendationJobStatusType,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "RoleArn": str,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "ModelName": str,
        "SamplePayloadUrl": str,
        "ModelPackageVersionArn": str,
    },
)

InstanceGroupTypeDef = TypedDict(
    "InstanceGroupTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "InstanceGroupName": str,
    },
)

IntegerParameterRangeSpecificationTypeDef = TypedDict(
    "IntegerParameterRangeSpecificationTypeDef",
    {
        "MinValue": str,
        "MaxValue": str,
    },
)

_RequiredIntegerParameterRangeTypeDef = TypedDict(
    "_RequiredIntegerParameterRangeTypeDef",
    {
        "Name": str,
        "MinValue": str,
        "MaxValue": str,
    },
)
_OptionalIntegerParameterRangeTypeDef = TypedDict(
    "_OptionalIntegerParameterRangeTypeDef",
    {
        "ScalingType": HyperParameterScalingTypeType,
    },
    total=False,
)


class IntegerParameterRangeTypeDef(
    _RequiredIntegerParameterRangeTypeDef, _OptionalIntegerParameterRangeTypeDef
):
    pass


_RequiredKernelSpecTypeDef = TypedDict(
    "_RequiredKernelSpecTypeDef",
    {
        "Name": str,
    },
)
_OptionalKernelSpecTypeDef = TypedDict(
    "_OptionalKernelSpecTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)


class KernelSpecTypeDef(_RequiredKernelSpecTypeDef, _OptionalKernelSpecTypeDef):
    pass


LabelCountersForWorkteamTypeDef = TypedDict(
    "LabelCountersForWorkteamTypeDef",
    {
        "HumanLabeled": int,
        "PendingHuman": int,
        "Total": int,
    },
)

LabelingJobDataAttributesTypeDef = TypedDict(
    "LabelingJobDataAttributesTypeDef",
    {
        "ContentClassifiers": Sequence[ContentClassifierType],
    },
    total=False,
)

LabelingJobS3DataSourceTypeDef = TypedDict(
    "LabelingJobS3DataSourceTypeDef",
    {
        "ManifestS3Uri": str,
    },
)

LabelingJobSnsDataSourceTypeDef = TypedDict(
    "LabelingJobSnsDataSourceTypeDef",
    {
        "SnsTopicArn": str,
    },
)

LineageGroupSummaryTypeDef = TypedDict(
    "LineageGroupSummaryTypeDef",
    {
        "LineageGroupArn": str,
        "LineageGroupName": str,
        "DisplayName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

ListActionsRequestListActionsPaginateTypeDef = TypedDict(
    "ListActionsRequestListActionsPaginateTypeDef",
    {
        "SourceUri": str,
        "ActionType": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortActionsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListActionsRequestRequestTypeDef = TypedDict(
    "ListActionsRequestRequestTypeDef",
    {
        "SourceUri": str,
        "ActionType": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortActionsByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListAlgorithmsInputListAlgorithmsPaginateTypeDef = TypedDict(
    "ListAlgorithmsInputListAlgorithmsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "NameContains": str,
        "SortBy": AlgorithmSortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAlgorithmsInputRequestTypeDef = TypedDict(
    "ListAlgorithmsInputRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NameContains": str,
        "NextToken": str,
        "SortBy": AlgorithmSortByType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

_RequiredListAliasesRequestListAliasesPaginateTypeDef = TypedDict(
    "_RequiredListAliasesRequestListAliasesPaginateTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalListAliasesRequestListAliasesPaginateTypeDef = TypedDict(
    "_OptionalListAliasesRequestListAliasesPaginateTypeDef",
    {
        "Alias": str,
        "Version": int,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListAliasesRequestListAliasesPaginateTypeDef(
    _RequiredListAliasesRequestListAliasesPaginateTypeDef,
    _OptionalListAliasesRequestListAliasesPaginateTypeDef,
):
    pass


_RequiredListAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListAliasesRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalListAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListAliasesRequestRequestTypeDef",
    {
        "Alias": str,
        "Version": int,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAliasesRequestRequestTypeDef(
    _RequiredListAliasesRequestRequestTypeDef, _OptionalListAliasesRequestRequestTypeDef
):
    pass


ListAliasesResponseTypeDef = TypedDict(
    "ListAliasesResponseTypeDef",
    {
        "SageMakerImageVersionAliases": List[str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef = TypedDict(
    "ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef",
    {
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "ModifiedTimeBefore": Union[datetime, str],
        "ModifiedTimeAfter": Union[datetime, str],
        "SortBy": AppImageConfigSortKeyType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAppImageConfigsRequestRequestTypeDef = TypedDict(
    "ListAppImageConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "ModifiedTimeBefore": Union[datetime, str],
        "ModifiedTimeAfter": Union[datetime, str],
        "SortBy": AppImageConfigSortKeyType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListAppsRequestListAppsPaginateTypeDef = TypedDict(
    "ListAppsRequestListAppsPaginateTypeDef",
    {
        "SortOrder": SortOrderType,
        "SortBy": Literal["CreationTime"],
        "DomainIdEquals": str,
        "UserProfileNameEquals": str,
        "SpaceNameEquals": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAppsRequestRequestTypeDef = TypedDict(
    "ListAppsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SortOrder": SortOrderType,
        "SortBy": Literal["CreationTime"],
        "DomainIdEquals": str,
        "UserProfileNameEquals": str,
        "SpaceNameEquals": str,
    },
    total=False,
)

ListArtifactsRequestListArtifactsPaginateTypeDef = TypedDict(
    "ListArtifactsRequestListArtifactsPaginateTypeDef",
    {
        "SourceUri": str,
        "ArtifactType": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": Literal["CreationTime"],
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListArtifactsRequestRequestTypeDef = TypedDict(
    "ListArtifactsRequestRequestTypeDef",
    {
        "SourceUri": str,
        "ArtifactType": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": Literal["CreationTime"],
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListAssociationsRequestListAssociationsPaginateTypeDef = TypedDict(
    "ListAssociationsRequestListAssociationsPaginateTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "SourceType": str,
        "DestinationType": str,
        "AssociationType": AssociationEdgeTypeType,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortAssociationsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAssociationsRequestRequestTypeDef = TypedDict(
    "ListAssociationsRequestRequestTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "SourceType": str,
        "DestinationType": str,
        "AssociationType": AssociationEdgeTypeType,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortAssociationsByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef = TypedDict(
    "ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": AutoMLJobStatusType,
        "SortOrder": AutoMLSortOrderType,
        "SortBy": AutoMLSortByType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAutoMLJobsRequestRequestTypeDef = TypedDict(
    "ListAutoMLJobsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": AutoMLJobStatusType,
        "SortOrder": AutoMLSortOrderType,
        "SortBy": AutoMLSortByType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef = TypedDict(
    "_RequiredListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef",
    {
        "AutoMLJobName": str,
    },
)
_OptionalListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef = TypedDict(
    "_OptionalListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef",
    {
        "StatusEquals": CandidateStatusType,
        "CandidateNameEquals": str,
        "SortOrder": AutoMLSortOrderType,
        "SortBy": CandidateSortByType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef(
    _RequiredListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef,
    _OptionalListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef,
):
    pass


_RequiredListCandidatesForAutoMLJobRequestRequestTypeDef = TypedDict(
    "_RequiredListCandidatesForAutoMLJobRequestRequestTypeDef",
    {
        "AutoMLJobName": str,
    },
)
_OptionalListCandidatesForAutoMLJobRequestRequestTypeDef = TypedDict(
    "_OptionalListCandidatesForAutoMLJobRequestRequestTypeDef",
    {
        "StatusEquals": CandidateStatusType,
        "CandidateNameEquals": str,
        "SortOrder": AutoMLSortOrderType,
        "SortBy": CandidateSortByType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListCandidatesForAutoMLJobRequestRequestTypeDef(
    _RequiredListCandidatesForAutoMLJobRequestRequestTypeDef,
    _OptionalListCandidatesForAutoMLJobRequestRequestTypeDef,
):
    pass


ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef = TypedDict(
    "ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "SortBy": CodeRepositorySortByType,
        "SortOrder": CodeRepositorySortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCodeRepositoriesInputRequestTypeDef = TypedDict(
    "ListCodeRepositoriesInputRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NameContains": str,
        "NextToken": str,
        "SortBy": CodeRepositorySortByType,
        "SortOrder": CodeRepositorySortOrderType,
    },
    total=False,
)

ListCompilationJobsRequestListCompilationJobsPaginateTypeDef = TypedDict(
    "ListCompilationJobsRequestListCompilationJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": CompilationJobStatusType,
        "SortBy": ListCompilationJobsSortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCompilationJobsRequestRequestTypeDef = TypedDict(
    "ListCompilationJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": CompilationJobStatusType,
        "SortBy": ListCompilationJobsSortByType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListContextsRequestListContextsPaginateTypeDef = TypedDict(
    "ListContextsRequestListContextsPaginateTypeDef",
    {
        "SourceUri": str,
        "ContextType": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortContextsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListContextsRequestRequestTypeDef = TypedDict(
    "ListContextsRequestRequestTypeDef",
    {
        "SourceUri": str,
        "ContextType": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortContextsByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef = TypedDict(
    "ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDataQualityJobDefinitionsRequestRequestTypeDef = TypedDict(
    "ListDataQualityJobDefinitionsRequestRequestTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
    },
    total=False,
)

MonitoringJobDefinitionSummaryTypeDef = TypedDict(
    "MonitoringJobDefinitionSummaryTypeDef",
    {
        "MonitoringJobDefinitionName": str,
        "MonitoringJobDefinitionArn": str,
        "CreationTime": datetime,
        "EndpointName": str,
    },
)

ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef = TypedDict(
    "ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "SortBy": ListDeviceFleetsSortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDeviceFleetsRequestRequestTypeDef = TypedDict(
    "ListDeviceFleetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "SortBy": ListDeviceFleetsSortByType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListDevicesRequestListDevicesPaginateTypeDef = TypedDict(
    "ListDevicesRequestListDevicesPaginateTypeDef",
    {
        "LatestHeartbeatAfter": Union[datetime, str],
        "ModelName": str,
        "DeviceFleetName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDevicesRequestRequestTypeDef = TypedDict(
    "ListDevicesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "LatestHeartbeatAfter": Union[datetime, str],
        "ModelName": str,
        "DeviceFleetName": str,
    },
    total=False,
)

ListDomainsRequestListDomainsPaginateTypeDef = TypedDict(
    "ListDomainsRequestListDomainsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDomainsRequestRequestTypeDef = TypedDict(
    "ListDomainsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef = TypedDict(
    "ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "DeviceFleetNameContains": str,
        "SortBy": ListEdgeDeploymentPlansSortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEdgeDeploymentPlansRequestRequestTypeDef = TypedDict(
    "ListEdgeDeploymentPlansRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "DeviceFleetNameContains": str,
        "SortBy": ListEdgeDeploymentPlansSortByType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef = TypedDict(
    "ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "ModelNameContains": str,
        "StatusEquals": EdgePackagingJobStatusType,
        "SortBy": ListEdgePackagingJobsSortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEdgePackagingJobsRequestRequestTypeDef = TypedDict(
    "ListEdgePackagingJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "ModelNameContains": str,
        "StatusEquals": EdgePackagingJobStatusType,
        "SortBy": ListEdgePackagingJobsSortByType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef = TypedDict(
    "ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef",
    {
        "SortBy": EndpointConfigSortKeyType,
        "SortOrder": OrderKeyType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEndpointConfigsInputRequestTypeDef = TypedDict(
    "ListEndpointConfigsInputRequestTypeDef",
    {
        "SortBy": EndpointConfigSortKeyType,
        "SortOrder": OrderKeyType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
    },
    total=False,
)

ListEndpointsInputListEndpointsPaginateTypeDef = TypedDict(
    "ListEndpointsInputListEndpointsPaginateTypeDef",
    {
        "SortBy": EndpointSortKeyType,
        "SortOrder": OrderKeyType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": EndpointStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEndpointsInputRequestTypeDef = TypedDict(
    "ListEndpointsInputRequestTypeDef",
    {
        "SortBy": EndpointSortKeyType,
        "SortOrder": OrderKeyType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": EndpointStatusType,
    },
    total=False,
)

ListExperimentsRequestListExperimentsPaginateTypeDef = TypedDict(
    "ListExperimentsRequestListExperimentsPaginateTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortExperimentsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListExperimentsRequestRequestTypeDef = TypedDict(
    "ListExperimentsRequestRequestTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortExperimentsByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef = TypedDict(
    "ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef",
    {
        "NameContains": str,
        "FeatureGroupStatusEquals": FeatureGroupStatusType,
        "OfflineStoreStatusEquals": OfflineStoreStatusValueType,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": FeatureGroupSortOrderType,
        "SortBy": FeatureGroupSortByType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFeatureGroupsRequestRequestTypeDef = TypedDict(
    "ListFeatureGroupsRequestRequestTypeDef",
    {
        "NameContains": str,
        "FeatureGroupStatusEquals": FeatureGroupStatusType,
        "OfflineStoreStatusEquals": OfflineStoreStatusValueType,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": FeatureGroupSortOrderType,
        "SortBy": FeatureGroupSortByType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef = TypedDict(
    "ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFlowDefinitionsRequestRequestTypeDef = TypedDict(
    "ListFlowDefinitionsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListHubContentVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListHubContentVersionsRequestRequestTypeDef",
    {
        "HubName": str,
        "HubContentType": HubContentTypeType,
        "HubContentName": str,
    },
)
_OptionalListHubContentVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListHubContentVersionsRequestRequestTypeDef",
    {
        "MinVersion": str,
        "MaxSchemaVersion": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "SortBy": HubContentSortByType,
        "SortOrder": SortOrderType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListHubContentVersionsRequestRequestTypeDef(
    _RequiredListHubContentVersionsRequestRequestTypeDef,
    _OptionalListHubContentVersionsRequestRequestTypeDef,
):
    pass


_RequiredListHubContentsRequestRequestTypeDef = TypedDict(
    "_RequiredListHubContentsRequestRequestTypeDef",
    {
        "HubName": str,
        "HubContentType": HubContentTypeType,
    },
)
_OptionalListHubContentsRequestRequestTypeDef = TypedDict(
    "_OptionalListHubContentsRequestRequestTypeDef",
    {
        "NameContains": str,
        "MaxSchemaVersion": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "SortBy": HubContentSortByType,
        "SortOrder": SortOrderType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListHubContentsRequestRequestTypeDef(
    _RequiredListHubContentsRequestRequestTypeDef, _OptionalListHubContentsRequestRequestTypeDef
):
    pass


ListHubsRequestRequestTypeDef = TypedDict(
    "ListHubsRequestRequestTypeDef",
    {
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "SortBy": HubSortByType,
        "SortOrder": SortOrderType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef = TypedDict(
    "ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListHumanTaskUisRequestRequestTypeDef = TypedDict(
    "ListHumanTaskUisRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef = TypedDict(
    "ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef",
    {
        "SortBy": HyperParameterTuningJobSortByOptionsType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "StatusEquals": HyperParameterTuningJobStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListHyperParameterTuningJobsRequestRequestTypeDef = TypedDict(
    "ListHyperParameterTuningJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SortBy": HyperParameterTuningJobSortByOptionsType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "StatusEquals": HyperParameterTuningJobStatusType,
    },
    total=False,
)

_RequiredListImageVersionsRequestListImageVersionsPaginateTypeDef = TypedDict(
    "_RequiredListImageVersionsRequestListImageVersionsPaginateTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalListImageVersionsRequestListImageVersionsPaginateTypeDef = TypedDict(
    "_OptionalListImageVersionsRequestListImageVersionsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "SortBy": ImageVersionSortByType,
        "SortOrder": ImageVersionSortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListImageVersionsRequestListImageVersionsPaginateTypeDef(
    _RequiredListImageVersionsRequestListImageVersionsPaginateTypeDef,
    _OptionalListImageVersionsRequestListImageVersionsPaginateTypeDef,
):
    pass


_RequiredListImageVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListImageVersionsRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalListImageVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListImageVersionsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NextToken": str,
        "SortBy": ImageVersionSortByType,
        "SortOrder": ImageVersionSortOrderType,
    },
    total=False,
)


class ListImageVersionsRequestRequestTypeDef(
    _RequiredListImageVersionsRequestRequestTypeDef, _OptionalListImageVersionsRequestRequestTypeDef
):
    pass


ListImagesRequestListImagesPaginateTypeDef = TypedDict(
    "ListImagesRequestListImagesPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "SortBy": ImageSortByType,
        "SortOrder": ImageSortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListImagesRequestRequestTypeDef = TypedDict(
    "ListImagesRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NameContains": str,
        "NextToken": str,
        "SortBy": ImageSortByType,
        "SortOrder": ImageSortOrderType,
    },
    total=False,
)

ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef = TypedDict(
    "ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef",
    {
        "NameContains": str,
        "Type": Literal["ShadowMode"],
        "StatusEquals": InferenceExperimentStatusType,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "SortBy": SortInferenceExperimentsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListInferenceExperimentsRequestRequestTypeDef = TypedDict(
    "ListInferenceExperimentsRequestRequestTypeDef",
    {
        "NameContains": str,
        "Type": Literal["ShadowMode"],
        "StatusEquals": InferenceExperimentStatusType,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "SortBy": SortInferenceExperimentsByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef = TypedDict(
    "_RequiredListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef",
    {
        "JobName": str,
    },
)
_OptionalListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef = TypedDict(
    "_OptionalListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef",
    {
        "Status": RecommendationJobStatusType,
        "StepType": Literal["BENCHMARK"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef(
    _RequiredListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef,
    _OptionalListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef,
):
    pass


_RequiredListInferenceRecommendationsJobStepsRequestRequestTypeDef = TypedDict(
    "_RequiredListInferenceRecommendationsJobStepsRequestRequestTypeDef",
    {
        "JobName": str,
    },
)
_OptionalListInferenceRecommendationsJobStepsRequestRequestTypeDef = TypedDict(
    "_OptionalListInferenceRecommendationsJobStepsRequestRequestTypeDef",
    {
        "Status": RecommendationJobStatusType,
        "StepType": Literal["BENCHMARK"],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListInferenceRecommendationsJobStepsRequestRequestTypeDef(
    _RequiredListInferenceRecommendationsJobStepsRequestRequestTypeDef,
    _OptionalListInferenceRecommendationsJobStepsRequestRequestTypeDef,
):
    pass


ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef = TypedDict(
    "ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": RecommendationJobStatusType,
        "SortBy": ListInferenceRecommendationsJobsSortByType,
        "SortOrder": SortOrderType,
        "ModelNameEquals": str,
        "ModelPackageVersionArnEquals": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListInferenceRecommendationsJobsRequestRequestTypeDef = TypedDict(
    "ListInferenceRecommendationsJobsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": RecommendationJobStatusType,
        "SortBy": ListInferenceRecommendationsJobsSortByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "ModelNameEquals": str,
        "ModelPackageVersionArnEquals": str,
    },
    total=False,
)

_RequiredListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef = TypedDict(
    "_RequiredListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef",
    {
        "WorkteamArn": str,
    },
)
_OptionalListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef = TypedDict(
    "_OptionalListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "JobReferenceCodeContains": str,
        "SortBy": Literal["CreationTime"],
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef(
    _RequiredListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef,
    _OptionalListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef,
):
    pass


_RequiredListLabelingJobsForWorkteamRequestRequestTypeDef = TypedDict(
    "_RequiredListLabelingJobsForWorkteamRequestRequestTypeDef",
    {
        "WorkteamArn": str,
    },
)
_OptionalListLabelingJobsForWorkteamRequestRequestTypeDef = TypedDict(
    "_OptionalListLabelingJobsForWorkteamRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "JobReferenceCodeContains": str,
        "SortBy": Literal["CreationTime"],
        "SortOrder": SortOrderType,
    },
    total=False,
)


class ListLabelingJobsForWorkteamRequestRequestTypeDef(
    _RequiredListLabelingJobsForWorkteamRequestRequestTypeDef,
    _OptionalListLabelingJobsForWorkteamRequestRequestTypeDef,
):
    pass


ListLabelingJobsRequestListLabelingJobsPaginateTypeDef = TypedDict(
    "ListLabelingJobsRequestListLabelingJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "StatusEquals": LabelingJobStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListLabelingJobsRequestRequestTypeDef = TypedDict(
    "ListLabelingJobsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NextToken": str,
        "NameContains": str,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "StatusEquals": LabelingJobStatusType,
    },
    total=False,
)

ListLineageGroupsRequestListLineageGroupsPaginateTypeDef = TypedDict(
    "ListLineageGroupsRequestListLineageGroupsPaginateTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortLineageGroupsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListLineageGroupsRequestRequestTypeDef = TypedDict(
    "ListLineageGroupsRequestRequestTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortLineageGroupsByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef = TypedDict(
    "ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelBiasJobDefinitionsRequestRequestTypeDef = TypedDict(
    "ListModelBiasJobDefinitionsRequestRequestTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
    },
    total=False,
)

_RequiredListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef = TypedDict(
    "_RequiredListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef",
    {
        "ModelCardName": str,
    },
)
_OptionalListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef = TypedDict(
    "_OptionalListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef",
    {
        "ModelCardVersion": int,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "ModelCardExportJobNameContains": str,
        "StatusEquals": ModelCardExportJobStatusType,
        "SortBy": ModelCardExportJobSortByType,
        "SortOrder": ModelCardExportJobSortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef(
    _RequiredListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef,
    _OptionalListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef,
):
    pass


_RequiredListModelCardExportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListModelCardExportJobsRequestRequestTypeDef",
    {
        "ModelCardName": str,
    },
)
_OptionalListModelCardExportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListModelCardExportJobsRequestRequestTypeDef",
    {
        "ModelCardVersion": int,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "ModelCardExportJobNameContains": str,
        "StatusEquals": ModelCardExportJobStatusType,
        "SortBy": ModelCardExportJobSortByType,
        "SortOrder": ModelCardExportJobSortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListModelCardExportJobsRequestRequestTypeDef(
    _RequiredListModelCardExportJobsRequestRequestTypeDef,
    _OptionalListModelCardExportJobsRequestRequestTypeDef,
):
    pass


ModelCardExportJobSummaryTypeDef = TypedDict(
    "ModelCardExportJobSummaryTypeDef",
    {
        "ModelCardExportJobName": str,
        "ModelCardExportJobArn": str,
        "Status": ModelCardExportJobStatusType,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "CreatedAt": datetime,
        "LastModifiedAt": datetime,
    },
)

_RequiredListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef = TypedDict(
    "_RequiredListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef",
    {
        "ModelCardName": str,
    },
)
_OptionalListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef = TypedDict(
    "_OptionalListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "ModelCardStatus": ModelCardStatusType,
        "SortBy": Literal["Version"],
        "SortOrder": ModelCardSortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef(
    _RequiredListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef,
    _OptionalListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef,
):
    pass


_RequiredListModelCardVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListModelCardVersionsRequestRequestTypeDef",
    {
        "ModelCardName": str,
    },
)
_OptionalListModelCardVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListModelCardVersionsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "ModelCardStatus": ModelCardStatusType,
        "NextToken": str,
        "SortBy": Literal["Version"],
        "SortOrder": ModelCardSortOrderType,
    },
    total=False,
)


class ListModelCardVersionsRequestRequestTypeDef(
    _RequiredListModelCardVersionsRequestRequestTypeDef,
    _OptionalListModelCardVersionsRequestRequestTypeDef,
):
    pass


ModelCardVersionSummaryTypeDef = TypedDict(
    "ModelCardVersionSummaryTypeDef",
    {
        "ModelCardName": str,
        "ModelCardArn": str,
        "ModelCardStatus": ModelCardStatusType,
        "ModelCardVersion": int,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

ListModelCardsRequestListModelCardsPaginateTypeDef = TypedDict(
    "ListModelCardsRequestListModelCardsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "NameContains": str,
        "ModelCardStatus": ModelCardStatusType,
        "SortBy": ModelCardSortByType,
        "SortOrder": ModelCardSortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelCardsRequestRequestTypeDef = TypedDict(
    "ListModelCardsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NameContains": str,
        "ModelCardStatus": ModelCardStatusType,
        "NextToken": str,
        "SortBy": ModelCardSortByType,
        "SortOrder": ModelCardSortOrderType,
    },
    total=False,
)

ModelCardSummaryTypeDef = TypedDict(
    "ModelCardSummaryTypeDef",
    {
        "ModelCardName": str,
        "ModelCardArn": str,
        "ModelCardStatus": ModelCardStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef = TypedDict(
    "ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelExplainabilityJobDefinitionsRequestRequestTypeDef = TypedDict(
    "ListModelExplainabilityJobDefinitionsRequestRequestTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
    },
    total=False,
)

ModelMetadataSummaryTypeDef = TypedDict(
    "ModelMetadataSummaryTypeDef",
    {
        "Domain": str,
        "Framework": str,
        "Task": str,
        "Model": str,
        "FrameworkVersion": str,
    },
)

ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef = TypedDict(
    "ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "NameContains": str,
        "SortBy": ModelPackageGroupSortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelPackageGroupsInputRequestTypeDef = TypedDict(
    "ListModelPackageGroupsInputRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NameContains": str,
        "NextToken": str,
        "SortBy": ModelPackageGroupSortByType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ModelPackageGroupSummaryTypeDef = TypedDict(
    "ModelPackageGroupSummaryTypeDef",
    {
        "ModelPackageGroupName": str,
        "ModelPackageGroupArn": str,
        "ModelPackageGroupDescription": str,
        "CreationTime": datetime,
        "ModelPackageGroupStatus": ModelPackageGroupStatusType,
    },
)

ListModelPackagesInputListModelPackagesPaginateTypeDef = TypedDict(
    "ListModelPackagesInputListModelPackagesPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "NameContains": str,
        "ModelApprovalStatus": ModelApprovalStatusType,
        "ModelPackageGroupName": str,
        "ModelPackageType": ModelPackageTypeType,
        "SortBy": ModelPackageSortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelPackagesInputRequestTypeDef = TypedDict(
    "ListModelPackagesInputRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NameContains": str,
        "ModelApprovalStatus": ModelApprovalStatusType,
        "ModelPackageGroupName": str,
        "ModelPackageType": ModelPackageTypeType,
        "NextToken": str,
        "SortBy": ModelPackageSortByType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ModelPackageSummaryTypeDef = TypedDict(
    "ModelPackageSummaryTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageGroupName": str,
        "ModelPackageVersion": int,
        "ModelPackageArn": str,
        "ModelPackageDescription": str,
        "CreationTime": datetime,
        "ModelPackageStatus": ModelPackageStatusType,
        "ModelApprovalStatus": ModelApprovalStatusType,
    },
)

ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef = TypedDict(
    "ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelQualityJobDefinitionsRequestRequestTypeDef = TypedDict(
    "ListModelQualityJobDefinitionsRequestRequestTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringJobDefinitionSortKeyType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
    },
    total=False,
)

ListModelsInputListModelsPaginateTypeDef = TypedDict(
    "ListModelsInputListModelsPaginateTypeDef",
    {
        "SortBy": ModelSortKeyType,
        "SortOrder": OrderKeyType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelsInputRequestTypeDef = TypedDict(
    "ListModelsInputRequestTypeDef",
    {
        "SortBy": ModelSortKeyType,
        "SortOrder": OrderKeyType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
    },
    total=False,
)

ModelSummaryTypeDef = TypedDict(
    "ModelSummaryTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "CreationTime": datetime,
    },
)

ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef = TypedDict(
    "ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringAlertName": str,
        "SortBy": MonitoringAlertHistorySortKeyType,
        "SortOrder": SortOrderType,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "StatusEquals": MonitoringAlertStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMonitoringAlertHistoryRequestRequestTypeDef = TypedDict(
    "ListMonitoringAlertHistoryRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringAlertName": str,
        "SortBy": MonitoringAlertHistorySortKeyType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "StatusEquals": MonitoringAlertStatusType,
    },
    total=False,
)

MonitoringAlertHistorySummaryTypeDef = TypedDict(
    "MonitoringAlertHistorySummaryTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringAlertName": str,
        "CreationTime": datetime,
        "AlertStatus": MonitoringAlertStatusType,
    },
)

_RequiredListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef = TypedDict(
    "_RequiredListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef",
    {
        "MonitoringScheduleName": str,
    },
)
_OptionalListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef = TypedDict(
    "_OptionalListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef(
    _RequiredListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef,
    _OptionalListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef,
):
    pass


_RequiredListMonitoringAlertsRequestRequestTypeDef = TypedDict(
    "_RequiredListMonitoringAlertsRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
    },
)
_OptionalListMonitoringAlertsRequestRequestTypeDef = TypedDict(
    "_OptionalListMonitoringAlertsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListMonitoringAlertsRequestRequestTypeDef(
    _RequiredListMonitoringAlertsRequestRequestTypeDef,
    _OptionalListMonitoringAlertsRequestRequestTypeDef,
):
    pass


ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef = TypedDict(
    "ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef",
    {
        "MonitoringScheduleName": str,
        "EndpointName": str,
        "SortBy": MonitoringExecutionSortKeyType,
        "SortOrder": SortOrderType,
        "ScheduledTimeBefore": Union[datetime, str],
        "ScheduledTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": ExecutionStatusType,
        "MonitoringJobDefinitionName": str,
        "MonitoringTypeEquals": MonitoringTypeType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMonitoringExecutionsRequestRequestTypeDef = TypedDict(
    "ListMonitoringExecutionsRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
        "EndpointName": str,
        "SortBy": MonitoringExecutionSortKeyType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "ScheduledTimeBefore": Union[datetime, str],
        "ScheduledTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": ExecutionStatusType,
        "MonitoringJobDefinitionName": str,
        "MonitoringTypeEquals": MonitoringTypeType,
    },
    total=False,
)

ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef = TypedDict(
    "ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringScheduleSortKeyType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": ScheduleStatusType,
        "MonitoringJobDefinitionName": str,
        "MonitoringTypeEquals": MonitoringTypeType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMonitoringSchedulesRequestRequestTypeDef = TypedDict(
    "ListMonitoringSchedulesRequestRequestTypeDef",
    {
        "EndpointName": str,
        "SortBy": MonitoringScheduleSortKeyType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": ScheduleStatusType,
        "MonitoringJobDefinitionName": str,
        "MonitoringTypeEquals": MonitoringTypeType,
    },
    total=False,
)

MonitoringScheduleSummaryTypeDef = TypedDict(
    "MonitoringScheduleSummaryTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringScheduleArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleStatus": ScheduleStatusType,
        "EndpointName": str,
        "MonitoringJobDefinitionName": str,
        "MonitoringType": MonitoringTypeType,
    },
)

ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef = TypedDict(
    "ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef",
    {
        "SortBy": NotebookInstanceLifecycleConfigSortKeyType,
        "SortOrder": NotebookInstanceLifecycleConfigSortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListNotebookInstanceLifecycleConfigsInputRequestTypeDef = TypedDict(
    "ListNotebookInstanceLifecycleConfigsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SortBy": NotebookInstanceLifecycleConfigSortKeyType,
        "SortOrder": NotebookInstanceLifecycleConfigSortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
    },
    total=False,
)

NotebookInstanceLifecycleConfigSummaryTypeDef = TypedDict(
    "NotebookInstanceLifecycleConfigSummaryTypeDef",
    {
        "NotebookInstanceLifecycleConfigName": str,
        "NotebookInstanceLifecycleConfigArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef = TypedDict(
    "ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef",
    {
        "SortBy": NotebookInstanceSortKeyType,
        "SortOrder": NotebookInstanceSortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": NotebookInstanceStatusType,
        "NotebookInstanceLifecycleConfigNameContains": str,
        "DefaultCodeRepositoryContains": str,
        "AdditionalCodeRepositoryEquals": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListNotebookInstancesInputRequestTypeDef = TypedDict(
    "ListNotebookInstancesInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SortBy": NotebookInstanceSortKeyType,
        "SortOrder": NotebookInstanceSortOrderType,
        "NameContains": str,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "StatusEquals": NotebookInstanceStatusType,
        "NotebookInstanceLifecycleConfigNameContains": str,
        "DefaultCodeRepositoryContains": str,
        "AdditionalCodeRepositoryEquals": str,
    },
    total=False,
)

NotebookInstanceSummaryTypeDef = TypedDict(
    "NotebookInstanceSummaryTypeDef",
    {
        "NotebookInstanceName": str,
        "NotebookInstanceArn": str,
        "NotebookInstanceStatus": NotebookInstanceStatusType,
        "Url": str,
        "InstanceType": InstanceTypeType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "NotebookInstanceLifecycleConfigName": str,
        "DefaultCodeRepository": str,
        "AdditionalCodeRepositories": List[str],
    },
)

ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef = TypedDict(
    "ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef",
    {
        "PipelineExecutionArn": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPipelineExecutionStepsRequestRequestTypeDef = TypedDict(
    "ListPipelineExecutionStepsRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
        "NextToken": str,
        "MaxResults": int,
        "SortOrder": SortOrderType,
    },
    total=False,
)

_RequiredListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef = TypedDict(
    "_RequiredListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef",
    {
        "PipelineName": str,
    },
)
_OptionalListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef = TypedDict(
    "_OptionalListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortPipelineExecutionsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef(
    _RequiredListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef,
    _OptionalListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef,
):
    pass


_RequiredListPipelineExecutionsRequestRequestTypeDef = TypedDict(
    "_RequiredListPipelineExecutionsRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)
_OptionalListPipelineExecutionsRequestRequestTypeDef = TypedDict(
    "_OptionalListPipelineExecutionsRequestRequestTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortPipelineExecutionsByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPipelineExecutionsRequestRequestTypeDef(
    _RequiredListPipelineExecutionsRequestRequestTypeDef,
    _OptionalListPipelineExecutionsRequestRequestTypeDef,
):
    pass


PipelineExecutionSummaryTypeDef = TypedDict(
    "PipelineExecutionSummaryTypeDef",
    {
        "PipelineExecutionArn": str,
        "StartTime": datetime,
        "PipelineExecutionStatus": PipelineExecutionStatusType,
        "PipelineExecutionDescription": str,
        "PipelineExecutionDisplayName": str,
        "PipelineExecutionFailureReason": str,
    },
)

_RequiredListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef = TypedDict(
    "_RequiredListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef",
    {
        "PipelineExecutionArn": str,
    },
)
_OptionalListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef = TypedDict(
    "_OptionalListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef(
    _RequiredListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef,
    _OptionalListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef,
):
    pass


_RequiredListPipelineParametersForExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredListPipelineParametersForExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
    },
)
_OptionalListPipelineParametersForExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalListPipelineParametersForExecutionRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPipelineParametersForExecutionRequestRequestTypeDef(
    _RequiredListPipelineParametersForExecutionRequestRequestTypeDef,
    _OptionalListPipelineParametersForExecutionRequestRequestTypeDef,
):
    pass


ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

ListPipelinesRequestListPipelinesPaginateTypeDef = TypedDict(
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    {
        "PipelineNamePrefix": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortPipelinesByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPipelinesRequestRequestTypeDef = TypedDict(
    "ListPipelinesRequestRequestTypeDef",
    {
        "PipelineNamePrefix": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortPipelinesByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

PipelineSummaryTypeDef = TypedDict(
    "PipelineSummaryTypeDef",
    {
        "PipelineArn": str,
        "PipelineName": str,
        "PipelineDisplayName": str,
        "PipelineDescription": str,
        "RoleArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastExecutionTime": datetime,
    },
)

ListProcessingJobsRequestListProcessingJobsPaginateTypeDef = TypedDict(
    "ListProcessingJobsRequestListProcessingJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": ProcessingJobStatusType,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListProcessingJobsRequestRequestTypeDef = TypedDict(
    "ListProcessingJobsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": ProcessingJobStatusType,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ProcessingJobSummaryTypeDef = TypedDict(
    "ProcessingJobSummaryTypeDef",
    {
        "ProcessingJobName": str,
        "ProcessingJobArn": str,
        "CreationTime": datetime,
        "ProcessingEndTime": datetime,
        "LastModifiedTime": datetime,
        "ProcessingJobStatus": ProcessingJobStatusType,
        "FailureReason": str,
        "ExitMessage": str,
    },
)

ListProjectsInputRequestTypeDef = TypedDict(
    "ListProjectsInputRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "MaxResults": int,
        "NameContains": str,
        "NextToken": str,
        "SortBy": ProjectSortByType,
        "SortOrder": ProjectSortOrderType,
    },
    total=False,
)

ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "ProjectName": str,
        "ProjectDescription": str,
        "ProjectArn": str,
        "ProjectId": str,
        "CreationTime": datetime,
        "ProjectStatus": ProjectStatusType,
    },
)

ListSpacesRequestListSpacesPaginateTypeDef = TypedDict(
    "ListSpacesRequestListSpacesPaginateTypeDef",
    {
        "SortOrder": SortOrderType,
        "SortBy": SpaceSortKeyType,
        "DomainIdEquals": str,
        "SpaceNameContains": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSpacesRequestRequestTypeDef = TypedDict(
    "ListSpacesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SortOrder": SortOrderType,
        "SortBy": SpaceSortKeyType,
        "DomainIdEquals": str,
        "SpaceNameContains": str,
    },
    total=False,
)

SpaceDetailsTypeDef = TypedDict(
    "SpaceDetailsTypeDef",
    {
        "DomainId": str,
        "SpaceName": str,
        "Status": SpaceStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

_RequiredListStageDevicesRequestListStageDevicesPaginateTypeDef = TypedDict(
    "_RequiredListStageDevicesRequestListStageDevicesPaginateTypeDef",
    {
        "EdgeDeploymentPlanName": str,
        "StageName": str,
    },
)
_OptionalListStageDevicesRequestListStageDevicesPaginateTypeDef = TypedDict(
    "_OptionalListStageDevicesRequestListStageDevicesPaginateTypeDef",
    {
        "ExcludeDevicesDeployedInOtherStage": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListStageDevicesRequestListStageDevicesPaginateTypeDef(
    _RequiredListStageDevicesRequestListStageDevicesPaginateTypeDef,
    _OptionalListStageDevicesRequestListStageDevicesPaginateTypeDef,
):
    pass


_RequiredListStageDevicesRequestRequestTypeDef = TypedDict(
    "_RequiredListStageDevicesRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
        "StageName": str,
    },
)
_OptionalListStageDevicesRequestRequestTypeDef = TypedDict(
    "_OptionalListStageDevicesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ExcludeDevicesDeployedInOtherStage": bool,
    },
    total=False,
)


class ListStageDevicesRequestRequestTypeDef(
    _RequiredListStageDevicesRequestRequestTypeDef, _OptionalListStageDevicesRequestRequestTypeDef
):
    pass


ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef = TypedDict(
    "ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef",
    {
        "NameContains": str,
        "AppTypeEquals": StudioLifecycleConfigAppTypeType,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "ModifiedTimeBefore": Union[datetime, str],
        "ModifiedTimeAfter": Union[datetime, str],
        "SortBy": StudioLifecycleConfigSortKeyType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListStudioLifecycleConfigsRequestRequestTypeDef = TypedDict(
    "ListStudioLifecycleConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "NameContains": str,
        "AppTypeEquals": StudioLifecycleConfigAppTypeType,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
        "ModifiedTimeBefore": Union[datetime, str],
        "ModifiedTimeAfter": Union[datetime, str],
        "SortBy": StudioLifecycleConfigSortKeyType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

StudioLifecycleConfigDetailsTypeDef = TypedDict(
    "StudioLifecycleConfigDetailsTypeDef",
    {
        "StudioLifecycleConfigArn": str,
        "StudioLifecycleConfigName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "StudioLifecycleConfigAppType": StudioLifecycleConfigAppTypeType,
    },
)

ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef = TypedDict(
    "ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef",
    {
        "NameContains": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSubscribedWorkteamsRequestRequestTypeDef = TypedDict(
    "ListSubscribedWorkteamsRequestRequestTypeDef",
    {
        "NameContains": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListTagsInputListTagsPaginateTypeDef = TypedDict(
    "_RequiredListTagsInputListTagsPaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsInputListTagsPaginateTypeDef = TypedDict(
    "_OptionalListTagsInputListTagsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTagsInputListTagsPaginateTypeDef(
    _RequiredListTagsInputListTagsPaginateTypeDef, _OptionalListTagsInputListTagsPaginateTypeDef
):
    pass


_RequiredListTagsInputRequestTypeDef = TypedDict(
    "_RequiredListTagsInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsInputRequestTypeDef = TypedDict(
    "_OptionalListTagsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTagsInputRequestTypeDef(
    _RequiredListTagsInputRequestTypeDef, _OptionalListTagsInputRequestTypeDef
):
    pass


_RequiredListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef = TypedDict(
    "_RequiredListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef",
    {
        "HyperParameterTuningJobName": str,
    },
)
_OptionalListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef = TypedDict(
    "_OptionalListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef",
    {
        "StatusEquals": TrainingJobStatusType,
        "SortBy": TrainingJobSortByOptionsType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef(
    _RequiredListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef,
    _OptionalListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef,
):
    pass


_RequiredListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef = TypedDict(
    "_RequiredListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef",
    {
        "HyperParameterTuningJobName": str,
    },
)
_OptionalListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef = TypedDict(
    "_OptionalListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "StatusEquals": TrainingJobStatusType,
        "SortBy": TrainingJobSortByOptionsType,
        "SortOrder": SortOrderType,
    },
    total=False,
)


class ListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef(
    _RequiredListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef,
    _OptionalListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef,
):
    pass


ListTrainingJobsRequestListTrainingJobsPaginateTypeDef = TypedDict(
    "ListTrainingJobsRequestListTrainingJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": TrainingJobStatusType,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "WarmPoolStatusEquals": WarmPoolResourceStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListTrainingJobsRequestRequestTypeDef = TypedDict(
    "ListTrainingJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": TrainingJobStatusType,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "WarmPoolStatusEquals": WarmPoolResourceStatusType,
    },
    total=False,
)

ListTransformJobsRequestListTransformJobsPaginateTypeDef = TypedDict(
    "ListTransformJobsRequestListTransformJobsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": TransformJobStatusType,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListTransformJobsRequestRequestTypeDef = TypedDict(
    "ListTransformJobsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "LastModifiedTimeAfter": Union[datetime, str],
        "LastModifiedTimeBefore": Union[datetime, str],
        "NameContains": str,
        "StatusEquals": TransformJobStatusType,
        "SortBy": SortByType,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

TransformJobSummaryTypeDef = TypedDict(
    "TransformJobSummaryTypeDef",
    {
        "TransformJobName": str,
        "TransformJobArn": str,
        "CreationTime": datetime,
        "TransformEndTime": datetime,
        "LastModifiedTime": datetime,
        "TransformJobStatus": TransformJobStatusType,
        "FailureReason": str,
    },
)

ListTrialComponentsRequestListTrialComponentsPaginateTypeDef = TypedDict(
    "ListTrialComponentsRequestListTrialComponentsPaginateTypeDef",
    {
        "ExperimentName": str,
        "TrialName": str,
        "SourceArn": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortTrialComponentsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListTrialComponentsRequestRequestTypeDef = TypedDict(
    "ListTrialComponentsRequestRequestTypeDef",
    {
        "ExperimentName": str,
        "TrialName": str,
        "SourceArn": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortTrialComponentsByType,
        "SortOrder": SortOrderType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTrialsRequestListTrialsPaginateTypeDef = TypedDict(
    "ListTrialsRequestListTrialsPaginateTypeDef",
    {
        "ExperimentName": str,
        "TrialComponentName": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortTrialsByType,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListTrialsRequestRequestTypeDef = TypedDict(
    "ListTrialsRequestRequestTypeDef",
    {
        "ExperimentName": str,
        "TrialComponentName": str,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "SortBy": SortTrialsByType,
        "SortOrder": SortOrderType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListUserProfilesRequestListUserProfilesPaginateTypeDef = TypedDict(
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
    {
        "SortOrder": SortOrderType,
        "SortBy": UserProfileSortKeyType,
        "DomainIdEquals": str,
        "UserProfileNameContains": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListUserProfilesRequestRequestTypeDef = TypedDict(
    "ListUserProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SortOrder": SortOrderType,
        "SortBy": UserProfileSortKeyType,
        "DomainIdEquals": str,
        "UserProfileNameContains": str,
    },
    total=False,
)

UserProfileDetailsTypeDef = TypedDict(
    "UserProfileDetailsTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
        "Status": UserProfileStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

ListWorkforcesRequestListWorkforcesPaginateTypeDef = TypedDict(
    "ListWorkforcesRequestListWorkforcesPaginateTypeDef",
    {
        "SortBy": ListWorkforcesSortByOptionsType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListWorkforcesRequestRequestTypeDef = TypedDict(
    "ListWorkforcesRequestRequestTypeDef",
    {
        "SortBy": ListWorkforcesSortByOptionsType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListWorkteamsRequestListWorkteamsPaginateTypeDef = TypedDict(
    "ListWorkteamsRequestListWorkteamsPaginateTypeDef",
    {
        "SortBy": ListWorkteamsSortByOptionsType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListWorkteamsRequestRequestTypeDef = TypedDict(
    "ListWorkteamsRequestRequestTypeDef",
    {
        "SortBy": ListWorkteamsSortByOptionsType,
        "SortOrder": SortOrderType,
        "NameContains": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

OidcMemberDefinitionTypeDef = TypedDict(
    "OidcMemberDefinitionTypeDef",
    {
        "Groups": Sequence[str],
    },
)

MonitoringGroundTruthS3InputTypeDef = TypedDict(
    "MonitoringGroundTruthS3InputTypeDef",
    {
        "S3Uri": str,
    },
    total=False,
)

ModelDashboardEndpointTypeDef = TypedDict(
    "ModelDashboardEndpointTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "EndpointStatus": EndpointStatusType,
    },
)

ModelDashboardIndicatorActionTypeDef = TypedDict(
    "ModelDashboardIndicatorActionTypeDef",
    {
        "Enabled": bool,
    },
)

S3ModelDataSourceTypeDef = TypedDict(
    "S3ModelDataSourceTypeDef",
    {
        "S3Uri": str,
        "S3DataType": S3ModelDataTypeType,
        "CompressionType": ModelCompressionTypeType,
    },
)

RealTimeInferenceConfigTypeDef = TypedDict(
    "RealTimeInferenceConfigTypeDef",
    {
        "InstanceType": InstanceTypeType,
        "InstanceCount": int,
    },
)

ModelInputTypeDef = TypedDict(
    "ModelInputTypeDef",
    {
        "DataInputConfig": str,
    },
)

ModelLatencyThresholdTypeDef = TypedDict(
    "ModelLatencyThresholdTypeDef",
    {
        "Percentile": str,
        "ValueInMilliseconds": int,
    },
    total=False,
)

ModelMetadataFilterTypeDef = TypedDict(
    "ModelMetadataFilterTypeDef",
    {
        "Name": ModelMetadataFilterTypeType,
        "Value": str,
    },
)

ModelPackageStatusItemTypeDef = TypedDict(
    "ModelPackageStatusItemTypeDef",
    {
        "Name": str,
        "Status": DetailedModelPackageStatusType,
        "FailureReason": str,
    },
)

ModelStepMetadataTypeDef = TypedDict(
    "ModelStepMetadataTypeDef",
    {
        "Arn": str,
    },
)

_RequiredMonitoringAppSpecificationTypeDef = TypedDict(
    "_RequiredMonitoringAppSpecificationTypeDef",
    {
        "ImageUri": str,
    },
)
_OptionalMonitoringAppSpecificationTypeDef = TypedDict(
    "_OptionalMonitoringAppSpecificationTypeDef",
    {
        "ContainerEntrypoint": Sequence[str],
        "ContainerArguments": Sequence[str],
        "RecordPreprocessorSourceUri": str,
        "PostAnalyticsProcessorSourceUri": str,
    },
    total=False,
)


class MonitoringAppSpecificationTypeDef(
    _RequiredMonitoringAppSpecificationTypeDef, _OptionalMonitoringAppSpecificationTypeDef
):
    pass


_RequiredMonitoringClusterConfigTypeDef = TypedDict(
    "_RequiredMonitoringClusterConfigTypeDef",
    {
        "InstanceCount": int,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
    },
)
_OptionalMonitoringClusterConfigTypeDef = TypedDict(
    "_OptionalMonitoringClusterConfigTypeDef",
    {
        "VolumeKmsKeyId": str,
    },
    total=False,
)


class MonitoringClusterConfigTypeDef(
    _RequiredMonitoringClusterConfigTypeDef, _OptionalMonitoringClusterConfigTypeDef
):
    pass


MonitoringCsvDatasetFormatTypeDef = TypedDict(
    "MonitoringCsvDatasetFormatTypeDef",
    {
        "Header": bool,
    },
    total=False,
)

MonitoringJsonDatasetFormatTypeDef = TypedDict(
    "MonitoringJsonDatasetFormatTypeDef",
    {
        "Line": bool,
    },
    total=False,
)

_RequiredMonitoringS3OutputTypeDef = TypedDict(
    "_RequiredMonitoringS3OutputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
    },
)
_OptionalMonitoringS3OutputTypeDef = TypedDict(
    "_OptionalMonitoringS3OutputTypeDef",
    {
        "S3UploadMode": ProcessingS3UploadModeType,
    },
    total=False,
)


class MonitoringS3OutputTypeDef(
    _RequiredMonitoringS3OutputTypeDef, _OptionalMonitoringS3OutputTypeDef
):
    pass


ScheduleConfigTypeDef = TypedDict(
    "ScheduleConfigTypeDef",
    {
        "ScheduleExpression": str,
    },
)

_RequiredS3StorageConfigTypeDef = TypedDict(
    "_RequiredS3StorageConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalS3StorageConfigTypeDef = TypedDict(
    "_OptionalS3StorageConfigTypeDef",
    {
        "KmsKeyId": str,
        "ResolvedOutputS3Uri": str,
    },
    total=False,
)


class S3StorageConfigTypeDef(_RequiredS3StorageConfigTypeDef, _OptionalS3StorageConfigTypeDef):
    pass


OidcConfigForResponseTypeDef = TypedDict(
    "OidcConfigForResponseTypeDef",
    {
        "ClientId": str,
        "Issuer": str,
        "AuthorizationEndpoint": str,
        "TokenEndpoint": str,
        "UserInfoEndpoint": str,
        "LogoutEndpoint": str,
        "JwksUri": str,
    },
)

OnlineStoreSecurityConfigTypeDef = TypedDict(
    "OnlineStoreSecurityConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

TtlDurationTypeDef = TypedDict(
    "TtlDurationTypeDef",
    {
        "Unit": TtlDurationUnitType,
        "Value": int,
    },
    total=False,
)

_RequiredTargetPlatformTypeDef = TypedDict(
    "_RequiredTargetPlatformTypeDef",
    {
        "Os": TargetPlatformOsType,
        "Arch": TargetPlatformArchType,
    },
)
_OptionalTargetPlatformTypeDef = TypedDict(
    "_OptionalTargetPlatformTypeDef",
    {
        "Accelerator": TargetPlatformAcceleratorType,
    },
    total=False,
)


class TargetPlatformTypeDef(_RequiredTargetPlatformTypeDef, _OptionalTargetPlatformTypeDef):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ParentTypeDef = TypedDict(
    "ParentTypeDef",
    {
        "TrialName": str,
        "ExperimentName": str,
    },
)

ProductionVariantStatusTypeDef = TypedDict(
    "ProductionVariantStatusTypeDef",
    {
        "Status": VariantStatusType,
        "StatusMessage": str,
        "StartTime": datetime,
    },
)

PhaseTypeDef = TypedDict(
    "PhaseTypeDef",
    {
        "InitialNumberOfUsers": int,
        "SpawnRate": int,
        "DurationInSeconds": int,
    },
    total=False,
)

ProcessingJobStepMetadataTypeDef = TypedDict(
    "ProcessingJobStepMetadataTypeDef",
    {
        "Arn": str,
    },
)

QualityCheckStepMetadataTypeDef = TypedDict(
    "QualityCheckStepMetadataTypeDef",
    {
        "CheckType": str,
        "BaselineUsedForDriftCheckStatistics": str,
        "BaselineUsedForDriftCheckConstraints": str,
        "CalculatedBaselineStatistics": str,
        "CalculatedBaselineConstraints": str,
        "ModelPackageGroupName": str,
        "ViolationReport": str,
        "CheckJobArn": str,
        "SkipCheck": bool,
        "RegisterNewBaseline": bool,
    },
)

RegisterModelStepMetadataTypeDef = TypedDict(
    "RegisterModelStepMetadataTypeDef",
    {
        "Arn": str,
    },
)

TrainingJobStepMetadataTypeDef = TypedDict(
    "TrainingJobStepMetadataTypeDef",
    {
        "Arn": str,
    },
)

TransformJobStepMetadataTypeDef = TypedDict(
    "TransformJobStepMetadataTypeDef",
    {
        "Arn": str,
    },
)

TuningJobStepMetaDataTypeDef = TypedDict(
    "TuningJobStepMetaDataTypeDef",
    {
        "Arn": str,
    },
)

SelectiveExecutionResultTypeDef = TypedDict(
    "SelectiveExecutionResultTypeDef",
    {
        "SourcePipelineExecutionArn": str,
    },
)

_RequiredProcessingClusterConfigTypeDef = TypedDict(
    "_RequiredProcessingClusterConfigTypeDef",
    {
        "InstanceCount": int,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
    },
)
_OptionalProcessingClusterConfigTypeDef = TypedDict(
    "_OptionalProcessingClusterConfigTypeDef",
    {
        "VolumeKmsKeyId": str,
    },
    total=False,
)


class ProcessingClusterConfigTypeDef(
    _RequiredProcessingClusterConfigTypeDef, _OptionalProcessingClusterConfigTypeDef
):
    pass


ProcessingFeatureStoreOutputTypeDef = TypedDict(
    "ProcessingFeatureStoreOutputTypeDef",
    {
        "FeatureGroupName": str,
    },
)

_RequiredProcessingS3InputTypeDef = TypedDict(
    "_RequiredProcessingS3InputTypeDef",
    {
        "S3Uri": str,
        "S3DataType": ProcessingS3DataTypeType,
    },
)
_OptionalProcessingS3InputTypeDef = TypedDict(
    "_OptionalProcessingS3InputTypeDef",
    {
        "LocalPath": str,
        "S3InputMode": ProcessingS3InputModeType,
        "S3DataDistributionType": ProcessingS3DataDistributionTypeType,
        "S3CompressionType": ProcessingS3CompressionTypeType,
    },
    total=False,
)


class ProcessingS3InputTypeDef(
    _RequiredProcessingS3InputTypeDef, _OptionalProcessingS3InputTypeDef
):
    pass


ProcessingS3OutputTypeDef = TypedDict(
    "ProcessingS3OutputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
        "S3UploadMode": ProcessingS3UploadModeType,
    },
)

_RequiredProductionVariantCoreDumpConfigTypeDef = TypedDict(
    "_RequiredProductionVariantCoreDumpConfigTypeDef",
    {
        "DestinationS3Uri": str,
    },
)
_OptionalProductionVariantCoreDumpConfigTypeDef = TypedDict(
    "_OptionalProductionVariantCoreDumpConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class ProductionVariantCoreDumpConfigTypeDef(
    _RequiredProductionVariantCoreDumpConfigTypeDef, _OptionalProductionVariantCoreDumpConfigTypeDef
):
    pass


ProfilerConfigForUpdateTypeDef = TypedDict(
    "ProfilerConfigForUpdateTypeDef",
    {
        "S3OutputPath": str,
        "ProfilingIntervalInMilliseconds": int,
        "ProfilingParameters": Mapping[str, str],
        "DisableProfiler": bool,
    },
    total=False,
)

PropertyNameQueryTypeDef = TypedDict(
    "PropertyNameQueryTypeDef",
    {
        "PropertyNameHint": str,
    },
)

ProvisioningParameterTypeDef = TypedDict(
    "ProvisioningParameterTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

USDTypeDef = TypedDict(
    "USDTypeDef",
    {
        "Dollars": int,
        "Cents": int,
        "TenthFractionsOfACent": int,
    },
    total=False,
)

PutModelPackageGroupPolicyInputRequestTypeDef = TypedDict(
    "PutModelPackageGroupPolicyInputRequestTypeDef",
    {
        "ModelPackageGroupName": str,
        "ResourcePolicy": str,
    },
)

PutModelPackageGroupPolicyOutputTypeDef = TypedDict(
    "PutModelPackageGroupPolicyOutputTypeDef",
    {
        "ModelPackageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

QueryFiltersTypeDef = TypedDict(
    "QueryFiltersTypeDef",
    {
        "Types": Sequence[str],
        "LineageTypes": Sequence[LineageTypeType],
        "CreatedBefore": Union[datetime, str],
        "CreatedAfter": Union[datetime, str],
        "ModifiedBefore": Union[datetime, str],
        "ModifiedAfter": Union[datetime, str],
        "Properties": Mapping[str, str],
    },
    total=False,
)

VertexTypeDef = TypedDict(
    "VertexTypeDef",
    {
        "Arn": str,
        "Type": str,
        "LineageType": LineageTypeType,
    },
)

RStudioServerProAppSettingsTypeDef = TypedDict(
    "RStudioServerProAppSettingsTypeDef",
    {
        "AccessStatus": RStudioServerProAccessStatusType,
        "UserGroup": RStudioServerProUserGroupType,
    },
    total=False,
)

RecommendationJobCompiledOutputConfigTypeDef = TypedDict(
    "RecommendationJobCompiledOutputConfigTypeDef",
    {
        "S3OutputUri": str,
    },
    total=False,
)

RecommendationJobPayloadConfigTypeDef = TypedDict(
    "RecommendationJobPayloadConfigTypeDef",
    {
        "SamplePayloadUrl": str,
        "SupportedContentTypes": Sequence[str],
    },
    total=False,
)

RecommendationJobResourceLimitTypeDef = TypedDict(
    "RecommendationJobResourceLimitTypeDef",
    {
        "MaxNumberOfTests": int,
        "MaxParallelOfTests": int,
    },
    total=False,
)

RecommendationJobVpcConfigTypeDef = TypedDict(
    "RecommendationJobVpcConfigTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "Subnets": Sequence[str],
    },
)

RenderableTaskTypeDef = TypedDict(
    "RenderableTaskTypeDef",
    {
        "Input": str,
    },
)

RenderingErrorTypeDef = TypedDict(
    "RenderingErrorTypeDef",
    {
        "Code": str,
        "Message": str,
    },
)

ResourceConfigForUpdateTypeDef = TypedDict(
    "ResourceConfigForUpdateTypeDef",
    {
        "KeepAlivePeriodInSeconds": int,
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

RetryPipelineExecutionResponseTypeDef = TypedDict(
    "RetryPipelineExecutionResponseTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSearchRequestRequestTypeDef = TypedDict(
    "_RequiredSearchRequestRequestTypeDef",
    {
        "Resource": ResourceTypeType,
    },
)
_OptionalSearchRequestRequestTypeDef = TypedDict(
    "_OptionalSearchRequestRequestTypeDef",
    {
        "SearchExpression": "SearchExpressionTypeDef",
        "SortBy": str,
        "SortOrder": SearchSortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchRequestRequestTypeDef(
    _RequiredSearchRequestRequestTypeDef, _OptionalSearchRequestRequestTypeDef
):
    pass


_RequiredSearchRequestSearchPaginateTypeDef = TypedDict(
    "_RequiredSearchRequestSearchPaginateTypeDef",
    {
        "Resource": ResourceTypeType,
    },
)
_OptionalSearchRequestSearchPaginateTypeDef = TypedDict(
    "_OptionalSearchRequestSearchPaginateTypeDef",
    {
        "SearchExpression": "SearchExpressionTypeDef",
        "SortBy": str,
        "SortOrder": SearchSortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchRequestSearchPaginateTypeDef(
    _RequiredSearchRequestSearchPaginateTypeDef, _OptionalSearchRequestSearchPaginateTypeDef
):
    pass


SelectedStepTypeDef = TypedDict(
    "SelectedStepTypeDef",
    {
        "StepName": str,
    },
)

_RequiredSendPipelineExecutionStepFailureRequestRequestTypeDef = TypedDict(
    "_RequiredSendPipelineExecutionStepFailureRequestRequestTypeDef",
    {
        "CallbackToken": str,
    },
)
_OptionalSendPipelineExecutionStepFailureRequestRequestTypeDef = TypedDict(
    "_OptionalSendPipelineExecutionStepFailureRequestRequestTypeDef",
    {
        "FailureReason": str,
        "ClientRequestToken": str,
    },
    total=False,
)


class SendPipelineExecutionStepFailureRequestRequestTypeDef(
    _RequiredSendPipelineExecutionStepFailureRequestRequestTypeDef,
    _OptionalSendPipelineExecutionStepFailureRequestRequestTypeDef,
):
    pass


SendPipelineExecutionStepFailureResponseTypeDef = TypedDict(
    "SendPipelineExecutionStepFailureResponseTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SendPipelineExecutionStepSuccessResponseTypeDef = TypedDict(
    "SendPipelineExecutionStepSuccessResponseTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ShadowModelVariantConfigTypeDef = TypedDict(
    "ShadowModelVariantConfigTypeDef",
    {
        "ShadowModelVariantName": str,
        "SamplingPercentage": int,
    },
)

SharingSettingsTypeDef = TypedDict(
    "SharingSettingsTypeDef",
    {
        "NotebookOutputOption": NotebookOutputOptionType,
        "S3OutputPath": str,
        "S3KmsKeyId": str,
    },
    total=False,
)

_RequiredSourceAlgorithmTypeDef = TypedDict(
    "_RequiredSourceAlgorithmTypeDef",
    {
        "AlgorithmName": str,
    },
)
_OptionalSourceAlgorithmTypeDef = TypedDict(
    "_OptionalSourceAlgorithmTypeDef",
    {
        "ModelDataUrl": str,
    },
    total=False,
)


class SourceAlgorithmTypeDef(_RequiredSourceAlgorithmTypeDef, _OptionalSourceAlgorithmTypeDef):
    pass


StartEdgeDeploymentStageRequestRequestTypeDef = TypedDict(
    "StartEdgeDeploymentStageRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
        "StageName": str,
    },
)

StartInferenceExperimentRequestRequestTypeDef = TypedDict(
    "StartInferenceExperimentRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StartInferenceExperimentResponseTypeDef = TypedDict(
    "StartInferenceExperimentResponseTypeDef",
    {
        "InferenceExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "StartMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
    },
)

StartNotebookInstanceInputRequestTypeDef = TypedDict(
    "StartNotebookInstanceInputRequestTypeDef",
    {
        "NotebookInstanceName": str,
    },
)

StartPipelineExecutionResponseTypeDef = TypedDict(
    "StartPipelineExecutionResponseTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopAutoMLJobRequestRequestTypeDef = TypedDict(
    "StopAutoMLJobRequestRequestTypeDef",
    {
        "AutoMLJobName": str,
    },
)

StopCompilationJobRequestRequestTypeDef = TypedDict(
    "StopCompilationJobRequestRequestTypeDef",
    {
        "CompilationJobName": str,
    },
)

StopEdgeDeploymentStageRequestRequestTypeDef = TypedDict(
    "StopEdgeDeploymentStageRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
        "StageName": str,
    },
)

StopEdgePackagingJobRequestRequestTypeDef = TypedDict(
    "StopEdgePackagingJobRequestRequestTypeDef",
    {
        "EdgePackagingJobName": str,
    },
)

StopHyperParameterTuningJobRequestRequestTypeDef = TypedDict(
    "StopHyperParameterTuningJobRequestRequestTypeDef",
    {
        "HyperParameterTuningJobName": str,
    },
)

StopInferenceExperimentResponseTypeDef = TypedDict(
    "StopInferenceExperimentResponseTypeDef",
    {
        "InferenceExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopInferenceRecommendationsJobRequestRequestTypeDef = TypedDict(
    "StopInferenceRecommendationsJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
)

StopLabelingJobRequestRequestTypeDef = TypedDict(
    "StopLabelingJobRequestRequestTypeDef",
    {
        "LabelingJobName": str,
    },
)

StopMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "StopMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
    },
)

StopNotebookInstanceInputRequestTypeDef = TypedDict(
    "StopNotebookInstanceInputRequestTypeDef",
    {
        "NotebookInstanceName": str,
    },
)

StopPipelineExecutionRequestRequestTypeDef = TypedDict(
    "StopPipelineExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
        "ClientRequestToken": str,
    },
)

StopPipelineExecutionResponseTypeDef = TypedDict(
    "StopPipelineExecutionResponseTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopProcessingJobRequestRequestTypeDef = TypedDict(
    "StopProcessingJobRequestRequestTypeDef",
    {
        "ProcessingJobName": str,
    },
)

StopTrainingJobRequestRequestTypeDef = TypedDict(
    "StopTrainingJobRequestRequestTypeDef",
    {
        "TrainingJobName": str,
    },
)

StopTransformJobRequestRequestTypeDef = TypedDict(
    "StopTransformJobRequestRequestTypeDef",
    {
        "TransformJobName": str,
    },
)

_RequiredTimeSeriesConfigTypeDef = TypedDict(
    "_RequiredTimeSeriesConfigTypeDef",
    {
        "TargetAttributeName": str,
        "TimestampAttributeName": str,
        "ItemIdentifierAttributeName": str,
    },
)
_OptionalTimeSeriesConfigTypeDef = TypedDict(
    "_OptionalTimeSeriesConfigTypeDef",
    {
        "GroupingAttributeNames": Sequence[str],
    },
    total=False,
)


class TimeSeriesConfigTypeDef(_RequiredTimeSeriesConfigTypeDef, _OptionalTimeSeriesConfigTypeDef):
    pass


TimeSeriesTransformationsTypeDef = TypedDict(
    "TimeSeriesTransformationsTypeDef",
    {
        "Filling": Mapping[str, Mapping[FillingTypeType, str]],
        "Aggregation": Mapping[str, AggregationTransformationValueType],
    },
    total=False,
)

TrainingRepositoryAuthConfigTypeDef = TypedDict(
    "TrainingRepositoryAuthConfigTypeDef",
    {
        "TrainingRepositoryCredentialsProviderArn": str,
    },
)

TransformS3DataSourceTypeDef = TypedDict(
    "TransformS3DataSourceTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
    },
)

_RequiredUpdateActionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateActionRequestRequestTypeDef",
    {
        "ActionName": str,
    },
)
_OptionalUpdateActionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateActionRequestRequestTypeDef",
    {
        "Description": str,
        "Status": ActionStatusType,
        "Properties": Mapping[str, str],
        "PropertiesToRemove": Sequence[str],
    },
    total=False,
)


class UpdateActionRequestRequestTypeDef(
    _RequiredUpdateActionRequestRequestTypeDef, _OptionalUpdateActionRequestRequestTypeDef
):
    pass


UpdateActionResponseTypeDef = TypedDict(
    "UpdateActionResponseTypeDef",
    {
        "ActionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateAppImageConfigResponseTypeDef = TypedDict(
    "UpdateAppImageConfigResponseTypeDef",
    {
        "AppImageConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateArtifactRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateArtifactRequestRequestTypeDef",
    {
        "ArtifactArn": str,
    },
)
_OptionalUpdateArtifactRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateArtifactRequestRequestTypeDef",
    {
        "ArtifactName": str,
        "Properties": Mapping[str, str],
        "PropertiesToRemove": Sequence[str],
    },
    total=False,
)


class UpdateArtifactRequestRequestTypeDef(
    _RequiredUpdateArtifactRequestRequestTypeDef, _OptionalUpdateArtifactRequestRequestTypeDef
):
    pass


UpdateArtifactResponseTypeDef = TypedDict(
    "UpdateArtifactResponseTypeDef",
    {
        "ArtifactArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateCodeRepositoryOutputTypeDef = TypedDict(
    "UpdateCodeRepositoryOutputTypeDef",
    {
        "CodeRepositoryArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateContextRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContextRequestRequestTypeDef",
    {
        "ContextName": str,
    },
)
_OptionalUpdateContextRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContextRequestRequestTypeDef",
    {
        "Description": str,
        "Properties": Mapping[str, str],
        "PropertiesToRemove": Sequence[str],
    },
    total=False,
)


class UpdateContextRequestRequestTypeDef(
    _RequiredUpdateContextRequestRequestTypeDef, _OptionalUpdateContextRequestRequestTypeDef
):
    pass


UpdateContextResponseTypeDef = TypedDict(
    "UpdateContextResponseTypeDef",
    {
        "ContextArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateDomainResponseTypeDef = TypedDict(
    "UpdateDomainResponseTypeDef",
    {
        "DomainArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

VariantPropertyTypeDef = TypedDict(
    "VariantPropertyTypeDef",
    {
        "VariantPropertyType": VariantPropertyTypeType,
    },
)

UpdateEndpointOutputTypeDef = TypedDict(
    "UpdateEndpointOutputTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEndpointWeightsAndCapacitiesOutputTypeDef = TypedDict(
    "UpdateEndpointWeightsAndCapacitiesOutputTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateExperimentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateExperimentRequestRequestTypeDef",
    {
        "ExperimentName": str,
    },
)
_OptionalUpdateExperimentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateExperimentRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
    },
    total=False,
)


class UpdateExperimentRequestRequestTypeDef(
    _RequiredUpdateExperimentRequestRequestTypeDef, _OptionalUpdateExperimentRequestRequestTypeDef
):
    pass


UpdateExperimentResponseTypeDef = TypedDict(
    "UpdateExperimentResponseTypeDef",
    {
        "ExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFeatureGroupResponseTypeDef = TypedDict(
    "UpdateFeatureGroupResponseTypeDef",
    {
        "FeatureGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateHubRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateHubRequestRequestTypeDef",
    {
        "HubName": str,
    },
)
_OptionalUpdateHubRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateHubRequestRequestTypeDef",
    {
        "HubDescription": str,
        "HubDisplayName": str,
        "HubSearchKeywords": Sequence[str],
    },
    total=False,
)


class UpdateHubRequestRequestTypeDef(
    _RequiredUpdateHubRequestRequestTypeDef, _OptionalUpdateHubRequestRequestTypeDef
):
    pass


UpdateHubResponseTypeDef = TypedDict(
    "UpdateHubResponseTypeDef",
    {
        "HubArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateImageRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateImageRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalUpdateImageRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateImageRequestRequestTypeDef",
    {
        "DeleteProperties": Sequence[str],
        "Description": str,
        "DisplayName": str,
        "RoleArn": str,
    },
    total=False,
)


class UpdateImageRequestRequestTypeDef(
    _RequiredUpdateImageRequestRequestTypeDef, _OptionalUpdateImageRequestRequestTypeDef
):
    pass


UpdateImageResponseTypeDef = TypedDict(
    "UpdateImageResponseTypeDef",
    {
        "ImageArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateImageVersionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateImageVersionRequestRequestTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalUpdateImageVersionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateImageVersionRequestRequestTypeDef",
    {
        "Alias": str,
        "Version": int,
        "AliasesToAdd": Sequence[str],
        "AliasesToDelete": Sequence[str],
        "VendorGuidance": VendorGuidanceType,
        "JobType": JobTypeType,
        "MLFramework": str,
        "ProgrammingLang": str,
        "Processor": ProcessorType,
        "Horovod": bool,
        "ReleaseNotes": str,
    },
    total=False,
)


class UpdateImageVersionRequestRequestTypeDef(
    _RequiredUpdateImageVersionRequestRequestTypeDef,
    _OptionalUpdateImageVersionRequestRequestTypeDef,
):
    pass


UpdateImageVersionResponseTypeDef = TypedDict(
    "UpdateImageVersionResponseTypeDef",
    {
        "ImageVersionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateInferenceExperimentResponseTypeDef = TypedDict(
    "UpdateInferenceExperimentResponseTypeDef",
    {
        "InferenceExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateModelCardRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateModelCardRequestRequestTypeDef",
    {
        "ModelCardName": str,
    },
)
_OptionalUpdateModelCardRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateModelCardRequestRequestTypeDef",
    {
        "Content": str,
        "ModelCardStatus": ModelCardStatusType,
    },
    total=False,
)


class UpdateModelCardRequestRequestTypeDef(
    _RequiredUpdateModelCardRequestRequestTypeDef, _OptionalUpdateModelCardRequestRequestTypeDef
):
    pass


UpdateModelCardResponseTypeDef = TypedDict(
    "UpdateModelCardResponseTypeDef",
    {
        "ModelCardArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateModelPackageOutputTypeDef = TypedDict(
    "UpdateModelPackageOutputTypeDef",
    {
        "ModelPackageArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateMonitoringAlertRequestRequestTypeDef = TypedDict(
    "UpdateMonitoringAlertRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringAlertName": str,
        "DatapointsToAlert": int,
        "EvaluationPeriod": int,
    },
)

UpdateMonitoringAlertResponseTypeDef = TypedDict(
    "UpdateMonitoringAlertResponseTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringAlertName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateMonitoringScheduleResponseTypeDef = TypedDict(
    "UpdateMonitoringScheduleResponseTypeDef",
    {
        "MonitoringScheduleArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePipelineExecutionResponseTypeDef = TypedDict(
    "UpdatePipelineExecutionResponseTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePipelineResponseTypeDef = TypedDict(
    "UpdatePipelineResponseTypeDef",
    {
        "PipelineArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateProjectOutputTypeDef = TypedDict(
    "UpdateProjectOutputTypeDef",
    {
        "ProjectArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateSpaceResponseTypeDef = TypedDict(
    "UpdateSpaceResponseTypeDef",
    {
        "SpaceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateTrainingJobResponseTypeDef = TypedDict(
    "UpdateTrainingJobResponseTypeDef",
    {
        "TrainingJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateTrialComponentResponseTypeDef = TypedDict(
    "UpdateTrialComponentResponseTypeDef",
    {
        "TrialComponentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateTrialRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrialRequestRequestTypeDef",
    {
        "TrialName": str,
    },
)
_OptionalUpdateTrialRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrialRequestRequestTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)


class UpdateTrialRequestRequestTypeDef(
    _RequiredUpdateTrialRequestRequestTypeDef, _OptionalUpdateTrialRequestRequestTypeDef
):
    pass


UpdateTrialResponseTypeDef = TypedDict(
    "UpdateTrialResponseTypeDef",
    {
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateUserProfileResponseTypeDef = TypedDict(
    "UpdateUserProfileResponseTypeDef",
    {
        "UserProfileArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

WorkforceVpcConfigResponseTypeDef = TypedDict(
    "WorkforceVpcConfigResponseTypeDef",
    {
        "VpcId": str,
        "SecurityGroupIds": List[str],
        "Subnets": List[str],
        "VpcEndpointId": str,
    },
)

ActionSummaryTypeDef = TypedDict(
    "ActionSummaryTypeDef",
    {
        "ActionArn": str,
        "ActionName": str,
        "Source": ActionSourceTypeDef,
        "ActionType": str,
        "Status": ActionStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

AddTagsInputRequestTypeDef = TypedDict(
    "AddTagsInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

AddTagsOutputTypeDef = TypedDict(
    "AddTagsOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateExperimentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateExperimentRequestRequestTypeDef",
    {
        "ExperimentName": str,
    },
)
_OptionalCreateExperimentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateExperimentRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateExperimentRequestRequestTypeDef(
    _RequiredCreateExperimentRequestRequestTypeDef, _OptionalCreateExperimentRequestRequestTypeDef
):
    pass


_RequiredCreateImageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageRequestRequestTypeDef",
    {
        "ImageName": str,
        "RoleArn": str,
    },
)
_OptionalCreateImageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateImageRequestRequestTypeDef(
    _RequiredCreateImageRequestRequestTypeDef, _OptionalCreateImageRequestRequestTypeDef
):
    pass


_RequiredCreateModelPackageGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateModelPackageGroupInputRequestTypeDef",
    {
        "ModelPackageGroupName": str,
    },
)
_OptionalCreateModelPackageGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateModelPackageGroupInputRequestTypeDef",
    {
        "ModelPackageGroupDescription": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateModelPackageGroupInputRequestTypeDef(
    _RequiredCreateModelPackageGroupInputRequestTypeDef,
    _OptionalCreateModelPackageGroupInputRequestTypeDef,
):
    pass


_RequiredCreateStudioLifecycleConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStudioLifecycleConfigRequestRequestTypeDef",
    {
        "StudioLifecycleConfigName": str,
        "StudioLifecycleConfigContent": str,
        "StudioLifecycleConfigAppType": StudioLifecycleConfigAppTypeType,
    },
)
_OptionalCreateStudioLifecycleConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStudioLifecycleConfigRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateStudioLifecycleConfigRequestRequestTypeDef(
    _RequiredCreateStudioLifecycleConfigRequestRequestTypeDef,
    _OptionalCreateStudioLifecycleConfigRequestRequestTypeDef,
):
    pass


_RequiredImportHubContentRequestRequestTypeDef = TypedDict(
    "_RequiredImportHubContentRequestRequestTypeDef",
    {
        "HubContentName": str,
        "HubContentType": HubContentTypeType,
        "DocumentSchemaVersion": str,
        "HubName": str,
        "HubContentDocument": str,
    },
)
_OptionalImportHubContentRequestRequestTypeDef = TypedDict(
    "_OptionalImportHubContentRequestRequestTypeDef",
    {
        "HubContentVersion": str,
        "HubContentDisplayName": str,
        "HubContentDescription": str,
        "HubContentMarkdown": str,
        "HubContentSearchKeywords": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class ImportHubContentRequestRequestTypeDef(
    _RequiredImportHubContentRequestRequestTypeDef, _OptionalImportHubContentRequestRequestTypeDef
):
    pass


ListTagsOutputTypeDef = TypedDict(
    "ListTagsOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoRollbackConfigTypeDef = TypedDict(
    "AutoRollbackConfigTypeDef",
    {
        "Alarms": Sequence[AlarmTypeDef],
    },
    total=False,
)

_RequiredHyperParameterAlgorithmSpecificationTypeDef = TypedDict(
    "_RequiredHyperParameterAlgorithmSpecificationTypeDef",
    {
        "TrainingInputMode": TrainingInputModeType,
    },
)
_OptionalHyperParameterAlgorithmSpecificationTypeDef = TypedDict(
    "_OptionalHyperParameterAlgorithmSpecificationTypeDef",
    {
        "TrainingImage": str,
        "AlgorithmName": str,
        "MetricDefinitions": Sequence[MetricDefinitionTypeDef],
    },
    total=False,
)


class HyperParameterAlgorithmSpecificationTypeDef(
    _RequiredHyperParameterAlgorithmSpecificationTypeDef,
    _OptionalHyperParameterAlgorithmSpecificationTypeDef,
):
    pass


AlgorithmStatusDetailsTypeDef = TypedDict(
    "AlgorithmStatusDetailsTypeDef",
    {
        "ValidationStatuses": List[AlgorithmStatusItemTypeDef],
        "ImageScanStatuses": List[AlgorithmStatusItemTypeDef],
    },
)

ListAlgorithmsOutputTypeDef = TypedDict(
    "ListAlgorithmsOutputTypeDef",
    {
        "AlgorithmSummaryList": List[AlgorithmSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAppsResponseTypeDef = TypedDict(
    "ListAppsResponseTypeDef",
    {
        "Apps": List[AppDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredArtifactSourceTypeDef = TypedDict(
    "_RequiredArtifactSourceTypeDef",
    {
        "SourceUri": str,
    },
)
_OptionalArtifactSourceTypeDef = TypedDict(
    "_OptionalArtifactSourceTypeDef",
    {
        "SourceTypes": Sequence[ArtifactSourceTypeTypeDef],
    },
    total=False,
)


class ArtifactSourceTypeDef(_RequiredArtifactSourceTypeDef, _OptionalArtifactSourceTypeDef):
    pass


AsyncInferenceOutputConfigTypeDef = TypedDict(
    "AsyncInferenceOutputConfigTypeDef",
    {
        "KmsKeyId": str,
        "S3OutputPath": str,
        "NotificationConfig": AsyncInferenceNotificationConfigTypeDef,
        "S3FailurePath": str,
    },
    total=False,
)

AutoMLCandidateGenerationConfigTypeDef = TypedDict(
    "AutoMLCandidateGenerationConfigTypeDef",
    {
        "FeatureSpecificationS3Uri": str,
        "AlgorithmsConfig": Sequence[AutoMLAlgorithmConfigTypeDef],
    },
    total=False,
)

CandidateGenerationConfigTypeDef = TypedDict(
    "CandidateGenerationConfigTypeDef",
    {
        "AlgorithmsConfig": Sequence[AutoMLAlgorithmConfigTypeDef],
    },
    total=False,
)

AutoMLDataSourceTypeDef = TypedDict(
    "AutoMLDataSourceTypeDef",
    {
        "S3DataSource": AutoMLS3DataSourceTypeDef,
    },
)

ImageClassificationJobConfigTypeDef = TypedDict(
    "ImageClassificationJobConfigTypeDef",
    {
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
    },
    total=False,
)

TextClassificationJobConfigTypeDef = TypedDict(
    "TextClassificationJobConfigTypeDef",
    {
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
        "ContentColumn": str,
        "TargetLabelColumn": str,
    },
    total=False,
)

ResolvedAttributesTypeDef = TypedDict(
    "ResolvedAttributesTypeDef",
    {
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "ProblemType": ProblemTypeType,
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
    },
)

AutoMLJobSummaryTypeDef = TypedDict(
    "AutoMLJobSummaryTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "AutoMLJobStatus": AutoMLJobStatusType,
        "AutoMLJobSecondaryStatus": AutoMLJobSecondaryStatusType,
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "PartialFailureReasons": List[AutoMLPartialFailureReasonTypeDef],
    },
)

AutoMLProblemTypeResolvedAttributesTypeDef = TypedDict(
    "AutoMLProblemTypeResolvedAttributesTypeDef",
    {
        "TabularResolvedAttributes": TabularResolvedAttributesTypeDef,
    },
)

AutoMLSecurityConfigTypeDef = TypedDict(
    "AutoMLSecurityConfigTypeDef",
    {
        "VolumeKmsKeyId": str,
        "EnableInterContainerTrafficEncryption": bool,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

LabelingJobResourceConfigTypeDef = TypedDict(
    "LabelingJobResourceConfigTypeDef",
    {
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

MonitoringNetworkConfigTypeDef = TypedDict(
    "MonitoringNetworkConfigTypeDef",
    {
        "EnableInterContainerTrafficEncryption": bool,
        "EnableNetworkIsolation": bool,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

NetworkConfigTypeDef = TypedDict(
    "NetworkConfigTypeDef",
    {
        "EnableInterContainerTrafficEncryption": bool,
        "EnableNetworkIsolation": bool,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

BiasTypeDef = TypedDict(
    "BiasTypeDef",
    {
        "Report": MetricsSourceTypeDef,
        "PreTrainingReport": MetricsSourceTypeDef,
        "PostTrainingReport": MetricsSourceTypeDef,
    },
    total=False,
)

DriftCheckModelDataQualityTypeDef = TypedDict(
    "DriftCheckModelDataQualityTypeDef",
    {
        "Statistics": MetricsSourceTypeDef,
        "Constraints": MetricsSourceTypeDef,
    },
    total=False,
)

DriftCheckModelQualityTypeDef = TypedDict(
    "DriftCheckModelQualityTypeDef",
    {
        "Statistics": MetricsSourceTypeDef,
        "Constraints": MetricsSourceTypeDef,
    },
    total=False,
)

ExplainabilityTypeDef = TypedDict(
    "ExplainabilityTypeDef",
    {
        "Report": MetricsSourceTypeDef,
    },
    total=False,
)

ModelDataQualityTypeDef = TypedDict(
    "ModelDataQualityTypeDef",
    {
        "Statistics": MetricsSourceTypeDef,
        "Constraints": MetricsSourceTypeDef,
    },
    total=False,
)

ModelQualityTypeDef = TypedDict(
    "ModelQualityTypeDef",
    {
        "Statistics": MetricsSourceTypeDef,
        "Constraints": MetricsSourceTypeDef,
    },
    total=False,
)

CallbackStepMetadataTypeDef = TypedDict(
    "CallbackStepMetadataTypeDef",
    {
        "CallbackToken": str,
        "SqsQueueUrl": str,
        "OutputParameters": List[OutputParameterTypeDef],
    },
)

LambdaStepMetadataTypeDef = TypedDict(
    "LambdaStepMetadataTypeDef",
    {
        "Arn": str,
        "OutputParameters": List[OutputParameterTypeDef],
    },
)

_RequiredSendPipelineExecutionStepSuccessRequestRequestTypeDef = TypedDict(
    "_RequiredSendPipelineExecutionStepSuccessRequestRequestTypeDef",
    {
        "CallbackToken": str,
    },
)
_OptionalSendPipelineExecutionStepSuccessRequestRequestTypeDef = TypedDict(
    "_OptionalSendPipelineExecutionStepSuccessRequestRequestTypeDef",
    {
        "OutputParameters": Sequence[OutputParameterTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)


class SendPipelineExecutionStepSuccessRequestRequestTypeDef(
    _RequiredSendPipelineExecutionStepSuccessRequestRequestTypeDef,
    _OptionalSendPipelineExecutionStepSuccessRequestRequestTypeDef,
):
    pass


CandidatePropertiesTypeDef = TypedDict(
    "CandidatePropertiesTypeDef",
    {
        "CandidateArtifactLocations": CandidateArtifactLocationsTypeDef,
        "CandidateMetrics": List[MetricDatumTypeDef],
    },
)

CanvasAppSettingsTypeDef = TypedDict(
    "CanvasAppSettingsTypeDef",
    {
        "TimeSeriesForecastingSettings": TimeSeriesForecastingSettingsTypeDef,
        "ModelRegisterSettings": ModelRegisterSettingsTypeDef,
        "WorkspaceSettings": WorkspaceSettingsTypeDef,
    },
    total=False,
)

_RequiredRollingUpdatePolicyTypeDef = TypedDict(
    "_RequiredRollingUpdatePolicyTypeDef",
    {
        "MaximumBatchSize": CapacitySizeTypeDef,
        "WaitIntervalInSeconds": int,
    },
)
_OptionalRollingUpdatePolicyTypeDef = TypedDict(
    "_OptionalRollingUpdatePolicyTypeDef",
    {
        "MaximumExecutionTimeoutInSeconds": int,
        "RollbackMaximumBatchSize": CapacitySizeTypeDef,
    },
    total=False,
)


class RollingUpdatePolicyTypeDef(
    _RequiredRollingUpdatePolicyTypeDef, _OptionalRollingUpdatePolicyTypeDef
):
    pass


_RequiredTrafficRoutingConfigTypeDef = TypedDict(
    "_RequiredTrafficRoutingConfigTypeDef",
    {
        "Type": TrafficRoutingConfigTypeType,
        "WaitIntervalInSeconds": int,
    },
)
_OptionalTrafficRoutingConfigTypeDef = TypedDict(
    "_OptionalTrafficRoutingConfigTypeDef",
    {
        "CanarySize": CapacitySizeTypeDef,
        "LinearStepSize": CapacitySizeTypeDef,
    },
    total=False,
)


class TrafficRoutingConfigTypeDef(
    _RequiredTrafficRoutingConfigTypeDef, _OptionalTrafficRoutingConfigTypeDef
):
    pass


_RequiredInferenceExperimentDataStorageConfigTypeDef = TypedDict(
    "_RequiredInferenceExperimentDataStorageConfigTypeDef",
    {
        "Destination": str,
    },
)
_OptionalInferenceExperimentDataStorageConfigTypeDef = TypedDict(
    "_OptionalInferenceExperimentDataStorageConfigTypeDef",
    {
        "KmsKey": str,
        "ContentType": CaptureContentTypeHeaderTypeDef,
    },
    total=False,
)


class InferenceExperimentDataStorageConfigTypeDef(
    _RequiredInferenceExperimentDataStorageConfigTypeDef,
    _OptionalInferenceExperimentDataStorageConfigTypeDef,
):
    pass


_RequiredDataCaptureConfigTypeDef = TypedDict(
    "_RequiredDataCaptureConfigTypeDef",
    {
        "InitialSamplingPercentage": int,
        "DestinationS3Uri": str,
        "CaptureOptions": Sequence[CaptureOptionTypeDef],
    },
)
_OptionalDataCaptureConfigTypeDef = TypedDict(
    "_OptionalDataCaptureConfigTypeDef",
    {
        "EnableCapture": bool,
        "KmsKeyId": str,
        "CaptureContentTypeHeader": CaptureContentTypeHeaderTypeDef,
    },
    total=False,
)


class DataCaptureConfigTypeDef(
    _RequiredDataCaptureConfigTypeDef, _OptionalDataCaptureConfigTypeDef
):
    pass


EnvironmentParameterRangesTypeDef = TypedDict(
    "EnvironmentParameterRangesTypeDef",
    {
        "CategoricalParameterRanges": Sequence[CategoricalParameterTypeDef],
    },
    total=False,
)

_RequiredClarifyShapConfigTypeDef = TypedDict(
    "_RequiredClarifyShapConfigTypeDef",
    {
        "ShapBaselineConfig": ClarifyShapBaselineConfigTypeDef,
    },
)
_OptionalClarifyShapConfigTypeDef = TypedDict(
    "_OptionalClarifyShapConfigTypeDef",
    {
        "NumberOfSamples": int,
        "UseLogit": bool,
        "Seed": int,
        "TextConfig": ClarifyTextConfigTypeDef,
    },
    total=False,
)


class ClarifyShapConfigTypeDef(
    _RequiredClarifyShapConfigTypeDef, _OptionalClarifyShapConfigTypeDef
):
    pass


CodeRepositorySummaryTypeDef = TypedDict(
    "CodeRepositorySummaryTypeDef",
    {
        "CodeRepositoryName": str,
        "CodeRepositoryArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "GitConfig": GitConfigTypeDef,
    },
)

_RequiredCreateCodeRepositoryInputRequestTypeDef = TypedDict(
    "_RequiredCreateCodeRepositoryInputRequestTypeDef",
    {
        "CodeRepositoryName": str,
        "GitConfig": GitConfigTypeDef,
    },
)
_OptionalCreateCodeRepositoryInputRequestTypeDef = TypedDict(
    "_OptionalCreateCodeRepositoryInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateCodeRepositoryInputRequestTypeDef(
    _RequiredCreateCodeRepositoryInputRequestTypeDef,
    _OptionalCreateCodeRepositoryInputRequestTypeDef,
):
    pass


DescribeCodeRepositoryOutputTypeDef = TypedDict(
    "DescribeCodeRepositoryOutputTypeDef",
    {
        "CodeRepositoryName": str,
        "CodeRepositoryArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "GitConfig": GitConfigTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDebugHookConfigTypeDef = TypedDict(
    "_RequiredDebugHookConfigTypeDef",
    {
        "S3OutputPath": str,
    },
)
_OptionalDebugHookConfigTypeDef = TypedDict(
    "_OptionalDebugHookConfigTypeDef",
    {
        "LocalPath": str,
        "HookParameters": Mapping[str, str],
        "CollectionConfigurations": Sequence[CollectionConfigurationTypeDef],
    },
    total=False,
)


class DebugHookConfigTypeDef(_RequiredDebugHookConfigTypeDef, _OptionalDebugHookConfigTypeDef):
    pass


ListCompilationJobsResponseTypeDef = TypedDict(
    "ListCompilationJobsResponseTypeDef",
    {
        "CompilationJobSummaries": List[CompilationJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ContextSummaryTypeDef = TypedDict(
    "ContextSummaryTypeDef",
    {
        "ContextArn": str,
        "ContextName": str,
        "Source": ContextSourceTypeDef,
        "ContextType": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

_RequiredCreateContextRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContextRequestRequestTypeDef",
    {
        "ContextName": str,
        "Source": ContextSourceTypeDef,
        "ContextType": str,
    },
)
_OptionalCreateContextRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContextRequestRequestTypeDef",
    {
        "Description": str,
        "Properties": Mapping[str, str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateContextRequestRequestTypeDef(
    _RequiredCreateContextRequestRequestTypeDef, _OptionalCreateContextRequestRequestTypeDef
):
    pass


TuningJobCompletionCriteriaTypeDef = TypedDict(
    "TuningJobCompletionCriteriaTypeDef",
    {
        "TargetObjectiveMetricValue": float,
        "BestObjectiveNotImproving": BestObjectiveNotImprovingTypeDef,
        "ConvergenceDetected": ConvergenceDetectedTypeDef,
    },
    total=False,
)

_RequiredCreateActionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateActionRequestRequestTypeDef",
    {
        "ActionName": str,
        "Source": ActionSourceTypeDef,
        "ActionType": str,
    },
)
_OptionalCreateActionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateActionRequestRequestTypeDef",
    {
        "Description": str,
        "Status": ActionStatusType,
        "Properties": Mapping[str, str],
        "MetadataProperties": MetadataPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateActionRequestRequestTypeDef(
    _RequiredCreateActionRequestRequestTypeDef, _OptionalCreateActionRequestRequestTypeDef
):
    pass


_RequiredCreateTrialRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrialRequestRequestTypeDef",
    {
        "TrialName": str,
        "ExperimentName": str,
    },
)
_OptionalCreateTrialRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrialRequestRequestTypeDef",
    {
        "DisplayName": str,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateTrialRequestRequestTypeDef(
    _RequiredCreateTrialRequestRequestTypeDef, _OptionalCreateTrialRequestRequestTypeDef
):
    pass


_RequiredCreateAppRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppRequestRequestTypeDef",
    {
        "DomainId": str,
        "AppType": AppTypeType,
        "AppName": str,
    },
)
_OptionalCreateAppRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppRequestRequestTypeDef",
    {
        "UserProfileName": str,
        "Tags": Sequence[TagTypeDef],
        "ResourceSpec": ResourceSpecTypeDef,
        "SpaceName": str,
    },
    total=False,
)


class CreateAppRequestRequestTypeDef(
    _RequiredCreateAppRequestRequestTypeDef, _OptionalCreateAppRequestRequestTypeDef
):
    pass


DescribeAppResponseTypeDef = TypedDict(
    "DescribeAppResponseTypeDef",
    {
        "AppArn": str,
        "AppType": AppTypeType,
        "AppName": str,
        "DomainId": str,
        "UserProfileName": str,
        "Status": AppStatusType,
        "LastHealthCheckTimestamp": datetime,
        "LastUserActivityTimestamp": datetime,
        "CreationTime": datetime,
        "FailureReason": str,
        "ResourceSpec": ResourceSpecTypeDef,
        "SpaceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

JupyterServerAppSettingsTypeDef = TypedDict(
    "JupyterServerAppSettingsTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecTypeDef,
        "LifecycleConfigArns": Sequence[str],
        "CodeRepositories": Sequence[CodeRepositoryTypeDef],
    },
    total=False,
)

_RequiredRStudioServerProDomainSettingsForUpdateTypeDef = TypedDict(
    "_RequiredRStudioServerProDomainSettingsForUpdateTypeDef",
    {
        "DomainExecutionRoleArn": str,
    },
)
_OptionalRStudioServerProDomainSettingsForUpdateTypeDef = TypedDict(
    "_OptionalRStudioServerProDomainSettingsForUpdateTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecTypeDef,
        "RStudioConnectUrl": str,
        "RStudioPackageManagerUrl": str,
    },
    total=False,
)


class RStudioServerProDomainSettingsForUpdateTypeDef(
    _RequiredRStudioServerProDomainSettingsForUpdateTypeDef,
    _OptionalRStudioServerProDomainSettingsForUpdateTypeDef,
):
    pass


_RequiredRStudioServerProDomainSettingsTypeDef = TypedDict(
    "_RequiredRStudioServerProDomainSettingsTypeDef",
    {
        "DomainExecutionRoleArn": str,
    },
)
_OptionalRStudioServerProDomainSettingsTypeDef = TypedDict(
    "_OptionalRStudioServerProDomainSettingsTypeDef",
    {
        "RStudioConnectUrl": str,
        "RStudioPackageManagerUrl": str,
        "DefaultResourceSpec": ResourceSpecTypeDef,
    },
    total=False,
)


class RStudioServerProDomainSettingsTypeDef(
    _RequiredRStudioServerProDomainSettingsTypeDef, _OptionalRStudioServerProDomainSettingsTypeDef
):
    pass


TensorBoardAppSettingsTypeDef = TypedDict(
    "TensorBoardAppSettingsTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecTypeDef,
    },
    total=False,
)

_RequiredCreateDeviceFleetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeviceFleetRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
        "OutputConfig": EdgeOutputConfigTypeDef,
    },
)
_OptionalCreateDeviceFleetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeviceFleetRequestRequestTypeDef",
    {
        "RoleArn": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "EnableIotRoleAlias": bool,
    },
    total=False,
)


class CreateDeviceFleetRequestRequestTypeDef(
    _RequiredCreateDeviceFleetRequestRequestTypeDef, _OptionalCreateDeviceFleetRequestRequestTypeDef
):
    pass


_RequiredCreateEdgePackagingJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEdgePackagingJobRequestRequestTypeDef",
    {
        "EdgePackagingJobName": str,
        "CompilationJobName": str,
        "ModelName": str,
        "ModelVersion": str,
        "RoleArn": str,
        "OutputConfig": EdgeOutputConfigTypeDef,
    },
)
_OptionalCreateEdgePackagingJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEdgePackagingJobRequestRequestTypeDef",
    {
        "ResourceKey": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEdgePackagingJobRequestRequestTypeDef(
    _RequiredCreateEdgePackagingJobRequestRequestTypeDef,
    _OptionalCreateEdgePackagingJobRequestRequestTypeDef,
):
    pass


DescribeDeviceFleetResponseTypeDef = TypedDict(
    "DescribeDeviceFleetResponseTypeDef",
    {
        "DeviceFleetName": str,
        "DeviceFleetArn": str,
        "OutputConfig": EdgeOutputConfigTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
        "IotRoleAlias": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateDeviceFleetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDeviceFleetRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
        "OutputConfig": EdgeOutputConfigTypeDef,
    },
)
_OptionalUpdateDeviceFleetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDeviceFleetRequestRequestTypeDef",
    {
        "RoleArn": str,
        "Description": str,
        "EnableIotRoleAlias": bool,
    },
    total=False,
)


class UpdateDeviceFleetRequestRequestTypeDef(
    _RequiredUpdateDeviceFleetRequestRequestTypeDef, _OptionalUpdateDeviceFleetRequestRequestTypeDef
):
    pass


_RequiredCreateHubRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHubRequestRequestTypeDef",
    {
        "HubName": str,
        "HubDescription": str,
    },
)
_OptionalCreateHubRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHubRequestRequestTypeDef",
    {
        "HubDisplayName": str,
        "HubSearchKeywords": Sequence[str],
        "S3StorageConfig": HubS3StorageConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateHubRequestRequestTypeDef(
    _RequiredCreateHubRequestRequestTypeDef, _OptionalCreateHubRequestRequestTypeDef
):
    pass


DescribeHubResponseTypeDef = TypedDict(
    "DescribeHubResponseTypeDef",
    {
        "HubName": str,
        "HubArn": str,
        "HubDisplayName": str,
        "HubDescription": str,
        "HubSearchKeywords": List[str],
        "S3StorageConfig": HubS3StorageConfigTypeDef,
        "HubStatus": HubStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateHumanTaskUiRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHumanTaskUiRequestRequestTypeDef",
    {
        "HumanTaskUiName": str,
        "UiTemplate": UiTemplateTypeDef,
    },
)
_OptionalCreateHumanTaskUiRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHumanTaskUiRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateHumanTaskUiRequestRequestTypeDef(
    _RequiredCreateHumanTaskUiRequestRequestTypeDef, _OptionalCreateHumanTaskUiRequestRequestTypeDef
):
    pass


InferenceExperimentSummaryTypeDef = TypedDict(
    "InferenceExperimentSummaryTypeDef",
    {
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Schedule": InferenceExperimentScheduleTypeDef,
        "Status": InferenceExperimentStatusType,
        "StatusReason": str,
        "Description": str,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
    },
)

_RequiredCreateModelCardExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateModelCardExportJobRequestRequestTypeDef",
    {
        "ModelCardName": str,
        "ModelCardExportJobName": str,
        "OutputConfig": ModelCardExportOutputConfigTypeDef,
    },
)
_OptionalCreateModelCardExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateModelCardExportJobRequestRequestTypeDef",
    {
        "ModelCardVersion": int,
    },
    total=False,
)


class CreateModelCardExportJobRequestRequestTypeDef(
    _RequiredCreateModelCardExportJobRequestRequestTypeDef,
    _OptionalCreateModelCardExportJobRequestRequestTypeDef,
):
    pass


_RequiredCreateModelCardRequestRequestTypeDef = TypedDict(
    "_RequiredCreateModelCardRequestRequestTypeDef",
    {
        "ModelCardName": str,
        "Content": str,
        "ModelCardStatus": ModelCardStatusType,
    },
)
_OptionalCreateModelCardRequestRequestTypeDef = TypedDict(
    "_OptionalCreateModelCardRequestRequestTypeDef",
    {
        "SecurityConfig": ModelCardSecurityConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateModelCardRequestRequestTypeDef(
    _RequiredCreateModelCardRequestRequestTypeDef, _OptionalCreateModelCardRequestRequestTypeDef
):
    pass


_RequiredCreateNotebookInstanceInputRequestTypeDef = TypedDict(
    "_RequiredCreateNotebookInstanceInputRequestTypeDef",
    {
        "NotebookInstanceName": str,
        "InstanceType": InstanceTypeType,
        "RoleArn": str,
    },
)
_OptionalCreateNotebookInstanceInputRequestTypeDef = TypedDict(
    "_OptionalCreateNotebookInstanceInputRequestTypeDef",
    {
        "SubnetId": str,
        "SecurityGroupIds": Sequence[str],
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
        "LifecycleConfigName": str,
        "DirectInternetAccess": DirectInternetAccessType,
        "VolumeSizeInGB": int,
        "AcceleratorTypes": Sequence[NotebookInstanceAcceleratorTypeType],
        "DefaultCodeRepository": str,
        "AdditionalCodeRepositories": Sequence[str],
        "RootAccess": RootAccessType,
        "PlatformIdentifier": str,
        "InstanceMetadataServiceConfiguration": InstanceMetadataServiceConfigurationTypeDef,
    },
    total=False,
)


class CreateNotebookInstanceInputRequestTypeDef(
    _RequiredCreateNotebookInstanceInputRequestTypeDef,
    _OptionalCreateNotebookInstanceInputRequestTypeDef,
):
    pass


DescribeNotebookInstanceOutputTypeDef = TypedDict(
    "DescribeNotebookInstanceOutputTypeDef",
    {
        "NotebookInstanceArn": str,
        "NotebookInstanceName": str,
        "NotebookInstanceStatus": NotebookInstanceStatusType,
        "FailureReason": str,
        "Url": str,
        "InstanceType": InstanceTypeType,
        "SubnetId": str,
        "SecurityGroups": List[str],
        "RoleArn": str,
        "KmsKeyId": str,
        "NetworkInterfaceId": str,
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "NotebookInstanceLifecycleConfigName": str,
        "DirectInternetAccess": DirectInternetAccessType,
        "VolumeSizeInGB": int,
        "AcceleratorTypes": List[NotebookInstanceAcceleratorTypeType],
        "DefaultCodeRepository": str,
        "AdditionalCodeRepositories": List[str],
        "RootAccess": RootAccessType,
        "PlatformIdentifier": str,
        "InstanceMetadataServiceConfiguration": InstanceMetadataServiceConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateNotebookInstanceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateNotebookInstanceInputRequestTypeDef",
    {
        "NotebookInstanceName": str,
    },
)
_OptionalUpdateNotebookInstanceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateNotebookInstanceInputRequestTypeDef",
    {
        "InstanceType": InstanceTypeType,
        "RoleArn": str,
        "LifecycleConfigName": str,
        "DisassociateLifecycleConfig": bool,
        "VolumeSizeInGB": int,
        "DefaultCodeRepository": str,
        "AdditionalCodeRepositories": Sequence[str],
        "AcceleratorTypes": Sequence[NotebookInstanceAcceleratorTypeType],
        "DisassociateAcceleratorTypes": bool,
        "DisassociateDefaultCodeRepository": bool,
        "DisassociateAdditionalCodeRepositories": bool,
        "RootAccess": RootAccessType,
        "InstanceMetadataServiceConfiguration": InstanceMetadataServiceConfigurationTypeDef,
    },
    total=False,
)


class UpdateNotebookInstanceInputRequestTypeDef(
    _RequiredUpdateNotebookInstanceInputRequestTypeDef,
    _OptionalUpdateNotebookInstanceInputRequestTypeDef,
):
    pass


_RequiredCreateNotebookInstanceLifecycleConfigInputRequestTypeDef = TypedDict(
    "_RequiredCreateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    {
        "NotebookInstanceLifecycleConfigName": str,
    },
)
_OptionalCreateNotebookInstanceLifecycleConfigInputRequestTypeDef = TypedDict(
    "_OptionalCreateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    {
        "OnCreate": Sequence[NotebookInstanceLifecycleHookTypeDef],
        "OnStart": Sequence[NotebookInstanceLifecycleHookTypeDef],
    },
    total=False,
)


class CreateNotebookInstanceLifecycleConfigInputRequestTypeDef(
    _RequiredCreateNotebookInstanceLifecycleConfigInputRequestTypeDef,
    _OptionalCreateNotebookInstanceLifecycleConfigInputRequestTypeDef,
):
    pass


DescribeNotebookInstanceLifecycleConfigOutputTypeDef = TypedDict(
    "DescribeNotebookInstanceLifecycleConfigOutputTypeDef",
    {
        "NotebookInstanceLifecycleConfigArn": str,
        "NotebookInstanceLifecycleConfigName": str,
        "OnCreate": List[NotebookInstanceLifecycleHookTypeDef],
        "OnStart": List[NotebookInstanceLifecycleHookTypeDef],
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateNotebookInstanceLifecycleConfigInputRequestTypeDef = TypedDict(
    "_RequiredUpdateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    {
        "NotebookInstanceLifecycleConfigName": str,
    },
)
_OptionalUpdateNotebookInstanceLifecycleConfigInputRequestTypeDef = TypedDict(
    "_OptionalUpdateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    {
        "OnCreate": Sequence[NotebookInstanceLifecycleHookTypeDef],
        "OnStart": Sequence[NotebookInstanceLifecycleHookTypeDef],
    },
    total=False,
)


class UpdateNotebookInstanceLifecycleConfigInputRequestTypeDef(
    _RequiredUpdateNotebookInstanceLifecycleConfigInputRequestTypeDef,
    _OptionalUpdateNotebookInstanceLifecycleConfigInputRequestTypeDef,
):
    pass


_RequiredRetryPipelineExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredRetryPipelineExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
        "ClientRequestToken": str,
    },
)
_OptionalRetryPipelineExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalRetryPipelineExecutionRequestRequestTypeDef",
    {
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
    },
    total=False,
)


class RetryPipelineExecutionRequestRequestTypeDef(
    _RequiredRetryPipelineExecutionRequestRequestTypeDef,
    _OptionalRetryPipelineExecutionRequestRequestTypeDef,
):
    pass


_RequiredUpdatePipelineExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePipelineExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
    },
)
_OptionalUpdatePipelineExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePipelineExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionDescription": str,
        "PipelineExecutionDisplayName": str,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
    },
    total=False,
)


class UpdatePipelineExecutionRequestRequestTypeDef(
    _RequiredUpdatePipelineExecutionRequestRequestTypeDef,
    _OptionalUpdatePipelineExecutionRequestRequestTypeDef,
):
    pass


_RequiredCreatePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
        "ClientRequestToken": str,
        "RoleArn": str,
    },
)
_OptionalCreatePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePipelineRequestRequestTypeDef",
    {
        "PipelineDisplayName": str,
        "PipelineDefinition": str,
        "PipelineDefinitionS3Location": PipelineDefinitionS3LocationTypeDef,
        "PipelineDescription": str,
        "Tags": Sequence[TagTypeDef],
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
    },
    total=False,
)


class CreatePipelineRequestRequestTypeDef(
    _RequiredCreatePipelineRequestRequestTypeDef, _OptionalCreatePipelineRequestRequestTypeDef
):
    pass


_RequiredUpdatePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)
_OptionalUpdatePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePipelineRequestRequestTypeDef",
    {
        "PipelineDisplayName": str,
        "PipelineDefinition": str,
        "PipelineDefinitionS3Location": PipelineDefinitionS3LocationTypeDef,
        "PipelineDescription": str,
        "RoleArn": str,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
    },
    total=False,
)


class UpdatePipelineRequestRequestTypeDef(
    _RequiredUpdatePipelineRequestRequestTypeDef, _OptionalUpdatePipelineRequestRequestTypeDef
):
    pass


_RequiredCreateTrialComponentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrialComponentRequestRequestTypeDef",
    {
        "TrialComponentName": str,
    },
)
_OptionalCreateTrialComponentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrialComponentRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Parameters": Mapping[str, TrialComponentParameterValueTypeDef],
        "InputArtifacts": Mapping[str, TrialComponentArtifactTypeDef],
        "OutputArtifacts": Mapping[str, TrialComponentArtifactTypeDef],
        "MetadataProperties": MetadataPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateTrialComponentRequestRequestTypeDef(
    _RequiredCreateTrialComponentRequestRequestTypeDef,
    _OptionalCreateTrialComponentRequestRequestTypeDef,
):
    pass


_RequiredUpdateTrialComponentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrialComponentRequestRequestTypeDef",
    {
        "TrialComponentName": str,
    },
)
_OptionalUpdateTrialComponentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrialComponentRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Parameters": Mapping[str, TrialComponentParameterValueTypeDef],
        "ParametersToRemove": Sequence[str],
        "InputArtifacts": Mapping[str, TrialComponentArtifactTypeDef],
        "InputArtifactsToRemove": Sequence[str],
        "OutputArtifacts": Mapping[str, TrialComponentArtifactTypeDef],
        "OutputArtifactsToRemove": Sequence[str],
    },
    total=False,
)


class UpdateTrialComponentRequestRequestTypeDef(
    _RequiredUpdateTrialComponentRequestRequestTypeDef,
    _OptionalUpdateTrialComponentRequestRequestTypeDef,
):
    pass


_RequiredCreateWorkforceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkforceRequestRequestTypeDef",
    {
        "WorkforceName": str,
    },
)
_OptionalCreateWorkforceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkforceRequestRequestTypeDef",
    {
        "CognitoConfig": CognitoConfigTypeDef,
        "OidcConfig": OidcConfigTypeDef,
        "SourceIpConfig": SourceIpConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "WorkforceVpcConfig": WorkforceVpcConfigRequestTypeDef,
    },
    total=False,
)


class CreateWorkforceRequestRequestTypeDef(
    _RequiredCreateWorkforceRequestRequestTypeDef, _OptionalCreateWorkforceRequestRequestTypeDef
):
    pass


_RequiredUpdateWorkforceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkforceRequestRequestTypeDef",
    {
        "WorkforceName": str,
    },
)
_OptionalUpdateWorkforceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkforceRequestRequestTypeDef",
    {
        "SourceIpConfig": SourceIpConfigTypeDef,
        "OidcConfig": OidcConfigTypeDef,
        "WorkforceVpcConfig": WorkforceVpcConfigRequestTypeDef,
    },
    total=False,
)


class UpdateWorkforceRequestRequestTypeDef(
    _RequiredUpdateWorkforceRequestRequestTypeDef, _OptionalUpdateWorkforceRequestRequestTypeDef
):
    pass


KernelGatewayAppSettingsTypeDef = TypedDict(
    "KernelGatewayAppSettingsTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecTypeDef,
        "CustomImages": Sequence[CustomImageTypeDef],
        "LifecycleConfigArns": Sequence[str],
    },
    total=False,
)

RSessionAppSettingsTypeDef = TypedDict(
    "RSessionAppSettingsTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecTypeDef,
        "CustomImages": Sequence[CustomImageTypeDef],
    },
    total=False,
)

ModelBiasBaselineConfigTypeDef = TypedDict(
    "ModelBiasBaselineConfigTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceTypeDef,
    },
    total=False,
)

ModelExplainabilityBaselineConfigTypeDef = TypedDict(
    "ModelExplainabilityBaselineConfigTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceTypeDef,
    },
    total=False,
)

ModelQualityBaselineConfigTypeDef = TypedDict(
    "ModelQualityBaselineConfigTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceTypeDef,
    },
    total=False,
)

DataQualityBaselineConfigTypeDef = TypedDict(
    "DataQualityBaselineConfigTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceTypeDef,
        "StatisticsResource": MonitoringStatisticsResourceTypeDef,
    },
    total=False,
)

MonitoringBaselineConfigTypeDef = TypedDict(
    "MonitoringBaselineConfigTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceTypeDef,
        "StatisticsResource": MonitoringStatisticsResourceTypeDef,
    },
    total=False,
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "S3DataSource": S3DataSourceTypeDef,
        "FileSystemDataSource": FileSystemDataSourceTypeDef,
    },
    total=False,
)

DatasetDefinitionTypeDef = TypedDict(
    "DatasetDefinitionTypeDef",
    {
        "AthenaDatasetDefinition": AthenaDatasetDefinitionTypeDef,
        "RedshiftDatasetDefinition": RedshiftDatasetDefinitionTypeDef,
        "LocalPath": str,
        "DataDistributionType": DataDistributionTypeType,
        "InputMode": InputModeType,
    },
    total=False,
)

_RequiredDeleteDomainRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDomainRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalDeleteDomainRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDomainRequestRequestTypeDef",
    {
        "RetentionPolicy": RetentionPolicyTypeDef,
    },
    total=False,
)


class DeleteDomainRequestRequestTypeDef(
    _RequiredDeleteDomainRequestRequestTypeDef, _OptionalDeleteDomainRequestRequestTypeDef
):
    pass


DeploymentRecommendationTypeDef = TypedDict(
    "DeploymentRecommendationTypeDef",
    {
        "RecommendationStatus": RecommendationStatusType,
        "RealTimeInferenceRecommendations": List[RealTimeInferenceRecommendationTypeDef],
    },
)

_RequiredDeploymentStageTypeDef = TypedDict(
    "_RequiredDeploymentStageTypeDef",
    {
        "StageName": str,
        "DeviceSelectionConfig": DeviceSelectionConfigTypeDef,
    },
)
_OptionalDeploymentStageTypeDef = TypedDict(
    "_OptionalDeploymentStageTypeDef",
    {
        "DeploymentConfig": EdgeDeploymentConfigTypeDef,
    },
    total=False,
)


class DeploymentStageTypeDef(_RequiredDeploymentStageTypeDef, _OptionalDeploymentStageTypeDef):
    pass


DeploymentStageStatusSummaryTypeDef = TypedDict(
    "DeploymentStageStatusSummaryTypeDef",
    {
        "StageName": str,
        "DeviceSelectionConfig": DeviceSelectionConfigTypeDef,
        "DeploymentConfig": EdgeDeploymentConfigTypeDef,
        "DeploymentStatus": EdgeDeploymentStatusTypeDef,
    },
)

DescribeDeviceResponseTypeDef = TypedDict(
    "DescribeDeviceResponseTypeDef",
    {
        "DeviceArn": str,
        "DeviceName": str,
        "Description": str,
        "DeviceFleetName": str,
        "IotThingName": str,
        "RegistrationTime": datetime,
        "LatestHeartbeat": datetime,
        "Models": List[EdgeModelTypeDef],
        "MaxModels": int,
        "NextToken": str,
        "AgentVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEdgePackagingJobResponseTypeDef = TypedDict(
    "DescribeEdgePackagingJobResponseTypeDef",
    {
        "EdgePackagingJobArn": str,
        "EdgePackagingJobName": str,
        "CompilationJobName": str,
        "ModelName": str,
        "ModelVersion": str,
        "RoleArn": str,
        "OutputConfig": EdgeOutputConfigTypeDef,
        "ResourceKey": str,
        "EdgePackagingJobStatus": EdgePackagingJobStatusType,
        "EdgePackagingJobStatusMessage": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ModelArtifact": str,
        "ModelSignature": str,
        "PresetDeploymentOutput": EdgePresetDeploymentOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeEndpointInputEndpointDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeEndpointInputEndpointDeletedWaitTypeDef",
    {
        "EndpointName": str,
    },
)
_OptionalDescribeEndpointInputEndpointDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeEndpointInputEndpointDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeEndpointInputEndpointDeletedWaitTypeDef(
    _RequiredDescribeEndpointInputEndpointDeletedWaitTypeDef,
    _OptionalDescribeEndpointInputEndpointDeletedWaitTypeDef,
):
    pass


_RequiredDescribeEndpointInputEndpointInServiceWaitTypeDef = TypedDict(
    "_RequiredDescribeEndpointInputEndpointInServiceWaitTypeDef",
    {
        "EndpointName": str,
    },
)
_OptionalDescribeEndpointInputEndpointInServiceWaitTypeDef = TypedDict(
    "_OptionalDescribeEndpointInputEndpointInServiceWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeEndpointInputEndpointInServiceWaitTypeDef(
    _RequiredDescribeEndpointInputEndpointInServiceWaitTypeDef,
    _OptionalDescribeEndpointInputEndpointInServiceWaitTypeDef,
):
    pass


_RequiredDescribeImageRequestImageCreatedWaitTypeDef = TypedDict(
    "_RequiredDescribeImageRequestImageCreatedWaitTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalDescribeImageRequestImageCreatedWaitTypeDef = TypedDict(
    "_OptionalDescribeImageRequestImageCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeImageRequestImageCreatedWaitTypeDef(
    _RequiredDescribeImageRequestImageCreatedWaitTypeDef,
    _OptionalDescribeImageRequestImageCreatedWaitTypeDef,
):
    pass


_RequiredDescribeImageRequestImageDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeImageRequestImageDeletedWaitTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalDescribeImageRequestImageDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeImageRequestImageDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeImageRequestImageDeletedWaitTypeDef(
    _RequiredDescribeImageRequestImageDeletedWaitTypeDef,
    _OptionalDescribeImageRequestImageDeletedWaitTypeDef,
):
    pass


_RequiredDescribeImageRequestImageUpdatedWaitTypeDef = TypedDict(
    "_RequiredDescribeImageRequestImageUpdatedWaitTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalDescribeImageRequestImageUpdatedWaitTypeDef = TypedDict(
    "_OptionalDescribeImageRequestImageUpdatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeImageRequestImageUpdatedWaitTypeDef(
    _RequiredDescribeImageRequestImageUpdatedWaitTypeDef,
    _OptionalDescribeImageRequestImageUpdatedWaitTypeDef,
):
    pass


_RequiredDescribeImageVersionRequestImageVersionCreatedWaitTypeDef = TypedDict(
    "_RequiredDescribeImageVersionRequestImageVersionCreatedWaitTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalDescribeImageVersionRequestImageVersionCreatedWaitTypeDef = TypedDict(
    "_OptionalDescribeImageVersionRequestImageVersionCreatedWaitTypeDef",
    {
        "Version": int,
        "Alias": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeImageVersionRequestImageVersionCreatedWaitTypeDef(
    _RequiredDescribeImageVersionRequestImageVersionCreatedWaitTypeDef,
    _OptionalDescribeImageVersionRequestImageVersionCreatedWaitTypeDef,
):
    pass


_RequiredDescribeImageVersionRequestImageVersionDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeImageVersionRequestImageVersionDeletedWaitTypeDef",
    {
        "ImageName": str,
    },
)
_OptionalDescribeImageVersionRequestImageVersionDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeImageVersionRequestImageVersionDeletedWaitTypeDef",
    {
        "Version": int,
        "Alias": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeImageVersionRequestImageVersionDeletedWaitTypeDef(
    _RequiredDescribeImageVersionRequestImageVersionDeletedWaitTypeDef,
    _OptionalDescribeImageVersionRequestImageVersionDeletedWaitTypeDef,
):
    pass


_RequiredDescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef",
    {
        "NotebookInstanceName": str,
    },
)
_OptionalDescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef(
    _RequiredDescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef,
    _OptionalDescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef,
):
    pass


_RequiredDescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef = TypedDict(
    "_RequiredDescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef",
    {
        "NotebookInstanceName": str,
    },
)
_OptionalDescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef = TypedDict(
    "_OptionalDescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef(
    _RequiredDescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef,
    _OptionalDescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef,
):
    pass


_RequiredDescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef = TypedDict(
    "_RequiredDescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef",
    {
        "NotebookInstanceName": str,
    },
)
_OptionalDescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef = TypedDict(
    "_OptionalDescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef(
    _RequiredDescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef,
    _OptionalDescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef,
):
    pass


_RequiredDescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef = TypedDict(
    "_RequiredDescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef",
    {
        "ProcessingJobName": str,
    },
)
_OptionalDescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef = TypedDict(
    "_OptionalDescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef(
    _RequiredDescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef,
    _OptionalDescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef,
):
    pass


_RequiredDescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef = TypedDict(
    "_RequiredDescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef",
    {
        "TrainingJobName": str,
    },
)
_OptionalDescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef = TypedDict(
    "_OptionalDescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef(
    _RequiredDescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef,
    _OptionalDescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef,
):
    pass


_RequiredDescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef = TypedDict(
    "_RequiredDescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef",
    {
        "TransformJobName": str,
    },
)
_OptionalDescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef = TypedDict(
    "_OptionalDescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef(
    _RequiredDescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef,
    _OptionalDescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef,
):
    pass


ExperimentSummaryTypeDef = TypedDict(
    "ExperimentSummaryTypeDef",
    {
        "ExperimentArn": str,
        "ExperimentName": str,
        "DisplayName": str,
        "ExperimentSource": ExperimentSourceTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

FeatureGroupSummaryTypeDef = TypedDict(
    "FeatureGroupSummaryTypeDef",
    {
        "FeatureGroupName": str,
        "FeatureGroupArn": str,
        "CreationTime": datetime,
        "FeatureGroupStatus": FeatureGroupStatusType,
        "OfflineStoreStatus": OfflineStoreStatusTypeDef,
    },
)

DescribeFeatureMetadataResponseTypeDef = TypedDict(
    "DescribeFeatureMetadataResponseTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "FeatureName": str,
        "FeatureType": FeatureTypeType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Description": str,
        "Parameters": List[FeatureParameterTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FeatureMetadataTypeDef = TypedDict(
    "FeatureMetadataTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "FeatureName": str,
        "FeatureType": FeatureTypeType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Description": str,
        "Parameters": List[FeatureParameterTypeDef],
    },
)

_RequiredUpdateFeatureMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFeatureMetadataRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
        "FeatureName": str,
    },
)
_OptionalUpdateFeatureMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFeatureMetadataRequestRequestTypeDef",
    {
        "Description": str,
        "ParameterAdditions": Sequence[FeatureParameterTypeDef],
        "ParameterRemovals": Sequence[str],
    },
    total=False,
)


class UpdateFeatureMetadataRequestRequestTypeDef(
    _RequiredUpdateFeatureMetadataRequestRequestTypeDef,
    _OptionalUpdateFeatureMetadataRequestRequestTypeDef,
):
    pass


DescribeHubContentResponseTypeDef = TypedDict(
    "DescribeHubContentResponseTypeDef",
    {
        "HubContentName": str,
        "HubContentArn": str,
        "HubContentVersion": str,
        "HubContentType": HubContentTypeType,
        "DocumentSchemaVersion": str,
        "HubName": str,
        "HubArn": str,
        "HubContentDisplayName": str,
        "HubContentDescription": str,
        "HubContentMarkdown": str,
        "HubContentDocument": str,
        "HubContentSearchKeywords": List[str],
        "HubContentDependencies": List[HubContentDependencyTypeDef],
        "HubContentStatus": HubContentStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeHumanTaskUiResponseTypeDef = TypedDict(
    "DescribeHumanTaskUiResponseTypeDef",
    {
        "HumanTaskUiArn": str,
        "HumanTaskUiName": str,
        "HumanTaskUiStatus": HumanTaskUiStatusType,
        "CreationTime": datetime,
        "UiTemplate": UiTemplateInfoTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelCardExportJobResponseTypeDef = TypedDict(
    "DescribeModelCardExportJobResponseTypeDef",
    {
        "ModelCardExportJobName": str,
        "ModelCardExportJobArn": str,
        "Status": ModelCardExportJobStatusType,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "OutputConfig": ModelCardExportOutputConfigTypeDef,
        "CreatedAt": datetime,
        "LastModifiedAt": datetime,
        "FailureReason": str,
        "ExportArtifacts": ModelCardExportArtifactsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringExecutionsResponseTypeDef = TypedDict(
    "ListMonitoringExecutionsResponseTypeDef",
    {
        "MonitoringExecutionSummaries": List[MonitoringExecutionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSubscribedWorkteamResponseTypeDef = TypedDict(
    "DescribeSubscribedWorkteamResponseTypeDef",
    {
        "SubscribedWorkteam": SubscribedWorkteamTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSubscribedWorkteamsResponseTypeDef = TypedDict(
    "ListSubscribedWorkteamsResponseTypeDef",
    {
        "SubscribedWorkteams": List[SubscribedWorkteamTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TrainingJobSummaryTypeDef = TypedDict(
    "TrainingJobSummaryTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "CreationTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatus": TrainingJobStatusType,
        "WarmPoolStatus": WarmPoolStatusTypeDef,
    },
)

TrialSummaryTypeDef = TypedDict(
    "TrialSummaryTypeDef",
    {
        "TrialArn": str,
        "TrialName": str,
        "DisplayName": str,
        "TrialSource": TrialSourceTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

_RequiredDesiredWeightAndCapacityTypeDef = TypedDict(
    "_RequiredDesiredWeightAndCapacityTypeDef",
    {
        "VariantName": str,
    },
)
_OptionalDesiredWeightAndCapacityTypeDef = TypedDict(
    "_OptionalDesiredWeightAndCapacityTypeDef",
    {
        "DesiredWeight": float,
        "DesiredInstanceCount": int,
        "ServerlessUpdateConfig": ProductionVariantServerlessUpdateConfigTypeDef,
    },
    total=False,
)


class DesiredWeightAndCapacityTypeDef(
    _RequiredDesiredWeightAndCapacityTypeDef, _OptionalDesiredWeightAndCapacityTypeDef
):
    pass


ListStageDevicesResponseTypeDef = TypedDict(
    "ListStageDevicesResponseTypeDef",
    {
        "DeviceDeploymentSummaries": List[DeviceDeploymentSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDeviceFleetsResponseTypeDef = TypedDict(
    "ListDeviceFleetsResponseTypeDef",
    {
        "DeviceFleetSummaries": List[DeviceFleetSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeviceSummaryTypeDef = TypedDict(
    "DeviceSummaryTypeDef",
    {
        "DeviceName": str,
        "DeviceArn": str,
        "Description": str,
        "DeviceFleetName": str,
        "IotThingName": str,
        "RegistrationTime": datetime,
        "LatestHeartbeat": datetime,
        "Models": List[EdgeModelSummaryTypeDef],
        "AgentVersion": str,
    },
)

_RequiredRegisterDevicesRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterDevicesRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
        "Devices": Sequence[DeviceTypeDef],
    },
)
_OptionalRegisterDevicesRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterDevicesRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class RegisterDevicesRequestRequestTypeDef(
    _RequiredRegisterDevicesRequestRequestTypeDef, _OptionalRegisterDevicesRequestRequestTypeDef
):
    pass


UpdateDevicesRequestRequestTypeDef = TypedDict(
    "UpdateDevicesRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
        "Devices": Sequence[DeviceTypeDef],
    },
)

ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {
        "Domains": List[DomainDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DriftCheckBiasTypeDef = TypedDict(
    "DriftCheckBiasTypeDef",
    {
        "ConfigFile": FileSourceTypeDef,
        "PreTrainingConstraints": MetricsSourceTypeDef,
        "PostTrainingConstraints": MetricsSourceTypeDef,
    },
    total=False,
)

DriftCheckExplainabilityTypeDef = TypedDict(
    "DriftCheckExplainabilityTypeDef",
    {
        "Constraints": MetricsSourceTypeDef,
        "ConfigFile": FileSourceTypeDef,
    },
    total=False,
)

ListEdgeDeploymentPlansResponseTypeDef = TypedDict(
    "ListEdgeDeploymentPlansResponseTypeDef",
    {
        "EdgeDeploymentPlanSummaries": List[EdgeDeploymentPlanSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDeviceFleetReportResponseTypeDef = TypedDict(
    "GetDeviceFleetReportResponseTypeDef",
    {
        "DeviceFleetArn": str,
        "DeviceFleetName": str,
        "OutputConfig": EdgeOutputConfigTypeDef,
        "Description": str,
        "ReportGenerated": datetime,
        "DeviceStats": DeviceStatsTypeDef,
        "AgentVersions": List[AgentVersionTypeDef],
        "ModelStats": List[EdgeModelStatTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEdgePackagingJobsResponseTypeDef = TypedDict(
    "ListEdgePackagingJobsResponseTypeDef",
    {
        "EdgePackagingJobSummaries": List[EdgePackagingJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEndpointConfigsOutputTypeDef = TypedDict(
    "ListEndpointConfigsOutputTypeDef",
    {
        "EndpointConfigs": List[EndpointConfigSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EndpointOutputConfigurationTypeDef = TypedDict(
    "EndpointOutputConfigurationTypeDef",
    {
        "EndpointName": str,
        "VariantName": str,
        "InstanceType": ProductionVariantInstanceTypeType,
        "InitialInstanceCount": int,
        "ServerlessConfig": ProductionVariantServerlessConfigTypeDef,
    },
)

EndpointPerformanceTypeDef = TypedDict(
    "EndpointPerformanceTypeDef",
    {
        "Metrics": InferenceMetricsTypeDef,
        "EndpointInfo": EndpointInfoTypeDef,
    },
)

ListEndpointsOutputTypeDef = TypedDict(
    "ListEndpointsOutputTypeDef",
    {
        "Endpoints": List[EndpointSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelConfigurationTypeDef = TypedDict(
    "ModelConfigurationTypeDef",
    {
        "InferenceSpecificationName": str,
        "EnvironmentParameters": List[EnvironmentParameterTypeDef],
        "CompilationJobName": str,
    },
)

NestedFiltersTypeDef = TypedDict(
    "NestedFiltersTypeDef",
    {
        "NestedPropertyName": str,
        "Filters": Sequence[FilterTypeDef],
    },
)

HyperParameterTrainingJobSummaryTypeDef = TypedDict(
    "HyperParameterTrainingJobSummaryTypeDef",
    {
        "TrainingJobDefinitionName": str,
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "TuningJobName": str,
        "CreationTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "TrainingJobStatus": TrainingJobStatusType,
        "TunedHyperParameters": Dict[str, str],
        "FailureReason": str,
        "FinalHyperParameterTuningJobObjectiveMetric": (
            FinalHyperParameterTuningJobObjectiveMetricTypeDef
        ),
        "ObjectiveStatus": ObjectiveStatusType,
    },
)

ListFlowDefinitionsResponseTypeDef = TypedDict(
    "ListFlowDefinitionsResponseTypeDef",
    {
        "FlowDefinitionSummaries": List[FlowDefinitionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSearchSuggestionsResponseTypeDef = TypedDict(
    "GetSearchSuggestionsResponseTypeDef",
    {
        "PropertyNameSuggestions": List[PropertyNameSuggestionTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateCodeRepositoryInputRequestTypeDef = TypedDict(
    "_RequiredUpdateCodeRepositoryInputRequestTypeDef",
    {
        "CodeRepositoryName": str,
    },
)
_OptionalUpdateCodeRepositoryInputRequestTypeDef = TypedDict(
    "_OptionalUpdateCodeRepositoryInputRequestTypeDef",
    {
        "GitConfig": GitConfigForUpdateTypeDef,
    },
    total=False,
)


class UpdateCodeRepositoryInputRequestTypeDef(
    _RequiredUpdateCodeRepositoryInputRequestTypeDef,
    _OptionalUpdateCodeRepositoryInputRequestTypeDef,
):
    pass


ListHubContentVersionsResponseTypeDef = TypedDict(
    "ListHubContentVersionsResponseTypeDef",
    {
        "HubContentSummaries": List[HubContentInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHubContentsResponseTypeDef = TypedDict(
    "ListHubContentsResponseTypeDef",
    {
        "HubContentSummaries": List[HubContentInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHubsResponseTypeDef = TypedDict(
    "ListHubsResponseTypeDef",
    {
        "HubSummaries": List[HubInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HumanLoopActivationConfigTypeDef = TypedDict(
    "HumanLoopActivationConfigTypeDef",
    {
        "HumanLoopActivationConditionsConfig": HumanLoopActivationConditionsConfigTypeDef,
    },
)

ListHumanTaskUisResponseTypeDef = TypedDict(
    "ListHumanTaskUisResponseTypeDef",
    {
        "HumanTaskUiSummaries": List[HumanTaskUiSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HyperParameterTuningResourceConfigTypeDef = TypedDict(
    "HyperParameterTuningResourceConfigTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "VolumeSizeInGB": int,
        "VolumeKmsKeyId": str,
        "AllocationStrategy": Literal["Prioritized"],
        "InstanceConfigs": Sequence[HyperParameterTuningInstanceConfigTypeDef],
    },
    total=False,
)

HyperParameterTuningJobSummaryTypeDef = TypedDict(
    "HyperParameterTuningJobSummaryTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobStatus": HyperParameterTuningJobStatusType,
        "Strategy": HyperParameterTuningJobStrategyTypeType,
        "CreationTime": datetime,
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersTypeDef,
        "ResourceLimits": ResourceLimitsTypeDef,
    },
)

HyperParameterTuningJobStrategyConfigTypeDef = TypedDict(
    "HyperParameterTuningJobStrategyConfigTypeDef",
    {
        "HyperbandStrategyConfig": HyperbandStrategyConfigTypeDef,
    },
    total=False,
)

HyperParameterTuningJobWarmStartConfigTypeDef = TypedDict(
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    {
        "ParentHyperParameterTuningJobs": Sequence[ParentHyperParameterTuningJobTypeDef],
        "WarmStartType": HyperParameterTuningJobWarmStartTypeType,
    },
)

UserContextTypeDef = TypedDict(
    "UserContextTypeDef",
    {
        "UserProfileArn": str,
        "UserProfileName": str,
        "DomainId": str,
        "IamIdentity": IamIdentityTypeDef,
    },
)

_RequiredImageConfigTypeDef = TypedDict(
    "_RequiredImageConfigTypeDef",
    {
        "RepositoryAccessMode": RepositoryAccessModeType,
    },
)
_OptionalImageConfigTypeDef = TypedDict(
    "_OptionalImageConfigTypeDef",
    {
        "RepositoryAuthConfig": RepositoryAuthConfigTypeDef,
    },
    total=False,
)


class ImageConfigTypeDef(_RequiredImageConfigTypeDef, _OptionalImageConfigTypeDef):
    pass


ListImagesResponseTypeDef = TypedDict(
    "ListImagesResponseTypeDef",
    {
        "Images": List[ImageTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListImageVersionsResponseTypeDef = TypedDict(
    "ListImageVersionsResponseTypeDef",
    {
        "ImageVersions": List[ImageVersionTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInferenceRecommendationsJobsResponseTypeDef = TypedDict(
    "ListInferenceRecommendationsJobsResponseTypeDef",
    {
        "InferenceRecommendationsJobs": List[InferenceRecommendationsJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredResourceConfigTypeDef = TypedDict(
    "_RequiredResourceConfigTypeDef",
    {
        "VolumeSizeInGB": int,
    },
)
_OptionalResourceConfigTypeDef = TypedDict(
    "_OptionalResourceConfigTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "VolumeKmsKeyId": str,
        "InstanceGroups": Sequence[InstanceGroupTypeDef],
        "KeepAlivePeriodInSeconds": int,
    },
    total=False,
)


class ResourceConfigTypeDef(_RequiredResourceConfigTypeDef, _OptionalResourceConfigTypeDef):
    pass


ParameterRangeTypeDef = TypedDict(
    "ParameterRangeTypeDef",
    {
        "IntegerParameterRangeSpecification": IntegerParameterRangeSpecificationTypeDef,
        "ContinuousParameterRangeSpecification": ContinuousParameterRangeSpecificationTypeDef,
        "CategoricalParameterRangeSpecification": CategoricalParameterRangeSpecificationTypeDef,
    },
    total=False,
)

ParameterRangesTypeDef = TypedDict(
    "ParameterRangesTypeDef",
    {
        "IntegerParameterRanges": Sequence[IntegerParameterRangeTypeDef],
        "ContinuousParameterRanges": Sequence[ContinuousParameterRangeTypeDef],
        "CategoricalParameterRanges": Sequence[CategoricalParameterRangeTypeDef],
        "AutoParameters": Sequence[AutoParameterTypeDef],
    },
    total=False,
)

_RequiredKernelGatewayImageConfigTypeDef = TypedDict(
    "_RequiredKernelGatewayImageConfigTypeDef",
    {
        "KernelSpecs": Sequence[KernelSpecTypeDef],
    },
)
_OptionalKernelGatewayImageConfigTypeDef = TypedDict(
    "_OptionalKernelGatewayImageConfigTypeDef",
    {
        "FileSystemConfig": FileSystemConfigTypeDef,
    },
    total=False,
)


class KernelGatewayImageConfigTypeDef(
    _RequiredKernelGatewayImageConfigTypeDef, _OptionalKernelGatewayImageConfigTypeDef
):
    pass


LabelingJobForWorkteamSummaryTypeDef = TypedDict(
    "LabelingJobForWorkteamSummaryTypeDef",
    {
        "LabelingJobName": str,
        "JobReferenceCode": str,
        "WorkRequesterAccountId": str,
        "CreationTime": datetime,
        "LabelCounters": LabelCountersForWorkteamTypeDef,
        "NumberOfHumanWorkersPerDataObject": int,
    },
)

LabelingJobDataSourceTypeDef = TypedDict(
    "LabelingJobDataSourceTypeDef",
    {
        "S3DataSource": LabelingJobS3DataSourceTypeDef,
        "SnsDataSource": LabelingJobSnsDataSourceTypeDef,
    },
    total=False,
)

ListLineageGroupsResponseTypeDef = TypedDict(
    "ListLineageGroupsResponseTypeDef",
    {
        "LineageGroupSummaries": List[LineageGroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDataQualityJobDefinitionsResponseTypeDef = TypedDict(
    "ListDataQualityJobDefinitionsResponseTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelBiasJobDefinitionsResponseTypeDef = TypedDict(
    "ListModelBiasJobDefinitionsResponseTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelExplainabilityJobDefinitionsResponseTypeDef = TypedDict(
    "ListModelExplainabilityJobDefinitionsResponseTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelQualityJobDefinitionsResponseTypeDef = TypedDict(
    "ListModelQualityJobDefinitionsResponseTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelCardExportJobsResponseTypeDef = TypedDict(
    "ListModelCardExportJobsResponseTypeDef",
    {
        "ModelCardExportJobSummaries": List[ModelCardExportJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelCardVersionsResponseTypeDef = TypedDict(
    "ListModelCardVersionsResponseTypeDef",
    {
        "ModelCardVersionSummaryList": List[ModelCardVersionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelCardsResponseTypeDef = TypedDict(
    "ListModelCardsResponseTypeDef",
    {
        "ModelCardSummaries": List[ModelCardSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelMetadataResponseTypeDef = TypedDict(
    "ListModelMetadataResponseTypeDef",
    {
        "ModelMetadataSummaries": List[ModelMetadataSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelPackageGroupsOutputTypeDef = TypedDict(
    "ListModelPackageGroupsOutputTypeDef",
    {
        "ModelPackageGroupSummaryList": List[ModelPackageGroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelPackagesOutputTypeDef = TypedDict(
    "ListModelPackagesOutputTypeDef",
    {
        "ModelPackageSummaryList": List[ModelPackageSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelsOutputTypeDef = TypedDict(
    "ListModelsOutputTypeDef",
    {
        "Models": List[ModelSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringAlertHistoryResponseTypeDef = TypedDict(
    "ListMonitoringAlertHistoryResponseTypeDef",
    {
        "MonitoringAlertHistory": List[MonitoringAlertHistorySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringSchedulesResponseTypeDef = TypedDict(
    "ListMonitoringSchedulesResponseTypeDef",
    {
        "MonitoringScheduleSummaries": List[MonitoringScheduleSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNotebookInstanceLifecycleConfigsOutputTypeDef = TypedDict(
    "ListNotebookInstanceLifecycleConfigsOutputTypeDef",
    {
        "NextToken": str,
        "NotebookInstanceLifecycleConfigs": List[NotebookInstanceLifecycleConfigSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNotebookInstancesOutputTypeDef = TypedDict(
    "ListNotebookInstancesOutputTypeDef",
    {
        "NextToken": str,
        "NotebookInstances": List[NotebookInstanceSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelineExecutionsResponseTypeDef = TypedDict(
    "ListPipelineExecutionsResponseTypeDef",
    {
        "PipelineExecutionSummaries": List[PipelineExecutionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelineParametersForExecutionResponseTypeDef = TypedDict(
    "ListPipelineParametersForExecutionResponseTypeDef",
    {
        "PipelineParameters": List[ParameterTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelinesResponseTypeDef = TypedDict(
    "ListPipelinesResponseTypeDef",
    {
        "PipelineSummaries": List[PipelineSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListProcessingJobsResponseTypeDef = TypedDict(
    "ListProcessingJobsResponseTypeDef",
    {
        "ProcessingJobSummaries": List[ProcessingJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListProjectsOutputTypeDef = TypedDict(
    "ListProjectsOutputTypeDef",
    {
        "ProjectSummaryList": List[ProjectSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSpacesResponseTypeDef = TypedDict(
    "ListSpacesResponseTypeDef",
    {
        "Spaces": List[SpaceDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStudioLifecycleConfigsResponseTypeDef = TypedDict(
    "ListStudioLifecycleConfigsResponseTypeDef",
    {
        "NextToken": str,
        "StudioLifecycleConfigs": List[StudioLifecycleConfigDetailsTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTransformJobsResponseTypeDef = TypedDict(
    "ListTransformJobsResponseTypeDef",
    {
        "TransformJobSummaries": List[TransformJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListUserProfilesResponseTypeDef = TypedDict(
    "ListUserProfilesResponseTypeDef",
    {
        "UserProfiles": List[UserProfileDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MemberDefinitionTypeDef = TypedDict(
    "MemberDefinitionTypeDef",
    {
        "CognitoMemberDefinition": CognitoMemberDefinitionTypeDef,
        "OidcMemberDefinition": OidcMemberDefinitionTypeDef,
    },
    total=False,
)

MonitoringAlertActionsTypeDef = TypedDict(
    "MonitoringAlertActionsTypeDef",
    {
        "ModelDashboardIndicator": ModelDashboardIndicatorActionTypeDef,
    },
)

ModelDataSourceTypeDef = TypedDict(
    "ModelDataSourceTypeDef",
    {
        "S3DataSource": S3ModelDataSourceTypeDef,
    },
)

ModelInfrastructureConfigTypeDef = TypedDict(
    "ModelInfrastructureConfigTypeDef",
    {
        "InfrastructureType": Literal["RealTimeInference"],
        "RealTimeInferenceConfig": RealTimeInferenceConfigTypeDef,
    },
)

ModelPackageContainerDefinitionTypeDef = TypedDict(
    "ModelPackageContainerDefinitionTypeDef",
    {
        "ContainerHostname": str,
        "Image": str,
        "ImageDigest": str,
        "ModelDataUrl": str,
        "ProductId": str,
        "Environment": Dict[str, str],
        "ModelInput": ModelInputTypeDef,
        "Framework": str,
        "FrameworkVersion": str,
        "NearestModelName": str,
    },
)

RecommendationJobStoppingConditionsTypeDef = TypedDict(
    "RecommendationJobStoppingConditionsTypeDef",
    {
        "MaxInvocations": int,
        "ModelLatencyThresholds": Sequence[ModelLatencyThresholdTypeDef],
    },
    total=False,
)

ModelMetadataSearchExpressionTypeDef = TypedDict(
    "ModelMetadataSearchExpressionTypeDef",
    {
        "Filters": Sequence[ModelMetadataFilterTypeDef],
    },
    total=False,
)

ModelPackageStatusDetailsTypeDef = TypedDict(
    "ModelPackageStatusDetailsTypeDef",
    {
        "ValidationStatuses": List[ModelPackageStatusItemTypeDef],
        "ImageScanStatuses": List[ModelPackageStatusItemTypeDef],
    },
)

MonitoringResourcesTypeDef = TypedDict(
    "MonitoringResourcesTypeDef",
    {
        "ClusterConfig": MonitoringClusterConfigTypeDef,
    },
)

MonitoringDatasetFormatTypeDef = TypedDict(
    "MonitoringDatasetFormatTypeDef",
    {
        "Csv": MonitoringCsvDatasetFormatTypeDef,
        "Json": MonitoringJsonDatasetFormatTypeDef,
        "Parquet": Mapping[str, Any],
    },
    total=False,
)

MonitoringOutputTypeDef = TypedDict(
    "MonitoringOutputTypeDef",
    {
        "S3Output": MonitoringS3OutputTypeDef,
    },
)

_RequiredOfflineStoreConfigTypeDef = TypedDict(
    "_RequiredOfflineStoreConfigTypeDef",
    {
        "S3StorageConfig": S3StorageConfigTypeDef,
    },
)
_OptionalOfflineStoreConfigTypeDef = TypedDict(
    "_OptionalOfflineStoreConfigTypeDef",
    {
        "DisableGlueTableCreation": bool,
        "DataCatalogConfig": DataCatalogConfigTypeDef,
        "TableFormat": TableFormatType,
    },
    total=False,
)


class OfflineStoreConfigTypeDef(
    _RequiredOfflineStoreConfigTypeDef, _OptionalOfflineStoreConfigTypeDef
):
    pass


OnlineStoreConfigTypeDef = TypedDict(
    "OnlineStoreConfigTypeDef",
    {
        "SecurityConfig": OnlineStoreSecurityConfigTypeDef,
        "EnableOnlineStore": bool,
        "TtlDuration": TtlDurationTypeDef,
    },
    total=False,
)

OnlineStoreConfigUpdateTypeDef = TypedDict(
    "OnlineStoreConfigUpdateTypeDef",
    {
        "TtlDuration": TtlDurationTypeDef,
    },
    total=False,
)

_RequiredOutputConfigTypeDef = TypedDict(
    "_RequiredOutputConfigTypeDef",
    {
        "S3OutputLocation": str,
    },
)
_OptionalOutputConfigTypeDef = TypedDict(
    "_OptionalOutputConfigTypeDef",
    {
        "TargetDevice": TargetDeviceType,
        "TargetPlatform": TargetPlatformTypeDef,
        "CompilerOptions": str,
        "KmsKeyId": str,
    },
    total=False,
)


class OutputConfigTypeDef(_RequiredOutputConfigTypeDef, _OptionalOutputConfigTypeDef):
    pass


PendingProductionVariantSummaryTypeDef = TypedDict(
    "PendingProductionVariantSummaryTypeDef",
    {
        "VariantName": str,
        "DeployedImages": List[DeployedImageTypeDef],
        "CurrentWeight": float,
        "DesiredWeight": float,
        "CurrentInstanceCount": int,
        "DesiredInstanceCount": int,
        "InstanceType": ProductionVariantInstanceTypeType,
        "AcceleratorType": ProductionVariantAcceleratorTypeType,
        "VariantStatus": List[ProductionVariantStatusTypeDef],
        "CurrentServerlessConfig": ProductionVariantServerlessConfigTypeDef,
        "DesiredServerlessConfig": ProductionVariantServerlessConfigTypeDef,
    },
)

ProductionVariantSummaryTypeDef = TypedDict(
    "ProductionVariantSummaryTypeDef",
    {
        "VariantName": str,
        "DeployedImages": List[DeployedImageTypeDef],
        "CurrentWeight": float,
        "DesiredWeight": float,
        "CurrentInstanceCount": int,
        "DesiredInstanceCount": int,
        "VariantStatus": List[ProductionVariantStatusTypeDef],
        "CurrentServerlessConfig": ProductionVariantServerlessConfigTypeDef,
        "DesiredServerlessConfig": ProductionVariantServerlessConfigTypeDef,
    },
)

TrafficPatternTypeDef = TypedDict(
    "TrafficPatternTypeDef",
    {
        "TrafficType": Literal["PHASES"],
        "Phases": Sequence[PhaseTypeDef],
    },
    total=False,
)

ProcessingResourcesTypeDef = TypedDict(
    "ProcessingResourcesTypeDef",
    {
        "ClusterConfig": ProcessingClusterConfigTypeDef,
    },
)

_RequiredProcessingOutputTypeDef = TypedDict(
    "_RequiredProcessingOutputTypeDef",
    {
        "OutputName": str,
    },
)
_OptionalProcessingOutputTypeDef = TypedDict(
    "_OptionalProcessingOutputTypeDef",
    {
        "S3Output": ProcessingS3OutputTypeDef,
        "FeatureStoreOutput": ProcessingFeatureStoreOutputTypeDef,
        "AppManaged": bool,
    },
    total=False,
)


class ProcessingOutputTypeDef(_RequiredProcessingOutputTypeDef, _OptionalProcessingOutputTypeDef):
    pass


_RequiredProductionVariantTypeDef = TypedDict(
    "_RequiredProductionVariantTypeDef",
    {
        "VariantName": str,
        "ModelName": str,
    },
)
_OptionalProductionVariantTypeDef = TypedDict(
    "_OptionalProductionVariantTypeDef",
    {
        "InitialInstanceCount": int,
        "InstanceType": ProductionVariantInstanceTypeType,
        "InitialVariantWeight": float,
        "AcceleratorType": ProductionVariantAcceleratorTypeType,
        "CoreDumpConfig": ProductionVariantCoreDumpConfigTypeDef,
        "ServerlessConfig": ProductionVariantServerlessConfigTypeDef,
        "VolumeSizeInGB": int,
        "ModelDataDownloadTimeoutInSeconds": int,
        "ContainerStartupHealthCheckTimeoutInSeconds": int,
        "EnableSSMAccess": bool,
    },
    total=False,
)


class ProductionVariantTypeDef(
    _RequiredProductionVariantTypeDef, _OptionalProductionVariantTypeDef
):
    pass


SuggestionQueryTypeDef = TypedDict(
    "SuggestionQueryTypeDef",
    {
        "PropertyNameQuery": PropertyNameQueryTypeDef,
    },
    total=False,
)

_RequiredServiceCatalogProvisioningDetailsTypeDef = TypedDict(
    "_RequiredServiceCatalogProvisioningDetailsTypeDef",
    {
        "ProductId": str,
    },
)
_OptionalServiceCatalogProvisioningDetailsTypeDef = TypedDict(
    "_OptionalServiceCatalogProvisioningDetailsTypeDef",
    {
        "ProvisioningArtifactId": str,
        "PathId": str,
        "ProvisioningParameters": Sequence[ProvisioningParameterTypeDef],
    },
    total=False,
)


class ServiceCatalogProvisioningDetailsTypeDef(
    _RequiredServiceCatalogProvisioningDetailsTypeDef,
    _OptionalServiceCatalogProvisioningDetailsTypeDef,
):
    pass


ServiceCatalogProvisioningUpdateDetailsTypeDef = TypedDict(
    "ServiceCatalogProvisioningUpdateDetailsTypeDef",
    {
        "ProvisioningArtifactId": str,
        "ProvisioningParameters": Sequence[ProvisioningParameterTypeDef],
    },
    total=False,
)

PublicWorkforceTaskPriceTypeDef = TypedDict(
    "PublicWorkforceTaskPriceTypeDef",
    {
        "AmountInUsd": USDTypeDef,
    },
    total=False,
)

QueryLineageRequestRequestTypeDef = TypedDict(
    "QueryLineageRequestRequestTypeDef",
    {
        "StartArns": Sequence[str],
        "Direction": DirectionType,
        "IncludeEdges": bool,
        "Filters": QueryFiltersTypeDef,
        "MaxDepth": int,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

QueryLineageResponseTypeDef = TypedDict(
    "QueryLineageResponseTypeDef",
    {
        "Vertices": List[VertexTypeDef],
        "Edges": List[EdgeTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommendationJobOutputConfigTypeDef = TypedDict(
    "RecommendationJobOutputConfigTypeDef",
    {
        "KmsKeyId": str,
        "CompiledOutputConfig": RecommendationJobCompiledOutputConfigTypeDef,
    },
    total=False,
)

RecommendationJobContainerConfigTypeDef = TypedDict(
    "RecommendationJobContainerConfigTypeDef",
    {
        "Domain": str,
        "Task": str,
        "Framework": str,
        "FrameworkVersion": str,
        "PayloadConfig": RecommendationJobPayloadConfigTypeDef,
        "NearestModelName": str,
        "SupportedInstanceTypes": Sequence[str],
        "DataInputConfig": str,
        "SupportedEndpointType": RecommendationJobSupportedEndpointTypeType,
    },
    total=False,
)

_RequiredRenderUiTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredRenderUiTemplateRequestRequestTypeDef",
    {
        "Task": RenderableTaskTypeDef,
        "RoleArn": str,
    },
)
_OptionalRenderUiTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalRenderUiTemplateRequestRequestTypeDef",
    {
        "UiTemplate": UiTemplateTypeDef,
        "HumanTaskUiArn": str,
    },
    total=False,
)


class RenderUiTemplateRequestRequestTypeDef(
    _RequiredRenderUiTemplateRequestRequestTypeDef, _OptionalRenderUiTemplateRequestRequestTypeDef
):
    pass


RenderUiTemplateResponseTypeDef = TypedDict(
    "RenderUiTemplateResponseTypeDef",
    {
        "RenderedContent": str,
        "Errors": List[RenderingErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateTrainingJobRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrainingJobRequestRequestTypeDef",
    {
        "TrainingJobName": str,
    },
)
_OptionalUpdateTrainingJobRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrainingJobRequestRequestTypeDef",
    {
        "ProfilerConfig": ProfilerConfigForUpdateTypeDef,
        "ProfilerRuleConfigurations": Sequence[ProfilerRuleConfigurationTypeDef],
        "ResourceConfig": ResourceConfigForUpdateTypeDef,
    },
    total=False,
)


class UpdateTrainingJobRequestRequestTypeDef(
    _RequiredUpdateTrainingJobRequestRequestTypeDef, _OptionalUpdateTrainingJobRequestRequestTypeDef
):
    pass


SelectiveExecutionConfigTypeDef = TypedDict(
    "SelectiveExecutionConfigTypeDef",
    {
        "SourcePipelineExecutionArn": str,
        "SelectedSteps": List[SelectedStepTypeDef],
    },
)

ShadowModeConfigTypeDef = TypedDict(
    "ShadowModeConfigTypeDef",
    {
        "SourceModelVariantName": str,
        "ShadowModelVariants": Sequence[ShadowModelVariantConfigTypeDef],
    },
)

SourceAlgorithmSpecificationTypeDef = TypedDict(
    "SourceAlgorithmSpecificationTypeDef",
    {
        "SourceAlgorithms": Sequence[SourceAlgorithmTypeDef],
    },
)

_RequiredTimeSeriesForecastingJobConfigTypeDef = TypedDict(
    "_RequiredTimeSeriesForecastingJobConfigTypeDef",
    {
        "ForecastFrequency": str,
        "ForecastHorizon": int,
        "TimeSeriesConfig": TimeSeriesConfigTypeDef,
    },
)
_OptionalTimeSeriesForecastingJobConfigTypeDef = TypedDict(
    "_OptionalTimeSeriesForecastingJobConfigTypeDef",
    {
        "FeatureSpecificationS3Uri": str,
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
        "ForecastQuantiles": Sequence[str],
        "Transformations": TimeSeriesTransformationsTypeDef,
    },
    total=False,
)


class TimeSeriesForecastingJobConfigTypeDef(
    _RequiredTimeSeriesForecastingJobConfigTypeDef, _OptionalTimeSeriesForecastingJobConfigTypeDef
):
    pass


_RequiredTrainingImageConfigTypeDef = TypedDict(
    "_RequiredTrainingImageConfigTypeDef",
    {
        "TrainingRepositoryAccessMode": TrainingRepositoryAccessModeType,
    },
)
_OptionalTrainingImageConfigTypeDef = TypedDict(
    "_OptionalTrainingImageConfigTypeDef",
    {
        "TrainingRepositoryAuthConfig": TrainingRepositoryAuthConfigTypeDef,
    },
    total=False,
)


class TrainingImageConfigTypeDef(
    _RequiredTrainingImageConfigTypeDef, _OptionalTrainingImageConfigTypeDef
):
    pass


TransformDataSourceTypeDef = TypedDict(
    "TransformDataSourceTypeDef",
    {
        "S3DataSource": TransformS3DataSourceTypeDef,
    },
)

WorkforceTypeDef = TypedDict(
    "WorkforceTypeDef",
    {
        "WorkforceName": str,
        "WorkforceArn": str,
        "LastUpdatedDate": datetime,
        "SourceIpConfig": SourceIpConfigTypeDef,
        "SubDomain": str,
        "CognitoConfig": CognitoConfigTypeDef,
        "OidcConfig": OidcConfigForResponseTypeDef,
        "CreateDate": datetime,
        "WorkforceVpcConfig": WorkforceVpcConfigResponseTypeDef,
        "Status": WorkforceStatusType,
        "FailureReason": str,
    },
)

ListActionsResponseTypeDef = TypedDict(
    "ListActionsResponseTypeDef",
    {
        "ActionSummaries": List[ActionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ArtifactSummaryTypeDef = TypedDict(
    "ArtifactSummaryTypeDef",
    {
        "ArtifactArn": str,
        "ArtifactName": str,
        "Source": ArtifactSourceTypeDef,
        "ArtifactType": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

_RequiredCreateArtifactRequestRequestTypeDef = TypedDict(
    "_RequiredCreateArtifactRequestRequestTypeDef",
    {
        "Source": ArtifactSourceTypeDef,
        "ArtifactType": str,
    },
)
_OptionalCreateArtifactRequestRequestTypeDef = TypedDict(
    "_OptionalCreateArtifactRequestRequestTypeDef",
    {
        "ArtifactName": str,
        "Properties": Mapping[str, str],
        "MetadataProperties": MetadataPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateArtifactRequestRequestTypeDef(
    _RequiredCreateArtifactRequestRequestTypeDef, _OptionalCreateArtifactRequestRequestTypeDef
):
    pass


DeleteArtifactRequestRequestTypeDef = TypedDict(
    "DeleteArtifactRequestRequestTypeDef",
    {
        "ArtifactArn": str,
        "Source": ArtifactSourceTypeDef,
    },
    total=False,
)

_RequiredAsyncInferenceConfigTypeDef = TypedDict(
    "_RequiredAsyncInferenceConfigTypeDef",
    {
        "OutputConfig": AsyncInferenceOutputConfigTypeDef,
    },
)
_OptionalAsyncInferenceConfigTypeDef = TypedDict(
    "_OptionalAsyncInferenceConfigTypeDef",
    {
        "ClientConfig": AsyncInferenceClientConfigTypeDef,
    },
    total=False,
)


class AsyncInferenceConfigTypeDef(
    _RequiredAsyncInferenceConfigTypeDef, _OptionalAsyncInferenceConfigTypeDef
):
    pass


_RequiredTabularJobConfigTypeDef = TypedDict(
    "_RequiredTabularJobConfigTypeDef",
    {
        "TargetAttributeName": str,
    },
)
_OptionalTabularJobConfigTypeDef = TypedDict(
    "_OptionalTabularJobConfigTypeDef",
    {
        "CandidateGenerationConfig": CandidateGenerationConfigTypeDef,
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
        "FeatureSpecificationS3Uri": str,
        "Mode": AutoMLModeType,
        "GenerateCandidateDefinitionsOnly": bool,
        "ProblemType": ProblemTypeType,
        "SampleWeightAttributeName": str,
    },
    total=False,
)


class TabularJobConfigTypeDef(_RequiredTabularJobConfigTypeDef, _OptionalTabularJobConfigTypeDef):
    pass


_RequiredAutoMLChannelTypeDef = TypedDict(
    "_RequiredAutoMLChannelTypeDef",
    {
        "DataSource": AutoMLDataSourceTypeDef,
        "TargetAttributeName": str,
    },
)
_OptionalAutoMLChannelTypeDef = TypedDict(
    "_OptionalAutoMLChannelTypeDef",
    {
        "CompressionType": CompressionTypeType,
        "ContentType": str,
        "ChannelType": AutoMLChannelTypeType,
        "SampleWeightAttributeName": str,
    },
    total=False,
)


class AutoMLChannelTypeDef(_RequiredAutoMLChannelTypeDef, _OptionalAutoMLChannelTypeDef):
    pass


AutoMLJobChannelTypeDef = TypedDict(
    "AutoMLJobChannelTypeDef",
    {
        "ChannelType": AutoMLChannelTypeType,
        "ContentType": str,
        "CompressionType": CompressionTypeType,
        "DataSource": AutoMLDataSourceTypeDef,
    },
    total=False,
)

ListAutoMLJobsResponseTypeDef = TypedDict(
    "ListAutoMLJobsResponseTypeDef",
    {
        "AutoMLJobSummaries": List[AutoMLJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoMLResolvedAttributesTypeDef = TypedDict(
    "AutoMLResolvedAttributesTypeDef",
    {
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
        "AutoMLProblemTypeResolvedAttributes": AutoMLProblemTypeResolvedAttributesTypeDef,
    },
)

AutoMLJobConfigTypeDef = TypedDict(
    "AutoMLJobConfigTypeDef",
    {
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
        "SecurityConfig": AutoMLSecurityConfigTypeDef,
        "DataSplitConfig": AutoMLDataSplitConfigTypeDef,
        "CandidateGenerationConfig": AutoMLCandidateGenerationConfigTypeDef,
        "Mode": AutoMLModeType,
    },
    total=False,
)

_RequiredLabelingJobAlgorithmsConfigTypeDef = TypedDict(
    "_RequiredLabelingJobAlgorithmsConfigTypeDef",
    {
        "LabelingJobAlgorithmSpecificationArn": str,
    },
)
_OptionalLabelingJobAlgorithmsConfigTypeDef = TypedDict(
    "_OptionalLabelingJobAlgorithmsConfigTypeDef",
    {
        "InitialActiveLearningModelArn": str,
        "LabelingJobResourceConfig": LabelingJobResourceConfigTypeDef,
    },
    total=False,
)


class LabelingJobAlgorithmsConfigTypeDef(
    _RequiredLabelingJobAlgorithmsConfigTypeDef, _OptionalLabelingJobAlgorithmsConfigTypeDef
):
    pass


ModelMetricsTypeDef = TypedDict(
    "ModelMetricsTypeDef",
    {
        "ModelQuality": ModelQualityTypeDef,
        "ModelDataQuality": ModelDataQualityTypeDef,
        "Bias": BiasTypeDef,
        "Explainability": ExplainabilityTypeDef,
    },
    total=False,
)

PipelineExecutionStepMetadataTypeDef = TypedDict(
    "PipelineExecutionStepMetadataTypeDef",
    {
        "TrainingJob": TrainingJobStepMetadataTypeDef,
        "ProcessingJob": ProcessingJobStepMetadataTypeDef,
        "TransformJob": TransformJobStepMetadataTypeDef,
        "TuningJob": TuningJobStepMetaDataTypeDef,
        "Model": ModelStepMetadataTypeDef,
        "RegisterModel": RegisterModelStepMetadataTypeDef,
        "Condition": ConditionStepMetadataTypeDef,
        "Callback": CallbackStepMetadataTypeDef,
        "Lambda": LambdaStepMetadataTypeDef,
        "QualityCheck": QualityCheckStepMetadataTypeDef,
        "ClarifyCheck": ClarifyCheckStepMetadataTypeDef,
        "EMR": EMRStepMetadataTypeDef,
        "Fail": FailStepMetadataTypeDef,
        "AutoMLJob": AutoMLJobStepMetadataTypeDef,
    },
)

AutoMLCandidateTypeDef = TypedDict(
    "AutoMLCandidateTypeDef",
    {
        "CandidateName": str,
        "FinalAutoMLJobObjectiveMetric": FinalAutoMLJobObjectiveMetricTypeDef,
        "ObjectiveStatus": ObjectiveStatusType,
        "CandidateSteps": List[AutoMLCandidateStepTypeDef],
        "CandidateStatus": CandidateStatusType,
        "InferenceContainers": List[AutoMLContainerDefinitionTypeDef],
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "CandidateProperties": CandidatePropertiesTypeDef,
        "InferenceContainerDefinitions": Dict[
            AutoMLProcessingUnitType, List[AutoMLContainerDefinitionTypeDef]
        ],
    },
)

_RequiredBlueGreenUpdatePolicyTypeDef = TypedDict(
    "_RequiredBlueGreenUpdatePolicyTypeDef",
    {
        "TrafficRoutingConfiguration": TrafficRoutingConfigTypeDef,
    },
)
_OptionalBlueGreenUpdatePolicyTypeDef = TypedDict(
    "_OptionalBlueGreenUpdatePolicyTypeDef",
    {
        "TerminationWaitInSeconds": int,
        "MaximumExecutionTimeoutInSeconds": int,
    },
    total=False,
)


class BlueGreenUpdatePolicyTypeDef(
    _RequiredBlueGreenUpdatePolicyTypeDef, _OptionalBlueGreenUpdatePolicyTypeDef
):
    pass


EndpointInputConfigurationTypeDef = TypedDict(
    "EndpointInputConfigurationTypeDef",
    {
        "InstanceType": ProductionVariantInstanceTypeType,
        "InferenceSpecificationName": str,
        "EnvironmentParameterRanges": EnvironmentParameterRangesTypeDef,
        "ServerlessConfig": ProductionVariantServerlessConfigTypeDef,
    },
    total=False,
)

_RequiredClarifyExplainerConfigTypeDef = TypedDict(
    "_RequiredClarifyExplainerConfigTypeDef",
    {
        "ShapConfig": ClarifyShapConfigTypeDef,
    },
)
_OptionalClarifyExplainerConfigTypeDef = TypedDict(
    "_OptionalClarifyExplainerConfigTypeDef",
    {
        "EnableExplanations": str,
        "InferenceConfig": ClarifyInferenceConfigTypeDef,
    },
    total=False,
)


class ClarifyExplainerConfigTypeDef(
    _RequiredClarifyExplainerConfigTypeDef, _OptionalClarifyExplainerConfigTypeDef
):
    pass


ListCodeRepositoriesOutputTypeDef = TypedDict(
    "ListCodeRepositoriesOutputTypeDef",
    {
        "CodeRepositorySummaryList": List[CodeRepositorySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListContextsResponseTypeDef = TypedDict(
    "ListContextsResponseTypeDef",
    {
        "ContextSummaries": List[ContextSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DomainSettingsForUpdateTypeDef = TypedDict(
    "DomainSettingsForUpdateTypeDef",
    {
        "RStudioServerProDomainSettingsForUpdate": RStudioServerProDomainSettingsForUpdateTypeDef,
        "ExecutionRoleIdentityConfig": ExecutionRoleIdentityConfigType,
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)

DomainSettingsTypeDef = TypedDict(
    "DomainSettingsTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "RStudioServerProDomainSettings": RStudioServerProDomainSettingsTypeDef,
        "ExecutionRoleIdentityConfig": ExecutionRoleIdentityConfigType,
    },
    total=False,
)

ListInferenceExperimentsResponseTypeDef = TypedDict(
    "ListInferenceExperimentsResponseTypeDef",
    {
        "InferenceExperiments": List[InferenceExperimentSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DefaultSpaceSettingsTypeDef = TypedDict(
    "DefaultSpaceSettingsTypeDef",
    {
        "ExecutionRole": str,
        "SecurityGroups": Sequence[str],
        "JupyterServerAppSettings": JupyterServerAppSettingsTypeDef,
        "KernelGatewayAppSettings": KernelGatewayAppSettingsTypeDef,
    },
    total=False,
)

SpaceSettingsTypeDef = TypedDict(
    "SpaceSettingsTypeDef",
    {
        "JupyterServerAppSettings": JupyterServerAppSettingsTypeDef,
        "KernelGatewayAppSettings": KernelGatewayAppSettingsTypeDef,
    },
    total=False,
)

UserSettingsTypeDef = TypedDict(
    "UserSettingsTypeDef",
    {
        "ExecutionRole": str,
        "SecurityGroups": Sequence[str],
        "SharingSettings": SharingSettingsTypeDef,
        "JupyterServerAppSettings": JupyterServerAppSettingsTypeDef,
        "KernelGatewayAppSettings": KernelGatewayAppSettingsTypeDef,
        "TensorBoardAppSettings": TensorBoardAppSettingsTypeDef,
        "RStudioServerProAppSettings": RStudioServerProAppSettingsTypeDef,
        "RSessionAppSettings": RSessionAppSettingsTypeDef,
        "CanvasAppSettings": CanvasAppSettingsTypeDef,
    },
    total=False,
)

_RequiredChannelTypeDef = TypedDict(
    "_RequiredChannelTypeDef",
    {
        "ChannelName": str,
        "DataSource": DataSourceTypeDef,
    },
)
_OptionalChannelTypeDef = TypedDict(
    "_OptionalChannelTypeDef",
    {
        "ContentType": str,
        "CompressionType": CompressionTypeType,
        "RecordWrapperType": RecordWrapperType,
        "InputMode": TrainingInputModeType,
        "ShuffleConfig": ShuffleConfigTypeDef,
    },
    total=False,
)


class ChannelTypeDef(_RequiredChannelTypeDef, _OptionalChannelTypeDef):
    pass


_RequiredProcessingInputTypeDef = TypedDict(
    "_RequiredProcessingInputTypeDef",
    {
        "InputName": str,
    },
)
_OptionalProcessingInputTypeDef = TypedDict(
    "_OptionalProcessingInputTypeDef",
    {
        "AppManaged": bool,
        "S3Input": ProcessingS3InputTypeDef,
        "DatasetDefinition": DatasetDefinitionTypeDef,
    },
    total=False,
)


class ProcessingInputTypeDef(_RequiredProcessingInputTypeDef, _OptionalProcessingInputTypeDef):
    pass


_RequiredCreateEdgeDeploymentPlanRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEdgeDeploymentPlanRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
        "ModelConfigs": Sequence[EdgeDeploymentModelConfigTypeDef],
        "DeviceFleetName": str,
    },
)
_OptionalCreateEdgeDeploymentPlanRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEdgeDeploymentPlanRequestRequestTypeDef",
    {
        "Stages": Sequence[DeploymentStageTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEdgeDeploymentPlanRequestRequestTypeDef(
    _RequiredCreateEdgeDeploymentPlanRequestRequestTypeDef,
    _OptionalCreateEdgeDeploymentPlanRequestRequestTypeDef,
):
    pass


CreateEdgeDeploymentStageRequestRequestTypeDef = TypedDict(
    "CreateEdgeDeploymentStageRequestRequestTypeDef",
    {
        "EdgeDeploymentPlanName": str,
        "Stages": Sequence[DeploymentStageTypeDef],
    },
)

DescribeEdgeDeploymentPlanResponseTypeDef = TypedDict(
    "DescribeEdgeDeploymentPlanResponseTypeDef",
    {
        "EdgeDeploymentPlanArn": str,
        "EdgeDeploymentPlanName": str,
        "ModelConfigs": List[EdgeDeploymentModelConfigTypeDef],
        "DeviceFleetName": str,
        "EdgeDeploymentSuccess": int,
        "EdgeDeploymentPending": int,
        "EdgeDeploymentFailed": int,
        "Stages": List[DeploymentStageStatusSummaryTypeDef],
        "NextToken": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListExperimentsResponseTypeDef = TypedDict(
    "ListExperimentsResponseTypeDef",
    {
        "ExperimentSummaries": List[ExperimentSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFeatureGroupsResponseTypeDef = TypedDict(
    "ListFeatureGroupsResponseTypeDef",
    {
        "FeatureGroupSummaries": List[FeatureGroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTrainingJobsResponseTypeDef = TypedDict(
    "ListTrainingJobsResponseTypeDef",
    {
        "TrainingJobSummaries": List[TrainingJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTrialsResponseTypeDef = TypedDict(
    "ListTrialsResponseTypeDef",
    {
        "TrialSummaries": List[TrialSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef = TypedDict(
    "UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef",
    {
        "EndpointName": str,
        "DesiredWeightsAndCapacities": Sequence[DesiredWeightAndCapacityTypeDef],
    },
)

ListDevicesResponseTypeDef = TypedDict(
    "ListDevicesResponseTypeDef",
    {
        "DeviceSummaries": List[DeviceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DriftCheckBaselinesTypeDef = TypedDict(
    "DriftCheckBaselinesTypeDef",
    {
        "Bias": DriftCheckBiasTypeDef,
        "Explainability": DriftCheckExplainabilityTypeDef,
        "ModelQuality": DriftCheckModelQualityTypeDef,
        "ModelDataQuality": DriftCheckModelDataQualityTypeDef,
    },
    total=False,
)

InferenceRecommendationTypeDef = TypedDict(
    "InferenceRecommendationTypeDef",
    {
        "Metrics": RecommendationMetricsTypeDef,
        "EndpointConfiguration": EndpointOutputConfigurationTypeDef,
        "ModelConfiguration": ModelConfigurationTypeDef,
        "RecommendationId": str,
        "InvocationEndTime": datetime,
        "InvocationStartTime": datetime,
    },
)

RecommendationJobInferenceBenchmarkTypeDef = TypedDict(
    "RecommendationJobInferenceBenchmarkTypeDef",
    {
        "Metrics": RecommendationMetricsTypeDef,
        "EndpointConfiguration": EndpointOutputConfigurationTypeDef,
        "ModelConfiguration": ModelConfigurationTypeDef,
        "FailureReason": str,
        "EndpointMetrics": InferenceMetricsTypeDef,
        "InvocationEndTime": datetime,
        "InvocationStartTime": datetime,
    },
)

SearchExpressionTypeDef = TypedDict(
    "SearchExpressionTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "NestedFilters": Sequence[NestedFiltersTypeDef],
        "SubExpressions": Sequence[Dict[str, Any]],
        "Operator": BooleanOperatorType,
    },
    total=False,
)

ListTrainingJobsForHyperParameterTuningJobResponseTypeDef = TypedDict(
    "ListTrainingJobsForHyperParameterTuningJobResponseTypeDef",
    {
        "TrainingJobSummaries": List[HyperParameterTrainingJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHyperParameterTuningJobsResponseTypeDef = TypedDict(
    "ListHyperParameterTuningJobsResponseTypeDef",
    {
        "HyperParameterTuningJobSummaries": List[HyperParameterTuningJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociationSummaryTypeDef = TypedDict(
    "AssociationSummaryTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "SourceType": str,
        "DestinationType": str,
        "AssociationType": AssociationEdgeTypeType,
        "SourceName": str,
        "DestinationName": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
    },
)

DescribeActionResponseTypeDef = TypedDict(
    "DescribeActionResponseTypeDef",
    {
        "ActionName": str,
        "ActionArn": str,
        "Source": ActionSourceTypeDef,
        "ActionType": str,
        "Description": str,
        "Status": ActionStatusType,
        "Properties": Dict[str, str],
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "LineageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeArtifactResponseTypeDef = TypedDict(
    "DescribeArtifactResponseTypeDef",
    {
        "ArtifactName": str,
        "ArtifactArn": str,
        "Source": ArtifactSourceTypeDef,
        "ArtifactType": str,
        "Properties": Dict[str, str],
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "LineageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeContextResponseTypeDef = TypedDict(
    "DescribeContextResponseTypeDef",
    {
        "ContextName": str,
        "ContextArn": str,
        "Source": ContextSourceTypeDef,
        "ContextType": str,
        "Description": str,
        "Properties": Dict[str, str],
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "LineageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeExperimentResponseTypeDef = TypedDict(
    "DescribeExperimentResponseTypeDef",
    {
        "ExperimentName": str,
        "ExperimentArn": str,
        "DisplayName": str,
        "Source": ExperimentSourceTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeLineageGroupResponseTypeDef = TypedDict(
    "DescribeLineageGroupResponseTypeDef",
    {
        "LineageGroupName": str,
        "LineageGroupArn": str,
        "DisplayName": str,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelCardResponseTypeDef = TypedDict(
    "DescribeModelCardResponseTypeDef",
    {
        "ModelCardArn": str,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "Content": str,
        "ModelCardStatus": ModelCardStatusType,
        "SecurityConfig": ModelCardSecurityConfigTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "ModelCardProcessingStatus": ModelCardProcessingStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelPackageGroupOutputTypeDef = TypedDict(
    "DescribeModelPackageGroupOutputTypeDef",
    {
        "ModelPackageGroupName": str,
        "ModelPackageGroupArn": str,
        "ModelPackageGroupDescription": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "ModelPackageGroupStatus": ModelPackageGroupStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePipelineResponseTypeDef = TypedDict(
    "DescribePipelineResponseTypeDef",
    {
        "PipelineArn": str,
        "PipelineName": str,
        "PipelineDisplayName": str,
        "PipelineDefinition": str,
        "PipelineDescription": str,
        "RoleArn": str,
        "PipelineStatus": Literal["Active"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastRunTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedBy": UserContextTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTrialComponentResponseTypeDef = TypedDict(
    "DescribeTrialComponentResponseTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "DisplayName": str,
        "Source": TrialComponentSourceTypeDef,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Parameters": Dict[str, TrialComponentParameterValueTypeDef],
        "InputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "OutputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "MetadataProperties": MetadataPropertiesTypeDef,
        "Metrics": List[TrialComponentMetricSummaryTypeDef],
        "LineageGroupArn": str,
        "Sources": List[TrialComponentSourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTrialResponseTypeDef = TypedDict(
    "DescribeTrialResponseTypeDef",
    {
        "TrialName": str,
        "TrialArn": str,
        "DisplayName": str,
        "ExperimentName": str,
        "Source": TrialSourceTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExperimentTypeDef = TypedDict(
    "ExperimentTypeDef",
    {
        "ExperimentName": str,
        "ExperimentArn": str,
        "DisplayName": str,
        "Source": ExperimentSourceTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Tags": List[TagTypeDef],
    },
)

ModelCardTypeDef = TypedDict(
    "ModelCardTypeDef",
    {
        "ModelCardArn": str,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "Content": str,
        "ModelCardStatus": ModelCardStatusType,
        "SecurityConfig": ModelCardSecurityConfigTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Tags": List[TagTypeDef],
        "ModelId": str,
        "RiskRating": str,
        "ModelPackageGroupName": str,
    },
)

ModelDashboardModelCardTypeDef = TypedDict(
    "ModelDashboardModelCardTypeDef",
    {
        "ModelCardArn": str,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "ModelCardStatus": ModelCardStatusType,
        "SecurityConfig": ModelCardSecurityConfigTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Tags": List[TagTypeDef],
        "ModelId": str,
        "RiskRating": str,
    },
)

ModelPackageGroupTypeDef = TypedDict(
    "ModelPackageGroupTypeDef",
    {
        "ModelPackageGroupName": str,
        "ModelPackageGroupArn": str,
        "ModelPackageGroupDescription": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "ModelPackageGroupStatus": ModelPackageGroupStatusType,
        "Tags": List[TagTypeDef],
    },
)

PipelineTypeDef = TypedDict(
    "PipelineTypeDef",
    {
        "PipelineArn": str,
        "PipelineName": str,
        "PipelineDisplayName": str,
        "PipelineDescription": str,
        "RoleArn": str,
        "PipelineStatus": Literal["Active"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastRunTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedBy": UserContextTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
        "Tags": List[TagTypeDef],
    },
)

TrialComponentSimpleSummaryTypeDef = TypedDict(
    "TrialComponentSimpleSummaryTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "TrialComponentSource": TrialComponentSourceTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
    },
)

TrialComponentSummaryTypeDef = TypedDict(
    "TrialComponentSummaryTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "DisplayName": str,
        "TrialComponentSource": TrialComponentSourceTypeDef,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
    },
)

_RequiredHyperParameterSpecificationTypeDef = TypedDict(
    "_RequiredHyperParameterSpecificationTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
    },
)
_OptionalHyperParameterSpecificationTypeDef = TypedDict(
    "_OptionalHyperParameterSpecificationTypeDef",
    {
        "Description": str,
        "Range": ParameterRangeTypeDef,
        "IsTunable": bool,
        "IsRequired": bool,
        "DefaultValue": str,
    },
    total=False,
)


class HyperParameterSpecificationTypeDef(
    _RequiredHyperParameterSpecificationTypeDef, _OptionalHyperParameterSpecificationTypeDef
):
    pass


_RequiredHyperParameterTuningJobConfigTypeDef = TypedDict(
    "_RequiredHyperParameterTuningJobConfigTypeDef",
    {
        "Strategy": HyperParameterTuningJobStrategyTypeType,
        "ResourceLimits": ResourceLimitsTypeDef,
    },
)
_OptionalHyperParameterTuningJobConfigTypeDef = TypedDict(
    "_OptionalHyperParameterTuningJobConfigTypeDef",
    {
        "StrategyConfig": HyperParameterTuningJobStrategyConfigTypeDef,
        "HyperParameterTuningJobObjective": HyperParameterTuningJobObjectiveTypeDef,
        "ParameterRanges": ParameterRangesTypeDef,
        "TrainingJobEarlyStoppingType": TrainingJobEarlyStoppingTypeType,
        "TuningJobCompletionCriteria": TuningJobCompletionCriteriaTypeDef,
        "RandomSeed": int,
    },
    total=False,
)


class HyperParameterTuningJobConfigTypeDef(
    _RequiredHyperParameterTuningJobConfigTypeDef, _OptionalHyperParameterTuningJobConfigTypeDef
):
    pass


AppImageConfigDetailsTypeDef = TypedDict(
    "AppImageConfigDetailsTypeDef",
    {
        "AppImageConfigArn": str,
        "AppImageConfigName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "KernelGatewayImageConfig": KernelGatewayImageConfigTypeDef,
    },
)

_RequiredCreateAppImageConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppImageConfigRequestRequestTypeDef",
    {
        "AppImageConfigName": str,
    },
)
_OptionalCreateAppImageConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppImageConfigRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "KernelGatewayImageConfig": KernelGatewayImageConfigTypeDef,
    },
    total=False,
)


class CreateAppImageConfigRequestRequestTypeDef(
    _RequiredCreateAppImageConfigRequestRequestTypeDef,
    _OptionalCreateAppImageConfigRequestRequestTypeDef,
):
    pass


DescribeAppImageConfigResponseTypeDef = TypedDict(
    "DescribeAppImageConfigResponseTypeDef",
    {
        "AppImageConfigArn": str,
        "AppImageConfigName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "KernelGatewayImageConfig": KernelGatewayImageConfigTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateAppImageConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppImageConfigRequestRequestTypeDef",
    {
        "AppImageConfigName": str,
    },
)
_OptionalUpdateAppImageConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppImageConfigRequestRequestTypeDef",
    {
        "KernelGatewayImageConfig": KernelGatewayImageConfigTypeDef,
    },
    total=False,
)


class UpdateAppImageConfigRequestRequestTypeDef(
    _RequiredUpdateAppImageConfigRequestRequestTypeDef,
    _OptionalUpdateAppImageConfigRequestRequestTypeDef,
):
    pass


ListLabelingJobsForWorkteamResponseTypeDef = TypedDict(
    "ListLabelingJobsForWorkteamResponseTypeDef",
    {
        "LabelingJobSummaryList": List[LabelingJobForWorkteamSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredLabelingJobInputConfigTypeDef = TypedDict(
    "_RequiredLabelingJobInputConfigTypeDef",
    {
        "DataSource": LabelingJobDataSourceTypeDef,
    },
)
_OptionalLabelingJobInputConfigTypeDef = TypedDict(
    "_OptionalLabelingJobInputConfigTypeDef",
    {
        "DataAttributes": LabelingJobDataAttributesTypeDef,
    },
    total=False,
)


class LabelingJobInputConfigTypeDef(
    _RequiredLabelingJobInputConfigTypeDef, _OptionalLabelingJobInputConfigTypeDef
):
    pass


_RequiredCreateWorkteamRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkteamRequestRequestTypeDef",
    {
        "WorkteamName": str,
        "MemberDefinitions": Sequence[MemberDefinitionTypeDef],
        "Description": str,
    },
)
_OptionalCreateWorkteamRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkteamRequestRequestTypeDef",
    {
        "WorkforceName": str,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWorkteamRequestRequestTypeDef(
    _RequiredCreateWorkteamRequestRequestTypeDef, _OptionalCreateWorkteamRequestRequestTypeDef
):
    pass


_RequiredUpdateWorkteamRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkteamRequestRequestTypeDef",
    {
        "WorkteamName": str,
    },
)
_OptionalUpdateWorkteamRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkteamRequestRequestTypeDef",
    {
        "MemberDefinitions": Sequence[MemberDefinitionTypeDef],
        "Description": str,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
    },
    total=False,
)


class UpdateWorkteamRequestRequestTypeDef(
    _RequiredUpdateWorkteamRequestRequestTypeDef, _OptionalUpdateWorkteamRequestRequestTypeDef
):
    pass


WorkteamTypeDef = TypedDict(
    "WorkteamTypeDef",
    {
        "WorkteamName": str,
        "MemberDefinitions": List[MemberDefinitionTypeDef],
        "WorkteamArn": str,
        "WorkforceArn": str,
        "ProductListingIds": List[str],
        "Description": str,
        "SubDomain": str,
        "CreateDate": datetime,
        "LastUpdatedDate": datetime,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
    },
)

MonitoringAlertSummaryTypeDef = TypedDict(
    "MonitoringAlertSummaryTypeDef",
    {
        "MonitoringAlertName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "AlertStatus": MonitoringAlertStatusType,
        "DatapointsToAlert": int,
        "EvaluationPeriod": int,
        "Actions": MonitoringAlertActionsTypeDef,
    },
)

ContainerDefinitionTypeDef = TypedDict(
    "ContainerDefinitionTypeDef",
    {
        "ContainerHostname": str,
        "Image": str,
        "ImageConfig": ImageConfigTypeDef,
        "Mode": ContainerModeType,
        "ModelDataUrl": str,
        "Environment": Mapping[str, str],
        "ModelPackageName": str,
        "InferenceSpecificationName": str,
        "MultiModelConfig": MultiModelConfigTypeDef,
        "ModelDataSource": ModelDataSourceTypeDef,
    },
    total=False,
)

ModelVariantConfigSummaryTypeDef = TypedDict(
    "ModelVariantConfigSummaryTypeDef",
    {
        "ModelName": str,
        "VariantName": str,
        "InfrastructureConfig": ModelInfrastructureConfigTypeDef,
        "Status": ModelVariantStatusType,
    },
)

ModelVariantConfigTypeDef = TypedDict(
    "ModelVariantConfigTypeDef",
    {
        "ModelName": str,
        "VariantName": str,
        "InfrastructureConfig": ModelInfrastructureConfigTypeDef,
    },
)

_RequiredAdditionalInferenceSpecificationDefinitionTypeDef = TypedDict(
    "_RequiredAdditionalInferenceSpecificationDefinitionTypeDef",
    {
        "Name": str,
        "Containers": Sequence[ModelPackageContainerDefinitionTypeDef],
    },
)
_OptionalAdditionalInferenceSpecificationDefinitionTypeDef = TypedDict(
    "_OptionalAdditionalInferenceSpecificationDefinitionTypeDef",
    {
        "Description": str,
        "SupportedTransformInstanceTypes": Sequence[TransformInstanceTypeType],
        "SupportedRealtimeInferenceInstanceTypes": Sequence[ProductionVariantInstanceTypeType],
        "SupportedContentTypes": Sequence[str],
        "SupportedResponseMIMETypes": Sequence[str],
    },
    total=False,
)


class AdditionalInferenceSpecificationDefinitionTypeDef(
    _RequiredAdditionalInferenceSpecificationDefinitionTypeDef,
    _OptionalAdditionalInferenceSpecificationDefinitionTypeDef,
):
    pass


InferenceSpecificationTypeDef = TypedDict(
    "InferenceSpecificationTypeDef",
    {
        "Containers": List[ModelPackageContainerDefinitionTypeDef],
        "SupportedTransformInstanceTypes": List[TransformInstanceTypeType],
        "SupportedRealtimeInferenceInstanceTypes": List[ProductionVariantInstanceTypeType],
        "SupportedContentTypes": List[str],
        "SupportedResponseMIMETypes": List[str],
    },
)

ListModelMetadataRequestListModelMetadataPaginateTypeDef = TypedDict(
    "ListModelMetadataRequestListModelMetadataPaginateTypeDef",
    {
        "SearchExpression": ModelMetadataSearchExpressionTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListModelMetadataRequestRequestTypeDef = TypedDict(
    "ListModelMetadataRequestRequestTypeDef",
    {
        "SearchExpression": ModelMetadataSearchExpressionTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredBatchTransformInputTypeDef = TypedDict(
    "_RequiredBatchTransformInputTypeDef",
    {
        "DataCapturedDestinationS3Uri": str,
        "DatasetFormat": MonitoringDatasetFormatTypeDef,
        "LocalPath": str,
    },
)
_OptionalBatchTransformInputTypeDef = TypedDict(
    "_OptionalBatchTransformInputTypeDef",
    {
        "S3InputMode": ProcessingS3InputModeType,
        "S3DataDistributionType": ProcessingS3DataDistributionTypeType,
        "FeaturesAttribute": str,
        "InferenceAttribute": str,
        "ProbabilityAttribute": str,
        "ProbabilityThresholdAttribute": float,
        "StartTimeOffset": str,
        "EndTimeOffset": str,
    },
    total=False,
)


class BatchTransformInputTypeDef(
    _RequiredBatchTransformInputTypeDef, _OptionalBatchTransformInputTypeDef
):
    pass


_RequiredMonitoringOutputConfigTypeDef = TypedDict(
    "_RequiredMonitoringOutputConfigTypeDef",
    {
        "MonitoringOutputs": Sequence[MonitoringOutputTypeDef],
    },
)
_OptionalMonitoringOutputConfigTypeDef = TypedDict(
    "_OptionalMonitoringOutputConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class MonitoringOutputConfigTypeDef(
    _RequiredMonitoringOutputConfigTypeDef, _OptionalMonitoringOutputConfigTypeDef
):
    pass


_RequiredCreateFeatureGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFeatureGroupRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
        "RecordIdentifierFeatureName": str,
        "EventTimeFeatureName": str,
        "FeatureDefinitions": Sequence[FeatureDefinitionTypeDef],
    },
)
_OptionalCreateFeatureGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFeatureGroupRequestRequestTypeDef",
    {
        "OnlineStoreConfig": OnlineStoreConfigTypeDef,
        "OfflineStoreConfig": OfflineStoreConfigTypeDef,
        "RoleArn": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFeatureGroupRequestRequestTypeDef(
    _RequiredCreateFeatureGroupRequestRequestTypeDef,
    _OptionalCreateFeatureGroupRequestRequestTypeDef,
):
    pass


DescribeFeatureGroupResponseTypeDef = TypedDict(
    "DescribeFeatureGroupResponseTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "RecordIdentifierFeatureName": str,
        "EventTimeFeatureName": str,
        "FeatureDefinitions": List[FeatureDefinitionTypeDef],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "OnlineStoreConfig": OnlineStoreConfigTypeDef,
        "OfflineStoreConfig": OfflineStoreConfigTypeDef,
        "RoleArn": str,
        "FeatureGroupStatus": FeatureGroupStatusType,
        "OfflineStoreStatus": OfflineStoreStatusTypeDef,
        "LastUpdateStatus": LastUpdateStatusTypeDef,
        "FailureReason": str,
        "Description": str,
        "NextToken": str,
        "OnlineStoreTotalSizeBytes": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FeatureGroupTypeDef = TypedDict(
    "FeatureGroupTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "RecordIdentifierFeatureName": str,
        "EventTimeFeatureName": str,
        "FeatureDefinitions": List[FeatureDefinitionTypeDef],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "OnlineStoreConfig": OnlineStoreConfigTypeDef,
        "OfflineStoreConfig": OfflineStoreConfigTypeDef,
        "RoleArn": str,
        "FeatureGroupStatus": FeatureGroupStatusType,
        "OfflineStoreStatus": OfflineStoreStatusTypeDef,
        "LastUpdateStatus": LastUpdateStatusTypeDef,
        "FailureReason": str,
        "Description": str,
        "Tags": List[TagTypeDef],
    },
)

_RequiredUpdateFeatureGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFeatureGroupRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
    },
)
_OptionalUpdateFeatureGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFeatureGroupRequestRequestTypeDef",
    {
        "FeatureAdditions": Sequence[FeatureDefinitionTypeDef],
        "OnlineStoreConfig": OnlineStoreConfigUpdateTypeDef,
    },
    total=False,
)


class UpdateFeatureGroupRequestRequestTypeDef(
    _RequiredUpdateFeatureGroupRequestRequestTypeDef,
    _OptionalUpdateFeatureGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateCompilationJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCompilationJobRequestRequestTypeDef",
    {
        "CompilationJobName": str,
        "RoleArn": str,
        "OutputConfig": OutputConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
    },
)
_OptionalCreateCompilationJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCompilationJobRequestRequestTypeDef",
    {
        "ModelPackageVersionArn": str,
        "InputConfig": InputConfigTypeDef,
        "VpcConfig": NeoVpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateCompilationJobRequestRequestTypeDef(
    _RequiredCreateCompilationJobRequestRequestTypeDef,
    _OptionalCreateCompilationJobRequestRequestTypeDef,
):
    pass


DescribeCompilationJobResponseTypeDef = TypedDict(
    "DescribeCompilationJobResponseTypeDef",
    {
        "CompilationJobName": str,
        "CompilationJobArn": str,
        "CompilationJobStatus": CompilationJobStatusType,
        "CompilationStartTime": datetime,
        "CompilationEndTime": datetime,
        "StoppingCondition": StoppingConditionTypeDef,
        "InferenceImage": str,
        "ModelPackageVersionArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "ModelArtifacts": ModelArtifactsTypeDef,
        "ModelDigests": ModelDigestsTypeDef,
        "RoleArn": str,
        "InputConfig": InputConfigTypeDef,
        "OutputConfig": OutputConfigTypeDef,
        "VpcConfig": NeoVpcConfigTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PendingDeploymentSummaryTypeDef = TypedDict(
    "PendingDeploymentSummaryTypeDef",
    {
        "EndpointConfigName": str,
        "ProductionVariants": List[PendingProductionVariantSummaryTypeDef],
        "StartTime": datetime,
        "ShadowProductionVariants": List[PendingProductionVariantSummaryTypeDef],
    },
)

_RequiredProcessingOutputConfigTypeDef = TypedDict(
    "_RequiredProcessingOutputConfigTypeDef",
    {
        "Outputs": Sequence[ProcessingOutputTypeDef],
    },
)
_OptionalProcessingOutputConfigTypeDef = TypedDict(
    "_OptionalProcessingOutputConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class ProcessingOutputConfigTypeDef(
    _RequiredProcessingOutputConfigTypeDef, _OptionalProcessingOutputConfigTypeDef
):
    pass


_RequiredGetSearchSuggestionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSearchSuggestionsRequestRequestTypeDef",
    {
        "Resource": ResourceTypeType,
    },
)
_OptionalGetSearchSuggestionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSearchSuggestionsRequestRequestTypeDef",
    {
        "SuggestionQuery": SuggestionQueryTypeDef,
    },
    total=False,
)


class GetSearchSuggestionsRequestRequestTypeDef(
    _RequiredGetSearchSuggestionsRequestRequestTypeDef,
    _OptionalGetSearchSuggestionsRequestRequestTypeDef,
):
    pass


_RequiredCreateProjectInputRequestTypeDef = TypedDict(
    "_RequiredCreateProjectInputRequestTypeDef",
    {
        "ProjectName": str,
        "ServiceCatalogProvisioningDetails": ServiceCatalogProvisioningDetailsTypeDef,
    },
)
_OptionalCreateProjectInputRequestTypeDef = TypedDict(
    "_OptionalCreateProjectInputRequestTypeDef",
    {
        "ProjectDescription": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateProjectInputRequestTypeDef(
    _RequiredCreateProjectInputRequestTypeDef, _OptionalCreateProjectInputRequestTypeDef
):
    pass


DescribeProjectOutputTypeDef = TypedDict(
    "DescribeProjectOutputTypeDef",
    {
        "ProjectArn": str,
        "ProjectName": str,
        "ProjectId": str,
        "ProjectDescription": str,
        "ServiceCatalogProvisioningDetails": ServiceCatalogProvisioningDetailsTypeDef,
        "ServiceCatalogProvisionedProductDetails": ServiceCatalogProvisionedProductDetailsTypeDef,
        "ProjectStatus": ProjectStatusType,
        "CreatedBy": UserContextTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ProjectTypeDef = TypedDict(
    "ProjectTypeDef",
    {
        "ProjectArn": str,
        "ProjectName": str,
        "ProjectId": str,
        "ProjectDescription": str,
        "ServiceCatalogProvisioningDetails": ServiceCatalogProvisioningDetailsTypeDef,
        "ServiceCatalogProvisionedProductDetails": ServiceCatalogProvisionedProductDetailsTypeDef,
        "ProjectStatus": ProjectStatusType,
        "CreatedBy": UserContextTypeDef,
        "CreationTime": datetime,
        "Tags": List[TagTypeDef],
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
    },
)

_RequiredUpdateProjectInputRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectInputRequestTypeDef",
    {
        "ProjectName": str,
    },
)
_OptionalUpdateProjectInputRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectInputRequestTypeDef",
    {
        "ProjectDescription": str,
        "ServiceCatalogProvisioningUpdateDetails": ServiceCatalogProvisioningUpdateDetailsTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class UpdateProjectInputRequestTypeDef(
    _RequiredUpdateProjectInputRequestTypeDef, _OptionalUpdateProjectInputRequestTypeDef
):
    pass


_RequiredHumanLoopConfigTypeDef = TypedDict(
    "_RequiredHumanLoopConfigTypeDef",
    {
        "WorkteamArn": str,
        "HumanTaskUiArn": str,
        "TaskTitle": str,
        "TaskDescription": str,
        "TaskCount": int,
    },
)
_OptionalHumanLoopConfigTypeDef = TypedDict(
    "_OptionalHumanLoopConfigTypeDef",
    {
        "TaskAvailabilityLifetimeInSeconds": int,
        "TaskTimeLimitInSeconds": int,
        "TaskKeywords": Sequence[str],
        "PublicWorkforceTaskPrice": PublicWorkforceTaskPriceTypeDef,
    },
    total=False,
)


class HumanLoopConfigTypeDef(_RequiredHumanLoopConfigTypeDef, _OptionalHumanLoopConfigTypeDef):
    pass


_RequiredHumanTaskConfigTypeDef = TypedDict(
    "_RequiredHumanTaskConfigTypeDef",
    {
        "WorkteamArn": str,
        "UiConfig": UiConfigTypeDef,
        "PreHumanTaskLambdaArn": str,
        "TaskTitle": str,
        "TaskDescription": str,
        "NumberOfHumanWorkersPerDataObject": int,
        "TaskTimeLimitInSeconds": int,
        "AnnotationConsolidationConfig": AnnotationConsolidationConfigTypeDef,
    },
)
_OptionalHumanTaskConfigTypeDef = TypedDict(
    "_OptionalHumanTaskConfigTypeDef",
    {
        "TaskKeywords": Sequence[str],
        "TaskAvailabilityLifetimeInSeconds": int,
        "MaxConcurrentTaskCount": int,
        "PublicWorkforceTaskPrice": PublicWorkforceTaskPriceTypeDef,
    },
    total=False,
)


class HumanTaskConfigTypeDef(_RequiredHumanTaskConfigTypeDef, _OptionalHumanTaskConfigTypeDef):
    pass


DescribePipelineExecutionResponseTypeDef = TypedDict(
    "DescribePipelineExecutionResponseTypeDef",
    {
        "PipelineArn": str,
        "PipelineExecutionArn": str,
        "PipelineExecutionDisplayName": str,
        "PipelineExecutionStatus": PipelineExecutionStatusType,
        "PipelineExecutionDescription": str,
        "PipelineExperimentConfig": PipelineExperimentConfigTypeDef,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedBy": UserContextTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
        "SelectiveExecutionConfig": SelectiveExecutionConfigTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PipelineExecutionTypeDef = TypedDict(
    "PipelineExecutionTypeDef",
    {
        "PipelineArn": str,
        "PipelineExecutionArn": str,
        "PipelineExecutionDisplayName": str,
        "PipelineExecutionStatus": PipelineExecutionStatusType,
        "PipelineExecutionDescription": str,
        "PipelineExperimentConfig": PipelineExperimentConfigTypeDef,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedBy": UserContextTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
        "PipelineParameters": List[ParameterTypeDef],
        "SelectiveExecutionConfig": SelectiveExecutionConfigTypeDef,
    },
)

_RequiredStartPipelineExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredStartPipelineExecutionRequestRequestTypeDef",
    {
        "PipelineName": str,
        "ClientRequestToken": str,
    },
)
_OptionalStartPipelineExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalStartPipelineExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionDisplayName": str,
        "PipelineParameters": Sequence[ParameterTypeDef],
        "PipelineExecutionDescription": str,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
        "SelectiveExecutionConfig": SelectiveExecutionConfigTypeDef,
    },
    total=False,
)


class StartPipelineExecutionRequestRequestTypeDef(
    _RequiredStartPipelineExecutionRequestRequestTypeDef,
    _OptionalStartPipelineExecutionRequestRequestTypeDef,
):
    pass


_RequiredAlgorithmSpecificationTypeDef = TypedDict(
    "_RequiredAlgorithmSpecificationTypeDef",
    {
        "TrainingInputMode": TrainingInputModeType,
    },
)
_OptionalAlgorithmSpecificationTypeDef = TypedDict(
    "_OptionalAlgorithmSpecificationTypeDef",
    {
        "TrainingImage": str,
        "AlgorithmName": str,
        "MetricDefinitions": Sequence[MetricDefinitionTypeDef],
        "EnableSageMakerMetricsTimeSeries": bool,
        "ContainerEntrypoint": Sequence[str],
        "ContainerArguments": Sequence[str],
        "TrainingImageConfig": TrainingImageConfigTypeDef,
    },
    total=False,
)


class AlgorithmSpecificationTypeDef(
    _RequiredAlgorithmSpecificationTypeDef, _OptionalAlgorithmSpecificationTypeDef
):
    pass


_RequiredTransformInputTypeDef = TypedDict(
    "_RequiredTransformInputTypeDef",
    {
        "DataSource": TransformDataSourceTypeDef,
    },
)
_OptionalTransformInputTypeDef = TypedDict(
    "_OptionalTransformInputTypeDef",
    {
        "ContentType": str,
        "CompressionType": CompressionTypeType,
        "SplitType": SplitTypeType,
    },
    total=False,
)


class TransformInputTypeDef(_RequiredTransformInputTypeDef, _OptionalTransformInputTypeDef):
    pass


DescribeWorkforceResponseTypeDef = TypedDict(
    "DescribeWorkforceResponseTypeDef",
    {
        "Workforce": WorkforceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWorkforcesResponseTypeDef = TypedDict(
    "ListWorkforcesResponseTypeDef",
    {
        "Workforces": List[WorkforceTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateWorkforceResponseTypeDef = TypedDict(
    "UpdateWorkforceResponseTypeDef",
    {
        "Workforce": WorkforceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListArtifactsResponseTypeDef = TypedDict(
    "ListArtifactsResponseTypeDef",
    {
        "ArtifactSummaries": List[ArtifactSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoMLProblemTypeConfigTypeDef = TypedDict(
    "AutoMLProblemTypeConfigTypeDef",
    {
        "ImageClassificationJobConfig": ImageClassificationJobConfigTypeDef,
        "TextClassificationJobConfig": TextClassificationJobConfigTypeDef,
        "TabularJobConfig": TabularJobConfigTypeDef,
        "TimeSeriesForecastingJobConfig": TimeSeriesForecastingJobConfigTypeDef,
    },
    total=False,
)

_RequiredCreateAutoMLJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAutoMLJobRequestRequestTypeDef",
    {
        "AutoMLJobName": str,
        "InputDataConfig": Sequence[AutoMLChannelTypeDef],
        "OutputDataConfig": AutoMLOutputDataConfigTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateAutoMLJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAutoMLJobRequestRequestTypeDef",
    {
        "ProblemType": ProblemTypeType,
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "AutoMLJobConfig": AutoMLJobConfigTypeDef,
        "GenerateCandidateDefinitionsOnly": bool,
        "Tags": Sequence[TagTypeDef],
        "ModelDeployConfig": ModelDeployConfigTypeDef,
    },
    total=False,
)


class CreateAutoMLJobRequestRequestTypeDef(
    _RequiredCreateAutoMLJobRequestRequestTypeDef, _OptionalCreateAutoMLJobRequestRequestTypeDef
):
    pass


PipelineExecutionStepTypeDef = TypedDict(
    "PipelineExecutionStepTypeDef",
    {
        "StepName": str,
        "StepDisplayName": str,
        "StepDescription": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "StepStatus": StepStatusType,
        "CacheHitResult": CacheHitResultTypeDef,
        "AttemptCount": int,
        "FailureReason": str,
        "Metadata": PipelineExecutionStepMetadataTypeDef,
        "SelectiveExecutionResult": SelectiveExecutionResultTypeDef,
    },
)

DescribeAutoMLJobResponseTypeDef = TypedDict(
    "DescribeAutoMLJobResponseTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "InputDataConfig": List[AutoMLChannelTypeDef],
        "OutputDataConfig": AutoMLOutputDataConfigTypeDef,
        "RoleArn": str,
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "ProblemType": ProblemTypeType,
        "AutoMLJobConfig": AutoMLJobConfigTypeDef,
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "PartialFailureReasons": List[AutoMLPartialFailureReasonTypeDef],
        "BestCandidate": AutoMLCandidateTypeDef,
        "AutoMLJobStatus": AutoMLJobStatusType,
        "AutoMLJobSecondaryStatus": AutoMLJobSecondaryStatusType,
        "GenerateCandidateDefinitionsOnly": bool,
        "AutoMLJobArtifacts": AutoMLJobArtifactsTypeDef,
        "ResolvedAttributes": ResolvedAttributesTypeDef,
        "ModelDeployConfig": ModelDeployConfigTypeDef,
        "ModelDeployResult": ModelDeployResultTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCandidatesForAutoMLJobResponseTypeDef = TypedDict(
    "ListCandidatesForAutoMLJobResponseTypeDef",
    {
        "Candidates": List[AutoMLCandidateTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeploymentConfigTypeDef = TypedDict(
    "DeploymentConfigTypeDef",
    {
        "BlueGreenUpdatePolicy": BlueGreenUpdatePolicyTypeDef,
        "AutoRollbackConfiguration": AutoRollbackConfigTypeDef,
        "RollingUpdatePolicy": RollingUpdatePolicyTypeDef,
    },
    total=False,
)

RecommendationJobInputConfigTypeDef = TypedDict(
    "RecommendationJobInputConfigTypeDef",
    {
        "ModelPackageVersionArn": str,
        "JobDurationInSeconds": int,
        "TrafficPattern": TrafficPatternTypeDef,
        "ResourceLimit": RecommendationJobResourceLimitTypeDef,
        "EndpointConfigurations": Sequence[EndpointInputConfigurationTypeDef],
        "VolumeKmsKeyId": str,
        "ContainerConfig": RecommendationJobContainerConfigTypeDef,
        "Endpoints": Sequence[EndpointInfoTypeDef],
        "VpcConfig": RecommendationJobVpcConfigTypeDef,
        "ModelName": str,
    },
    total=False,
)

ExplainerConfigTypeDef = TypedDict(
    "ExplainerConfigTypeDef",
    {
        "ClarifyExplainerConfig": ClarifyExplainerConfigTypeDef,
    },
    total=False,
)

_RequiredCreateSpaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSpaceRequestRequestTypeDef",
    {
        "DomainId": str,
        "SpaceName": str,
    },
)
_OptionalCreateSpaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSpaceRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "SpaceSettings": SpaceSettingsTypeDef,
    },
    total=False,
)


class CreateSpaceRequestRequestTypeDef(
    _RequiredCreateSpaceRequestRequestTypeDef, _OptionalCreateSpaceRequestRequestTypeDef
):
    pass


DescribeSpaceResponseTypeDef = TypedDict(
    "DescribeSpaceResponseTypeDef",
    {
        "DomainId": str,
        "SpaceArn": str,
        "SpaceName": str,
        "HomeEfsFileSystemUid": str,
        "Status": SpaceStatusType,
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "FailureReason": str,
        "SpaceSettings": SpaceSettingsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateSpaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSpaceRequestRequestTypeDef",
    {
        "DomainId": str,
        "SpaceName": str,
    },
)
_OptionalUpdateSpaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSpaceRequestRequestTypeDef",
    {
        "SpaceSettings": SpaceSettingsTypeDef,
    },
    total=False,
)


class UpdateSpaceRequestRequestTypeDef(
    _RequiredUpdateSpaceRequestRequestTypeDef, _OptionalUpdateSpaceRequestRequestTypeDef
):
    pass


_RequiredCreateDomainRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "AuthMode": AuthModeType,
        "DefaultUserSettings": UserSettingsTypeDef,
        "SubnetIds": Sequence[str],
        "VpcId": str,
    },
)
_OptionalCreateDomainRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDomainRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "AppNetworkAccessType": AppNetworkAccessTypeType,
        "HomeEfsFileSystemKmsKeyId": str,
        "KmsKeyId": str,
        "AppSecurityGroupManagement": AppSecurityGroupManagementType,
        "DomainSettings": DomainSettingsTypeDef,
        "DefaultSpaceSettings": DefaultSpaceSettingsTypeDef,
    },
    total=False,
)


class CreateDomainRequestRequestTypeDef(
    _RequiredCreateDomainRequestRequestTypeDef, _OptionalCreateDomainRequestRequestTypeDef
):
    pass


_RequiredCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserProfileRequestRequestTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
    },
)
_OptionalCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserProfileRequestRequestTypeDef",
    {
        "SingleSignOnUserIdentifier": str,
        "SingleSignOnUserValue": str,
        "Tags": Sequence[TagTypeDef],
        "UserSettings": UserSettingsTypeDef,
    },
    total=False,
)


class CreateUserProfileRequestRequestTypeDef(
    _RequiredCreateUserProfileRequestRequestTypeDef, _OptionalCreateUserProfileRequestRequestTypeDef
):
    pass


DescribeDomainResponseTypeDef = TypedDict(
    "DescribeDomainResponseTypeDef",
    {
        "DomainArn": str,
        "DomainId": str,
        "DomainName": str,
        "HomeEfsFileSystemId": str,
        "SingleSignOnManagedApplicationInstanceId": str,
        "Status": DomainStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "AuthMode": AuthModeType,
        "DefaultUserSettings": UserSettingsTypeDef,
        "AppNetworkAccessType": AppNetworkAccessTypeType,
        "HomeEfsFileSystemKmsKeyId": str,
        "SubnetIds": List[str],
        "Url": str,
        "VpcId": str,
        "KmsKeyId": str,
        "DomainSettings": DomainSettingsTypeDef,
        "AppSecurityGroupManagement": AppSecurityGroupManagementType,
        "SecurityGroupIdForDomainBoundary": str,
        "DefaultSpaceSettings": DefaultSpaceSettingsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeUserProfileResponseTypeDef = TypedDict(
    "DescribeUserProfileResponseTypeDef",
    {
        "DomainId": str,
        "UserProfileArn": str,
        "UserProfileName": str,
        "HomeEfsFileSystemUid": str,
        "Status": UserProfileStatusType,
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "FailureReason": str,
        "SingleSignOnUserIdentifier": str,
        "SingleSignOnUserValue": str,
        "UserSettings": UserSettingsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateDomainRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDomainRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalUpdateDomainRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDomainRequestRequestTypeDef",
    {
        "DefaultUserSettings": UserSettingsTypeDef,
        "DomainSettingsForUpdate": DomainSettingsForUpdateTypeDef,
        "DefaultSpaceSettings": DefaultSpaceSettingsTypeDef,
        "AppSecurityGroupManagement": AppSecurityGroupManagementType,
    },
    total=False,
)


class UpdateDomainRequestRequestTypeDef(
    _RequiredUpdateDomainRequestRequestTypeDef, _OptionalUpdateDomainRequestRequestTypeDef
):
    pass


_RequiredUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserProfileRequestRequestTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
    },
)
_OptionalUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserProfileRequestRequestTypeDef",
    {
        "UserSettings": UserSettingsTypeDef,
    },
    total=False,
)


class UpdateUserProfileRequestRequestTypeDef(
    _RequiredUpdateUserProfileRequestRequestTypeDef, _OptionalUpdateUserProfileRequestRequestTypeDef
):
    pass


_RequiredHyperParameterTrainingJobDefinitionTypeDef = TypedDict(
    "_RequiredHyperParameterTrainingJobDefinitionTypeDef",
    {
        "AlgorithmSpecification": HyperParameterAlgorithmSpecificationTypeDef,
        "RoleArn": str,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
    },
)
_OptionalHyperParameterTrainingJobDefinitionTypeDef = TypedDict(
    "_OptionalHyperParameterTrainingJobDefinitionTypeDef",
    {
        "DefinitionName": str,
        "TuningObjective": HyperParameterTuningJobObjectiveTypeDef,
        "HyperParameterRanges": ParameterRangesTypeDef,
        "StaticHyperParameters": Mapping[str, str],
        "InputDataConfig": Sequence[ChannelTypeDef],
        "VpcConfig": VpcConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigTypeDef,
        "RetryStrategy": RetryStrategyTypeDef,
        "HyperParameterTuningResourceConfig": HyperParameterTuningResourceConfigTypeDef,
        "Environment": Mapping[str, str],
    },
    total=False,
)


class HyperParameterTrainingJobDefinitionTypeDef(
    _RequiredHyperParameterTrainingJobDefinitionTypeDef,
    _OptionalHyperParameterTrainingJobDefinitionTypeDef,
):
    pass


_RequiredTrainingJobDefinitionTypeDef = TypedDict(
    "_RequiredTrainingJobDefinitionTypeDef",
    {
        "TrainingInputMode": TrainingInputModeType,
        "InputDataConfig": Sequence[ChannelTypeDef],
        "OutputDataConfig": OutputDataConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
    },
)
_OptionalTrainingJobDefinitionTypeDef = TypedDict(
    "_OptionalTrainingJobDefinitionTypeDef",
    {
        "HyperParameters": Mapping[str, str],
    },
    total=False,
)


class TrainingJobDefinitionTypeDef(
    _RequiredTrainingJobDefinitionTypeDef, _OptionalTrainingJobDefinitionTypeDef
):
    pass


InferenceRecommendationsJobStepTypeDef = TypedDict(
    "InferenceRecommendationsJobStepTypeDef",
    {
        "StepType": Literal["BENCHMARK"],
        "JobName": str,
        "Status": RecommendationJobStatusType,
        "InferenceBenchmark": RecommendationJobInferenceBenchmarkTypeDef,
    },
)

ListAssociationsResponseTypeDef = TypedDict(
    "ListAssociationsResponseTypeDef",
    {
        "AssociationSummaries": List[AssociationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TrialTypeDef = TypedDict(
    "TrialTypeDef",
    {
        "TrialName": str,
        "TrialArn": str,
        "DisplayName": str,
        "ExperimentName": str,
        "Source": TrialSourceTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "Tags": List[TagTypeDef],
        "TrialComponentSummaries": List[TrialComponentSimpleSummaryTypeDef],
    },
)

ListTrialComponentsResponseTypeDef = TypedDict(
    "ListTrialComponentsResponseTypeDef",
    {
        "TrialComponentSummaries": List[TrialComponentSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredTrainingSpecificationTypeDef = TypedDict(
    "_RequiredTrainingSpecificationTypeDef",
    {
        "TrainingImage": str,
        "SupportedTrainingInstanceTypes": Sequence[TrainingInstanceTypeType],
        "TrainingChannels": Sequence[ChannelSpecificationTypeDef],
    },
)
_OptionalTrainingSpecificationTypeDef = TypedDict(
    "_OptionalTrainingSpecificationTypeDef",
    {
        "TrainingImageDigest": str,
        "SupportedHyperParameters": Sequence[HyperParameterSpecificationTypeDef],
        "SupportsDistributedTraining": bool,
        "MetricDefinitions": Sequence[MetricDefinitionTypeDef],
        "SupportedTuningJobObjectiveMetrics": Sequence[HyperParameterTuningJobObjectiveTypeDef],
    },
    total=False,
)


class TrainingSpecificationTypeDef(
    _RequiredTrainingSpecificationTypeDef, _OptionalTrainingSpecificationTypeDef
):
    pass


ListAppImageConfigsResponseTypeDef = TypedDict(
    "ListAppImageConfigsResponseTypeDef",
    {
        "NextToken": str,
        "AppImageConfigs": List[AppImageConfigDetailsTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LabelingJobSummaryTypeDef = TypedDict(
    "LabelingJobSummaryTypeDef",
    {
        "LabelingJobName": str,
        "LabelingJobArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LabelingJobStatus": LabelingJobStatusType,
        "LabelCounters": LabelCountersTypeDef,
        "WorkteamArn": str,
        "PreHumanTaskLambdaArn": str,
        "AnnotationConsolidationLambdaArn": str,
        "FailureReason": str,
        "LabelingJobOutput": LabelingJobOutputTypeDef,
        "InputConfig": LabelingJobInputConfigTypeDef,
    },
)

DescribeWorkteamResponseTypeDef = TypedDict(
    "DescribeWorkteamResponseTypeDef",
    {
        "Workteam": WorkteamTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWorkteamsResponseTypeDef = TypedDict(
    "ListWorkteamsResponseTypeDef",
    {
        "Workteams": List[WorkteamTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateWorkteamResponseTypeDef = TypedDict(
    "UpdateWorkteamResponseTypeDef",
    {
        "Workteam": WorkteamTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringAlertsResponseTypeDef = TypedDict(
    "ListMonitoringAlertsResponseTypeDef",
    {
        "MonitoringAlertSummaries": List[MonitoringAlertSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateModelInputRequestTypeDef = TypedDict(
    "_RequiredCreateModelInputRequestTypeDef",
    {
        "ModelName": str,
        "ExecutionRoleArn": str,
    },
)
_OptionalCreateModelInputRequestTypeDef = TypedDict(
    "_OptionalCreateModelInputRequestTypeDef",
    {
        "PrimaryContainer": ContainerDefinitionTypeDef,
        "Containers": Sequence[ContainerDefinitionTypeDef],
        "InferenceExecutionConfig": InferenceExecutionConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "VpcConfig": VpcConfigTypeDef,
        "EnableNetworkIsolation": bool,
    },
    total=False,
)


class CreateModelInputRequestTypeDef(
    _RequiredCreateModelInputRequestTypeDef, _OptionalCreateModelInputRequestTypeDef
):
    pass


DescribeModelOutputTypeDef = TypedDict(
    "DescribeModelOutputTypeDef",
    {
        "ModelName": str,
        "PrimaryContainer": ContainerDefinitionTypeDef,
        "Containers": List[ContainerDefinitionTypeDef],
        "InferenceExecutionConfig": InferenceExecutionConfigTypeDef,
        "ExecutionRoleArn": str,
        "VpcConfig": VpcConfigTypeDef,
        "CreationTime": datetime,
        "ModelArn": str,
        "EnableNetworkIsolation": bool,
        "DeploymentRecommendation": DeploymentRecommendationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelTypeDef = TypedDict(
    "ModelTypeDef",
    {
        "ModelName": str,
        "PrimaryContainer": ContainerDefinitionTypeDef,
        "Containers": List[ContainerDefinitionTypeDef],
        "InferenceExecutionConfig": InferenceExecutionConfigTypeDef,
        "ExecutionRoleArn": str,
        "VpcConfig": VpcConfigTypeDef,
        "CreationTime": datetime,
        "ModelArn": str,
        "EnableNetworkIsolation": bool,
        "Tags": List[TagTypeDef],
        "DeploymentRecommendation": DeploymentRecommendationTypeDef,
    },
)

DescribeInferenceExperimentResponseTypeDef = TypedDict(
    "DescribeInferenceExperimentResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Schedule": InferenceExperimentScheduleTypeDef,
        "Status": InferenceExperimentStatusType,
        "StatusReason": str,
        "Description": str,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
        "EndpointMetadata": EndpointMetadataTypeDef,
        "ModelVariants": List[ModelVariantConfigSummaryTypeDef],
        "DataStorageConfig": InferenceExperimentDataStorageConfigTypeDef,
        "ShadowModeConfig": ShadowModeConfigTypeDef,
        "KmsKey": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateInferenceExperimentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInferenceExperimentRequestRequestTypeDef",
    {
        "Name": str,
        "Type": Literal["ShadowMode"],
        "RoleArn": str,
        "EndpointName": str,
        "ModelVariants": Sequence[ModelVariantConfigTypeDef],
        "ShadowModeConfig": ShadowModeConfigTypeDef,
    },
)
_OptionalCreateInferenceExperimentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInferenceExperimentRequestRequestTypeDef",
    {
        "Schedule": InferenceExperimentScheduleTypeDef,
        "Description": str,
        "DataStorageConfig": InferenceExperimentDataStorageConfigTypeDef,
        "KmsKey": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateInferenceExperimentRequestRequestTypeDef(
    _RequiredCreateInferenceExperimentRequestRequestTypeDef,
    _OptionalCreateInferenceExperimentRequestRequestTypeDef,
):
    pass


_RequiredStopInferenceExperimentRequestRequestTypeDef = TypedDict(
    "_RequiredStopInferenceExperimentRequestRequestTypeDef",
    {
        "Name": str,
        "ModelVariantActions": Mapping[str, ModelVariantActionType],
    },
)
_OptionalStopInferenceExperimentRequestRequestTypeDef = TypedDict(
    "_OptionalStopInferenceExperimentRequestRequestTypeDef",
    {
        "DesiredModelVariants": Sequence[ModelVariantConfigTypeDef],
        "DesiredState": InferenceExperimentStopDesiredStateType,
        "Reason": str,
    },
    total=False,
)


class StopInferenceExperimentRequestRequestTypeDef(
    _RequiredStopInferenceExperimentRequestRequestTypeDef,
    _OptionalStopInferenceExperimentRequestRequestTypeDef,
):
    pass


_RequiredUpdateInferenceExperimentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInferenceExperimentRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateInferenceExperimentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInferenceExperimentRequestRequestTypeDef",
    {
        "Schedule": InferenceExperimentScheduleTypeDef,
        "Description": str,
        "ModelVariants": Sequence[ModelVariantConfigTypeDef],
        "DataStorageConfig": InferenceExperimentDataStorageConfigTypeDef,
        "ShadowModeConfig": ShadowModeConfigTypeDef,
    },
    total=False,
)


class UpdateInferenceExperimentRequestRequestTypeDef(
    _RequiredUpdateInferenceExperimentRequestRequestTypeDef,
    _OptionalUpdateInferenceExperimentRequestRequestTypeDef,
):
    pass


_RequiredUpdateModelPackageInputRequestTypeDef = TypedDict(
    "_RequiredUpdateModelPackageInputRequestTypeDef",
    {
        "ModelPackageArn": str,
    },
)
_OptionalUpdateModelPackageInputRequestTypeDef = TypedDict(
    "_OptionalUpdateModelPackageInputRequestTypeDef",
    {
        "ModelApprovalStatus": ModelApprovalStatusType,
        "ApprovalDescription": str,
        "CustomerMetadataProperties": Mapping[str, str],
        "CustomerMetadataPropertiesToRemove": Sequence[str],
        "AdditionalInferenceSpecificationsToAdd": Sequence[
            AdditionalInferenceSpecificationDefinitionTypeDef
        ],
    },
    total=False,
)


class UpdateModelPackageInputRequestTypeDef(
    _RequiredUpdateModelPackageInputRequestTypeDef, _OptionalUpdateModelPackageInputRequestTypeDef
):
    pass


BatchDescribeModelPackageSummaryTypeDef = TypedDict(
    "BatchDescribeModelPackageSummaryTypeDef",
    {
        "ModelPackageGroupName": str,
        "ModelPackageVersion": int,
        "ModelPackageArn": str,
        "ModelPackageDescription": str,
        "CreationTime": datetime,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "ModelPackageStatus": ModelPackageStatusType,
        "ModelApprovalStatus": ModelApprovalStatusType,
    },
)

DataQualityJobInputTypeDef = TypedDict(
    "DataQualityJobInputTypeDef",
    {
        "EndpointInput": EndpointInputTypeDef,
        "BatchTransformInput": BatchTransformInputTypeDef,
    },
    total=False,
)

_RequiredModelBiasJobInputTypeDef = TypedDict(
    "_RequiredModelBiasJobInputTypeDef",
    {
        "GroundTruthS3Input": MonitoringGroundTruthS3InputTypeDef,
    },
)
_OptionalModelBiasJobInputTypeDef = TypedDict(
    "_OptionalModelBiasJobInputTypeDef",
    {
        "EndpointInput": EndpointInputTypeDef,
        "BatchTransformInput": BatchTransformInputTypeDef,
    },
    total=False,
)


class ModelBiasJobInputTypeDef(
    _RequiredModelBiasJobInputTypeDef, _OptionalModelBiasJobInputTypeDef
):
    pass


ModelExplainabilityJobInputTypeDef = TypedDict(
    "ModelExplainabilityJobInputTypeDef",
    {
        "EndpointInput": EndpointInputTypeDef,
        "BatchTransformInput": BatchTransformInputTypeDef,
    },
    total=False,
)

_RequiredModelQualityJobInputTypeDef = TypedDict(
    "_RequiredModelQualityJobInputTypeDef",
    {
        "GroundTruthS3Input": MonitoringGroundTruthS3InputTypeDef,
    },
)
_OptionalModelQualityJobInputTypeDef = TypedDict(
    "_OptionalModelQualityJobInputTypeDef",
    {
        "EndpointInput": EndpointInputTypeDef,
        "BatchTransformInput": BatchTransformInputTypeDef,
    },
    total=False,
)


class ModelQualityJobInputTypeDef(
    _RequiredModelQualityJobInputTypeDef, _OptionalModelQualityJobInputTypeDef
):
    pass


MonitoringInputTypeDef = TypedDict(
    "MonitoringInputTypeDef",
    {
        "EndpointInput": EndpointInputTypeDef,
        "BatchTransformInput": BatchTransformInputTypeDef,
    },
    total=False,
)

_RequiredCreateProcessingJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProcessingJobRequestRequestTypeDef",
    {
        "ProcessingJobName": str,
        "ProcessingResources": ProcessingResourcesTypeDef,
        "AppSpecification": AppSpecificationTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateProcessingJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProcessingJobRequestRequestTypeDef",
    {
        "ProcessingInputs": Sequence[ProcessingInputTypeDef],
        "ProcessingOutputConfig": ProcessingOutputConfigTypeDef,
        "StoppingCondition": ProcessingStoppingConditionTypeDef,
        "Environment": Mapping[str, str],
        "NetworkConfig": NetworkConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "ExperimentConfig": ExperimentConfigTypeDef,
    },
    total=False,
)


class CreateProcessingJobRequestRequestTypeDef(
    _RequiredCreateProcessingJobRequestRequestTypeDef,
    _OptionalCreateProcessingJobRequestRequestTypeDef,
):
    pass


DescribeProcessingJobResponseTypeDef = TypedDict(
    "DescribeProcessingJobResponseTypeDef",
    {
        "ProcessingInputs": List[ProcessingInputTypeDef],
        "ProcessingOutputConfig": ProcessingOutputConfigTypeDef,
        "ProcessingJobName": str,
        "ProcessingResources": ProcessingResourcesTypeDef,
        "StoppingCondition": ProcessingStoppingConditionTypeDef,
        "AppSpecification": AppSpecificationTypeDef,
        "Environment": Dict[str, str],
        "NetworkConfig": NetworkConfigTypeDef,
        "RoleArn": str,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "ProcessingJobArn": str,
        "ProcessingJobStatus": ProcessingJobStatusType,
        "ExitMessage": str,
        "FailureReason": str,
        "ProcessingEndTime": datetime,
        "ProcessingStartTime": datetime,
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "MonitoringScheduleArn": str,
        "AutoMLJobArn": str,
        "TrainingJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ProcessingJobTypeDef = TypedDict(
    "ProcessingJobTypeDef",
    {
        "ProcessingInputs": List[ProcessingInputTypeDef],
        "ProcessingOutputConfig": ProcessingOutputConfigTypeDef,
        "ProcessingJobName": str,
        "ProcessingResources": ProcessingResourcesTypeDef,
        "StoppingCondition": ProcessingStoppingConditionTypeDef,
        "AppSpecification": AppSpecificationTypeDef,
        "Environment": Dict[str, str],
        "NetworkConfig": NetworkConfigTypeDef,
        "RoleArn": str,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "ProcessingJobArn": str,
        "ProcessingJobStatus": ProcessingJobStatusType,
        "ExitMessage": str,
        "FailureReason": str,
        "ProcessingEndTime": datetime,
        "ProcessingStartTime": datetime,
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "MonitoringScheduleArn": str,
        "AutoMLJobArn": str,
        "TrainingJobArn": str,
        "Tags": List[TagTypeDef],
    },
)

_RequiredCreateFlowDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFlowDefinitionRequestRequestTypeDef",
    {
        "FlowDefinitionName": str,
        "HumanLoopConfig": HumanLoopConfigTypeDef,
        "OutputConfig": FlowDefinitionOutputConfigTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateFlowDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFlowDefinitionRequestRequestTypeDef",
    {
        "HumanLoopRequestSource": HumanLoopRequestSourceTypeDef,
        "HumanLoopActivationConfig": HumanLoopActivationConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFlowDefinitionRequestRequestTypeDef(
    _RequiredCreateFlowDefinitionRequestRequestTypeDef,
    _OptionalCreateFlowDefinitionRequestRequestTypeDef,
):
    pass


DescribeFlowDefinitionResponseTypeDef = TypedDict(
    "DescribeFlowDefinitionResponseTypeDef",
    {
        "FlowDefinitionArn": str,
        "FlowDefinitionName": str,
        "FlowDefinitionStatus": FlowDefinitionStatusType,
        "CreationTime": datetime,
        "HumanLoopRequestSource": HumanLoopRequestSourceTypeDef,
        "HumanLoopActivationConfig": HumanLoopActivationConfigTypeDef,
        "HumanLoopConfig": HumanLoopConfigTypeDef,
        "OutputConfig": FlowDefinitionOutputConfigTypeDef,
        "RoleArn": str,
        "FailureReason": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateLabelingJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLabelingJobRequestRequestTypeDef",
    {
        "LabelingJobName": str,
        "LabelAttributeName": str,
        "InputConfig": LabelingJobInputConfigTypeDef,
        "OutputConfig": LabelingJobOutputConfigTypeDef,
        "RoleArn": str,
        "HumanTaskConfig": HumanTaskConfigTypeDef,
    },
)
_OptionalCreateLabelingJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLabelingJobRequestRequestTypeDef",
    {
        "LabelCategoryConfigS3Uri": str,
        "StoppingConditions": LabelingJobStoppingConditionsTypeDef,
        "LabelingJobAlgorithmsConfig": LabelingJobAlgorithmsConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateLabelingJobRequestRequestTypeDef(
    _RequiredCreateLabelingJobRequestRequestTypeDef, _OptionalCreateLabelingJobRequestRequestTypeDef
):
    pass


DescribeLabelingJobResponseTypeDef = TypedDict(
    "DescribeLabelingJobResponseTypeDef",
    {
        "LabelingJobStatus": LabelingJobStatusType,
        "LabelCounters": LabelCountersTypeDef,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "JobReferenceCode": str,
        "LabelingJobName": str,
        "LabelingJobArn": str,
        "LabelAttributeName": str,
        "InputConfig": LabelingJobInputConfigTypeDef,
        "OutputConfig": LabelingJobOutputConfigTypeDef,
        "RoleArn": str,
        "LabelCategoryConfigS3Uri": str,
        "StoppingConditions": LabelingJobStoppingConditionsTypeDef,
        "LabelingJobAlgorithmsConfig": LabelingJobAlgorithmsConfigTypeDef,
        "HumanTaskConfig": HumanTaskConfigTypeDef,
        "Tags": List[TagTypeDef],
        "LabelingJobOutput": LabelingJobOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateTrainingJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrainingJobRequestRequestTypeDef",
    {
        "TrainingJobName": str,
        "AlgorithmSpecification": AlgorithmSpecificationTypeDef,
        "RoleArn": str,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
    },
)
_OptionalCreateTrainingJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrainingJobRequestRequestTypeDef",
    {
        "HyperParameters": Mapping[str, str],
        "InputDataConfig": Sequence[ChannelTypeDef],
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigTypeDef,
        "DebugHookConfig": DebugHookConfigTypeDef,
        "DebugRuleConfigurations": Sequence[DebugRuleConfigurationTypeDef],
        "TensorBoardOutputConfig": TensorBoardOutputConfigTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "ProfilerConfig": ProfilerConfigTypeDef,
        "ProfilerRuleConfigurations": Sequence[ProfilerRuleConfigurationTypeDef],
        "Environment": Mapping[str, str],
        "RetryStrategy": RetryStrategyTypeDef,
    },
    total=False,
)


class CreateTrainingJobRequestRequestTypeDef(
    _RequiredCreateTrainingJobRequestRequestTypeDef, _OptionalCreateTrainingJobRequestRequestTypeDef
):
    pass


DescribeTrainingJobResponseTypeDef = TypedDict(
    "DescribeTrainingJobResponseTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "TuningJobArn": str,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "ModelArtifacts": ModelArtifactsTypeDef,
        "TrainingJobStatus": TrainingJobStatusType,
        "SecondaryStatus": SecondaryStatusType,
        "FailureReason": str,
        "HyperParameters": Dict[str, str],
        "AlgorithmSpecification": AlgorithmSpecificationTypeDef,
        "RoleArn": str,
        "InputDataConfig": List[ChannelTypeDef],
        "OutputDataConfig": OutputDataConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
        "CreationTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "SecondaryStatusTransitions": List[SecondaryStatusTransitionTypeDef],
        "FinalMetricDataList": List[MetricDataTypeDef],
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigTypeDef,
        "TrainingTimeInSeconds": int,
        "BillableTimeInSeconds": int,
        "DebugHookConfig": DebugHookConfigTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "DebugRuleConfigurations": List[DebugRuleConfigurationTypeDef],
        "TensorBoardOutputConfig": TensorBoardOutputConfigTypeDef,
        "DebugRuleEvaluationStatuses": List[DebugRuleEvaluationStatusTypeDef],
        "ProfilerConfig": ProfilerConfigTypeDef,
        "ProfilerRuleConfigurations": List[ProfilerRuleConfigurationTypeDef],
        "ProfilerRuleEvaluationStatuses": List[ProfilerRuleEvaluationStatusTypeDef],
        "ProfilingStatus": ProfilingStatusType,
        "RetryStrategy": RetryStrategyTypeDef,
        "Environment": Dict[str, str],
        "WarmPoolStatus": WarmPoolStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TrainingJobTypeDef = TypedDict(
    "TrainingJobTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "TuningJobArn": str,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "ModelArtifacts": ModelArtifactsTypeDef,
        "TrainingJobStatus": TrainingJobStatusType,
        "SecondaryStatus": SecondaryStatusType,
        "FailureReason": str,
        "HyperParameters": Dict[str, str],
        "AlgorithmSpecification": AlgorithmSpecificationTypeDef,
        "RoleArn": str,
        "InputDataConfig": List[ChannelTypeDef],
        "OutputDataConfig": OutputDataConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
        "CreationTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "SecondaryStatusTransitions": List[SecondaryStatusTransitionTypeDef],
        "FinalMetricDataList": List[MetricDataTypeDef],
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigTypeDef,
        "TrainingTimeInSeconds": int,
        "BillableTimeInSeconds": int,
        "DebugHookConfig": DebugHookConfigTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "DebugRuleConfigurations": List[DebugRuleConfigurationTypeDef],
        "TensorBoardOutputConfig": TensorBoardOutputConfigTypeDef,
        "DebugRuleEvaluationStatuses": List[DebugRuleEvaluationStatusTypeDef],
        "Environment": Dict[str, str],
        "RetryStrategy": RetryStrategyTypeDef,
        "Tags": List[TagTypeDef],
    },
)

_RequiredCreateTransformJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTransformJobRequestRequestTypeDef",
    {
        "TransformJobName": str,
        "ModelName": str,
        "TransformInput": TransformInputTypeDef,
        "TransformOutput": TransformOutputTypeDef,
        "TransformResources": TransformResourcesTypeDef,
    },
)
_OptionalCreateTransformJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTransformJobRequestRequestTypeDef",
    {
        "MaxConcurrentTransforms": int,
        "ModelClientConfig": ModelClientConfigTypeDef,
        "MaxPayloadInMB": int,
        "BatchStrategy": BatchStrategyType,
        "Environment": Mapping[str, str],
        "DataCaptureConfig": BatchDataCaptureConfigTypeDef,
        "DataProcessing": DataProcessingTypeDef,
        "Tags": Sequence[TagTypeDef],
        "ExperimentConfig": ExperimentConfigTypeDef,
    },
    total=False,
)


class CreateTransformJobRequestRequestTypeDef(
    _RequiredCreateTransformJobRequestRequestTypeDef,
    _OptionalCreateTransformJobRequestRequestTypeDef,
):
    pass


DescribeTransformJobResponseTypeDef = TypedDict(
    "DescribeTransformJobResponseTypeDef",
    {
        "TransformJobName": str,
        "TransformJobArn": str,
        "TransformJobStatus": TransformJobStatusType,
        "FailureReason": str,
        "ModelName": str,
        "MaxConcurrentTransforms": int,
        "ModelClientConfig": ModelClientConfigTypeDef,
        "MaxPayloadInMB": int,
        "BatchStrategy": BatchStrategyType,
        "Environment": Dict[str, str],
        "TransformInput": TransformInputTypeDef,
        "TransformOutput": TransformOutputTypeDef,
        "DataCaptureConfig": BatchDataCaptureConfigTypeDef,
        "TransformResources": TransformResourcesTypeDef,
        "CreationTime": datetime,
        "TransformStartTime": datetime,
        "TransformEndTime": datetime,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "DataProcessing": DataProcessingTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredTransformJobDefinitionTypeDef = TypedDict(
    "_RequiredTransformJobDefinitionTypeDef",
    {
        "TransformInput": TransformInputTypeDef,
        "TransformOutput": TransformOutputTypeDef,
        "TransformResources": TransformResourcesTypeDef,
    },
)
_OptionalTransformJobDefinitionTypeDef = TypedDict(
    "_OptionalTransformJobDefinitionTypeDef",
    {
        "MaxConcurrentTransforms": int,
        "MaxPayloadInMB": int,
        "BatchStrategy": BatchStrategyType,
        "Environment": Mapping[str, str],
    },
    total=False,
)


class TransformJobDefinitionTypeDef(
    _RequiredTransformJobDefinitionTypeDef, _OptionalTransformJobDefinitionTypeDef
):
    pass


TransformJobTypeDef = TypedDict(
    "TransformJobTypeDef",
    {
        "TransformJobName": str,
        "TransformJobArn": str,
        "TransformJobStatus": TransformJobStatusType,
        "FailureReason": str,
        "ModelName": str,
        "MaxConcurrentTransforms": int,
        "ModelClientConfig": ModelClientConfigTypeDef,
        "MaxPayloadInMB": int,
        "BatchStrategy": BatchStrategyType,
        "Environment": Dict[str, str],
        "TransformInput": TransformInputTypeDef,
        "TransformOutput": TransformOutputTypeDef,
        "TransformResources": TransformResourcesTypeDef,
        "CreationTime": datetime,
        "TransformStartTime": datetime,
        "TransformEndTime": datetime,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "DataProcessing": DataProcessingTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "Tags": List[TagTypeDef],
    },
)

_RequiredCreateAutoMLJobV2RequestRequestTypeDef = TypedDict(
    "_RequiredCreateAutoMLJobV2RequestRequestTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobInputDataConfig": Sequence[AutoMLJobChannelTypeDef],
        "OutputDataConfig": AutoMLOutputDataConfigTypeDef,
        "AutoMLProblemTypeConfig": AutoMLProblemTypeConfigTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateAutoMLJobV2RequestRequestTypeDef = TypedDict(
    "_OptionalCreateAutoMLJobV2RequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "SecurityConfig": AutoMLSecurityConfigTypeDef,
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "ModelDeployConfig": ModelDeployConfigTypeDef,
        "DataSplitConfig": AutoMLDataSplitConfigTypeDef,
    },
    total=False,
)


class CreateAutoMLJobV2RequestRequestTypeDef(
    _RequiredCreateAutoMLJobV2RequestRequestTypeDef, _OptionalCreateAutoMLJobV2RequestRequestTypeDef
):
    pass


DescribeAutoMLJobV2ResponseTypeDef = TypedDict(
    "DescribeAutoMLJobV2ResponseTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "AutoMLJobInputDataConfig": List[AutoMLJobChannelTypeDef],
        "OutputDataConfig": AutoMLOutputDataConfigTypeDef,
        "RoleArn": str,
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "AutoMLProblemTypeConfig": AutoMLProblemTypeConfigTypeDef,
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "PartialFailureReasons": List[AutoMLPartialFailureReasonTypeDef],
        "BestCandidate": AutoMLCandidateTypeDef,
        "AutoMLJobStatus": AutoMLJobStatusType,
        "AutoMLJobSecondaryStatus": AutoMLJobSecondaryStatusType,
        "ModelDeployConfig": ModelDeployConfigTypeDef,
        "ModelDeployResult": ModelDeployResultTypeDef,
        "DataSplitConfig": AutoMLDataSplitConfigTypeDef,
        "SecurityConfig": AutoMLSecurityConfigTypeDef,
        "AutoMLJobArtifacts": AutoMLJobArtifactsTypeDef,
        "ResolvedAttributes": AutoMLResolvedAttributesTypeDef,
        "AutoMLProblemTypeConfigName": AutoMLProblemTypeConfigNameType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelineExecutionStepsResponseTypeDef = TypedDict(
    "ListPipelineExecutionStepsResponseTypeDef",
    {
        "PipelineExecutionSteps": List[PipelineExecutionStepTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEndpointInputRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointInputRequestTypeDef",
    {
        "EndpointName": str,
        "EndpointConfigName": str,
    },
)
_OptionalCreateEndpointInputRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointInputRequestTypeDef",
    {
        "DeploymentConfig": DeploymentConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEndpointInputRequestTypeDef(
    _RequiredCreateEndpointInputRequestTypeDef, _OptionalCreateEndpointInputRequestTypeDef
):
    pass


_RequiredUpdateEndpointInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEndpointInputRequestTypeDef",
    {
        "EndpointName": str,
        "EndpointConfigName": str,
    },
)
_OptionalUpdateEndpointInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEndpointInputRequestTypeDef",
    {
        "RetainAllVariantProperties": bool,
        "ExcludeRetainedVariantProperties": Sequence[VariantPropertyTypeDef],
        "DeploymentConfig": DeploymentConfigTypeDef,
        "RetainDeploymentConfig": bool,
    },
    total=False,
)


class UpdateEndpointInputRequestTypeDef(
    _RequiredUpdateEndpointInputRequestTypeDef, _OptionalUpdateEndpointInputRequestTypeDef
):
    pass


_RequiredCreateInferenceRecommendationsJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInferenceRecommendationsJobRequestRequestTypeDef",
    {
        "JobName": str,
        "JobType": RecommendationJobTypeType,
        "RoleArn": str,
        "InputConfig": RecommendationJobInputConfigTypeDef,
    },
)
_OptionalCreateInferenceRecommendationsJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInferenceRecommendationsJobRequestRequestTypeDef",
    {
        "JobDescription": str,
        "StoppingConditions": RecommendationJobStoppingConditionsTypeDef,
        "OutputConfig": RecommendationJobOutputConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateInferenceRecommendationsJobRequestRequestTypeDef(
    _RequiredCreateInferenceRecommendationsJobRequestRequestTypeDef,
    _OptionalCreateInferenceRecommendationsJobRequestRequestTypeDef,
):
    pass


DescribeInferenceRecommendationsJobResponseTypeDef = TypedDict(
    "DescribeInferenceRecommendationsJobResponseTypeDef",
    {
        "JobName": str,
        "JobDescription": str,
        "JobType": RecommendationJobTypeType,
        "JobArn": str,
        "RoleArn": str,
        "Status": RecommendationJobStatusType,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "InputConfig": RecommendationJobInputConfigTypeDef,
        "StoppingConditions": RecommendationJobStoppingConditionsTypeDef,
        "InferenceRecommendations": List[InferenceRecommendationTypeDef],
        "EndpointPerformances": List[EndpointPerformanceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEndpointConfigInputRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointConfigInputRequestTypeDef",
    {
        "EndpointConfigName": str,
        "ProductionVariants": Sequence[ProductionVariantTypeDef],
    },
)
_OptionalCreateEndpointConfigInputRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointConfigInputRequestTypeDef",
    {
        "DataCaptureConfig": DataCaptureConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "AsyncInferenceConfig": AsyncInferenceConfigTypeDef,
        "ExplainerConfig": ExplainerConfigTypeDef,
        "ShadowProductionVariants": Sequence[ProductionVariantTypeDef],
    },
    total=False,
)


class CreateEndpointConfigInputRequestTypeDef(
    _RequiredCreateEndpointConfigInputRequestTypeDef,
    _OptionalCreateEndpointConfigInputRequestTypeDef,
):
    pass


DescribeEndpointConfigOutputTypeDef = TypedDict(
    "DescribeEndpointConfigOutputTypeDef",
    {
        "EndpointConfigName": str,
        "EndpointConfigArn": str,
        "ProductionVariants": List[ProductionVariantTypeDef],
        "DataCaptureConfig": DataCaptureConfigTypeDef,
        "KmsKeyId": str,
        "CreationTime": datetime,
        "AsyncInferenceConfig": AsyncInferenceConfigTypeDef,
        "ExplainerConfig": ExplainerConfigTypeDef,
        "ShadowProductionVariants": List[ProductionVariantTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEndpointOutputTypeDef = TypedDict(
    "DescribeEndpointOutputTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "EndpointConfigName": str,
        "ProductionVariants": List[ProductionVariantSummaryTypeDef],
        "DataCaptureConfig": DataCaptureConfigSummaryTypeDef,
        "EndpointStatus": EndpointStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastDeploymentConfig": DeploymentConfigTypeDef,
        "AsyncInferenceConfig": AsyncInferenceConfigTypeDef,
        "PendingDeploymentSummary": PendingDeploymentSummaryTypeDef,
        "ExplainerConfig": ExplainerConfigTypeDef,
        "ShadowProductionVariants": List[ProductionVariantSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateHyperParameterTuningJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHyperParameterTuningJobRequestRequestTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobConfig": HyperParameterTuningJobConfigTypeDef,
    },
)
_OptionalCreateHyperParameterTuningJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHyperParameterTuningJobRequestRequestTypeDef",
    {
        "TrainingJobDefinition": HyperParameterTrainingJobDefinitionTypeDef,
        "TrainingJobDefinitions": Sequence[HyperParameterTrainingJobDefinitionTypeDef],
        "WarmStartConfig": HyperParameterTuningJobWarmStartConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "Autotune": AutotuneTypeDef,
    },
    total=False,
)


class CreateHyperParameterTuningJobRequestRequestTypeDef(
    _RequiredCreateHyperParameterTuningJobRequestRequestTypeDef,
    _OptionalCreateHyperParameterTuningJobRequestRequestTypeDef,
):
    pass


DescribeHyperParameterTuningJobResponseTypeDef = TypedDict(
    "DescribeHyperParameterTuningJobResponseTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobConfig": HyperParameterTuningJobConfigTypeDef,
        "TrainingJobDefinition": HyperParameterTrainingJobDefinitionTypeDef,
        "TrainingJobDefinitions": List[HyperParameterTrainingJobDefinitionTypeDef],
        "HyperParameterTuningJobStatus": HyperParameterTuningJobStatusType,
        "CreationTime": datetime,
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersTypeDef,
        "BestTrainingJob": HyperParameterTrainingJobSummaryTypeDef,
        "OverallBestTrainingJob": HyperParameterTrainingJobSummaryTypeDef,
        "WarmStartConfig": HyperParameterTuningJobWarmStartConfigTypeDef,
        "FailureReason": str,
        "TuningJobCompletionDetails": HyperParameterTuningJobCompletionDetailsTypeDef,
        "ConsumedResources": HyperParameterTuningJobConsumedResourcesTypeDef,
        "Autotune": AutotuneTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HyperParameterTuningJobSearchEntityTypeDef = TypedDict(
    "HyperParameterTuningJobSearchEntityTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobConfig": HyperParameterTuningJobConfigTypeDef,
        "TrainingJobDefinition": HyperParameterTrainingJobDefinitionTypeDef,
        "TrainingJobDefinitions": List[HyperParameterTrainingJobDefinitionTypeDef],
        "HyperParameterTuningJobStatus": HyperParameterTuningJobStatusType,
        "CreationTime": datetime,
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersTypeDef,
        "BestTrainingJob": HyperParameterTrainingJobSummaryTypeDef,
        "OverallBestTrainingJob": HyperParameterTrainingJobSummaryTypeDef,
        "WarmStartConfig": HyperParameterTuningJobWarmStartConfigTypeDef,
        "FailureReason": str,
        "Tags": List[TagTypeDef],
        "TuningJobCompletionDetails": HyperParameterTuningJobCompletionDetailsTypeDef,
        "ConsumedResources": HyperParameterTuningJobConsumedResourcesTypeDef,
    },
)

ListInferenceRecommendationsJobStepsResponseTypeDef = TypedDict(
    "ListInferenceRecommendationsJobStepsResponseTypeDef",
    {
        "Steps": List[InferenceRecommendationsJobStepTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListLabelingJobsResponseTypeDef = TypedDict(
    "ListLabelingJobsResponseTypeDef",
    {
        "LabelingJobSummaryList": List[LabelingJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDescribeModelPackageOutputTypeDef = TypedDict(
    "BatchDescribeModelPackageOutputTypeDef",
    {
        "ModelPackageSummaries": Dict[str, BatchDescribeModelPackageSummaryTypeDef],
        "BatchDescribeModelPackageErrorMap": Dict[str, BatchDescribeModelPackageErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateDataQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataQualityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
        "DataQualityAppSpecification": DataQualityAppSpecificationTypeDef,
        "DataQualityJobInput": DataQualityJobInputTypeDef,
        "DataQualityJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateDataQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataQualityJobDefinitionRequestRequestTypeDef",
    {
        "DataQualityBaselineConfig": DataQualityBaselineConfigTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDataQualityJobDefinitionRequestRequestTypeDef(
    _RequiredCreateDataQualityJobDefinitionRequestRequestTypeDef,
    _OptionalCreateDataQualityJobDefinitionRequestRequestTypeDef,
):
    pass


DescribeDataQualityJobDefinitionResponseTypeDef = TypedDict(
    "DescribeDataQualityJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "DataQualityBaselineConfig": DataQualityBaselineConfigTypeDef,
        "DataQualityAppSpecification": DataQualityAppSpecificationTypeDef,
        "DataQualityJobInput": DataQualityJobInputTypeDef,
        "DataQualityJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateModelBiasJobDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateModelBiasJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
        "ModelBiasAppSpecification": ModelBiasAppSpecificationTypeDef,
        "ModelBiasJobInput": ModelBiasJobInputTypeDef,
        "ModelBiasJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateModelBiasJobDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateModelBiasJobDefinitionRequestRequestTypeDef",
    {
        "ModelBiasBaselineConfig": ModelBiasBaselineConfigTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateModelBiasJobDefinitionRequestRequestTypeDef(
    _RequiredCreateModelBiasJobDefinitionRequestRequestTypeDef,
    _OptionalCreateModelBiasJobDefinitionRequestRequestTypeDef,
):
    pass


DescribeModelBiasJobDefinitionResponseTypeDef = TypedDict(
    "DescribeModelBiasJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "ModelBiasBaselineConfig": ModelBiasBaselineConfigTypeDef,
        "ModelBiasAppSpecification": ModelBiasAppSpecificationTypeDef,
        "ModelBiasJobInput": ModelBiasJobInputTypeDef,
        "ModelBiasJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateModelExplainabilityJobDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateModelExplainabilityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
        "ModelExplainabilityAppSpecification": ModelExplainabilityAppSpecificationTypeDef,
        "ModelExplainabilityJobInput": ModelExplainabilityJobInputTypeDef,
        "ModelExplainabilityJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateModelExplainabilityJobDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateModelExplainabilityJobDefinitionRequestRequestTypeDef",
    {
        "ModelExplainabilityBaselineConfig": ModelExplainabilityBaselineConfigTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateModelExplainabilityJobDefinitionRequestRequestTypeDef(
    _RequiredCreateModelExplainabilityJobDefinitionRequestRequestTypeDef,
    _OptionalCreateModelExplainabilityJobDefinitionRequestRequestTypeDef,
):
    pass


DescribeModelExplainabilityJobDefinitionResponseTypeDef = TypedDict(
    "DescribeModelExplainabilityJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "ModelExplainabilityBaselineConfig": ModelExplainabilityBaselineConfigTypeDef,
        "ModelExplainabilityAppSpecification": ModelExplainabilityAppSpecificationTypeDef,
        "ModelExplainabilityJobInput": ModelExplainabilityJobInputTypeDef,
        "ModelExplainabilityJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateModelQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateModelQualityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
        "ModelQualityAppSpecification": ModelQualityAppSpecificationTypeDef,
        "ModelQualityJobInput": ModelQualityJobInputTypeDef,
        "ModelQualityJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateModelQualityJobDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateModelQualityJobDefinitionRequestRequestTypeDef",
    {
        "ModelQualityBaselineConfig": ModelQualityBaselineConfigTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateModelQualityJobDefinitionRequestRequestTypeDef(
    _RequiredCreateModelQualityJobDefinitionRequestRequestTypeDef,
    _OptionalCreateModelQualityJobDefinitionRequestRequestTypeDef,
):
    pass


DescribeModelQualityJobDefinitionResponseTypeDef = TypedDict(
    "DescribeModelQualityJobDefinitionResponseTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "ModelQualityBaselineConfig": ModelQualityBaselineConfigTypeDef,
        "ModelQualityAppSpecification": ModelQualityAppSpecificationTypeDef,
        "ModelQualityJobInput": ModelQualityJobInputTypeDef,
        "ModelQualityJobOutputConfig": MonitoringOutputConfigTypeDef,
        "JobResources": MonitoringResourcesTypeDef,
        "NetworkConfig": MonitoringNetworkConfigTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredMonitoringJobDefinitionTypeDef = TypedDict(
    "_RequiredMonitoringJobDefinitionTypeDef",
    {
        "MonitoringInputs": Sequence[MonitoringInputTypeDef],
        "MonitoringOutputConfig": MonitoringOutputConfigTypeDef,
        "MonitoringResources": MonitoringResourcesTypeDef,
        "MonitoringAppSpecification": MonitoringAppSpecificationTypeDef,
        "RoleArn": str,
    },
)
_OptionalMonitoringJobDefinitionTypeDef = TypedDict(
    "_OptionalMonitoringJobDefinitionTypeDef",
    {
        "BaselineConfig": MonitoringBaselineConfigTypeDef,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "Environment": Mapping[str, str],
        "NetworkConfig": NetworkConfigTypeDef,
    },
    total=False,
)


class MonitoringJobDefinitionTypeDef(
    _RequiredMonitoringJobDefinitionTypeDef, _OptionalMonitoringJobDefinitionTypeDef
):
    pass


_RequiredAlgorithmValidationProfileTypeDef = TypedDict(
    "_RequiredAlgorithmValidationProfileTypeDef",
    {
        "ProfileName": str,
        "TrainingJobDefinition": TrainingJobDefinitionTypeDef,
    },
)
_OptionalAlgorithmValidationProfileTypeDef = TypedDict(
    "_OptionalAlgorithmValidationProfileTypeDef",
    {
        "TransformJobDefinition": TransformJobDefinitionTypeDef,
    },
    total=False,
)


class AlgorithmValidationProfileTypeDef(
    _RequiredAlgorithmValidationProfileTypeDef, _OptionalAlgorithmValidationProfileTypeDef
):
    pass


ModelPackageValidationProfileTypeDef = TypedDict(
    "ModelPackageValidationProfileTypeDef",
    {
        "ProfileName": str,
        "TransformJobDefinition": TransformJobDefinitionTypeDef,
    },
)

TrialComponentSourceDetailTypeDef = TypedDict(
    "TrialComponentSourceDetailTypeDef",
    {
        "SourceArn": str,
        "TrainingJob": TrainingJobTypeDef,
        "ProcessingJob": ProcessingJobTypeDef,
        "TransformJob": TransformJobTypeDef,
    },
)

MonitoringScheduleConfigTypeDef = TypedDict(
    "MonitoringScheduleConfigTypeDef",
    {
        "ScheduleConfig": ScheduleConfigTypeDef,
        "MonitoringJobDefinition": MonitoringJobDefinitionTypeDef,
        "MonitoringJobDefinitionName": str,
        "MonitoringType": MonitoringTypeType,
    },
    total=False,
)

AlgorithmValidationSpecificationTypeDef = TypedDict(
    "AlgorithmValidationSpecificationTypeDef",
    {
        "ValidationRole": str,
        "ValidationProfiles": Sequence[AlgorithmValidationProfileTypeDef],
    },
)

ModelPackageValidationSpecificationTypeDef = TypedDict(
    "ModelPackageValidationSpecificationTypeDef",
    {
        "ValidationRole": str,
        "ValidationProfiles": Sequence[ModelPackageValidationProfileTypeDef],
    },
)

TrialComponentTypeDef = TypedDict(
    "TrialComponentTypeDef",
    {
        "TrialComponentName": str,
        "DisplayName": str,
        "TrialComponentArn": str,
        "Source": TrialComponentSourceTypeDef,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Parameters": Dict[str, TrialComponentParameterValueTypeDef],
        "InputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "OutputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "Metrics": List[TrialComponentMetricSummaryTypeDef],
        "MetadataProperties": MetadataPropertiesTypeDef,
        "SourceDetail": TrialComponentSourceDetailTypeDef,
        "LineageGroupArn": str,
        "Tags": List[TagTypeDef],
        "Parents": List[ParentTypeDef],
        "RunName": str,
    },
)

_RequiredCreateMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringScheduleConfig": MonitoringScheduleConfigTypeDef,
    },
)
_OptionalCreateMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMonitoringScheduleRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMonitoringScheduleRequestRequestTypeDef(
    _RequiredCreateMonitoringScheduleRequestRequestTypeDef,
    _OptionalCreateMonitoringScheduleRequestRequestTypeDef,
):
    pass


DescribeMonitoringScheduleResponseTypeDef = TypedDict(
    "DescribeMonitoringScheduleResponseTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringScheduleName": str,
        "MonitoringScheduleStatus": ScheduleStatusType,
        "MonitoringType": MonitoringTypeType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleConfig": MonitoringScheduleConfigTypeDef,
        "EndpointName": str,
        "LastMonitoringExecutionSummary": MonitoringExecutionSummaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelDashboardMonitoringScheduleTypeDef = TypedDict(
    "ModelDashboardMonitoringScheduleTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringScheduleName": str,
        "MonitoringScheduleStatus": ScheduleStatusType,
        "MonitoringType": MonitoringTypeType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleConfig": MonitoringScheduleConfigTypeDef,
        "EndpointName": str,
        "MonitoringAlertSummaries": List[MonitoringAlertSummaryTypeDef],
        "LastMonitoringExecutionSummary": MonitoringExecutionSummaryTypeDef,
    },
)

MonitoringScheduleTypeDef = TypedDict(
    "MonitoringScheduleTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringScheduleName": str,
        "MonitoringScheduleStatus": ScheduleStatusType,
        "MonitoringType": MonitoringTypeType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleConfig": MonitoringScheduleConfigTypeDef,
        "EndpointName": str,
        "LastMonitoringExecutionSummary": MonitoringExecutionSummaryTypeDef,
        "Tags": List[TagTypeDef],
    },
)

UpdateMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "UpdateMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringScheduleConfig": MonitoringScheduleConfigTypeDef,
    },
)

_RequiredCreateAlgorithmInputRequestTypeDef = TypedDict(
    "_RequiredCreateAlgorithmInputRequestTypeDef",
    {
        "AlgorithmName": str,
        "TrainingSpecification": TrainingSpecificationTypeDef,
    },
)
_OptionalCreateAlgorithmInputRequestTypeDef = TypedDict(
    "_OptionalCreateAlgorithmInputRequestTypeDef",
    {
        "AlgorithmDescription": str,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "ValidationSpecification": AlgorithmValidationSpecificationTypeDef,
        "CertifyForMarketplace": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAlgorithmInputRequestTypeDef(
    _RequiredCreateAlgorithmInputRequestTypeDef, _OptionalCreateAlgorithmInputRequestTypeDef
):
    pass


DescribeAlgorithmOutputTypeDef = TypedDict(
    "DescribeAlgorithmOutputTypeDef",
    {
        "AlgorithmName": str,
        "AlgorithmArn": str,
        "AlgorithmDescription": str,
        "CreationTime": datetime,
        "TrainingSpecification": TrainingSpecificationTypeDef,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "ValidationSpecification": AlgorithmValidationSpecificationTypeDef,
        "AlgorithmStatus": AlgorithmStatusType,
        "AlgorithmStatusDetails": AlgorithmStatusDetailsTypeDef,
        "ProductId": str,
        "CertifyForMarketplace": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateModelPackageInputRequestTypeDef = TypedDict(
    "CreateModelPackageInputRequestTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageGroupName": str,
        "ModelPackageDescription": str,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "ValidationSpecification": ModelPackageValidationSpecificationTypeDef,
        "SourceAlgorithmSpecification": SourceAlgorithmSpecificationTypeDef,
        "CertifyForMarketplace": bool,
        "Tags": Sequence[TagTypeDef],
        "ModelApprovalStatus": ModelApprovalStatusType,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "ModelMetrics": ModelMetricsTypeDef,
        "ClientToken": str,
        "CustomerMetadataProperties": Mapping[str, str],
        "DriftCheckBaselines": DriftCheckBaselinesTypeDef,
        "Domain": str,
        "Task": str,
        "SamplePayloadUrl": str,
        "AdditionalInferenceSpecifications": Sequence[
            AdditionalInferenceSpecificationDefinitionTypeDef
        ],
    },
    total=False,
)

DescribeModelPackageOutputTypeDef = TypedDict(
    "DescribeModelPackageOutputTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageGroupName": str,
        "ModelPackageVersion": int,
        "ModelPackageArn": str,
        "ModelPackageDescription": str,
        "CreationTime": datetime,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "SourceAlgorithmSpecification": SourceAlgorithmSpecificationTypeDef,
        "ValidationSpecification": ModelPackageValidationSpecificationTypeDef,
        "ModelPackageStatus": ModelPackageStatusType,
        "ModelPackageStatusDetails": ModelPackageStatusDetailsTypeDef,
        "CertifyForMarketplace": bool,
        "ModelApprovalStatus": ModelApprovalStatusType,
        "CreatedBy": UserContextTypeDef,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "ModelMetrics": ModelMetricsTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "ApprovalDescription": str,
        "CustomerMetadataProperties": Dict[str, str],
        "DriftCheckBaselines": DriftCheckBaselinesTypeDef,
        "Domain": str,
        "Task": str,
        "SamplePayloadUrl": str,
        "AdditionalInferenceSpecifications": List[
            AdditionalInferenceSpecificationDefinitionTypeDef
        ],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelPackageTypeDef = TypedDict(
    "ModelPackageTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageGroupName": str,
        "ModelPackageVersion": int,
        "ModelPackageArn": str,
        "ModelPackageDescription": str,
        "CreationTime": datetime,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "SourceAlgorithmSpecification": SourceAlgorithmSpecificationTypeDef,
        "ValidationSpecification": ModelPackageValidationSpecificationTypeDef,
        "ModelPackageStatus": ModelPackageStatusType,
        "ModelPackageStatusDetails": ModelPackageStatusDetailsTypeDef,
        "CertifyForMarketplace": bool,
        "ModelApprovalStatus": ModelApprovalStatusType,
        "CreatedBy": UserContextTypeDef,
        "MetadataProperties": MetadataPropertiesTypeDef,
        "ModelMetrics": ModelMetricsTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "ApprovalDescription": str,
        "Domain": str,
        "Task": str,
        "SamplePayloadUrl": str,
        "AdditionalInferenceSpecifications": List[
            AdditionalInferenceSpecificationDefinitionTypeDef
        ],
        "Tags": List[TagTypeDef],
        "CustomerMetadataProperties": Dict[str, str],
        "DriftCheckBaselines": DriftCheckBaselinesTypeDef,
    },
)

ModelDashboardModelTypeDef = TypedDict(
    "ModelDashboardModelTypeDef",
    {
        "Model": ModelTypeDef,
        "Endpoints": List[ModelDashboardEndpointTypeDef],
        "LastBatchTransformJob": TransformJobTypeDef,
        "MonitoringSchedules": List[ModelDashboardMonitoringScheduleTypeDef],
        "ModelCard": ModelDashboardModelCardTypeDef,
    },
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "EndpointConfigName": str,
        "ProductionVariants": List[ProductionVariantSummaryTypeDef],
        "DataCaptureConfig": DataCaptureConfigSummaryTypeDef,
        "EndpointStatus": EndpointStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringSchedules": List[MonitoringScheduleTypeDef],
        "Tags": List[TagTypeDef],
        "ShadowProductionVariants": List[ProductionVariantSummaryTypeDef],
    },
)

SearchRecordTypeDef = TypedDict(
    "SearchRecordTypeDef",
    {
        "TrainingJob": TrainingJobTypeDef,
        "Experiment": ExperimentTypeDef,
        "Trial": TrialTypeDef,
        "TrialComponent": TrialComponentTypeDef,
        "Endpoint": EndpointTypeDef,
        "ModelPackage": ModelPackageTypeDef,
        "ModelPackageGroup": ModelPackageGroupTypeDef,
        "Pipeline": PipelineTypeDef,
        "PipelineExecution": PipelineExecutionTypeDef,
        "FeatureGroup": FeatureGroupTypeDef,
        "Project": ProjectTypeDef,
        "FeatureMetadata": FeatureMetadataTypeDef,
        "HyperParameterTuningJob": HyperParameterTuningJobSearchEntityTypeDef,
        "Model": ModelDashboardModelTypeDef,
        "ModelCard": ModelCardTypeDef,
    },
)

SearchResponseTypeDef = TypedDict(
    "SearchResponseTypeDef",
    {
        "Results": List[SearchRecordTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
