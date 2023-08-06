"""
Type annotations for personalize service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/type_defs/)

Usage::

    ```python
    from mypy_boto3_personalize.type_defs import AlgorithmImageTypeDef

    data: AlgorithmImageTypeDef = {...}
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
    "AlgorithmImageTypeDef",
    "AutoMLConfigTypeDef",
    "AutoMLResultTypeDef",
    "BatchInferenceJobConfigTypeDef",
    "S3DataConfigTypeDef",
    "BatchInferenceJobSummaryTypeDef",
    "BatchSegmentJobSummaryTypeDef",
    "CampaignConfigTypeDef",
    "CampaignSummaryTypeDef",
    "CategoricalHyperParameterRangeTypeDef",
    "ContinuousHyperParameterRangeTypeDef",
    "TagTypeDef",
    "CreateBatchInferenceJobResponseTypeDef",
    "CreateBatchSegmentJobResponseTypeDef",
    "CreateCampaignResponseTypeDef",
    "CreateDatasetExportJobResponseTypeDef",
    "CreateDatasetGroupResponseTypeDef",
    "DataSourceTypeDef",
    "CreateDatasetImportJobResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateEventTrackerResponseTypeDef",
    "CreateFilterResponseTypeDef",
    "MetricAttributeTypeDef",
    "CreateMetricAttributionResponseTypeDef",
    "CreateRecommenderResponseTypeDef",
    "CreateSchemaRequestRequestTypeDef",
    "CreateSchemaResponseTypeDef",
    "CreateSolutionResponseTypeDef",
    "CreateSolutionVersionResponseTypeDef",
    "DatasetExportJobSummaryTypeDef",
    "DatasetGroupSummaryTypeDef",
    "DatasetGroupTypeDef",
    "DatasetImportJobSummaryTypeDef",
    "DatasetSchemaSummaryTypeDef",
    "DatasetSchemaTypeDef",
    "DatasetSummaryTypeDef",
    "DatasetUpdateSummaryTypeDef",
    "DefaultCategoricalHyperParameterRangeTypeDef",
    "DefaultContinuousHyperParameterRangeTypeDef",
    "DefaultIntegerHyperParameterRangeTypeDef",
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
    "EventTrackerTypeDef",
    "DescribeFeatureTransformationRequestRequestTypeDef",
    "FeatureTransformationTypeDef",
    "DescribeFilterRequestRequestTypeDef",
    "FilterTypeDef",
    "DescribeMetricAttributionRequestRequestTypeDef",
    "DescribeRecipeRequestRequestTypeDef",
    "RecipeTypeDef",
    "DescribeRecommenderRequestRequestTypeDef",
    "DescribeSchemaRequestRequestTypeDef",
    "DescribeSolutionRequestRequestTypeDef",
    "DescribeSolutionVersionRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventTrackerSummaryTypeDef",
    "FilterSummaryTypeDef",
    "GetSolutionMetricsRequestRequestTypeDef",
    "GetSolutionMetricsResponseTypeDef",
    "HPOObjectiveTypeDef",
    "HPOResourceConfigTypeDef",
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
    "ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef",
    "ListMetricAttributionsRequestRequestTypeDef",
    "MetricAttributionSummaryTypeDef",
    "ListRecipesRequestListRecipesPaginateTypeDef",
    "ListRecipesRequestRequestTypeDef",
    "RecipeSummaryTypeDef",
    "ListRecommendersRequestListRecommendersPaginateTypeDef",
    "ListRecommendersRequestRequestTypeDef",
    "ListSchemasRequestListSchemasPaginateTypeDef",
    "ListSchemasRequestRequestTypeDef",
    "ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef",
    "ListSolutionVersionsRequestRequestTypeDef",
    "SolutionVersionSummaryTypeDef",
    "ListSolutionsRequestListSolutionsPaginateTypeDef",
    "ListSolutionsRequestRequestTypeDef",
    "SolutionSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "OptimizationObjectiveTypeDef",
    "PaginatorConfigTypeDef",
    "TrainingDataConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TunedHPOParamsTypeDef",
    "StartRecommenderRequestRequestTypeDef",
    "StartRecommenderResponseTypeDef",
    "StopRecommenderRequestRequestTypeDef",
    "StopRecommenderResponseTypeDef",
    "StopSolutionVersionCreationRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCampaignResponseTypeDef",
    "UpdateDatasetRequestRequestTypeDef",
    "UpdateDatasetResponseTypeDef",
    "UpdateMetricAttributionResponseTypeDef",
    "UpdateRecommenderResponseTypeDef",
    "BatchInferenceJobInputTypeDef",
    "BatchInferenceJobOutputTypeDef",
    "BatchSegmentJobInputTypeDef",
    "BatchSegmentJobOutputTypeDef",
    "DatasetExportJobOutputTypeDef",
    "MetricAttributionOutputTypeDef",
    "ListBatchInferenceJobsResponseTypeDef",
    "ListBatchSegmentJobsResponseTypeDef",
    "CampaignUpdateSummaryTypeDef",
    "UpdateCampaignRequestRequestTypeDef",
    "ListCampaignsResponseTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "CreateDatasetGroupRequestRequestTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateEventTrackerRequestRequestTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "CreateSolutionVersionRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateDatasetImportJobRequestRequestTypeDef",
    "DatasetImportJobTypeDef",
    "ListMetricAttributionMetricsResponseTypeDef",
    "ListDatasetExportJobsResponseTypeDef",
    "ListDatasetGroupsResponseTypeDef",
    "DescribeDatasetGroupResponseTypeDef",
    "ListDatasetImportJobsResponseTypeDef",
    "ListSchemasResponseTypeDef",
    "DescribeSchemaResponseTypeDef",
    "ListDatasetsResponseTypeDef",
    "DatasetTypeDef",
    "DefaultHyperParameterRangesTypeDef",
    "DescribeEventTrackerResponseTypeDef",
    "DescribeFeatureTransformationResponseTypeDef",
    "DescribeFilterResponseTypeDef",
    "DescribeRecipeResponseTypeDef",
    "ListEventTrackersResponseTypeDef",
    "ListFiltersResponseTypeDef",
    "HyperParameterRangesTypeDef",
    "ListMetricAttributionsResponseTypeDef",
    "ListRecipesResponseTypeDef",
    "ListSolutionVersionsResponseTypeDef",
    "ListSolutionsResponseTypeDef",
    "RecommenderConfigTypeDef",
    "BatchInferenceJobTypeDef",
    "CreateBatchInferenceJobRequestRequestTypeDef",
    "BatchSegmentJobTypeDef",
    "CreateBatchSegmentJobRequestRequestTypeDef",
    "CreateDatasetExportJobRequestRequestTypeDef",
    "DatasetExportJobTypeDef",
    "CreateMetricAttributionRequestRequestTypeDef",
    "MetricAttributionTypeDef",
    "UpdateMetricAttributionRequestRequestTypeDef",
    "CampaignTypeDef",
    "DescribeDatasetImportJobResponseTypeDef",
    "DescribeDatasetResponseTypeDef",
    "AlgorithmTypeDef",
    "HPOConfigTypeDef",
    "CreateRecommenderRequestRequestTypeDef",
    "RecommenderSummaryTypeDef",
    "RecommenderUpdateSummaryTypeDef",
    "UpdateRecommenderRequestRequestTypeDef",
    "DescribeBatchInferenceJobResponseTypeDef",
    "DescribeBatchSegmentJobResponseTypeDef",
    "DescribeDatasetExportJobResponseTypeDef",
    "DescribeMetricAttributionResponseTypeDef",
    "DescribeCampaignResponseTypeDef",
    "DescribeAlgorithmResponseTypeDef",
    "SolutionConfigTypeDef",
    "ListRecommendersResponseTypeDef",
    "RecommenderTypeDef",
    "CreateSolutionRequestRequestTypeDef",
    "SolutionTypeDef",
    "SolutionVersionTypeDef",
    "DescribeRecommenderResponseTypeDef",
    "DescribeSolutionResponseTypeDef",
    "DescribeSolutionVersionResponseTypeDef",
)

AlgorithmImageTypeDef = TypedDict(
    "AlgorithmImageTypeDef",
    {
        "name": str,
        "dockerURI": str,
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

AutoMLResultTypeDef = TypedDict(
    "AutoMLResultTypeDef",
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

BatchInferenceJobSummaryTypeDef = TypedDict(
    "BatchInferenceJobSummaryTypeDef",
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

BatchSegmentJobSummaryTypeDef = TypedDict(
    "BatchSegmentJobSummaryTypeDef",
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

CampaignConfigTypeDef = TypedDict(
    "CampaignConfigTypeDef",
    {
        "itemExplorationConfig": Mapping[str, str],
    },
    total=False,
)

CampaignSummaryTypeDef = TypedDict(
    "CampaignSummaryTypeDef",
    {
        "name": str,
        "campaignArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
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

CreateBatchInferenceJobResponseTypeDef = TypedDict(
    "CreateBatchInferenceJobResponseTypeDef",
    {
        "batchInferenceJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateBatchSegmentJobResponseTypeDef = TypedDict(
    "CreateBatchSegmentJobResponseTypeDef",
    {
        "batchSegmentJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef",
    {
        "campaignArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetExportJobResponseTypeDef = TypedDict(
    "CreateDatasetExportJobResponseTypeDef",
    {
        "datasetExportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetGroupResponseTypeDef = TypedDict(
    "CreateDatasetGroupResponseTypeDef",
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

CreateDatasetImportJobResponseTypeDef = TypedDict(
    "CreateDatasetImportJobResponseTypeDef",
    {
        "datasetImportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "datasetArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEventTrackerResponseTypeDef = TypedDict(
    "CreateEventTrackerResponseTypeDef",
    {
        "eventTrackerArn": str,
        "trackingId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateFilterResponseTypeDef = TypedDict(
    "CreateFilterResponseTypeDef",
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

CreateMetricAttributionResponseTypeDef = TypedDict(
    "CreateMetricAttributionResponseTypeDef",
    {
        "metricAttributionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateRecommenderResponseTypeDef = TypedDict(
    "CreateRecommenderResponseTypeDef",
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

CreateSchemaResponseTypeDef = TypedDict(
    "CreateSchemaResponseTypeDef",
    {
        "schemaArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateSolutionResponseTypeDef = TypedDict(
    "CreateSolutionResponseTypeDef",
    {
        "solutionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateSolutionVersionResponseTypeDef = TypedDict(
    "CreateSolutionVersionResponseTypeDef",
    {
        "solutionVersionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatasetExportJobSummaryTypeDef = TypedDict(
    "DatasetExportJobSummaryTypeDef",
    {
        "datasetExportJobArn": str,
        "jobName": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
)

DatasetGroupSummaryTypeDef = TypedDict(
    "DatasetGroupSummaryTypeDef",
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

DatasetGroupTypeDef = TypedDict(
    "DatasetGroupTypeDef",
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

DatasetImportJobSummaryTypeDef = TypedDict(
    "DatasetImportJobSummaryTypeDef",
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

DatasetSchemaSummaryTypeDef = TypedDict(
    "DatasetSchemaSummaryTypeDef",
    {
        "name": str,
        "schemaArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "domain": DomainType,
    },
)

DatasetSchemaTypeDef = TypedDict(
    "DatasetSchemaTypeDef",
    {
        "name": str,
        "schemaArn": str,
        "schema": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "domain": DomainType,
    },
)

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "name": str,
        "datasetArn": str,
        "datasetType": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

DatasetUpdateSummaryTypeDef = TypedDict(
    "DatasetUpdateSummaryTypeDef",
    {
        "schemaArn": str,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

DefaultCategoricalHyperParameterRangeTypeDef = TypedDict(
    "DefaultCategoricalHyperParameterRangeTypeDef",
    {
        "name": str,
        "values": List[str],
        "isTunable": bool,
    },
)

DefaultContinuousHyperParameterRangeTypeDef = TypedDict(
    "DefaultContinuousHyperParameterRangeTypeDef",
    {
        "name": str,
        "minValue": float,
        "maxValue": float,
        "isTunable": bool,
    },
)

DefaultIntegerHyperParameterRangeTypeDef = TypedDict(
    "DefaultIntegerHyperParameterRangeTypeDef",
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

EventTrackerTypeDef = TypedDict(
    "EventTrackerTypeDef",
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

FeatureTransformationTypeDef = TypedDict(
    "FeatureTransformationTypeDef",
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

FilterTypeDef = TypedDict(
    "FilterTypeDef",
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

RecipeTypeDef = TypedDict(
    "RecipeTypeDef",
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

EventTrackerSummaryTypeDef = TypedDict(
    "EventTrackerSummaryTypeDef",
    {
        "name": str,
        "eventTrackerArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

FilterSummaryTypeDef = TypedDict(
    "FilterSummaryTypeDef",
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

GetSolutionMetricsResponseTypeDef = TypedDict(
    "GetSolutionMetricsResponseTypeDef",
    {
        "solutionVersionArn": str,
        "metrics": Dict[str, float],
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

MetricAttributionSummaryTypeDef = TypedDict(
    "MetricAttributionSummaryTypeDef",
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

RecipeSummaryTypeDef = TypedDict(
    "RecipeSummaryTypeDef",
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

SolutionVersionSummaryTypeDef = TypedDict(
    "SolutionVersionSummaryTypeDef",
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

SolutionSummaryTypeDef = TypedDict(
    "SolutionSummaryTypeDef",
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

TunedHPOParamsTypeDef = TypedDict(
    "TunedHPOParamsTypeDef",
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

StartRecommenderResponseTypeDef = TypedDict(
    "StartRecommenderResponseTypeDef",
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

StopRecommenderResponseTypeDef = TypedDict(
    "StopRecommenderResponseTypeDef",
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

UpdateCampaignResponseTypeDef = TypedDict(
    "UpdateCampaignResponseTypeDef",
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

UpdateDatasetResponseTypeDef = TypedDict(
    "UpdateDatasetResponseTypeDef",
    {
        "datasetArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateMetricAttributionResponseTypeDef = TypedDict(
    "UpdateMetricAttributionResponseTypeDef",
    {
        "metricAttributionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateRecommenderResponseTypeDef = TypedDict(
    "UpdateRecommenderResponseTypeDef",
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

ListBatchInferenceJobsResponseTypeDef = TypedDict(
    "ListBatchInferenceJobsResponseTypeDef",
    {
        "batchInferenceJobs": List[BatchInferenceJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBatchSegmentJobsResponseTypeDef = TypedDict(
    "ListBatchSegmentJobsResponseTypeDef",
    {
        "batchSegmentJobs": List[BatchSegmentJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CampaignUpdateSummaryTypeDef = TypedDict(
    "CampaignUpdateSummaryTypeDef",
    {
        "solutionVersionArn": str,
        "minProvisionedTPS": int,
        "campaignConfig": CampaignConfigTypeDef,
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

ListCampaignsResponseTypeDef = TypedDict(
    "ListCampaignsResponseTypeDef",
    {
        "campaigns": List[CampaignSummaryTypeDef],
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

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

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

DatasetImportJobTypeDef = TypedDict(
    "DatasetImportJobTypeDef",
    {
        "jobName": str,
        "datasetImportJobArn": str,
        "datasetArn": str,
        "dataSource": DataSourceTypeDef,
        "roleArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "importMode": ImportModeType,
        "publishAttributionMetricsToS3": bool,
    },
)

ListMetricAttributionMetricsResponseTypeDef = TypedDict(
    "ListMetricAttributionMetricsResponseTypeDef",
    {
        "metrics": List[MetricAttributeTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetExportJobsResponseTypeDef = TypedDict(
    "ListDatasetExportJobsResponseTypeDef",
    {
        "datasetExportJobs": List[DatasetExportJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetGroupsResponseTypeDef = TypedDict(
    "ListDatasetGroupsResponseTypeDef",
    {
        "datasetGroups": List[DatasetGroupSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDatasetGroupResponseTypeDef = TypedDict(
    "DescribeDatasetGroupResponseTypeDef",
    {
        "datasetGroup": DatasetGroupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetImportJobsResponseTypeDef = TypedDict(
    "ListDatasetImportJobsResponseTypeDef",
    {
        "datasetImportJobs": List[DatasetImportJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSchemasResponseTypeDef = TypedDict(
    "ListSchemasResponseTypeDef",
    {
        "schemas": List[DatasetSchemaSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSchemaResponseTypeDef = TypedDict(
    "DescribeSchemaResponseTypeDef",
    {
        "schema": DatasetSchemaTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {
        "datasets": List[DatasetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatasetTypeDef = TypedDict(
    "DatasetTypeDef",
    {
        "name": str,
        "datasetArn": str,
        "datasetGroupArn": str,
        "datasetType": str,
        "schemaArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestDatasetUpdate": DatasetUpdateSummaryTypeDef,
    },
)

DefaultHyperParameterRangesTypeDef = TypedDict(
    "DefaultHyperParameterRangesTypeDef",
    {
        "integerHyperParameterRanges": List[DefaultIntegerHyperParameterRangeTypeDef],
        "continuousHyperParameterRanges": List[DefaultContinuousHyperParameterRangeTypeDef],
        "categoricalHyperParameterRanges": List[DefaultCategoricalHyperParameterRangeTypeDef],
    },
)

DescribeEventTrackerResponseTypeDef = TypedDict(
    "DescribeEventTrackerResponseTypeDef",
    {
        "eventTracker": EventTrackerTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFeatureTransformationResponseTypeDef = TypedDict(
    "DescribeFeatureTransformationResponseTypeDef",
    {
        "featureTransformation": FeatureTransformationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFilterResponseTypeDef = TypedDict(
    "DescribeFilterResponseTypeDef",
    {
        "filter": FilterTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecipeResponseTypeDef = TypedDict(
    "DescribeRecipeResponseTypeDef",
    {
        "recipe": RecipeTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEventTrackersResponseTypeDef = TypedDict(
    "ListEventTrackersResponseTypeDef",
    {
        "eventTrackers": List[EventTrackerSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFiltersResponseTypeDef = TypedDict(
    "ListFiltersResponseTypeDef",
    {
        "Filters": List[FilterSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

ListMetricAttributionsResponseTypeDef = TypedDict(
    "ListMetricAttributionsResponseTypeDef",
    {
        "metricAttributions": List[MetricAttributionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRecipesResponseTypeDef = TypedDict(
    "ListRecipesResponseTypeDef",
    {
        "recipes": List[RecipeSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSolutionVersionsResponseTypeDef = TypedDict(
    "ListSolutionVersionsResponseTypeDef",
    {
        "solutionVersions": List[SolutionVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSolutionsResponseTypeDef = TypedDict(
    "ListSolutionsResponseTypeDef",
    {
        "solutions": List[SolutionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

BatchInferenceJobTypeDef = TypedDict(
    "BatchInferenceJobTypeDef",
    {
        "jobName": str,
        "batchInferenceJobArn": str,
        "filterArn": str,
        "failureReason": str,
        "solutionVersionArn": str,
        "numResults": int,
        "jobInput": BatchInferenceJobInputTypeDef,
        "jobOutput": BatchInferenceJobOutputTypeDef,
        "batchInferenceJobConfig": BatchInferenceJobConfigTypeDef,
        "roleArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
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

BatchSegmentJobTypeDef = TypedDict(
    "BatchSegmentJobTypeDef",
    {
        "jobName": str,
        "batchSegmentJobArn": str,
        "filterArn": str,
        "failureReason": str,
        "solutionVersionArn": str,
        "numResults": int,
        "jobInput": BatchSegmentJobInputTypeDef,
        "jobOutput": BatchSegmentJobOutputTypeDef,
        "roleArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
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

DatasetExportJobTypeDef = TypedDict(
    "DatasetExportJobTypeDef",
    {
        "jobName": str,
        "datasetExportJobArn": str,
        "datasetArn": str,
        "ingestionMode": IngestionModeType,
        "roleArn": str,
        "status": str,
        "jobOutput": DatasetExportJobOutputTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
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

MetricAttributionTypeDef = TypedDict(
    "MetricAttributionTypeDef",
    {
        "name": str,
        "metricAttributionArn": str,
        "datasetGroupArn": str,
        "metricsOutputConfig": MetricAttributionOutputTypeDef,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
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

CampaignTypeDef = TypedDict(
    "CampaignTypeDef",
    {
        "name": str,
        "campaignArn": str,
        "solutionVersionArn": str,
        "minProvisionedTPS": int,
        "campaignConfig": CampaignConfigTypeDef,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestCampaignUpdate": CampaignUpdateSummaryTypeDef,
    },
)

DescribeDatasetImportJobResponseTypeDef = TypedDict(
    "DescribeDatasetImportJobResponseTypeDef",
    {
        "datasetImportJob": DatasetImportJobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "dataset": DatasetTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AlgorithmTypeDef = TypedDict(
    "AlgorithmTypeDef",
    {
        "name": str,
        "algorithmArn": str,
        "algorithmImage": AlgorithmImageTypeDef,
        "defaultHyperParameters": Dict[str, str],
        "defaultHyperParameterRanges": DefaultHyperParameterRangesTypeDef,
        "defaultResourceConfig": Dict[str, str],
        "trainingInputMode": str,
        "roleArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
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

RecommenderSummaryTypeDef = TypedDict(
    "RecommenderSummaryTypeDef",
    {
        "name": str,
        "recommenderArn": str,
        "datasetGroupArn": str,
        "recipeArn": str,
        "recommenderConfig": RecommenderConfigTypeDef,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

RecommenderUpdateSummaryTypeDef = TypedDict(
    "RecommenderUpdateSummaryTypeDef",
    {
        "recommenderConfig": RecommenderConfigTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "status": str,
        "failureReason": str,
    },
)

UpdateRecommenderRequestRequestTypeDef = TypedDict(
    "UpdateRecommenderRequestRequestTypeDef",
    {
        "recommenderArn": str,
        "recommenderConfig": RecommenderConfigTypeDef,
    },
)

DescribeBatchInferenceJobResponseTypeDef = TypedDict(
    "DescribeBatchInferenceJobResponseTypeDef",
    {
        "batchInferenceJob": BatchInferenceJobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeBatchSegmentJobResponseTypeDef = TypedDict(
    "DescribeBatchSegmentJobResponseTypeDef",
    {
        "batchSegmentJob": BatchSegmentJobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDatasetExportJobResponseTypeDef = TypedDict(
    "DescribeDatasetExportJobResponseTypeDef",
    {
        "datasetExportJob": DatasetExportJobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeMetricAttributionResponseTypeDef = TypedDict(
    "DescribeMetricAttributionResponseTypeDef",
    {
        "metricAttribution": MetricAttributionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCampaignResponseTypeDef = TypedDict(
    "DescribeCampaignResponseTypeDef",
    {
        "campaign": CampaignTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeAlgorithmResponseTypeDef = TypedDict(
    "DescribeAlgorithmResponseTypeDef",
    {
        "algorithm": AlgorithmTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

ListRecommendersResponseTypeDef = TypedDict(
    "ListRecommendersResponseTypeDef",
    {
        "recommenders": List[RecommenderSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommenderTypeDef = TypedDict(
    "RecommenderTypeDef",
    {
        "recommenderArn": str,
        "datasetGroupArn": str,
        "name": str,
        "recipeArn": str,
        "recommenderConfig": RecommenderConfigTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "status": str,
        "failureReason": str,
        "latestRecommenderUpdate": RecommenderUpdateSummaryTypeDef,
        "modelMetrics": Dict[str, float],
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

SolutionTypeDef = TypedDict(
    "SolutionTypeDef",
    {
        "name": str,
        "solutionArn": str,
        "performHPO": bool,
        "performAutoML": bool,
        "recipeArn": str,
        "datasetGroupArn": str,
        "eventType": str,
        "solutionConfig": SolutionConfigTypeDef,
        "autoMLResult": AutoMLResultTypeDef,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestSolutionVersion": SolutionVersionSummaryTypeDef,
    },
)

SolutionVersionTypeDef = TypedDict(
    "SolutionVersionTypeDef",
    {
        "name": str,
        "solutionVersionArn": str,
        "solutionArn": str,
        "performHPO": bool,
        "performAutoML": bool,
        "recipeArn": str,
        "eventType": str,
        "datasetGroupArn": str,
        "solutionConfig": SolutionConfigTypeDef,
        "trainingHours": float,
        "trainingMode": TrainingModeType,
        "tunedHPOParams": TunedHPOParamsTypeDef,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
)

DescribeRecommenderResponseTypeDef = TypedDict(
    "DescribeRecommenderResponseTypeDef",
    {
        "recommender": RecommenderTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSolutionResponseTypeDef = TypedDict(
    "DescribeSolutionResponseTypeDef",
    {
        "solution": SolutionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSolutionVersionResponseTypeDef = TypedDict(
    "DescribeSolutionVersionResponseTypeDef",
    {
        "solutionVersion": SolutionVersionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
