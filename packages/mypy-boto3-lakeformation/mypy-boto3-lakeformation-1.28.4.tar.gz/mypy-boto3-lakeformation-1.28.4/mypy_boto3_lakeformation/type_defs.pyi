"""
Type annotations for lakeformation service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lakeformation/type_defs/)

Usage::

    ```python
    from mypy_boto3_lakeformation.type_defs import LFTagPairTypeDef

    data: LFTagPairTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ComparisonOperatorType,
    DataLakeResourceTypeType,
    FieldNameStringType,
    OptimizerTypeType,
    PermissionType,
    PermissionTypeType,
    QueryStateStringType,
    ResourceShareTypeType,
    ResourceTypeType,
    TransactionStatusFilterType,
    TransactionStatusType,
    TransactionTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "LFTagPairTypeDef",
    "ResponseMetadataTypeDef",
    "AddObjectInputTypeDef",
    "AssumeDecoratedRoleWithSAMLRequestRequestTypeDef",
    "AuditContextTypeDef",
    "ErrorDetailTypeDef",
    "DataLakePrincipalOutputTypeDef",
    "DataLakePrincipalTypeDef",
    "CancelTransactionRequestRequestTypeDef",
    "LFTagPairOutputTypeDef",
    "ColumnWildcardOutputTypeDef",
    "ColumnWildcardTypeDef",
    "CommitTransactionRequestRequestTypeDef",
    "CreateLFTagRequestRequestTypeDef",
    "RowFilterOutputTypeDef",
    "DataCellsFilterResourceOutputTypeDef",
    "DataCellsFilterResourceTypeDef",
    "RowFilterTypeDef",
    "DataLocationResourceOutputTypeDef",
    "DataLocationResourceTypeDef",
    "DatabaseResourceOutputTypeDef",
    "DatabaseResourceTypeDef",
    "DeleteDataCellsFilterRequestRequestTypeDef",
    "DeleteLFTagRequestRequestTypeDef",
    "DeleteObjectInputTypeDef",
    "VirtualObjectTypeDef",
    "DeregisterResourceRequestRequestTypeDef",
    "DescribeResourceRequestRequestTypeDef",
    "ResourceInfoTypeDef",
    "DescribeTransactionRequestRequestTypeDef",
    "TransactionDescriptionTypeDef",
    "DetailsMapTypeDef",
    "ExecutionStatisticsTypeDef",
    "ExtendTransactionRequestRequestTypeDef",
    "FilterConditionTypeDef",
    "GetDataCellsFilterRequestRequestTypeDef",
    "GetDataLakeSettingsRequestRequestTypeDef",
    "GetEffectivePermissionsForPathRequestRequestTypeDef",
    "GetLFTagRequestRequestTypeDef",
    "GetQueryStateRequestRequestTypeDef",
    "GetQueryStatisticsRequestRequestTypeDef",
    "PlanningStatisticsTypeDef",
    "GetTableObjectsRequestRequestTypeDef",
    "PartitionValueListTypeDef",
    "GetWorkUnitResultsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetWorkUnitsRequestRequestTypeDef",
    "WorkUnitRangeTypeDef",
    "LFTagKeyResourceOutputTypeDef",
    "LFTagKeyResourceTypeDef",
    "LFTagOutputTypeDef",
    "LFTagTypeDef",
    "TableResourceTypeDef",
    "ListLFTagsRequestRequestTypeDef",
    "ListTableStorageOptimizersRequestRequestTypeDef",
    "StorageOptimizerTypeDef",
    "ListTransactionsRequestRequestTypeDef",
    "TableObjectTypeDef",
    "QueryPlanningContextTypeDef",
    "RegisterResourceRequestRequestTypeDef",
    "TableResourceOutputTypeDef",
    "StartTransactionRequestRequestTypeDef",
    "UpdateLFTagRequestRequestTypeDef",
    "UpdateResourceRequestRequestTypeDef",
    "UpdateTableStorageOptimizerRequestRequestTypeDef",
    "AssumeDecoratedRoleWithSAMLResponseTypeDef",
    "CommitTransactionResponseTypeDef",
    "GetLFTagResponseTypeDef",
    "GetQueryStateResponseTypeDef",
    "GetTemporaryGluePartitionCredentialsResponseTypeDef",
    "GetTemporaryGlueTableCredentialsResponseTypeDef",
    "GetWorkUnitResultsResponseTypeDef",
    "StartQueryPlanningResponseTypeDef",
    "StartTransactionResponseTypeDef",
    "UpdateTableStorageOptimizerResponseTypeDef",
    "GetTemporaryGlueTableCredentialsRequestRequestTypeDef",
    "PrincipalPermissionsOutputTypeDef",
    "PrincipalPermissionsTypeDef",
    "ColumnLFTagTypeDef",
    "LFTagErrorTypeDef",
    "ListLFTagsResponseTypeDef",
    "TableWithColumnsResourceOutputTypeDef",
    "TableWithColumnsResourceTypeDef",
    "DataCellsFilterOutputTypeDef",
    "DataCellsFilterTypeDef",
    "TaggedDatabaseTypeDef",
    "WriteOperationTypeDef",
    "DeleteObjectsOnCancelRequestRequestTypeDef",
    "DescribeResourceResponseTypeDef",
    "ListResourcesResponseTypeDef",
    "DescribeTransactionResponseTypeDef",
    "ListTransactionsResponseTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "GetQueryStatisticsResponseTypeDef",
    "GetTemporaryGluePartitionCredentialsRequestRequestTypeDef",
    "GetWorkUnitsRequestGetWorkUnitsPaginateTypeDef",
    "ListLFTagsRequestListLFTagsPaginateTypeDef",
    "GetWorkUnitsResponseTypeDef",
    "LFTagPolicyResourceOutputTypeDef",
    "LFTagPolicyResourceTypeDef",
    "SearchDatabasesByLFTagsRequestRequestTypeDef",
    "SearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef",
    "SearchTablesByLFTagsRequestRequestTypeDef",
    "SearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef",
    "ListDataCellsFilterRequestListDataCellsFilterPaginateTypeDef",
    "ListDataCellsFilterRequestRequestTypeDef",
    "ListTableStorageOptimizersResponseTypeDef",
    "PartitionObjectsTypeDef",
    "StartQueryPlanningRequestRequestTypeDef",
    "DataLakeSettingsOutputTypeDef",
    "DataLakeSettingsTypeDef",
    "GetResourceLFTagsResponseTypeDef",
    "TaggedTableTypeDef",
    "AddLFTagsToResourceResponseTypeDef",
    "RemoveLFTagsFromResourceResponseTypeDef",
    "GetDataCellsFilterResponseTypeDef",
    "ListDataCellsFilterResponseTypeDef",
    "CreateDataCellsFilterRequestRequestTypeDef",
    "UpdateDataCellsFilterRequestRequestTypeDef",
    "SearchDatabasesByLFTagsResponseTypeDef",
    "UpdateTableObjectsRequestRequestTypeDef",
    "ResourceOutputTypeDef",
    "ResourceTypeDef",
    "GetTableObjectsResponseTypeDef",
    "GetDataLakeSettingsResponseTypeDef",
    "PutDataLakeSettingsRequestRequestTypeDef",
    "SearchTablesByLFTagsResponseTypeDef",
    "BatchPermissionsRequestEntryOutputTypeDef",
    "PrincipalResourcePermissionsTypeDef",
    "AddLFTagsToResourceRequestRequestTypeDef",
    "BatchPermissionsRequestEntryTypeDef",
    "GetResourceLFTagsRequestRequestTypeDef",
    "GrantPermissionsRequestRequestTypeDef",
    "ListPermissionsRequestRequestTypeDef",
    "RemoveLFTagsFromResourceRequestRequestTypeDef",
    "RevokePermissionsRequestRequestTypeDef",
    "BatchPermissionsFailureEntryTypeDef",
    "GetEffectivePermissionsForPathResponseTypeDef",
    "ListPermissionsResponseTypeDef",
    "BatchGrantPermissionsRequestRequestTypeDef",
    "BatchRevokePermissionsRequestRequestTypeDef",
    "BatchGrantPermissionsResponseTypeDef",
    "BatchRevokePermissionsResponseTypeDef",
)

_RequiredLFTagPairTypeDef = TypedDict(
    "_RequiredLFTagPairTypeDef",
    {
        "TagKey": str,
        "TagValues": Sequence[str],
    },
)
_OptionalLFTagPairTypeDef = TypedDict(
    "_OptionalLFTagPairTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class LFTagPairTypeDef(_RequiredLFTagPairTypeDef, _OptionalLFTagPairTypeDef):
    pass

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

_RequiredAddObjectInputTypeDef = TypedDict(
    "_RequiredAddObjectInputTypeDef",
    {
        "Uri": str,
        "ETag": str,
        "Size": int,
    },
)
_OptionalAddObjectInputTypeDef = TypedDict(
    "_OptionalAddObjectInputTypeDef",
    {
        "PartitionValues": Sequence[str],
    },
    total=False,
)

class AddObjectInputTypeDef(_RequiredAddObjectInputTypeDef, _OptionalAddObjectInputTypeDef):
    pass

_RequiredAssumeDecoratedRoleWithSAMLRequestRequestTypeDef = TypedDict(
    "_RequiredAssumeDecoratedRoleWithSAMLRequestRequestTypeDef",
    {
        "SAMLAssertion": str,
        "RoleArn": str,
        "PrincipalArn": str,
    },
)
_OptionalAssumeDecoratedRoleWithSAMLRequestRequestTypeDef = TypedDict(
    "_OptionalAssumeDecoratedRoleWithSAMLRequestRequestTypeDef",
    {
        "DurationSeconds": int,
    },
    total=False,
)

class AssumeDecoratedRoleWithSAMLRequestRequestTypeDef(
    _RequiredAssumeDecoratedRoleWithSAMLRequestRequestTypeDef,
    _OptionalAssumeDecoratedRoleWithSAMLRequestRequestTypeDef,
):
    pass

AuditContextTypeDef = TypedDict(
    "AuditContextTypeDef",
    {
        "AdditionalAuditContext": str,
    },
    total=False,
)

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
    },
)

DataLakePrincipalOutputTypeDef = TypedDict(
    "DataLakePrincipalOutputTypeDef",
    {
        "DataLakePrincipalIdentifier": str,
    },
)

DataLakePrincipalTypeDef = TypedDict(
    "DataLakePrincipalTypeDef",
    {
        "DataLakePrincipalIdentifier": str,
    },
    total=False,
)

CancelTransactionRequestRequestTypeDef = TypedDict(
    "CancelTransactionRequestRequestTypeDef",
    {
        "TransactionId": str,
    },
)

LFTagPairOutputTypeDef = TypedDict(
    "LFTagPairOutputTypeDef",
    {
        "CatalogId": str,
        "TagKey": str,
        "TagValues": List[str],
    },
)

ColumnWildcardOutputTypeDef = TypedDict(
    "ColumnWildcardOutputTypeDef",
    {
        "ExcludedColumnNames": List[str],
    },
)

ColumnWildcardTypeDef = TypedDict(
    "ColumnWildcardTypeDef",
    {
        "ExcludedColumnNames": Sequence[str],
    },
    total=False,
)

CommitTransactionRequestRequestTypeDef = TypedDict(
    "CommitTransactionRequestRequestTypeDef",
    {
        "TransactionId": str,
    },
)

_RequiredCreateLFTagRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLFTagRequestRequestTypeDef",
    {
        "TagKey": str,
        "TagValues": Sequence[str],
    },
)
_OptionalCreateLFTagRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLFTagRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class CreateLFTagRequestRequestTypeDef(
    _RequiredCreateLFTagRequestRequestTypeDef, _OptionalCreateLFTagRequestRequestTypeDef
):
    pass

RowFilterOutputTypeDef = TypedDict(
    "RowFilterOutputTypeDef",
    {
        "FilterExpression": str,
        "AllRowsWildcard": Dict[str, Any],
    },
)

DataCellsFilterResourceOutputTypeDef = TypedDict(
    "DataCellsFilterResourceOutputTypeDef",
    {
        "TableCatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Name": str,
    },
)

DataCellsFilterResourceTypeDef = TypedDict(
    "DataCellsFilterResourceTypeDef",
    {
        "TableCatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Name": str,
    },
    total=False,
)

RowFilterTypeDef = TypedDict(
    "RowFilterTypeDef",
    {
        "FilterExpression": str,
        "AllRowsWildcard": Mapping[str, Any],
    },
    total=False,
)

DataLocationResourceOutputTypeDef = TypedDict(
    "DataLocationResourceOutputTypeDef",
    {
        "CatalogId": str,
        "ResourceArn": str,
    },
)

_RequiredDataLocationResourceTypeDef = TypedDict(
    "_RequiredDataLocationResourceTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalDataLocationResourceTypeDef = TypedDict(
    "_OptionalDataLocationResourceTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class DataLocationResourceTypeDef(
    _RequiredDataLocationResourceTypeDef, _OptionalDataLocationResourceTypeDef
):
    pass

DatabaseResourceOutputTypeDef = TypedDict(
    "DatabaseResourceOutputTypeDef",
    {
        "CatalogId": str,
        "Name": str,
    },
)

_RequiredDatabaseResourceTypeDef = TypedDict(
    "_RequiredDatabaseResourceTypeDef",
    {
        "Name": str,
    },
)
_OptionalDatabaseResourceTypeDef = TypedDict(
    "_OptionalDatabaseResourceTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class DatabaseResourceTypeDef(_RequiredDatabaseResourceTypeDef, _OptionalDatabaseResourceTypeDef):
    pass

DeleteDataCellsFilterRequestRequestTypeDef = TypedDict(
    "DeleteDataCellsFilterRequestRequestTypeDef",
    {
        "TableCatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Name": str,
    },
    total=False,
)

_RequiredDeleteLFTagRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteLFTagRequestRequestTypeDef",
    {
        "TagKey": str,
    },
)
_OptionalDeleteLFTagRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteLFTagRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class DeleteLFTagRequestRequestTypeDef(
    _RequiredDeleteLFTagRequestRequestTypeDef, _OptionalDeleteLFTagRequestRequestTypeDef
):
    pass

_RequiredDeleteObjectInputTypeDef = TypedDict(
    "_RequiredDeleteObjectInputTypeDef",
    {
        "Uri": str,
    },
)
_OptionalDeleteObjectInputTypeDef = TypedDict(
    "_OptionalDeleteObjectInputTypeDef",
    {
        "ETag": str,
        "PartitionValues": Sequence[str],
    },
    total=False,
)

class DeleteObjectInputTypeDef(
    _RequiredDeleteObjectInputTypeDef, _OptionalDeleteObjectInputTypeDef
):
    pass

_RequiredVirtualObjectTypeDef = TypedDict(
    "_RequiredVirtualObjectTypeDef",
    {
        "Uri": str,
    },
)
_OptionalVirtualObjectTypeDef = TypedDict(
    "_OptionalVirtualObjectTypeDef",
    {
        "ETag": str,
    },
    total=False,
)

class VirtualObjectTypeDef(_RequiredVirtualObjectTypeDef, _OptionalVirtualObjectTypeDef):
    pass

DeregisterResourceRequestRequestTypeDef = TypedDict(
    "DeregisterResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DescribeResourceRequestRequestTypeDef = TypedDict(
    "DescribeResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ResourceInfoTypeDef = TypedDict(
    "ResourceInfoTypeDef",
    {
        "ResourceArn": str,
        "RoleArn": str,
        "LastModified": datetime,
        "WithFederation": bool,
    },
)

DescribeTransactionRequestRequestTypeDef = TypedDict(
    "DescribeTransactionRequestRequestTypeDef",
    {
        "TransactionId": str,
    },
)

TransactionDescriptionTypeDef = TypedDict(
    "TransactionDescriptionTypeDef",
    {
        "TransactionId": str,
        "TransactionStatus": TransactionStatusType,
        "TransactionStartTime": datetime,
        "TransactionEndTime": datetime,
    },
)

DetailsMapTypeDef = TypedDict(
    "DetailsMapTypeDef",
    {
        "ResourceShare": List[str],
    },
)

ExecutionStatisticsTypeDef = TypedDict(
    "ExecutionStatisticsTypeDef",
    {
        "AverageExecutionTimeMillis": int,
        "DataScannedBytes": int,
        "WorkUnitsExecutedCount": int,
    },
)

ExtendTransactionRequestRequestTypeDef = TypedDict(
    "ExtendTransactionRequestRequestTypeDef",
    {
        "TransactionId": str,
    },
    total=False,
)

FilterConditionTypeDef = TypedDict(
    "FilterConditionTypeDef",
    {
        "Field": FieldNameStringType,
        "ComparisonOperator": ComparisonOperatorType,
        "StringValueList": Sequence[str],
    },
    total=False,
)

GetDataCellsFilterRequestRequestTypeDef = TypedDict(
    "GetDataCellsFilterRequestRequestTypeDef",
    {
        "TableCatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Name": str,
    },
)

GetDataLakeSettingsRequestRequestTypeDef = TypedDict(
    "GetDataLakeSettingsRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

_RequiredGetEffectivePermissionsForPathRequestRequestTypeDef = TypedDict(
    "_RequiredGetEffectivePermissionsForPathRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalGetEffectivePermissionsForPathRequestRequestTypeDef = TypedDict(
    "_OptionalGetEffectivePermissionsForPathRequestRequestTypeDef",
    {
        "CatalogId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class GetEffectivePermissionsForPathRequestRequestTypeDef(
    _RequiredGetEffectivePermissionsForPathRequestRequestTypeDef,
    _OptionalGetEffectivePermissionsForPathRequestRequestTypeDef,
):
    pass

_RequiredGetLFTagRequestRequestTypeDef = TypedDict(
    "_RequiredGetLFTagRequestRequestTypeDef",
    {
        "TagKey": str,
    },
)
_OptionalGetLFTagRequestRequestTypeDef = TypedDict(
    "_OptionalGetLFTagRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class GetLFTagRequestRequestTypeDef(
    _RequiredGetLFTagRequestRequestTypeDef, _OptionalGetLFTagRequestRequestTypeDef
):
    pass

GetQueryStateRequestRequestTypeDef = TypedDict(
    "GetQueryStateRequestRequestTypeDef",
    {
        "QueryId": str,
    },
)

GetQueryStatisticsRequestRequestTypeDef = TypedDict(
    "GetQueryStatisticsRequestRequestTypeDef",
    {
        "QueryId": str,
    },
)

PlanningStatisticsTypeDef = TypedDict(
    "PlanningStatisticsTypeDef",
    {
        "EstimatedDataToScanBytes": int,
        "PlanningTimeMillis": int,
        "QueueTimeMillis": int,
        "WorkUnitsGeneratedCount": int,
    },
)

_RequiredGetTableObjectsRequestRequestTypeDef = TypedDict(
    "_RequiredGetTableObjectsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetTableObjectsRequestRequestTypeDef = TypedDict(
    "_OptionalGetTableObjectsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "TransactionId": str,
        "QueryAsOfTime": Union[datetime, str],
        "PartitionPredicate": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetTableObjectsRequestRequestTypeDef(
    _RequiredGetTableObjectsRequestRequestTypeDef, _OptionalGetTableObjectsRequestRequestTypeDef
):
    pass

PartitionValueListTypeDef = TypedDict(
    "PartitionValueListTypeDef",
    {
        "Values": Sequence[str],
    },
)

GetWorkUnitResultsRequestRequestTypeDef = TypedDict(
    "GetWorkUnitResultsRequestRequestTypeDef",
    {
        "QueryId": str,
        "WorkUnitId": int,
        "WorkUnitToken": str,
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

_RequiredGetWorkUnitsRequestRequestTypeDef = TypedDict(
    "_RequiredGetWorkUnitsRequestRequestTypeDef",
    {
        "QueryId": str,
    },
)
_OptionalGetWorkUnitsRequestRequestTypeDef = TypedDict(
    "_OptionalGetWorkUnitsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

class GetWorkUnitsRequestRequestTypeDef(
    _RequiredGetWorkUnitsRequestRequestTypeDef, _OptionalGetWorkUnitsRequestRequestTypeDef
):
    pass

WorkUnitRangeTypeDef = TypedDict(
    "WorkUnitRangeTypeDef",
    {
        "WorkUnitIdMax": int,
        "WorkUnitIdMin": int,
        "WorkUnitToken": str,
    },
)

LFTagKeyResourceOutputTypeDef = TypedDict(
    "LFTagKeyResourceOutputTypeDef",
    {
        "CatalogId": str,
        "TagKey": str,
        "TagValues": List[str],
    },
)

_RequiredLFTagKeyResourceTypeDef = TypedDict(
    "_RequiredLFTagKeyResourceTypeDef",
    {
        "TagKey": str,
        "TagValues": Sequence[str],
    },
)
_OptionalLFTagKeyResourceTypeDef = TypedDict(
    "_OptionalLFTagKeyResourceTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class LFTagKeyResourceTypeDef(_RequiredLFTagKeyResourceTypeDef, _OptionalLFTagKeyResourceTypeDef):
    pass

LFTagOutputTypeDef = TypedDict(
    "LFTagOutputTypeDef",
    {
        "TagKey": str,
        "TagValues": List[str],
    },
)

LFTagTypeDef = TypedDict(
    "LFTagTypeDef",
    {
        "TagKey": str,
        "TagValues": Sequence[str],
    },
)

_RequiredTableResourceTypeDef = TypedDict(
    "_RequiredTableResourceTypeDef",
    {
        "DatabaseName": str,
    },
)
_OptionalTableResourceTypeDef = TypedDict(
    "_OptionalTableResourceTypeDef",
    {
        "CatalogId": str,
        "Name": str,
        "TableWildcard": Mapping[str, Any],
    },
    total=False,
)

class TableResourceTypeDef(_RequiredTableResourceTypeDef, _OptionalTableResourceTypeDef):
    pass

ListLFTagsRequestRequestTypeDef = TypedDict(
    "ListLFTagsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "ResourceShareType": ResourceShareTypeType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListTableStorageOptimizersRequestRequestTypeDef = TypedDict(
    "_RequiredListTableStorageOptimizersRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalListTableStorageOptimizersRequestRequestTypeDef = TypedDict(
    "_OptionalListTableStorageOptimizersRequestRequestTypeDef",
    {
        "CatalogId": str,
        "StorageOptimizerType": OptimizerTypeType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListTableStorageOptimizersRequestRequestTypeDef(
    _RequiredListTableStorageOptimizersRequestRequestTypeDef,
    _OptionalListTableStorageOptimizersRequestRequestTypeDef,
):
    pass

StorageOptimizerTypeDef = TypedDict(
    "StorageOptimizerTypeDef",
    {
        "StorageOptimizerType": OptimizerTypeType,
        "Config": Dict[str, str],
        "ErrorMessage": str,
        "Warnings": str,
        "LastRunDetails": str,
    },
)

ListTransactionsRequestRequestTypeDef = TypedDict(
    "ListTransactionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "StatusFilter": TransactionStatusFilterType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

TableObjectTypeDef = TypedDict(
    "TableObjectTypeDef",
    {
        "Uri": str,
        "ETag": str,
        "Size": int,
    },
)

_RequiredQueryPlanningContextTypeDef = TypedDict(
    "_RequiredQueryPlanningContextTypeDef",
    {
        "DatabaseName": str,
    },
)
_OptionalQueryPlanningContextTypeDef = TypedDict(
    "_OptionalQueryPlanningContextTypeDef",
    {
        "CatalogId": str,
        "QueryAsOfTime": Union[datetime, str],
        "QueryParameters": Mapping[str, str],
        "TransactionId": str,
    },
    total=False,
)

class QueryPlanningContextTypeDef(
    _RequiredQueryPlanningContextTypeDef, _OptionalQueryPlanningContextTypeDef
):
    pass

_RequiredRegisterResourceRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalRegisterResourceRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterResourceRequestRequestTypeDef",
    {
        "UseServiceLinkedRole": bool,
        "RoleArn": str,
        "WithFederation": bool,
    },
    total=False,
)

class RegisterResourceRequestRequestTypeDef(
    _RequiredRegisterResourceRequestRequestTypeDef, _OptionalRegisterResourceRequestRequestTypeDef
):
    pass

TableResourceOutputTypeDef = TypedDict(
    "TableResourceOutputTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "Name": str,
        "TableWildcard": Dict[str, Any],
    },
)

StartTransactionRequestRequestTypeDef = TypedDict(
    "StartTransactionRequestRequestTypeDef",
    {
        "TransactionType": TransactionTypeType,
    },
    total=False,
)

_RequiredUpdateLFTagRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLFTagRequestRequestTypeDef",
    {
        "TagKey": str,
    },
)
_OptionalUpdateLFTagRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLFTagRequestRequestTypeDef",
    {
        "CatalogId": str,
        "TagValuesToDelete": Sequence[str],
        "TagValuesToAdd": Sequence[str],
    },
    total=False,
)

class UpdateLFTagRequestRequestTypeDef(
    _RequiredUpdateLFTagRequestRequestTypeDef, _OptionalUpdateLFTagRequestRequestTypeDef
):
    pass

_RequiredUpdateResourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResourceRequestRequestTypeDef",
    {
        "RoleArn": str,
        "ResourceArn": str,
    },
)
_OptionalUpdateResourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResourceRequestRequestTypeDef",
    {
        "WithFederation": bool,
    },
    total=False,
)

class UpdateResourceRequestRequestTypeDef(
    _RequiredUpdateResourceRequestRequestTypeDef, _OptionalUpdateResourceRequestRequestTypeDef
):
    pass

_RequiredUpdateTableStorageOptimizerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTableStorageOptimizerRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "StorageOptimizerConfig": Mapping[OptimizerTypeType, Mapping[str, str]],
    },
)
_OptionalUpdateTableStorageOptimizerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTableStorageOptimizerRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class UpdateTableStorageOptimizerRequestRequestTypeDef(
    _RequiredUpdateTableStorageOptimizerRequestRequestTypeDef,
    _OptionalUpdateTableStorageOptimizerRequestRequestTypeDef,
):
    pass

AssumeDecoratedRoleWithSAMLResponseTypeDef = TypedDict(
    "AssumeDecoratedRoleWithSAMLResponseTypeDef",
    {
        "AccessKeyId": str,
        "SecretAccessKey": str,
        "SessionToken": str,
        "Expiration": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CommitTransactionResponseTypeDef = TypedDict(
    "CommitTransactionResponseTypeDef",
    {
        "TransactionStatus": TransactionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLFTagResponseTypeDef = TypedDict(
    "GetLFTagResponseTypeDef",
    {
        "CatalogId": str,
        "TagKey": str,
        "TagValues": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueryStateResponseTypeDef = TypedDict(
    "GetQueryStateResponseTypeDef",
    {
        "Error": str,
        "State": QueryStateStringType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTemporaryGluePartitionCredentialsResponseTypeDef = TypedDict(
    "GetTemporaryGluePartitionCredentialsResponseTypeDef",
    {
        "AccessKeyId": str,
        "SecretAccessKey": str,
        "SessionToken": str,
        "Expiration": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTemporaryGlueTableCredentialsResponseTypeDef = TypedDict(
    "GetTemporaryGlueTableCredentialsResponseTypeDef",
    {
        "AccessKeyId": str,
        "SecretAccessKey": str,
        "SessionToken": str,
        "Expiration": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWorkUnitResultsResponseTypeDef = TypedDict(
    "GetWorkUnitResultsResponseTypeDef",
    {
        "ResultStream": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartQueryPlanningResponseTypeDef = TypedDict(
    "StartQueryPlanningResponseTypeDef",
    {
        "QueryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTransactionResponseTypeDef = TypedDict(
    "StartTransactionResponseTypeDef",
    {
        "TransactionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTableStorageOptimizerResponseTypeDef = TypedDict(
    "UpdateTableStorageOptimizerResponseTypeDef",
    {
        "Result": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetTemporaryGlueTableCredentialsRequestRequestTypeDef = TypedDict(
    "_RequiredGetTemporaryGlueTableCredentialsRequestRequestTypeDef",
    {
        "TableArn": str,
    },
)
_OptionalGetTemporaryGlueTableCredentialsRequestRequestTypeDef = TypedDict(
    "_OptionalGetTemporaryGlueTableCredentialsRequestRequestTypeDef",
    {
        "Permissions": Sequence[PermissionType],
        "DurationSeconds": int,
        "AuditContext": AuditContextTypeDef,
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
    },
    total=False,
)

class GetTemporaryGlueTableCredentialsRequestRequestTypeDef(
    _RequiredGetTemporaryGlueTableCredentialsRequestRequestTypeDef,
    _OptionalGetTemporaryGlueTableCredentialsRequestRequestTypeDef,
):
    pass

PrincipalPermissionsOutputTypeDef = TypedDict(
    "PrincipalPermissionsOutputTypeDef",
    {
        "Principal": DataLakePrincipalOutputTypeDef,
        "Permissions": List[PermissionType],
    },
)

PrincipalPermissionsTypeDef = TypedDict(
    "PrincipalPermissionsTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Permissions": Sequence[PermissionType],
    },
    total=False,
)

ColumnLFTagTypeDef = TypedDict(
    "ColumnLFTagTypeDef",
    {
        "Name": str,
        "LFTags": List[LFTagPairOutputTypeDef],
    },
)

LFTagErrorTypeDef = TypedDict(
    "LFTagErrorTypeDef",
    {
        "LFTag": LFTagPairOutputTypeDef,
        "Error": ErrorDetailTypeDef,
    },
)

ListLFTagsResponseTypeDef = TypedDict(
    "ListLFTagsResponseTypeDef",
    {
        "LFTags": List[LFTagPairOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TableWithColumnsResourceOutputTypeDef = TypedDict(
    "TableWithColumnsResourceOutputTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "Name": str,
        "ColumnNames": List[str],
        "ColumnWildcard": ColumnWildcardOutputTypeDef,
    },
)

_RequiredTableWithColumnsResourceTypeDef = TypedDict(
    "_RequiredTableWithColumnsResourceTypeDef",
    {
        "DatabaseName": str,
        "Name": str,
    },
)
_OptionalTableWithColumnsResourceTypeDef = TypedDict(
    "_OptionalTableWithColumnsResourceTypeDef",
    {
        "CatalogId": str,
        "ColumnNames": Sequence[str],
        "ColumnWildcard": ColumnWildcardTypeDef,
    },
    total=False,
)

class TableWithColumnsResourceTypeDef(
    _RequiredTableWithColumnsResourceTypeDef, _OptionalTableWithColumnsResourceTypeDef
):
    pass

DataCellsFilterOutputTypeDef = TypedDict(
    "DataCellsFilterOutputTypeDef",
    {
        "TableCatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Name": str,
        "RowFilter": RowFilterOutputTypeDef,
        "ColumnNames": List[str],
        "ColumnWildcard": ColumnWildcardOutputTypeDef,
        "VersionId": str,
    },
)

_RequiredDataCellsFilterTypeDef = TypedDict(
    "_RequiredDataCellsFilterTypeDef",
    {
        "TableCatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Name": str,
    },
)
_OptionalDataCellsFilterTypeDef = TypedDict(
    "_OptionalDataCellsFilterTypeDef",
    {
        "RowFilter": RowFilterTypeDef,
        "ColumnNames": Sequence[str],
        "ColumnWildcard": ColumnWildcardTypeDef,
        "VersionId": str,
    },
    total=False,
)

class DataCellsFilterTypeDef(_RequiredDataCellsFilterTypeDef, _OptionalDataCellsFilterTypeDef):
    pass

TaggedDatabaseTypeDef = TypedDict(
    "TaggedDatabaseTypeDef",
    {
        "Database": DatabaseResourceOutputTypeDef,
        "LFTags": List[LFTagPairOutputTypeDef],
    },
)

WriteOperationTypeDef = TypedDict(
    "WriteOperationTypeDef",
    {
        "AddObject": AddObjectInputTypeDef,
        "DeleteObject": DeleteObjectInputTypeDef,
    },
    total=False,
)

_RequiredDeleteObjectsOnCancelRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteObjectsOnCancelRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "TransactionId": str,
        "Objects": Sequence[VirtualObjectTypeDef],
    },
)
_OptionalDeleteObjectsOnCancelRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteObjectsOnCancelRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class DeleteObjectsOnCancelRequestRequestTypeDef(
    _RequiredDeleteObjectsOnCancelRequestRequestTypeDef,
    _OptionalDeleteObjectsOnCancelRequestRequestTypeDef,
):
    pass

DescribeResourceResponseTypeDef = TypedDict(
    "DescribeResourceResponseTypeDef",
    {
        "ResourceInfo": ResourceInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourcesResponseTypeDef = TypedDict(
    "ListResourcesResponseTypeDef",
    {
        "ResourceInfoList": List[ResourceInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTransactionResponseTypeDef = TypedDict(
    "DescribeTransactionResponseTypeDef",
    {
        "TransactionDescription": TransactionDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTransactionsResponseTypeDef = TypedDict(
    "ListTransactionsResponseTypeDef",
    {
        "Transactions": List[TransactionDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourcesRequestRequestTypeDef = TypedDict(
    "ListResourcesRequestRequestTypeDef",
    {
        "FilterConditionList": Sequence[FilterConditionTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

GetQueryStatisticsResponseTypeDef = TypedDict(
    "GetQueryStatisticsResponseTypeDef",
    {
        "ExecutionStatistics": ExecutionStatisticsTypeDef,
        "PlanningStatistics": PlanningStatisticsTypeDef,
        "QuerySubmissionTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetTemporaryGluePartitionCredentialsRequestRequestTypeDef = TypedDict(
    "_RequiredGetTemporaryGluePartitionCredentialsRequestRequestTypeDef",
    {
        "TableArn": str,
        "Partition": PartitionValueListTypeDef,
    },
)
_OptionalGetTemporaryGluePartitionCredentialsRequestRequestTypeDef = TypedDict(
    "_OptionalGetTemporaryGluePartitionCredentialsRequestRequestTypeDef",
    {
        "Permissions": Sequence[PermissionType],
        "DurationSeconds": int,
        "AuditContext": AuditContextTypeDef,
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
    },
    total=False,
)

class GetTemporaryGluePartitionCredentialsRequestRequestTypeDef(
    _RequiredGetTemporaryGluePartitionCredentialsRequestRequestTypeDef,
    _OptionalGetTemporaryGluePartitionCredentialsRequestRequestTypeDef,
):
    pass

_RequiredGetWorkUnitsRequestGetWorkUnitsPaginateTypeDef = TypedDict(
    "_RequiredGetWorkUnitsRequestGetWorkUnitsPaginateTypeDef",
    {
        "QueryId": str,
    },
)
_OptionalGetWorkUnitsRequestGetWorkUnitsPaginateTypeDef = TypedDict(
    "_OptionalGetWorkUnitsRequestGetWorkUnitsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetWorkUnitsRequestGetWorkUnitsPaginateTypeDef(
    _RequiredGetWorkUnitsRequestGetWorkUnitsPaginateTypeDef,
    _OptionalGetWorkUnitsRequestGetWorkUnitsPaginateTypeDef,
):
    pass

ListLFTagsRequestListLFTagsPaginateTypeDef = TypedDict(
    "ListLFTagsRequestListLFTagsPaginateTypeDef",
    {
        "CatalogId": str,
        "ResourceShareType": ResourceShareTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetWorkUnitsResponseTypeDef = TypedDict(
    "GetWorkUnitsResponseTypeDef",
    {
        "NextToken": str,
        "QueryId": str,
        "WorkUnitRanges": List[WorkUnitRangeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LFTagPolicyResourceOutputTypeDef = TypedDict(
    "LFTagPolicyResourceOutputTypeDef",
    {
        "CatalogId": str,
        "ResourceType": ResourceTypeType,
        "Expression": List[LFTagOutputTypeDef],
    },
)

_RequiredLFTagPolicyResourceTypeDef = TypedDict(
    "_RequiredLFTagPolicyResourceTypeDef",
    {
        "ResourceType": ResourceTypeType,
        "Expression": Sequence[LFTagTypeDef],
    },
)
_OptionalLFTagPolicyResourceTypeDef = TypedDict(
    "_OptionalLFTagPolicyResourceTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class LFTagPolicyResourceTypeDef(
    _RequiredLFTagPolicyResourceTypeDef, _OptionalLFTagPolicyResourceTypeDef
):
    pass

_RequiredSearchDatabasesByLFTagsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchDatabasesByLFTagsRequestRequestTypeDef",
    {
        "Expression": Sequence[LFTagTypeDef],
    },
)
_OptionalSearchDatabasesByLFTagsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchDatabasesByLFTagsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "CatalogId": str,
    },
    total=False,
)

class SearchDatabasesByLFTagsRequestRequestTypeDef(
    _RequiredSearchDatabasesByLFTagsRequestRequestTypeDef,
    _OptionalSearchDatabasesByLFTagsRequestRequestTypeDef,
):
    pass

_RequiredSearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef = TypedDict(
    "_RequiredSearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef",
    {
        "Expression": Sequence[LFTagTypeDef],
    },
)
_OptionalSearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef = TypedDict(
    "_OptionalSearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef",
    {
        "CatalogId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef(
    _RequiredSearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef,
    _OptionalSearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef,
):
    pass

_RequiredSearchTablesByLFTagsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchTablesByLFTagsRequestRequestTypeDef",
    {
        "Expression": Sequence[LFTagTypeDef],
    },
)
_OptionalSearchTablesByLFTagsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchTablesByLFTagsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "CatalogId": str,
    },
    total=False,
)

class SearchTablesByLFTagsRequestRequestTypeDef(
    _RequiredSearchTablesByLFTagsRequestRequestTypeDef,
    _OptionalSearchTablesByLFTagsRequestRequestTypeDef,
):
    pass

_RequiredSearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef = TypedDict(
    "_RequiredSearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef",
    {
        "Expression": Sequence[LFTagTypeDef],
    },
)
_OptionalSearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef = TypedDict(
    "_OptionalSearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef",
    {
        "CatalogId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef(
    _RequiredSearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef,
    _OptionalSearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef,
):
    pass

ListDataCellsFilterRequestListDataCellsFilterPaginateTypeDef = TypedDict(
    "ListDataCellsFilterRequestListDataCellsFilterPaginateTypeDef",
    {
        "Table": TableResourceTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDataCellsFilterRequestRequestTypeDef = TypedDict(
    "ListDataCellsFilterRequestRequestTypeDef",
    {
        "Table": TableResourceTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTableStorageOptimizersResponseTypeDef = TypedDict(
    "ListTableStorageOptimizersResponseTypeDef",
    {
        "StorageOptimizerList": List[StorageOptimizerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PartitionObjectsTypeDef = TypedDict(
    "PartitionObjectsTypeDef",
    {
        "PartitionValues": List[str],
        "Objects": List[TableObjectTypeDef],
    },
)

StartQueryPlanningRequestRequestTypeDef = TypedDict(
    "StartQueryPlanningRequestRequestTypeDef",
    {
        "QueryPlanningContext": QueryPlanningContextTypeDef,
        "QueryString": str,
    },
)

DataLakeSettingsOutputTypeDef = TypedDict(
    "DataLakeSettingsOutputTypeDef",
    {
        "DataLakeAdmins": List[DataLakePrincipalOutputTypeDef],
        "ReadOnlyAdmins": List[DataLakePrincipalOutputTypeDef],
        "CreateDatabaseDefaultPermissions": List[PrincipalPermissionsOutputTypeDef],
        "CreateTableDefaultPermissions": List[PrincipalPermissionsOutputTypeDef],
        "Parameters": Dict[str, str],
        "TrustedResourceOwners": List[str],
        "AllowExternalDataFiltering": bool,
        "AllowFullTableExternalDataAccess": bool,
        "ExternalDataFilteringAllowList": List[DataLakePrincipalOutputTypeDef],
        "AuthorizedSessionTagValueList": List[str],
    },
)

DataLakeSettingsTypeDef = TypedDict(
    "DataLakeSettingsTypeDef",
    {
        "DataLakeAdmins": Sequence[DataLakePrincipalTypeDef],
        "ReadOnlyAdmins": Sequence[DataLakePrincipalTypeDef],
        "CreateDatabaseDefaultPermissions": Sequence[PrincipalPermissionsTypeDef],
        "CreateTableDefaultPermissions": Sequence[PrincipalPermissionsTypeDef],
        "Parameters": Mapping[str, str],
        "TrustedResourceOwners": Sequence[str],
        "AllowExternalDataFiltering": bool,
        "AllowFullTableExternalDataAccess": bool,
        "ExternalDataFilteringAllowList": Sequence[DataLakePrincipalTypeDef],
        "AuthorizedSessionTagValueList": Sequence[str],
    },
    total=False,
)

GetResourceLFTagsResponseTypeDef = TypedDict(
    "GetResourceLFTagsResponseTypeDef",
    {
        "LFTagOnDatabase": List[LFTagPairOutputTypeDef],
        "LFTagsOnTable": List[LFTagPairOutputTypeDef],
        "LFTagsOnColumns": List[ColumnLFTagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TaggedTableTypeDef = TypedDict(
    "TaggedTableTypeDef",
    {
        "Table": TableResourceOutputTypeDef,
        "LFTagOnDatabase": List[LFTagPairOutputTypeDef],
        "LFTagsOnTable": List[LFTagPairOutputTypeDef],
        "LFTagsOnColumns": List[ColumnLFTagTypeDef],
    },
)

AddLFTagsToResourceResponseTypeDef = TypedDict(
    "AddLFTagsToResourceResponseTypeDef",
    {
        "Failures": List[LFTagErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveLFTagsFromResourceResponseTypeDef = TypedDict(
    "RemoveLFTagsFromResourceResponseTypeDef",
    {
        "Failures": List[LFTagErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataCellsFilterResponseTypeDef = TypedDict(
    "GetDataCellsFilterResponseTypeDef",
    {
        "DataCellsFilter": DataCellsFilterOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataCellsFilterResponseTypeDef = TypedDict(
    "ListDataCellsFilterResponseTypeDef",
    {
        "DataCellsFilters": List[DataCellsFilterOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataCellsFilterRequestRequestTypeDef = TypedDict(
    "CreateDataCellsFilterRequestRequestTypeDef",
    {
        "TableData": DataCellsFilterTypeDef,
    },
)

UpdateDataCellsFilterRequestRequestTypeDef = TypedDict(
    "UpdateDataCellsFilterRequestRequestTypeDef",
    {
        "TableData": DataCellsFilterTypeDef,
    },
)

SearchDatabasesByLFTagsResponseTypeDef = TypedDict(
    "SearchDatabasesByLFTagsResponseTypeDef",
    {
        "NextToken": str,
        "DatabaseList": List[TaggedDatabaseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTableObjectsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTableObjectsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "WriteOperations": Sequence[WriteOperationTypeDef],
    },
)
_OptionalUpdateTableObjectsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTableObjectsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "TransactionId": str,
    },
    total=False,
)

class UpdateTableObjectsRequestRequestTypeDef(
    _RequiredUpdateTableObjectsRequestRequestTypeDef,
    _OptionalUpdateTableObjectsRequestRequestTypeDef,
):
    pass

ResourceOutputTypeDef = TypedDict(
    "ResourceOutputTypeDef",
    {
        "Catalog": Dict[str, Any],
        "Database": DatabaseResourceOutputTypeDef,
        "Table": TableResourceOutputTypeDef,
        "TableWithColumns": TableWithColumnsResourceOutputTypeDef,
        "DataLocation": DataLocationResourceOutputTypeDef,
        "DataCellsFilter": DataCellsFilterResourceOutputTypeDef,
        "LFTag": LFTagKeyResourceOutputTypeDef,
        "LFTagPolicy": LFTagPolicyResourceOutputTypeDef,
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "Catalog": Mapping[str, Any],
        "Database": DatabaseResourceTypeDef,
        "Table": TableResourceTypeDef,
        "TableWithColumns": TableWithColumnsResourceTypeDef,
        "DataLocation": DataLocationResourceTypeDef,
        "DataCellsFilter": DataCellsFilterResourceTypeDef,
        "LFTag": LFTagKeyResourceTypeDef,
        "LFTagPolicy": LFTagPolicyResourceTypeDef,
    },
    total=False,
)

GetTableObjectsResponseTypeDef = TypedDict(
    "GetTableObjectsResponseTypeDef",
    {
        "Objects": List[PartitionObjectsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataLakeSettingsResponseTypeDef = TypedDict(
    "GetDataLakeSettingsResponseTypeDef",
    {
        "DataLakeSettings": DataLakeSettingsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutDataLakeSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredPutDataLakeSettingsRequestRequestTypeDef",
    {
        "DataLakeSettings": DataLakeSettingsTypeDef,
    },
)
_OptionalPutDataLakeSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalPutDataLakeSettingsRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class PutDataLakeSettingsRequestRequestTypeDef(
    _RequiredPutDataLakeSettingsRequestRequestTypeDef,
    _OptionalPutDataLakeSettingsRequestRequestTypeDef,
):
    pass

SearchTablesByLFTagsResponseTypeDef = TypedDict(
    "SearchTablesByLFTagsResponseTypeDef",
    {
        "NextToken": str,
        "TableList": List[TaggedTableTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPermissionsRequestEntryOutputTypeDef = TypedDict(
    "BatchPermissionsRequestEntryOutputTypeDef",
    {
        "Id": str,
        "Principal": DataLakePrincipalOutputTypeDef,
        "Resource": ResourceOutputTypeDef,
        "Permissions": List[PermissionType],
        "PermissionsWithGrantOption": List[PermissionType],
    },
)

PrincipalResourcePermissionsTypeDef = TypedDict(
    "PrincipalResourcePermissionsTypeDef",
    {
        "Principal": DataLakePrincipalOutputTypeDef,
        "Resource": ResourceOutputTypeDef,
        "Permissions": List[PermissionType],
        "PermissionsWithGrantOption": List[PermissionType],
        "AdditionalDetails": DetailsMapTypeDef,
    },
)

_RequiredAddLFTagsToResourceRequestRequestTypeDef = TypedDict(
    "_RequiredAddLFTagsToResourceRequestRequestTypeDef",
    {
        "Resource": ResourceTypeDef,
        "LFTags": Sequence[LFTagPairTypeDef],
    },
)
_OptionalAddLFTagsToResourceRequestRequestTypeDef = TypedDict(
    "_OptionalAddLFTagsToResourceRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class AddLFTagsToResourceRequestRequestTypeDef(
    _RequiredAddLFTagsToResourceRequestRequestTypeDef,
    _OptionalAddLFTagsToResourceRequestRequestTypeDef,
):
    pass

_RequiredBatchPermissionsRequestEntryTypeDef = TypedDict(
    "_RequiredBatchPermissionsRequestEntryTypeDef",
    {
        "Id": str,
    },
)
_OptionalBatchPermissionsRequestEntryTypeDef = TypedDict(
    "_OptionalBatchPermissionsRequestEntryTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Resource": ResourceTypeDef,
        "Permissions": Sequence[PermissionType],
        "PermissionsWithGrantOption": Sequence[PermissionType],
    },
    total=False,
)

class BatchPermissionsRequestEntryTypeDef(
    _RequiredBatchPermissionsRequestEntryTypeDef, _OptionalBatchPermissionsRequestEntryTypeDef
):
    pass

_RequiredGetResourceLFTagsRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourceLFTagsRequestRequestTypeDef",
    {
        "Resource": ResourceTypeDef,
    },
)
_OptionalGetResourceLFTagsRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourceLFTagsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "ShowAssignedLFTags": bool,
    },
    total=False,
)

class GetResourceLFTagsRequestRequestTypeDef(
    _RequiredGetResourceLFTagsRequestRequestTypeDef, _OptionalGetResourceLFTagsRequestRequestTypeDef
):
    pass

_RequiredGrantPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredGrantPermissionsRequestRequestTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Resource": ResourceTypeDef,
        "Permissions": Sequence[PermissionType],
    },
)
_OptionalGrantPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalGrantPermissionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "PermissionsWithGrantOption": Sequence[PermissionType],
    },
    total=False,
)

class GrantPermissionsRequestRequestTypeDef(
    _RequiredGrantPermissionsRequestRequestTypeDef, _OptionalGrantPermissionsRequestRequestTypeDef
):
    pass

ListPermissionsRequestRequestTypeDef = TypedDict(
    "ListPermissionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "Principal": DataLakePrincipalTypeDef,
        "ResourceType": DataLakeResourceTypeType,
        "Resource": ResourceTypeDef,
        "NextToken": str,
        "MaxResults": int,
        "IncludeRelated": str,
    },
    total=False,
)

_RequiredRemoveLFTagsFromResourceRequestRequestTypeDef = TypedDict(
    "_RequiredRemoveLFTagsFromResourceRequestRequestTypeDef",
    {
        "Resource": ResourceTypeDef,
        "LFTags": Sequence[LFTagPairTypeDef],
    },
)
_OptionalRemoveLFTagsFromResourceRequestRequestTypeDef = TypedDict(
    "_OptionalRemoveLFTagsFromResourceRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class RemoveLFTagsFromResourceRequestRequestTypeDef(
    _RequiredRemoveLFTagsFromResourceRequestRequestTypeDef,
    _OptionalRemoveLFTagsFromResourceRequestRequestTypeDef,
):
    pass

_RequiredRevokePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredRevokePermissionsRequestRequestTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Resource": ResourceTypeDef,
        "Permissions": Sequence[PermissionType],
    },
)
_OptionalRevokePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalRevokePermissionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "PermissionsWithGrantOption": Sequence[PermissionType],
    },
    total=False,
)

class RevokePermissionsRequestRequestTypeDef(
    _RequiredRevokePermissionsRequestRequestTypeDef, _OptionalRevokePermissionsRequestRequestTypeDef
):
    pass

BatchPermissionsFailureEntryTypeDef = TypedDict(
    "BatchPermissionsFailureEntryTypeDef",
    {
        "RequestEntry": BatchPermissionsRequestEntryOutputTypeDef,
        "Error": ErrorDetailTypeDef,
    },
)

GetEffectivePermissionsForPathResponseTypeDef = TypedDict(
    "GetEffectivePermissionsForPathResponseTypeDef",
    {
        "Permissions": List[PrincipalResourcePermissionsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPermissionsResponseTypeDef = TypedDict(
    "ListPermissionsResponseTypeDef",
    {
        "PrincipalResourcePermissions": List[PrincipalResourcePermissionsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchGrantPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGrantPermissionsRequestRequestTypeDef",
    {
        "Entries": Sequence[BatchPermissionsRequestEntryTypeDef],
    },
)
_OptionalBatchGrantPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGrantPermissionsRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class BatchGrantPermissionsRequestRequestTypeDef(
    _RequiredBatchGrantPermissionsRequestRequestTypeDef,
    _OptionalBatchGrantPermissionsRequestRequestTypeDef,
):
    pass

_RequiredBatchRevokePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchRevokePermissionsRequestRequestTypeDef",
    {
        "Entries": Sequence[BatchPermissionsRequestEntryTypeDef],
    },
)
_OptionalBatchRevokePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchRevokePermissionsRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

class BatchRevokePermissionsRequestRequestTypeDef(
    _RequiredBatchRevokePermissionsRequestRequestTypeDef,
    _OptionalBatchRevokePermissionsRequestRequestTypeDef,
):
    pass

BatchGrantPermissionsResponseTypeDef = TypedDict(
    "BatchGrantPermissionsResponseTypeDef",
    {
        "Failures": List[BatchPermissionsFailureEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchRevokePermissionsResponseTypeDef = TypedDict(
    "BatchRevokePermissionsResponseTypeDef",
    {
        "Failures": List[BatchPermissionsFailureEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
