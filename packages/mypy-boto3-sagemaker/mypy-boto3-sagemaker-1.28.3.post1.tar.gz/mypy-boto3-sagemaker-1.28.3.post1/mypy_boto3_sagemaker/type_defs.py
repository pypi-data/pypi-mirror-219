"""
Type annotations for sagemaker service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker.type_defs import ActionSourceOutputTypeDef

    data: ActionSourceOutputTypeDef = {...}
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
    "ActionSourceOutputTypeDef",
    "ActionSourceTypeDef",
    "AddAssociationRequestRequestTypeDef",
    "AddAssociationResponseOutputTypeDef",
    "TagTypeDef",
    "TagOutputTypeDef",
    "AgentVersionOutputTypeDef",
    "AlarmOutputTypeDef",
    "AlarmTypeDef",
    "MetricDefinitionOutputTypeDef",
    "MetricDefinitionTypeDef",
    "AlgorithmStatusItemOutputTypeDef",
    "AlgorithmSummaryOutputTypeDef",
    "AnnotationConsolidationConfigOutputTypeDef",
    "AnnotationConsolidationConfigTypeDef",
    "AppDetailsOutputTypeDef",
    "AppSpecificationOutputTypeDef",
    "AppSpecificationTypeDef",
    "ArtifactSourceTypeOutputTypeDef",
    "ArtifactSourceTypeTypeDef",
    "AssociateTrialComponentRequestRequestTypeDef",
    "AssociateTrialComponentResponseOutputTypeDef",
    "AsyncInferenceClientConfigOutputTypeDef",
    "AsyncInferenceClientConfigTypeDef",
    "AsyncInferenceNotificationConfigOutputTypeDef",
    "AsyncInferenceNotificationConfigTypeDef",
    "AthenaDatasetDefinitionOutputTypeDef",
    "AthenaDatasetDefinitionTypeDef",
    "AutoMLAlgorithmConfigOutputTypeDef",
    "AutoMLAlgorithmConfigTypeDef",
    "AutoMLCandidateStepOutputTypeDef",
    "AutoMLContainerDefinitionOutputTypeDef",
    "FinalAutoMLJobObjectiveMetricOutputTypeDef",
    "AutoMLS3DataSourceOutputTypeDef",
    "AutoMLS3DataSourceTypeDef",
    "AutoMLDataSplitConfigOutputTypeDef",
    "AutoMLDataSplitConfigTypeDef",
    "AutoMLJobArtifactsOutputTypeDef",
    "AutoMLJobCompletionCriteriaOutputTypeDef",
    "AutoMLJobCompletionCriteriaTypeDef",
    "AutoMLJobObjectiveOutputTypeDef",
    "AutoMLJobObjectiveTypeDef",
    "AutoMLJobStepMetadataOutputTypeDef",
    "AutoMLPartialFailureReasonOutputTypeDef",
    "AutoMLOutputDataConfigOutputTypeDef",
    "AutoMLOutputDataConfigTypeDef",
    "TabularResolvedAttributesOutputTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "AutoParameterOutputTypeDef",
    "AutoParameterTypeDef",
    "AutotuneOutputTypeDef",
    "AutotuneTypeDef",
    "BatchDataCaptureConfigOutputTypeDef",
    "BatchDataCaptureConfigTypeDef",
    "BatchDescribeModelPackageErrorOutputTypeDef",
    "BatchDescribeModelPackageInputRequestTypeDef",
    "BestObjectiveNotImprovingOutputTypeDef",
    "BestObjectiveNotImprovingTypeDef",
    "MetricsSourceOutputTypeDef",
    "MetricsSourceTypeDef",
    "CacheHitResultOutputTypeDef",
    "OutputParameterOutputTypeDef",
    "CandidateArtifactLocationsOutputTypeDef",
    "MetricDatumOutputTypeDef",
    "ModelRegisterSettingsOutputTypeDef",
    "TimeSeriesForecastingSettingsOutputTypeDef",
    "WorkspaceSettingsOutputTypeDef",
    "ModelRegisterSettingsTypeDef",
    "TimeSeriesForecastingSettingsTypeDef",
    "WorkspaceSettingsTypeDef",
    "CapacitySizeOutputTypeDef",
    "CapacitySizeTypeDef",
    "CaptureContentTypeHeaderOutputTypeDef",
    "CaptureContentTypeHeaderTypeDef",
    "CaptureOptionOutputTypeDef",
    "CaptureOptionTypeDef",
    "CategoricalParameterOutputTypeDef",
    "CategoricalParameterRangeOutputTypeDef",
    "CategoricalParameterRangeSpecificationOutputTypeDef",
    "CategoricalParameterRangeSpecificationTypeDef",
    "CategoricalParameterRangeTypeDef",
    "CategoricalParameterTypeDef",
    "ShuffleConfigOutputTypeDef",
    "ChannelSpecificationOutputTypeDef",
    "ChannelSpecificationTypeDef",
    "ShuffleConfigTypeDef",
    "CheckpointConfigOutputTypeDef",
    "CheckpointConfigTypeDef",
    "ClarifyCheckStepMetadataOutputTypeDef",
    "ClarifyInferenceConfigOutputTypeDef",
    "ClarifyInferenceConfigTypeDef",
    "ClarifyShapBaselineConfigOutputTypeDef",
    "ClarifyShapBaselineConfigTypeDef",
    "ClarifyTextConfigOutputTypeDef",
    "ClarifyTextConfigTypeDef",
    "CodeRepositoryOutputTypeDef",
    "GitConfigOutputTypeDef",
    "CodeRepositoryTypeDef",
    "CognitoConfigOutputTypeDef",
    "CognitoConfigTypeDef",
    "CognitoMemberDefinitionOutputTypeDef",
    "CognitoMemberDefinitionTypeDef",
    "CollectionConfigurationOutputTypeDef",
    "CollectionConfigurationTypeDef",
    "CompilationJobSummaryOutputTypeDef",
    "ConditionStepMetadataOutputTypeDef",
    "MultiModelConfigOutputTypeDef",
    "MultiModelConfigTypeDef",
    "ContextSourceOutputTypeDef",
    "ContextSourceTypeDef",
    "ContinuousParameterRangeOutputTypeDef",
    "ContinuousParameterRangeSpecificationOutputTypeDef",
    "ContinuousParameterRangeSpecificationTypeDef",
    "ContinuousParameterRangeTypeDef",
    "ConvergenceDetectedOutputTypeDef",
    "ConvergenceDetectedTypeDef",
    "MetadataPropertiesTypeDef",
    "CreateActionResponseOutputTypeDef",
    "CreateAlgorithmOutputOutputTypeDef",
    "CreateAppImageConfigResponseOutputTypeDef",
    "ResourceSpecTypeDef",
    "CreateAppResponseOutputTypeDef",
    "CreateArtifactResponseOutputTypeDef",
    "ModelDeployConfigTypeDef",
    "CreateAutoMLJobResponseOutputTypeDef",
    "CreateAutoMLJobV2ResponseOutputTypeDef",
    "GitConfigTypeDef",
    "CreateCodeRepositoryOutputOutputTypeDef",
    "InputConfigTypeDef",
    "NeoVpcConfigTypeDef",
    "StoppingConditionTypeDef",
    "CreateCompilationJobResponseOutputTypeDef",
    "CreateContextResponseOutputTypeDef",
    "DataQualityAppSpecificationTypeDef",
    "MonitoringStoppingConditionTypeDef",
    "CreateDataQualityJobDefinitionResponseOutputTypeDef",
    "EdgeOutputConfigTypeDef",
    "CreateDomainResponseOutputTypeDef",
    "EdgeDeploymentModelConfigTypeDef",
    "CreateEdgeDeploymentPlanResponseOutputTypeDef",
    "CreateEndpointConfigOutputOutputTypeDef",
    "CreateEndpointOutputOutputTypeDef",
    "CreateExperimentResponseOutputTypeDef",
    "FeatureDefinitionTypeDef",
    "CreateFeatureGroupResponseOutputTypeDef",
    "FlowDefinitionOutputConfigTypeDef",
    "HumanLoopRequestSourceTypeDef",
    "CreateFlowDefinitionResponseOutputTypeDef",
    "HubS3StorageConfigTypeDef",
    "CreateHubResponseOutputTypeDef",
    "UiTemplateTypeDef",
    "CreateHumanTaskUiResponseOutputTypeDef",
    "CreateHyperParameterTuningJobResponseOutputTypeDef",
    "CreateImageResponseOutputTypeDef",
    "CreateImageVersionRequestRequestTypeDef",
    "CreateImageVersionResponseOutputTypeDef",
    "InferenceExperimentScheduleTypeDef",
    "CreateInferenceExperimentResponseOutputTypeDef",
    "CreateInferenceRecommendationsJobResponseOutputTypeDef",
    "LabelingJobOutputConfigTypeDef",
    "LabelingJobStoppingConditionsTypeDef",
    "CreateLabelingJobResponseOutputTypeDef",
    "ModelBiasAppSpecificationTypeDef",
    "CreateModelBiasJobDefinitionResponseOutputTypeDef",
    "ModelCardExportOutputConfigTypeDef",
    "CreateModelCardExportJobResponseOutputTypeDef",
    "ModelCardSecurityConfigTypeDef",
    "CreateModelCardResponseOutputTypeDef",
    "ModelExplainabilityAppSpecificationTypeDef",
    "CreateModelExplainabilityJobDefinitionResponseOutputTypeDef",
    "InferenceExecutionConfigTypeDef",
    "CreateModelOutputOutputTypeDef",
    "CreateModelPackageGroupOutputOutputTypeDef",
    "CreateModelPackageOutputOutputTypeDef",
    "ModelQualityAppSpecificationTypeDef",
    "CreateModelQualityJobDefinitionResponseOutputTypeDef",
    "CreateMonitoringScheduleResponseOutputTypeDef",
    "InstanceMetadataServiceConfigurationTypeDef",
    "NotebookInstanceLifecycleHookTypeDef",
    "CreateNotebookInstanceLifecycleConfigOutputOutputTypeDef",
    "CreateNotebookInstanceOutputOutputTypeDef",
    "ParallelismConfigurationTypeDef",
    "PipelineDefinitionS3LocationTypeDef",
    "CreatePipelineResponseOutputTypeDef",
    "CreatePresignedDomainUrlRequestRequestTypeDef",
    "CreatePresignedDomainUrlResponseOutputTypeDef",
    "CreatePresignedNotebookInstanceUrlInputRequestTypeDef",
    "CreatePresignedNotebookInstanceUrlOutputOutputTypeDef",
    "ExperimentConfigTypeDef",
    "ProcessingStoppingConditionTypeDef",
    "CreateProcessingJobResponseOutputTypeDef",
    "CreateProjectOutputOutputTypeDef",
    "CreateSpaceResponseOutputTypeDef",
    "CreateStudioLifecycleConfigResponseOutputTypeDef",
    "DebugRuleConfigurationTypeDef",
    "OutputDataConfigTypeDef",
    "ProfilerConfigTypeDef",
    "ProfilerRuleConfigurationTypeDef",
    "RetryStrategyTypeDef",
    "TensorBoardOutputConfigTypeDef",
    "CreateTrainingJobResponseOutputTypeDef",
    "DataProcessingTypeDef",
    "ModelClientConfigTypeDef",
    "TransformOutputTypeDef",
    "TransformResourcesTypeDef",
    "CreateTransformJobResponseOutputTypeDef",
    "TrialComponentArtifactTypeDef",
    "TrialComponentParameterValueTypeDef",
    "TrialComponentStatusTypeDef",
    "CreateTrialComponentResponseOutputTypeDef",
    "CreateTrialResponseOutputTypeDef",
    "CreateUserProfileResponseOutputTypeDef",
    "OidcConfigTypeDef",
    "SourceIpConfigTypeDef",
    "WorkforceVpcConfigRequestTypeDef",
    "CreateWorkforceResponseOutputTypeDef",
    "NotificationConfigurationTypeDef",
    "CreateWorkteamResponseOutputTypeDef",
    "CustomImageOutputTypeDef",
    "CustomImageTypeDef",
    "DataCaptureConfigSummaryOutputTypeDef",
    "DataCatalogConfigOutputTypeDef",
    "DataCatalogConfigTypeDef",
    "DataProcessingOutputTypeDef",
    "DataQualityAppSpecificationOutputTypeDef",
    "MonitoringConstraintsResourceOutputTypeDef",
    "MonitoringStatisticsResourceOutputTypeDef",
    "MonitoringConstraintsResourceTypeDef",
    "MonitoringStatisticsResourceTypeDef",
    "EndpointInputOutputTypeDef",
    "EndpointInputTypeDef",
    "FileSystemDataSourceOutputTypeDef",
    "S3DataSourceOutputTypeDef",
    "FileSystemDataSourceTypeDef",
    "S3DataSourceTypeDef",
    "RedshiftDatasetDefinitionOutputTypeDef",
    "RedshiftDatasetDefinitionTypeDef",
    "DebugRuleConfigurationOutputTypeDef",
    "DebugRuleEvaluationStatusOutputTypeDef",
    "DeleteActionRequestRequestTypeDef",
    "DeleteActionResponseOutputTypeDef",
    "DeleteAlgorithmInputRequestTypeDef",
    "DeleteAppImageConfigRequestRequestTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteArtifactResponseOutputTypeDef",
    "DeleteAssociationRequestRequestTypeDef",
    "DeleteAssociationResponseOutputTypeDef",
    "DeleteCodeRepositoryInputRequestTypeDef",
    "DeleteContextRequestRequestTypeDef",
    "DeleteContextResponseOutputTypeDef",
    "DeleteDataQualityJobDefinitionRequestRequestTypeDef",
    "DeleteDeviceFleetRequestRequestTypeDef",
    "RetentionPolicyTypeDef",
    "DeleteEdgeDeploymentPlanRequestRequestTypeDef",
    "DeleteEdgeDeploymentStageRequestRequestTypeDef",
    "DeleteEndpointConfigInputRequestTypeDef",
    "DeleteEndpointInputRequestTypeDef",
    "DeleteExperimentRequestRequestTypeDef",
    "DeleteExperimentResponseOutputTypeDef",
    "DeleteFeatureGroupRequestRequestTypeDef",
    "DeleteFlowDefinitionRequestRequestTypeDef",
    "DeleteHubContentRequestRequestTypeDef",
    "DeleteHubRequestRequestTypeDef",
    "DeleteHumanTaskUiRequestRequestTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteImageVersionRequestRequestTypeDef",
    "DeleteInferenceExperimentRequestRequestTypeDef",
    "DeleteInferenceExperimentResponseOutputTypeDef",
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
    "DeletePipelineResponseOutputTypeDef",
    "DeleteProjectInputRequestTypeDef",
    "DeleteSpaceRequestRequestTypeDef",
    "DeleteStudioLifecycleConfigRequestRequestTypeDef",
    "DeleteTagsInputRequestTypeDef",
    "DeleteTrialComponentRequestRequestTypeDef",
    "DeleteTrialComponentResponseOutputTypeDef",
    "DeleteTrialRequestRequestTypeDef",
    "DeleteTrialResponseOutputTypeDef",
    "DeleteUserProfileRequestRequestTypeDef",
    "DeleteWorkforceRequestRequestTypeDef",
    "DeleteWorkteamRequestRequestTypeDef",
    "DeleteWorkteamResponseOutputTypeDef",
    "DeployedImageOutputTypeDef",
    "RealTimeInferenceRecommendationOutputTypeDef",
    "DeviceSelectionConfigOutputTypeDef",
    "EdgeDeploymentConfigOutputTypeDef",
    "EdgeDeploymentStatusOutputTypeDef",
    "DeviceSelectionConfigTypeDef",
    "EdgeDeploymentConfigTypeDef",
    "DeregisterDevicesRequestRequestTypeDef",
    "DescribeActionRequestRequestTypeDef",
    "MetadataPropertiesOutputTypeDef",
    "DescribeAlgorithmInputRequestTypeDef",
    "DescribeAppImageConfigRequestRequestTypeDef",
    "DescribeAppRequestRequestTypeDef",
    "ResourceSpecOutputTypeDef",
    "DescribeArtifactRequestRequestTypeDef",
    "DescribeAutoMLJobRequestRequestTypeDef",
    "ModelDeployConfigOutputTypeDef",
    "ModelDeployResultOutputTypeDef",
    "DescribeAutoMLJobV2RequestRequestTypeDef",
    "DescribeCodeRepositoryInputRequestTypeDef",
    "DescribeCompilationJobRequestRequestTypeDef",
    "InputConfigOutputTypeDef",
    "ModelArtifactsOutputTypeDef",
    "ModelDigestsOutputTypeDef",
    "NeoVpcConfigOutputTypeDef",
    "StoppingConditionOutputTypeDef",
    "DescribeContextRequestRequestTypeDef",
    "DescribeDataQualityJobDefinitionRequestRequestTypeDef",
    "MonitoringStoppingConditionOutputTypeDef",
    "DescribeDeviceFleetRequestRequestTypeDef",
    "EdgeOutputConfigOutputTypeDef",
    "DescribeDeviceRequestRequestTypeDef",
    "EdgeModelOutputTypeDef",
    "DescribeDomainRequestRequestTypeDef",
    "DescribeEdgeDeploymentPlanRequestRequestTypeDef",
    "EdgeDeploymentModelConfigOutputTypeDef",
    "DescribeEdgePackagingJobRequestRequestTypeDef",
    "EdgePresetDeploymentOutputOutputTypeDef",
    "DescribeEndpointConfigInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeEndpointInputRequestTypeDef",
    "DescribeExperimentRequestRequestTypeDef",
    "ExperimentSourceOutputTypeDef",
    "DescribeFeatureGroupRequestRequestTypeDef",
    "FeatureDefinitionOutputTypeDef",
    "LastUpdateStatusOutputTypeDef",
    "OfflineStoreStatusOutputTypeDef",
    "DescribeFeatureMetadataRequestRequestTypeDef",
    "FeatureParameterOutputTypeDef",
    "DescribeFlowDefinitionRequestRequestTypeDef",
    "FlowDefinitionOutputConfigOutputTypeDef",
    "HumanLoopRequestSourceOutputTypeDef",
    "DescribeHubContentRequestRequestTypeDef",
    "HubContentDependencyOutputTypeDef",
    "DescribeHubRequestRequestTypeDef",
    "HubS3StorageConfigOutputTypeDef",
    "DescribeHumanTaskUiRequestRequestTypeDef",
    "UiTemplateInfoOutputTypeDef",
    "DescribeHyperParameterTuningJobRequestRequestTypeDef",
    "HyperParameterTuningJobCompletionDetailsOutputTypeDef",
    "HyperParameterTuningJobConsumedResourcesOutputTypeDef",
    "ObjectiveStatusCountersOutputTypeDef",
    "TrainingJobStatusCountersOutputTypeDef",
    "DescribeImageRequestRequestTypeDef",
    "DescribeImageResponseOutputTypeDef",
    "DescribeImageVersionRequestRequestTypeDef",
    "DescribeImageVersionResponseOutputTypeDef",
    "DescribeInferenceExperimentRequestRequestTypeDef",
    "EndpointMetadataOutputTypeDef",
    "InferenceExperimentScheduleOutputTypeDef",
    "DescribeInferenceRecommendationsJobRequestRequestTypeDef",
    "DescribeLabelingJobRequestRequestTypeDef",
    "LabelCountersOutputTypeDef",
    "LabelingJobOutputConfigOutputTypeDef",
    "LabelingJobOutputOutputTypeDef",
    "LabelingJobStoppingConditionsOutputTypeDef",
    "DescribeLineageGroupRequestRequestTypeDef",
    "DescribeModelBiasJobDefinitionRequestRequestTypeDef",
    "ModelBiasAppSpecificationOutputTypeDef",
    "DescribeModelCardExportJobRequestRequestTypeDef",
    "ModelCardExportArtifactsOutputTypeDef",
    "ModelCardExportOutputConfigOutputTypeDef",
    "DescribeModelCardRequestRequestTypeDef",
    "ModelCardSecurityConfigOutputTypeDef",
    "DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "ModelExplainabilityAppSpecificationOutputTypeDef",
    "DescribeModelInputRequestTypeDef",
    "InferenceExecutionConfigOutputTypeDef",
    "DescribeModelPackageGroupInputRequestTypeDef",
    "DescribeModelPackageInputRequestTypeDef",
    "DescribeModelQualityJobDefinitionRequestRequestTypeDef",
    "ModelQualityAppSpecificationOutputTypeDef",
    "DescribeMonitoringScheduleRequestRequestTypeDef",
    "MonitoringExecutionSummaryOutputTypeDef",
    "DescribeNotebookInstanceInputRequestTypeDef",
    "DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "NotebookInstanceLifecycleHookOutputTypeDef",
    "InstanceMetadataServiceConfigurationOutputTypeDef",
    "DescribePipelineDefinitionForExecutionRequestRequestTypeDef",
    "DescribePipelineDefinitionForExecutionResponseOutputTypeDef",
    "DescribePipelineExecutionRequestRequestTypeDef",
    "ParallelismConfigurationOutputTypeDef",
    "PipelineExperimentConfigOutputTypeDef",
    "DescribePipelineRequestRequestTypeDef",
    "DescribeProcessingJobRequestRequestTypeDef",
    "ExperimentConfigOutputTypeDef",
    "ProcessingStoppingConditionOutputTypeDef",
    "DescribeProjectInputRequestTypeDef",
    "ServiceCatalogProvisionedProductDetailsOutputTypeDef",
    "DescribeSpaceRequestRequestTypeDef",
    "DescribeStudioLifecycleConfigRequestRequestTypeDef",
    "DescribeStudioLifecycleConfigResponseOutputTypeDef",
    "DescribeSubscribedWorkteamRequestRequestTypeDef",
    "SubscribedWorkteamOutputTypeDef",
    "DescribeTrainingJobRequestRequestTypeDef",
    "MetricDataOutputTypeDef",
    "OutputDataConfigOutputTypeDef",
    "ProfilerConfigOutputTypeDef",
    "ProfilerRuleConfigurationOutputTypeDef",
    "ProfilerRuleEvaluationStatusOutputTypeDef",
    "RetryStrategyOutputTypeDef",
    "SecondaryStatusTransitionOutputTypeDef",
    "TensorBoardOutputConfigOutputTypeDef",
    "WarmPoolStatusOutputTypeDef",
    "DescribeTransformJobRequestRequestTypeDef",
    "ModelClientConfigOutputTypeDef",
    "TransformOutputOutputTypeDef",
    "TransformResourcesOutputTypeDef",
    "DescribeTrialComponentRequestRequestTypeDef",
    "TrialComponentArtifactOutputTypeDef",
    "TrialComponentMetricSummaryOutputTypeDef",
    "TrialComponentParameterValueOutputTypeDef",
    "TrialComponentSourceOutputTypeDef",
    "TrialComponentStatusOutputTypeDef",
    "DescribeTrialRequestRequestTypeDef",
    "TrialSourceOutputTypeDef",
    "DescribeUserProfileRequestRequestTypeDef",
    "DescribeWorkforceRequestRequestTypeDef",
    "DescribeWorkteamRequestRequestTypeDef",
    "ProductionVariantServerlessUpdateConfigTypeDef",
    "DeviceDeploymentSummaryOutputTypeDef",
    "DeviceFleetSummaryOutputTypeDef",
    "DeviceStatsOutputTypeDef",
    "EdgeModelSummaryOutputTypeDef",
    "DeviceTypeDef",
    "DisassociateTrialComponentRequestRequestTypeDef",
    "DisassociateTrialComponentResponseOutputTypeDef",
    "DomainDetailsOutputTypeDef",
    "FileSourceOutputTypeDef",
    "FileSourceTypeDef",
    "EMRStepMetadataOutputTypeDef",
    "EdgeDeploymentPlanSummaryOutputTypeDef",
    "EdgeModelStatOutputTypeDef",
    "EdgeOutputTypeDef",
    "EdgePackagingJobSummaryOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointConfigSummaryOutputTypeDef",
    "EndpointInfoOutputTypeDef",
    "EndpointInfoTypeDef",
    "ProductionVariantServerlessConfigOutputTypeDef",
    "ProductionVariantServerlessConfigTypeDef",
    "InferenceMetricsOutputTypeDef",
    "EndpointSummaryOutputTypeDef",
    "EnvironmentParameterOutputTypeDef",
    "FailStepMetadataOutputTypeDef",
    "FeatureParameterTypeDef",
    "FileSystemConfigOutputTypeDef",
    "FileSystemConfigTypeDef",
    "FilterTypeDef",
    "FinalHyperParameterTuningJobObjectiveMetricOutputTypeDef",
    "FlowDefinitionSummaryOutputTypeDef",
    "GetDeviceFleetReportRequestRequestTypeDef",
    "GetLineageGroupPolicyRequestRequestTypeDef",
    "GetLineageGroupPolicyResponseOutputTypeDef",
    "GetModelPackageGroupPolicyInputRequestTypeDef",
    "GetModelPackageGroupPolicyOutputOutputTypeDef",
    "GetSagemakerServicecatalogPortfolioStatusOutputOutputTypeDef",
    "PropertyNameSuggestionOutputTypeDef",
    "GitConfigForUpdateTypeDef",
    "HubContentInfoOutputTypeDef",
    "HubInfoOutputTypeDef",
    "HumanLoopActivationConditionsConfigOutputTypeDef",
    "HumanLoopActivationConditionsConfigTypeDef",
    "UiConfigOutputTypeDef",
    "UiConfigTypeDef",
    "HumanTaskUiSummaryOutputTypeDef",
    "HyperParameterTuningJobObjectiveOutputTypeDef",
    "HyperParameterTuningJobObjectiveTypeDef",
    "HyperParameterTuningInstanceConfigOutputTypeDef",
    "HyperParameterTuningInstanceConfigTypeDef",
    "ResourceLimitsOutputTypeDef",
    "ResourceLimitsTypeDef",
    "HyperbandStrategyConfigOutputTypeDef",
    "HyperbandStrategyConfigTypeDef",
    "ParentHyperParameterTuningJobOutputTypeDef",
    "ParentHyperParameterTuningJobTypeDef",
    "IamIdentityOutputTypeDef",
    "RepositoryAuthConfigOutputTypeDef",
    "RepositoryAuthConfigTypeDef",
    "ImageOutputTypeDef",
    "ImageVersionOutputTypeDef",
    "ImportHubContentResponseOutputTypeDef",
    "RecommendationMetricsOutputTypeDef",
    "InferenceRecommendationsJobOutputTypeDef",
    "InstanceGroupOutputTypeDef",
    "InstanceGroupTypeDef",
    "IntegerParameterRangeOutputTypeDef",
    "IntegerParameterRangeSpecificationOutputTypeDef",
    "IntegerParameterRangeSpecificationTypeDef",
    "IntegerParameterRangeTypeDef",
    "KernelSpecOutputTypeDef",
    "KernelSpecTypeDef",
    "LabelCountersForWorkteamOutputTypeDef",
    "LabelingJobDataAttributesOutputTypeDef",
    "LabelingJobDataAttributesTypeDef",
    "LabelingJobS3DataSourceOutputTypeDef",
    "LabelingJobSnsDataSourceOutputTypeDef",
    "LabelingJobS3DataSourceTypeDef",
    "LabelingJobSnsDataSourceTypeDef",
    "LineageGroupSummaryOutputTypeDef",
    "ListActionsRequestListActionsPaginateTypeDef",
    "ListActionsRequestRequestTypeDef",
    "ListAlgorithmsInputListAlgorithmsPaginateTypeDef",
    "ListAlgorithmsInputRequestTypeDef",
    "ListAliasesRequestListAliasesPaginateTypeDef",
    "ListAliasesRequestRequestTypeDef",
    "ListAliasesResponseOutputTypeDef",
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
    "MonitoringJobDefinitionSummaryOutputTypeDef",
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
    "ModelCardExportJobSummaryOutputTypeDef",
    "ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef",
    "ListModelCardVersionsRequestRequestTypeDef",
    "ModelCardVersionSummaryOutputTypeDef",
    "ListModelCardsRequestListModelCardsPaginateTypeDef",
    "ListModelCardsRequestRequestTypeDef",
    "ModelCardSummaryOutputTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestRequestTypeDef",
    "ModelMetadataSummaryOutputTypeDef",
    "ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef",
    "ListModelPackageGroupsInputRequestTypeDef",
    "ModelPackageGroupSummaryOutputTypeDef",
    "ListModelPackagesInputListModelPackagesPaginateTypeDef",
    "ListModelPackagesInputRequestTypeDef",
    "ModelPackageSummaryOutputTypeDef",
    "ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef",
    "ListModelQualityJobDefinitionsRequestRequestTypeDef",
    "ListModelsInputListModelsPaginateTypeDef",
    "ListModelsInputRequestTypeDef",
    "ModelSummaryOutputTypeDef",
    "ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef",
    "ListMonitoringAlertHistoryRequestRequestTypeDef",
    "MonitoringAlertHistorySummaryOutputTypeDef",
    "ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef",
    "ListMonitoringAlertsRequestRequestTypeDef",
    "ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef",
    "ListMonitoringExecutionsRequestRequestTypeDef",
    "ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef",
    "ListMonitoringSchedulesRequestRequestTypeDef",
    "MonitoringScheduleSummaryOutputTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputRequestTypeDef",
    "NotebookInstanceLifecycleConfigSummaryOutputTypeDef",
    "ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef",
    "ListNotebookInstancesInputRequestTypeDef",
    "NotebookInstanceSummaryOutputTypeDef",
    "ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef",
    "ListPipelineExecutionStepsRequestRequestTypeDef",
    "ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef",
    "ListPipelineExecutionsRequestRequestTypeDef",
    "PipelineExecutionSummaryOutputTypeDef",
    "ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef",
    "ListPipelineParametersForExecutionRequestRequestTypeDef",
    "ParameterOutputTypeDef",
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "PipelineSummaryOutputTypeDef",
    "ListProcessingJobsRequestListProcessingJobsPaginateTypeDef",
    "ListProcessingJobsRequestRequestTypeDef",
    "ProcessingJobSummaryOutputTypeDef",
    "ListProjectsInputRequestTypeDef",
    "ProjectSummaryOutputTypeDef",
    "ListSpacesRequestListSpacesPaginateTypeDef",
    "ListSpacesRequestRequestTypeDef",
    "SpaceDetailsOutputTypeDef",
    "ListStageDevicesRequestListStageDevicesPaginateTypeDef",
    "ListStageDevicesRequestRequestTypeDef",
    "ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef",
    "ListStudioLifecycleConfigsRequestRequestTypeDef",
    "StudioLifecycleConfigDetailsOutputTypeDef",
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
    "TransformJobSummaryOutputTypeDef",
    "ListTrialComponentsRequestListTrialComponentsPaginateTypeDef",
    "ListTrialComponentsRequestRequestTypeDef",
    "ListTrialsRequestListTrialsPaginateTypeDef",
    "ListTrialsRequestRequestTypeDef",
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
    "ListUserProfilesRequestRequestTypeDef",
    "UserProfileDetailsOutputTypeDef",
    "ListWorkforcesRequestListWorkforcesPaginateTypeDef",
    "ListWorkforcesRequestRequestTypeDef",
    "ListWorkteamsRequestListWorkteamsPaginateTypeDef",
    "ListWorkteamsRequestRequestTypeDef",
    "OidcMemberDefinitionOutputTypeDef",
    "OidcMemberDefinitionTypeDef",
    "MonitoringGroundTruthS3InputOutputTypeDef",
    "MonitoringGroundTruthS3InputTypeDef",
    "ModelDashboardEndpointOutputTypeDef",
    "ModelDashboardIndicatorActionOutputTypeDef",
    "S3ModelDataSourceOutputTypeDef",
    "S3ModelDataSourceTypeDef",
    "RealTimeInferenceConfigOutputTypeDef",
    "RealTimeInferenceConfigTypeDef",
    "ModelInputOutputTypeDef",
    "ModelInputTypeDef",
    "ModelLatencyThresholdOutputTypeDef",
    "ModelLatencyThresholdTypeDef",
    "ModelMetadataFilterTypeDef",
    "ModelPackageStatusItemOutputTypeDef",
    "ModelStepMetadataOutputTypeDef",
    "MonitoringAppSpecificationOutputTypeDef",
    "MonitoringAppSpecificationTypeDef",
    "MonitoringClusterConfigOutputTypeDef",
    "MonitoringClusterConfigTypeDef",
    "MonitoringCsvDatasetFormatOutputTypeDef",
    "MonitoringCsvDatasetFormatTypeDef",
    "MonitoringJsonDatasetFormatOutputTypeDef",
    "MonitoringJsonDatasetFormatTypeDef",
    "MonitoringS3OutputOutputTypeDef",
    "MonitoringS3OutputTypeDef",
    "ScheduleConfigOutputTypeDef",
    "ScheduleConfigTypeDef",
    "NotificationConfigurationOutputTypeDef",
    "S3StorageConfigOutputTypeDef",
    "S3StorageConfigTypeDef",
    "OidcConfigForResponseOutputTypeDef",
    "OnlineStoreSecurityConfigOutputTypeDef",
    "TtlDurationOutputTypeDef",
    "OnlineStoreSecurityConfigTypeDef",
    "TtlDurationTypeDef",
    "TargetPlatformOutputTypeDef",
    "TargetPlatformTypeDef",
    "OutputParameterTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterTypeDef",
    "ParentOutputTypeDef",
    "ProductionVariantStatusOutputTypeDef",
    "PhaseOutputTypeDef",
    "PhaseTypeDef",
    "ProcessingJobStepMetadataOutputTypeDef",
    "QualityCheckStepMetadataOutputTypeDef",
    "RegisterModelStepMetadataOutputTypeDef",
    "TrainingJobStepMetadataOutputTypeDef",
    "TransformJobStepMetadataOutputTypeDef",
    "TuningJobStepMetaDataOutputTypeDef",
    "SelectiveExecutionResultOutputTypeDef",
    "ProcessingClusterConfigOutputTypeDef",
    "ProcessingClusterConfigTypeDef",
    "ProcessingFeatureStoreOutputOutputTypeDef",
    "ProcessingFeatureStoreOutputTypeDef",
    "ProcessingS3InputOutputTypeDef",
    "ProcessingS3InputTypeDef",
    "ProcessingS3OutputOutputTypeDef",
    "ProcessingS3OutputTypeDef",
    "ProductionVariantCoreDumpConfigOutputTypeDef",
    "ProductionVariantCoreDumpConfigTypeDef",
    "ProfilerConfigForUpdateTypeDef",
    "PropertyNameQueryTypeDef",
    "ProvisioningParameterOutputTypeDef",
    "ProvisioningParameterTypeDef",
    "USDOutputTypeDef",
    "USDTypeDef",
    "PutModelPackageGroupPolicyInputRequestTypeDef",
    "PutModelPackageGroupPolicyOutputOutputTypeDef",
    "QueryFiltersTypeDef",
    "VertexOutputTypeDef",
    "RStudioServerProAppSettingsOutputTypeDef",
    "RStudioServerProAppSettingsTypeDef",
    "RecommendationJobCompiledOutputConfigTypeDef",
    "RecommendationJobPayloadConfigOutputTypeDef",
    "RecommendationJobPayloadConfigTypeDef",
    "RecommendationJobResourceLimitOutputTypeDef",
    "RecommendationJobVpcConfigOutputTypeDef",
    "RecommendationJobResourceLimitTypeDef",
    "RecommendationJobVpcConfigTypeDef",
    "RenderableTaskTypeDef",
    "RenderingErrorOutputTypeDef",
    "ResourceConfigForUpdateTypeDef",
    "ResponseMetadataTypeDef",
    "RetryPipelineExecutionResponseOutputTypeDef",
    "SearchRequestRequestTypeDef",
    "SearchRequestSearchPaginateTypeDef",
    "SelectedStepOutputTypeDef",
    "SelectedStepTypeDef",
    "SendPipelineExecutionStepFailureRequestRequestTypeDef",
    "SendPipelineExecutionStepFailureResponseOutputTypeDef",
    "SendPipelineExecutionStepSuccessResponseOutputTypeDef",
    "ShadowModelVariantConfigOutputTypeDef",
    "ShadowModelVariantConfigTypeDef",
    "SharingSettingsOutputTypeDef",
    "SharingSettingsTypeDef",
    "SourceAlgorithmOutputTypeDef",
    "SourceAlgorithmTypeDef",
    "SourceIpConfigOutputTypeDef",
    "StartEdgeDeploymentStageRequestRequestTypeDef",
    "StartInferenceExperimentRequestRequestTypeDef",
    "StartInferenceExperimentResponseOutputTypeDef",
    "StartMonitoringScheduleRequestRequestTypeDef",
    "StartNotebookInstanceInputRequestTypeDef",
    "StartPipelineExecutionResponseOutputTypeDef",
    "StopAutoMLJobRequestRequestTypeDef",
    "StopCompilationJobRequestRequestTypeDef",
    "StopEdgeDeploymentStageRequestRequestTypeDef",
    "StopEdgePackagingJobRequestRequestTypeDef",
    "StopHyperParameterTuningJobRequestRequestTypeDef",
    "StopInferenceExperimentResponseOutputTypeDef",
    "StopInferenceRecommendationsJobRequestRequestTypeDef",
    "StopLabelingJobRequestRequestTypeDef",
    "StopMonitoringScheduleRequestRequestTypeDef",
    "StopNotebookInstanceInputRequestTypeDef",
    "StopPipelineExecutionRequestRequestTypeDef",
    "StopPipelineExecutionResponseOutputTypeDef",
    "StopProcessingJobRequestRequestTypeDef",
    "StopTrainingJobRequestRequestTypeDef",
    "StopTransformJobRequestRequestTypeDef",
    "TimeSeriesConfigOutputTypeDef",
    "TimeSeriesConfigTypeDef",
    "TimeSeriesTransformationsOutputTypeDef",
    "TimeSeriesTransformationsTypeDef",
    "TrainingRepositoryAuthConfigOutputTypeDef",
    "TrainingRepositoryAuthConfigTypeDef",
    "TransformS3DataSourceOutputTypeDef",
    "TransformS3DataSourceTypeDef",
    "UpdateActionRequestRequestTypeDef",
    "UpdateActionResponseOutputTypeDef",
    "UpdateAppImageConfigResponseOutputTypeDef",
    "UpdateArtifactRequestRequestTypeDef",
    "UpdateArtifactResponseOutputTypeDef",
    "UpdateCodeRepositoryOutputOutputTypeDef",
    "UpdateContextRequestRequestTypeDef",
    "UpdateContextResponseOutputTypeDef",
    "UpdateDomainResponseOutputTypeDef",
    "VariantPropertyTypeDef",
    "UpdateEndpointOutputOutputTypeDef",
    "UpdateEndpointWeightsAndCapacitiesOutputOutputTypeDef",
    "UpdateExperimentRequestRequestTypeDef",
    "UpdateExperimentResponseOutputTypeDef",
    "UpdateFeatureGroupResponseOutputTypeDef",
    "UpdateHubRequestRequestTypeDef",
    "UpdateHubResponseOutputTypeDef",
    "UpdateImageRequestRequestTypeDef",
    "UpdateImageResponseOutputTypeDef",
    "UpdateImageVersionRequestRequestTypeDef",
    "UpdateImageVersionResponseOutputTypeDef",
    "UpdateInferenceExperimentResponseOutputTypeDef",
    "UpdateModelCardRequestRequestTypeDef",
    "UpdateModelCardResponseOutputTypeDef",
    "UpdateModelPackageOutputOutputTypeDef",
    "UpdateMonitoringAlertRequestRequestTypeDef",
    "UpdateMonitoringAlertResponseOutputTypeDef",
    "UpdateMonitoringScheduleResponseOutputTypeDef",
    "UpdatePipelineExecutionResponseOutputTypeDef",
    "UpdatePipelineResponseOutputTypeDef",
    "UpdateProjectOutputOutputTypeDef",
    "UpdateSpaceResponseOutputTypeDef",
    "UpdateTrainingJobResponseOutputTypeDef",
    "UpdateTrialComponentResponseOutputTypeDef",
    "UpdateTrialRequestRequestTypeDef",
    "UpdateTrialResponseOutputTypeDef",
    "UpdateUserProfileResponseOutputTypeDef",
    "WorkforceVpcConfigResponseOutputTypeDef",
    "ActionSummaryOutputTypeDef",
    "AddTagsInputRequestTypeDef",
    "CreateExperimentRequestRequestTypeDef",
    "CreateImageRequestRequestTypeDef",
    "CreateModelPackageGroupInputRequestTypeDef",
    "CreateStudioLifecycleConfigRequestRequestTypeDef",
    "ImportHubContentRequestRequestTypeDef",
    "AddTagsOutputOutputTypeDef",
    "ListTagsOutputOutputTypeDef",
    "AutoRollbackConfigOutputTypeDef",
    "AutoRollbackConfigTypeDef",
    "HyperParameterAlgorithmSpecificationOutputTypeDef",
    "HyperParameterAlgorithmSpecificationTypeDef",
    "AlgorithmStatusDetailsOutputTypeDef",
    "ListAlgorithmsOutputOutputTypeDef",
    "ListAppsResponseOutputTypeDef",
    "ArtifactSourceOutputTypeDef",
    "ArtifactSourceTypeDef",
    "AsyncInferenceOutputConfigOutputTypeDef",
    "AsyncInferenceOutputConfigTypeDef",
    "AutoMLCandidateGenerationConfigOutputTypeDef",
    "CandidateGenerationConfigOutputTypeDef",
    "AutoMLCandidateGenerationConfigTypeDef",
    "CandidateGenerationConfigTypeDef",
    "AutoMLDataSourceOutputTypeDef",
    "AutoMLDataSourceTypeDef",
    "ImageClassificationJobConfigOutputTypeDef",
    "TextClassificationJobConfigOutputTypeDef",
    "ImageClassificationJobConfigTypeDef",
    "TextClassificationJobConfigTypeDef",
    "ResolvedAttributesOutputTypeDef",
    "AutoMLJobSummaryOutputTypeDef",
    "AutoMLProblemTypeResolvedAttributesOutputTypeDef",
    "AutoMLSecurityConfigOutputTypeDef",
    "LabelingJobResourceConfigOutputTypeDef",
    "MonitoringNetworkConfigOutputTypeDef",
    "NetworkConfigOutputTypeDef",
    "AutoMLSecurityConfigTypeDef",
    "LabelingJobResourceConfigTypeDef",
    "MonitoringNetworkConfigTypeDef",
    "NetworkConfigTypeDef",
    "BiasOutputTypeDef",
    "DriftCheckModelDataQualityOutputTypeDef",
    "DriftCheckModelQualityOutputTypeDef",
    "ExplainabilityOutputTypeDef",
    "ModelDataQualityOutputTypeDef",
    "ModelQualityOutputTypeDef",
    "BiasTypeDef",
    "DriftCheckModelDataQualityTypeDef",
    "DriftCheckModelQualityTypeDef",
    "ExplainabilityTypeDef",
    "ModelDataQualityTypeDef",
    "ModelQualityTypeDef",
    "CallbackStepMetadataOutputTypeDef",
    "LambdaStepMetadataOutputTypeDef",
    "CandidatePropertiesOutputTypeDef",
    "CanvasAppSettingsOutputTypeDef",
    "CanvasAppSettingsTypeDef",
    "RollingUpdatePolicyOutputTypeDef",
    "TrafficRoutingConfigOutputTypeDef",
    "RollingUpdatePolicyTypeDef",
    "TrafficRoutingConfigTypeDef",
    "InferenceExperimentDataStorageConfigOutputTypeDef",
    "InferenceExperimentDataStorageConfigTypeDef",
    "DataCaptureConfigOutputTypeDef",
    "DataCaptureConfigTypeDef",
    "EnvironmentParameterRangesOutputTypeDef",
    "EnvironmentParameterRangesTypeDef",
    "ClarifyShapConfigOutputTypeDef",
    "ClarifyShapConfigTypeDef",
    "CodeRepositorySummaryOutputTypeDef",
    "DescribeCodeRepositoryOutputOutputTypeDef",
    "DebugHookConfigOutputTypeDef",
    "DebugHookConfigTypeDef",
    "ListCompilationJobsResponseOutputTypeDef",
    "ContextSummaryOutputTypeDef",
    "CreateContextRequestRequestTypeDef",
    "TuningJobCompletionCriteriaOutputTypeDef",
    "TuningJobCompletionCriteriaTypeDef",
    "CreateActionRequestRequestTypeDef",
    "CreateTrialRequestRequestTypeDef",
    "CreateAppRequestRequestTypeDef",
    "JupyterServerAppSettingsTypeDef",
    "RStudioServerProDomainSettingsForUpdateTypeDef",
    "RStudioServerProDomainSettingsTypeDef",
    "TensorBoardAppSettingsTypeDef",
    "CreateCodeRepositoryInputRequestTypeDef",
    "CreateDeviceFleetRequestRequestTypeDef",
    "CreateEdgePackagingJobRequestRequestTypeDef",
    "UpdateDeviceFleetRequestRequestTypeDef",
    "CreateHubRequestRequestTypeDef",
    "CreateHumanTaskUiRequestRequestTypeDef",
    "CreateModelCardExportJobRequestRequestTypeDef",
    "CreateModelCardRequestRequestTypeDef",
    "CreateNotebookInstanceInputRequestTypeDef",
    "UpdateNotebookInstanceInputRequestTypeDef",
    "CreateNotebookInstanceLifecycleConfigInputRequestTypeDef",
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
    "ModelBiasBaselineConfigOutputTypeDef",
    "ModelExplainabilityBaselineConfigOutputTypeDef",
    "ModelQualityBaselineConfigOutputTypeDef",
    "DataQualityBaselineConfigOutputTypeDef",
    "MonitoringBaselineConfigOutputTypeDef",
    "ModelBiasBaselineConfigTypeDef",
    "ModelExplainabilityBaselineConfigTypeDef",
    "ModelQualityBaselineConfigTypeDef",
    "DataQualityBaselineConfigTypeDef",
    "MonitoringBaselineConfigTypeDef",
    "DataSourceOutputTypeDef",
    "DataSourceTypeDef",
    "DatasetDefinitionOutputTypeDef",
    "DatasetDefinitionTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeploymentRecommendationOutputTypeDef",
    "DeploymentStageStatusSummaryOutputTypeDef",
    "DeploymentStageTypeDef",
    "DescribeAppResponseOutputTypeDef",
    "JupyterServerAppSettingsOutputTypeDef",
    "KernelGatewayAppSettingsOutputTypeDef",
    "RSessionAppSettingsOutputTypeDef",
    "RStudioServerProDomainSettingsOutputTypeDef",
    "TensorBoardAppSettingsOutputTypeDef",
    "DescribeDeviceFleetResponseOutputTypeDef",
    "DescribeDeviceResponseOutputTypeDef",
    "DescribeEdgePackagingJobResponseOutputTypeDef",
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
    "ExperimentSummaryOutputTypeDef",
    "FeatureGroupSummaryOutputTypeDef",
    "DescribeFeatureMetadataResponseOutputTypeDef",
    "FeatureMetadataOutputTypeDef",
    "DescribeHubContentResponseOutputTypeDef",
    "DescribeHubResponseOutputTypeDef",
    "DescribeHumanTaskUiResponseOutputTypeDef",
    "InferenceExperimentSummaryOutputTypeDef",
    "DescribeModelCardExportJobResponseOutputTypeDef",
    "ListMonitoringExecutionsResponseOutputTypeDef",
    "DescribeNotebookInstanceLifecycleConfigOutputOutputTypeDef",
    "DescribeNotebookInstanceOutputOutputTypeDef",
    "DescribeSubscribedWorkteamResponseOutputTypeDef",
    "ListSubscribedWorkteamsResponseOutputTypeDef",
    "TrainingJobSummaryOutputTypeDef",
    "TrialSummaryOutputTypeDef",
    "DesiredWeightAndCapacityTypeDef",
    "ListStageDevicesResponseOutputTypeDef",
    "ListDeviceFleetsResponseOutputTypeDef",
    "DeviceSummaryOutputTypeDef",
    "RegisterDevicesRequestRequestTypeDef",
    "UpdateDevicesRequestRequestTypeDef",
    "ListDomainsResponseOutputTypeDef",
    "DriftCheckBiasOutputTypeDef",
    "DriftCheckExplainabilityOutputTypeDef",
    "DriftCheckBiasTypeDef",
    "DriftCheckExplainabilityTypeDef",
    "ListEdgeDeploymentPlansResponseOutputTypeDef",
    "GetDeviceFleetReportResponseOutputTypeDef",
    "ListEdgePackagingJobsResponseOutputTypeDef",
    "ListEndpointConfigsOutputOutputTypeDef",
    "EndpointOutputConfigurationOutputTypeDef",
    "EndpointPerformanceOutputTypeDef",
    "ListEndpointsOutputOutputTypeDef",
    "ModelConfigurationOutputTypeDef",
    "UpdateFeatureMetadataRequestRequestTypeDef",
    "NestedFiltersTypeDef",
    "HyperParameterTrainingJobSummaryOutputTypeDef",
    "ListFlowDefinitionsResponseOutputTypeDef",
    "GetSearchSuggestionsResponseOutputTypeDef",
    "UpdateCodeRepositoryInputRequestTypeDef",
    "ListHubContentVersionsResponseOutputTypeDef",
    "ListHubContentsResponseOutputTypeDef",
    "ListHubsResponseOutputTypeDef",
    "HumanLoopActivationConfigOutputTypeDef",
    "HumanLoopActivationConfigTypeDef",
    "ListHumanTaskUisResponseOutputTypeDef",
    "HyperParameterTuningResourceConfigOutputTypeDef",
    "HyperParameterTuningResourceConfigTypeDef",
    "HyperParameterTuningJobSummaryOutputTypeDef",
    "HyperParameterTuningJobStrategyConfigOutputTypeDef",
    "HyperParameterTuningJobStrategyConfigTypeDef",
    "HyperParameterTuningJobWarmStartConfigOutputTypeDef",
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    "UserContextOutputTypeDef",
    "ImageConfigOutputTypeDef",
    "ImageConfigTypeDef",
    "ListImagesResponseOutputTypeDef",
    "ListImageVersionsResponseOutputTypeDef",
    "ListInferenceRecommendationsJobsResponseOutputTypeDef",
    "ResourceConfigOutputTypeDef",
    "ResourceConfigTypeDef",
    "ParameterRangesOutputTypeDef",
    "ParameterRangeOutputTypeDef",
    "ParameterRangeTypeDef",
    "ParameterRangesTypeDef",
    "KernelGatewayImageConfigOutputTypeDef",
    "KernelGatewayImageConfigTypeDef",
    "LabelingJobForWorkteamSummaryOutputTypeDef",
    "LabelingJobDataSourceOutputTypeDef",
    "LabelingJobDataSourceTypeDef",
    "ListLineageGroupsResponseOutputTypeDef",
    "ListDataQualityJobDefinitionsResponseOutputTypeDef",
    "ListModelBiasJobDefinitionsResponseOutputTypeDef",
    "ListModelExplainabilityJobDefinitionsResponseOutputTypeDef",
    "ListModelQualityJobDefinitionsResponseOutputTypeDef",
    "ListModelCardExportJobsResponseOutputTypeDef",
    "ListModelCardVersionsResponseOutputTypeDef",
    "ListModelCardsResponseOutputTypeDef",
    "ListModelMetadataResponseOutputTypeDef",
    "ListModelPackageGroupsOutputOutputTypeDef",
    "ListModelPackagesOutputOutputTypeDef",
    "ListModelsOutputOutputTypeDef",
    "ListMonitoringAlertHistoryResponseOutputTypeDef",
    "ListMonitoringSchedulesResponseOutputTypeDef",
    "ListNotebookInstanceLifecycleConfigsOutputOutputTypeDef",
    "ListNotebookInstancesOutputOutputTypeDef",
    "ListPipelineExecutionsResponseOutputTypeDef",
    "ListPipelineParametersForExecutionResponseOutputTypeDef",
    "ListPipelinesResponseOutputTypeDef",
    "ListProcessingJobsResponseOutputTypeDef",
    "ListProjectsOutputOutputTypeDef",
    "ListSpacesResponseOutputTypeDef",
    "ListStudioLifecycleConfigsResponseOutputTypeDef",
    "ListTransformJobsResponseOutputTypeDef",
    "ListUserProfilesResponseOutputTypeDef",
    "MemberDefinitionOutputTypeDef",
    "MemberDefinitionTypeDef",
    "MonitoringAlertActionsOutputTypeDef",
    "ModelDataSourceOutputTypeDef",
    "ModelDataSourceTypeDef",
    "ModelInfrastructureConfigOutputTypeDef",
    "ModelInfrastructureConfigTypeDef",
    "ModelPackageContainerDefinitionOutputTypeDef",
    "ModelPackageContainerDefinitionTypeDef",
    "RecommendationJobStoppingConditionsOutputTypeDef",
    "RecommendationJobStoppingConditionsTypeDef",
    "ModelMetadataSearchExpressionTypeDef",
    "ModelPackageStatusDetailsOutputTypeDef",
    "MonitoringResourcesOutputTypeDef",
    "MonitoringResourcesTypeDef",
    "MonitoringDatasetFormatOutputTypeDef",
    "MonitoringDatasetFormatTypeDef",
    "MonitoringOutputOutputTypeDef",
    "MonitoringOutputTypeDef",
    "OfflineStoreConfigOutputTypeDef",
    "OfflineStoreConfigTypeDef",
    "OnlineStoreConfigOutputTypeDef",
    "OnlineStoreConfigTypeDef",
    "OnlineStoreConfigUpdateTypeDef",
    "OutputConfigOutputTypeDef",
    "OutputConfigTypeDef",
    "SendPipelineExecutionStepSuccessRequestRequestTypeDef",
    "PendingProductionVariantSummaryOutputTypeDef",
    "ProductionVariantSummaryOutputTypeDef",
    "TrafficPatternOutputTypeDef",
    "TrafficPatternTypeDef",
    "ProcessingResourcesOutputTypeDef",
    "ProcessingResourcesTypeDef",
    "ProcessingOutputOutputTypeDef",
    "ProcessingOutputTypeDef",
    "ProductionVariantOutputTypeDef",
    "ProductionVariantTypeDef",
    "SuggestionQueryTypeDef",
    "ServiceCatalogProvisioningDetailsOutputTypeDef",
    "ServiceCatalogProvisioningDetailsTypeDef",
    "ServiceCatalogProvisioningUpdateDetailsTypeDef",
    "PublicWorkforceTaskPriceOutputTypeDef",
    "PublicWorkforceTaskPriceTypeDef",
    "QueryLineageRequestRequestTypeDef",
    "QueryLineageResponseOutputTypeDef",
    "RecommendationJobOutputConfigTypeDef",
    "RecommendationJobContainerConfigOutputTypeDef",
    "RecommendationJobContainerConfigTypeDef",
    "RenderUiTemplateRequestRequestTypeDef",
    "RenderUiTemplateResponseOutputTypeDef",
    "UpdateTrainingJobRequestRequestTypeDef",
    "SelectiveExecutionConfigOutputTypeDef",
    "SelectiveExecutionConfigTypeDef",
    "ShadowModeConfigOutputTypeDef",
    "ShadowModeConfigTypeDef",
    "SourceAlgorithmSpecificationOutputTypeDef",
    "SourceAlgorithmSpecificationTypeDef",
    "TimeSeriesForecastingJobConfigOutputTypeDef",
    "TimeSeriesForecastingJobConfigTypeDef",
    "TrainingImageConfigOutputTypeDef",
    "TrainingImageConfigTypeDef",
    "TransformDataSourceOutputTypeDef",
    "TransformDataSourceTypeDef",
    "WorkforceOutputTypeDef",
    "ListActionsResponseOutputTypeDef",
    "ArtifactSummaryOutputTypeDef",
    "CreateArtifactRequestRequestTypeDef",
    "DeleteArtifactRequestRequestTypeDef",
    "AsyncInferenceConfigOutputTypeDef",
    "AsyncInferenceConfigTypeDef",
    "TabularJobConfigOutputTypeDef",
    "TabularJobConfigTypeDef",
    "AutoMLChannelOutputTypeDef",
    "AutoMLJobChannelOutputTypeDef",
    "AutoMLChannelTypeDef",
    "AutoMLJobChannelTypeDef",
    "ListAutoMLJobsResponseOutputTypeDef",
    "AutoMLResolvedAttributesOutputTypeDef",
    "AutoMLJobConfigOutputTypeDef",
    "LabelingJobAlgorithmsConfigOutputTypeDef",
    "AutoMLJobConfigTypeDef",
    "LabelingJobAlgorithmsConfigTypeDef",
    "ModelMetricsOutputTypeDef",
    "ModelMetricsTypeDef",
    "PipelineExecutionStepMetadataOutputTypeDef",
    "AutoMLCandidateOutputTypeDef",
    "BlueGreenUpdatePolicyOutputTypeDef",
    "BlueGreenUpdatePolicyTypeDef",
    "EndpointInputConfigurationOutputTypeDef",
    "EndpointInputConfigurationTypeDef",
    "ClarifyExplainerConfigOutputTypeDef",
    "ClarifyExplainerConfigTypeDef",
    "ListCodeRepositoriesOutputOutputTypeDef",
    "ListContextsResponseOutputTypeDef",
    "DomainSettingsForUpdateTypeDef",
    "DomainSettingsTypeDef",
    "DefaultSpaceSettingsTypeDef",
    "SpaceSettingsTypeDef",
    "UserSettingsTypeDef",
    "ChannelOutputTypeDef",
    "ChannelTypeDef",
    "ProcessingInputOutputTypeDef",
    "ProcessingInputTypeDef",
    "DescribeEdgeDeploymentPlanResponseOutputTypeDef",
    "CreateEdgeDeploymentPlanRequestRequestTypeDef",
    "CreateEdgeDeploymentStageRequestRequestTypeDef",
    "DefaultSpaceSettingsOutputTypeDef",
    "SpaceSettingsOutputTypeDef",
    "DomainSettingsOutputTypeDef",
    "UserSettingsOutputTypeDef",
    "ListExperimentsResponseOutputTypeDef",
    "ListFeatureGroupsResponseOutputTypeDef",
    "ListInferenceExperimentsResponseOutputTypeDef",
    "ListTrainingJobsResponseOutputTypeDef",
    "ListTrialsResponseOutputTypeDef",
    "UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef",
    "ListDevicesResponseOutputTypeDef",
    "DriftCheckBaselinesOutputTypeDef",
    "DriftCheckBaselinesTypeDef",
    "InferenceRecommendationOutputTypeDef",
    "RecommendationJobInferenceBenchmarkOutputTypeDef",
    "SearchExpressionTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobResponseOutputTypeDef",
    "ListHyperParameterTuningJobsResponseOutputTypeDef",
    "AssociationSummaryOutputTypeDef",
    "DescribeActionResponseOutputTypeDef",
    "DescribeArtifactResponseOutputTypeDef",
    "DescribeContextResponseOutputTypeDef",
    "DescribeExperimentResponseOutputTypeDef",
    "DescribeLineageGroupResponseOutputTypeDef",
    "DescribeModelCardResponseOutputTypeDef",
    "DescribeModelPackageGroupOutputOutputTypeDef",
    "DescribePipelineResponseOutputTypeDef",
    "DescribeTrialComponentResponseOutputTypeDef",
    "DescribeTrialResponseOutputTypeDef",
    "ExperimentOutputTypeDef",
    "ModelCardOutputTypeDef",
    "ModelDashboardModelCardOutputTypeDef",
    "ModelPackageGroupOutputTypeDef",
    "PipelineOutputTypeDef",
    "TrialComponentSimpleSummaryOutputTypeDef",
    "TrialComponentSummaryOutputTypeDef",
    "HyperParameterTuningJobConfigOutputTypeDef",
    "HyperParameterSpecificationOutputTypeDef",
    "HyperParameterSpecificationTypeDef",
    "HyperParameterTuningJobConfigTypeDef",
    "AppImageConfigDetailsOutputTypeDef",
    "DescribeAppImageConfigResponseOutputTypeDef",
    "CreateAppImageConfigRequestRequestTypeDef",
    "UpdateAppImageConfigRequestRequestTypeDef",
    "ListLabelingJobsForWorkteamResponseOutputTypeDef",
    "LabelingJobInputConfigOutputTypeDef",
    "LabelingJobInputConfigTypeDef",
    "WorkteamOutputTypeDef",
    "CreateWorkteamRequestRequestTypeDef",
    "UpdateWorkteamRequestRequestTypeDef",
    "MonitoringAlertSummaryOutputTypeDef",
    "ContainerDefinitionOutputTypeDef",
    "ContainerDefinitionTypeDef",
    "ModelVariantConfigSummaryOutputTypeDef",
    "ModelVariantConfigTypeDef",
    "AdditionalInferenceSpecificationDefinitionOutputTypeDef",
    "InferenceSpecificationOutputTypeDef",
    "AdditionalInferenceSpecificationDefinitionTypeDef",
    "InferenceSpecificationTypeDef",
    "ListModelMetadataRequestListModelMetadataPaginateTypeDef",
    "ListModelMetadataRequestRequestTypeDef",
    "BatchTransformInputOutputTypeDef",
    "BatchTransformInputTypeDef",
    "MonitoringOutputConfigOutputTypeDef",
    "MonitoringOutputConfigTypeDef",
    "DescribeFeatureGroupResponseOutputTypeDef",
    "FeatureGroupOutputTypeDef",
    "CreateFeatureGroupRequestRequestTypeDef",
    "UpdateFeatureGroupRequestRequestTypeDef",
    "DescribeCompilationJobResponseOutputTypeDef",
    "CreateCompilationJobRequestRequestTypeDef",
    "PendingDeploymentSummaryOutputTypeDef",
    "ProcessingOutputConfigOutputTypeDef",
    "ProcessingOutputConfigTypeDef",
    "GetSearchSuggestionsRequestRequestTypeDef",
    "DescribeProjectOutputOutputTypeDef",
    "ProjectOutputTypeDef",
    "CreateProjectInputRequestTypeDef",
    "UpdateProjectInputRequestTypeDef",
    "HumanLoopConfigOutputTypeDef",
    "HumanTaskConfigOutputTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanTaskConfigTypeDef",
    "DescribePipelineExecutionResponseOutputTypeDef",
    "PipelineExecutionOutputTypeDef",
    "StartPipelineExecutionRequestRequestTypeDef",
    "AlgorithmSpecificationOutputTypeDef",
    "AlgorithmSpecificationTypeDef",
    "TransformInputOutputTypeDef",
    "TransformInputTypeDef",
    "DescribeWorkforceResponseOutputTypeDef",
    "ListWorkforcesResponseOutputTypeDef",
    "UpdateWorkforceResponseOutputTypeDef",
    "ListArtifactsResponseOutputTypeDef",
    "AutoMLProblemTypeConfigOutputTypeDef",
    "AutoMLProblemTypeConfigTypeDef",
    "CreateAutoMLJobRequestRequestTypeDef",
    "PipelineExecutionStepOutputTypeDef",
    "DescribeAutoMLJobResponseOutputTypeDef",
    "ListCandidatesForAutoMLJobResponseOutputTypeDef",
    "DeploymentConfigOutputTypeDef",
    "DeploymentConfigTypeDef",
    "RecommendationJobInputConfigOutputTypeDef",
    "RecommendationJobInputConfigTypeDef",
    "ExplainerConfigOutputTypeDef",
    "ExplainerConfigTypeDef",
    "CreateSpaceRequestRequestTypeDef",
    "UpdateSpaceRequestRequestTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateUserProfileRequestRequestTypeDef",
    "UpdateDomainRequestRequestTypeDef",
    "UpdateUserProfileRequestRequestTypeDef",
    "HyperParameterTrainingJobDefinitionOutputTypeDef",
    "TrainingJobDefinitionOutputTypeDef",
    "HyperParameterTrainingJobDefinitionTypeDef",
    "TrainingJobDefinitionTypeDef",
    "DescribeSpaceResponseOutputTypeDef",
    "DescribeDomainResponseOutputTypeDef",
    "DescribeUserProfileResponseOutputTypeDef",
    "InferenceRecommendationsJobStepOutputTypeDef",
    "ListAssociationsResponseOutputTypeDef",
    "TrialOutputTypeDef",
    "ListTrialComponentsResponseOutputTypeDef",
    "TrainingSpecificationOutputTypeDef",
    "TrainingSpecificationTypeDef",
    "ListAppImageConfigsResponseOutputTypeDef",
    "LabelingJobSummaryOutputTypeDef",
    "DescribeWorkteamResponseOutputTypeDef",
    "ListWorkteamsResponseOutputTypeDef",
    "UpdateWorkteamResponseOutputTypeDef",
    "ListMonitoringAlertsResponseOutputTypeDef",
    "DescribeModelOutputOutputTypeDef",
    "ModelOutputTypeDef",
    "CreateModelInputRequestTypeDef",
    "DescribeInferenceExperimentResponseOutputTypeDef",
    "CreateInferenceExperimentRequestRequestTypeDef",
    "StopInferenceExperimentRequestRequestTypeDef",
    "UpdateInferenceExperimentRequestRequestTypeDef",
    "BatchDescribeModelPackageSummaryOutputTypeDef",
    "UpdateModelPackageInputRequestTypeDef",
    "DataQualityJobInputOutputTypeDef",
    "ModelBiasJobInputOutputTypeDef",
    "ModelExplainabilityJobInputOutputTypeDef",
    "ModelQualityJobInputOutputTypeDef",
    "MonitoringInputOutputTypeDef",
    "DataQualityJobInputTypeDef",
    "ModelBiasJobInputTypeDef",
    "ModelExplainabilityJobInputTypeDef",
    "ModelQualityJobInputTypeDef",
    "MonitoringInputTypeDef",
    "DescribeProcessingJobResponseOutputTypeDef",
    "ProcessingJobOutputTypeDef",
    "CreateProcessingJobRequestRequestTypeDef",
    "DescribeFlowDefinitionResponseOutputTypeDef",
    "DescribeLabelingJobResponseOutputTypeDef",
    "CreateFlowDefinitionRequestRequestTypeDef",
    "CreateLabelingJobRequestRequestTypeDef",
    "DescribeTrainingJobResponseOutputTypeDef",
    "TrainingJobOutputTypeDef",
    "CreateTrainingJobRequestRequestTypeDef",
    "DescribeTransformJobResponseOutputTypeDef",
    "TransformJobDefinitionOutputTypeDef",
    "TransformJobOutputTypeDef",
    "CreateTransformJobRequestRequestTypeDef",
    "TransformJobDefinitionTypeDef",
    "DescribeAutoMLJobV2ResponseOutputTypeDef",
    "CreateAutoMLJobV2RequestRequestTypeDef",
    "ListPipelineExecutionStepsResponseOutputTypeDef",
    "CreateEndpointInputRequestTypeDef",
    "UpdateEndpointInputRequestTypeDef",
    "DescribeInferenceRecommendationsJobResponseOutputTypeDef",
    "CreateInferenceRecommendationsJobRequestRequestTypeDef",
    "DescribeEndpointConfigOutputOutputTypeDef",
    "DescribeEndpointOutputOutputTypeDef",
    "CreateEndpointConfigInputRequestTypeDef",
    "DescribeHyperParameterTuningJobResponseOutputTypeDef",
    "HyperParameterTuningJobSearchEntityOutputTypeDef",
    "CreateHyperParameterTuningJobRequestRequestTypeDef",
    "ListInferenceRecommendationsJobStepsResponseOutputTypeDef",
    "ListLabelingJobsResponseOutputTypeDef",
    "BatchDescribeModelPackageOutputOutputTypeDef",
    "DescribeDataQualityJobDefinitionResponseOutputTypeDef",
    "DescribeModelBiasJobDefinitionResponseOutputTypeDef",
    "DescribeModelExplainabilityJobDefinitionResponseOutputTypeDef",
    "DescribeModelQualityJobDefinitionResponseOutputTypeDef",
    "MonitoringJobDefinitionOutputTypeDef",
    "CreateDataQualityJobDefinitionRequestRequestTypeDef",
    "CreateModelBiasJobDefinitionRequestRequestTypeDef",
    "CreateModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "CreateModelQualityJobDefinitionRequestRequestTypeDef",
    "MonitoringJobDefinitionTypeDef",
    "AlgorithmValidationProfileOutputTypeDef",
    "ModelPackageValidationProfileOutputTypeDef",
    "TrialComponentSourceDetailOutputTypeDef",
    "AlgorithmValidationProfileTypeDef",
    "ModelPackageValidationProfileTypeDef",
    "MonitoringScheduleConfigOutputTypeDef",
    "MonitoringScheduleConfigTypeDef",
    "AlgorithmValidationSpecificationOutputTypeDef",
    "ModelPackageValidationSpecificationOutputTypeDef",
    "TrialComponentOutputTypeDef",
    "AlgorithmValidationSpecificationTypeDef",
    "ModelPackageValidationSpecificationTypeDef",
    "DescribeMonitoringScheduleResponseOutputTypeDef",
    "ModelDashboardMonitoringScheduleOutputTypeDef",
    "MonitoringScheduleOutputTypeDef",
    "CreateMonitoringScheduleRequestRequestTypeDef",
    "UpdateMonitoringScheduleRequestRequestTypeDef",
    "DescribeAlgorithmOutputOutputTypeDef",
    "DescribeModelPackageOutputOutputTypeDef",
    "ModelPackageOutputTypeDef",
    "CreateAlgorithmInputRequestTypeDef",
    "CreateModelPackageInputRequestTypeDef",
    "ModelDashboardModelOutputTypeDef",
    "EndpointOutputTypeDef",
    "SearchRecordOutputTypeDef",
    "SearchResponseOutputTypeDef",
)

ActionSourceOutputTypeDef = TypedDict(
    "ActionSourceOutputTypeDef",
    {
        "SourceUri": str,
        "SourceType": str,
        "SourceId": str,
    },
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


AddAssociationResponseOutputTypeDef = TypedDict(
    "AddAssociationResponseOutputTypeDef",
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

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

AgentVersionOutputTypeDef = TypedDict(
    "AgentVersionOutputTypeDef",
    {
        "Version": str,
        "AgentCount": int,
    },
)

AlarmOutputTypeDef = TypedDict(
    "AlarmOutputTypeDef",
    {
        "AlarmName": str,
    },
)

AlarmTypeDef = TypedDict(
    "AlarmTypeDef",
    {
        "AlarmName": str,
    },
    total=False,
)

MetricDefinitionOutputTypeDef = TypedDict(
    "MetricDefinitionOutputTypeDef",
    {
        "Name": str,
        "Regex": str,
    },
)

MetricDefinitionTypeDef = TypedDict(
    "MetricDefinitionTypeDef",
    {
        "Name": str,
        "Regex": str,
    },
)

AlgorithmStatusItemOutputTypeDef = TypedDict(
    "AlgorithmStatusItemOutputTypeDef",
    {
        "Name": str,
        "Status": DetailedAlgorithmStatusType,
        "FailureReason": str,
    },
)

AlgorithmSummaryOutputTypeDef = TypedDict(
    "AlgorithmSummaryOutputTypeDef",
    {
        "AlgorithmName": str,
        "AlgorithmArn": str,
        "AlgorithmDescription": str,
        "CreationTime": datetime,
        "AlgorithmStatus": AlgorithmStatusType,
    },
)

AnnotationConsolidationConfigOutputTypeDef = TypedDict(
    "AnnotationConsolidationConfigOutputTypeDef",
    {
        "AnnotationConsolidationLambdaArn": str,
    },
)

AnnotationConsolidationConfigTypeDef = TypedDict(
    "AnnotationConsolidationConfigTypeDef",
    {
        "AnnotationConsolidationLambdaArn": str,
    },
)

AppDetailsOutputTypeDef = TypedDict(
    "AppDetailsOutputTypeDef",
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

AppSpecificationOutputTypeDef = TypedDict(
    "AppSpecificationOutputTypeDef",
    {
        "ImageUri": str,
        "ContainerEntrypoint": List[str],
        "ContainerArguments": List[str],
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


ArtifactSourceTypeOutputTypeDef = TypedDict(
    "ArtifactSourceTypeOutputTypeDef",
    {
        "SourceIdType": ArtifactSourceIdTypeType,
        "Value": str,
    },
)

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

AssociateTrialComponentResponseOutputTypeDef = TypedDict(
    "AssociateTrialComponentResponseOutputTypeDef",
    {
        "TrialComponentArn": str,
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AsyncInferenceClientConfigOutputTypeDef = TypedDict(
    "AsyncInferenceClientConfigOutputTypeDef",
    {
        "MaxConcurrentInvocationsPerInstance": int,
    },
)

AsyncInferenceClientConfigTypeDef = TypedDict(
    "AsyncInferenceClientConfigTypeDef",
    {
        "MaxConcurrentInvocationsPerInstance": int,
    },
    total=False,
)

AsyncInferenceNotificationConfigOutputTypeDef = TypedDict(
    "AsyncInferenceNotificationConfigOutputTypeDef",
    {
        "SuccessTopic": str,
        "ErrorTopic": str,
        "IncludeInferenceResponseIn": List[AsyncNotificationTopicTypesType],
    },
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

AthenaDatasetDefinitionOutputTypeDef = TypedDict(
    "AthenaDatasetDefinitionOutputTypeDef",
    {
        "Catalog": str,
        "Database": str,
        "QueryString": str,
        "WorkGroup": str,
        "OutputS3Uri": str,
        "KmsKeyId": str,
        "OutputFormat": AthenaResultFormatType,
        "OutputCompression": AthenaResultCompressionTypeType,
    },
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


AutoMLAlgorithmConfigOutputTypeDef = TypedDict(
    "AutoMLAlgorithmConfigOutputTypeDef",
    {
        "AutoMLAlgorithms": List[AutoMLAlgorithmType],
    },
)

AutoMLAlgorithmConfigTypeDef = TypedDict(
    "AutoMLAlgorithmConfigTypeDef",
    {
        "AutoMLAlgorithms": Sequence[AutoMLAlgorithmType],
    },
)

AutoMLCandidateStepOutputTypeDef = TypedDict(
    "AutoMLCandidateStepOutputTypeDef",
    {
        "CandidateStepType": CandidateStepTypeType,
        "CandidateStepArn": str,
        "CandidateStepName": str,
    },
)

AutoMLContainerDefinitionOutputTypeDef = TypedDict(
    "AutoMLContainerDefinitionOutputTypeDef",
    {
        "Image": str,
        "ModelDataUrl": str,
        "Environment": Dict[str, str],
    },
)

FinalAutoMLJobObjectiveMetricOutputTypeDef = TypedDict(
    "FinalAutoMLJobObjectiveMetricOutputTypeDef",
    {
        "Type": AutoMLJobObjectiveTypeType,
        "MetricName": AutoMLMetricEnumType,
        "Value": float,
        "StandardMetricName": AutoMLMetricEnumType,
    },
)

AutoMLS3DataSourceOutputTypeDef = TypedDict(
    "AutoMLS3DataSourceOutputTypeDef",
    {
        "S3DataType": AutoMLS3DataTypeType,
        "S3Uri": str,
    },
)

AutoMLS3DataSourceTypeDef = TypedDict(
    "AutoMLS3DataSourceTypeDef",
    {
        "S3DataType": AutoMLS3DataTypeType,
        "S3Uri": str,
    },
)

AutoMLDataSplitConfigOutputTypeDef = TypedDict(
    "AutoMLDataSplitConfigOutputTypeDef",
    {
        "ValidationFraction": float,
    },
)

AutoMLDataSplitConfigTypeDef = TypedDict(
    "AutoMLDataSplitConfigTypeDef",
    {
        "ValidationFraction": float,
    },
    total=False,
)

AutoMLJobArtifactsOutputTypeDef = TypedDict(
    "AutoMLJobArtifactsOutputTypeDef",
    {
        "CandidateDefinitionNotebookLocation": str,
        "DataExplorationNotebookLocation": str,
    },
)

AutoMLJobCompletionCriteriaOutputTypeDef = TypedDict(
    "AutoMLJobCompletionCriteriaOutputTypeDef",
    {
        "MaxCandidates": int,
        "MaxRuntimePerTrainingJobInSeconds": int,
        "MaxAutoMLJobRuntimeInSeconds": int,
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

AutoMLJobObjectiveOutputTypeDef = TypedDict(
    "AutoMLJobObjectiveOutputTypeDef",
    {
        "MetricName": AutoMLMetricEnumType,
    },
)

AutoMLJobObjectiveTypeDef = TypedDict(
    "AutoMLJobObjectiveTypeDef",
    {
        "MetricName": AutoMLMetricEnumType,
    },
)

AutoMLJobStepMetadataOutputTypeDef = TypedDict(
    "AutoMLJobStepMetadataOutputTypeDef",
    {
        "Arn": str,
    },
)

AutoMLPartialFailureReasonOutputTypeDef = TypedDict(
    "AutoMLPartialFailureReasonOutputTypeDef",
    {
        "PartialFailureMessage": str,
    },
)

AutoMLOutputDataConfigOutputTypeDef = TypedDict(
    "AutoMLOutputDataConfigOutputTypeDef",
    {
        "KmsKeyId": str,
        "S3OutputPath": str,
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


TabularResolvedAttributesOutputTypeDef = TypedDict(
    "TabularResolvedAttributesOutputTypeDef",
    {
        "ProblemType": ProblemTypeType,
    },
)

VpcConfigOutputTypeDef = TypedDict(
    "VpcConfigOutputTypeDef",
    {
        "SecurityGroupIds": List[str],
        "Subnets": List[str],
    },
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "Subnets": Sequence[str],
    },
)

AutoParameterOutputTypeDef = TypedDict(
    "AutoParameterOutputTypeDef",
    {
        "Name": str,
        "ValueHint": str,
    },
)

AutoParameterTypeDef = TypedDict(
    "AutoParameterTypeDef",
    {
        "Name": str,
        "ValueHint": str,
    },
)

AutotuneOutputTypeDef = TypedDict(
    "AutotuneOutputTypeDef",
    {
        "Mode": Literal["Enabled"],
    },
)

AutotuneTypeDef = TypedDict(
    "AutotuneTypeDef",
    {
        "Mode": Literal["Enabled"],
    },
)

BatchDataCaptureConfigOutputTypeDef = TypedDict(
    "BatchDataCaptureConfigOutputTypeDef",
    {
        "DestinationS3Uri": str,
        "KmsKeyId": str,
        "GenerateInferenceId": bool,
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


BatchDescribeModelPackageErrorOutputTypeDef = TypedDict(
    "BatchDescribeModelPackageErrorOutputTypeDef",
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

BestObjectiveNotImprovingOutputTypeDef = TypedDict(
    "BestObjectiveNotImprovingOutputTypeDef",
    {
        "MaxNumberOfTrainingJobsNotImproving": int,
    },
)

BestObjectiveNotImprovingTypeDef = TypedDict(
    "BestObjectiveNotImprovingTypeDef",
    {
        "MaxNumberOfTrainingJobsNotImproving": int,
    },
    total=False,
)

MetricsSourceOutputTypeDef = TypedDict(
    "MetricsSourceOutputTypeDef",
    {
        "ContentType": str,
        "ContentDigest": str,
        "S3Uri": str,
    },
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


CacheHitResultOutputTypeDef = TypedDict(
    "CacheHitResultOutputTypeDef",
    {
        "SourcePipelineExecutionArn": str,
    },
)

OutputParameterOutputTypeDef = TypedDict(
    "OutputParameterOutputTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

CandidateArtifactLocationsOutputTypeDef = TypedDict(
    "CandidateArtifactLocationsOutputTypeDef",
    {
        "Explainability": str,
        "ModelInsights": str,
        "BacktestResults": str,
    },
)

MetricDatumOutputTypeDef = TypedDict(
    "MetricDatumOutputTypeDef",
    {
        "MetricName": AutoMLMetricEnumType,
        "Value": float,
        "Set": MetricSetSourceType,
        "StandardMetricName": AutoMLMetricExtendedEnumType,
    },
)

ModelRegisterSettingsOutputTypeDef = TypedDict(
    "ModelRegisterSettingsOutputTypeDef",
    {
        "Status": FeatureStatusType,
        "CrossAccountModelRegisterRoleArn": str,
    },
)

TimeSeriesForecastingSettingsOutputTypeDef = TypedDict(
    "TimeSeriesForecastingSettingsOutputTypeDef",
    {
        "Status": FeatureStatusType,
        "AmazonForecastRoleArn": str,
    },
)

WorkspaceSettingsOutputTypeDef = TypedDict(
    "WorkspaceSettingsOutputTypeDef",
    {
        "S3ArtifactPath": str,
        "S3KmsKeyId": str,
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

CapacitySizeOutputTypeDef = TypedDict(
    "CapacitySizeOutputTypeDef",
    {
        "Type": CapacitySizeTypeType,
        "Value": int,
    },
)

CapacitySizeTypeDef = TypedDict(
    "CapacitySizeTypeDef",
    {
        "Type": CapacitySizeTypeType,
        "Value": int,
    },
)

CaptureContentTypeHeaderOutputTypeDef = TypedDict(
    "CaptureContentTypeHeaderOutputTypeDef",
    {
        "CsvContentTypes": List[str],
        "JsonContentTypes": List[str],
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

CaptureOptionOutputTypeDef = TypedDict(
    "CaptureOptionOutputTypeDef",
    {
        "CaptureMode": CaptureModeType,
    },
)

CaptureOptionTypeDef = TypedDict(
    "CaptureOptionTypeDef",
    {
        "CaptureMode": CaptureModeType,
    },
)

CategoricalParameterOutputTypeDef = TypedDict(
    "CategoricalParameterOutputTypeDef",
    {
        "Name": str,
        "Value": List[str],
    },
)

CategoricalParameterRangeOutputTypeDef = TypedDict(
    "CategoricalParameterRangeOutputTypeDef",
    {
        "Name": str,
        "Values": List[str],
    },
)

CategoricalParameterRangeSpecificationOutputTypeDef = TypedDict(
    "CategoricalParameterRangeSpecificationOutputTypeDef",
    {
        "Values": List[str],
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

ShuffleConfigOutputTypeDef = TypedDict(
    "ShuffleConfigOutputTypeDef",
    {
        "Seed": int,
    },
)

ChannelSpecificationOutputTypeDef = TypedDict(
    "ChannelSpecificationOutputTypeDef",
    {
        "Name": str,
        "Description": str,
        "IsRequired": bool,
        "SupportedContentTypes": List[str],
        "SupportedCompressionTypes": List[CompressionTypeType],
        "SupportedInputModes": List[TrainingInputModeType],
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

CheckpointConfigOutputTypeDef = TypedDict(
    "CheckpointConfigOutputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
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


ClarifyCheckStepMetadataOutputTypeDef = TypedDict(
    "ClarifyCheckStepMetadataOutputTypeDef",
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

ClarifyInferenceConfigOutputTypeDef = TypedDict(
    "ClarifyInferenceConfigOutputTypeDef",
    {
        "FeaturesAttribute": str,
        "ContentTemplate": str,
        "MaxRecordCount": int,
        "MaxPayloadInMB": int,
        "ProbabilityIndex": int,
        "LabelIndex": int,
        "ProbabilityAttribute": str,
        "LabelAttribute": str,
        "LabelHeaders": List[str],
        "FeatureHeaders": List[str],
        "FeatureTypes": List[ClarifyFeatureTypeType],
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

ClarifyShapBaselineConfigOutputTypeDef = TypedDict(
    "ClarifyShapBaselineConfigOutputTypeDef",
    {
        "MimeType": str,
        "ShapBaseline": str,
        "ShapBaselineUri": str,
    },
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

ClarifyTextConfigOutputTypeDef = TypedDict(
    "ClarifyTextConfigOutputTypeDef",
    {
        "Language": ClarifyTextLanguageType,
        "Granularity": ClarifyTextGranularityType,
    },
)

ClarifyTextConfigTypeDef = TypedDict(
    "ClarifyTextConfigTypeDef",
    {
        "Language": ClarifyTextLanguageType,
        "Granularity": ClarifyTextGranularityType,
    },
)

CodeRepositoryOutputTypeDef = TypedDict(
    "CodeRepositoryOutputTypeDef",
    {
        "RepositoryUrl": str,
    },
)

GitConfigOutputTypeDef = TypedDict(
    "GitConfigOutputTypeDef",
    {
        "RepositoryUrl": str,
        "Branch": str,
        "SecretArn": str,
    },
)

CodeRepositoryTypeDef = TypedDict(
    "CodeRepositoryTypeDef",
    {
        "RepositoryUrl": str,
    },
)

CognitoConfigOutputTypeDef = TypedDict(
    "CognitoConfigOutputTypeDef",
    {
        "UserPool": str,
        "ClientId": str,
    },
)

CognitoConfigTypeDef = TypedDict(
    "CognitoConfigTypeDef",
    {
        "UserPool": str,
        "ClientId": str,
    },
)

CognitoMemberDefinitionOutputTypeDef = TypedDict(
    "CognitoMemberDefinitionOutputTypeDef",
    {
        "UserPool": str,
        "UserGroup": str,
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

CollectionConfigurationOutputTypeDef = TypedDict(
    "CollectionConfigurationOutputTypeDef",
    {
        "CollectionName": str,
        "CollectionParameters": Dict[str, str],
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

CompilationJobSummaryOutputTypeDef = TypedDict(
    "CompilationJobSummaryOutputTypeDef",
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

ConditionStepMetadataOutputTypeDef = TypedDict(
    "ConditionStepMetadataOutputTypeDef",
    {
        "Outcome": ConditionOutcomeType,
    },
)

MultiModelConfigOutputTypeDef = TypedDict(
    "MultiModelConfigOutputTypeDef",
    {
        "ModelCacheSetting": ModelCacheSettingType,
    },
)

MultiModelConfigTypeDef = TypedDict(
    "MultiModelConfigTypeDef",
    {
        "ModelCacheSetting": ModelCacheSettingType,
    },
    total=False,
)

ContextSourceOutputTypeDef = TypedDict(
    "ContextSourceOutputTypeDef",
    {
        "SourceUri": str,
        "SourceType": str,
        "SourceId": str,
    },
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


ContinuousParameterRangeOutputTypeDef = TypedDict(
    "ContinuousParameterRangeOutputTypeDef",
    {
        "Name": str,
        "MinValue": str,
        "MaxValue": str,
        "ScalingType": HyperParameterScalingTypeType,
    },
)

ContinuousParameterRangeSpecificationOutputTypeDef = TypedDict(
    "ContinuousParameterRangeSpecificationOutputTypeDef",
    {
        "MinValue": str,
        "MaxValue": str,
    },
)

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


ConvergenceDetectedOutputTypeDef = TypedDict(
    "ConvergenceDetectedOutputTypeDef",
    {
        "CompleteOnConvergence": CompleteOnConvergenceType,
    },
)

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

CreateActionResponseOutputTypeDef = TypedDict(
    "CreateActionResponseOutputTypeDef",
    {
        "ActionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAlgorithmOutputOutputTypeDef = TypedDict(
    "CreateAlgorithmOutputOutputTypeDef",
    {
        "AlgorithmArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAppImageConfigResponseOutputTypeDef = TypedDict(
    "CreateAppImageConfigResponseOutputTypeDef",
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

CreateAppResponseOutputTypeDef = TypedDict(
    "CreateAppResponseOutputTypeDef",
    {
        "AppArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateArtifactResponseOutputTypeDef = TypedDict(
    "CreateArtifactResponseOutputTypeDef",
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

CreateAutoMLJobResponseOutputTypeDef = TypedDict(
    "CreateAutoMLJobResponseOutputTypeDef",
    {
        "AutoMLJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAutoMLJobV2ResponseOutputTypeDef = TypedDict(
    "CreateAutoMLJobV2ResponseOutputTypeDef",
    {
        "AutoMLJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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


CreateCodeRepositoryOutputOutputTypeDef = TypedDict(
    "CreateCodeRepositoryOutputOutputTypeDef",
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

CreateCompilationJobResponseOutputTypeDef = TypedDict(
    "CreateCompilationJobResponseOutputTypeDef",
    {
        "CompilationJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateContextResponseOutputTypeDef = TypedDict(
    "CreateContextResponseOutputTypeDef",
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

CreateDataQualityJobDefinitionResponseOutputTypeDef = TypedDict(
    "CreateDataQualityJobDefinitionResponseOutputTypeDef",
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


CreateDomainResponseOutputTypeDef = TypedDict(
    "CreateDomainResponseOutputTypeDef",
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

CreateEdgeDeploymentPlanResponseOutputTypeDef = TypedDict(
    "CreateEdgeDeploymentPlanResponseOutputTypeDef",
    {
        "EdgeDeploymentPlanArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEndpointConfigOutputOutputTypeDef = TypedDict(
    "CreateEndpointConfigOutputOutputTypeDef",
    {
        "EndpointConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEndpointOutputOutputTypeDef = TypedDict(
    "CreateEndpointOutputOutputTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateExperimentResponseOutputTypeDef = TypedDict(
    "CreateExperimentResponseOutputTypeDef",
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

CreateFeatureGroupResponseOutputTypeDef = TypedDict(
    "CreateFeatureGroupResponseOutputTypeDef",
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

CreateFlowDefinitionResponseOutputTypeDef = TypedDict(
    "CreateFlowDefinitionResponseOutputTypeDef",
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

CreateHubResponseOutputTypeDef = TypedDict(
    "CreateHubResponseOutputTypeDef",
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

CreateHumanTaskUiResponseOutputTypeDef = TypedDict(
    "CreateHumanTaskUiResponseOutputTypeDef",
    {
        "HumanTaskUiArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateHyperParameterTuningJobResponseOutputTypeDef = TypedDict(
    "CreateHyperParameterTuningJobResponseOutputTypeDef",
    {
        "HyperParameterTuningJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateImageResponseOutputTypeDef = TypedDict(
    "CreateImageResponseOutputTypeDef",
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


CreateImageVersionResponseOutputTypeDef = TypedDict(
    "CreateImageVersionResponseOutputTypeDef",
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

CreateInferenceExperimentResponseOutputTypeDef = TypedDict(
    "CreateInferenceExperimentResponseOutputTypeDef",
    {
        "InferenceExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateInferenceRecommendationsJobResponseOutputTypeDef = TypedDict(
    "CreateInferenceRecommendationsJobResponseOutputTypeDef",
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

CreateLabelingJobResponseOutputTypeDef = TypedDict(
    "CreateLabelingJobResponseOutputTypeDef",
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


CreateModelBiasJobDefinitionResponseOutputTypeDef = TypedDict(
    "CreateModelBiasJobDefinitionResponseOutputTypeDef",
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

CreateModelCardExportJobResponseOutputTypeDef = TypedDict(
    "CreateModelCardExportJobResponseOutputTypeDef",
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

CreateModelCardResponseOutputTypeDef = TypedDict(
    "CreateModelCardResponseOutputTypeDef",
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


CreateModelExplainabilityJobDefinitionResponseOutputTypeDef = TypedDict(
    "CreateModelExplainabilityJobDefinitionResponseOutputTypeDef",
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

CreateModelOutputOutputTypeDef = TypedDict(
    "CreateModelOutputOutputTypeDef",
    {
        "ModelArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateModelPackageGroupOutputOutputTypeDef = TypedDict(
    "CreateModelPackageGroupOutputOutputTypeDef",
    {
        "ModelPackageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateModelPackageOutputOutputTypeDef = TypedDict(
    "CreateModelPackageOutputOutputTypeDef",
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


CreateModelQualityJobDefinitionResponseOutputTypeDef = TypedDict(
    "CreateModelQualityJobDefinitionResponseOutputTypeDef",
    {
        "JobDefinitionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMonitoringScheduleResponseOutputTypeDef = TypedDict(
    "CreateMonitoringScheduleResponseOutputTypeDef",
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

CreateNotebookInstanceLifecycleConfigOutputOutputTypeDef = TypedDict(
    "CreateNotebookInstanceLifecycleConfigOutputOutputTypeDef",
    {
        "NotebookInstanceLifecycleConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateNotebookInstanceOutputOutputTypeDef = TypedDict(
    "CreateNotebookInstanceOutputOutputTypeDef",
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


CreatePipelineResponseOutputTypeDef = TypedDict(
    "CreatePipelineResponseOutputTypeDef",
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


CreatePresignedDomainUrlResponseOutputTypeDef = TypedDict(
    "CreatePresignedDomainUrlResponseOutputTypeDef",
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


CreatePresignedNotebookInstanceUrlOutputOutputTypeDef = TypedDict(
    "CreatePresignedNotebookInstanceUrlOutputOutputTypeDef",
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

CreateProcessingJobResponseOutputTypeDef = TypedDict(
    "CreateProcessingJobResponseOutputTypeDef",
    {
        "ProcessingJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateProjectOutputOutputTypeDef = TypedDict(
    "CreateProjectOutputOutputTypeDef",
    {
        "ProjectArn": str,
        "ProjectId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateSpaceResponseOutputTypeDef = TypedDict(
    "CreateSpaceResponseOutputTypeDef",
    {
        "SpaceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateStudioLifecycleConfigResponseOutputTypeDef = TypedDict(
    "CreateStudioLifecycleConfigResponseOutputTypeDef",
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


CreateTrainingJobResponseOutputTypeDef = TypedDict(
    "CreateTrainingJobResponseOutputTypeDef",
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


CreateTransformJobResponseOutputTypeDef = TypedDict(
    "CreateTransformJobResponseOutputTypeDef",
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

CreateTrialComponentResponseOutputTypeDef = TypedDict(
    "CreateTrialComponentResponseOutputTypeDef",
    {
        "TrialComponentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateTrialResponseOutputTypeDef = TypedDict(
    "CreateTrialResponseOutputTypeDef",
    {
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateUserProfileResponseOutputTypeDef = TypedDict(
    "CreateUserProfileResponseOutputTypeDef",
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

CreateWorkforceResponseOutputTypeDef = TypedDict(
    "CreateWorkforceResponseOutputTypeDef",
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

CreateWorkteamResponseOutputTypeDef = TypedDict(
    "CreateWorkteamResponseOutputTypeDef",
    {
        "WorkteamArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CustomImageOutputTypeDef = TypedDict(
    "CustomImageOutputTypeDef",
    {
        "ImageName": str,
        "ImageVersionNumber": int,
        "AppImageConfigName": str,
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


DataCaptureConfigSummaryOutputTypeDef = TypedDict(
    "DataCaptureConfigSummaryOutputTypeDef",
    {
        "EnableCapture": bool,
        "CaptureStatus": CaptureStatusType,
        "CurrentSamplingPercentage": int,
        "DestinationS3Uri": str,
        "KmsKeyId": str,
    },
)

DataCatalogConfigOutputTypeDef = TypedDict(
    "DataCatalogConfigOutputTypeDef",
    {
        "TableName": str,
        "Catalog": str,
        "Database": str,
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

DataProcessingOutputTypeDef = TypedDict(
    "DataProcessingOutputTypeDef",
    {
        "InputFilter": str,
        "OutputFilter": str,
        "JoinSource": JoinSourceType,
    },
)

DataQualityAppSpecificationOutputTypeDef = TypedDict(
    "DataQualityAppSpecificationOutputTypeDef",
    {
        "ImageUri": str,
        "ContainerEntrypoint": List[str],
        "ContainerArguments": List[str],
        "RecordPreprocessorSourceUri": str,
        "PostAnalyticsProcessorSourceUri": str,
        "Environment": Dict[str, str],
    },
)

MonitoringConstraintsResourceOutputTypeDef = TypedDict(
    "MonitoringConstraintsResourceOutputTypeDef",
    {
        "S3Uri": str,
    },
)

MonitoringStatisticsResourceOutputTypeDef = TypedDict(
    "MonitoringStatisticsResourceOutputTypeDef",
    {
        "S3Uri": str,
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

EndpointInputOutputTypeDef = TypedDict(
    "EndpointInputOutputTypeDef",
    {
        "EndpointName": str,
        "LocalPath": str,
        "S3InputMode": ProcessingS3InputModeType,
        "S3DataDistributionType": ProcessingS3DataDistributionTypeType,
        "FeaturesAttribute": str,
        "InferenceAttribute": str,
        "ProbabilityAttribute": str,
        "ProbabilityThresholdAttribute": float,
        "StartTimeOffset": str,
        "EndTimeOffset": str,
    },
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


FileSystemDataSourceOutputTypeDef = TypedDict(
    "FileSystemDataSourceOutputTypeDef",
    {
        "FileSystemId": str,
        "FileSystemAccessMode": FileSystemAccessModeType,
        "FileSystemType": FileSystemTypeType,
        "DirectoryPath": str,
    },
)

S3DataSourceOutputTypeDef = TypedDict(
    "S3DataSourceOutputTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
        "S3DataDistributionType": S3DataDistributionType,
        "AttributeNames": List[str],
        "InstanceGroupNames": List[str],
    },
)

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


RedshiftDatasetDefinitionOutputTypeDef = TypedDict(
    "RedshiftDatasetDefinitionOutputTypeDef",
    {
        "ClusterId": str,
        "Database": str,
        "DbUser": str,
        "QueryString": str,
        "ClusterRoleArn": str,
        "OutputS3Uri": str,
        "KmsKeyId": str,
        "OutputFormat": RedshiftResultFormatType,
        "OutputCompression": RedshiftResultCompressionTypeType,
    },
)

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


DebugRuleConfigurationOutputTypeDef = TypedDict(
    "DebugRuleConfigurationOutputTypeDef",
    {
        "RuleConfigurationName": str,
        "LocalPath": str,
        "S3OutputPath": str,
        "RuleEvaluatorImage": str,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
        "RuleParameters": Dict[str, str],
    },
)

DebugRuleEvaluationStatusOutputTypeDef = TypedDict(
    "DebugRuleEvaluationStatusOutputTypeDef",
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

DeleteActionResponseOutputTypeDef = TypedDict(
    "DeleteActionResponseOutputTypeDef",
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


DeleteArtifactResponseOutputTypeDef = TypedDict(
    "DeleteArtifactResponseOutputTypeDef",
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

DeleteAssociationResponseOutputTypeDef = TypedDict(
    "DeleteAssociationResponseOutputTypeDef",
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

DeleteContextResponseOutputTypeDef = TypedDict(
    "DeleteContextResponseOutputTypeDef",
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

DeleteExperimentResponseOutputTypeDef = TypedDict(
    "DeleteExperimentResponseOutputTypeDef",
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

DeleteInferenceExperimentResponseOutputTypeDef = TypedDict(
    "DeleteInferenceExperimentResponseOutputTypeDef",
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

DeletePipelineResponseOutputTypeDef = TypedDict(
    "DeletePipelineResponseOutputTypeDef",
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

DeleteTrialComponentResponseOutputTypeDef = TypedDict(
    "DeleteTrialComponentResponseOutputTypeDef",
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

DeleteTrialResponseOutputTypeDef = TypedDict(
    "DeleteTrialResponseOutputTypeDef",
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

DeleteWorkteamResponseOutputTypeDef = TypedDict(
    "DeleteWorkteamResponseOutputTypeDef",
    {
        "Success": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeployedImageOutputTypeDef = TypedDict(
    "DeployedImageOutputTypeDef",
    {
        "SpecifiedImage": str,
        "ResolvedImage": str,
        "ResolutionTime": datetime,
    },
)

RealTimeInferenceRecommendationOutputTypeDef = TypedDict(
    "RealTimeInferenceRecommendationOutputTypeDef",
    {
        "RecommendationId": str,
        "InstanceType": ProductionVariantInstanceTypeType,
        "Environment": Dict[str, str],
    },
)

DeviceSelectionConfigOutputTypeDef = TypedDict(
    "DeviceSelectionConfigOutputTypeDef",
    {
        "DeviceSubsetType": DeviceSubsetTypeType,
        "Percentage": int,
        "DeviceNames": List[str],
        "DeviceNameContains": str,
    },
)

EdgeDeploymentConfigOutputTypeDef = TypedDict(
    "EdgeDeploymentConfigOutputTypeDef",
    {
        "FailureHandlingPolicy": FailureHandlingPolicyType,
    },
)

EdgeDeploymentStatusOutputTypeDef = TypedDict(
    "EdgeDeploymentStatusOutputTypeDef",
    {
        "StageStatus": StageStatusType,
        "EdgeDeploymentSuccessInStage": int,
        "EdgeDeploymentPendingInStage": int,
        "EdgeDeploymentFailedInStage": int,
        "EdgeDeploymentStatusMessage": str,
        "EdgeDeploymentStageStartTime": datetime,
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

MetadataPropertiesOutputTypeDef = TypedDict(
    "MetadataPropertiesOutputTypeDef",
    {
        "CommitId": str,
        "Repository": str,
        "GeneratedBy": str,
        "ProjectId": str,
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


ResourceSpecOutputTypeDef = TypedDict(
    "ResourceSpecOutputTypeDef",
    {
        "SageMakerImageArn": str,
        "SageMakerImageVersionArn": str,
        "InstanceType": AppInstanceTypeType,
        "LifecycleConfigArn": str,
    },
)

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

ModelDeployConfigOutputTypeDef = TypedDict(
    "ModelDeployConfigOutputTypeDef",
    {
        "AutoGenerateEndpointName": bool,
        "EndpointName": str,
    },
)

ModelDeployResultOutputTypeDef = TypedDict(
    "ModelDeployResultOutputTypeDef",
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

InputConfigOutputTypeDef = TypedDict(
    "InputConfigOutputTypeDef",
    {
        "S3Uri": str,
        "DataInputConfig": str,
        "Framework": FrameworkType,
        "FrameworkVersion": str,
    },
)

ModelArtifactsOutputTypeDef = TypedDict(
    "ModelArtifactsOutputTypeDef",
    {
        "S3ModelArtifacts": str,
    },
)

ModelDigestsOutputTypeDef = TypedDict(
    "ModelDigestsOutputTypeDef",
    {
        "ArtifactDigest": str,
    },
)

NeoVpcConfigOutputTypeDef = TypedDict(
    "NeoVpcConfigOutputTypeDef",
    {
        "SecurityGroupIds": List[str],
        "Subnets": List[str],
    },
)

StoppingConditionOutputTypeDef = TypedDict(
    "StoppingConditionOutputTypeDef",
    {
        "MaxRuntimeInSeconds": int,
        "MaxWaitTimeInSeconds": int,
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

MonitoringStoppingConditionOutputTypeDef = TypedDict(
    "MonitoringStoppingConditionOutputTypeDef",
    {
        "MaxRuntimeInSeconds": int,
    },
)

DescribeDeviceFleetRequestRequestTypeDef = TypedDict(
    "DescribeDeviceFleetRequestRequestTypeDef",
    {
        "DeviceFleetName": str,
    },
)

EdgeOutputConfigOutputTypeDef = TypedDict(
    "EdgeOutputConfigOutputTypeDef",
    {
        "S3OutputLocation": str,
        "KmsKeyId": str,
        "PresetDeploymentType": Literal["GreengrassV2Component"],
        "PresetDeploymentConfig": str,
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


EdgeModelOutputTypeDef = TypedDict(
    "EdgeModelOutputTypeDef",
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


EdgeDeploymentModelConfigOutputTypeDef = TypedDict(
    "EdgeDeploymentModelConfigOutputTypeDef",
    {
        "ModelHandle": str,
        "EdgePackagingJobName": str,
    },
)

DescribeEdgePackagingJobRequestRequestTypeDef = TypedDict(
    "DescribeEdgePackagingJobRequestRequestTypeDef",
    {
        "EdgePackagingJobName": str,
    },
)

EdgePresetDeploymentOutputOutputTypeDef = TypedDict(
    "EdgePresetDeploymentOutputOutputTypeDef",
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

ExperimentSourceOutputTypeDef = TypedDict(
    "ExperimentSourceOutputTypeDef",
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


FeatureDefinitionOutputTypeDef = TypedDict(
    "FeatureDefinitionOutputTypeDef",
    {
        "FeatureName": str,
        "FeatureType": FeatureTypeType,
    },
)

LastUpdateStatusOutputTypeDef = TypedDict(
    "LastUpdateStatusOutputTypeDef",
    {
        "Status": LastUpdateStatusValueType,
        "FailureReason": str,
    },
)

OfflineStoreStatusOutputTypeDef = TypedDict(
    "OfflineStoreStatusOutputTypeDef",
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

FeatureParameterOutputTypeDef = TypedDict(
    "FeatureParameterOutputTypeDef",
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

FlowDefinitionOutputConfigOutputTypeDef = TypedDict(
    "FlowDefinitionOutputConfigOutputTypeDef",
    {
        "S3OutputPath": str,
        "KmsKeyId": str,
    },
)

HumanLoopRequestSourceOutputTypeDef = TypedDict(
    "HumanLoopRequestSourceOutputTypeDef",
    {
        "AwsManagedHumanLoopRequestSource": AwsManagedHumanLoopRequestSourceType,
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


HubContentDependencyOutputTypeDef = TypedDict(
    "HubContentDependencyOutputTypeDef",
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

HubS3StorageConfigOutputTypeDef = TypedDict(
    "HubS3StorageConfigOutputTypeDef",
    {
        "S3OutputPath": str,
    },
)

DescribeHumanTaskUiRequestRequestTypeDef = TypedDict(
    "DescribeHumanTaskUiRequestRequestTypeDef",
    {
        "HumanTaskUiName": str,
    },
)

UiTemplateInfoOutputTypeDef = TypedDict(
    "UiTemplateInfoOutputTypeDef",
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

HyperParameterTuningJobCompletionDetailsOutputTypeDef = TypedDict(
    "HyperParameterTuningJobCompletionDetailsOutputTypeDef",
    {
        "NumberOfTrainingJobsObjectiveNotImproving": int,
        "ConvergenceDetectedTime": datetime,
    },
)

HyperParameterTuningJobConsumedResourcesOutputTypeDef = TypedDict(
    "HyperParameterTuningJobConsumedResourcesOutputTypeDef",
    {
        "RuntimeInSeconds": int,
    },
)

ObjectiveStatusCountersOutputTypeDef = TypedDict(
    "ObjectiveStatusCountersOutputTypeDef",
    {
        "Succeeded": int,
        "Pending": int,
        "Failed": int,
    },
)

TrainingJobStatusCountersOutputTypeDef = TypedDict(
    "TrainingJobStatusCountersOutputTypeDef",
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

DescribeImageResponseOutputTypeDef = TypedDict(
    "DescribeImageResponseOutputTypeDef",
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


DescribeImageVersionResponseOutputTypeDef = TypedDict(
    "DescribeImageVersionResponseOutputTypeDef",
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

EndpointMetadataOutputTypeDef = TypedDict(
    "EndpointMetadataOutputTypeDef",
    {
        "EndpointName": str,
        "EndpointConfigName": str,
        "EndpointStatus": EndpointStatusType,
        "FailureReason": str,
    },
)

InferenceExperimentScheduleOutputTypeDef = TypedDict(
    "InferenceExperimentScheduleOutputTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
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

LabelCountersOutputTypeDef = TypedDict(
    "LabelCountersOutputTypeDef",
    {
        "TotalLabeled": int,
        "HumanLabeled": int,
        "MachineLabeled": int,
        "FailedNonRetryableError": int,
        "Unlabeled": int,
    },
)

LabelingJobOutputConfigOutputTypeDef = TypedDict(
    "LabelingJobOutputConfigOutputTypeDef",
    {
        "S3OutputPath": str,
        "KmsKeyId": str,
        "SnsTopicArn": str,
    },
)

LabelingJobOutputOutputTypeDef = TypedDict(
    "LabelingJobOutputOutputTypeDef",
    {
        "OutputDatasetS3Uri": str,
        "FinalActiveLearningModelArn": str,
    },
)

LabelingJobStoppingConditionsOutputTypeDef = TypedDict(
    "LabelingJobStoppingConditionsOutputTypeDef",
    {
        "MaxHumanLabeledObjectCount": int,
        "MaxPercentageOfInputDatasetLabeled": int,
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

ModelBiasAppSpecificationOutputTypeDef = TypedDict(
    "ModelBiasAppSpecificationOutputTypeDef",
    {
        "ImageUri": str,
        "ConfigUri": str,
        "Environment": Dict[str, str],
    },
)

DescribeModelCardExportJobRequestRequestTypeDef = TypedDict(
    "DescribeModelCardExportJobRequestRequestTypeDef",
    {
        "ModelCardExportJobArn": str,
    },
)

ModelCardExportArtifactsOutputTypeDef = TypedDict(
    "ModelCardExportArtifactsOutputTypeDef",
    {
        "S3ExportArtifacts": str,
    },
)

ModelCardExportOutputConfigOutputTypeDef = TypedDict(
    "ModelCardExportOutputConfigOutputTypeDef",
    {
        "S3OutputPath": str,
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


ModelCardSecurityConfigOutputTypeDef = TypedDict(
    "ModelCardSecurityConfigOutputTypeDef",
    {
        "KmsKeyId": str,
    },
)

DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef",
    {
        "JobDefinitionName": str,
    },
)

ModelExplainabilityAppSpecificationOutputTypeDef = TypedDict(
    "ModelExplainabilityAppSpecificationOutputTypeDef",
    {
        "ImageUri": str,
        "ConfigUri": str,
        "Environment": Dict[str, str],
    },
)

DescribeModelInputRequestTypeDef = TypedDict(
    "DescribeModelInputRequestTypeDef",
    {
        "ModelName": str,
    },
)

InferenceExecutionConfigOutputTypeDef = TypedDict(
    "InferenceExecutionConfigOutputTypeDef",
    {
        "Mode": InferenceExecutionModeType,
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

ModelQualityAppSpecificationOutputTypeDef = TypedDict(
    "ModelQualityAppSpecificationOutputTypeDef",
    {
        "ImageUri": str,
        "ContainerEntrypoint": List[str],
        "ContainerArguments": List[str],
        "RecordPreprocessorSourceUri": str,
        "PostAnalyticsProcessorSourceUri": str,
        "ProblemType": MonitoringProblemTypeType,
        "Environment": Dict[str, str],
    },
)

DescribeMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "DescribeMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
    },
)

MonitoringExecutionSummaryOutputTypeDef = TypedDict(
    "MonitoringExecutionSummaryOutputTypeDef",
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

NotebookInstanceLifecycleHookOutputTypeDef = TypedDict(
    "NotebookInstanceLifecycleHookOutputTypeDef",
    {
        "Content": str,
    },
)

InstanceMetadataServiceConfigurationOutputTypeDef = TypedDict(
    "InstanceMetadataServiceConfigurationOutputTypeDef",
    {
        "MinimumInstanceMetadataServiceVersion": str,
    },
)

DescribePipelineDefinitionForExecutionRequestRequestTypeDef = TypedDict(
    "DescribePipelineDefinitionForExecutionRequestRequestTypeDef",
    {
        "PipelineExecutionArn": str,
    },
)

DescribePipelineDefinitionForExecutionResponseOutputTypeDef = TypedDict(
    "DescribePipelineDefinitionForExecutionResponseOutputTypeDef",
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

ParallelismConfigurationOutputTypeDef = TypedDict(
    "ParallelismConfigurationOutputTypeDef",
    {
        "MaxParallelExecutionSteps": int,
    },
)

PipelineExperimentConfigOutputTypeDef = TypedDict(
    "PipelineExperimentConfigOutputTypeDef",
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

ExperimentConfigOutputTypeDef = TypedDict(
    "ExperimentConfigOutputTypeDef",
    {
        "ExperimentName": str,
        "TrialName": str,
        "TrialComponentDisplayName": str,
        "RunName": str,
    },
)

ProcessingStoppingConditionOutputTypeDef = TypedDict(
    "ProcessingStoppingConditionOutputTypeDef",
    {
        "MaxRuntimeInSeconds": int,
    },
)

DescribeProjectInputRequestTypeDef = TypedDict(
    "DescribeProjectInputRequestTypeDef",
    {
        "ProjectName": str,
    },
)

ServiceCatalogProvisionedProductDetailsOutputTypeDef = TypedDict(
    "ServiceCatalogProvisionedProductDetailsOutputTypeDef",
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

DescribeStudioLifecycleConfigResponseOutputTypeDef = TypedDict(
    "DescribeStudioLifecycleConfigResponseOutputTypeDef",
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

SubscribedWorkteamOutputTypeDef = TypedDict(
    "SubscribedWorkteamOutputTypeDef",
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

MetricDataOutputTypeDef = TypedDict(
    "MetricDataOutputTypeDef",
    {
        "MetricName": str,
        "Value": float,
        "Timestamp": datetime,
    },
)

OutputDataConfigOutputTypeDef = TypedDict(
    "OutputDataConfigOutputTypeDef",
    {
        "KmsKeyId": str,
        "S3OutputPath": str,
        "CompressionType": OutputCompressionTypeType,
    },
)

ProfilerConfigOutputTypeDef = TypedDict(
    "ProfilerConfigOutputTypeDef",
    {
        "S3OutputPath": str,
        "ProfilingIntervalInMilliseconds": int,
        "ProfilingParameters": Dict[str, str],
        "DisableProfiler": bool,
    },
)

ProfilerRuleConfigurationOutputTypeDef = TypedDict(
    "ProfilerRuleConfigurationOutputTypeDef",
    {
        "RuleConfigurationName": str,
        "LocalPath": str,
        "S3OutputPath": str,
        "RuleEvaluatorImage": str,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
        "RuleParameters": Dict[str, str],
    },
)

ProfilerRuleEvaluationStatusOutputTypeDef = TypedDict(
    "ProfilerRuleEvaluationStatusOutputTypeDef",
    {
        "RuleConfigurationName": str,
        "RuleEvaluationJobArn": str,
        "RuleEvaluationStatus": RuleEvaluationStatusType,
        "StatusDetails": str,
        "LastModifiedTime": datetime,
    },
)

RetryStrategyOutputTypeDef = TypedDict(
    "RetryStrategyOutputTypeDef",
    {
        "MaximumRetryAttempts": int,
    },
)

SecondaryStatusTransitionOutputTypeDef = TypedDict(
    "SecondaryStatusTransitionOutputTypeDef",
    {
        "Status": SecondaryStatusType,
        "StartTime": datetime,
        "EndTime": datetime,
        "StatusMessage": str,
    },
)

TensorBoardOutputConfigOutputTypeDef = TypedDict(
    "TensorBoardOutputConfigOutputTypeDef",
    {
        "LocalPath": str,
        "S3OutputPath": str,
    },
)

WarmPoolStatusOutputTypeDef = TypedDict(
    "WarmPoolStatusOutputTypeDef",
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

ModelClientConfigOutputTypeDef = TypedDict(
    "ModelClientConfigOutputTypeDef",
    {
        "InvocationsTimeoutInSeconds": int,
        "InvocationsMaxRetries": int,
    },
)

TransformOutputOutputTypeDef = TypedDict(
    "TransformOutputOutputTypeDef",
    {
        "S3OutputPath": str,
        "Accept": str,
        "AssembleWith": AssemblyTypeType,
        "KmsKeyId": str,
    },
)

TransformResourcesOutputTypeDef = TypedDict(
    "TransformResourcesOutputTypeDef",
    {
        "InstanceType": TransformInstanceTypeType,
        "InstanceCount": int,
        "VolumeKmsKeyId": str,
    },
)

DescribeTrialComponentRequestRequestTypeDef = TypedDict(
    "DescribeTrialComponentRequestRequestTypeDef",
    {
        "TrialComponentName": str,
    },
)

TrialComponentArtifactOutputTypeDef = TypedDict(
    "TrialComponentArtifactOutputTypeDef",
    {
        "MediaType": str,
        "Value": str,
    },
)

TrialComponentMetricSummaryOutputTypeDef = TypedDict(
    "TrialComponentMetricSummaryOutputTypeDef",
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

TrialComponentParameterValueOutputTypeDef = TypedDict(
    "TrialComponentParameterValueOutputTypeDef",
    {
        "StringValue": str,
        "NumberValue": float,
    },
)

TrialComponentSourceOutputTypeDef = TypedDict(
    "TrialComponentSourceOutputTypeDef",
    {
        "SourceArn": str,
        "SourceType": str,
    },
)

TrialComponentStatusOutputTypeDef = TypedDict(
    "TrialComponentStatusOutputTypeDef",
    {
        "PrimaryStatus": TrialComponentPrimaryStatusType,
        "Message": str,
    },
)

DescribeTrialRequestRequestTypeDef = TypedDict(
    "DescribeTrialRequestRequestTypeDef",
    {
        "TrialName": str,
    },
)

TrialSourceOutputTypeDef = TypedDict(
    "TrialSourceOutputTypeDef",
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

DeviceDeploymentSummaryOutputTypeDef = TypedDict(
    "DeviceDeploymentSummaryOutputTypeDef",
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

DeviceFleetSummaryOutputTypeDef = TypedDict(
    "DeviceFleetSummaryOutputTypeDef",
    {
        "DeviceFleetArn": str,
        "DeviceFleetName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

DeviceStatsOutputTypeDef = TypedDict(
    "DeviceStatsOutputTypeDef",
    {
        "ConnectedDeviceCount": int,
        "RegisteredDeviceCount": int,
    },
)

EdgeModelSummaryOutputTypeDef = TypedDict(
    "EdgeModelSummaryOutputTypeDef",
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

DisassociateTrialComponentResponseOutputTypeDef = TypedDict(
    "DisassociateTrialComponentResponseOutputTypeDef",
    {
        "TrialComponentArn": str,
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DomainDetailsOutputTypeDef = TypedDict(
    "DomainDetailsOutputTypeDef",
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

FileSourceOutputTypeDef = TypedDict(
    "FileSourceOutputTypeDef",
    {
        "ContentType": str,
        "ContentDigest": str,
        "S3Uri": str,
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


EMRStepMetadataOutputTypeDef = TypedDict(
    "EMRStepMetadataOutputTypeDef",
    {
        "ClusterId": str,
        "StepId": str,
        "StepName": str,
        "LogFilePath": str,
    },
)

EdgeDeploymentPlanSummaryOutputTypeDef = TypedDict(
    "EdgeDeploymentPlanSummaryOutputTypeDef",
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

EdgeModelStatOutputTypeDef = TypedDict(
    "EdgeModelStatOutputTypeDef",
    {
        "ModelName": str,
        "ModelVersion": str,
        "OfflineDeviceCount": int,
        "ConnectedDeviceCount": int,
        "ActiveDeviceCount": int,
        "SamplingDeviceCount": int,
    },
)

EdgeOutputTypeDef = TypedDict(
    "EdgeOutputTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "AssociationType": AssociationEdgeTypeType,
    },
)

EdgePackagingJobSummaryOutputTypeDef = TypedDict(
    "EdgePackagingJobSummaryOutputTypeDef",
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

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EndpointConfigSummaryOutputTypeDef = TypedDict(
    "EndpointConfigSummaryOutputTypeDef",
    {
        "EndpointConfigName": str,
        "EndpointConfigArn": str,
        "CreationTime": datetime,
    },
)

EndpointInfoOutputTypeDef = TypedDict(
    "EndpointInfoOutputTypeDef",
    {
        "EndpointName": str,
    },
)

EndpointInfoTypeDef = TypedDict(
    "EndpointInfoTypeDef",
    {
        "EndpointName": str,
    },
)

ProductionVariantServerlessConfigOutputTypeDef = TypedDict(
    "ProductionVariantServerlessConfigOutputTypeDef",
    {
        "MemorySizeInMB": int,
        "MaxConcurrency": int,
        "ProvisionedConcurrency": int,
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


InferenceMetricsOutputTypeDef = TypedDict(
    "InferenceMetricsOutputTypeDef",
    {
        "MaxInvocations": int,
        "ModelLatency": int,
    },
)

EndpointSummaryOutputTypeDef = TypedDict(
    "EndpointSummaryOutputTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "EndpointStatus": EndpointStatusType,
    },
)

EnvironmentParameterOutputTypeDef = TypedDict(
    "EnvironmentParameterOutputTypeDef",
    {
        "Key": str,
        "ValueType": str,
        "Value": str,
    },
)

FailStepMetadataOutputTypeDef = TypedDict(
    "FailStepMetadataOutputTypeDef",
    {
        "ErrorMessage": str,
    },
)

FeatureParameterTypeDef = TypedDict(
    "FeatureParameterTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

FileSystemConfigOutputTypeDef = TypedDict(
    "FileSystemConfigOutputTypeDef",
    {
        "MountPath": str,
        "DefaultUid": int,
        "DefaultGid": int,
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


FinalHyperParameterTuningJobObjectiveMetricOutputTypeDef = TypedDict(
    "FinalHyperParameterTuningJobObjectiveMetricOutputTypeDef",
    {
        "Type": HyperParameterTuningJobObjectiveTypeType,
        "MetricName": str,
        "Value": float,
    },
)

FlowDefinitionSummaryOutputTypeDef = TypedDict(
    "FlowDefinitionSummaryOutputTypeDef",
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

GetLineageGroupPolicyResponseOutputTypeDef = TypedDict(
    "GetLineageGroupPolicyResponseOutputTypeDef",
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

GetModelPackageGroupPolicyOutputOutputTypeDef = TypedDict(
    "GetModelPackageGroupPolicyOutputOutputTypeDef",
    {
        "ResourcePolicy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSagemakerServicecatalogPortfolioStatusOutputOutputTypeDef = TypedDict(
    "GetSagemakerServicecatalogPortfolioStatusOutputOutputTypeDef",
    {
        "Status": SagemakerServicecatalogStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PropertyNameSuggestionOutputTypeDef = TypedDict(
    "PropertyNameSuggestionOutputTypeDef",
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

HubContentInfoOutputTypeDef = TypedDict(
    "HubContentInfoOutputTypeDef",
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

HubInfoOutputTypeDef = TypedDict(
    "HubInfoOutputTypeDef",
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

HumanLoopActivationConditionsConfigOutputTypeDef = TypedDict(
    "HumanLoopActivationConditionsConfigOutputTypeDef",
    {
        "HumanLoopActivationConditions": str,
    },
)

HumanLoopActivationConditionsConfigTypeDef = TypedDict(
    "HumanLoopActivationConditionsConfigTypeDef",
    {
        "HumanLoopActivationConditions": str,
    },
)

UiConfigOutputTypeDef = TypedDict(
    "UiConfigOutputTypeDef",
    {
        "UiTemplateS3Uri": str,
        "HumanTaskUiArn": str,
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

HumanTaskUiSummaryOutputTypeDef = TypedDict(
    "HumanTaskUiSummaryOutputTypeDef",
    {
        "HumanTaskUiName": str,
        "HumanTaskUiArn": str,
        "CreationTime": datetime,
    },
)

HyperParameterTuningJobObjectiveOutputTypeDef = TypedDict(
    "HyperParameterTuningJobObjectiveOutputTypeDef",
    {
        "Type": HyperParameterTuningJobObjectiveTypeType,
        "MetricName": str,
    },
)

HyperParameterTuningJobObjectiveTypeDef = TypedDict(
    "HyperParameterTuningJobObjectiveTypeDef",
    {
        "Type": HyperParameterTuningJobObjectiveTypeType,
        "MetricName": str,
    },
)

HyperParameterTuningInstanceConfigOutputTypeDef = TypedDict(
    "HyperParameterTuningInstanceConfigOutputTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "VolumeSizeInGB": int,
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

ResourceLimitsOutputTypeDef = TypedDict(
    "ResourceLimitsOutputTypeDef",
    {
        "MaxNumberOfTrainingJobs": int,
        "MaxParallelTrainingJobs": int,
        "MaxRuntimeInSeconds": int,
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


HyperbandStrategyConfigOutputTypeDef = TypedDict(
    "HyperbandStrategyConfigOutputTypeDef",
    {
        "MinResource": int,
        "MaxResource": int,
    },
)

HyperbandStrategyConfigTypeDef = TypedDict(
    "HyperbandStrategyConfigTypeDef",
    {
        "MinResource": int,
        "MaxResource": int,
    },
    total=False,
)

ParentHyperParameterTuningJobOutputTypeDef = TypedDict(
    "ParentHyperParameterTuningJobOutputTypeDef",
    {
        "HyperParameterTuningJobName": str,
    },
)

ParentHyperParameterTuningJobTypeDef = TypedDict(
    "ParentHyperParameterTuningJobTypeDef",
    {
        "HyperParameterTuningJobName": str,
    },
    total=False,
)

IamIdentityOutputTypeDef = TypedDict(
    "IamIdentityOutputTypeDef",
    {
        "Arn": str,
        "PrincipalId": str,
        "SourceIdentity": str,
    },
)

RepositoryAuthConfigOutputTypeDef = TypedDict(
    "RepositoryAuthConfigOutputTypeDef",
    {
        "RepositoryCredentialsProviderArn": str,
    },
)

RepositoryAuthConfigTypeDef = TypedDict(
    "RepositoryAuthConfigTypeDef",
    {
        "RepositoryCredentialsProviderArn": str,
    },
)

ImageOutputTypeDef = TypedDict(
    "ImageOutputTypeDef",
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

ImageVersionOutputTypeDef = TypedDict(
    "ImageVersionOutputTypeDef",
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

ImportHubContentResponseOutputTypeDef = TypedDict(
    "ImportHubContentResponseOutputTypeDef",
    {
        "HubArn": str,
        "HubContentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommendationMetricsOutputTypeDef = TypedDict(
    "RecommendationMetricsOutputTypeDef",
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

InferenceRecommendationsJobOutputTypeDef = TypedDict(
    "InferenceRecommendationsJobOutputTypeDef",
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

InstanceGroupOutputTypeDef = TypedDict(
    "InstanceGroupOutputTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "InstanceGroupName": str,
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

IntegerParameterRangeOutputTypeDef = TypedDict(
    "IntegerParameterRangeOutputTypeDef",
    {
        "Name": str,
        "MinValue": str,
        "MaxValue": str,
        "ScalingType": HyperParameterScalingTypeType,
    },
)

IntegerParameterRangeSpecificationOutputTypeDef = TypedDict(
    "IntegerParameterRangeSpecificationOutputTypeDef",
    {
        "MinValue": str,
        "MaxValue": str,
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


KernelSpecOutputTypeDef = TypedDict(
    "KernelSpecOutputTypeDef",
    {
        "Name": str,
        "DisplayName": str,
    },
)

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


LabelCountersForWorkteamOutputTypeDef = TypedDict(
    "LabelCountersForWorkteamOutputTypeDef",
    {
        "HumanLabeled": int,
        "PendingHuman": int,
        "Total": int,
    },
)

LabelingJobDataAttributesOutputTypeDef = TypedDict(
    "LabelingJobDataAttributesOutputTypeDef",
    {
        "ContentClassifiers": List[ContentClassifierType],
    },
)

LabelingJobDataAttributesTypeDef = TypedDict(
    "LabelingJobDataAttributesTypeDef",
    {
        "ContentClassifiers": Sequence[ContentClassifierType],
    },
    total=False,
)

LabelingJobS3DataSourceOutputTypeDef = TypedDict(
    "LabelingJobS3DataSourceOutputTypeDef",
    {
        "ManifestS3Uri": str,
    },
)

LabelingJobSnsDataSourceOutputTypeDef = TypedDict(
    "LabelingJobSnsDataSourceOutputTypeDef",
    {
        "SnsTopicArn": str,
    },
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

LineageGroupSummaryOutputTypeDef = TypedDict(
    "LineageGroupSummaryOutputTypeDef",
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


ListAliasesResponseOutputTypeDef = TypedDict(
    "ListAliasesResponseOutputTypeDef",
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

MonitoringJobDefinitionSummaryOutputTypeDef = TypedDict(
    "MonitoringJobDefinitionSummaryOutputTypeDef",
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


ModelCardExportJobSummaryOutputTypeDef = TypedDict(
    "ModelCardExportJobSummaryOutputTypeDef",
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


ModelCardVersionSummaryOutputTypeDef = TypedDict(
    "ModelCardVersionSummaryOutputTypeDef",
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

ModelCardSummaryOutputTypeDef = TypedDict(
    "ModelCardSummaryOutputTypeDef",
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

ModelMetadataSummaryOutputTypeDef = TypedDict(
    "ModelMetadataSummaryOutputTypeDef",
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

ModelPackageGroupSummaryOutputTypeDef = TypedDict(
    "ModelPackageGroupSummaryOutputTypeDef",
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

ModelPackageSummaryOutputTypeDef = TypedDict(
    "ModelPackageSummaryOutputTypeDef",
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

ModelSummaryOutputTypeDef = TypedDict(
    "ModelSummaryOutputTypeDef",
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

MonitoringAlertHistorySummaryOutputTypeDef = TypedDict(
    "MonitoringAlertHistorySummaryOutputTypeDef",
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

MonitoringScheduleSummaryOutputTypeDef = TypedDict(
    "MonitoringScheduleSummaryOutputTypeDef",
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

NotebookInstanceLifecycleConfigSummaryOutputTypeDef = TypedDict(
    "NotebookInstanceLifecycleConfigSummaryOutputTypeDef",
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

NotebookInstanceSummaryOutputTypeDef = TypedDict(
    "NotebookInstanceSummaryOutputTypeDef",
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


PipelineExecutionSummaryOutputTypeDef = TypedDict(
    "PipelineExecutionSummaryOutputTypeDef",
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


ParameterOutputTypeDef = TypedDict(
    "ParameterOutputTypeDef",
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

PipelineSummaryOutputTypeDef = TypedDict(
    "PipelineSummaryOutputTypeDef",
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

ProcessingJobSummaryOutputTypeDef = TypedDict(
    "ProcessingJobSummaryOutputTypeDef",
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

ProjectSummaryOutputTypeDef = TypedDict(
    "ProjectSummaryOutputTypeDef",
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

SpaceDetailsOutputTypeDef = TypedDict(
    "SpaceDetailsOutputTypeDef",
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

StudioLifecycleConfigDetailsOutputTypeDef = TypedDict(
    "StudioLifecycleConfigDetailsOutputTypeDef",
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

TransformJobSummaryOutputTypeDef = TypedDict(
    "TransformJobSummaryOutputTypeDef",
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

UserProfileDetailsOutputTypeDef = TypedDict(
    "UserProfileDetailsOutputTypeDef",
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

OidcMemberDefinitionOutputTypeDef = TypedDict(
    "OidcMemberDefinitionOutputTypeDef",
    {
        "Groups": List[str],
    },
)

OidcMemberDefinitionTypeDef = TypedDict(
    "OidcMemberDefinitionTypeDef",
    {
        "Groups": Sequence[str],
    },
)

MonitoringGroundTruthS3InputOutputTypeDef = TypedDict(
    "MonitoringGroundTruthS3InputOutputTypeDef",
    {
        "S3Uri": str,
    },
)

MonitoringGroundTruthS3InputTypeDef = TypedDict(
    "MonitoringGroundTruthS3InputTypeDef",
    {
        "S3Uri": str,
    },
    total=False,
)

ModelDashboardEndpointOutputTypeDef = TypedDict(
    "ModelDashboardEndpointOutputTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "EndpointStatus": EndpointStatusType,
    },
)

ModelDashboardIndicatorActionOutputTypeDef = TypedDict(
    "ModelDashboardIndicatorActionOutputTypeDef",
    {
        "Enabled": bool,
    },
)

S3ModelDataSourceOutputTypeDef = TypedDict(
    "S3ModelDataSourceOutputTypeDef",
    {
        "S3Uri": str,
        "S3DataType": S3ModelDataTypeType,
        "CompressionType": ModelCompressionTypeType,
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

RealTimeInferenceConfigOutputTypeDef = TypedDict(
    "RealTimeInferenceConfigOutputTypeDef",
    {
        "InstanceType": InstanceTypeType,
        "InstanceCount": int,
    },
)

RealTimeInferenceConfigTypeDef = TypedDict(
    "RealTimeInferenceConfigTypeDef",
    {
        "InstanceType": InstanceTypeType,
        "InstanceCount": int,
    },
)

ModelInputOutputTypeDef = TypedDict(
    "ModelInputOutputTypeDef",
    {
        "DataInputConfig": str,
    },
)

ModelInputTypeDef = TypedDict(
    "ModelInputTypeDef",
    {
        "DataInputConfig": str,
    },
)

ModelLatencyThresholdOutputTypeDef = TypedDict(
    "ModelLatencyThresholdOutputTypeDef",
    {
        "Percentile": str,
        "ValueInMilliseconds": int,
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

ModelPackageStatusItemOutputTypeDef = TypedDict(
    "ModelPackageStatusItemOutputTypeDef",
    {
        "Name": str,
        "Status": DetailedModelPackageStatusType,
        "FailureReason": str,
    },
)

ModelStepMetadataOutputTypeDef = TypedDict(
    "ModelStepMetadataOutputTypeDef",
    {
        "Arn": str,
    },
)

MonitoringAppSpecificationOutputTypeDef = TypedDict(
    "MonitoringAppSpecificationOutputTypeDef",
    {
        "ImageUri": str,
        "ContainerEntrypoint": List[str],
        "ContainerArguments": List[str],
        "RecordPreprocessorSourceUri": str,
        "PostAnalyticsProcessorSourceUri": str,
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


MonitoringClusterConfigOutputTypeDef = TypedDict(
    "MonitoringClusterConfigOutputTypeDef",
    {
        "InstanceCount": int,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
        "VolumeKmsKeyId": str,
    },
)

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


MonitoringCsvDatasetFormatOutputTypeDef = TypedDict(
    "MonitoringCsvDatasetFormatOutputTypeDef",
    {
        "Header": bool,
    },
)

MonitoringCsvDatasetFormatTypeDef = TypedDict(
    "MonitoringCsvDatasetFormatTypeDef",
    {
        "Header": bool,
    },
    total=False,
)

MonitoringJsonDatasetFormatOutputTypeDef = TypedDict(
    "MonitoringJsonDatasetFormatOutputTypeDef",
    {
        "Line": bool,
    },
)

MonitoringJsonDatasetFormatTypeDef = TypedDict(
    "MonitoringJsonDatasetFormatTypeDef",
    {
        "Line": bool,
    },
    total=False,
)

MonitoringS3OutputOutputTypeDef = TypedDict(
    "MonitoringS3OutputOutputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
        "S3UploadMode": ProcessingS3UploadModeType,
    },
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


ScheduleConfigOutputTypeDef = TypedDict(
    "ScheduleConfigOutputTypeDef",
    {
        "ScheduleExpression": str,
    },
)

ScheduleConfigTypeDef = TypedDict(
    "ScheduleConfigTypeDef",
    {
        "ScheduleExpression": str,
    },
)

NotificationConfigurationOutputTypeDef = TypedDict(
    "NotificationConfigurationOutputTypeDef",
    {
        "NotificationTopicArn": str,
    },
)

S3StorageConfigOutputTypeDef = TypedDict(
    "S3StorageConfigOutputTypeDef",
    {
        "S3Uri": str,
        "KmsKeyId": str,
        "ResolvedOutputS3Uri": str,
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


OidcConfigForResponseOutputTypeDef = TypedDict(
    "OidcConfigForResponseOutputTypeDef",
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

OnlineStoreSecurityConfigOutputTypeDef = TypedDict(
    "OnlineStoreSecurityConfigOutputTypeDef",
    {
        "KmsKeyId": str,
    },
)

TtlDurationOutputTypeDef = TypedDict(
    "TtlDurationOutputTypeDef",
    {
        "Unit": TtlDurationUnitType,
        "Value": int,
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

TargetPlatformOutputTypeDef = TypedDict(
    "TargetPlatformOutputTypeDef",
    {
        "Os": TargetPlatformOsType,
        "Arch": TargetPlatformArchType,
        "Accelerator": TargetPlatformAcceleratorType,
    },
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


OutputParameterTypeDef = TypedDict(
    "OutputParameterTypeDef",
    {
        "Name": str,
        "Value": str,
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

ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

ParentOutputTypeDef = TypedDict(
    "ParentOutputTypeDef",
    {
        "TrialName": str,
        "ExperimentName": str,
    },
)

ProductionVariantStatusOutputTypeDef = TypedDict(
    "ProductionVariantStatusOutputTypeDef",
    {
        "Status": VariantStatusType,
        "StatusMessage": str,
        "StartTime": datetime,
    },
)

PhaseOutputTypeDef = TypedDict(
    "PhaseOutputTypeDef",
    {
        "InitialNumberOfUsers": int,
        "SpawnRate": int,
        "DurationInSeconds": int,
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

ProcessingJobStepMetadataOutputTypeDef = TypedDict(
    "ProcessingJobStepMetadataOutputTypeDef",
    {
        "Arn": str,
    },
)

QualityCheckStepMetadataOutputTypeDef = TypedDict(
    "QualityCheckStepMetadataOutputTypeDef",
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

RegisterModelStepMetadataOutputTypeDef = TypedDict(
    "RegisterModelStepMetadataOutputTypeDef",
    {
        "Arn": str,
    },
)

TrainingJobStepMetadataOutputTypeDef = TypedDict(
    "TrainingJobStepMetadataOutputTypeDef",
    {
        "Arn": str,
    },
)

TransformJobStepMetadataOutputTypeDef = TypedDict(
    "TransformJobStepMetadataOutputTypeDef",
    {
        "Arn": str,
    },
)

TuningJobStepMetaDataOutputTypeDef = TypedDict(
    "TuningJobStepMetaDataOutputTypeDef",
    {
        "Arn": str,
    },
)

SelectiveExecutionResultOutputTypeDef = TypedDict(
    "SelectiveExecutionResultOutputTypeDef",
    {
        "SourcePipelineExecutionArn": str,
    },
)

ProcessingClusterConfigOutputTypeDef = TypedDict(
    "ProcessingClusterConfigOutputTypeDef",
    {
        "InstanceCount": int,
        "InstanceType": ProcessingInstanceTypeType,
        "VolumeSizeInGB": int,
        "VolumeKmsKeyId": str,
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


ProcessingFeatureStoreOutputOutputTypeDef = TypedDict(
    "ProcessingFeatureStoreOutputOutputTypeDef",
    {
        "FeatureGroupName": str,
    },
)

ProcessingFeatureStoreOutputTypeDef = TypedDict(
    "ProcessingFeatureStoreOutputTypeDef",
    {
        "FeatureGroupName": str,
    },
)

ProcessingS3InputOutputTypeDef = TypedDict(
    "ProcessingS3InputOutputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
        "S3DataType": ProcessingS3DataTypeType,
        "S3InputMode": ProcessingS3InputModeType,
        "S3DataDistributionType": ProcessingS3DataDistributionTypeType,
        "S3CompressionType": ProcessingS3CompressionTypeType,
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


ProcessingS3OutputOutputTypeDef = TypedDict(
    "ProcessingS3OutputOutputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
        "S3UploadMode": ProcessingS3UploadModeType,
    },
)

ProcessingS3OutputTypeDef = TypedDict(
    "ProcessingS3OutputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
        "S3UploadMode": ProcessingS3UploadModeType,
    },
)

ProductionVariantCoreDumpConfigOutputTypeDef = TypedDict(
    "ProductionVariantCoreDumpConfigOutputTypeDef",
    {
        "DestinationS3Uri": str,
        "KmsKeyId": str,
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

ProvisioningParameterOutputTypeDef = TypedDict(
    "ProvisioningParameterOutputTypeDef",
    {
        "Key": str,
        "Value": str,
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

USDOutputTypeDef = TypedDict(
    "USDOutputTypeDef",
    {
        "Dollars": int,
        "Cents": int,
        "TenthFractionsOfACent": int,
    },
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

PutModelPackageGroupPolicyOutputOutputTypeDef = TypedDict(
    "PutModelPackageGroupPolicyOutputOutputTypeDef",
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

VertexOutputTypeDef = TypedDict(
    "VertexOutputTypeDef",
    {
        "Arn": str,
        "Type": str,
        "LineageType": LineageTypeType,
    },
)

RStudioServerProAppSettingsOutputTypeDef = TypedDict(
    "RStudioServerProAppSettingsOutputTypeDef",
    {
        "AccessStatus": RStudioServerProAccessStatusType,
        "UserGroup": RStudioServerProUserGroupType,
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

RecommendationJobPayloadConfigOutputTypeDef = TypedDict(
    "RecommendationJobPayloadConfigOutputTypeDef",
    {
        "SamplePayloadUrl": str,
        "SupportedContentTypes": List[str],
    },
)

RecommendationJobPayloadConfigTypeDef = TypedDict(
    "RecommendationJobPayloadConfigTypeDef",
    {
        "SamplePayloadUrl": str,
        "SupportedContentTypes": Sequence[str],
    },
    total=False,
)

RecommendationJobResourceLimitOutputTypeDef = TypedDict(
    "RecommendationJobResourceLimitOutputTypeDef",
    {
        "MaxNumberOfTests": int,
        "MaxParallelOfTests": int,
    },
)

RecommendationJobVpcConfigOutputTypeDef = TypedDict(
    "RecommendationJobVpcConfigOutputTypeDef",
    {
        "SecurityGroupIds": List[str],
        "Subnets": List[str],
    },
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

RenderingErrorOutputTypeDef = TypedDict(
    "RenderingErrorOutputTypeDef",
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

RetryPipelineExecutionResponseOutputTypeDef = TypedDict(
    "RetryPipelineExecutionResponseOutputTypeDef",
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


SelectedStepOutputTypeDef = TypedDict(
    "SelectedStepOutputTypeDef",
    {
        "StepName": str,
    },
)

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


SendPipelineExecutionStepFailureResponseOutputTypeDef = TypedDict(
    "SendPipelineExecutionStepFailureResponseOutputTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SendPipelineExecutionStepSuccessResponseOutputTypeDef = TypedDict(
    "SendPipelineExecutionStepSuccessResponseOutputTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ShadowModelVariantConfigOutputTypeDef = TypedDict(
    "ShadowModelVariantConfigOutputTypeDef",
    {
        "ShadowModelVariantName": str,
        "SamplingPercentage": int,
    },
)

ShadowModelVariantConfigTypeDef = TypedDict(
    "ShadowModelVariantConfigTypeDef",
    {
        "ShadowModelVariantName": str,
        "SamplingPercentage": int,
    },
)

SharingSettingsOutputTypeDef = TypedDict(
    "SharingSettingsOutputTypeDef",
    {
        "NotebookOutputOption": NotebookOutputOptionType,
        "S3OutputPath": str,
        "S3KmsKeyId": str,
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

SourceAlgorithmOutputTypeDef = TypedDict(
    "SourceAlgorithmOutputTypeDef",
    {
        "ModelDataUrl": str,
        "AlgorithmName": str,
    },
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


SourceIpConfigOutputTypeDef = TypedDict(
    "SourceIpConfigOutputTypeDef",
    {
        "Cidrs": List[str],
    },
)

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

StartInferenceExperimentResponseOutputTypeDef = TypedDict(
    "StartInferenceExperimentResponseOutputTypeDef",
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

StartPipelineExecutionResponseOutputTypeDef = TypedDict(
    "StartPipelineExecutionResponseOutputTypeDef",
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

StopInferenceExperimentResponseOutputTypeDef = TypedDict(
    "StopInferenceExperimentResponseOutputTypeDef",
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

StopPipelineExecutionResponseOutputTypeDef = TypedDict(
    "StopPipelineExecutionResponseOutputTypeDef",
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

TimeSeriesConfigOutputTypeDef = TypedDict(
    "TimeSeriesConfigOutputTypeDef",
    {
        "TargetAttributeName": str,
        "TimestampAttributeName": str,
        "ItemIdentifierAttributeName": str,
        "GroupingAttributeNames": List[str],
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


TimeSeriesTransformationsOutputTypeDef = TypedDict(
    "TimeSeriesTransformationsOutputTypeDef",
    {
        "Filling": Dict[str, Dict[FillingTypeType, str]],
        "Aggregation": Dict[str, AggregationTransformationValueType],
    },
)

TimeSeriesTransformationsTypeDef = TypedDict(
    "TimeSeriesTransformationsTypeDef",
    {
        "Filling": Mapping[str, Mapping[FillingTypeType, str]],
        "Aggregation": Mapping[str, AggregationTransformationValueType],
    },
    total=False,
)

TrainingRepositoryAuthConfigOutputTypeDef = TypedDict(
    "TrainingRepositoryAuthConfigOutputTypeDef",
    {
        "TrainingRepositoryCredentialsProviderArn": str,
    },
)

TrainingRepositoryAuthConfigTypeDef = TypedDict(
    "TrainingRepositoryAuthConfigTypeDef",
    {
        "TrainingRepositoryCredentialsProviderArn": str,
    },
)

TransformS3DataSourceOutputTypeDef = TypedDict(
    "TransformS3DataSourceOutputTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
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


UpdateActionResponseOutputTypeDef = TypedDict(
    "UpdateActionResponseOutputTypeDef",
    {
        "ActionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateAppImageConfigResponseOutputTypeDef = TypedDict(
    "UpdateAppImageConfigResponseOutputTypeDef",
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


UpdateArtifactResponseOutputTypeDef = TypedDict(
    "UpdateArtifactResponseOutputTypeDef",
    {
        "ArtifactArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateCodeRepositoryOutputOutputTypeDef = TypedDict(
    "UpdateCodeRepositoryOutputOutputTypeDef",
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


UpdateContextResponseOutputTypeDef = TypedDict(
    "UpdateContextResponseOutputTypeDef",
    {
        "ContextArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateDomainResponseOutputTypeDef = TypedDict(
    "UpdateDomainResponseOutputTypeDef",
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

UpdateEndpointOutputOutputTypeDef = TypedDict(
    "UpdateEndpointOutputOutputTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEndpointWeightsAndCapacitiesOutputOutputTypeDef = TypedDict(
    "UpdateEndpointWeightsAndCapacitiesOutputOutputTypeDef",
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


UpdateExperimentResponseOutputTypeDef = TypedDict(
    "UpdateExperimentResponseOutputTypeDef",
    {
        "ExperimentArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFeatureGroupResponseOutputTypeDef = TypedDict(
    "UpdateFeatureGroupResponseOutputTypeDef",
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


UpdateHubResponseOutputTypeDef = TypedDict(
    "UpdateHubResponseOutputTypeDef",
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


UpdateImageResponseOutputTypeDef = TypedDict(
    "UpdateImageResponseOutputTypeDef",
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


UpdateImageVersionResponseOutputTypeDef = TypedDict(
    "UpdateImageVersionResponseOutputTypeDef",
    {
        "ImageVersionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateInferenceExperimentResponseOutputTypeDef = TypedDict(
    "UpdateInferenceExperimentResponseOutputTypeDef",
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


UpdateModelCardResponseOutputTypeDef = TypedDict(
    "UpdateModelCardResponseOutputTypeDef",
    {
        "ModelCardArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateModelPackageOutputOutputTypeDef = TypedDict(
    "UpdateModelPackageOutputOutputTypeDef",
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

UpdateMonitoringAlertResponseOutputTypeDef = TypedDict(
    "UpdateMonitoringAlertResponseOutputTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringAlertName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateMonitoringScheduleResponseOutputTypeDef = TypedDict(
    "UpdateMonitoringScheduleResponseOutputTypeDef",
    {
        "MonitoringScheduleArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePipelineExecutionResponseOutputTypeDef = TypedDict(
    "UpdatePipelineExecutionResponseOutputTypeDef",
    {
        "PipelineExecutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePipelineResponseOutputTypeDef = TypedDict(
    "UpdatePipelineResponseOutputTypeDef",
    {
        "PipelineArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateProjectOutputOutputTypeDef = TypedDict(
    "UpdateProjectOutputOutputTypeDef",
    {
        "ProjectArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateSpaceResponseOutputTypeDef = TypedDict(
    "UpdateSpaceResponseOutputTypeDef",
    {
        "SpaceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateTrainingJobResponseOutputTypeDef = TypedDict(
    "UpdateTrainingJobResponseOutputTypeDef",
    {
        "TrainingJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateTrialComponentResponseOutputTypeDef = TypedDict(
    "UpdateTrialComponentResponseOutputTypeDef",
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


UpdateTrialResponseOutputTypeDef = TypedDict(
    "UpdateTrialResponseOutputTypeDef",
    {
        "TrialArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateUserProfileResponseOutputTypeDef = TypedDict(
    "UpdateUserProfileResponseOutputTypeDef",
    {
        "UserProfileArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

WorkforceVpcConfigResponseOutputTypeDef = TypedDict(
    "WorkforceVpcConfigResponseOutputTypeDef",
    {
        "VpcId": str,
        "SecurityGroupIds": List[str],
        "Subnets": List[str],
        "VpcEndpointId": str,
    },
)

ActionSummaryOutputTypeDef = TypedDict(
    "ActionSummaryOutputTypeDef",
    {
        "ActionArn": str,
        "ActionName": str,
        "Source": ActionSourceOutputTypeDef,
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


AddTagsOutputOutputTypeDef = TypedDict(
    "AddTagsOutputOutputTypeDef",
    {
        "Tags": List[TagOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsOutputOutputTypeDef = TypedDict(
    "ListTagsOutputOutputTypeDef",
    {
        "Tags": List[TagOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoRollbackConfigOutputTypeDef = TypedDict(
    "AutoRollbackConfigOutputTypeDef",
    {
        "Alarms": List[AlarmOutputTypeDef],
    },
)

AutoRollbackConfigTypeDef = TypedDict(
    "AutoRollbackConfigTypeDef",
    {
        "Alarms": Sequence[AlarmTypeDef],
    },
    total=False,
)

HyperParameterAlgorithmSpecificationOutputTypeDef = TypedDict(
    "HyperParameterAlgorithmSpecificationOutputTypeDef",
    {
        "TrainingImage": str,
        "TrainingInputMode": TrainingInputModeType,
        "AlgorithmName": str,
        "MetricDefinitions": List[MetricDefinitionOutputTypeDef],
    },
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


AlgorithmStatusDetailsOutputTypeDef = TypedDict(
    "AlgorithmStatusDetailsOutputTypeDef",
    {
        "ValidationStatuses": List[AlgorithmStatusItemOutputTypeDef],
        "ImageScanStatuses": List[AlgorithmStatusItemOutputTypeDef],
    },
)

ListAlgorithmsOutputOutputTypeDef = TypedDict(
    "ListAlgorithmsOutputOutputTypeDef",
    {
        "AlgorithmSummaryList": List[AlgorithmSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAppsResponseOutputTypeDef = TypedDict(
    "ListAppsResponseOutputTypeDef",
    {
        "Apps": List[AppDetailsOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ArtifactSourceOutputTypeDef = TypedDict(
    "ArtifactSourceOutputTypeDef",
    {
        "SourceUri": str,
        "SourceTypes": List[ArtifactSourceTypeOutputTypeDef],
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


AsyncInferenceOutputConfigOutputTypeDef = TypedDict(
    "AsyncInferenceOutputConfigOutputTypeDef",
    {
        "KmsKeyId": str,
        "S3OutputPath": str,
        "NotificationConfig": AsyncInferenceNotificationConfigOutputTypeDef,
        "S3FailurePath": str,
    },
)

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

AutoMLCandidateGenerationConfigOutputTypeDef = TypedDict(
    "AutoMLCandidateGenerationConfigOutputTypeDef",
    {
        "FeatureSpecificationS3Uri": str,
        "AlgorithmsConfig": List[AutoMLAlgorithmConfigOutputTypeDef],
    },
)

CandidateGenerationConfigOutputTypeDef = TypedDict(
    "CandidateGenerationConfigOutputTypeDef",
    {
        "AlgorithmsConfig": List[AutoMLAlgorithmConfigOutputTypeDef],
    },
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

AutoMLDataSourceOutputTypeDef = TypedDict(
    "AutoMLDataSourceOutputTypeDef",
    {
        "S3DataSource": AutoMLS3DataSourceOutputTypeDef,
    },
)

AutoMLDataSourceTypeDef = TypedDict(
    "AutoMLDataSourceTypeDef",
    {
        "S3DataSource": AutoMLS3DataSourceTypeDef,
    },
)

ImageClassificationJobConfigOutputTypeDef = TypedDict(
    "ImageClassificationJobConfigOutputTypeDef",
    {
        "CompletionCriteria": AutoMLJobCompletionCriteriaOutputTypeDef,
    },
)

TextClassificationJobConfigOutputTypeDef = TypedDict(
    "TextClassificationJobConfigOutputTypeDef",
    {
        "CompletionCriteria": AutoMLJobCompletionCriteriaOutputTypeDef,
        "ContentColumn": str,
        "TargetLabelColumn": str,
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

ResolvedAttributesOutputTypeDef = TypedDict(
    "ResolvedAttributesOutputTypeDef",
    {
        "AutoMLJobObjective": AutoMLJobObjectiveOutputTypeDef,
        "ProblemType": ProblemTypeType,
        "CompletionCriteria": AutoMLJobCompletionCriteriaOutputTypeDef,
    },
)

AutoMLJobSummaryOutputTypeDef = TypedDict(
    "AutoMLJobSummaryOutputTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "AutoMLJobStatus": AutoMLJobStatusType,
        "AutoMLJobSecondaryStatus": AutoMLJobSecondaryStatusType,
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "PartialFailureReasons": List[AutoMLPartialFailureReasonOutputTypeDef],
    },
)

AutoMLProblemTypeResolvedAttributesOutputTypeDef = TypedDict(
    "AutoMLProblemTypeResolvedAttributesOutputTypeDef",
    {
        "TabularResolvedAttributes": TabularResolvedAttributesOutputTypeDef,
    },
)

AutoMLSecurityConfigOutputTypeDef = TypedDict(
    "AutoMLSecurityConfigOutputTypeDef",
    {
        "VolumeKmsKeyId": str,
        "EnableInterContainerTrafficEncryption": bool,
        "VpcConfig": VpcConfigOutputTypeDef,
    },
)

LabelingJobResourceConfigOutputTypeDef = TypedDict(
    "LabelingJobResourceConfigOutputTypeDef",
    {
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigOutputTypeDef,
    },
)

MonitoringNetworkConfigOutputTypeDef = TypedDict(
    "MonitoringNetworkConfigOutputTypeDef",
    {
        "EnableInterContainerTrafficEncryption": bool,
        "EnableNetworkIsolation": bool,
        "VpcConfig": VpcConfigOutputTypeDef,
    },
)

NetworkConfigOutputTypeDef = TypedDict(
    "NetworkConfigOutputTypeDef",
    {
        "EnableInterContainerTrafficEncryption": bool,
        "EnableNetworkIsolation": bool,
        "VpcConfig": VpcConfigOutputTypeDef,
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

BiasOutputTypeDef = TypedDict(
    "BiasOutputTypeDef",
    {
        "Report": MetricsSourceOutputTypeDef,
        "PreTrainingReport": MetricsSourceOutputTypeDef,
        "PostTrainingReport": MetricsSourceOutputTypeDef,
    },
)

DriftCheckModelDataQualityOutputTypeDef = TypedDict(
    "DriftCheckModelDataQualityOutputTypeDef",
    {
        "Statistics": MetricsSourceOutputTypeDef,
        "Constraints": MetricsSourceOutputTypeDef,
    },
)

DriftCheckModelQualityOutputTypeDef = TypedDict(
    "DriftCheckModelQualityOutputTypeDef",
    {
        "Statistics": MetricsSourceOutputTypeDef,
        "Constraints": MetricsSourceOutputTypeDef,
    },
)

ExplainabilityOutputTypeDef = TypedDict(
    "ExplainabilityOutputTypeDef",
    {
        "Report": MetricsSourceOutputTypeDef,
    },
)

ModelDataQualityOutputTypeDef = TypedDict(
    "ModelDataQualityOutputTypeDef",
    {
        "Statistics": MetricsSourceOutputTypeDef,
        "Constraints": MetricsSourceOutputTypeDef,
    },
)

ModelQualityOutputTypeDef = TypedDict(
    "ModelQualityOutputTypeDef",
    {
        "Statistics": MetricsSourceOutputTypeDef,
        "Constraints": MetricsSourceOutputTypeDef,
    },
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

CallbackStepMetadataOutputTypeDef = TypedDict(
    "CallbackStepMetadataOutputTypeDef",
    {
        "CallbackToken": str,
        "SqsQueueUrl": str,
        "OutputParameters": List[OutputParameterOutputTypeDef],
    },
)

LambdaStepMetadataOutputTypeDef = TypedDict(
    "LambdaStepMetadataOutputTypeDef",
    {
        "Arn": str,
        "OutputParameters": List[OutputParameterOutputTypeDef],
    },
)

CandidatePropertiesOutputTypeDef = TypedDict(
    "CandidatePropertiesOutputTypeDef",
    {
        "CandidateArtifactLocations": CandidateArtifactLocationsOutputTypeDef,
        "CandidateMetrics": List[MetricDatumOutputTypeDef],
    },
)

CanvasAppSettingsOutputTypeDef = TypedDict(
    "CanvasAppSettingsOutputTypeDef",
    {
        "TimeSeriesForecastingSettings": TimeSeriesForecastingSettingsOutputTypeDef,
        "ModelRegisterSettings": ModelRegisterSettingsOutputTypeDef,
        "WorkspaceSettings": WorkspaceSettingsOutputTypeDef,
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

RollingUpdatePolicyOutputTypeDef = TypedDict(
    "RollingUpdatePolicyOutputTypeDef",
    {
        "MaximumBatchSize": CapacitySizeOutputTypeDef,
        "WaitIntervalInSeconds": int,
        "MaximumExecutionTimeoutInSeconds": int,
        "RollbackMaximumBatchSize": CapacitySizeOutputTypeDef,
    },
)

TrafficRoutingConfigOutputTypeDef = TypedDict(
    "TrafficRoutingConfigOutputTypeDef",
    {
        "Type": TrafficRoutingConfigTypeType,
        "WaitIntervalInSeconds": int,
        "CanarySize": CapacitySizeOutputTypeDef,
        "LinearStepSize": CapacitySizeOutputTypeDef,
    },
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


InferenceExperimentDataStorageConfigOutputTypeDef = TypedDict(
    "InferenceExperimentDataStorageConfigOutputTypeDef",
    {
        "Destination": str,
        "KmsKey": str,
        "ContentType": CaptureContentTypeHeaderOutputTypeDef,
    },
)

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


DataCaptureConfigOutputTypeDef = TypedDict(
    "DataCaptureConfigOutputTypeDef",
    {
        "EnableCapture": bool,
        "InitialSamplingPercentage": int,
        "DestinationS3Uri": str,
        "KmsKeyId": str,
        "CaptureOptions": List[CaptureOptionOutputTypeDef],
        "CaptureContentTypeHeader": CaptureContentTypeHeaderOutputTypeDef,
    },
)

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


EnvironmentParameterRangesOutputTypeDef = TypedDict(
    "EnvironmentParameterRangesOutputTypeDef",
    {
        "CategoricalParameterRanges": List[CategoricalParameterOutputTypeDef],
    },
)

EnvironmentParameterRangesTypeDef = TypedDict(
    "EnvironmentParameterRangesTypeDef",
    {
        "CategoricalParameterRanges": Sequence[CategoricalParameterTypeDef],
    },
    total=False,
)

ClarifyShapConfigOutputTypeDef = TypedDict(
    "ClarifyShapConfigOutputTypeDef",
    {
        "ShapBaselineConfig": ClarifyShapBaselineConfigOutputTypeDef,
        "NumberOfSamples": int,
        "UseLogit": bool,
        "Seed": int,
        "TextConfig": ClarifyTextConfigOutputTypeDef,
    },
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


CodeRepositorySummaryOutputTypeDef = TypedDict(
    "CodeRepositorySummaryOutputTypeDef",
    {
        "CodeRepositoryName": str,
        "CodeRepositoryArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "GitConfig": GitConfigOutputTypeDef,
    },
)

DescribeCodeRepositoryOutputOutputTypeDef = TypedDict(
    "DescribeCodeRepositoryOutputOutputTypeDef",
    {
        "CodeRepositoryName": str,
        "CodeRepositoryArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "GitConfig": GitConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DebugHookConfigOutputTypeDef = TypedDict(
    "DebugHookConfigOutputTypeDef",
    {
        "LocalPath": str,
        "S3OutputPath": str,
        "HookParameters": Dict[str, str],
        "CollectionConfigurations": List[CollectionConfigurationOutputTypeDef],
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


ListCompilationJobsResponseOutputTypeDef = TypedDict(
    "ListCompilationJobsResponseOutputTypeDef",
    {
        "CompilationJobSummaries": List[CompilationJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ContextSummaryOutputTypeDef = TypedDict(
    "ContextSummaryOutputTypeDef",
    {
        "ContextArn": str,
        "ContextName": str,
        "Source": ContextSourceOutputTypeDef,
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


TuningJobCompletionCriteriaOutputTypeDef = TypedDict(
    "TuningJobCompletionCriteriaOutputTypeDef",
    {
        "TargetObjectiveMetricValue": float,
        "BestObjectiveNotImproving": BestObjectiveNotImprovingOutputTypeDef,
        "ConvergenceDetected": ConvergenceDetectedOutputTypeDef,
    },
)

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

ModelBiasBaselineConfigOutputTypeDef = TypedDict(
    "ModelBiasBaselineConfigOutputTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceOutputTypeDef,
    },
)

ModelExplainabilityBaselineConfigOutputTypeDef = TypedDict(
    "ModelExplainabilityBaselineConfigOutputTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceOutputTypeDef,
    },
)

ModelQualityBaselineConfigOutputTypeDef = TypedDict(
    "ModelQualityBaselineConfigOutputTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceOutputTypeDef,
    },
)

DataQualityBaselineConfigOutputTypeDef = TypedDict(
    "DataQualityBaselineConfigOutputTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceOutputTypeDef,
        "StatisticsResource": MonitoringStatisticsResourceOutputTypeDef,
    },
)

MonitoringBaselineConfigOutputTypeDef = TypedDict(
    "MonitoringBaselineConfigOutputTypeDef",
    {
        "BaseliningJobName": str,
        "ConstraintsResource": MonitoringConstraintsResourceOutputTypeDef,
        "StatisticsResource": MonitoringStatisticsResourceOutputTypeDef,
    },
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

DataSourceOutputTypeDef = TypedDict(
    "DataSourceOutputTypeDef",
    {
        "S3DataSource": S3DataSourceOutputTypeDef,
        "FileSystemDataSource": FileSystemDataSourceOutputTypeDef,
    },
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "S3DataSource": S3DataSourceTypeDef,
        "FileSystemDataSource": FileSystemDataSourceTypeDef,
    },
    total=False,
)

DatasetDefinitionOutputTypeDef = TypedDict(
    "DatasetDefinitionOutputTypeDef",
    {
        "AthenaDatasetDefinition": AthenaDatasetDefinitionOutputTypeDef,
        "RedshiftDatasetDefinition": RedshiftDatasetDefinitionOutputTypeDef,
        "LocalPath": str,
        "DataDistributionType": DataDistributionTypeType,
        "InputMode": InputModeType,
    },
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


DeploymentRecommendationOutputTypeDef = TypedDict(
    "DeploymentRecommendationOutputTypeDef",
    {
        "RecommendationStatus": RecommendationStatusType,
        "RealTimeInferenceRecommendations": List[RealTimeInferenceRecommendationOutputTypeDef],
    },
)

DeploymentStageStatusSummaryOutputTypeDef = TypedDict(
    "DeploymentStageStatusSummaryOutputTypeDef",
    {
        "StageName": str,
        "DeviceSelectionConfig": DeviceSelectionConfigOutputTypeDef,
        "DeploymentConfig": EdgeDeploymentConfigOutputTypeDef,
        "DeploymentStatus": EdgeDeploymentStatusOutputTypeDef,
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


DescribeAppResponseOutputTypeDef = TypedDict(
    "DescribeAppResponseOutputTypeDef",
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
        "ResourceSpec": ResourceSpecOutputTypeDef,
        "SpaceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

JupyterServerAppSettingsOutputTypeDef = TypedDict(
    "JupyterServerAppSettingsOutputTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecOutputTypeDef,
        "LifecycleConfigArns": List[str],
        "CodeRepositories": List[CodeRepositoryOutputTypeDef],
    },
)

KernelGatewayAppSettingsOutputTypeDef = TypedDict(
    "KernelGatewayAppSettingsOutputTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecOutputTypeDef,
        "CustomImages": List[CustomImageOutputTypeDef],
        "LifecycleConfigArns": List[str],
    },
)

RSessionAppSettingsOutputTypeDef = TypedDict(
    "RSessionAppSettingsOutputTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecOutputTypeDef,
        "CustomImages": List[CustomImageOutputTypeDef],
    },
)

RStudioServerProDomainSettingsOutputTypeDef = TypedDict(
    "RStudioServerProDomainSettingsOutputTypeDef",
    {
        "DomainExecutionRoleArn": str,
        "RStudioConnectUrl": str,
        "RStudioPackageManagerUrl": str,
        "DefaultResourceSpec": ResourceSpecOutputTypeDef,
    },
)

TensorBoardAppSettingsOutputTypeDef = TypedDict(
    "TensorBoardAppSettingsOutputTypeDef",
    {
        "DefaultResourceSpec": ResourceSpecOutputTypeDef,
    },
)

DescribeDeviceFleetResponseOutputTypeDef = TypedDict(
    "DescribeDeviceFleetResponseOutputTypeDef",
    {
        "DeviceFleetName": str,
        "DeviceFleetArn": str,
        "OutputConfig": EdgeOutputConfigOutputTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
        "IotRoleAlias": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDeviceResponseOutputTypeDef = TypedDict(
    "DescribeDeviceResponseOutputTypeDef",
    {
        "DeviceArn": str,
        "DeviceName": str,
        "Description": str,
        "DeviceFleetName": str,
        "IotThingName": str,
        "RegistrationTime": datetime,
        "LatestHeartbeat": datetime,
        "Models": List[EdgeModelOutputTypeDef],
        "MaxModels": int,
        "NextToken": str,
        "AgentVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEdgePackagingJobResponseOutputTypeDef = TypedDict(
    "DescribeEdgePackagingJobResponseOutputTypeDef",
    {
        "EdgePackagingJobArn": str,
        "EdgePackagingJobName": str,
        "CompilationJobName": str,
        "ModelName": str,
        "ModelVersion": str,
        "RoleArn": str,
        "OutputConfig": EdgeOutputConfigOutputTypeDef,
        "ResourceKey": str,
        "EdgePackagingJobStatus": EdgePackagingJobStatusType,
        "EdgePackagingJobStatusMessage": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ModelArtifact": str,
        "ModelSignature": str,
        "PresetDeploymentOutput": EdgePresetDeploymentOutputOutputTypeDef,
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


ExperimentSummaryOutputTypeDef = TypedDict(
    "ExperimentSummaryOutputTypeDef",
    {
        "ExperimentArn": str,
        "ExperimentName": str,
        "DisplayName": str,
        "ExperimentSource": ExperimentSourceOutputTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)

FeatureGroupSummaryOutputTypeDef = TypedDict(
    "FeatureGroupSummaryOutputTypeDef",
    {
        "FeatureGroupName": str,
        "FeatureGroupArn": str,
        "CreationTime": datetime,
        "FeatureGroupStatus": FeatureGroupStatusType,
        "OfflineStoreStatus": OfflineStoreStatusOutputTypeDef,
    },
)

DescribeFeatureMetadataResponseOutputTypeDef = TypedDict(
    "DescribeFeatureMetadataResponseOutputTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "FeatureName": str,
        "FeatureType": FeatureTypeType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Description": str,
        "Parameters": List[FeatureParameterOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FeatureMetadataOutputTypeDef = TypedDict(
    "FeatureMetadataOutputTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "FeatureName": str,
        "FeatureType": FeatureTypeType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Description": str,
        "Parameters": List[FeatureParameterOutputTypeDef],
    },
)

DescribeHubContentResponseOutputTypeDef = TypedDict(
    "DescribeHubContentResponseOutputTypeDef",
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
        "HubContentDependencies": List[HubContentDependencyOutputTypeDef],
        "HubContentStatus": HubContentStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeHubResponseOutputTypeDef = TypedDict(
    "DescribeHubResponseOutputTypeDef",
    {
        "HubName": str,
        "HubArn": str,
        "HubDisplayName": str,
        "HubDescription": str,
        "HubSearchKeywords": List[str],
        "S3StorageConfig": HubS3StorageConfigOutputTypeDef,
        "HubStatus": HubStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeHumanTaskUiResponseOutputTypeDef = TypedDict(
    "DescribeHumanTaskUiResponseOutputTypeDef",
    {
        "HumanTaskUiArn": str,
        "HumanTaskUiName": str,
        "HumanTaskUiStatus": HumanTaskUiStatusType,
        "CreationTime": datetime,
        "UiTemplate": UiTemplateInfoOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InferenceExperimentSummaryOutputTypeDef = TypedDict(
    "InferenceExperimentSummaryOutputTypeDef",
    {
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Schedule": InferenceExperimentScheduleOutputTypeDef,
        "Status": InferenceExperimentStatusType,
        "StatusReason": str,
        "Description": str,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
    },
)

DescribeModelCardExportJobResponseOutputTypeDef = TypedDict(
    "DescribeModelCardExportJobResponseOutputTypeDef",
    {
        "ModelCardExportJobName": str,
        "ModelCardExportJobArn": str,
        "Status": ModelCardExportJobStatusType,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "OutputConfig": ModelCardExportOutputConfigOutputTypeDef,
        "CreatedAt": datetime,
        "LastModifiedAt": datetime,
        "FailureReason": str,
        "ExportArtifacts": ModelCardExportArtifactsOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringExecutionsResponseOutputTypeDef = TypedDict(
    "ListMonitoringExecutionsResponseOutputTypeDef",
    {
        "MonitoringExecutionSummaries": List[MonitoringExecutionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeNotebookInstanceLifecycleConfigOutputOutputTypeDef = TypedDict(
    "DescribeNotebookInstanceLifecycleConfigOutputOutputTypeDef",
    {
        "NotebookInstanceLifecycleConfigArn": str,
        "NotebookInstanceLifecycleConfigName": str,
        "OnCreate": List[NotebookInstanceLifecycleHookOutputTypeDef],
        "OnStart": List[NotebookInstanceLifecycleHookOutputTypeDef],
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeNotebookInstanceOutputOutputTypeDef = TypedDict(
    "DescribeNotebookInstanceOutputOutputTypeDef",
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
        "InstanceMetadataServiceConfiguration": InstanceMetadataServiceConfigurationOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSubscribedWorkteamResponseOutputTypeDef = TypedDict(
    "DescribeSubscribedWorkteamResponseOutputTypeDef",
    {
        "SubscribedWorkteam": SubscribedWorkteamOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSubscribedWorkteamsResponseOutputTypeDef = TypedDict(
    "ListSubscribedWorkteamsResponseOutputTypeDef",
    {
        "SubscribedWorkteams": List[SubscribedWorkteamOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TrainingJobSummaryOutputTypeDef = TypedDict(
    "TrainingJobSummaryOutputTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "CreationTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatus": TrainingJobStatusType,
        "WarmPoolStatus": WarmPoolStatusOutputTypeDef,
    },
)

TrialSummaryOutputTypeDef = TypedDict(
    "TrialSummaryOutputTypeDef",
    {
        "TrialArn": str,
        "TrialName": str,
        "DisplayName": str,
        "TrialSource": TrialSourceOutputTypeDef,
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


ListStageDevicesResponseOutputTypeDef = TypedDict(
    "ListStageDevicesResponseOutputTypeDef",
    {
        "DeviceDeploymentSummaries": List[DeviceDeploymentSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDeviceFleetsResponseOutputTypeDef = TypedDict(
    "ListDeviceFleetsResponseOutputTypeDef",
    {
        "DeviceFleetSummaries": List[DeviceFleetSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeviceSummaryOutputTypeDef = TypedDict(
    "DeviceSummaryOutputTypeDef",
    {
        "DeviceName": str,
        "DeviceArn": str,
        "Description": str,
        "DeviceFleetName": str,
        "IotThingName": str,
        "RegistrationTime": datetime,
        "LatestHeartbeat": datetime,
        "Models": List[EdgeModelSummaryOutputTypeDef],
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

ListDomainsResponseOutputTypeDef = TypedDict(
    "ListDomainsResponseOutputTypeDef",
    {
        "Domains": List[DomainDetailsOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DriftCheckBiasOutputTypeDef = TypedDict(
    "DriftCheckBiasOutputTypeDef",
    {
        "ConfigFile": FileSourceOutputTypeDef,
        "PreTrainingConstraints": MetricsSourceOutputTypeDef,
        "PostTrainingConstraints": MetricsSourceOutputTypeDef,
    },
)

DriftCheckExplainabilityOutputTypeDef = TypedDict(
    "DriftCheckExplainabilityOutputTypeDef",
    {
        "Constraints": MetricsSourceOutputTypeDef,
        "ConfigFile": FileSourceOutputTypeDef,
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

ListEdgeDeploymentPlansResponseOutputTypeDef = TypedDict(
    "ListEdgeDeploymentPlansResponseOutputTypeDef",
    {
        "EdgeDeploymentPlanSummaries": List[EdgeDeploymentPlanSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDeviceFleetReportResponseOutputTypeDef = TypedDict(
    "GetDeviceFleetReportResponseOutputTypeDef",
    {
        "DeviceFleetArn": str,
        "DeviceFleetName": str,
        "OutputConfig": EdgeOutputConfigOutputTypeDef,
        "Description": str,
        "ReportGenerated": datetime,
        "DeviceStats": DeviceStatsOutputTypeDef,
        "AgentVersions": List[AgentVersionOutputTypeDef],
        "ModelStats": List[EdgeModelStatOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEdgePackagingJobsResponseOutputTypeDef = TypedDict(
    "ListEdgePackagingJobsResponseOutputTypeDef",
    {
        "EdgePackagingJobSummaries": List[EdgePackagingJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEndpointConfigsOutputOutputTypeDef = TypedDict(
    "ListEndpointConfigsOutputOutputTypeDef",
    {
        "EndpointConfigs": List[EndpointConfigSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EndpointOutputConfigurationOutputTypeDef = TypedDict(
    "EndpointOutputConfigurationOutputTypeDef",
    {
        "EndpointName": str,
        "VariantName": str,
        "InstanceType": ProductionVariantInstanceTypeType,
        "InitialInstanceCount": int,
        "ServerlessConfig": ProductionVariantServerlessConfigOutputTypeDef,
    },
)

EndpointPerformanceOutputTypeDef = TypedDict(
    "EndpointPerformanceOutputTypeDef",
    {
        "Metrics": InferenceMetricsOutputTypeDef,
        "EndpointInfo": EndpointInfoOutputTypeDef,
    },
)

ListEndpointsOutputOutputTypeDef = TypedDict(
    "ListEndpointsOutputOutputTypeDef",
    {
        "Endpoints": List[EndpointSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelConfigurationOutputTypeDef = TypedDict(
    "ModelConfigurationOutputTypeDef",
    {
        "InferenceSpecificationName": str,
        "EnvironmentParameters": List[EnvironmentParameterOutputTypeDef],
        "CompilationJobName": str,
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


NestedFiltersTypeDef = TypedDict(
    "NestedFiltersTypeDef",
    {
        "NestedPropertyName": str,
        "Filters": Sequence[FilterTypeDef],
    },
)

HyperParameterTrainingJobSummaryOutputTypeDef = TypedDict(
    "HyperParameterTrainingJobSummaryOutputTypeDef",
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
            FinalHyperParameterTuningJobObjectiveMetricOutputTypeDef
        ),
        "ObjectiveStatus": ObjectiveStatusType,
    },
)

ListFlowDefinitionsResponseOutputTypeDef = TypedDict(
    "ListFlowDefinitionsResponseOutputTypeDef",
    {
        "FlowDefinitionSummaries": List[FlowDefinitionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSearchSuggestionsResponseOutputTypeDef = TypedDict(
    "GetSearchSuggestionsResponseOutputTypeDef",
    {
        "PropertyNameSuggestions": List[PropertyNameSuggestionOutputTypeDef],
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


ListHubContentVersionsResponseOutputTypeDef = TypedDict(
    "ListHubContentVersionsResponseOutputTypeDef",
    {
        "HubContentSummaries": List[HubContentInfoOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHubContentsResponseOutputTypeDef = TypedDict(
    "ListHubContentsResponseOutputTypeDef",
    {
        "HubContentSummaries": List[HubContentInfoOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHubsResponseOutputTypeDef = TypedDict(
    "ListHubsResponseOutputTypeDef",
    {
        "HubSummaries": List[HubInfoOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HumanLoopActivationConfigOutputTypeDef = TypedDict(
    "HumanLoopActivationConfigOutputTypeDef",
    {
        "HumanLoopActivationConditionsConfig": HumanLoopActivationConditionsConfigOutputTypeDef,
    },
)

HumanLoopActivationConfigTypeDef = TypedDict(
    "HumanLoopActivationConfigTypeDef",
    {
        "HumanLoopActivationConditionsConfig": HumanLoopActivationConditionsConfigTypeDef,
    },
)

ListHumanTaskUisResponseOutputTypeDef = TypedDict(
    "ListHumanTaskUisResponseOutputTypeDef",
    {
        "HumanTaskUiSummaries": List[HumanTaskUiSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HyperParameterTuningResourceConfigOutputTypeDef = TypedDict(
    "HyperParameterTuningResourceConfigOutputTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "VolumeSizeInGB": int,
        "VolumeKmsKeyId": str,
        "AllocationStrategy": Literal["Prioritized"],
        "InstanceConfigs": List[HyperParameterTuningInstanceConfigOutputTypeDef],
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

HyperParameterTuningJobSummaryOutputTypeDef = TypedDict(
    "HyperParameterTuningJobSummaryOutputTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobStatus": HyperParameterTuningJobStatusType,
        "Strategy": HyperParameterTuningJobStrategyTypeType,
        "CreationTime": datetime,
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersOutputTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersOutputTypeDef,
        "ResourceLimits": ResourceLimitsOutputTypeDef,
    },
)

HyperParameterTuningJobStrategyConfigOutputTypeDef = TypedDict(
    "HyperParameterTuningJobStrategyConfigOutputTypeDef",
    {
        "HyperbandStrategyConfig": HyperbandStrategyConfigOutputTypeDef,
    },
)

HyperParameterTuningJobStrategyConfigTypeDef = TypedDict(
    "HyperParameterTuningJobStrategyConfigTypeDef",
    {
        "HyperbandStrategyConfig": HyperbandStrategyConfigTypeDef,
    },
    total=False,
)

HyperParameterTuningJobWarmStartConfigOutputTypeDef = TypedDict(
    "HyperParameterTuningJobWarmStartConfigOutputTypeDef",
    {
        "ParentHyperParameterTuningJobs": List[ParentHyperParameterTuningJobOutputTypeDef],
        "WarmStartType": HyperParameterTuningJobWarmStartTypeType,
    },
)

HyperParameterTuningJobWarmStartConfigTypeDef = TypedDict(
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    {
        "ParentHyperParameterTuningJobs": Sequence[ParentHyperParameterTuningJobTypeDef],
        "WarmStartType": HyperParameterTuningJobWarmStartTypeType,
    },
)

UserContextOutputTypeDef = TypedDict(
    "UserContextOutputTypeDef",
    {
        "UserProfileArn": str,
        "UserProfileName": str,
        "DomainId": str,
        "IamIdentity": IamIdentityOutputTypeDef,
    },
)

ImageConfigOutputTypeDef = TypedDict(
    "ImageConfigOutputTypeDef",
    {
        "RepositoryAccessMode": RepositoryAccessModeType,
        "RepositoryAuthConfig": RepositoryAuthConfigOutputTypeDef,
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


ListImagesResponseOutputTypeDef = TypedDict(
    "ListImagesResponseOutputTypeDef",
    {
        "Images": List[ImageOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListImageVersionsResponseOutputTypeDef = TypedDict(
    "ListImageVersionsResponseOutputTypeDef",
    {
        "ImageVersions": List[ImageVersionOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInferenceRecommendationsJobsResponseOutputTypeDef = TypedDict(
    "ListInferenceRecommendationsJobsResponseOutputTypeDef",
    {
        "InferenceRecommendationsJobs": List[InferenceRecommendationsJobOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourceConfigOutputTypeDef = TypedDict(
    "ResourceConfigOutputTypeDef",
    {
        "InstanceType": TrainingInstanceTypeType,
        "InstanceCount": int,
        "VolumeSizeInGB": int,
        "VolumeKmsKeyId": str,
        "InstanceGroups": List[InstanceGroupOutputTypeDef],
        "KeepAlivePeriodInSeconds": int,
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


ParameterRangesOutputTypeDef = TypedDict(
    "ParameterRangesOutputTypeDef",
    {
        "IntegerParameterRanges": List[IntegerParameterRangeOutputTypeDef],
        "ContinuousParameterRanges": List[ContinuousParameterRangeOutputTypeDef],
        "CategoricalParameterRanges": List[CategoricalParameterRangeOutputTypeDef],
        "AutoParameters": List[AutoParameterOutputTypeDef],
    },
)

ParameterRangeOutputTypeDef = TypedDict(
    "ParameterRangeOutputTypeDef",
    {
        "IntegerParameterRangeSpecification": IntegerParameterRangeSpecificationOutputTypeDef,
        "ContinuousParameterRangeSpecification": ContinuousParameterRangeSpecificationOutputTypeDef,
        "CategoricalParameterRangeSpecification": (
            CategoricalParameterRangeSpecificationOutputTypeDef
        ),
    },
)

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

KernelGatewayImageConfigOutputTypeDef = TypedDict(
    "KernelGatewayImageConfigOutputTypeDef",
    {
        "KernelSpecs": List[KernelSpecOutputTypeDef],
        "FileSystemConfig": FileSystemConfigOutputTypeDef,
    },
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


LabelingJobForWorkteamSummaryOutputTypeDef = TypedDict(
    "LabelingJobForWorkteamSummaryOutputTypeDef",
    {
        "LabelingJobName": str,
        "JobReferenceCode": str,
        "WorkRequesterAccountId": str,
        "CreationTime": datetime,
        "LabelCounters": LabelCountersForWorkteamOutputTypeDef,
        "NumberOfHumanWorkersPerDataObject": int,
    },
)

LabelingJobDataSourceOutputTypeDef = TypedDict(
    "LabelingJobDataSourceOutputTypeDef",
    {
        "S3DataSource": LabelingJobS3DataSourceOutputTypeDef,
        "SnsDataSource": LabelingJobSnsDataSourceOutputTypeDef,
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

ListLineageGroupsResponseOutputTypeDef = TypedDict(
    "ListLineageGroupsResponseOutputTypeDef",
    {
        "LineageGroupSummaries": List[LineageGroupSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDataQualityJobDefinitionsResponseOutputTypeDef = TypedDict(
    "ListDataQualityJobDefinitionsResponseOutputTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelBiasJobDefinitionsResponseOutputTypeDef = TypedDict(
    "ListModelBiasJobDefinitionsResponseOutputTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelExplainabilityJobDefinitionsResponseOutputTypeDef = TypedDict(
    "ListModelExplainabilityJobDefinitionsResponseOutputTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelQualityJobDefinitionsResponseOutputTypeDef = TypedDict(
    "ListModelQualityJobDefinitionsResponseOutputTypeDef",
    {
        "JobDefinitionSummaries": List[MonitoringJobDefinitionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelCardExportJobsResponseOutputTypeDef = TypedDict(
    "ListModelCardExportJobsResponseOutputTypeDef",
    {
        "ModelCardExportJobSummaries": List[ModelCardExportJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelCardVersionsResponseOutputTypeDef = TypedDict(
    "ListModelCardVersionsResponseOutputTypeDef",
    {
        "ModelCardVersionSummaryList": List[ModelCardVersionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelCardsResponseOutputTypeDef = TypedDict(
    "ListModelCardsResponseOutputTypeDef",
    {
        "ModelCardSummaries": List[ModelCardSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelMetadataResponseOutputTypeDef = TypedDict(
    "ListModelMetadataResponseOutputTypeDef",
    {
        "ModelMetadataSummaries": List[ModelMetadataSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelPackageGroupsOutputOutputTypeDef = TypedDict(
    "ListModelPackageGroupsOutputOutputTypeDef",
    {
        "ModelPackageGroupSummaryList": List[ModelPackageGroupSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelPackagesOutputOutputTypeDef = TypedDict(
    "ListModelPackagesOutputOutputTypeDef",
    {
        "ModelPackageSummaryList": List[ModelPackageSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListModelsOutputOutputTypeDef = TypedDict(
    "ListModelsOutputOutputTypeDef",
    {
        "Models": List[ModelSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringAlertHistoryResponseOutputTypeDef = TypedDict(
    "ListMonitoringAlertHistoryResponseOutputTypeDef",
    {
        "MonitoringAlertHistory": List[MonitoringAlertHistorySummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringSchedulesResponseOutputTypeDef = TypedDict(
    "ListMonitoringSchedulesResponseOutputTypeDef",
    {
        "MonitoringScheduleSummaries": List[MonitoringScheduleSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNotebookInstanceLifecycleConfigsOutputOutputTypeDef = TypedDict(
    "ListNotebookInstanceLifecycleConfigsOutputOutputTypeDef",
    {
        "NextToken": str,
        "NotebookInstanceLifecycleConfigs": List[
            NotebookInstanceLifecycleConfigSummaryOutputTypeDef
        ],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNotebookInstancesOutputOutputTypeDef = TypedDict(
    "ListNotebookInstancesOutputOutputTypeDef",
    {
        "NextToken": str,
        "NotebookInstances": List[NotebookInstanceSummaryOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelineExecutionsResponseOutputTypeDef = TypedDict(
    "ListPipelineExecutionsResponseOutputTypeDef",
    {
        "PipelineExecutionSummaries": List[PipelineExecutionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelineParametersForExecutionResponseOutputTypeDef = TypedDict(
    "ListPipelineParametersForExecutionResponseOutputTypeDef",
    {
        "PipelineParameters": List[ParameterOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelinesResponseOutputTypeDef = TypedDict(
    "ListPipelinesResponseOutputTypeDef",
    {
        "PipelineSummaries": List[PipelineSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListProcessingJobsResponseOutputTypeDef = TypedDict(
    "ListProcessingJobsResponseOutputTypeDef",
    {
        "ProcessingJobSummaries": List[ProcessingJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListProjectsOutputOutputTypeDef = TypedDict(
    "ListProjectsOutputOutputTypeDef",
    {
        "ProjectSummaryList": List[ProjectSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSpacesResponseOutputTypeDef = TypedDict(
    "ListSpacesResponseOutputTypeDef",
    {
        "Spaces": List[SpaceDetailsOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStudioLifecycleConfigsResponseOutputTypeDef = TypedDict(
    "ListStudioLifecycleConfigsResponseOutputTypeDef",
    {
        "NextToken": str,
        "StudioLifecycleConfigs": List[StudioLifecycleConfigDetailsOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTransformJobsResponseOutputTypeDef = TypedDict(
    "ListTransformJobsResponseOutputTypeDef",
    {
        "TransformJobSummaries": List[TransformJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListUserProfilesResponseOutputTypeDef = TypedDict(
    "ListUserProfilesResponseOutputTypeDef",
    {
        "UserProfiles": List[UserProfileDetailsOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MemberDefinitionOutputTypeDef = TypedDict(
    "MemberDefinitionOutputTypeDef",
    {
        "CognitoMemberDefinition": CognitoMemberDefinitionOutputTypeDef,
        "OidcMemberDefinition": OidcMemberDefinitionOutputTypeDef,
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

MonitoringAlertActionsOutputTypeDef = TypedDict(
    "MonitoringAlertActionsOutputTypeDef",
    {
        "ModelDashboardIndicator": ModelDashboardIndicatorActionOutputTypeDef,
    },
)

ModelDataSourceOutputTypeDef = TypedDict(
    "ModelDataSourceOutputTypeDef",
    {
        "S3DataSource": S3ModelDataSourceOutputTypeDef,
    },
)

ModelDataSourceTypeDef = TypedDict(
    "ModelDataSourceTypeDef",
    {
        "S3DataSource": S3ModelDataSourceTypeDef,
    },
)

ModelInfrastructureConfigOutputTypeDef = TypedDict(
    "ModelInfrastructureConfigOutputTypeDef",
    {
        "InfrastructureType": Literal["RealTimeInference"],
        "RealTimeInferenceConfig": RealTimeInferenceConfigOutputTypeDef,
    },
)

ModelInfrastructureConfigTypeDef = TypedDict(
    "ModelInfrastructureConfigTypeDef",
    {
        "InfrastructureType": Literal["RealTimeInference"],
        "RealTimeInferenceConfig": RealTimeInferenceConfigTypeDef,
    },
)

ModelPackageContainerDefinitionOutputTypeDef = TypedDict(
    "ModelPackageContainerDefinitionOutputTypeDef",
    {
        "ContainerHostname": str,
        "Image": str,
        "ImageDigest": str,
        "ModelDataUrl": str,
        "ProductId": str,
        "Environment": Dict[str, str],
        "ModelInput": ModelInputOutputTypeDef,
        "Framework": str,
        "FrameworkVersion": str,
        "NearestModelName": str,
    },
)

_RequiredModelPackageContainerDefinitionTypeDef = TypedDict(
    "_RequiredModelPackageContainerDefinitionTypeDef",
    {
        "Image": str,
    },
)
_OptionalModelPackageContainerDefinitionTypeDef = TypedDict(
    "_OptionalModelPackageContainerDefinitionTypeDef",
    {
        "ContainerHostname": str,
        "ImageDigest": str,
        "ModelDataUrl": str,
        "ProductId": str,
        "Environment": Mapping[str, str],
        "ModelInput": ModelInputTypeDef,
        "Framework": str,
        "FrameworkVersion": str,
        "NearestModelName": str,
    },
    total=False,
)


class ModelPackageContainerDefinitionTypeDef(
    _RequiredModelPackageContainerDefinitionTypeDef, _OptionalModelPackageContainerDefinitionTypeDef
):
    pass


RecommendationJobStoppingConditionsOutputTypeDef = TypedDict(
    "RecommendationJobStoppingConditionsOutputTypeDef",
    {
        "MaxInvocations": int,
        "ModelLatencyThresholds": List[ModelLatencyThresholdOutputTypeDef],
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

ModelPackageStatusDetailsOutputTypeDef = TypedDict(
    "ModelPackageStatusDetailsOutputTypeDef",
    {
        "ValidationStatuses": List[ModelPackageStatusItemOutputTypeDef],
        "ImageScanStatuses": List[ModelPackageStatusItemOutputTypeDef],
    },
)

MonitoringResourcesOutputTypeDef = TypedDict(
    "MonitoringResourcesOutputTypeDef",
    {
        "ClusterConfig": MonitoringClusterConfigOutputTypeDef,
    },
)

MonitoringResourcesTypeDef = TypedDict(
    "MonitoringResourcesTypeDef",
    {
        "ClusterConfig": MonitoringClusterConfigTypeDef,
    },
)

MonitoringDatasetFormatOutputTypeDef = TypedDict(
    "MonitoringDatasetFormatOutputTypeDef",
    {
        "Csv": MonitoringCsvDatasetFormatOutputTypeDef,
        "Json": MonitoringJsonDatasetFormatOutputTypeDef,
        "Parquet": Dict[str, Any],
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

MonitoringOutputOutputTypeDef = TypedDict(
    "MonitoringOutputOutputTypeDef",
    {
        "S3Output": MonitoringS3OutputOutputTypeDef,
    },
)

MonitoringOutputTypeDef = TypedDict(
    "MonitoringOutputTypeDef",
    {
        "S3Output": MonitoringS3OutputTypeDef,
    },
)

OfflineStoreConfigOutputTypeDef = TypedDict(
    "OfflineStoreConfigOutputTypeDef",
    {
        "S3StorageConfig": S3StorageConfigOutputTypeDef,
        "DisableGlueTableCreation": bool,
        "DataCatalogConfig": DataCatalogConfigOutputTypeDef,
        "TableFormat": TableFormatType,
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


OnlineStoreConfigOutputTypeDef = TypedDict(
    "OnlineStoreConfigOutputTypeDef",
    {
        "SecurityConfig": OnlineStoreSecurityConfigOutputTypeDef,
        "EnableOnlineStore": bool,
        "TtlDuration": TtlDurationOutputTypeDef,
    },
)

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

OutputConfigOutputTypeDef = TypedDict(
    "OutputConfigOutputTypeDef",
    {
        "S3OutputLocation": str,
        "TargetDevice": TargetDeviceType,
        "TargetPlatform": TargetPlatformOutputTypeDef,
        "CompilerOptions": str,
        "KmsKeyId": str,
    },
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


PendingProductionVariantSummaryOutputTypeDef = TypedDict(
    "PendingProductionVariantSummaryOutputTypeDef",
    {
        "VariantName": str,
        "DeployedImages": List[DeployedImageOutputTypeDef],
        "CurrentWeight": float,
        "DesiredWeight": float,
        "CurrentInstanceCount": int,
        "DesiredInstanceCount": int,
        "InstanceType": ProductionVariantInstanceTypeType,
        "AcceleratorType": ProductionVariantAcceleratorTypeType,
        "VariantStatus": List[ProductionVariantStatusOutputTypeDef],
        "CurrentServerlessConfig": ProductionVariantServerlessConfigOutputTypeDef,
        "DesiredServerlessConfig": ProductionVariantServerlessConfigOutputTypeDef,
    },
)

ProductionVariantSummaryOutputTypeDef = TypedDict(
    "ProductionVariantSummaryOutputTypeDef",
    {
        "VariantName": str,
        "DeployedImages": List[DeployedImageOutputTypeDef],
        "CurrentWeight": float,
        "DesiredWeight": float,
        "CurrentInstanceCount": int,
        "DesiredInstanceCount": int,
        "VariantStatus": List[ProductionVariantStatusOutputTypeDef],
        "CurrentServerlessConfig": ProductionVariantServerlessConfigOutputTypeDef,
        "DesiredServerlessConfig": ProductionVariantServerlessConfigOutputTypeDef,
    },
)

TrafficPatternOutputTypeDef = TypedDict(
    "TrafficPatternOutputTypeDef",
    {
        "TrafficType": Literal["PHASES"],
        "Phases": List[PhaseOutputTypeDef],
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

ProcessingResourcesOutputTypeDef = TypedDict(
    "ProcessingResourcesOutputTypeDef",
    {
        "ClusterConfig": ProcessingClusterConfigOutputTypeDef,
    },
)

ProcessingResourcesTypeDef = TypedDict(
    "ProcessingResourcesTypeDef",
    {
        "ClusterConfig": ProcessingClusterConfigTypeDef,
    },
)

ProcessingOutputOutputTypeDef = TypedDict(
    "ProcessingOutputOutputTypeDef",
    {
        "OutputName": str,
        "S3Output": ProcessingS3OutputOutputTypeDef,
        "FeatureStoreOutput": ProcessingFeatureStoreOutputOutputTypeDef,
        "AppManaged": bool,
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


ProductionVariantOutputTypeDef = TypedDict(
    "ProductionVariantOutputTypeDef",
    {
        "VariantName": str,
        "ModelName": str,
        "InitialInstanceCount": int,
        "InstanceType": ProductionVariantInstanceTypeType,
        "InitialVariantWeight": float,
        "AcceleratorType": ProductionVariantAcceleratorTypeType,
        "CoreDumpConfig": ProductionVariantCoreDumpConfigOutputTypeDef,
        "ServerlessConfig": ProductionVariantServerlessConfigOutputTypeDef,
        "VolumeSizeInGB": int,
        "ModelDataDownloadTimeoutInSeconds": int,
        "ContainerStartupHealthCheckTimeoutInSeconds": int,
        "EnableSSMAccess": bool,
    },
)

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

ServiceCatalogProvisioningDetailsOutputTypeDef = TypedDict(
    "ServiceCatalogProvisioningDetailsOutputTypeDef",
    {
        "ProductId": str,
        "ProvisioningArtifactId": str,
        "PathId": str,
        "ProvisioningParameters": List[ProvisioningParameterOutputTypeDef],
    },
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

PublicWorkforceTaskPriceOutputTypeDef = TypedDict(
    "PublicWorkforceTaskPriceOutputTypeDef",
    {
        "AmountInUsd": USDOutputTypeDef,
    },
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

QueryLineageResponseOutputTypeDef = TypedDict(
    "QueryLineageResponseOutputTypeDef",
    {
        "Vertices": List[VertexOutputTypeDef],
        "Edges": List[EdgeOutputTypeDef],
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

RecommendationJobContainerConfigOutputTypeDef = TypedDict(
    "RecommendationJobContainerConfigOutputTypeDef",
    {
        "Domain": str,
        "Task": str,
        "Framework": str,
        "FrameworkVersion": str,
        "PayloadConfig": RecommendationJobPayloadConfigOutputTypeDef,
        "NearestModelName": str,
        "SupportedInstanceTypes": List[str],
        "DataInputConfig": str,
        "SupportedEndpointType": RecommendationJobSupportedEndpointTypeType,
    },
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


RenderUiTemplateResponseOutputTypeDef = TypedDict(
    "RenderUiTemplateResponseOutputTypeDef",
    {
        "RenderedContent": str,
        "Errors": List[RenderingErrorOutputTypeDef],
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


SelectiveExecutionConfigOutputTypeDef = TypedDict(
    "SelectiveExecutionConfigOutputTypeDef",
    {
        "SourcePipelineExecutionArn": str,
        "SelectedSteps": List[SelectedStepOutputTypeDef],
    },
)

SelectiveExecutionConfigTypeDef = TypedDict(
    "SelectiveExecutionConfigTypeDef",
    {
        "SourcePipelineExecutionArn": str,
        "SelectedSteps": Sequence[SelectedStepTypeDef],
    },
)

ShadowModeConfigOutputTypeDef = TypedDict(
    "ShadowModeConfigOutputTypeDef",
    {
        "SourceModelVariantName": str,
        "ShadowModelVariants": List[ShadowModelVariantConfigOutputTypeDef],
    },
)

ShadowModeConfigTypeDef = TypedDict(
    "ShadowModeConfigTypeDef",
    {
        "SourceModelVariantName": str,
        "ShadowModelVariants": Sequence[ShadowModelVariantConfigTypeDef],
    },
)

SourceAlgorithmSpecificationOutputTypeDef = TypedDict(
    "SourceAlgorithmSpecificationOutputTypeDef",
    {
        "SourceAlgorithms": List[SourceAlgorithmOutputTypeDef],
    },
)

SourceAlgorithmSpecificationTypeDef = TypedDict(
    "SourceAlgorithmSpecificationTypeDef",
    {
        "SourceAlgorithms": Sequence[SourceAlgorithmTypeDef],
    },
)

TimeSeriesForecastingJobConfigOutputTypeDef = TypedDict(
    "TimeSeriesForecastingJobConfigOutputTypeDef",
    {
        "FeatureSpecificationS3Uri": str,
        "CompletionCriteria": AutoMLJobCompletionCriteriaOutputTypeDef,
        "ForecastFrequency": str,
        "ForecastHorizon": int,
        "ForecastQuantiles": List[str],
        "Transformations": TimeSeriesTransformationsOutputTypeDef,
        "TimeSeriesConfig": TimeSeriesConfigOutputTypeDef,
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


TrainingImageConfigOutputTypeDef = TypedDict(
    "TrainingImageConfigOutputTypeDef",
    {
        "TrainingRepositoryAccessMode": TrainingRepositoryAccessModeType,
        "TrainingRepositoryAuthConfig": TrainingRepositoryAuthConfigOutputTypeDef,
    },
)

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


TransformDataSourceOutputTypeDef = TypedDict(
    "TransformDataSourceOutputTypeDef",
    {
        "S3DataSource": TransformS3DataSourceOutputTypeDef,
    },
)

TransformDataSourceTypeDef = TypedDict(
    "TransformDataSourceTypeDef",
    {
        "S3DataSource": TransformS3DataSourceTypeDef,
    },
)

WorkforceOutputTypeDef = TypedDict(
    "WorkforceOutputTypeDef",
    {
        "WorkforceName": str,
        "WorkforceArn": str,
        "LastUpdatedDate": datetime,
        "SourceIpConfig": SourceIpConfigOutputTypeDef,
        "SubDomain": str,
        "CognitoConfig": CognitoConfigOutputTypeDef,
        "OidcConfig": OidcConfigForResponseOutputTypeDef,
        "CreateDate": datetime,
        "WorkforceVpcConfig": WorkforceVpcConfigResponseOutputTypeDef,
        "Status": WorkforceStatusType,
        "FailureReason": str,
    },
)

ListActionsResponseOutputTypeDef = TypedDict(
    "ListActionsResponseOutputTypeDef",
    {
        "ActionSummaries": List[ActionSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ArtifactSummaryOutputTypeDef = TypedDict(
    "ArtifactSummaryOutputTypeDef",
    {
        "ArtifactArn": str,
        "ArtifactName": str,
        "Source": ArtifactSourceOutputTypeDef,
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

AsyncInferenceConfigOutputTypeDef = TypedDict(
    "AsyncInferenceConfigOutputTypeDef",
    {
        "ClientConfig": AsyncInferenceClientConfigOutputTypeDef,
        "OutputConfig": AsyncInferenceOutputConfigOutputTypeDef,
    },
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


TabularJobConfigOutputTypeDef = TypedDict(
    "TabularJobConfigOutputTypeDef",
    {
        "CandidateGenerationConfig": CandidateGenerationConfigOutputTypeDef,
        "CompletionCriteria": AutoMLJobCompletionCriteriaOutputTypeDef,
        "FeatureSpecificationS3Uri": str,
        "Mode": AutoMLModeType,
        "GenerateCandidateDefinitionsOnly": bool,
        "ProblemType": ProblemTypeType,
        "TargetAttributeName": str,
        "SampleWeightAttributeName": str,
    },
)

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


AutoMLChannelOutputTypeDef = TypedDict(
    "AutoMLChannelOutputTypeDef",
    {
        "DataSource": AutoMLDataSourceOutputTypeDef,
        "CompressionType": CompressionTypeType,
        "TargetAttributeName": str,
        "ContentType": str,
        "ChannelType": AutoMLChannelTypeType,
        "SampleWeightAttributeName": str,
    },
)

AutoMLJobChannelOutputTypeDef = TypedDict(
    "AutoMLJobChannelOutputTypeDef",
    {
        "ChannelType": AutoMLChannelTypeType,
        "ContentType": str,
        "CompressionType": CompressionTypeType,
        "DataSource": AutoMLDataSourceOutputTypeDef,
    },
)

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

ListAutoMLJobsResponseOutputTypeDef = TypedDict(
    "ListAutoMLJobsResponseOutputTypeDef",
    {
        "AutoMLJobSummaries": List[AutoMLJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoMLResolvedAttributesOutputTypeDef = TypedDict(
    "AutoMLResolvedAttributesOutputTypeDef",
    {
        "AutoMLJobObjective": AutoMLJobObjectiveOutputTypeDef,
        "CompletionCriteria": AutoMLJobCompletionCriteriaOutputTypeDef,
        "AutoMLProblemTypeResolvedAttributes": AutoMLProblemTypeResolvedAttributesOutputTypeDef,
    },
)

AutoMLJobConfigOutputTypeDef = TypedDict(
    "AutoMLJobConfigOutputTypeDef",
    {
        "CompletionCriteria": AutoMLJobCompletionCriteriaOutputTypeDef,
        "SecurityConfig": AutoMLSecurityConfigOutputTypeDef,
        "DataSplitConfig": AutoMLDataSplitConfigOutputTypeDef,
        "CandidateGenerationConfig": AutoMLCandidateGenerationConfigOutputTypeDef,
        "Mode": AutoMLModeType,
    },
)

LabelingJobAlgorithmsConfigOutputTypeDef = TypedDict(
    "LabelingJobAlgorithmsConfigOutputTypeDef",
    {
        "LabelingJobAlgorithmSpecificationArn": str,
        "InitialActiveLearningModelArn": str,
        "LabelingJobResourceConfig": LabelingJobResourceConfigOutputTypeDef,
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


ModelMetricsOutputTypeDef = TypedDict(
    "ModelMetricsOutputTypeDef",
    {
        "ModelQuality": ModelQualityOutputTypeDef,
        "ModelDataQuality": ModelDataQualityOutputTypeDef,
        "Bias": BiasOutputTypeDef,
        "Explainability": ExplainabilityOutputTypeDef,
    },
)

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

PipelineExecutionStepMetadataOutputTypeDef = TypedDict(
    "PipelineExecutionStepMetadataOutputTypeDef",
    {
        "TrainingJob": TrainingJobStepMetadataOutputTypeDef,
        "ProcessingJob": ProcessingJobStepMetadataOutputTypeDef,
        "TransformJob": TransformJobStepMetadataOutputTypeDef,
        "TuningJob": TuningJobStepMetaDataOutputTypeDef,
        "Model": ModelStepMetadataOutputTypeDef,
        "RegisterModel": RegisterModelStepMetadataOutputTypeDef,
        "Condition": ConditionStepMetadataOutputTypeDef,
        "Callback": CallbackStepMetadataOutputTypeDef,
        "Lambda": LambdaStepMetadataOutputTypeDef,
        "QualityCheck": QualityCheckStepMetadataOutputTypeDef,
        "ClarifyCheck": ClarifyCheckStepMetadataOutputTypeDef,
        "EMR": EMRStepMetadataOutputTypeDef,
        "Fail": FailStepMetadataOutputTypeDef,
        "AutoMLJob": AutoMLJobStepMetadataOutputTypeDef,
    },
)

AutoMLCandidateOutputTypeDef = TypedDict(
    "AutoMLCandidateOutputTypeDef",
    {
        "CandidateName": str,
        "FinalAutoMLJobObjectiveMetric": FinalAutoMLJobObjectiveMetricOutputTypeDef,
        "ObjectiveStatus": ObjectiveStatusType,
        "CandidateSteps": List[AutoMLCandidateStepOutputTypeDef],
        "CandidateStatus": CandidateStatusType,
        "InferenceContainers": List[AutoMLContainerDefinitionOutputTypeDef],
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "CandidateProperties": CandidatePropertiesOutputTypeDef,
        "InferenceContainerDefinitions": Dict[
            AutoMLProcessingUnitType, List[AutoMLContainerDefinitionOutputTypeDef]
        ],
    },
)

BlueGreenUpdatePolicyOutputTypeDef = TypedDict(
    "BlueGreenUpdatePolicyOutputTypeDef",
    {
        "TrafficRoutingConfiguration": TrafficRoutingConfigOutputTypeDef,
        "TerminationWaitInSeconds": int,
        "MaximumExecutionTimeoutInSeconds": int,
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


EndpointInputConfigurationOutputTypeDef = TypedDict(
    "EndpointInputConfigurationOutputTypeDef",
    {
        "InstanceType": ProductionVariantInstanceTypeType,
        "InferenceSpecificationName": str,
        "EnvironmentParameterRanges": EnvironmentParameterRangesOutputTypeDef,
        "ServerlessConfig": ProductionVariantServerlessConfigOutputTypeDef,
    },
)

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

ClarifyExplainerConfigOutputTypeDef = TypedDict(
    "ClarifyExplainerConfigOutputTypeDef",
    {
        "EnableExplanations": str,
        "InferenceConfig": ClarifyInferenceConfigOutputTypeDef,
        "ShapConfig": ClarifyShapConfigOutputTypeDef,
    },
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


ListCodeRepositoriesOutputOutputTypeDef = TypedDict(
    "ListCodeRepositoriesOutputOutputTypeDef",
    {
        "CodeRepositorySummaryList": List[CodeRepositorySummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListContextsResponseOutputTypeDef = TypedDict(
    "ListContextsResponseOutputTypeDef",
    {
        "ContextSummaries": List[ContextSummaryOutputTypeDef],
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

ChannelOutputTypeDef = TypedDict(
    "ChannelOutputTypeDef",
    {
        "ChannelName": str,
        "DataSource": DataSourceOutputTypeDef,
        "ContentType": str,
        "CompressionType": CompressionTypeType,
        "RecordWrapperType": RecordWrapperType,
        "InputMode": TrainingInputModeType,
        "ShuffleConfig": ShuffleConfigOutputTypeDef,
    },
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


ProcessingInputOutputTypeDef = TypedDict(
    "ProcessingInputOutputTypeDef",
    {
        "InputName": str,
        "AppManaged": bool,
        "S3Input": ProcessingS3InputOutputTypeDef,
        "DatasetDefinition": DatasetDefinitionOutputTypeDef,
    },
)

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


DescribeEdgeDeploymentPlanResponseOutputTypeDef = TypedDict(
    "DescribeEdgeDeploymentPlanResponseOutputTypeDef",
    {
        "EdgeDeploymentPlanArn": str,
        "EdgeDeploymentPlanName": str,
        "ModelConfigs": List[EdgeDeploymentModelConfigOutputTypeDef],
        "DeviceFleetName": str,
        "EdgeDeploymentSuccess": int,
        "EdgeDeploymentPending": int,
        "EdgeDeploymentFailed": int,
        "Stages": List[DeploymentStageStatusSummaryOutputTypeDef],
        "NextToken": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

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

DefaultSpaceSettingsOutputTypeDef = TypedDict(
    "DefaultSpaceSettingsOutputTypeDef",
    {
        "ExecutionRole": str,
        "SecurityGroups": List[str],
        "JupyterServerAppSettings": JupyterServerAppSettingsOutputTypeDef,
        "KernelGatewayAppSettings": KernelGatewayAppSettingsOutputTypeDef,
    },
)

SpaceSettingsOutputTypeDef = TypedDict(
    "SpaceSettingsOutputTypeDef",
    {
        "JupyterServerAppSettings": JupyterServerAppSettingsOutputTypeDef,
        "KernelGatewayAppSettings": KernelGatewayAppSettingsOutputTypeDef,
    },
)

DomainSettingsOutputTypeDef = TypedDict(
    "DomainSettingsOutputTypeDef",
    {
        "SecurityGroupIds": List[str],
        "RStudioServerProDomainSettings": RStudioServerProDomainSettingsOutputTypeDef,
        "ExecutionRoleIdentityConfig": ExecutionRoleIdentityConfigType,
    },
)

UserSettingsOutputTypeDef = TypedDict(
    "UserSettingsOutputTypeDef",
    {
        "ExecutionRole": str,
        "SecurityGroups": List[str],
        "SharingSettings": SharingSettingsOutputTypeDef,
        "JupyterServerAppSettings": JupyterServerAppSettingsOutputTypeDef,
        "KernelGatewayAppSettings": KernelGatewayAppSettingsOutputTypeDef,
        "TensorBoardAppSettings": TensorBoardAppSettingsOutputTypeDef,
        "RStudioServerProAppSettings": RStudioServerProAppSettingsOutputTypeDef,
        "RSessionAppSettings": RSessionAppSettingsOutputTypeDef,
        "CanvasAppSettings": CanvasAppSettingsOutputTypeDef,
    },
)

ListExperimentsResponseOutputTypeDef = TypedDict(
    "ListExperimentsResponseOutputTypeDef",
    {
        "ExperimentSummaries": List[ExperimentSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFeatureGroupsResponseOutputTypeDef = TypedDict(
    "ListFeatureGroupsResponseOutputTypeDef",
    {
        "FeatureGroupSummaries": List[FeatureGroupSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInferenceExperimentsResponseOutputTypeDef = TypedDict(
    "ListInferenceExperimentsResponseOutputTypeDef",
    {
        "InferenceExperiments": List[InferenceExperimentSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTrainingJobsResponseOutputTypeDef = TypedDict(
    "ListTrainingJobsResponseOutputTypeDef",
    {
        "TrainingJobSummaries": List[TrainingJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTrialsResponseOutputTypeDef = TypedDict(
    "ListTrialsResponseOutputTypeDef",
    {
        "TrialSummaries": List[TrialSummaryOutputTypeDef],
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

ListDevicesResponseOutputTypeDef = TypedDict(
    "ListDevicesResponseOutputTypeDef",
    {
        "DeviceSummaries": List[DeviceSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DriftCheckBaselinesOutputTypeDef = TypedDict(
    "DriftCheckBaselinesOutputTypeDef",
    {
        "Bias": DriftCheckBiasOutputTypeDef,
        "Explainability": DriftCheckExplainabilityOutputTypeDef,
        "ModelQuality": DriftCheckModelQualityOutputTypeDef,
        "ModelDataQuality": DriftCheckModelDataQualityOutputTypeDef,
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

InferenceRecommendationOutputTypeDef = TypedDict(
    "InferenceRecommendationOutputTypeDef",
    {
        "Metrics": RecommendationMetricsOutputTypeDef,
        "EndpointConfiguration": EndpointOutputConfigurationOutputTypeDef,
        "ModelConfiguration": ModelConfigurationOutputTypeDef,
        "RecommendationId": str,
        "InvocationEndTime": datetime,
        "InvocationStartTime": datetime,
    },
)

RecommendationJobInferenceBenchmarkOutputTypeDef = TypedDict(
    "RecommendationJobInferenceBenchmarkOutputTypeDef",
    {
        "Metrics": RecommendationMetricsOutputTypeDef,
        "EndpointConfiguration": EndpointOutputConfigurationOutputTypeDef,
        "ModelConfiguration": ModelConfigurationOutputTypeDef,
        "FailureReason": str,
        "EndpointMetrics": InferenceMetricsOutputTypeDef,
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

ListTrainingJobsForHyperParameterTuningJobResponseOutputTypeDef = TypedDict(
    "ListTrainingJobsForHyperParameterTuningJobResponseOutputTypeDef",
    {
        "TrainingJobSummaries": List[HyperParameterTrainingJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHyperParameterTuningJobsResponseOutputTypeDef = TypedDict(
    "ListHyperParameterTuningJobsResponseOutputTypeDef",
    {
        "HyperParameterTuningJobSummaries": List[HyperParameterTuningJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociationSummaryOutputTypeDef = TypedDict(
    "AssociationSummaryOutputTypeDef",
    {
        "SourceArn": str,
        "DestinationArn": str,
        "SourceType": str,
        "DestinationType": str,
        "AssociationType": AssociationEdgeTypeType,
        "SourceName": str,
        "DestinationName": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
    },
)

DescribeActionResponseOutputTypeDef = TypedDict(
    "DescribeActionResponseOutputTypeDef",
    {
        "ActionName": str,
        "ActionArn": str,
        "Source": ActionSourceOutputTypeDef,
        "ActionType": str,
        "Description": str,
        "Status": ActionStatusType,
        "Properties": Dict[str, str],
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "LineageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeArtifactResponseOutputTypeDef = TypedDict(
    "DescribeArtifactResponseOutputTypeDef",
    {
        "ArtifactName": str,
        "ArtifactArn": str,
        "Source": ArtifactSourceOutputTypeDef,
        "ArtifactType": str,
        "Properties": Dict[str, str],
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "LineageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeContextResponseOutputTypeDef = TypedDict(
    "DescribeContextResponseOutputTypeDef",
    {
        "ContextName": str,
        "ContextArn": str,
        "Source": ContextSourceOutputTypeDef,
        "ContextType": str,
        "Description": str,
        "Properties": Dict[str, str],
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "LineageGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeExperimentResponseOutputTypeDef = TypedDict(
    "DescribeExperimentResponseOutputTypeDef",
    {
        "ExperimentName": str,
        "ExperimentArn": str,
        "DisplayName": str,
        "Source": ExperimentSourceOutputTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeLineageGroupResponseOutputTypeDef = TypedDict(
    "DescribeLineageGroupResponseOutputTypeDef",
    {
        "LineageGroupName": str,
        "LineageGroupArn": str,
        "DisplayName": str,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelCardResponseOutputTypeDef = TypedDict(
    "DescribeModelCardResponseOutputTypeDef",
    {
        "ModelCardArn": str,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "Content": str,
        "ModelCardStatus": ModelCardStatusType,
        "SecurityConfig": ModelCardSecurityConfigOutputTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ModelCardProcessingStatus": ModelCardProcessingStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelPackageGroupOutputOutputTypeDef = TypedDict(
    "DescribeModelPackageGroupOutputOutputTypeDef",
    {
        "ModelPackageGroupName": str,
        "ModelPackageGroupArn": str,
        "ModelPackageGroupDescription": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "ModelPackageGroupStatus": ModelPackageGroupStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePipelineResponseOutputTypeDef = TypedDict(
    "DescribePipelineResponseOutputTypeDef",
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
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTrialComponentResponseOutputTypeDef = TypedDict(
    "DescribeTrialComponentResponseOutputTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "DisplayName": str,
        "Source": TrialComponentSourceOutputTypeDef,
        "Status": TrialComponentStatusOutputTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "Parameters": Dict[str, TrialComponentParameterValueOutputTypeDef],
        "InputArtifacts": Dict[str, TrialComponentArtifactOutputTypeDef],
        "OutputArtifacts": Dict[str, TrialComponentArtifactOutputTypeDef],
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "Metrics": List[TrialComponentMetricSummaryOutputTypeDef],
        "LineageGroupArn": str,
        "Sources": List[TrialComponentSourceOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTrialResponseOutputTypeDef = TypedDict(
    "DescribeTrialResponseOutputTypeDef",
    {
        "TrialName": str,
        "TrialArn": str,
        "DisplayName": str,
        "ExperimentName": str,
        "Source": TrialSourceOutputTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExperimentOutputTypeDef = TypedDict(
    "ExperimentOutputTypeDef",
    {
        "ExperimentName": str,
        "ExperimentArn": str,
        "DisplayName": str,
        "Source": ExperimentSourceOutputTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
    },
)

ModelCardOutputTypeDef = TypedDict(
    "ModelCardOutputTypeDef",
    {
        "ModelCardArn": str,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "Content": str,
        "ModelCardStatus": ModelCardStatusType,
        "SecurityConfig": ModelCardSecurityConfigOutputTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
        "ModelId": str,
        "RiskRating": str,
        "ModelPackageGroupName": str,
    },
)

ModelDashboardModelCardOutputTypeDef = TypedDict(
    "ModelDashboardModelCardOutputTypeDef",
    {
        "ModelCardArn": str,
        "ModelCardName": str,
        "ModelCardVersion": int,
        "ModelCardStatus": ModelCardStatusType,
        "SecurityConfig": ModelCardSecurityConfigOutputTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
        "ModelId": str,
        "RiskRating": str,
    },
)

ModelPackageGroupOutputTypeDef = TypedDict(
    "ModelPackageGroupOutputTypeDef",
    {
        "ModelPackageGroupName": str,
        "ModelPackageGroupArn": str,
        "ModelPackageGroupDescription": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "ModelPackageGroupStatus": ModelPackageGroupStatusType,
        "Tags": List[TagOutputTypeDef],
    },
)

PipelineOutputTypeDef = TypedDict(
    "PipelineOutputTypeDef",
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
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
    },
)

TrialComponentSimpleSummaryOutputTypeDef = TypedDict(
    "TrialComponentSimpleSummaryOutputTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "TrialComponentSource": TrialComponentSourceOutputTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
    },
)

TrialComponentSummaryOutputTypeDef = TypedDict(
    "TrialComponentSummaryOutputTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "DisplayName": str,
        "TrialComponentSource": TrialComponentSourceOutputTypeDef,
        "Status": TrialComponentStatusOutputTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
    },
)

HyperParameterTuningJobConfigOutputTypeDef = TypedDict(
    "HyperParameterTuningJobConfigOutputTypeDef",
    {
        "Strategy": HyperParameterTuningJobStrategyTypeType,
        "StrategyConfig": HyperParameterTuningJobStrategyConfigOutputTypeDef,
        "HyperParameterTuningJobObjective": HyperParameterTuningJobObjectiveOutputTypeDef,
        "ResourceLimits": ResourceLimitsOutputTypeDef,
        "ParameterRanges": ParameterRangesOutputTypeDef,
        "TrainingJobEarlyStoppingType": TrainingJobEarlyStoppingTypeType,
        "TuningJobCompletionCriteria": TuningJobCompletionCriteriaOutputTypeDef,
        "RandomSeed": int,
    },
)

HyperParameterSpecificationOutputTypeDef = TypedDict(
    "HyperParameterSpecificationOutputTypeDef",
    {
        "Name": str,
        "Description": str,
        "Type": ParameterTypeType,
        "Range": ParameterRangeOutputTypeDef,
        "IsTunable": bool,
        "IsRequired": bool,
        "DefaultValue": str,
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


AppImageConfigDetailsOutputTypeDef = TypedDict(
    "AppImageConfigDetailsOutputTypeDef",
    {
        "AppImageConfigArn": str,
        "AppImageConfigName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "KernelGatewayImageConfig": KernelGatewayImageConfigOutputTypeDef,
    },
)

DescribeAppImageConfigResponseOutputTypeDef = TypedDict(
    "DescribeAppImageConfigResponseOutputTypeDef",
    {
        "AppImageConfigArn": str,
        "AppImageConfigName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "KernelGatewayImageConfig": KernelGatewayImageConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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


ListLabelingJobsForWorkteamResponseOutputTypeDef = TypedDict(
    "ListLabelingJobsForWorkteamResponseOutputTypeDef",
    {
        "LabelingJobSummaryList": List[LabelingJobForWorkteamSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LabelingJobInputConfigOutputTypeDef = TypedDict(
    "LabelingJobInputConfigOutputTypeDef",
    {
        "DataSource": LabelingJobDataSourceOutputTypeDef,
        "DataAttributes": LabelingJobDataAttributesOutputTypeDef,
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


WorkteamOutputTypeDef = TypedDict(
    "WorkteamOutputTypeDef",
    {
        "WorkteamName": str,
        "MemberDefinitions": List[MemberDefinitionOutputTypeDef],
        "WorkteamArn": str,
        "WorkforceArn": str,
        "ProductListingIds": List[str],
        "Description": str,
        "SubDomain": str,
        "CreateDate": datetime,
        "LastUpdatedDate": datetime,
        "NotificationConfiguration": NotificationConfigurationOutputTypeDef,
    },
)

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


MonitoringAlertSummaryOutputTypeDef = TypedDict(
    "MonitoringAlertSummaryOutputTypeDef",
    {
        "MonitoringAlertName": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "AlertStatus": MonitoringAlertStatusType,
        "DatapointsToAlert": int,
        "EvaluationPeriod": int,
        "Actions": MonitoringAlertActionsOutputTypeDef,
    },
)

ContainerDefinitionOutputTypeDef = TypedDict(
    "ContainerDefinitionOutputTypeDef",
    {
        "ContainerHostname": str,
        "Image": str,
        "ImageConfig": ImageConfigOutputTypeDef,
        "Mode": ContainerModeType,
        "ModelDataUrl": str,
        "Environment": Dict[str, str],
        "ModelPackageName": str,
        "InferenceSpecificationName": str,
        "MultiModelConfig": MultiModelConfigOutputTypeDef,
        "ModelDataSource": ModelDataSourceOutputTypeDef,
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

ModelVariantConfigSummaryOutputTypeDef = TypedDict(
    "ModelVariantConfigSummaryOutputTypeDef",
    {
        "ModelName": str,
        "VariantName": str,
        "InfrastructureConfig": ModelInfrastructureConfigOutputTypeDef,
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

AdditionalInferenceSpecificationDefinitionOutputTypeDef = TypedDict(
    "AdditionalInferenceSpecificationDefinitionOutputTypeDef",
    {
        "Name": str,
        "Description": str,
        "Containers": List[ModelPackageContainerDefinitionOutputTypeDef],
        "SupportedTransformInstanceTypes": List[TransformInstanceTypeType],
        "SupportedRealtimeInferenceInstanceTypes": List[ProductionVariantInstanceTypeType],
        "SupportedContentTypes": List[str],
        "SupportedResponseMIMETypes": List[str],
    },
)

InferenceSpecificationOutputTypeDef = TypedDict(
    "InferenceSpecificationOutputTypeDef",
    {
        "Containers": List[ModelPackageContainerDefinitionOutputTypeDef],
        "SupportedTransformInstanceTypes": List[TransformInstanceTypeType],
        "SupportedRealtimeInferenceInstanceTypes": List[ProductionVariantInstanceTypeType],
        "SupportedContentTypes": List[str],
        "SupportedResponseMIMETypes": List[str],
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


_RequiredInferenceSpecificationTypeDef = TypedDict(
    "_RequiredInferenceSpecificationTypeDef",
    {
        "Containers": Sequence[ModelPackageContainerDefinitionTypeDef],
        "SupportedContentTypes": Sequence[str],
        "SupportedResponseMIMETypes": Sequence[str],
    },
)
_OptionalInferenceSpecificationTypeDef = TypedDict(
    "_OptionalInferenceSpecificationTypeDef",
    {
        "SupportedTransformInstanceTypes": Sequence[TransformInstanceTypeType],
        "SupportedRealtimeInferenceInstanceTypes": Sequence[ProductionVariantInstanceTypeType],
    },
    total=False,
)


class InferenceSpecificationTypeDef(
    _RequiredInferenceSpecificationTypeDef, _OptionalInferenceSpecificationTypeDef
):
    pass


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

BatchTransformInputOutputTypeDef = TypedDict(
    "BatchTransformInputOutputTypeDef",
    {
        "DataCapturedDestinationS3Uri": str,
        "DatasetFormat": MonitoringDatasetFormatOutputTypeDef,
        "LocalPath": str,
        "S3InputMode": ProcessingS3InputModeType,
        "S3DataDistributionType": ProcessingS3DataDistributionTypeType,
        "FeaturesAttribute": str,
        "InferenceAttribute": str,
        "ProbabilityAttribute": str,
        "ProbabilityThresholdAttribute": float,
        "StartTimeOffset": str,
        "EndTimeOffset": str,
    },
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


MonitoringOutputConfigOutputTypeDef = TypedDict(
    "MonitoringOutputConfigOutputTypeDef",
    {
        "MonitoringOutputs": List[MonitoringOutputOutputTypeDef],
        "KmsKeyId": str,
    },
)

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


DescribeFeatureGroupResponseOutputTypeDef = TypedDict(
    "DescribeFeatureGroupResponseOutputTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "RecordIdentifierFeatureName": str,
        "EventTimeFeatureName": str,
        "FeatureDefinitions": List[FeatureDefinitionOutputTypeDef],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "OnlineStoreConfig": OnlineStoreConfigOutputTypeDef,
        "OfflineStoreConfig": OfflineStoreConfigOutputTypeDef,
        "RoleArn": str,
        "FeatureGroupStatus": FeatureGroupStatusType,
        "OfflineStoreStatus": OfflineStoreStatusOutputTypeDef,
        "LastUpdateStatus": LastUpdateStatusOutputTypeDef,
        "FailureReason": str,
        "Description": str,
        "NextToken": str,
        "OnlineStoreTotalSizeBytes": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FeatureGroupOutputTypeDef = TypedDict(
    "FeatureGroupOutputTypeDef",
    {
        "FeatureGroupArn": str,
        "FeatureGroupName": str,
        "RecordIdentifierFeatureName": str,
        "EventTimeFeatureName": str,
        "FeatureDefinitions": List[FeatureDefinitionOutputTypeDef],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "OnlineStoreConfig": OnlineStoreConfigOutputTypeDef,
        "OfflineStoreConfig": OfflineStoreConfigOutputTypeDef,
        "RoleArn": str,
        "FeatureGroupStatus": FeatureGroupStatusType,
        "OfflineStoreStatus": OfflineStoreStatusOutputTypeDef,
        "LastUpdateStatus": LastUpdateStatusOutputTypeDef,
        "FailureReason": str,
        "Description": str,
        "Tags": List[TagOutputTypeDef],
    },
)

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


DescribeCompilationJobResponseOutputTypeDef = TypedDict(
    "DescribeCompilationJobResponseOutputTypeDef",
    {
        "CompilationJobName": str,
        "CompilationJobArn": str,
        "CompilationJobStatus": CompilationJobStatusType,
        "CompilationStartTime": datetime,
        "CompilationEndTime": datetime,
        "StoppingCondition": StoppingConditionOutputTypeDef,
        "InferenceImage": str,
        "ModelPackageVersionArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "ModelArtifacts": ModelArtifactsOutputTypeDef,
        "ModelDigests": ModelDigestsOutputTypeDef,
        "RoleArn": str,
        "InputConfig": InputConfigOutputTypeDef,
        "OutputConfig": OutputConfigOutputTypeDef,
        "VpcConfig": NeoVpcConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

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


PendingDeploymentSummaryOutputTypeDef = TypedDict(
    "PendingDeploymentSummaryOutputTypeDef",
    {
        "EndpointConfigName": str,
        "ProductionVariants": List[PendingProductionVariantSummaryOutputTypeDef],
        "StartTime": datetime,
        "ShadowProductionVariants": List[PendingProductionVariantSummaryOutputTypeDef],
    },
)

ProcessingOutputConfigOutputTypeDef = TypedDict(
    "ProcessingOutputConfigOutputTypeDef",
    {
        "Outputs": List[ProcessingOutputOutputTypeDef],
        "KmsKeyId": str,
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


DescribeProjectOutputOutputTypeDef = TypedDict(
    "DescribeProjectOutputOutputTypeDef",
    {
        "ProjectArn": str,
        "ProjectName": str,
        "ProjectId": str,
        "ProjectDescription": str,
        "ServiceCatalogProvisioningDetails": ServiceCatalogProvisioningDetailsOutputTypeDef,
        "ServiceCatalogProvisionedProductDetails": (
            ServiceCatalogProvisionedProductDetailsOutputTypeDef
        ),
        "ProjectStatus": ProjectStatusType,
        "CreatedBy": UserContextOutputTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ProjectOutputTypeDef = TypedDict(
    "ProjectOutputTypeDef",
    {
        "ProjectArn": str,
        "ProjectName": str,
        "ProjectId": str,
        "ProjectDescription": str,
        "ServiceCatalogProvisioningDetails": ServiceCatalogProvisioningDetailsOutputTypeDef,
        "ServiceCatalogProvisionedProductDetails": (
            ServiceCatalogProvisionedProductDetailsOutputTypeDef
        ),
        "ProjectStatus": ProjectStatusType,
        "CreatedBy": UserContextOutputTypeDef,
        "CreationTime": datetime,
        "Tags": List[TagOutputTypeDef],
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
    },
)

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


HumanLoopConfigOutputTypeDef = TypedDict(
    "HumanLoopConfigOutputTypeDef",
    {
        "WorkteamArn": str,
        "HumanTaskUiArn": str,
        "TaskTitle": str,
        "TaskDescription": str,
        "TaskCount": int,
        "TaskAvailabilityLifetimeInSeconds": int,
        "TaskTimeLimitInSeconds": int,
        "TaskKeywords": List[str],
        "PublicWorkforceTaskPrice": PublicWorkforceTaskPriceOutputTypeDef,
    },
)

HumanTaskConfigOutputTypeDef = TypedDict(
    "HumanTaskConfigOutputTypeDef",
    {
        "WorkteamArn": str,
        "UiConfig": UiConfigOutputTypeDef,
        "PreHumanTaskLambdaArn": str,
        "TaskKeywords": List[str],
        "TaskTitle": str,
        "TaskDescription": str,
        "NumberOfHumanWorkersPerDataObject": int,
        "TaskTimeLimitInSeconds": int,
        "TaskAvailabilityLifetimeInSeconds": int,
        "MaxConcurrentTaskCount": int,
        "AnnotationConsolidationConfig": AnnotationConsolidationConfigOutputTypeDef,
        "PublicWorkforceTaskPrice": PublicWorkforceTaskPriceOutputTypeDef,
    },
)

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


DescribePipelineExecutionResponseOutputTypeDef = TypedDict(
    "DescribePipelineExecutionResponseOutputTypeDef",
    {
        "PipelineArn": str,
        "PipelineExecutionArn": str,
        "PipelineExecutionDisplayName": str,
        "PipelineExecutionStatus": PipelineExecutionStatusType,
        "PipelineExecutionDescription": str,
        "PipelineExperimentConfig": PipelineExperimentConfigOutputTypeDef,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationOutputTypeDef,
        "SelectiveExecutionConfig": SelectiveExecutionConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PipelineExecutionOutputTypeDef = TypedDict(
    "PipelineExecutionOutputTypeDef",
    {
        "PipelineArn": str,
        "PipelineExecutionArn": str,
        "PipelineExecutionDisplayName": str,
        "PipelineExecutionStatus": PipelineExecutionStatusType,
        "PipelineExecutionDescription": str,
        "PipelineExperimentConfig": PipelineExperimentConfigOutputTypeDef,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationOutputTypeDef,
        "PipelineParameters": List[ParameterOutputTypeDef],
        "SelectiveExecutionConfig": SelectiveExecutionConfigOutputTypeDef,
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


AlgorithmSpecificationOutputTypeDef = TypedDict(
    "AlgorithmSpecificationOutputTypeDef",
    {
        "TrainingImage": str,
        "AlgorithmName": str,
        "TrainingInputMode": TrainingInputModeType,
        "MetricDefinitions": List[MetricDefinitionOutputTypeDef],
        "EnableSageMakerMetricsTimeSeries": bool,
        "ContainerEntrypoint": List[str],
        "ContainerArguments": List[str],
        "TrainingImageConfig": TrainingImageConfigOutputTypeDef,
    },
)

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


TransformInputOutputTypeDef = TypedDict(
    "TransformInputOutputTypeDef",
    {
        "DataSource": TransformDataSourceOutputTypeDef,
        "ContentType": str,
        "CompressionType": CompressionTypeType,
        "SplitType": SplitTypeType,
    },
)

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


DescribeWorkforceResponseOutputTypeDef = TypedDict(
    "DescribeWorkforceResponseOutputTypeDef",
    {
        "Workforce": WorkforceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWorkforcesResponseOutputTypeDef = TypedDict(
    "ListWorkforcesResponseOutputTypeDef",
    {
        "Workforces": List[WorkforceOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateWorkforceResponseOutputTypeDef = TypedDict(
    "UpdateWorkforceResponseOutputTypeDef",
    {
        "Workforce": WorkforceOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListArtifactsResponseOutputTypeDef = TypedDict(
    "ListArtifactsResponseOutputTypeDef",
    {
        "ArtifactSummaries": List[ArtifactSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoMLProblemTypeConfigOutputTypeDef = TypedDict(
    "AutoMLProblemTypeConfigOutputTypeDef",
    {
        "ImageClassificationJobConfig": ImageClassificationJobConfigOutputTypeDef,
        "TextClassificationJobConfig": TextClassificationJobConfigOutputTypeDef,
        "TabularJobConfig": TabularJobConfigOutputTypeDef,
        "TimeSeriesForecastingJobConfig": TimeSeriesForecastingJobConfigOutputTypeDef,
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


PipelineExecutionStepOutputTypeDef = TypedDict(
    "PipelineExecutionStepOutputTypeDef",
    {
        "StepName": str,
        "StepDisplayName": str,
        "StepDescription": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "StepStatus": StepStatusType,
        "CacheHitResult": CacheHitResultOutputTypeDef,
        "AttemptCount": int,
        "FailureReason": str,
        "Metadata": PipelineExecutionStepMetadataOutputTypeDef,
        "SelectiveExecutionResult": SelectiveExecutionResultOutputTypeDef,
    },
)

DescribeAutoMLJobResponseOutputTypeDef = TypedDict(
    "DescribeAutoMLJobResponseOutputTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "InputDataConfig": List[AutoMLChannelOutputTypeDef],
        "OutputDataConfig": AutoMLOutputDataConfigOutputTypeDef,
        "RoleArn": str,
        "AutoMLJobObjective": AutoMLJobObjectiveOutputTypeDef,
        "ProblemType": ProblemTypeType,
        "AutoMLJobConfig": AutoMLJobConfigOutputTypeDef,
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "PartialFailureReasons": List[AutoMLPartialFailureReasonOutputTypeDef],
        "BestCandidate": AutoMLCandidateOutputTypeDef,
        "AutoMLJobStatus": AutoMLJobStatusType,
        "AutoMLJobSecondaryStatus": AutoMLJobSecondaryStatusType,
        "GenerateCandidateDefinitionsOnly": bool,
        "AutoMLJobArtifacts": AutoMLJobArtifactsOutputTypeDef,
        "ResolvedAttributes": ResolvedAttributesOutputTypeDef,
        "ModelDeployConfig": ModelDeployConfigOutputTypeDef,
        "ModelDeployResult": ModelDeployResultOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCandidatesForAutoMLJobResponseOutputTypeDef = TypedDict(
    "ListCandidatesForAutoMLJobResponseOutputTypeDef",
    {
        "Candidates": List[AutoMLCandidateOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeploymentConfigOutputTypeDef = TypedDict(
    "DeploymentConfigOutputTypeDef",
    {
        "BlueGreenUpdatePolicy": BlueGreenUpdatePolicyOutputTypeDef,
        "AutoRollbackConfiguration": AutoRollbackConfigOutputTypeDef,
        "RollingUpdatePolicy": RollingUpdatePolicyOutputTypeDef,
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

RecommendationJobInputConfigOutputTypeDef = TypedDict(
    "RecommendationJobInputConfigOutputTypeDef",
    {
        "ModelPackageVersionArn": str,
        "JobDurationInSeconds": int,
        "TrafficPattern": TrafficPatternOutputTypeDef,
        "ResourceLimit": RecommendationJobResourceLimitOutputTypeDef,
        "EndpointConfigurations": List[EndpointInputConfigurationOutputTypeDef],
        "VolumeKmsKeyId": str,
        "ContainerConfig": RecommendationJobContainerConfigOutputTypeDef,
        "Endpoints": List[EndpointInfoOutputTypeDef],
        "VpcConfig": RecommendationJobVpcConfigOutputTypeDef,
        "ModelName": str,
    },
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

ExplainerConfigOutputTypeDef = TypedDict(
    "ExplainerConfigOutputTypeDef",
    {
        "ClarifyExplainerConfig": ClarifyExplainerConfigOutputTypeDef,
    },
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


HyperParameterTrainingJobDefinitionOutputTypeDef = TypedDict(
    "HyperParameterTrainingJobDefinitionOutputTypeDef",
    {
        "DefinitionName": str,
        "TuningObjective": HyperParameterTuningJobObjectiveOutputTypeDef,
        "HyperParameterRanges": ParameterRangesOutputTypeDef,
        "StaticHyperParameters": Dict[str, str],
        "AlgorithmSpecification": HyperParameterAlgorithmSpecificationOutputTypeDef,
        "RoleArn": str,
        "InputDataConfig": List[ChannelOutputTypeDef],
        "VpcConfig": VpcConfigOutputTypeDef,
        "OutputDataConfig": OutputDataConfigOutputTypeDef,
        "ResourceConfig": ResourceConfigOutputTypeDef,
        "StoppingCondition": StoppingConditionOutputTypeDef,
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigOutputTypeDef,
        "RetryStrategy": RetryStrategyOutputTypeDef,
        "HyperParameterTuningResourceConfig": HyperParameterTuningResourceConfigOutputTypeDef,
        "Environment": Dict[str, str],
    },
)

TrainingJobDefinitionOutputTypeDef = TypedDict(
    "TrainingJobDefinitionOutputTypeDef",
    {
        "TrainingInputMode": TrainingInputModeType,
        "HyperParameters": Dict[str, str],
        "InputDataConfig": List[ChannelOutputTypeDef],
        "OutputDataConfig": OutputDataConfigOutputTypeDef,
        "ResourceConfig": ResourceConfigOutputTypeDef,
        "StoppingCondition": StoppingConditionOutputTypeDef,
    },
)

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


DescribeSpaceResponseOutputTypeDef = TypedDict(
    "DescribeSpaceResponseOutputTypeDef",
    {
        "DomainId": str,
        "SpaceArn": str,
        "SpaceName": str,
        "HomeEfsFileSystemUid": str,
        "Status": SpaceStatusType,
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "FailureReason": str,
        "SpaceSettings": SpaceSettingsOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDomainResponseOutputTypeDef = TypedDict(
    "DescribeDomainResponseOutputTypeDef",
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
        "DefaultUserSettings": UserSettingsOutputTypeDef,
        "AppNetworkAccessType": AppNetworkAccessTypeType,
        "HomeEfsFileSystemKmsKeyId": str,
        "SubnetIds": List[str],
        "Url": str,
        "VpcId": str,
        "KmsKeyId": str,
        "DomainSettings": DomainSettingsOutputTypeDef,
        "AppSecurityGroupManagement": AppSecurityGroupManagementType,
        "SecurityGroupIdForDomainBoundary": str,
        "DefaultSpaceSettings": DefaultSpaceSettingsOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeUserProfileResponseOutputTypeDef = TypedDict(
    "DescribeUserProfileResponseOutputTypeDef",
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
        "UserSettings": UserSettingsOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InferenceRecommendationsJobStepOutputTypeDef = TypedDict(
    "InferenceRecommendationsJobStepOutputTypeDef",
    {
        "StepType": Literal["BENCHMARK"],
        "JobName": str,
        "Status": RecommendationJobStatusType,
        "InferenceBenchmark": RecommendationJobInferenceBenchmarkOutputTypeDef,
    },
)

ListAssociationsResponseOutputTypeDef = TypedDict(
    "ListAssociationsResponseOutputTypeDef",
    {
        "AssociationSummaries": List[AssociationSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TrialOutputTypeDef = TypedDict(
    "TrialOutputTypeDef",
    {
        "TrialName": str,
        "TrialArn": str,
        "DisplayName": str,
        "ExperimentName": str,
        "Source": TrialSourceOutputTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
        "TrialComponentSummaries": List[TrialComponentSimpleSummaryOutputTypeDef],
    },
)

ListTrialComponentsResponseOutputTypeDef = TypedDict(
    "ListTrialComponentsResponseOutputTypeDef",
    {
        "TrialComponentSummaries": List[TrialComponentSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TrainingSpecificationOutputTypeDef = TypedDict(
    "TrainingSpecificationOutputTypeDef",
    {
        "TrainingImage": str,
        "TrainingImageDigest": str,
        "SupportedHyperParameters": List[HyperParameterSpecificationOutputTypeDef],
        "SupportedTrainingInstanceTypes": List[TrainingInstanceTypeType],
        "SupportsDistributedTraining": bool,
        "MetricDefinitions": List[MetricDefinitionOutputTypeDef],
        "TrainingChannels": List[ChannelSpecificationOutputTypeDef],
        "SupportedTuningJobObjectiveMetrics": List[HyperParameterTuningJobObjectiveOutputTypeDef],
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


ListAppImageConfigsResponseOutputTypeDef = TypedDict(
    "ListAppImageConfigsResponseOutputTypeDef",
    {
        "NextToken": str,
        "AppImageConfigs": List[AppImageConfigDetailsOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LabelingJobSummaryOutputTypeDef = TypedDict(
    "LabelingJobSummaryOutputTypeDef",
    {
        "LabelingJobName": str,
        "LabelingJobArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LabelingJobStatus": LabelingJobStatusType,
        "LabelCounters": LabelCountersOutputTypeDef,
        "WorkteamArn": str,
        "PreHumanTaskLambdaArn": str,
        "AnnotationConsolidationLambdaArn": str,
        "FailureReason": str,
        "LabelingJobOutput": LabelingJobOutputOutputTypeDef,
        "InputConfig": LabelingJobInputConfigOutputTypeDef,
    },
)

DescribeWorkteamResponseOutputTypeDef = TypedDict(
    "DescribeWorkteamResponseOutputTypeDef",
    {
        "Workteam": WorkteamOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWorkteamsResponseOutputTypeDef = TypedDict(
    "ListWorkteamsResponseOutputTypeDef",
    {
        "Workteams": List[WorkteamOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateWorkteamResponseOutputTypeDef = TypedDict(
    "UpdateWorkteamResponseOutputTypeDef",
    {
        "Workteam": WorkteamOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMonitoringAlertsResponseOutputTypeDef = TypedDict(
    "ListMonitoringAlertsResponseOutputTypeDef",
    {
        "MonitoringAlertSummaries": List[MonitoringAlertSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelOutputOutputTypeDef = TypedDict(
    "DescribeModelOutputOutputTypeDef",
    {
        "ModelName": str,
        "PrimaryContainer": ContainerDefinitionOutputTypeDef,
        "Containers": List[ContainerDefinitionOutputTypeDef],
        "InferenceExecutionConfig": InferenceExecutionConfigOutputTypeDef,
        "ExecutionRoleArn": str,
        "VpcConfig": VpcConfigOutputTypeDef,
        "CreationTime": datetime,
        "ModelArn": str,
        "EnableNetworkIsolation": bool,
        "DeploymentRecommendation": DeploymentRecommendationOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelOutputTypeDef = TypedDict(
    "ModelOutputTypeDef",
    {
        "ModelName": str,
        "PrimaryContainer": ContainerDefinitionOutputTypeDef,
        "Containers": List[ContainerDefinitionOutputTypeDef],
        "InferenceExecutionConfig": InferenceExecutionConfigOutputTypeDef,
        "ExecutionRoleArn": str,
        "VpcConfig": VpcConfigOutputTypeDef,
        "CreationTime": datetime,
        "ModelArn": str,
        "EnableNetworkIsolation": bool,
        "Tags": List[TagOutputTypeDef],
        "DeploymentRecommendation": DeploymentRecommendationOutputTypeDef,
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


DescribeInferenceExperimentResponseOutputTypeDef = TypedDict(
    "DescribeInferenceExperimentResponseOutputTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Schedule": InferenceExperimentScheduleOutputTypeDef,
        "Status": InferenceExperimentStatusType,
        "StatusReason": str,
        "Description": str,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
        "EndpointMetadata": EndpointMetadataOutputTypeDef,
        "ModelVariants": List[ModelVariantConfigSummaryOutputTypeDef],
        "DataStorageConfig": InferenceExperimentDataStorageConfigOutputTypeDef,
        "ShadowModeConfig": ShadowModeConfigOutputTypeDef,
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


BatchDescribeModelPackageSummaryOutputTypeDef = TypedDict(
    "BatchDescribeModelPackageSummaryOutputTypeDef",
    {
        "ModelPackageGroupName": str,
        "ModelPackageVersion": int,
        "ModelPackageArn": str,
        "ModelPackageDescription": str,
        "CreationTime": datetime,
        "InferenceSpecification": InferenceSpecificationOutputTypeDef,
        "ModelPackageStatus": ModelPackageStatusType,
        "ModelApprovalStatus": ModelApprovalStatusType,
    },
)

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


DataQualityJobInputOutputTypeDef = TypedDict(
    "DataQualityJobInputOutputTypeDef",
    {
        "EndpointInput": EndpointInputOutputTypeDef,
        "BatchTransformInput": BatchTransformInputOutputTypeDef,
    },
)

ModelBiasJobInputOutputTypeDef = TypedDict(
    "ModelBiasJobInputOutputTypeDef",
    {
        "EndpointInput": EndpointInputOutputTypeDef,
        "BatchTransformInput": BatchTransformInputOutputTypeDef,
        "GroundTruthS3Input": MonitoringGroundTruthS3InputOutputTypeDef,
    },
)

ModelExplainabilityJobInputOutputTypeDef = TypedDict(
    "ModelExplainabilityJobInputOutputTypeDef",
    {
        "EndpointInput": EndpointInputOutputTypeDef,
        "BatchTransformInput": BatchTransformInputOutputTypeDef,
    },
)

ModelQualityJobInputOutputTypeDef = TypedDict(
    "ModelQualityJobInputOutputTypeDef",
    {
        "EndpointInput": EndpointInputOutputTypeDef,
        "BatchTransformInput": BatchTransformInputOutputTypeDef,
        "GroundTruthS3Input": MonitoringGroundTruthS3InputOutputTypeDef,
    },
)

MonitoringInputOutputTypeDef = TypedDict(
    "MonitoringInputOutputTypeDef",
    {
        "EndpointInput": EndpointInputOutputTypeDef,
        "BatchTransformInput": BatchTransformInputOutputTypeDef,
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

DescribeProcessingJobResponseOutputTypeDef = TypedDict(
    "DescribeProcessingJobResponseOutputTypeDef",
    {
        "ProcessingInputs": List[ProcessingInputOutputTypeDef],
        "ProcessingOutputConfig": ProcessingOutputConfigOutputTypeDef,
        "ProcessingJobName": str,
        "ProcessingResources": ProcessingResourcesOutputTypeDef,
        "StoppingCondition": ProcessingStoppingConditionOutputTypeDef,
        "AppSpecification": AppSpecificationOutputTypeDef,
        "Environment": Dict[str, str],
        "NetworkConfig": NetworkConfigOutputTypeDef,
        "RoleArn": str,
        "ExperimentConfig": ExperimentConfigOutputTypeDef,
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

ProcessingJobOutputTypeDef = TypedDict(
    "ProcessingJobOutputTypeDef",
    {
        "ProcessingInputs": List[ProcessingInputOutputTypeDef],
        "ProcessingOutputConfig": ProcessingOutputConfigOutputTypeDef,
        "ProcessingJobName": str,
        "ProcessingResources": ProcessingResourcesOutputTypeDef,
        "StoppingCondition": ProcessingStoppingConditionOutputTypeDef,
        "AppSpecification": AppSpecificationOutputTypeDef,
        "Environment": Dict[str, str],
        "NetworkConfig": NetworkConfigOutputTypeDef,
        "RoleArn": str,
        "ExperimentConfig": ExperimentConfigOutputTypeDef,
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
        "Tags": List[TagOutputTypeDef],
    },
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


DescribeFlowDefinitionResponseOutputTypeDef = TypedDict(
    "DescribeFlowDefinitionResponseOutputTypeDef",
    {
        "FlowDefinitionArn": str,
        "FlowDefinitionName": str,
        "FlowDefinitionStatus": FlowDefinitionStatusType,
        "CreationTime": datetime,
        "HumanLoopRequestSource": HumanLoopRequestSourceOutputTypeDef,
        "HumanLoopActivationConfig": HumanLoopActivationConfigOutputTypeDef,
        "HumanLoopConfig": HumanLoopConfigOutputTypeDef,
        "OutputConfig": FlowDefinitionOutputConfigOutputTypeDef,
        "RoleArn": str,
        "FailureReason": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeLabelingJobResponseOutputTypeDef = TypedDict(
    "DescribeLabelingJobResponseOutputTypeDef",
    {
        "LabelingJobStatus": LabelingJobStatusType,
        "LabelCounters": LabelCountersOutputTypeDef,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "JobReferenceCode": str,
        "LabelingJobName": str,
        "LabelingJobArn": str,
        "LabelAttributeName": str,
        "InputConfig": LabelingJobInputConfigOutputTypeDef,
        "OutputConfig": LabelingJobOutputConfigOutputTypeDef,
        "RoleArn": str,
        "LabelCategoryConfigS3Uri": str,
        "StoppingConditions": LabelingJobStoppingConditionsOutputTypeDef,
        "LabelingJobAlgorithmsConfig": LabelingJobAlgorithmsConfigOutputTypeDef,
        "HumanTaskConfig": HumanTaskConfigOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
        "LabelingJobOutput": LabelingJobOutputOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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


DescribeTrainingJobResponseOutputTypeDef = TypedDict(
    "DescribeTrainingJobResponseOutputTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "TuningJobArn": str,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "ModelArtifacts": ModelArtifactsOutputTypeDef,
        "TrainingJobStatus": TrainingJobStatusType,
        "SecondaryStatus": SecondaryStatusType,
        "FailureReason": str,
        "HyperParameters": Dict[str, str],
        "AlgorithmSpecification": AlgorithmSpecificationOutputTypeDef,
        "RoleArn": str,
        "InputDataConfig": List[ChannelOutputTypeDef],
        "OutputDataConfig": OutputDataConfigOutputTypeDef,
        "ResourceConfig": ResourceConfigOutputTypeDef,
        "VpcConfig": VpcConfigOutputTypeDef,
        "StoppingCondition": StoppingConditionOutputTypeDef,
        "CreationTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "SecondaryStatusTransitions": List[SecondaryStatusTransitionOutputTypeDef],
        "FinalMetricDataList": List[MetricDataOutputTypeDef],
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigOutputTypeDef,
        "TrainingTimeInSeconds": int,
        "BillableTimeInSeconds": int,
        "DebugHookConfig": DebugHookConfigOutputTypeDef,
        "ExperimentConfig": ExperimentConfigOutputTypeDef,
        "DebugRuleConfigurations": List[DebugRuleConfigurationOutputTypeDef],
        "TensorBoardOutputConfig": TensorBoardOutputConfigOutputTypeDef,
        "DebugRuleEvaluationStatuses": List[DebugRuleEvaluationStatusOutputTypeDef],
        "ProfilerConfig": ProfilerConfigOutputTypeDef,
        "ProfilerRuleConfigurations": List[ProfilerRuleConfigurationOutputTypeDef],
        "ProfilerRuleEvaluationStatuses": List[ProfilerRuleEvaluationStatusOutputTypeDef],
        "ProfilingStatus": ProfilingStatusType,
        "RetryStrategy": RetryStrategyOutputTypeDef,
        "Environment": Dict[str, str],
        "WarmPoolStatus": WarmPoolStatusOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TrainingJobOutputTypeDef = TypedDict(
    "TrainingJobOutputTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "TuningJobArn": str,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "ModelArtifacts": ModelArtifactsOutputTypeDef,
        "TrainingJobStatus": TrainingJobStatusType,
        "SecondaryStatus": SecondaryStatusType,
        "FailureReason": str,
        "HyperParameters": Dict[str, str],
        "AlgorithmSpecification": AlgorithmSpecificationOutputTypeDef,
        "RoleArn": str,
        "InputDataConfig": List[ChannelOutputTypeDef],
        "OutputDataConfig": OutputDataConfigOutputTypeDef,
        "ResourceConfig": ResourceConfigOutputTypeDef,
        "VpcConfig": VpcConfigOutputTypeDef,
        "StoppingCondition": StoppingConditionOutputTypeDef,
        "CreationTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "SecondaryStatusTransitions": List[SecondaryStatusTransitionOutputTypeDef],
        "FinalMetricDataList": List[MetricDataOutputTypeDef],
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigOutputTypeDef,
        "TrainingTimeInSeconds": int,
        "BillableTimeInSeconds": int,
        "DebugHookConfig": DebugHookConfigOutputTypeDef,
        "ExperimentConfig": ExperimentConfigOutputTypeDef,
        "DebugRuleConfigurations": List[DebugRuleConfigurationOutputTypeDef],
        "TensorBoardOutputConfig": TensorBoardOutputConfigOutputTypeDef,
        "DebugRuleEvaluationStatuses": List[DebugRuleEvaluationStatusOutputTypeDef],
        "Environment": Dict[str, str],
        "RetryStrategy": RetryStrategyOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
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


DescribeTransformJobResponseOutputTypeDef = TypedDict(
    "DescribeTransformJobResponseOutputTypeDef",
    {
        "TransformJobName": str,
        "TransformJobArn": str,
        "TransformJobStatus": TransformJobStatusType,
        "FailureReason": str,
        "ModelName": str,
        "MaxConcurrentTransforms": int,
        "ModelClientConfig": ModelClientConfigOutputTypeDef,
        "MaxPayloadInMB": int,
        "BatchStrategy": BatchStrategyType,
        "Environment": Dict[str, str],
        "TransformInput": TransformInputOutputTypeDef,
        "TransformOutput": TransformOutputOutputTypeDef,
        "DataCaptureConfig": BatchDataCaptureConfigOutputTypeDef,
        "TransformResources": TransformResourcesOutputTypeDef,
        "CreationTime": datetime,
        "TransformStartTime": datetime,
        "TransformEndTime": datetime,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "DataProcessing": DataProcessingOutputTypeDef,
        "ExperimentConfig": ExperimentConfigOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TransformJobDefinitionOutputTypeDef = TypedDict(
    "TransformJobDefinitionOutputTypeDef",
    {
        "MaxConcurrentTransforms": int,
        "MaxPayloadInMB": int,
        "BatchStrategy": BatchStrategyType,
        "Environment": Dict[str, str],
        "TransformInput": TransformInputOutputTypeDef,
        "TransformOutput": TransformOutputOutputTypeDef,
        "TransformResources": TransformResourcesOutputTypeDef,
    },
)

TransformJobOutputTypeDef = TypedDict(
    "TransformJobOutputTypeDef",
    {
        "TransformJobName": str,
        "TransformJobArn": str,
        "TransformJobStatus": TransformJobStatusType,
        "FailureReason": str,
        "ModelName": str,
        "MaxConcurrentTransforms": int,
        "ModelClientConfig": ModelClientConfigOutputTypeDef,
        "MaxPayloadInMB": int,
        "BatchStrategy": BatchStrategyType,
        "Environment": Dict[str, str],
        "TransformInput": TransformInputOutputTypeDef,
        "TransformOutput": TransformOutputOutputTypeDef,
        "TransformResources": TransformResourcesOutputTypeDef,
        "CreationTime": datetime,
        "TransformStartTime": datetime,
        "TransformEndTime": datetime,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "DataProcessing": DataProcessingOutputTypeDef,
        "ExperimentConfig": ExperimentConfigOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
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


DescribeAutoMLJobV2ResponseOutputTypeDef = TypedDict(
    "DescribeAutoMLJobV2ResponseOutputTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "AutoMLJobInputDataConfig": List[AutoMLJobChannelOutputTypeDef],
        "OutputDataConfig": AutoMLOutputDataConfigOutputTypeDef,
        "RoleArn": str,
        "AutoMLJobObjective": AutoMLJobObjectiveOutputTypeDef,
        "AutoMLProblemTypeConfig": AutoMLProblemTypeConfigOutputTypeDef,
        "CreationTime": datetime,
        "EndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "PartialFailureReasons": List[AutoMLPartialFailureReasonOutputTypeDef],
        "BestCandidate": AutoMLCandidateOutputTypeDef,
        "AutoMLJobStatus": AutoMLJobStatusType,
        "AutoMLJobSecondaryStatus": AutoMLJobSecondaryStatusType,
        "ModelDeployConfig": ModelDeployConfigOutputTypeDef,
        "ModelDeployResult": ModelDeployResultOutputTypeDef,
        "DataSplitConfig": AutoMLDataSplitConfigOutputTypeDef,
        "SecurityConfig": AutoMLSecurityConfigOutputTypeDef,
        "AutoMLJobArtifacts": AutoMLJobArtifactsOutputTypeDef,
        "ResolvedAttributes": AutoMLResolvedAttributesOutputTypeDef,
        "AutoMLProblemTypeConfigName": AutoMLProblemTypeConfigNameType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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


ListPipelineExecutionStepsResponseOutputTypeDef = TypedDict(
    "ListPipelineExecutionStepsResponseOutputTypeDef",
    {
        "PipelineExecutionSteps": List[PipelineExecutionStepOutputTypeDef],
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


DescribeInferenceRecommendationsJobResponseOutputTypeDef = TypedDict(
    "DescribeInferenceRecommendationsJobResponseOutputTypeDef",
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
        "InputConfig": RecommendationJobInputConfigOutputTypeDef,
        "StoppingConditions": RecommendationJobStoppingConditionsOutputTypeDef,
        "InferenceRecommendations": List[InferenceRecommendationOutputTypeDef],
        "EndpointPerformances": List[EndpointPerformanceOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

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


DescribeEndpointConfigOutputOutputTypeDef = TypedDict(
    "DescribeEndpointConfigOutputOutputTypeDef",
    {
        "EndpointConfigName": str,
        "EndpointConfigArn": str,
        "ProductionVariants": List[ProductionVariantOutputTypeDef],
        "DataCaptureConfig": DataCaptureConfigOutputTypeDef,
        "KmsKeyId": str,
        "CreationTime": datetime,
        "AsyncInferenceConfig": AsyncInferenceConfigOutputTypeDef,
        "ExplainerConfig": ExplainerConfigOutputTypeDef,
        "ShadowProductionVariants": List[ProductionVariantOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEndpointOutputOutputTypeDef = TypedDict(
    "DescribeEndpointOutputOutputTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "EndpointConfigName": str,
        "ProductionVariants": List[ProductionVariantSummaryOutputTypeDef],
        "DataCaptureConfig": DataCaptureConfigSummaryOutputTypeDef,
        "EndpointStatus": EndpointStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastDeploymentConfig": DeploymentConfigOutputTypeDef,
        "AsyncInferenceConfig": AsyncInferenceConfigOutputTypeDef,
        "PendingDeploymentSummary": PendingDeploymentSummaryOutputTypeDef,
        "ExplainerConfig": ExplainerConfigOutputTypeDef,
        "ShadowProductionVariants": List[ProductionVariantSummaryOutputTypeDef],
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


DescribeHyperParameterTuningJobResponseOutputTypeDef = TypedDict(
    "DescribeHyperParameterTuningJobResponseOutputTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobConfig": HyperParameterTuningJobConfigOutputTypeDef,
        "TrainingJobDefinition": HyperParameterTrainingJobDefinitionOutputTypeDef,
        "TrainingJobDefinitions": List[HyperParameterTrainingJobDefinitionOutputTypeDef],
        "HyperParameterTuningJobStatus": HyperParameterTuningJobStatusType,
        "CreationTime": datetime,
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersOutputTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersOutputTypeDef,
        "BestTrainingJob": HyperParameterTrainingJobSummaryOutputTypeDef,
        "OverallBestTrainingJob": HyperParameterTrainingJobSummaryOutputTypeDef,
        "WarmStartConfig": HyperParameterTuningJobWarmStartConfigOutputTypeDef,
        "FailureReason": str,
        "TuningJobCompletionDetails": HyperParameterTuningJobCompletionDetailsOutputTypeDef,
        "ConsumedResources": HyperParameterTuningJobConsumedResourcesOutputTypeDef,
        "Autotune": AutotuneOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HyperParameterTuningJobSearchEntityOutputTypeDef = TypedDict(
    "HyperParameterTuningJobSearchEntityOutputTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobConfig": HyperParameterTuningJobConfigOutputTypeDef,
        "TrainingJobDefinition": HyperParameterTrainingJobDefinitionOutputTypeDef,
        "TrainingJobDefinitions": List[HyperParameterTrainingJobDefinitionOutputTypeDef],
        "HyperParameterTuningJobStatus": HyperParameterTuningJobStatusType,
        "CreationTime": datetime,
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersOutputTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersOutputTypeDef,
        "BestTrainingJob": HyperParameterTrainingJobSummaryOutputTypeDef,
        "OverallBestTrainingJob": HyperParameterTrainingJobSummaryOutputTypeDef,
        "WarmStartConfig": HyperParameterTuningJobWarmStartConfigOutputTypeDef,
        "FailureReason": str,
        "Tags": List[TagOutputTypeDef],
        "TuningJobCompletionDetails": HyperParameterTuningJobCompletionDetailsOutputTypeDef,
        "ConsumedResources": HyperParameterTuningJobConsumedResourcesOutputTypeDef,
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


ListInferenceRecommendationsJobStepsResponseOutputTypeDef = TypedDict(
    "ListInferenceRecommendationsJobStepsResponseOutputTypeDef",
    {
        "Steps": List[InferenceRecommendationsJobStepOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListLabelingJobsResponseOutputTypeDef = TypedDict(
    "ListLabelingJobsResponseOutputTypeDef",
    {
        "LabelingJobSummaryList": List[LabelingJobSummaryOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDescribeModelPackageOutputOutputTypeDef = TypedDict(
    "BatchDescribeModelPackageOutputOutputTypeDef",
    {
        "ModelPackageSummaries": Dict[str, BatchDescribeModelPackageSummaryOutputTypeDef],
        "BatchDescribeModelPackageErrorMap": Dict[str, BatchDescribeModelPackageErrorOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDataQualityJobDefinitionResponseOutputTypeDef = TypedDict(
    "DescribeDataQualityJobDefinitionResponseOutputTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "DataQualityBaselineConfig": DataQualityBaselineConfigOutputTypeDef,
        "DataQualityAppSpecification": DataQualityAppSpecificationOutputTypeDef,
        "DataQualityJobInput": DataQualityJobInputOutputTypeDef,
        "DataQualityJobOutputConfig": MonitoringOutputConfigOutputTypeDef,
        "JobResources": MonitoringResourcesOutputTypeDef,
        "NetworkConfig": MonitoringNetworkConfigOutputTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelBiasJobDefinitionResponseOutputTypeDef = TypedDict(
    "DescribeModelBiasJobDefinitionResponseOutputTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "ModelBiasBaselineConfig": ModelBiasBaselineConfigOutputTypeDef,
        "ModelBiasAppSpecification": ModelBiasAppSpecificationOutputTypeDef,
        "ModelBiasJobInput": ModelBiasJobInputOutputTypeDef,
        "ModelBiasJobOutputConfig": MonitoringOutputConfigOutputTypeDef,
        "JobResources": MonitoringResourcesOutputTypeDef,
        "NetworkConfig": MonitoringNetworkConfigOutputTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelExplainabilityJobDefinitionResponseOutputTypeDef = TypedDict(
    "DescribeModelExplainabilityJobDefinitionResponseOutputTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "ModelExplainabilityBaselineConfig": ModelExplainabilityBaselineConfigOutputTypeDef,
        "ModelExplainabilityAppSpecification": ModelExplainabilityAppSpecificationOutputTypeDef,
        "ModelExplainabilityJobInput": ModelExplainabilityJobInputOutputTypeDef,
        "ModelExplainabilityJobOutputConfig": MonitoringOutputConfigOutputTypeDef,
        "JobResources": MonitoringResourcesOutputTypeDef,
        "NetworkConfig": MonitoringNetworkConfigOutputTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelQualityJobDefinitionResponseOutputTypeDef = TypedDict(
    "DescribeModelQualityJobDefinitionResponseOutputTypeDef",
    {
        "JobDefinitionArn": str,
        "JobDefinitionName": str,
        "CreationTime": datetime,
        "ModelQualityBaselineConfig": ModelQualityBaselineConfigOutputTypeDef,
        "ModelQualityAppSpecification": ModelQualityAppSpecificationOutputTypeDef,
        "ModelQualityJobInput": ModelQualityJobInputOutputTypeDef,
        "ModelQualityJobOutputConfig": MonitoringOutputConfigOutputTypeDef,
        "JobResources": MonitoringResourcesOutputTypeDef,
        "NetworkConfig": MonitoringNetworkConfigOutputTypeDef,
        "RoleArn": str,
        "StoppingCondition": MonitoringStoppingConditionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MonitoringJobDefinitionOutputTypeDef = TypedDict(
    "MonitoringJobDefinitionOutputTypeDef",
    {
        "BaselineConfig": MonitoringBaselineConfigOutputTypeDef,
        "MonitoringInputs": List[MonitoringInputOutputTypeDef],
        "MonitoringOutputConfig": MonitoringOutputConfigOutputTypeDef,
        "MonitoringResources": MonitoringResourcesOutputTypeDef,
        "MonitoringAppSpecification": MonitoringAppSpecificationOutputTypeDef,
        "StoppingCondition": MonitoringStoppingConditionOutputTypeDef,
        "Environment": Dict[str, str],
        "NetworkConfig": NetworkConfigOutputTypeDef,
        "RoleArn": str,
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


AlgorithmValidationProfileOutputTypeDef = TypedDict(
    "AlgorithmValidationProfileOutputTypeDef",
    {
        "ProfileName": str,
        "TrainingJobDefinition": TrainingJobDefinitionOutputTypeDef,
        "TransformJobDefinition": TransformJobDefinitionOutputTypeDef,
    },
)

ModelPackageValidationProfileOutputTypeDef = TypedDict(
    "ModelPackageValidationProfileOutputTypeDef",
    {
        "ProfileName": str,
        "TransformJobDefinition": TransformJobDefinitionOutputTypeDef,
    },
)

TrialComponentSourceDetailOutputTypeDef = TypedDict(
    "TrialComponentSourceDetailOutputTypeDef",
    {
        "SourceArn": str,
        "TrainingJob": TrainingJobOutputTypeDef,
        "ProcessingJob": ProcessingJobOutputTypeDef,
        "TransformJob": TransformJobOutputTypeDef,
    },
)

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

MonitoringScheduleConfigOutputTypeDef = TypedDict(
    "MonitoringScheduleConfigOutputTypeDef",
    {
        "ScheduleConfig": ScheduleConfigOutputTypeDef,
        "MonitoringJobDefinition": MonitoringJobDefinitionOutputTypeDef,
        "MonitoringJobDefinitionName": str,
        "MonitoringType": MonitoringTypeType,
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

AlgorithmValidationSpecificationOutputTypeDef = TypedDict(
    "AlgorithmValidationSpecificationOutputTypeDef",
    {
        "ValidationRole": str,
        "ValidationProfiles": List[AlgorithmValidationProfileOutputTypeDef],
    },
)

ModelPackageValidationSpecificationOutputTypeDef = TypedDict(
    "ModelPackageValidationSpecificationOutputTypeDef",
    {
        "ValidationRole": str,
        "ValidationProfiles": List[ModelPackageValidationProfileOutputTypeDef],
    },
)

TrialComponentOutputTypeDef = TypedDict(
    "TrialComponentOutputTypeDef",
    {
        "TrialComponentName": str,
        "DisplayName": str,
        "TrialComponentArn": str,
        "Source": TrialComponentSourceOutputTypeDef,
        "Status": TrialComponentStatusOutputTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "Parameters": Dict[str, TrialComponentParameterValueOutputTypeDef],
        "InputArtifacts": Dict[str, TrialComponentArtifactOutputTypeDef],
        "OutputArtifacts": Dict[str, TrialComponentArtifactOutputTypeDef],
        "Metrics": List[TrialComponentMetricSummaryOutputTypeDef],
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "SourceDetail": TrialComponentSourceDetailOutputTypeDef,
        "LineageGroupArn": str,
        "Tags": List[TagOutputTypeDef],
        "Parents": List[ParentOutputTypeDef],
        "RunName": str,
    },
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

DescribeMonitoringScheduleResponseOutputTypeDef = TypedDict(
    "DescribeMonitoringScheduleResponseOutputTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringScheduleName": str,
        "MonitoringScheduleStatus": ScheduleStatusType,
        "MonitoringType": MonitoringTypeType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleConfig": MonitoringScheduleConfigOutputTypeDef,
        "EndpointName": str,
        "LastMonitoringExecutionSummary": MonitoringExecutionSummaryOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelDashboardMonitoringScheduleOutputTypeDef = TypedDict(
    "ModelDashboardMonitoringScheduleOutputTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringScheduleName": str,
        "MonitoringScheduleStatus": ScheduleStatusType,
        "MonitoringType": MonitoringTypeType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleConfig": MonitoringScheduleConfigOutputTypeDef,
        "EndpointName": str,
        "MonitoringAlertSummaries": List[MonitoringAlertSummaryOutputTypeDef],
        "LastMonitoringExecutionSummary": MonitoringExecutionSummaryOutputTypeDef,
    },
)

MonitoringScheduleOutputTypeDef = TypedDict(
    "MonitoringScheduleOutputTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringScheduleName": str,
        "MonitoringScheduleStatus": ScheduleStatusType,
        "MonitoringType": MonitoringTypeType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleConfig": MonitoringScheduleConfigOutputTypeDef,
        "EndpointName": str,
        "LastMonitoringExecutionSummary": MonitoringExecutionSummaryOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
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


UpdateMonitoringScheduleRequestRequestTypeDef = TypedDict(
    "UpdateMonitoringScheduleRequestRequestTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringScheduleConfig": MonitoringScheduleConfigTypeDef,
    },
)

DescribeAlgorithmOutputOutputTypeDef = TypedDict(
    "DescribeAlgorithmOutputOutputTypeDef",
    {
        "AlgorithmName": str,
        "AlgorithmArn": str,
        "AlgorithmDescription": str,
        "CreationTime": datetime,
        "TrainingSpecification": TrainingSpecificationOutputTypeDef,
        "InferenceSpecification": InferenceSpecificationOutputTypeDef,
        "ValidationSpecification": AlgorithmValidationSpecificationOutputTypeDef,
        "AlgorithmStatus": AlgorithmStatusType,
        "AlgorithmStatusDetails": AlgorithmStatusDetailsOutputTypeDef,
        "ProductId": str,
        "CertifyForMarketplace": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeModelPackageOutputOutputTypeDef = TypedDict(
    "DescribeModelPackageOutputOutputTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageGroupName": str,
        "ModelPackageVersion": int,
        "ModelPackageArn": str,
        "ModelPackageDescription": str,
        "CreationTime": datetime,
        "InferenceSpecification": InferenceSpecificationOutputTypeDef,
        "SourceAlgorithmSpecification": SourceAlgorithmSpecificationOutputTypeDef,
        "ValidationSpecification": ModelPackageValidationSpecificationOutputTypeDef,
        "ModelPackageStatus": ModelPackageStatusType,
        "ModelPackageStatusDetails": ModelPackageStatusDetailsOutputTypeDef,
        "CertifyForMarketplace": bool,
        "ModelApprovalStatus": ModelApprovalStatusType,
        "CreatedBy": UserContextOutputTypeDef,
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "ModelMetrics": ModelMetricsOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ApprovalDescription": str,
        "CustomerMetadataProperties": Dict[str, str],
        "DriftCheckBaselines": DriftCheckBaselinesOutputTypeDef,
        "Domain": str,
        "Task": str,
        "SamplePayloadUrl": str,
        "AdditionalInferenceSpecifications": List[
            AdditionalInferenceSpecificationDefinitionOutputTypeDef
        ],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModelPackageOutputTypeDef = TypedDict(
    "ModelPackageOutputTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageGroupName": str,
        "ModelPackageVersion": int,
        "ModelPackageArn": str,
        "ModelPackageDescription": str,
        "CreationTime": datetime,
        "InferenceSpecification": InferenceSpecificationOutputTypeDef,
        "SourceAlgorithmSpecification": SourceAlgorithmSpecificationOutputTypeDef,
        "ValidationSpecification": ModelPackageValidationSpecificationOutputTypeDef,
        "ModelPackageStatus": ModelPackageStatusType,
        "ModelPackageStatusDetails": ModelPackageStatusDetailsOutputTypeDef,
        "CertifyForMarketplace": bool,
        "ModelApprovalStatus": ModelApprovalStatusType,
        "CreatedBy": UserContextOutputTypeDef,
        "MetadataProperties": MetadataPropertiesOutputTypeDef,
        "ModelMetrics": ModelMetricsOutputTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextOutputTypeDef,
        "ApprovalDescription": str,
        "Domain": str,
        "Task": str,
        "SamplePayloadUrl": str,
        "AdditionalInferenceSpecifications": List[
            AdditionalInferenceSpecificationDefinitionOutputTypeDef
        ],
        "Tags": List[TagOutputTypeDef],
        "CustomerMetadataProperties": Dict[str, str],
        "DriftCheckBaselines": DriftCheckBaselinesOutputTypeDef,
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

ModelDashboardModelOutputTypeDef = TypedDict(
    "ModelDashboardModelOutputTypeDef",
    {
        "Model": ModelOutputTypeDef,
        "Endpoints": List[ModelDashboardEndpointOutputTypeDef],
        "LastBatchTransformJob": TransformJobOutputTypeDef,
        "MonitoringSchedules": List[ModelDashboardMonitoringScheduleOutputTypeDef],
        "ModelCard": ModelDashboardModelCardOutputTypeDef,
    },
)

EndpointOutputTypeDef = TypedDict(
    "EndpointOutputTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "EndpointConfigName": str,
        "ProductionVariants": List[ProductionVariantSummaryOutputTypeDef],
        "DataCaptureConfig": DataCaptureConfigSummaryOutputTypeDef,
        "EndpointStatus": EndpointStatusType,
        "FailureReason": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringSchedules": List[MonitoringScheduleOutputTypeDef],
        "Tags": List[TagOutputTypeDef],
        "ShadowProductionVariants": List[ProductionVariantSummaryOutputTypeDef],
    },
)

SearchRecordOutputTypeDef = TypedDict(
    "SearchRecordOutputTypeDef",
    {
        "TrainingJob": TrainingJobOutputTypeDef,
        "Experiment": ExperimentOutputTypeDef,
        "Trial": TrialOutputTypeDef,
        "TrialComponent": TrialComponentOutputTypeDef,
        "Endpoint": EndpointOutputTypeDef,
        "ModelPackage": ModelPackageOutputTypeDef,
        "ModelPackageGroup": ModelPackageGroupOutputTypeDef,
        "Pipeline": PipelineOutputTypeDef,
        "PipelineExecution": PipelineExecutionOutputTypeDef,
        "FeatureGroup": FeatureGroupOutputTypeDef,
        "Project": ProjectOutputTypeDef,
        "FeatureMetadata": FeatureMetadataOutputTypeDef,
        "HyperParameterTuningJob": HyperParameterTuningJobSearchEntityOutputTypeDef,
        "Model": ModelDashboardModelOutputTypeDef,
        "ModelCard": ModelCardOutputTypeDef,
    },
)

SearchResponseOutputTypeDef = TypedDict(
    "SearchResponseOutputTypeDef",
    {
        "Results": List[SearchRecordOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
