"""
Type annotations for personalize service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/type_defs/)

Usage::

    ```python
    from mypy_boto3_personalize.type_defs import AlgorithmImageOutputTypeDef

    data: AlgorithmImageOutputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    DomainType,
    ImportModeType,
    IngestionModeType,
    ObjectiveSensitivityType,
    TrainingModeType,
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
    "AlgorithmImageOutputTypeDef",
    "AutoMLConfigOutputTypeDef",
    "AutoMLConfigTypeDef",
    "AutoMLResultOutputTypeDef",
    "BatchInferenceJobConfigTypeDef",
    "S3DataConfigTypeDef",
    "BatchInferenceJobSummaryOutputTypeDef",
    "BatchSegmentJobSummaryOutputTypeDef",
    "CampaignConfigOutputTypeDef",
    "CampaignConfigTypeDef",
    "CampaignSummaryOutputTypeDef",
    "CategoricalHyperParameterRangeOutputTypeDef",
    "CategoricalHyperParameterRangeTypeDef",
    "ContinuousHyperParameterRangeOutputTypeDef",
    "ContinuousHyperParameterRangeTypeDef",
    "TagTypeDef",
    "CreateBatchInferenceJobResponseOutputTypeDef",
    "CreateBatchSegmentJobResponseOutputTypeDef",
    "CreateCampaignResponseOutputTypeDef",
    "CreateDatasetExportJobResponseOutputTypeDef",
    "CreateDatasetGroupResponseOutputTypeDef",
    "DataSourceTypeDef",
    "CreateDatasetImportJobResponseOutputTypeDef",
    "CreateDatasetResponseOutputTypeDef",
    "CreateEventTrackerResponseOutputTypeDef",
    "CreateFilterResponseOutputTypeDef",
    "MetricAttributeTypeDef",
    "CreateMetricAttributionResponseOutputTypeDef",
    "CreateRecommenderResponseOutputTypeDef",
    "CreateSchemaRequestRequestTypeDef",
    "CreateSchemaResponseOutputTypeDef",
    "CreateSolutionResponseOutputTypeDef",
    "CreateSolutionVersionResponseOutputTypeDef",
    "DataSourceOutputTypeDef",
    "DatasetExportJobSummaryOutputTypeDef",
    "DatasetGroupOutputTypeDef",
    "DatasetGroupSummaryOutputTypeDef",
    "DatasetImportJobSummaryOutputTypeDef",
    "DatasetUpdateSummaryOutputTypeDef",
    "DatasetSchemaOutputTypeDef",
    "DatasetSchemaSummaryOutputTypeDef",
    "DatasetSummaryOutputTypeDef",
    "DefaultCategoricalHyperParameterRangeOutputTypeDef",
    "DefaultContinuousHyperParameterRangeOutputTypeDef",
    "DefaultIntegerHyperParameterRangeOutputTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteDatasetGroupRequestRequestTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteEventTrackerRequestRequestTypeDef",
    "DeleteFilterRequestRequestTypeDef",
    "DeleteMetricAttributionRequestRequestTypeDef",
    "DeleteRecommenderRequestRequestTypeDef",
    "DeleteSchemaRequestRequestTypeDef",
    "DeleteSolutionRequestRequestTypeDef",
    "DescribeAlgorithmRequestRequestTypeDef",
    "DescribeBatchInferenceJobRequestRequestTypeDef",
    "DescribeBatchSegmentJobRequestRequestTypeDef",
    "DescribeCampaignRequestRequestTypeDef",
    "DescribeDatasetExportJobRequestRequestTypeDef",
    "DescribeDatasetGroupRequestRequestTypeDef",
    "DescribeDatasetImportJobRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeEventTrackerRequestRequestTypeDef",
    "EventTrackerOutputTypeDef",
    "DescribeFeatureTransformationRequestRequestTypeDef",
    "FeatureTransformationOutputTypeDef",
    "DescribeFilterRequestRequestTypeDef",
    "FilterOutputTypeDef",
    "DescribeMetricAttributionRequestRequestTypeDef",
    "DescribeRecipeRequestRequestTypeDef",
    "RecipeOutputTypeDef",
    "DescribeRecommenderRequestRequestTypeDef",
    "DescribeSchemaRequestRequestTypeDef",
    "DescribeSolutionRequestRequestTypeDef",
    "DescribeSolutionVersionRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventTrackerSummaryOutputTypeDef",
    "FilterSummaryOutputTypeDef",
    "GetSolutionMetricsRequestRequestTypeDef",
    "GetSolutionMetricsResponseOutputTypeDef",
    "HPOObjectiveOutputTypeDef",
    "HPOResourceConfigOutputTypeDef",
    "HPOObjectiveTypeDef",
    "HPOResourceConfigTypeDef",
    "IntegerHyperParameterRangeOutputTypeDef",
    "IntegerHyperParameterRangeTypeDef",
    "ListBatchInferenceJobsRequestListBatchInferenceJobsPaginateTypeDef",
    "ListBatchInferenceJobsRequestRequestTypeDef",
    "ListBatchSegmentJobsRequestListBatchSegmentJobsPaginateTypeDef",
    "ListBatchSegmentJobsRequestRequestTypeDef",
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    "ListCampaignsRequestRequestTypeDef",
    "ListDatasetExportJobsRequestListDatasetExportJobsPaginateTypeDef",
    "ListDatasetExportJobsRequestRequestTypeDef",
    "ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef",
    "ListDatasetGroupsRequestRequestTypeDef",
    "ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef",
    "ListDatasetImportJobsRequestRequestTypeDef",
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListEventTrackersRequestListEventTrackersPaginateTypeDef",
    "ListEventTrackersRequestRequestTypeDef",
    "ListFiltersRequestListFiltersPaginateTypeDef",
    "ListFiltersRequestRequestTypeDef",
    "ListMetricAttributionMetricsRequestListMetricAttributionMetricsPaginateTypeDef",
    "ListMetricAttributionMetricsRequestRequestTypeDef",
    "MetricAttributeOutputTypeDef",
    "ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef",
    "ListMetricAttributionsRequestRequestTypeDef",
    "MetricAttributionSummaryOutputTypeDef",
    "ListRecipesRequestListRecipesPaginateTypeDef",
    "ListRecipesRequestRequestTypeDef",
    "RecipeSummaryOutputTypeDef",
    "ListRecommendersRequestListRecommendersPaginateTypeDef",
    "ListRecommendersRequestRequestTypeDef",
    "ListSchemasRequestListSchemasPaginateTypeDef",
    "ListSchemasRequestRequestTypeDef",
    "ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef",
    "ListSolutionVersionsRequestRequestTypeDef",
    "SolutionVersionSummaryOutputTypeDef",
    "ListSolutionsRequestListSolutionsPaginateTypeDef",
    "ListSolutionsRequestRequestTypeDef",
    "SolutionSummaryOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagOutputTypeDef",
    "OptimizationObjectiveOutputTypeDef",
    "OptimizationObjectiveTypeDef",
    "PaginatorConfigTypeDef",
    "TrainingDataConfigOutputTypeDef",
    "TrainingDataConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TunedHPOParamsOutputTypeDef",
    "StartRecommenderRequestRequestTypeDef",
    "StartRecommenderResponseOutputTypeDef",
    "StopRecommenderRequestRequestTypeDef",
    "StopRecommenderResponseOutputTypeDef",
    "StopSolutionVersionCreationRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCampaignResponseOutputTypeDef",
    "UpdateDatasetRequestRequestTypeDef",
    "UpdateDatasetResponseOutputTypeDef",
    "UpdateMetricAttributionResponseOutputTypeDef",
    "UpdateRecommenderResponseOutputTypeDef",
    "BatchInferenceJobInputTypeDef",
    "BatchInferenceJobOutputTypeDef",
    "BatchSegmentJobInputTypeDef",
    "BatchSegmentJobOutputTypeDef",
    "DatasetExportJobOutputTypeDef",
    "MetricAttributionOutputTypeDef",
    "ListBatchInferenceJobsResponseOutputTypeDef",
    "ListBatchSegmentJobsResponseOutputTypeDef",
    "CampaignUpdateSummaryOutputTypeDef",
    "UpdateCampaignRequestRequestTypeDef",
    "ListCampaignsResponseOutputTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "CreateDatasetGroupRequestRequestTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateEventTrackerRequestRequestTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "CreateSolutionVersionRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateDatasetImportJobRequestRequestTypeDef",
    "DatasetImportJobOutputTypeDef",
    "ListDatasetExportJobsResponseOutputTypeDef",
    "DescribeDatasetGroupResponseOutputTypeDef",
    "ListDatasetGroupsResponseOutputTypeDef",
    "ListDatasetImportJobsResponseOutputTypeDef",
    "DatasetOutputTypeDef",
    "DescribeSchemaResponseOutputTypeDef",
    "ListSchemasResponseOutputTypeDef",
    "ListDatasetsResponseOutputTypeDef",
    "DefaultHyperParameterRangesOutputTypeDef",
    "DescribeEventTrackerResponseOutputTypeDef",
    "DescribeFeatureTransformationResponseOutputTypeDef",
    "DescribeFilterResponseOutputTypeDef",
    "DescribeRecipeResponseOutputTypeDef",
    "ListEventTrackersResponseOutputTypeDef",
    "ListFiltersResponseOutputTypeDef",
    "HyperParameterRangesOutputTypeDef",
    "HyperParameterRangesTypeDef",
    "ListMetricAttributionMetricsResponseOutputTypeDef",
    "ListMetricAttributionsResponseOutputTypeDef",
    "ListRecipesResponseOutputTypeDef",
    "ListSolutionVersionsResponseOutputTypeDef",
    "ListSolutionsResponseOutputTypeDef",
    "ListTagsForResourceResponseOutputTypeDef",
    "RecommenderConfigOutputTypeDef",
    "RecommenderConfigTypeDef",
    "CreateBatchInferenceJobRequestRequestTypeDef",
    "DescribeBatchInferenceJobResponseOutputTypeDef",
    "CreateBatchSegmentJobRequestRequestTypeDef",
    "DescribeBatchSegmentJobResponseOutputTypeDef",
    "CreateDatasetExportJobRequestRequestTypeDef",
    "DescribeDatasetExportJobResponseOutputTypeDef",
    "CreateMetricAttributionRequestRequestTypeDef",
    "DescribeMetricAttributionResponseOutputTypeDef",
    "UpdateMetricAttributionRequestRequestTypeDef",
    "CampaignOutputTypeDef",
    "DescribeDatasetImportJobResponseOutputTypeDef",
    "DescribeDatasetResponseOutputTypeDef",
    "AlgorithmOutputTypeDef",
    "HPOConfigOutputTypeDef",
    "HPOConfigTypeDef",
    "RecommenderSummaryOutputTypeDef",
    "RecommenderUpdateSummaryOutputTypeDef",
    "CreateRecommenderRequestRequestTypeDef",
    "UpdateRecommenderRequestRequestTypeDef",
    "DescribeCampaignResponseOutputTypeDef",
    "DescribeAlgorithmResponseOutputTypeDef",
    "SolutionConfigOutputTypeDef",
    "SolutionConfigTypeDef",
    "ListRecommendersResponseOutputTypeDef",
    "RecommenderOutputTypeDef",
    "SolutionOutputTypeDef",
    "SolutionVersionOutputTypeDef",
    "CreateSolutionRequestRequestTypeDef",
    "DescribeRecommenderResponseOutputTypeDef",
    "DescribeSolutionResponseOutputTypeDef",
    "DescribeSolutionVersionResponseOutputTypeDef",
)

AlgorithmImageOutputTypeDef = TypedDict(
    "AlgorithmImageOutputTypeDef",
    {
        "name": str,
        "dockerURI": str,
    },
)

AutoMLConfigOutputTypeDef = TypedDict(
    "AutoMLConfigOutputTypeDef",
    {
        "metricName": str,
        "recipeList": List[str],
    },
)

AutoMLConfigTypeDef = TypedDict(
    "AutoMLConfigTypeDef",
    {
        "metricName": str,
        "recipeList": Sequence[str],
    },
    total=False,
)

AutoMLResultOutputTypeDef = TypedDict(
    "AutoMLResultOutputTypeDef",
    {
        "bestRecipeArn": str,
    },
)

BatchInferenceJobConfigTypeDef = TypedDict(
    "BatchInferenceJobConfigTypeDef",
    {
        "itemExplorationConfig": Mapping[str, str],
    },
    total=False,
)

_RequiredS3DataConfigTypeDef = TypedDict(
    "_RequiredS3DataConfigTypeDef",
    {
        "path": str,
    },
)
_OptionalS3DataConfigTypeDef = TypedDict(
    "_OptionalS3DataConfigTypeDef",
    {
        "kmsKeyArn": str,
    },
    total=False,
)

class S3DataConfigTypeDef(_RequiredS3DataConfigTypeDef, _OptionalS3DataConfigTypeDef):
    pass

BatchInferenceJobSummaryOutputTypeDef = TypedDict(
    "BatchInferenceJobSummaryOutputTypeDef",
    {
        "batchInferenceJobArn": str,
        "jobName": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "solutionVersionArn": str,
    },
)

BatchSegmentJobSummaryOutputTypeDef = TypedDict(
    "BatchSegmentJobSummaryOutputTypeDef",
    {
        "batchSegmentJobArn": str,
        "jobName": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "solutionVersionArn": str,
    },
)

CampaignConfigOutputTypeDef = TypedDict(
    "CampaignConfigOutputTypeDef",
    {
        "itemExplorationConfig": Dict[str, str],
    },
)

CampaignConfigTypeDef = TypedDict(
    "CampaignConfigTypeDef",
    {
        "itemExplorationConfig": Mapping[str, str],
    },
    total=False,
)

CampaignSummaryOutputTypeDef = TypedDict(
    "CampaignSummaryOutputTypeDef",
    {
        "name": str,
        "campaignArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
)

CategoricalHyperParameterRangeOutputTypeDef = TypedDict(
    "CategoricalHyperParameterRangeOutputTypeDef",
    {
        "name": str,
        "values": List[str],
    },
)

CategoricalHyperParameterRangeTypeDef = TypedDict(
    "CategoricalHyperParameterRangeTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
    total=False,
)

ContinuousHyperParameterRangeOutputTypeDef = TypedDict(
    "ContinuousHyperParameterRangeOutputTypeDef",
    {
        "name": str,
        "minValue": float,
        "maxValue": float,
    },
)

ContinuousHyperParameterRangeTypeDef = TypedDict(
    "ContinuousHyperParameterRangeTypeDef",
    {
        "name": str,
        "minValue": float,
        "maxValue": float,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "tagKey": str,
        "tagValue": str,
    },
)

CreateBatchInferenceJobResponseOutputTypeDef = TypedDict(
    "CreateBatchInferenceJobResponseOutputTypeDef",
    {
        "batchInferenceJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateBatchSegmentJobResponseOutputTypeDef = TypedDict(
    "CreateBatchSegmentJobResponseOutputTypeDef",
    {
        "batchSegmentJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateCampaignResponseOutputTypeDef = TypedDict(
    "CreateCampaignResponseOutputTypeDef",
    {
        "campaignArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetExportJobResponseOutputTypeDef = TypedDict(
    "CreateDatasetExportJobResponseOutputTypeDef",
    {
        "datasetExportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetGroupResponseOutputTypeDef = TypedDict(
    "CreateDatasetGroupResponseOutputTypeDef",
    {
        "datasetGroupArn": str,
        "domain": DomainType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "dataLocation": str,
    },
    total=False,
)

CreateDatasetImportJobResponseOutputTypeDef = TypedDict(
    "CreateDatasetImportJobResponseOutputTypeDef",
    {
        "datasetImportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetResponseOutputTypeDef = TypedDict(
    "CreateDatasetResponseOutputTypeDef",
    {
        "datasetArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEventTrackerResponseOutputTypeDef = TypedDict(
    "CreateEventTrackerResponseOutputTypeDef",
    {
        "eventTrackerArn": str,
        "trackingId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateFilterResponseOutputTypeDef = TypedDict(
    "CreateFilterResponseOutputTypeDef",
    {
        "filterArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MetricAttributeTypeDef = TypedDict(
    "MetricAttributeTypeDef",
    {
        "eventType": str,
        "metricName": str,
        "expression": str,
    },
)

CreateMetricAttributionResponseOutputTypeDef = TypedDict(
    "CreateMetricAttributionResponseOutputTypeDef",
    {
        "metricAttributionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateRecommenderResponseOutputTypeDef = TypedDict(
    "CreateRecommenderResponseOutputTypeDef",
    {
        "recommenderArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateSchemaRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSchemaRequestRequestTypeDef",
    {
        "name": str,
        "schema": str,
    },
)
_OptionalCreateSchemaRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSchemaRequestRequestTypeDef",
    {
        "domain": DomainType,
    },
    total=False,
)

class CreateSchemaRequestRequestTypeDef(
    _RequiredCreateSchemaRequestRequestTypeDef, _OptionalCreateSchemaRequestRequestTypeDef
):
    pass

CreateSchemaResponseOutputTypeDef = TypedDict(
    "CreateSchemaResponseOutputTypeDef",
    {
        "schemaArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateSolutionResponseOutputTypeDef = TypedDict(
    "CreateSolutionResponseOutputTypeDef",
    {
        "solutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateSolutionVersionResponseOutputTypeDef = TypedDict(
    "CreateSolutionVersionResponseOutputTypeDef",
    {
        "solutionVersionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataSourceOutputTypeDef = TypedDict(
    "DataSourceOutputTypeDef",
    {
        "dataLocation": str,
    },
)

DatasetExportJobSummaryOutputTypeDef = TypedDict(
    "DatasetExportJobSummaryOutputTypeDef",
    {
        "datasetExportJobArn": str,
        "jobName": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
)

DatasetGroupOutputTypeDef = TypedDict(
    "DatasetGroupOutputTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
        "status": str,
        "roleArn": str,
        "kmsKeyArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "domain": DomainType,
    },
)

DatasetGroupSummaryOutputTypeDef = TypedDict(
    "DatasetGroupSummaryOutputTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "domain": DomainType,
    },
)

DatasetImportJobSummaryOutputTypeDef = TypedDict(
    "DatasetImportJobSummaryOutputTypeDef",
    {
        "datasetImportJobArn": str,
        "jobName": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "importMode": ImportModeType,
    },
)

DatasetUpdateSummaryOutputTypeDef = TypedDict(
    "DatasetUpdateSummaryOutputTypeDef",
    {
        "schemaArn": str,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

DatasetSchemaOutputTypeDef = TypedDict(
    "DatasetSchemaOutputTypeDef",
    {
        "name": str,
        "schemaArn": str,
        "schema": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "domain": DomainType,
    },
)

DatasetSchemaSummaryOutputTypeDef = TypedDict(
    "DatasetSchemaSummaryOutputTypeDef",
    {
        "name": str,
        "schemaArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "domain": DomainType,
    },
)

DatasetSummaryOutputTypeDef = TypedDict(
    "DatasetSummaryOutputTypeDef",
    {
        "name": str,
        "datasetArn": str,
        "datasetType": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

DefaultCategoricalHyperParameterRangeOutputTypeDef = TypedDict(
    "DefaultCategoricalHyperParameterRangeOutputTypeDef",
    {
        "name": str,
        "values": List[str],
        "isTunable": bool,
    },
)

DefaultContinuousHyperParameterRangeOutputTypeDef = TypedDict(
    "DefaultContinuousHyperParameterRangeOutputTypeDef",
    {
        "name": str,
        "minValue": float,
        "maxValue": float,
        "isTunable": bool,
    },
)

DefaultIntegerHyperParameterRangeOutputTypeDef = TypedDict(
    "DefaultIntegerHyperParameterRangeOutputTypeDef",
    {
        "name": str,
        "minValue": int,
        "maxValue": int,
        "isTunable": bool,
    },
)

DeleteCampaignRequestRequestTypeDef = TypedDict(
    "DeleteCampaignRequestRequestTypeDef",
    {
        "campaignArn": str,
    },
)

DeleteDatasetGroupRequestRequestTypeDef = TypedDict(
    "DeleteDatasetGroupRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
    },
)

DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "datasetArn": str,
    },
)

DeleteEventTrackerRequestRequestTypeDef = TypedDict(
    "DeleteEventTrackerRequestRequestTypeDef",
    {
        "eventTrackerArn": str,
    },
)

DeleteFilterRequestRequestTypeDef = TypedDict(
    "DeleteFilterRequestRequestTypeDef",
    {
        "filterArn": str,
    },
)

DeleteMetricAttributionRequestRequestTypeDef = TypedDict(
    "DeleteMetricAttributionRequestRequestTypeDef",
    {
        "metricAttributionArn": str,
    },
)

DeleteRecommenderRequestRequestTypeDef = TypedDict(
    "DeleteRecommenderRequestRequestTypeDef",
    {
        "recommenderArn": str,
    },
)

DeleteSchemaRequestRequestTypeDef = TypedDict(
    "DeleteSchemaRequestRequestTypeDef",
    {
        "schemaArn": str,
    },
)

DeleteSolutionRequestRequestTypeDef = TypedDict(
    "DeleteSolutionRequestRequestTypeDef",
    {
        "solutionArn": str,
    },
)

DescribeAlgorithmRequestRequestTypeDef = TypedDict(
    "DescribeAlgorithmRequestRequestTypeDef",
    {
        "algorithmArn": str,
    },
)

DescribeBatchInferenceJobRequestRequestTypeDef = TypedDict(
    "DescribeBatchInferenceJobRequestRequestTypeDef",
    {
        "batchInferenceJobArn": str,
    },
)

DescribeBatchSegmentJobRequestRequestTypeDef = TypedDict(
    "DescribeBatchSegmentJobRequestRequestTypeDef",
    {
        "batchSegmentJobArn": str,
    },
)

DescribeCampaignRequestRequestTypeDef = TypedDict(
    "DescribeCampaignRequestRequestTypeDef",
    {
        "campaignArn": str,
    },
)

DescribeDatasetExportJobRequestRequestTypeDef = TypedDict(
    "DescribeDatasetExportJobRequestRequestTypeDef",
    {
        "datasetExportJobArn": str,
    },
)

DescribeDatasetGroupRequestRequestTypeDef = TypedDict(
    "DescribeDatasetGroupRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
    },
)

DescribeDatasetImportJobRequestRequestTypeDef = TypedDict(
    "DescribeDatasetImportJobRequestRequestTypeDef",
    {
        "datasetImportJobArn": str,
    },
)

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "datasetArn": str,
    },
)

DescribeEventTrackerRequestRequestTypeDef = TypedDict(
    "DescribeEventTrackerRequestRequestTypeDef",
    {
        "eventTrackerArn": str,
    },
)

EventTrackerOutputTypeDef = TypedDict(
    "EventTrackerOutputTypeDef",
    {
        "name": str,
        "eventTrackerArn": str,
        "accountId": str,
        "trackingId": str,
        "datasetGroupArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

DescribeFeatureTransformationRequestRequestTypeDef = TypedDict(
    "DescribeFeatureTransformationRequestRequestTypeDef",
    {
        "featureTransformationArn": str,
    },
)

FeatureTransformationOutputTypeDef = TypedDict(
    "FeatureTransformationOutputTypeDef",
    {
        "name": str,
        "featureTransformationArn": str,
        "defaultParameters": Dict[str, str],
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "status": str,
    },
)

DescribeFilterRequestRequestTypeDef = TypedDict(
    "DescribeFilterRequestRequestTypeDef",
    {
        "filterArn": str,
    },
)

FilterOutputTypeDef = TypedDict(
    "FilterOutputTypeDef",
    {
        "name": str,
        "filterArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "datasetGroupArn": str,
        "failureReason": str,
        "filterExpression": str,
        "status": str,
    },
)

DescribeMetricAttributionRequestRequestTypeDef = TypedDict(
    "DescribeMetricAttributionRequestRequestTypeDef",
    {
        "metricAttributionArn": str,
    },
)

DescribeRecipeRequestRequestTypeDef = TypedDict(
    "DescribeRecipeRequestRequestTypeDef",
    {
        "recipeArn": str,
    },
)

RecipeOutputTypeDef = TypedDict(
    "RecipeOutputTypeDef",
    {
        "name": str,
        "recipeArn": str,
        "algorithmArn": str,
        "featureTransformationArn": str,
        "status": str,
        "description": str,
        "creationDateTime": datetime,
        "recipeType": str,
        "lastUpdatedDateTime": datetime,
    },
)

DescribeRecommenderRequestRequestTypeDef = TypedDict(
    "DescribeRecommenderRequestRequestTypeDef",
    {
        "recommenderArn": str,
    },
)

DescribeSchemaRequestRequestTypeDef = TypedDict(
    "DescribeSchemaRequestRequestTypeDef",
    {
        "schemaArn": str,
    },
)

DescribeSolutionRequestRequestTypeDef = TypedDict(
    "DescribeSolutionRequestRequestTypeDef",
    {
        "solutionArn": str,
    },
)

DescribeSolutionVersionRequestRequestTypeDef = TypedDict(
    "DescribeSolutionVersionRequestRequestTypeDef",
    {
        "solutionVersionArn": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EventTrackerSummaryOutputTypeDef = TypedDict(
    "EventTrackerSummaryOutputTypeDef",
    {
        "name": str,
        "eventTrackerArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

FilterSummaryOutputTypeDef = TypedDict(
    "FilterSummaryOutputTypeDef",
    {
        "name": str,
        "filterArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "datasetGroupArn": str,
        "failureReason": str,
        "status": str,
    },
)

GetSolutionMetricsRequestRequestTypeDef = TypedDict(
    "GetSolutionMetricsRequestRequestTypeDef",
    {
        "solutionVersionArn": str,
    },
)

GetSolutionMetricsResponseOutputTypeDef = TypedDict(
    "GetSolutionMetricsResponseOutputTypeDef",
    {
        "solutionVersionArn": str,
        "metrics": Dict[str, float],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HPOObjectiveOutputTypeDef = TypedDict(
    "HPOObjectiveOutputTypeDef",
    {
        "type": str,
        "metricName": str,
        "metricRegex": str,
    },
)

HPOResourceConfigOutputTypeDef = TypedDict(
    "HPOResourceConfigOutputTypeDef",
    {
        "maxNumberOfTrainingJobs": str,
        "maxParallelTrainingJobs": str,
    },
)

HPOObjectiveTypeDef = TypedDict(
    "HPOObjectiveTypeDef",
    {
        "type": str,
        "metricName": str,
        "metricRegex": str,
    },
    total=False,
)

HPOResourceConfigTypeDef = TypedDict(
    "HPOResourceConfigTypeDef",
    {
        "maxNumberOfTrainingJobs": str,
        "maxParallelTrainingJobs": str,
    },
    total=False,
)

IntegerHyperParameterRangeOutputTypeDef = TypedDict(
    "IntegerHyperParameterRangeOutputTypeDef",
    {
        "name": str,
        "minValue": int,
        "maxValue": int,
    },
)

IntegerHyperParameterRangeTypeDef = TypedDict(
    "IntegerHyperParameterRangeTypeDef",
    {
        "name": str,
        "minValue": int,
        "maxValue": int,
    },
    total=False,
)

ListBatchInferenceJobsRequestListBatchInferenceJobsPaginateTypeDef = TypedDict(
    "ListBatchInferenceJobsRequestListBatchInferenceJobsPaginateTypeDef",
    {
        "solutionVersionArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBatchInferenceJobsRequestRequestTypeDef = TypedDict(
    "ListBatchInferenceJobsRequestRequestTypeDef",
    {
        "solutionVersionArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListBatchSegmentJobsRequestListBatchSegmentJobsPaginateTypeDef = TypedDict(
    "ListBatchSegmentJobsRequestListBatchSegmentJobsPaginateTypeDef",
    {
        "solutionVersionArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBatchSegmentJobsRequestRequestTypeDef = TypedDict(
    "ListBatchSegmentJobsRequestRequestTypeDef",
    {
        "solutionVersionArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListCampaignsRequestListCampaignsPaginateTypeDef = TypedDict(
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    {
        "solutionArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCampaignsRequestRequestTypeDef = TypedDict(
    "ListCampaignsRequestRequestTypeDef",
    {
        "solutionArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListDatasetExportJobsRequestListDatasetExportJobsPaginateTypeDef = TypedDict(
    "ListDatasetExportJobsRequestListDatasetExportJobsPaginateTypeDef",
    {
        "datasetArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDatasetExportJobsRequestRequestTypeDef = TypedDict(
    "ListDatasetExportJobsRequestRequestTypeDef",
    {
        "datasetArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef = TypedDict(
    "ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDatasetGroupsRequestRequestTypeDef = TypedDict(
    "ListDatasetGroupsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef = TypedDict(
    "ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef",
    {
        "datasetArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDatasetImportJobsRequestRequestTypeDef = TypedDict(
    "ListDatasetImportJobsRequestRequestTypeDef",
    {
        "datasetArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListDatasetsRequestListDatasetsPaginateTypeDef = TypedDict(
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    {
        "datasetGroupArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDatasetsRequestRequestTypeDef = TypedDict(
    "ListDatasetsRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListEventTrackersRequestListEventTrackersPaginateTypeDef = TypedDict(
    "ListEventTrackersRequestListEventTrackersPaginateTypeDef",
    {
        "datasetGroupArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEventTrackersRequestRequestTypeDef = TypedDict(
    "ListEventTrackersRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListFiltersRequestListFiltersPaginateTypeDef = TypedDict(
    "ListFiltersRequestListFiltersPaginateTypeDef",
    {
        "datasetGroupArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFiltersRequestRequestTypeDef = TypedDict(
    "ListFiltersRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListMetricAttributionMetricsRequestListMetricAttributionMetricsPaginateTypeDef = TypedDict(
    "ListMetricAttributionMetricsRequestListMetricAttributionMetricsPaginateTypeDef",
    {
        "metricAttributionArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMetricAttributionMetricsRequestRequestTypeDef = TypedDict(
    "ListMetricAttributionMetricsRequestRequestTypeDef",
    {
        "metricAttributionArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

MetricAttributeOutputTypeDef = TypedDict(
    "MetricAttributeOutputTypeDef",
    {
        "eventType": str,
        "metricName": str,
        "expression": str,
    },
)

ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef = TypedDict(
    "ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef",
    {
        "datasetGroupArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMetricAttributionsRequestRequestTypeDef = TypedDict(
    "ListMetricAttributionsRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

MetricAttributionSummaryOutputTypeDef = TypedDict(
    "MetricAttributionSummaryOutputTypeDef",
    {
        "name": str,
        "metricAttributionArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
)

ListRecipesRequestListRecipesPaginateTypeDef = TypedDict(
    "ListRecipesRequestListRecipesPaginateTypeDef",
    {
        "recipeProvider": Literal["SERVICE"],
        "domain": DomainType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListRecipesRequestRequestTypeDef = TypedDict(
    "ListRecipesRequestRequestTypeDef",
    {
        "recipeProvider": Literal["SERVICE"],
        "nextToken": str,
        "maxResults": int,
        "domain": DomainType,
    },
    total=False,
)

RecipeSummaryOutputTypeDef = TypedDict(
    "RecipeSummaryOutputTypeDef",
    {
        "name": str,
        "recipeArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "domain": DomainType,
    },
)

ListRecommendersRequestListRecommendersPaginateTypeDef = TypedDict(
    "ListRecommendersRequestListRecommendersPaginateTypeDef",
    {
        "datasetGroupArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListRecommendersRequestRequestTypeDef = TypedDict(
    "ListRecommendersRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListSchemasRequestListSchemasPaginateTypeDef = TypedDict(
    "ListSchemasRequestListSchemasPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSchemasRequestRequestTypeDef = TypedDict(
    "ListSchemasRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef = TypedDict(
    "ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef",
    {
        "solutionArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSolutionVersionsRequestRequestTypeDef = TypedDict(
    "ListSolutionVersionsRequestRequestTypeDef",
    {
        "solutionArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

SolutionVersionSummaryOutputTypeDef = TypedDict(
    "SolutionVersionSummaryOutputTypeDef",
    {
        "solutionVersionArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
)

ListSolutionsRequestListSolutionsPaginateTypeDef = TypedDict(
    "ListSolutionsRequestListSolutionsPaginateTypeDef",
    {
        "datasetGroupArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSolutionsRequestRequestTypeDef = TypedDict(
    "ListSolutionsRequestRequestTypeDef",
    {
        "datasetGroupArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

SolutionSummaryOutputTypeDef = TypedDict(
    "SolutionSummaryOutputTypeDef",
    {
        "name": str,
        "solutionArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "recipeArn": str,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "tagKey": str,
        "tagValue": str,
    },
)

OptimizationObjectiveOutputTypeDef = TypedDict(
    "OptimizationObjectiveOutputTypeDef",
    {
        "itemAttribute": str,
        "objectiveSensitivity": ObjectiveSensitivityType,
    },
)

OptimizationObjectiveTypeDef = TypedDict(
    "OptimizationObjectiveTypeDef",
    {
        "itemAttribute": str,
        "objectiveSensitivity": ObjectiveSensitivityType,
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

TrainingDataConfigOutputTypeDef = TypedDict(
    "TrainingDataConfigOutputTypeDef",
    {
        "excludedDatasetColumns": Dict[str, List[str]],
    },
)

TrainingDataConfigTypeDef = TypedDict(
    "TrainingDataConfigTypeDef",
    {
        "excludedDatasetColumns": Mapping[str, Sequence[str]],
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

TunedHPOParamsOutputTypeDef = TypedDict(
    "TunedHPOParamsOutputTypeDef",
    {
        "algorithmHyperParameters": Dict[str, str],
    },
)

StartRecommenderRequestRequestTypeDef = TypedDict(
    "StartRecommenderRequestRequestTypeDef",
    {
        "recommenderArn": str,
    },
)

StartRecommenderResponseOutputTypeDef = TypedDict(
    "StartRecommenderResponseOutputTypeDef",
    {
        "recommenderArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopRecommenderRequestRequestTypeDef = TypedDict(
    "StopRecommenderRequestRequestTypeDef",
    {
        "recommenderArn": str,
    },
)

StopRecommenderResponseOutputTypeDef = TypedDict(
    "StopRecommenderResponseOutputTypeDef",
    {
        "recommenderArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopSolutionVersionCreationRequestRequestTypeDef = TypedDict(
    "StopSolutionVersionCreationRequestRequestTypeDef",
    {
        "solutionVersionArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateCampaignResponseOutputTypeDef = TypedDict(
    "UpdateCampaignResponseOutputTypeDef",
    {
        "campaignArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateDatasetRequestRequestTypeDef = TypedDict(
    "UpdateDatasetRequestRequestTypeDef",
    {
        "datasetArn": str,
        "schemaArn": str,
    },
)

UpdateDatasetResponseOutputTypeDef = TypedDict(
    "UpdateDatasetResponseOutputTypeDef",
    {
        "datasetArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateMetricAttributionResponseOutputTypeDef = TypedDict(
    "UpdateMetricAttributionResponseOutputTypeDef",
    {
        "metricAttributionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateRecommenderResponseOutputTypeDef = TypedDict(
    "UpdateRecommenderResponseOutputTypeDef",
    {
        "recommenderArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchInferenceJobInputTypeDef = TypedDict(
    "BatchInferenceJobInputTypeDef",
    {
        "s3DataSource": S3DataConfigTypeDef,
    },
)

BatchInferenceJobOutputTypeDef = TypedDict(
    "BatchInferenceJobOutputTypeDef",
    {
        "s3DataDestination": S3DataConfigTypeDef,
    },
)

BatchSegmentJobInputTypeDef = TypedDict(
    "BatchSegmentJobInputTypeDef",
    {
        "s3DataSource": S3DataConfigTypeDef,
    },
)

BatchSegmentJobOutputTypeDef = TypedDict(
    "BatchSegmentJobOutputTypeDef",
    {
        "s3DataDestination": S3DataConfigTypeDef,
    },
)

DatasetExportJobOutputTypeDef = TypedDict(
    "DatasetExportJobOutputTypeDef",
    {
        "s3DataDestination": S3DataConfigTypeDef,
    },
)

_RequiredMetricAttributionOutputTypeDef = TypedDict(
    "_RequiredMetricAttributionOutputTypeDef",
    {
        "roleArn": str,
    },
)
_OptionalMetricAttributionOutputTypeDef = TypedDict(
    "_OptionalMetricAttributionOutputTypeDef",
    {
        "s3DataDestination": S3DataConfigTypeDef,
    },
    total=False,
)

class MetricAttributionOutputTypeDef(
    _RequiredMetricAttributionOutputTypeDef, _OptionalMetricAttributionOutputTypeDef
):
    pass

ListBatchInferenceJobsResponseOutputTypeDef = TypedDict(
    "ListBatchInferenceJobsResponseOutputTypeDef",
    {
        "batchInferenceJobs": List[BatchInferenceJobSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBatchSegmentJobsResponseOutputTypeDef = TypedDict(
    "ListBatchSegmentJobsResponseOutputTypeDef",
    {
        "batchSegmentJobs": List[BatchSegmentJobSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CampaignUpdateSummaryOutputTypeDef = TypedDict(
    "CampaignUpdateSummaryOutputTypeDef",
    {
        "solutionVersionArn": str,
        "minProvisionedTPS": int,
        "campaignConfig": CampaignConfigOutputTypeDef,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

_RequiredUpdateCampaignRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCampaignRequestRequestTypeDef",
    {
        "campaignArn": str,
    },
)
_OptionalUpdateCampaignRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCampaignRequestRequestTypeDef",
    {
        "solutionVersionArn": str,
        "minProvisionedTPS": int,
        "campaignConfig": CampaignConfigTypeDef,
    },
    total=False,
)

class UpdateCampaignRequestRequestTypeDef(
    _RequiredUpdateCampaignRequestRequestTypeDef, _OptionalUpdateCampaignRequestRequestTypeDef
):
    pass

ListCampaignsResponseOutputTypeDef = TypedDict(
    "ListCampaignsResponseOutputTypeDef",
    {
        "campaigns": List[CampaignSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateCampaignRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCampaignRequestRequestTypeDef",
    {
        "name": str,
        "solutionVersionArn": str,
    },
)
_OptionalCreateCampaignRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCampaignRequestRequestTypeDef",
    {
        "minProvisionedTPS": int,
        "campaignConfig": CampaignConfigTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateCampaignRequestRequestTypeDef(
    _RequiredCreateCampaignRequestRequestTypeDef, _OptionalCreateCampaignRequestRequestTypeDef
):
    pass

_RequiredCreateDatasetGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetGroupRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateDatasetGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetGroupRequestRequestTypeDef",
    {
        "roleArn": str,
        "kmsKeyArn": str,
        "domain": DomainType,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateDatasetGroupRequestRequestTypeDef(
    _RequiredCreateDatasetGroupRequestRequestTypeDef,
    _OptionalCreateDatasetGroupRequestRequestTypeDef,
):
    pass

_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "name": str,
        "schemaArn": str,
        "datasetGroupArn": str,
        "datasetType": str,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass

_RequiredCreateEventTrackerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEventTrackerRequestRequestTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
    },
)
_OptionalCreateEventTrackerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEventTrackerRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEventTrackerRequestRequestTypeDef(
    _RequiredCreateEventTrackerRequestRequestTypeDef,
    _OptionalCreateEventTrackerRequestRequestTypeDef,
):
    pass

_RequiredCreateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFilterRequestRequestTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
        "filterExpression": str,
    },
)
_OptionalCreateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFilterRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateFilterRequestRequestTypeDef(
    _RequiredCreateFilterRequestRequestTypeDef, _OptionalCreateFilterRequestRequestTypeDef
):
    pass

_RequiredCreateSolutionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSolutionVersionRequestRequestTypeDef",
    {
        "solutionArn": str,
    },
)
_OptionalCreateSolutionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSolutionVersionRequestRequestTypeDef",
    {
        "name": str,
        "trainingMode": TrainingModeType,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateSolutionVersionRequestRequestTypeDef(
    _RequiredCreateSolutionVersionRequestRequestTypeDef,
    _OptionalCreateSolutionVersionRequestRequestTypeDef,
):
    pass

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateDatasetImportJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetImportJobRequestRequestTypeDef",
    {
        "jobName": str,
        "datasetArn": str,
        "dataSource": DataSourceTypeDef,
        "roleArn": str,
    },
)
_OptionalCreateDatasetImportJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetImportJobRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
        "importMode": ImportModeType,
        "publishAttributionMetricsToS3": bool,
    },
    total=False,
)

class CreateDatasetImportJobRequestRequestTypeDef(
    _RequiredCreateDatasetImportJobRequestRequestTypeDef,
    _OptionalCreateDatasetImportJobRequestRequestTypeDef,
):
    pass

DatasetImportJobOutputTypeDef = TypedDict(
    "DatasetImportJobOutputTypeDef",
    {
        "jobName": str,
        "datasetImportJobArn": str,
        "datasetArn": str,
        "dataSource": DataSourceOutputTypeDef,
        "roleArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "importMode": ImportModeType,
        "publishAttributionMetricsToS3": bool,
    },
)

ListDatasetExportJobsResponseOutputTypeDef = TypedDict(
    "ListDatasetExportJobsResponseOutputTypeDef",
    {
        "datasetExportJobs": List[DatasetExportJobSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDatasetGroupResponseOutputTypeDef = TypedDict(
    "DescribeDatasetGroupResponseOutputTypeDef",
    {
        "datasetGroup": DatasetGroupOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetGroupsResponseOutputTypeDef = TypedDict(
    "ListDatasetGroupsResponseOutputTypeDef",
    {
        "datasetGroups": List[DatasetGroupSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetImportJobsResponseOutputTypeDef = TypedDict(
    "ListDatasetImportJobsResponseOutputTypeDef",
    {
        "datasetImportJobs": List[DatasetImportJobSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatasetOutputTypeDef = TypedDict(
    "DatasetOutputTypeDef",
    {
        "name": str,
        "datasetArn": str,
        "datasetGroupArn": str,
        "datasetType": str,
        "schemaArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestDatasetUpdate": DatasetUpdateSummaryOutputTypeDef,
    },
)

DescribeSchemaResponseOutputTypeDef = TypedDict(
    "DescribeSchemaResponseOutputTypeDef",
    {
        "schema": DatasetSchemaOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSchemasResponseOutputTypeDef = TypedDict(
    "ListSchemasResponseOutputTypeDef",
    {
        "schemas": List[DatasetSchemaSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetsResponseOutputTypeDef = TypedDict(
    "ListDatasetsResponseOutputTypeDef",
    {
        "datasets": List[DatasetSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DefaultHyperParameterRangesOutputTypeDef = TypedDict(
    "DefaultHyperParameterRangesOutputTypeDef",
    {
        "integerHyperParameterRanges": List[DefaultIntegerHyperParameterRangeOutputTypeDef],
        "continuousHyperParameterRanges": List[DefaultContinuousHyperParameterRangeOutputTypeDef],
        "categoricalHyperParameterRanges": List[DefaultCategoricalHyperParameterRangeOutputTypeDef],
    },
)

DescribeEventTrackerResponseOutputTypeDef = TypedDict(
    "DescribeEventTrackerResponseOutputTypeDef",
    {
        "eventTracker": EventTrackerOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFeatureTransformationResponseOutputTypeDef = TypedDict(
    "DescribeFeatureTransformationResponseOutputTypeDef",
    {
        "featureTransformation": FeatureTransformationOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFilterResponseOutputTypeDef = TypedDict(
    "DescribeFilterResponseOutputTypeDef",
    {
        "filter": FilterOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecipeResponseOutputTypeDef = TypedDict(
    "DescribeRecipeResponseOutputTypeDef",
    {
        "recipe": RecipeOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEventTrackersResponseOutputTypeDef = TypedDict(
    "ListEventTrackersResponseOutputTypeDef",
    {
        "eventTrackers": List[EventTrackerSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFiltersResponseOutputTypeDef = TypedDict(
    "ListFiltersResponseOutputTypeDef",
    {
        "Filters": List[FilterSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HyperParameterRangesOutputTypeDef = TypedDict(
    "HyperParameterRangesOutputTypeDef",
    {
        "integerHyperParameterRanges": List[IntegerHyperParameterRangeOutputTypeDef],
        "continuousHyperParameterRanges": List[ContinuousHyperParameterRangeOutputTypeDef],
        "categoricalHyperParameterRanges": List[CategoricalHyperParameterRangeOutputTypeDef],
    },
)

HyperParameterRangesTypeDef = TypedDict(
    "HyperParameterRangesTypeDef",
    {
        "integerHyperParameterRanges": Sequence[IntegerHyperParameterRangeTypeDef],
        "continuousHyperParameterRanges": Sequence[ContinuousHyperParameterRangeTypeDef],
        "categoricalHyperParameterRanges": Sequence[CategoricalHyperParameterRangeTypeDef],
    },
    total=False,
)

ListMetricAttributionMetricsResponseOutputTypeDef = TypedDict(
    "ListMetricAttributionMetricsResponseOutputTypeDef",
    {
        "metrics": List[MetricAttributeOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMetricAttributionsResponseOutputTypeDef = TypedDict(
    "ListMetricAttributionsResponseOutputTypeDef",
    {
        "metricAttributions": List[MetricAttributionSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRecipesResponseOutputTypeDef = TypedDict(
    "ListRecipesResponseOutputTypeDef",
    {
        "recipes": List[RecipeSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSolutionVersionsResponseOutputTypeDef = TypedDict(
    "ListSolutionVersionsResponseOutputTypeDef",
    {
        "solutionVersions": List[SolutionVersionSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSolutionsResponseOutputTypeDef = TypedDict(
    "ListSolutionsResponseOutputTypeDef",
    {
        "solutions": List[SolutionSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceResponseOutputTypeDef = TypedDict(
    "ListTagsForResourceResponseOutputTypeDef",
    {
        "tags": List[TagOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommenderConfigOutputTypeDef = TypedDict(
    "RecommenderConfigOutputTypeDef",
    {
        "itemExplorationConfig": Dict[str, str],
        "minRecommendationRequestsPerSecond": int,
        "trainingDataConfig": TrainingDataConfigOutputTypeDef,
    },
)

RecommenderConfigTypeDef = TypedDict(
    "RecommenderConfigTypeDef",
    {
        "itemExplorationConfig": Mapping[str, str],
        "minRecommendationRequestsPerSecond": int,
        "trainingDataConfig": TrainingDataConfigTypeDef,
    },
    total=False,
)

_RequiredCreateBatchInferenceJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBatchInferenceJobRequestRequestTypeDef",
    {
        "jobName": str,
        "solutionVersionArn": str,
        "jobInput": BatchInferenceJobInputTypeDef,
        "jobOutput": BatchInferenceJobOutputTypeDef,
        "roleArn": str,
    },
)
_OptionalCreateBatchInferenceJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBatchInferenceJobRequestRequestTypeDef",
    {
        "filterArn": str,
        "numResults": int,
        "batchInferenceJobConfig": BatchInferenceJobConfigTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateBatchInferenceJobRequestRequestTypeDef(
    _RequiredCreateBatchInferenceJobRequestRequestTypeDef,
    _OptionalCreateBatchInferenceJobRequestRequestTypeDef,
):
    pass

DescribeBatchInferenceJobResponseOutputTypeDef = TypedDict(
    "DescribeBatchInferenceJobResponseOutputTypeDef",
    {
        "batchInferenceJob": BatchInferenceJobOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateBatchSegmentJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBatchSegmentJobRequestRequestTypeDef",
    {
        "jobName": str,
        "solutionVersionArn": str,
        "jobInput": BatchSegmentJobInputTypeDef,
        "jobOutput": BatchSegmentJobOutputTypeDef,
        "roleArn": str,
    },
)
_OptionalCreateBatchSegmentJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBatchSegmentJobRequestRequestTypeDef",
    {
        "filterArn": str,
        "numResults": int,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateBatchSegmentJobRequestRequestTypeDef(
    _RequiredCreateBatchSegmentJobRequestRequestTypeDef,
    _OptionalCreateBatchSegmentJobRequestRequestTypeDef,
):
    pass

DescribeBatchSegmentJobResponseOutputTypeDef = TypedDict(
    "DescribeBatchSegmentJobResponseOutputTypeDef",
    {
        "batchSegmentJob": BatchSegmentJobOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateDatasetExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetExportJobRequestRequestTypeDef",
    {
        "jobName": str,
        "datasetArn": str,
        "roleArn": str,
        "jobOutput": DatasetExportJobOutputTypeDef,
    },
)
_OptionalCreateDatasetExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetExportJobRequestRequestTypeDef",
    {
        "ingestionMode": IngestionModeType,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateDatasetExportJobRequestRequestTypeDef(
    _RequiredCreateDatasetExportJobRequestRequestTypeDef,
    _OptionalCreateDatasetExportJobRequestRequestTypeDef,
):
    pass

DescribeDatasetExportJobResponseOutputTypeDef = TypedDict(
    "DescribeDatasetExportJobResponseOutputTypeDef",
    {
        "datasetExportJob": DatasetExportJobOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMetricAttributionRequestRequestTypeDef = TypedDict(
    "CreateMetricAttributionRequestRequestTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
        "metrics": Sequence[MetricAttributeTypeDef],
        "metricsOutputConfig": MetricAttributionOutputTypeDef,
    },
)

DescribeMetricAttributionResponseOutputTypeDef = TypedDict(
    "DescribeMetricAttributionResponseOutputTypeDef",
    {
        "metricAttribution": MetricAttributionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateMetricAttributionRequestRequestTypeDef = TypedDict(
    "UpdateMetricAttributionRequestRequestTypeDef",
    {
        "addMetrics": Sequence[MetricAttributeTypeDef],
        "removeMetrics": Sequence[str],
        "metricsOutputConfig": MetricAttributionOutputTypeDef,
        "metricAttributionArn": str,
    },
    total=False,
)

CampaignOutputTypeDef = TypedDict(
    "CampaignOutputTypeDef",
    {
        "name": str,
        "campaignArn": str,
        "solutionVersionArn": str,
        "minProvisionedTPS": int,
        "campaignConfig": CampaignConfigOutputTypeDef,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestCampaignUpdate": CampaignUpdateSummaryOutputTypeDef,
    },
)

DescribeDatasetImportJobResponseOutputTypeDef = TypedDict(
    "DescribeDatasetImportJobResponseOutputTypeDef",
    {
        "datasetImportJob": DatasetImportJobOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDatasetResponseOutputTypeDef = TypedDict(
    "DescribeDatasetResponseOutputTypeDef",
    {
        "dataset": DatasetOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AlgorithmOutputTypeDef = TypedDict(
    "AlgorithmOutputTypeDef",
    {
        "name": str,
        "algorithmArn": str,
        "algorithmImage": AlgorithmImageOutputTypeDef,
        "defaultHyperParameters": Dict[str, str],
        "defaultHyperParameterRanges": DefaultHyperParameterRangesOutputTypeDef,
        "defaultResourceConfig": Dict[str, str],
        "trainingInputMode": str,
        "roleArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

HPOConfigOutputTypeDef = TypedDict(
    "HPOConfigOutputTypeDef",
    {
        "hpoObjective": HPOObjectiveOutputTypeDef,
        "hpoResourceConfig": HPOResourceConfigOutputTypeDef,
        "algorithmHyperParameterRanges": HyperParameterRangesOutputTypeDef,
    },
)

HPOConfigTypeDef = TypedDict(
    "HPOConfigTypeDef",
    {
        "hpoObjective": HPOObjectiveTypeDef,
        "hpoResourceConfig": HPOResourceConfigTypeDef,
        "algorithmHyperParameterRanges": HyperParameterRangesTypeDef,
    },
    total=False,
)

RecommenderSummaryOutputTypeDef = TypedDict(
    "RecommenderSummaryOutputTypeDef",
    {
        "name": str,
        "recommenderArn": str,
        "datasetGroupArn": str,
        "recipeArn": str,
        "recommenderConfig": RecommenderConfigOutputTypeDef,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

RecommenderUpdateSummaryOutputTypeDef = TypedDict(
    "RecommenderUpdateSummaryOutputTypeDef",
    {
        "recommenderConfig": RecommenderConfigOutputTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "status": str,
        "failureReason": str,
    },
)

_RequiredCreateRecommenderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRecommenderRequestRequestTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
        "recipeArn": str,
    },
)
_OptionalCreateRecommenderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRecommenderRequestRequestTypeDef",
    {
        "recommenderConfig": RecommenderConfigTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateRecommenderRequestRequestTypeDef(
    _RequiredCreateRecommenderRequestRequestTypeDef, _OptionalCreateRecommenderRequestRequestTypeDef
):
    pass

UpdateRecommenderRequestRequestTypeDef = TypedDict(
    "UpdateRecommenderRequestRequestTypeDef",
    {
        "recommenderArn": str,
        "recommenderConfig": RecommenderConfigTypeDef,
    },
)

DescribeCampaignResponseOutputTypeDef = TypedDict(
    "DescribeCampaignResponseOutputTypeDef",
    {
        "campaign": CampaignOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeAlgorithmResponseOutputTypeDef = TypedDict(
    "DescribeAlgorithmResponseOutputTypeDef",
    {
        "algorithm": AlgorithmOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SolutionConfigOutputTypeDef = TypedDict(
    "SolutionConfigOutputTypeDef",
    {
        "eventValueThreshold": str,
        "hpoConfig": HPOConfigOutputTypeDef,
        "algorithmHyperParameters": Dict[str, str],
        "featureTransformationParameters": Dict[str, str],
        "autoMLConfig": AutoMLConfigOutputTypeDef,
        "optimizationObjective": OptimizationObjectiveOutputTypeDef,
        "trainingDataConfig": TrainingDataConfigOutputTypeDef,
    },
)

SolutionConfigTypeDef = TypedDict(
    "SolutionConfigTypeDef",
    {
        "eventValueThreshold": str,
        "hpoConfig": HPOConfigTypeDef,
        "algorithmHyperParameters": Mapping[str, str],
        "featureTransformationParameters": Mapping[str, str],
        "autoMLConfig": AutoMLConfigTypeDef,
        "optimizationObjective": OptimizationObjectiveTypeDef,
        "trainingDataConfig": TrainingDataConfigTypeDef,
    },
    total=False,
)

ListRecommendersResponseOutputTypeDef = TypedDict(
    "ListRecommendersResponseOutputTypeDef",
    {
        "recommenders": List[RecommenderSummaryOutputTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommenderOutputTypeDef = TypedDict(
    "RecommenderOutputTypeDef",
    {
        "recommenderArn": str,
        "datasetGroupArn": str,
        "name": str,
        "recipeArn": str,
        "recommenderConfig": RecommenderConfigOutputTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "status": str,
        "failureReason": str,
        "latestRecommenderUpdate": RecommenderUpdateSummaryOutputTypeDef,
        "modelMetrics": Dict[str, float],
    },
)

SolutionOutputTypeDef = TypedDict(
    "SolutionOutputTypeDef",
    {
        "name": str,
        "solutionArn": str,
        "performHPO": bool,
        "performAutoML": bool,
        "recipeArn": str,
        "datasetGroupArn": str,
        "eventType": str,
        "solutionConfig": SolutionConfigOutputTypeDef,
        "autoMLResult": AutoMLResultOutputTypeDef,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestSolutionVersion": SolutionVersionSummaryOutputTypeDef,
    },
)

SolutionVersionOutputTypeDef = TypedDict(
    "SolutionVersionOutputTypeDef",
    {
        "name": str,
        "solutionVersionArn": str,
        "solutionArn": str,
        "performHPO": bool,
        "performAutoML": bool,
        "recipeArn": str,
        "eventType": str,
        "datasetGroupArn": str,
        "solutionConfig": SolutionConfigOutputTypeDef,
        "trainingHours": float,
        "trainingMode": TrainingModeType,
        "tunedHPOParams": TunedHPOParamsOutputTypeDef,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

_RequiredCreateSolutionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSolutionRequestRequestTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
    },
)
_OptionalCreateSolutionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSolutionRequestRequestTypeDef",
    {
        "performHPO": bool,
        "performAutoML": bool,
        "recipeArn": str,
        "eventType": str,
        "solutionConfig": SolutionConfigTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateSolutionRequestRequestTypeDef(
    _RequiredCreateSolutionRequestRequestTypeDef, _OptionalCreateSolutionRequestRequestTypeDef
):
    pass

DescribeRecommenderResponseOutputTypeDef = TypedDict(
    "DescribeRecommenderResponseOutputTypeDef",
    {
        "recommender": RecommenderOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSolutionResponseOutputTypeDef = TypedDict(
    "DescribeSolutionResponseOutputTypeDef",
    {
        "solution": SolutionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSolutionVersionResponseOutputTypeDef = TypedDict(
    "DescribeSolutionVersionResponseOutputTypeDef",
    {
        "solutionVersion": SolutionVersionOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
