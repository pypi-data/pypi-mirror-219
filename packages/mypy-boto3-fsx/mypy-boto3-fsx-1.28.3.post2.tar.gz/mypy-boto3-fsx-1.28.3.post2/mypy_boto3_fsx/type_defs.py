"""
Type annotations for fsx service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/type_defs/)

Usage::

    ```python
    from mypy_boto3_fsx.type_defs import ActiveDirectoryBackupAttributesTypeDef

    data: ActiveDirectoryBackupAttributesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence

from .literals import (
    AdministrativeActionTypeType,
    AliasLifecycleType,
    AutocommitPeriodTypeType,
    AutoImportPolicyTypeType,
    BackupLifecycleType,
    BackupTypeType,
    DataCompressionTypeType,
    DataRepositoryLifecycleType,
    DataRepositoryTaskFilterNameType,
    DataRepositoryTaskLifecycleType,
    DataRepositoryTaskTypeType,
    DiskIopsConfigurationModeType,
    DriveCacheTypeType,
    EventTypeType,
    FileCacheLifecycleType,
    FileSystemLifecycleType,
    FileSystemMaintenanceOperationType,
    FileSystemTypeType,
    FilterNameType,
    FlexCacheEndpointTypeType,
    InputOntapVolumeTypeType,
    LustreAccessAuditLogLevelType,
    LustreDeploymentTypeType,
    OntapDeploymentTypeType,
    OntapVolumeTypeType,
    OpenZFSCopyStrategyType,
    OpenZFSDataCompressionTypeType,
    OpenZFSDeploymentTypeType,
    OpenZFSQuotaTypeType,
    PrivilegedDeleteType,
    ResourceTypeType,
    RestoreOpenZFSVolumeOptionType,
    RetentionPeriodTypeType,
    SecurityStyleType,
    SnaplockTypeType,
    SnapshotFilterNameType,
    SnapshotLifecycleType,
    StatusType,
    StorageTypeType,
    StorageVirtualMachineLifecycleType,
    StorageVirtualMachineRootVolumeSecurityStyleType,
    StorageVirtualMachineSubtypeType,
    TieringPolicyNameType,
    VolumeFilterNameType,
    VolumeLifecycleType,
    VolumeTypeType,
    WindowsAccessAuditLogLevelType,
    WindowsDeploymentTypeType,
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
    "ActiveDirectoryBackupAttributesTypeDef",
    "AdministrativeActionFailureDetailsTypeDef",
    "AliasTypeDef",
    "AssociateFileSystemAliasesRequestRequestTypeDef",
    "AutoExportPolicyOutputTypeDef",
    "AutoExportPolicyTypeDef",
    "AutoImportPolicyOutputTypeDef",
    "AutoImportPolicyTypeDef",
    "AutocommitPeriodOutputTypeDef",
    "AutocommitPeriodTypeDef",
    "BackupFailureDetailsTypeDef",
    "TagOutputTypeDef",
    "CancelDataRepositoryTaskRequestRequestTypeDef",
    "CancelDataRepositoryTaskResponseTypeDef",
    "CompletionReportOutputTypeDef",
    "CompletionReportTypeDef",
    "TagTypeDef",
    "FileCacheLustreMetadataConfigurationTypeDef",
    "CreateFileSystemFromBackupResponseTypeDef",
    "LustreLogCreateConfigurationTypeDef",
    "LustreRootSquashConfigurationTypeDef",
    "DiskIopsConfigurationTypeDef",
    "CreateFileSystemResponseTypeDef",
    "SelfManagedActiveDirectoryConfigurationTypeDef",
    "WindowsAuditLogCreateConfigurationTypeDef",
    "TieringPolicyTypeDef",
    "CreateOpenZFSOriginSnapshotConfigurationTypeDef",
    "OpenZFSUserOrGroupQuotaTypeDef",
    "DataRepositoryFailureDetailsTypeDef",
    "DataRepositoryTaskFailureDetailsTypeDef",
    "DataRepositoryTaskFilterTypeDef",
    "DataRepositoryTaskStatusTypeDef",
    "DeleteBackupRequestRequestTypeDef",
    "DeleteBackupResponseTypeDef",
    "DeleteDataRepositoryAssociationRequestRequestTypeDef",
    "DeleteDataRepositoryAssociationResponseTypeDef",
    "DeleteFileCacheRequestRequestTypeDef",
    "DeleteFileCacheResponseTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteSnapshotResponseTypeDef",
    "DeleteStorageVirtualMachineRequestRequestTypeDef",
    "DeleteStorageVirtualMachineResponseTypeDef",
    "DeleteVolumeOpenZFSConfigurationTypeDef",
    "FilterTypeDef",
    "DescribeFileCachesRequestRequestTypeDef",
    "DescribeFileSystemAliasesRequestRequestTypeDef",
    "DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef",
    "DescribeFileSystemsRequestRequestTypeDef",
    "DescribeFileSystemsResponseTypeDef",
    "SnapshotFilterTypeDef",
    "StorageVirtualMachineFilterTypeDef",
    "VolumeFilterTypeDef",
    "DisassociateFileSystemAliasesRequestRequestTypeDef",
    "DiskIopsConfigurationOutputTypeDef",
    "FileCacheFailureDetailsTypeDef",
    "FileCacheNFSConfigurationTypeDef",
    "FileCacheLustreMetadataConfigurationOutputTypeDef",
    "LustreLogConfigurationTypeDef",
    "FileSystemEndpointTypeDef",
    "FileSystemFailureDetailsTypeDef",
    "LifecycleTransitionReasonTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "LustreRootSquashConfigurationOutputTypeDef",
    "TieringPolicyOutputTypeDef",
    "OpenZFSClientConfigurationOutputTypeDef",
    "OpenZFSClientConfigurationTypeDef",
    "OpenZFSOriginSnapshotConfigurationTypeDef",
    "OpenZFSUserOrGroupQuotaOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ReleaseFileSystemNfsV3LocksRequestRequestTypeDef",
    "ReleaseFileSystemNfsV3LocksResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreVolumeFromSnapshotRequestRequestTypeDef",
    "RestoreVolumeFromSnapshotResponseTypeDef",
    "RetentionPeriodOutputTypeDef",
    "RetentionPeriodTypeDef",
    "SelfManagedActiveDirectoryAttributesTypeDef",
    "SelfManagedActiveDirectoryConfigurationUpdatesTypeDef",
    "SvmEndpointTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFileCacheLustreConfigurationTypeDef",
    "UpdateFileSystemResponseTypeDef",
    "UpdateSnapshotRequestRequestTypeDef",
    "WindowsAuditLogConfigurationTypeDef",
    "AssociateFileSystemAliasesResponseTypeDef",
    "DescribeFileSystemAliasesResponseTypeDef",
    "DisassociateFileSystemAliasesResponseTypeDef",
    "NFSDataRepositoryConfigurationTypeDef",
    "S3DataRepositoryConfigurationOutputTypeDef",
    "S3DataRepositoryConfigurationTypeDef",
    "DeleteFileSystemLustreResponseTypeDef",
    "DeleteFileSystemOpenZFSResponseTypeDef",
    "DeleteFileSystemWindowsResponseTypeDef",
    "DeleteVolumeOntapResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CopyBackupRequestRequestTypeDef",
    "CreateBackupRequestRequestTypeDef",
    "CreateDataRepositoryTaskRequestRequestTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "DeleteFileSystemLustreConfigurationTypeDef",
    "DeleteFileSystemOpenZFSConfigurationTypeDef",
    "DeleteFileSystemWindowsConfigurationTypeDef",
    "DeleteVolumeOntapConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateFileCacheLustreConfigurationTypeDef",
    "CreateFileSystemLustreConfigurationTypeDef",
    "UpdateFileSystemLustreConfigurationTypeDef",
    "CreateFileSystemOntapConfigurationTypeDef",
    "UpdateFileSystemOntapConfigurationTypeDef",
    "UpdateFileSystemOpenZFSConfigurationTypeDef",
    "CreateSvmActiveDirectoryConfigurationTypeDef",
    "CreateFileSystemWindowsConfigurationTypeDef",
    "DataRepositoryConfigurationTypeDef",
    "DescribeDataRepositoryTasksRequestRequestTypeDef",
    "DataRepositoryTaskTypeDef",
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    "DescribeBackupsRequestRequestTypeDef",
    "DescribeDataRepositoryAssociationsRequestRequestTypeDef",
    "DescribeSnapshotsRequestRequestTypeDef",
    "DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef",
    "DescribeStorageVirtualMachinesRequestRequestTypeDef",
    "DescribeVolumesRequestDescribeVolumesPaginateTypeDef",
    "DescribeVolumesRequestRequestTypeDef",
    "OpenZFSFileSystemConfigurationTypeDef",
    "FileCacheDataRepositoryAssociationTypeDef",
    "FileCacheLustreConfigurationTypeDef",
    "FileSystemEndpointsTypeDef",
    "SnapshotTypeDef",
    "OpenZFSNfsExportOutputTypeDef",
    "OpenZFSNfsExportTypeDef",
    "SnaplockRetentionPeriodOutputTypeDef",
    "SnaplockRetentionPeriodTypeDef",
    "SvmActiveDirectoryConfigurationTypeDef",
    "UpdateFileSystemWindowsConfigurationTypeDef",
    "UpdateSvmActiveDirectoryConfigurationTypeDef",
    "SvmEndpointsTypeDef",
    "UpdateFileCacheRequestRequestTypeDef",
    "WindowsFileSystemConfigurationTypeDef",
    "DataRepositoryAssociationTypeDef",
    "CreateDataRepositoryAssociationRequestRequestTypeDef",
    "UpdateDataRepositoryAssociationRequestRequestTypeDef",
    "DeleteFileSystemResponseTypeDef",
    "DeleteVolumeResponseTypeDef",
    "DeleteFileSystemRequestRequestTypeDef",
    "DeleteVolumeRequestRequestTypeDef",
    "CreateStorageVirtualMachineRequestRequestTypeDef",
    "LustreFileSystemConfigurationTypeDef",
    "CreateDataRepositoryTaskResponseTypeDef",
    "DescribeDataRepositoryTasksResponseTypeDef",
    "CreateFileCacheRequestRequestTypeDef",
    "FileCacheCreatingTypeDef",
    "FileCacheTypeDef",
    "OntapFileSystemConfigurationTypeDef",
    "CreateSnapshotResponseTypeDef",
    "DescribeSnapshotsResponseTypeDef",
    "UpdateSnapshotResponseTypeDef",
    "OpenZFSVolumeConfigurationTypeDef",
    "CreateOpenZFSVolumeConfigurationTypeDef",
    "OpenZFSCreateRootVolumeConfigurationTypeDef",
    "UpdateOpenZFSVolumeConfigurationTypeDef",
    "SnaplockConfigurationTypeDef",
    "CreateSnaplockConfigurationTypeDef",
    "UpdateSnaplockConfigurationTypeDef",
    "UpdateFileSystemRequestRequestTypeDef",
    "UpdateStorageVirtualMachineRequestRequestTypeDef",
    "StorageVirtualMachineTypeDef",
    "CreateDataRepositoryAssociationResponseTypeDef",
    "DescribeDataRepositoryAssociationsResponseTypeDef",
    "UpdateDataRepositoryAssociationResponseTypeDef",
    "CreateFileCacheResponseTypeDef",
    "DescribeFileCachesResponseTypeDef",
    "UpdateFileCacheResponseTypeDef",
    "FileSystemTypeDef",
    "CreateFileSystemOpenZFSConfigurationTypeDef",
    "OntapVolumeConfigurationTypeDef",
    "CreateOntapVolumeConfigurationTypeDef",
    "UpdateOntapVolumeConfigurationTypeDef",
    "CreateStorageVirtualMachineResponseTypeDef",
    "DescribeStorageVirtualMachinesResponseTypeDef",
    "UpdateStorageVirtualMachineResponseTypeDef",
    "CreateFileSystemFromBackupRequestRequestTypeDef",
    "CreateFileSystemRequestRequestTypeDef",
    "VolumeTypeDef",
    "CreateVolumeFromBackupRequestRequestTypeDef",
    "CreateVolumeRequestRequestTypeDef",
    "UpdateVolumeRequestRequestTypeDef",
    "AdministrativeActionTypeDef",
    "BackupTypeDef",
    "CreateVolumeFromBackupResponseTypeDef",
    "CreateVolumeResponseTypeDef",
    "DescribeVolumesResponseTypeDef",
    "UpdateVolumeResponseTypeDef",
    "CopyBackupResponseTypeDef",
    "CreateBackupResponseTypeDef",
    "DescribeBackupsResponseTypeDef",
)

ActiveDirectoryBackupAttributesTypeDef = TypedDict(
    "ActiveDirectoryBackupAttributesTypeDef",
    {
        "DomainName": str,
        "ActiveDirectoryId": str,
        "ResourceARN": str,
    },
)

AdministrativeActionFailureDetailsTypeDef = TypedDict(
    "AdministrativeActionFailureDetailsTypeDef",
    {
        "Message": str,
    },
)

AliasTypeDef = TypedDict(
    "AliasTypeDef",
    {
        "Name": str,
        "Lifecycle": AliasLifecycleType,
    },
)

_RequiredAssociateFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateFileSystemAliasesRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "Aliases": Sequence[str],
    },
)
_OptionalAssociateFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateFileSystemAliasesRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class AssociateFileSystemAliasesRequestRequestTypeDef(
    _RequiredAssociateFileSystemAliasesRequestRequestTypeDef,
    _OptionalAssociateFileSystemAliasesRequestRequestTypeDef,
):
    pass


AutoExportPolicyOutputTypeDef = TypedDict(
    "AutoExportPolicyOutputTypeDef",
    {
        "Events": List[EventTypeType],
    },
)

AutoExportPolicyTypeDef = TypedDict(
    "AutoExportPolicyTypeDef",
    {
        "Events": Sequence[EventTypeType],
    },
    total=False,
)

AutoImportPolicyOutputTypeDef = TypedDict(
    "AutoImportPolicyOutputTypeDef",
    {
        "Events": List[EventTypeType],
    },
)

AutoImportPolicyTypeDef = TypedDict(
    "AutoImportPolicyTypeDef",
    {
        "Events": Sequence[EventTypeType],
    },
    total=False,
)

AutocommitPeriodOutputTypeDef = TypedDict(
    "AutocommitPeriodOutputTypeDef",
    {
        "Type": AutocommitPeriodTypeType,
        "Value": int,
    },
)

_RequiredAutocommitPeriodTypeDef = TypedDict(
    "_RequiredAutocommitPeriodTypeDef",
    {
        "Type": AutocommitPeriodTypeType,
    },
)
_OptionalAutocommitPeriodTypeDef = TypedDict(
    "_OptionalAutocommitPeriodTypeDef",
    {
        "Value": int,
    },
    total=False,
)


class AutocommitPeriodTypeDef(_RequiredAutocommitPeriodTypeDef, _OptionalAutocommitPeriodTypeDef):
    pass


BackupFailureDetailsTypeDef = TypedDict(
    "BackupFailureDetailsTypeDef",
    {
        "Message": str,
    },
)

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CancelDataRepositoryTaskRequestRequestTypeDef = TypedDict(
    "CancelDataRepositoryTaskRequestRequestTypeDef",
    {
        "TaskId": str,
    },
)

CancelDataRepositoryTaskResponseTypeDef = TypedDict(
    "CancelDataRepositoryTaskResponseTypeDef",
    {
        "Lifecycle": DataRepositoryTaskLifecycleType,
        "TaskId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CompletionReportOutputTypeDef = TypedDict(
    "CompletionReportOutputTypeDef",
    {
        "Enabled": bool,
        "Path": str,
        "Format": Literal["REPORT_CSV_20191124"],
        "Scope": Literal["FAILED_FILES_ONLY"],
    },
)

_RequiredCompletionReportTypeDef = TypedDict(
    "_RequiredCompletionReportTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalCompletionReportTypeDef = TypedDict(
    "_OptionalCompletionReportTypeDef",
    {
        "Path": str,
        "Format": Literal["REPORT_CSV_20191124"],
        "Scope": Literal["FAILED_FILES_ONLY"],
    },
    total=False,
)


class CompletionReportTypeDef(_RequiredCompletionReportTypeDef, _OptionalCompletionReportTypeDef):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

FileCacheLustreMetadataConfigurationTypeDef = TypedDict(
    "FileCacheLustreMetadataConfigurationTypeDef",
    {
        "StorageCapacity": int,
    },
)

CreateFileSystemFromBackupResponseTypeDef = TypedDict(
    "CreateFileSystemFromBackupResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredLustreLogCreateConfigurationTypeDef = TypedDict(
    "_RequiredLustreLogCreateConfigurationTypeDef",
    {
        "Level": LustreAccessAuditLogLevelType,
    },
)
_OptionalLustreLogCreateConfigurationTypeDef = TypedDict(
    "_OptionalLustreLogCreateConfigurationTypeDef",
    {
        "Destination": str,
    },
    total=False,
)


class LustreLogCreateConfigurationTypeDef(
    _RequiredLustreLogCreateConfigurationTypeDef, _OptionalLustreLogCreateConfigurationTypeDef
):
    pass


LustreRootSquashConfigurationTypeDef = TypedDict(
    "LustreRootSquashConfigurationTypeDef",
    {
        "RootSquash": str,
        "NoSquashNids": Sequence[str],
    },
    total=False,
)

DiskIopsConfigurationTypeDef = TypedDict(
    "DiskIopsConfigurationTypeDef",
    {
        "Mode": DiskIopsConfigurationModeType,
        "Iops": int,
    },
    total=False,
)

CreateFileSystemResponseTypeDef = TypedDict(
    "CreateFileSystemResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSelfManagedActiveDirectoryConfigurationTypeDef = TypedDict(
    "_RequiredSelfManagedActiveDirectoryConfigurationTypeDef",
    {
        "DomainName": str,
        "UserName": str,
        "Password": str,
        "DnsIps": Sequence[str],
    },
)
_OptionalSelfManagedActiveDirectoryConfigurationTypeDef = TypedDict(
    "_OptionalSelfManagedActiveDirectoryConfigurationTypeDef",
    {
        "OrganizationalUnitDistinguishedName": str,
        "FileSystemAdministratorsGroup": str,
    },
    total=False,
)


class SelfManagedActiveDirectoryConfigurationTypeDef(
    _RequiredSelfManagedActiveDirectoryConfigurationTypeDef,
    _OptionalSelfManagedActiveDirectoryConfigurationTypeDef,
):
    pass


_RequiredWindowsAuditLogCreateConfigurationTypeDef = TypedDict(
    "_RequiredWindowsAuditLogCreateConfigurationTypeDef",
    {
        "FileAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
        "FileShareAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
    },
)
_OptionalWindowsAuditLogCreateConfigurationTypeDef = TypedDict(
    "_OptionalWindowsAuditLogCreateConfigurationTypeDef",
    {
        "AuditLogDestination": str,
    },
    total=False,
)


class WindowsAuditLogCreateConfigurationTypeDef(
    _RequiredWindowsAuditLogCreateConfigurationTypeDef,
    _OptionalWindowsAuditLogCreateConfigurationTypeDef,
):
    pass


TieringPolicyTypeDef = TypedDict(
    "TieringPolicyTypeDef",
    {
        "CoolingPeriod": int,
        "Name": TieringPolicyNameType,
    },
    total=False,
)

CreateOpenZFSOriginSnapshotConfigurationTypeDef = TypedDict(
    "CreateOpenZFSOriginSnapshotConfigurationTypeDef",
    {
        "SnapshotARN": str,
        "CopyStrategy": OpenZFSCopyStrategyType,
    },
)

OpenZFSUserOrGroupQuotaTypeDef = TypedDict(
    "OpenZFSUserOrGroupQuotaTypeDef",
    {
        "Type": OpenZFSQuotaTypeType,
        "Id": int,
        "StorageCapacityQuotaGiB": int,
    },
)

DataRepositoryFailureDetailsTypeDef = TypedDict(
    "DataRepositoryFailureDetailsTypeDef",
    {
        "Message": str,
    },
)

DataRepositoryTaskFailureDetailsTypeDef = TypedDict(
    "DataRepositoryTaskFailureDetailsTypeDef",
    {
        "Message": str,
    },
)

DataRepositoryTaskFilterTypeDef = TypedDict(
    "DataRepositoryTaskFilterTypeDef",
    {
        "Name": DataRepositoryTaskFilterNameType,
        "Values": Sequence[str],
    },
    total=False,
)

DataRepositoryTaskStatusTypeDef = TypedDict(
    "DataRepositoryTaskStatusTypeDef",
    {
        "TotalCount": int,
        "SucceededCount": int,
        "FailedCount": int,
        "LastUpdatedTime": datetime,
        "ReleasedCapacity": int,
    },
)

_RequiredDeleteBackupRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBackupRequestRequestTypeDef",
    {
        "BackupId": str,
    },
)
_OptionalDeleteBackupRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBackupRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class DeleteBackupRequestRequestTypeDef(
    _RequiredDeleteBackupRequestRequestTypeDef, _OptionalDeleteBackupRequestRequestTypeDef
):
    pass


DeleteBackupResponseTypeDef = TypedDict(
    "DeleteBackupResponseTypeDef",
    {
        "BackupId": str,
        "Lifecycle": BackupLifecycleType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDataRepositoryAssociationRequestRequestTypeDef",
    {
        "AssociationId": str,
    },
)
_OptionalDeleteDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDataRepositoryAssociationRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "DeleteDataInFileSystem": bool,
    },
    total=False,
)


class DeleteDataRepositoryAssociationRequestRequestTypeDef(
    _RequiredDeleteDataRepositoryAssociationRequestRequestTypeDef,
    _OptionalDeleteDataRepositoryAssociationRequestRequestTypeDef,
):
    pass


DeleteDataRepositoryAssociationResponseTypeDef = TypedDict(
    "DeleteDataRepositoryAssociationResponseTypeDef",
    {
        "AssociationId": str,
        "Lifecycle": DataRepositoryLifecycleType,
        "DeleteDataInFileSystem": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteFileCacheRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFileCacheRequestRequestTypeDef",
    {
        "FileCacheId": str,
    },
)
_OptionalDeleteFileCacheRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFileCacheRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class DeleteFileCacheRequestRequestTypeDef(
    _RequiredDeleteFileCacheRequestRequestTypeDef, _OptionalDeleteFileCacheRequestRequestTypeDef
):
    pass


DeleteFileCacheResponseTypeDef = TypedDict(
    "DeleteFileCacheResponseTypeDef",
    {
        "FileCacheId": str,
        "Lifecycle": FileCacheLifecycleType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSnapshotRequestRequestTypeDef",
    {
        "SnapshotId": str,
    },
)
_OptionalDeleteSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSnapshotRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class DeleteSnapshotRequestRequestTypeDef(
    _RequiredDeleteSnapshotRequestRequestTypeDef, _OptionalDeleteSnapshotRequestRequestTypeDef
):
    pass


DeleteSnapshotResponseTypeDef = TypedDict(
    "DeleteSnapshotResponseTypeDef",
    {
        "SnapshotId": str,
        "Lifecycle": SnapshotLifecycleType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteStorageVirtualMachineRequestRequestTypeDef",
    {
        "StorageVirtualMachineId": str,
    },
)
_OptionalDeleteStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteStorageVirtualMachineRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class DeleteStorageVirtualMachineRequestRequestTypeDef(
    _RequiredDeleteStorageVirtualMachineRequestRequestTypeDef,
    _OptionalDeleteStorageVirtualMachineRequestRequestTypeDef,
):
    pass


DeleteStorageVirtualMachineResponseTypeDef = TypedDict(
    "DeleteStorageVirtualMachineResponseTypeDef",
    {
        "StorageVirtualMachineId": str,
        "Lifecycle": StorageVirtualMachineLifecycleType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteVolumeOpenZFSConfigurationTypeDef = TypedDict(
    "DeleteVolumeOpenZFSConfigurationTypeDef",
    {
        "Options": Sequence[Literal["DELETE_CHILD_VOLUMES_AND_SNAPSHOTS"]],
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": FilterNameType,
        "Values": Sequence[str],
    },
    total=False,
)

DescribeFileCachesRequestRequestTypeDef = TypedDict(
    "DescribeFileCachesRequestRequestTypeDef",
    {
        "FileCacheIds": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeFileSystemAliasesRequestRequestTypeDef",
    {
        "FileSystemId": str,
    },
)
_OptionalDescribeFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeFileSystemAliasesRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeFileSystemAliasesRequestRequestTypeDef(
    _RequiredDescribeFileSystemAliasesRequestRequestTypeDef,
    _OptionalDescribeFileSystemAliasesRequestRequestTypeDef,
):
    pass


DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef = TypedDict(
    "DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef",
    {
        "FileSystemIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeFileSystemsRequestRequestTypeDef = TypedDict(
    "DescribeFileSystemsRequestRequestTypeDef",
    {
        "FileSystemIds": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFileSystemsResponseTypeDef = TypedDict(
    "DescribeFileSystemsResponseTypeDef",
    {
        "FileSystems": List["FileSystemTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SnapshotFilterTypeDef = TypedDict(
    "SnapshotFilterTypeDef",
    {
        "Name": SnapshotFilterNameType,
        "Values": Sequence[str],
    },
    total=False,
)

StorageVirtualMachineFilterTypeDef = TypedDict(
    "StorageVirtualMachineFilterTypeDef",
    {
        "Name": Literal["file-system-id"],
        "Values": Sequence[str],
    },
    total=False,
)

VolumeFilterTypeDef = TypedDict(
    "VolumeFilterTypeDef",
    {
        "Name": VolumeFilterNameType,
        "Values": Sequence[str],
    },
    total=False,
)

_RequiredDisassociateFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateFileSystemAliasesRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "Aliases": Sequence[str],
    },
)
_OptionalDisassociateFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateFileSystemAliasesRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class DisassociateFileSystemAliasesRequestRequestTypeDef(
    _RequiredDisassociateFileSystemAliasesRequestRequestTypeDef,
    _OptionalDisassociateFileSystemAliasesRequestRequestTypeDef,
):
    pass


DiskIopsConfigurationOutputTypeDef = TypedDict(
    "DiskIopsConfigurationOutputTypeDef",
    {
        "Mode": DiskIopsConfigurationModeType,
        "Iops": int,
    },
)

FileCacheFailureDetailsTypeDef = TypedDict(
    "FileCacheFailureDetailsTypeDef",
    {
        "Message": str,
    },
)

_RequiredFileCacheNFSConfigurationTypeDef = TypedDict(
    "_RequiredFileCacheNFSConfigurationTypeDef",
    {
        "Version": Literal["NFS3"],
    },
)
_OptionalFileCacheNFSConfigurationTypeDef = TypedDict(
    "_OptionalFileCacheNFSConfigurationTypeDef",
    {
        "DnsIps": Sequence[str],
    },
    total=False,
)


class FileCacheNFSConfigurationTypeDef(
    _RequiredFileCacheNFSConfigurationTypeDef, _OptionalFileCacheNFSConfigurationTypeDef
):
    pass


FileCacheLustreMetadataConfigurationOutputTypeDef = TypedDict(
    "FileCacheLustreMetadataConfigurationOutputTypeDef",
    {
        "StorageCapacity": int,
    },
)

LustreLogConfigurationTypeDef = TypedDict(
    "LustreLogConfigurationTypeDef",
    {
        "Level": LustreAccessAuditLogLevelType,
        "Destination": str,
    },
)

FileSystemEndpointTypeDef = TypedDict(
    "FileSystemEndpointTypeDef",
    {
        "DNSName": str,
        "IpAddresses": List[str],
    },
)

FileSystemFailureDetailsTypeDef = TypedDict(
    "FileSystemFailureDetailsTypeDef",
    {
        "Message": str,
    },
)

LifecycleTransitionReasonTypeDef = TypedDict(
    "LifecycleTransitionReasonTypeDef",
    {
        "Message": str,
    },
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


LustreRootSquashConfigurationOutputTypeDef = TypedDict(
    "LustreRootSquashConfigurationOutputTypeDef",
    {
        "RootSquash": str,
        "NoSquashNids": List[str],
    },
)

TieringPolicyOutputTypeDef = TypedDict(
    "TieringPolicyOutputTypeDef",
    {
        "CoolingPeriod": int,
        "Name": TieringPolicyNameType,
    },
)

OpenZFSClientConfigurationOutputTypeDef = TypedDict(
    "OpenZFSClientConfigurationOutputTypeDef",
    {
        "Clients": str,
        "Options": List[str],
    },
)

OpenZFSClientConfigurationTypeDef = TypedDict(
    "OpenZFSClientConfigurationTypeDef",
    {
        "Clients": str,
        "Options": Sequence[str],
    },
)

OpenZFSOriginSnapshotConfigurationTypeDef = TypedDict(
    "OpenZFSOriginSnapshotConfigurationTypeDef",
    {
        "SnapshotARN": str,
        "CopyStrategy": OpenZFSCopyStrategyType,
    },
)

OpenZFSUserOrGroupQuotaOutputTypeDef = TypedDict(
    "OpenZFSUserOrGroupQuotaOutputTypeDef",
    {
        "Type": OpenZFSQuotaTypeType,
        "Id": int,
        "StorageCapacityQuotaGiB": int,
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

_RequiredReleaseFileSystemNfsV3LocksRequestRequestTypeDef = TypedDict(
    "_RequiredReleaseFileSystemNfsV3LocksRequestRequestTypeDef",
    {
        "FileSystemId": str,
    },
)
_OptionalReleaseFileSystemNfsV3LocksRequestRequestTypeDef = TypedDict(
    "_OptionalReleaseFileSystemNfsV3LocksRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class ReleaseFileSystemNfsV3LocksRequestRequestTypeDef(
    _RequiredReleaseFileSystemNfsV3LocksRequestRequestTypeDef,
    _OptionalReleaseFileSystemNfsV3LocksRequestRequestTypeDef,
):
    pass


ReleaseFileSystemNfsV3LocksResponseTypeDef = TypedDict(
    "ReleaseFileSystemNfsV3LocksResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

_RequiredRestoreVolumeFromSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredRestoreVolumeFromSnapshotRequestRequestTypeDef",
    {
        "VolumeId": str,
        "SnapshotId": str,
    },
)
_OptionalRestoreVolumeFromSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalRestoreVolumeFromSnapshotRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Options": Sequence[RestoreOpenZFSVolumeOptionType],
    },
    total=False,
)


class RestoreVolumeFromSnapshotRequestRequestTypeDef(
    _RequiredRestoreVolumeFromSnapshotRequestRequestTypeDef,
    _OptionalRestoreVolumeFromSnapshotRequestRequestTypeDef,
):
    pass


RestoreVolumeFromSnapshotResponseTypeDef = TypedDict(
    "RestoreVolumeFromSnapshotResponseTypeDef",
    {
        "VolumeId": str,
        "Lifecycle": VolumeLifecycleType,
        "AdministrativeActions": List["AdministrativeActionTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RetentionPeriodOutputTypeDef = TypedDict(
    "RetentionPeriodOutputTypeDef",
    {
        "Type": RetentionPeriodTypeType,
        "Value": int,
    },
)

_RequiredRetentionPeriodTypeDef = TypedDict(
    "_RequiredRetentionPeriodTypeDef",
    {
        "Type": RetentionPeriodTypeType,
    },
)
_OptionalRetentionPeriodTypeDef = TypedDict(
    "_OptionalRetentionPeriodTypeDef",
    {
        "Value": int,
    },
    total=False,
)


class RetentionPeriodTypeDef(_RequiredRetentionPeriodTypeDef, _OptionalRetentionPeriodTypeDef):
    pass


SelfManagedActiveDirectoryAttributesTypeDef = TypedDict(
    "SelfManagedActiveDirectoryAttributesTypeDef",
    {
        "DomainName": str,
        "OrganizationalUnitDistinguishedName": str,
        "FileSystemAdministratorsGroup": str,
        "UserName": str,
        "DnsIps": List[str],
    },
)

SelfManagedActiveDirectoryConfigurationUpdatesTypeDef = TypedDict(
    "SelfManagedActiveDirectoryConfigurationUpdatesTypeDef",
    {
        "UserName": str,
        "Password": str,
        "DnsIps": Sequence[str],
        "DomainName": str,
        "OrganizationalUnitDistinguishedName": str,
        "FileSystemAdministratorsGroup": str,
    },
    total=False,
)

SvmEndpointTypeDef = TypedDict(
    "SvmEndpointTypeDef",
    {
        "DNSName": str,
        "IpAddresses": List[str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateFileCacheLustreConfigurationTypeDef = TypedDict(
    "UpdateFileCacheLustreConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": str,
    },
    total=False,
)

UpdateFileSystemResponseTypeDef = TypedDict(
    "UpdateFileSystemResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSnapshotRequestRequestTypeDef",
    {
        "Name": str,
        "SnapshotId": str,
    },
)
_OptionalUpdateSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSnapshotRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class UpdateSnapshotRequestRequestTypeDef(
    _RequiredUpdateSnapshotRequestRequestTypeDef, _OptionalUpdateSnapshotRequestRequestTypeDef
):
    pass


WindowsAuditLogConfigurationTypeDef = TypedDict(
    "WindowsAuditLogConfigurationTypeDef",
    {
        "FileAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
        "FileShareAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
        "AuditLogDestination": str,
    },
)

AssociateFileSystemAliasesResponseTypeDef = TypedDict(
    "AssociateFileSystemAliasesResponseTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFileSystemAliasesResponseTypeDef = TypedDict(
    "DescribeFileSystemAliasesResponseTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateFileSystemAliasesResponseTypeDef = TypedDict(
    "DisassociateFileSystemAliasesResponseTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NFSDataRepositoryConfigurationTypeDef = TypedDict(
    "NFSDataRepositoryConfigurationTypeDef",
    {
        "Version": Literal["NFS3"],
        "DnsIps": List[str],
        "AutoExportPolicy": AutoExportPolicyOutputTypeDef,
    },
)

S3DataRepositoryConfigurationOutputTypeDef = TypedDict(
    "S3DataRepositoryConfigurationOutputTypeDef",
    {
        "AutoImportPolicy": AutoImportPolicyOutputTypeDef,
        "AutoExportPolicy": AutoExportPolicyOutputTypeDef,
    },
)

S3DataRepositoryConfigurationTypeDef = TypedDict(
    "S3DataRepositoryConfigurationTypeDef",
    {
        "AutoImportPolicy": AutoImportPolicyTypeDef,
        "AutoExportPolicy": AutoExportPolicyTypeDef,
    },
    total=False,
)

DeleteFileSystemLustreResponseTypeDef = TypedDict(
    "DeleteFileSystemLustreResponseTypeDef",
    {
        "FinalBackupId": str,
        "FinalBackupTags": List[TagOutputTypeDef],
    },
)

DeleteFileSystemOpenZFSResponseTypeDef = TypedDict(
    "DeleteFileSystemOpenZFSResponseTypeDef",
    {
        "FinalBackupId": str,
        "FinalBackupTags": List[TagOutputTypeDef],
    },
)

DeleteFileSystemWindowsResponseTypeDef = TypedDict(
    "DeleteFileSystemWindowsResponseTypeDef",
    {
        "FinalBackupId": str,
        "FinalBackupTags": List[TagOutputTypeDef],
    },
)

DeleteVolumeOntapResponseTypeDef = TypedDict(
    "DeleteVolumeOntapResponseTypeDef",
    {
        "FinalBackupId": str,
        "FinalBackupTags": List[TagOutputTypeDef],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCopyBackupRequestRequestTypeDef = TypedDict(
    "_RequiredCopyBackupRequestRequestTypeDef",
    {
        "SourceBackupId": str,
    },
)
_OptionalCopyBackupRequestRequestTypeDef = TypedDict(
    "_OptionalCopyBackupRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "SourceRegion": str,
        "KmsKeyId": str,
        "CopyTags": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyBackupRequestRequestTypeDef(
    _RequiredCopyBackupRequestRequestTypeDef, _OptionalCopyBackupRequestRequestTypeDef
):
    pass


CreateBackupRequestRequestTypeDef = TypedDict(
    "CreateBackupRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
        "VolumeId": str,
    },
    total=False,
)

_RequiredCreateDataRepositoryTaskRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataRepositoryTaskRequestRequestTypeDef",
    {
        "Type": DataRepositoryTaskTypeType,
        "FileSystemId": str,
        "Report": CompletionReportTypeDef,
    },
)
_OptionalCreateDataRepositoryTaskRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataRepositoryTaskRequestRequestTypeDef",
    {
        "Paths": Sequence[str],
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
        "CapacityToRelease": int,
    },
    total=False,
)


class CreateDataRepositoryTaskRequestRequestTypeDef(
    _RequiredCreateDataRepositoryTaskRequestRequestTypeDef,
    _OptionalCreateDataRepositoryTaskRequestRequestTypeDef,
):
    pass


_RequiredCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSnapshotRequestRequestTypeDef",
    {
        "Name": str,
        "VolumeId": str,
    },
)
_OptionalCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSnapshotRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSnapshotRequestRequestTypeDef(
    _RequiredCreateSnapshotRequestRequestTypeDef, _OptionalCreateSnapshotRequestRequestTypeDef
):
    pass


DeleteFileSystemLustreConfigurationTypeDef = TypedDict(
    "DeleteFileSystemLustreConfigurationTypeDef",
    {
        "SkipFinalBackup": bool,
        "FinalBackupTags": Sequence[TagTypeDef],
    },
    total=False,
)

DeleteFileSystemOpenZFSConfigurationTypeDef = TypedDict(
    "DeleteFileSystemOpenZFSConfigurationTypeDef",
    {
        "SkipFinalBackup": bool,
        "FinalBackupTags": Sequence[TagTypeDef],
        "Options": Sequence[Literal["DELETE_CHILD_VOLUMES_AND_SNAPSHOTS"]],
    },
    total=False,
)

DeleteFileSystemWindowsConfigurationTypeDef = TypedDict(
    "DeleteFileSystemWindowsConfigurationTypeDef",
    {
        "SkipFinalBackup": bool,
        "FinalBackupTags": Sequence[TagTypeDef],
    },
    total=False,
)

DeleteVolumeOntapConfigurationTypeDef = TypedDict(
    "DeleteVolumeOntapConfigurationTypeDef",
    {
        "SkipFinalBackup": bool,
        "FinalBackupTags": Sequence[TagTypeDef],
        "BypassSnaplockEnterpriseRetention": bool,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateFileCacheLustreConfigurationTypeDef = TypedDict(
    "_RequiredCreateFileCacheLustreConfigurationTypeDef",
    {
        "PerUnitStorageThroughput": int,
        "DeploymentType": Literal["CACHE_1"],
        "MetadataConfiguration": FileCacheLustreMetadataConfigurationTypeDef,
    },
)
_OptionalCreateFileCacheLustreConfigurationTypeDef = TypedDict(
    "_OptionalCreateFileCacheLustreConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": str,
    },
    total=False,
)


class CreateFileCacheLustreConfigurationTypeDef(
    _RequiredCreateFileCacheLustreConfigurationTypeDef,
    _OptionalCreateFileCacheLustreConfigurationTypeDef,
):
    pass


CreateFileSystemLustreConfigurationTypeDef = TypedDict(
    "CreateFileSystemLustreConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": str,
        "ImportPath": str,
        "ExportPath": str,
        "ImportedFileChunkSize": int,
        "DeploymentType": LustreDeploymentTypeType,
        "AutoImportPolicy": AutoImportPolicyTypeType,
        "PerUnitStorageThroughput": int,
        "DailyAutomaticBackupStartTime": str,
        "AutomaticBackupRetentionDays": int,
        "CopyTagsToBackups": bool,
        "DriveCacheType": DriveCacheTypeType,
        "DataCompressionType": DataCompressionTypeType,
        "LogConfiguration": LustreLogCreateConfigurationTypeDef,
        "RootSquashConfiguration": LustreRootSquashConfigurationTypeDef,
    },
    total=False,
)

UpdateFileSystemLustreConfigurationTypeDef = TypedDict(
    "UpdateFileSystemLustreConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": str,
        "DailyAutomaticBackupStartTime": str,
        "AutomaticBackupRetentionDays": int,
        "AutoImportPolicy": AutoImportPolicyTypeType,
        "DataCompressionType": DataCompressionTypeType,
        "LogConfiguration": LustreLogCreateConfigurationTypeDef,
        "RootSquashConfiguration": LustreRootSquashConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateFileSystemOntapConfigurationTypeDef = TypedDict(
    "_RequiredCreateFileSystemOntapConfigurationTypeDef",
    {
        "DeploymentType": OntapDeploymentTypeType,
        "ThroughputCapacity": int,
    },
)
_OptionalCreateFileSystemOntapConfigurationTypeDef = TypedDict(
    "_OptionalCreateFileSystemOntapConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": int,
        "DailyAutomaticBackupStartTime": str,
        "EndpointIpAddressRange": str,
        "FsxAdminPassword": str,
        "DiskIopsConfiguration": DiskIopsConfigurationTypeDef,
        "PreferredSubnetId": str,
        "RouteTableIds": Sequence[str],
        "WeeklyMaintenanceStartTime": str,
    },
    total=False,
)


class CreateFileSystemOntapConfigurationTypeDef(
    _RequiredCreateFileSystemOntapConfigurationTypeDef,
    _OptionalCreateFileSystemOntapConfigurationTypeDef,
):
    pass


UpdateFileSystemOntapConfigurationTypeDef = TypedDict(
    "UpdateFileSystemOntapConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": int,
        "DailyAutomaticBackupStartTime": str,
        "FsxAdminPassword": str,
        "WeeklyMaintenanceStartTime": str,
        "DiskIopsConfiguration": DiskIopsConfigurationTypeDef,
        "ThroughputCapacity": int,
        "AddRouteTableIds": Sequence[str],
        "RemoveRouteTableIds": Sequence[str],
    },
    total=False,
)

UpdateFileSystemOpenZFSConfigurationTypeDef = TypedDict(
    "UpdateFileSystemOpenZFSConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": int,
        "CopyTagsToBackups": bool,
        "CopyTagsToVolumes": bool,
        "DailyAutomaticBackupStartTime": str,
        "ThroughputCapacity": int,
        "WeeklyMaintenanceStartTime": str,
        "DiskIopsConfiguration": DiskIopsConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateSvmActiveDirectoryConfigurationTypeDef = TypedDict(
    "_RequiredCreateSvmActiveDirectoryConfigurationTypeDef",
    {
        "NetBiosName": str,
    },
)
_OptionalCreateSvmActiveDirectoryConfigurationTypeDef = TypedDict(
    "_OptionalCreateSvmActiveDirectoryConfigurationTypeDef",
    {
        "SelfManagedActiveDirectoryConfiguration": SelfManagedActiveDirectoryConfigurationTypeDef,
    },
    total=False,
)


class CreateSvmActiveDirectoryConfigurationTypeDef(
    _RequiredCreateSvmActiveDirectoryConfigurationTypeDef,
    _OptionalCreateSvmActiveDirectoryConfigurationTypeDef,
):
    pass


_RequiredCreateFileSystemWindowsConfigurationTypeDef = TypedDict(
    "_RequiredCreateFileSystemWindowsConfigurationTypeDef",
    {
        "ThroughputCapacity": int,
    },
)
_OptionalCreateFileSystemWindowsConfigurationTypeDef = TypedDict(
    "_OptionalCreateFileSystemWindowsConfigurationTypeDef",
    {
        "ActiveDirectoryId": str,
        "SelfManagedActiveDirectoryConfiguration": SelfManagedActiveDirectoryConfigurationTypeDef,
        "DeploymentType": WindowsDeploymentTypeType,
        "PreferredSubnetId": str,
        "WeeklyMaintenanceStartTime": str,
        "DailyAutomaticBackupStartTime": str,
        "AutomaticBackupRetentionDays": int,
        "CopyTagsToBackups": bool,
        "Aliases": Sequence[str],
        "AuditLogConfiguration": WindowsAuditLogCreateConfigurationTypeDef,
    },
    total=False,
)


class CreateFileSystemWindowsConfigurationTypeDef(
    _RequiredCreateFileSystemWindowsConfigurationTypeDef,
    _OptionalCreateFileSystemWindowsConfigurationTypeDef,
):
    pass


DataRepositoryConfigurationTypeDef = TypedDict(
    "DataRepositoryConfigurationTypeDef",
    {
        "Lifecycle": DataRepositoryLifecycleType,
        "ImportPath": str,
        "ExportPath": str,
        "ImportedFileChunkSize": int,
        "AutoImportPolicy": AutoImportPolicyTypeType,
        "FailureDetails": DataRepositoryFailureDetailsTypeDef,
    },
)

DescribeDataRepositoryTasksRequestRequestTypeDef = TypedDict(
    "DescribeDataRepositoryTasksRequestRequestTypeDef",
    {
        "TaskIds": Sequence[str],
        "Filters": Sequence[DataRepositoryTaskFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DataRepositoryTaskTypeDef = TypedDict(
    "DataRepositoryTaskTypeDef",
    {
        "TaskId": str,
        "Lifecycle": DataRepositoryTaskLifecycleType,
        "Type": DataRepositoryTaskTypeType,
        "CreationTime": datetime,
        "StartTime": datetime,
        "EndTime": datetime,
        "ResourceARN": str,
        "Tags": List[TagOutputTypeDef],
        "FileSystemId": str,
        "Paths": List[str],
        "FailureDetails": DataRepositoryTaskFailureDetailsTypeDef,
        "Status": DataRepositoryTaskStatusTypeDef,
        "Report": CompletionReportOutputTypeDef,
        "CapacityToRelease": int,
        "FileCacheId": str,
    },
)

DescribeBackupsRequestDescribeBackupsPaginateTypeDef = TypedDict(
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    {
        "BackupIds": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeBackupsRequestRequestTypeDef = TypedDict(
    "DescribeBackupsRequestRequestTypeDef",
    {
        "BackupIds": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeDataRepositoryAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeDataRepositoryAssociationsRequestRequestTypeDef",
    {
        "AssociationIds": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeSnapshotsRequestRequestTypeDef = TypedDict(
    "DescribeSnapshotsRequestRequestTypeDef",
    {
        "SnapshotIds": Sequence[str],
        "Filters": Sequence[SnapshotFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef = TypedDict(
    "DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef",
    {
        "StorageVirtualMachineIds": Sequence[str],
        "Filters": Sequence[StorageVirtualMachineFilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeStorageVirtualMachinesRequestRequestTypeDef = TypedDict(
    "DescribeStorageVirtualMachinesRequestRequestTypeDef",
    {
        "StorageVirtualMachineIds": Sequence[str],
        "Filters": Sequence[StorageVirtualMachineFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeVolumesRequestDescribeVolumesPaginateTypeDef = TypedDict(
    "DescribeVolumesRequestDescribeVolumesPaginateTypeDef",
    {
        "VolumeIds": Sequence[str],
        "Filters": Sequence[VolumeFilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeVolumesRequestRequestTypeDef = TypedDict(
    "DescribeVolumesRequestRequestTypeDef",
    {
        "VolumeIds": Sequence[str],
        "Filters": Sequence[VolumeFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

OpenZFSFileSystemConfigurationTypeDef = TypedDict(
    "OpenZFSFileSystemConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": int,
        "CopyTagsToBackups": bool,
        "CopyTagsToVolumes": bool,
        "DailyAutomaticBackupStartTime": str,
        "DeploymentType": OpenZFSDeploymentTypeType,
        "ThroughputCapacity": int,
        "WeeklyMaintenanceStartTime": str,
        "DiskIopsConfiguration": DiskIopsConfigurationOutputTypeDef,
        "RootVolumeId": str,
    },
)

_RequiredFileCacheDataRepositoryAssociationTypeDef = TypedDict(
    "_RequiredFileCacheDataRepositoryAssociationTypeDef",
    {
        "FileCachePath": str,
        "DataRepositoryPath": str,
    },
)
_OptionalFileCacheDataRepositoryAssociationTypeDef = TypedDict(
    "_OptionalFileCacheDataRepositoryAssociationTypeDef",
    {
        "DataRepositorySubdirectories": Sequence[str],
        "NFS": FileCacheNFSConfigurationTypeDef,
    },
    total=False,
)


class FileCacheDataRepositoryAssociationTypeDef(
    _RequiredFileCacheDataRepositoryAssociationTypeDef,
    _OptionalFileCacheDataRepositoryAssociationTypeDef,
):
    pass


FileCacheLustreConfigurationTypeDef = TypedDict(
    "FileCacheLustreConfigurationTypeDef",
    {
        "PerUnitStorageThroughput": int,
        "DeploymentType": Literal["CACHE_1"],
        "MountName": str,
        "WeeklyMaintenanceStartTime": str,
        "MetadataConfiguration": FileCacheLustreMetadataConfigurationOutputTypeDef,
        "LogConfiguration": LustreLogConfigurationTypeDef,
    },
)

FileSystemEndpointsTypeDef = TypedDict(
    "FileSystemEndpointsTypeDef",
    {
        "Intercluster": FileSystemEndpointTypeDef,
        "Management": FileSystemEndpointTypeDef,
    },
)

SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "ResourceARN": str,
        "SnapshotId": str,
        "Name": str,
        "VolumeId": str,
        "CreationTime": datetime,
        "Lifecycle": SnapshotLifecycleType,
        "LifecycleTransitionReason": LifecycleTransitionReasonTypeDef,
        "Tags": List[TagOutputTypeDef],
        "AdministrativeActions": List[Dict[str, Any]],
    },
)

OpenZFSNfsExportOutputTypeDef = TypedDict(
    "OpenZFSNfsExportOutputTypeDef",
    {
        "ClientConfigurations": List[OpenZFSClientConfigurationOutputTypeDef],
    },
)

OpenZFSNfsExportTypeDef = TypedDict(
    "OpenZFSNfsExportTypeDef",
    {
        "ClientConfigurations": Sequence[OpenZFSClientConfigurationTypeDef],
    },
)

SnaplockRetentionPeriodOutputTypeDef = TypedDict(
    "SnaplockRetentionPeriodOutputTypeDef",
    {
        "DefaultRetention": RetentionPeriodOutputTypeDef,
        "MinimumRetention": RetentionPeriodOutputTypeDef,
        "MaximumRetention": RetentionPeriodOutputTypeDef,
    },
)

SnaplockRetentionPeriodTypeDef = TypedDict(
    "SnaplockRetentionPeriodTypeDef",
    {
        "DefaultRetention": RetentionPeriodTypeDef,
        "MinimumRetention": RetentionPeriodTypeDef,
        "MaximumRetention": RetentionPeriodTypeDef,
    },
)

SvmActiveDirectoryConfigurationTypeDef = TypedDict(
    "SvmActiveDirectoryConfigurationTypeDef",
    {
        "NetBiosName": str,
        "SelfManagedActiveDirectoryConfiguration": SelfManagedActiveDirectoryAttributesTypeDef,
    },
)

UpdateFileSystemWindowsConfigurationTypeDef = TypedDict(
    "UpdateFileSystemWindowsConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": str,
        "DailyAutomaticBackupStartTime": str,
        "AutomaticBackupRetentionDays": int,
        "ThroughputCapacity": int,
        "SelfManagedActiveDirectoryConfiguration": (
            SelfManagedActiveDirectoryConfigurationUpdatesTypeDef
        ),
        "AuditLogConfiguration": WindowsAuditLogCreateConfigurationTypeDef,
    },
    total=False,
)

UpdateSvmActiveDirectoryConfigurationTypeDef = TypedDict(
    "UpdateSvmActiveDirectoryConfigurationTypeDef",
    {
        "SelfManagedActiveDirectoryConfiguration": (
            SelfManagedActiveDirectoryConfigurationUpdatesTypeDef
        ),
        "NetBiosName": str,
    },
    total=False,
)

SvmEndpointsTypeDef = TypedDict(
    "SvmEndpointsTypeDef",
    {
        "Iscsi": SvmEndpointTypeDef,
        "Management": SvmEndpointTypeDef,
        "Nfs": SvmEndpointTypeDef,
        "Smb": SvmEndpointTypeDef,
    },
)

_RequiredUpdateFileCacheRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFileCacheRequestRequestTypeDef",
    {
        "FileCacheId": str,
    },
)
_OptionalUpdateFileCacheRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFileCacheRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "LustreConfiguration": UpdateFileCacheLustreConfigurationTypeDef,
    },
    total=False,
)


class UpdateFileCacheRequestRequestTypeDef(
    _RequiredUpdateFileCacheRequestRequestTypeDef, _OptionalUpdateFileCacheRequestRequestTypeDef
):
    pass


WindowsFileSystemConfigurationTypeDef = TypedDict(
    "WindowsFileSystemConfigurationTypeDef",
    {
        "ActiveDirectoryId": str,
        "SelfManagedActiveDirectoryConfiguration": SelfManagedActiveDirectoryAttributesTypeDef,
        "DeploymentType": WindowsDeploymentTypeType,
        "RemoteAdministrationEndpoint": str,
        "PreferredSubnetId": str,
        "PreferredFileServerIp": str,
        "ThroughputCapacity": int,
        "MaintenanceOperationsInProgress": List[FileSystemMaintenanceOperationType],
        "WeeklyMaintenanceStartTime": str,
        "DailyAutomaticBackupStartTime": str,
        "AutomaticBackupRetentionDays": int,
        "CopyTagsToBackups": bool,
        "Aliases": List[AliasTypeDef],
        "AuditLogConfiguration": WindowsAuditLogConfigurationTypeDef,
    },
)

DataRepositoryAssociationTypeDef = TypedDict(
    "DataRepositoryAssociationTypeDef",
    {
        "AssociationId": str,
        "ResourceARN": str,
        "FileSystemId": str,
        "Lifecycle": DataRepositoryLifecycleType,
        "FailureDetails": DataRepositoryFailureDetailsTypeDef,
        "FileSystemPath": str,
        "DataRepositoryPath": str,
        "BatchImportMetaDataOnCreate": bool,
        "ImportedFileChunkSize": int,
        "S3": S3DataRepositoryConfigurationOutputTypeDef,
        "Tags": List[TagOutputTypeDef],
        "CreationTime": datetime,
        "FileCacheId": str,
        "FileCachePath": str,
        "DataRepositorySubdirectories": List[str],
        "NFS": NFSDataRepositoryConfigurationTypeDef,
    },
)

_RequiredCreateDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataRepositoryAssociationRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "DataRepositoryPath": str,
    },
)
_OptionalCreateDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataRepositoryAssociationRequestRequestTypeDef",
    {
        "FileSystemPath": str,
        "BatchImportMetaDataOnCreate": bool,
        "ImportedFileChunkSize": int,
        "S3": S3DataRepositoryConfigurationTypeDef,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDataRepositoryAssociationRequestRequestTypeDef(
    _RequiredCreateDataRepositoryAssociationRequestRequestTypeDef,
    _OptionalCreateDataRepositoryAssociationRequestRequestTypeDef,
):
    pass


_RequiredUpdateDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataRepositoryAssociationRequestRequestTypeDef",
    {
        "AssociationId": str,
    },
)
_OptionalUpdateDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataRepositoryAssociationRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "ImportedFileChunkSize": int,
        "S3": S3DataRepositoryConfigurationTypeDef,
    },
    total=False,
)


class UpdateDataRepositoryAssociationRequestRequestTypeDef(
    _RequiredUpdateDataRepositoryAssociationRequestRequestTypeDef,
    _OptionalUpdateDataRepositoryAssociationRequestRequestTypeDef,
):
    pass


DeleteFileSystemResponseTypeDef = TypedDict(
    "DeleteFileSystemResponseTypeDef",
    {
        "FileSystemId": str,
        "Lifecycle": FileSystemLifecycleType,
        "WindowsResponse": DeleteFileSystemWindowsResponseTypeDef,
        "LustreResponse": DeleteFileSystemLustreResponseTypeDef,
        "OpenZFSResponse": DeleteFileSystemOpenZFSResponseTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteVolumeResponseTypeDef = TypedDict(
    "DeleteVolumeResponseTypeDef",
    {
        "VolumeId": str,
        "Lifecycle": VolumeLifecycleType,
        "OntapResponse": DeleteVolumeOntapResponseTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteFileSystemRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFileSystemRequestRequestTypeDef",
    {
        "FileSystemId": str,
    },
)
_OptionalDeleteFileSystemRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFileSystemRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "WindowsConfiguration": DeleteFileSystemWindowsConfigurationTypeDef,
        "LustreConfiguration": DeleteFileSystemLustreConfigurationTypeDef,
        "OpenZFSConfiguration": DeleteFileSystemOpenZFSConfigurationTypeDef,
    },
    total=False,
)


class DeleteFileSystemRequestRequestTypeDef(
    _RequiredDeleteFileSystemRequestRequestTypeDef, _OptionalDeleteFileSystemRequestRequestTypeDef
):
    pass


_RequiredDeleteVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)
_OptionalDeleteVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteVolumeRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "OntapConfiguration": DeleteVolumeOntapConfigurationTypeDef,
        "OpenZFSConfiguration": DeleteVolumeOpenZFSConfigurationTypeDef,
    },
    total=False,
)


class DeleteVolumeRequestRequestTypeDef(
    _RequiredDeleteVolumeRequestRequestTypeDef, _OptionalDeleteVolumeRequestRequestTypeDef
):
    pass


_RequiredCreateStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStorageVirtualMachineRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "Name": str,
    },
)
_OptionalCreateStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStorageVirtualMachineRequestRequestTypeDef",
    {
        "ActiveDirectoryConfiguration": CreateSvmActiveDirectoryConfigurationTypeDef,
        "ClientRequestToken": str,
        "SvmAdminPassword": str,
        "Tags": Sequence[TagTypeDef],
        "RootVolumeSecurityStyle": StorageVirtualMachineRootVolumeSecurityStyleType,
    },
    total=False,
)


class CreateStorageVirtualMachineRequestRequestTypeDef(
    _RequiredCreateStorageVirtualMachineRequestRequestTypeDef,
    _OptionalCreateStorageVirtualMachineRequestRequestTypeDef,
):
    pass


LustreFileSystemConfigurationTypeDef = TypedDict(
    "LustreFileSystemConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": str,
        "DataRepositoryConfiguration": DataRepositoryConfigurationTypeDef,
        "DeploymentType": LustreDeploymentTypeType,
        "PerUnitStorageThroughput": int,
        "MountName": str,
        "DailyAutomaticBackupStartTime": str,
        "AutomaticBackupRetentionDays": int,
        "CopyTagsToBackups": bool,
        "DriveCacheType": DriveCacheTypeType,
        "DataCompressionType": DataCompressionTypeType,
        "LogConfiguration": LustreLogConfigurationTypeDef,
        "RootSquashConfiguration": LustreRootSquashConfigurationOutputTypeDef,
    },
)

CreateDataRepositoryTaskResponseTypeDef = TypedDict(
    "CreateDataRepositoryTaskResponseTypeDef",
    {
        "DataRepositoryTask": DataRepositoryTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDataRepositoryTasksResponseTypeDef = TypedDict(
    "DescribeDataRepositoryTasksResponseTypeDef",
    {
        "DataRepositoryTasks": List[DataRepositoryTaskTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFileCacheRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFileCacheRequestRequestTypeDef",
    {
        "FileCacheType": Literal["LUSTRE"],
        "FileCacheTypeVersion": str,
        "StorageCapacity": int,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateFileCacheRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFileCacheRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "SecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "CopyTagsToDataRepositoryAssociations": bool,
        "KmsKeyId": str,
        "LustreConfiguration": CreateFileCacheLustreConfigurationTypeDef,
        "DataRepositoryAssociations": Sequence[FileCacheDataRepositoryAssociationTypeDef],
    },
    total=False,
)


class CreateFileCacheRequestRequestTypeDef(
    _RequiredCreateFileCacheRequestRequestTypeDef, _OptionalCreateFileCacheRequestRequestTypeDef
):
    pass


FileCacheCreatingTypeDef = TypedDict(
    "FileCacheCreatingTypeDef",
    {
        "OwnerId": str,
        "CreationTime": datetime,
        "FileCacheId": str,
        "FileCacheType": Literal["LUSTRE"],
        "FileCacheTypeVersion": str,
        "Lifecycle": FileCacheLifecycleType,
        "FailureDetails": FileCacheFailureDetailsTypeDef,
        "StorageCapacity": int,
        "VpcId": str,
        "SubnetIds": List[str],
        "NetworkInterfaceIds": List[str],
        "DNSName": str,
        "KmsKeyId": str,
        "ResourceARN": str,
        "Tags": List[TagOutputTypeDef],
        "CopyTagsToDataRepositoryAssociations": bool,
        "LustreConfiguration": FileCacheLustreConfigurationTypeDef,
        "DataRepositoryAssociationIds": List[str],
    },
)

FileCacheTypeDef = TypedDict(
    "FileCacheTypeDef",
    {
        "OwnerId": str,
        "CreationTime": datetime,
        "FileCacheId": str,
        "FileCacheType": Literal["LUSTRE"],
        "FileCacheTypeVersion": str,
        "Lifecycle": FileCacheLifecycleType,
        "FailureDetails": FileCacheFailureDetailsTypeDef,
        "StorageCapacity": int,
        "VpcId": str,
        "SubnetIds": List[str],
        "NetworkInterfaceIds": List[str],
        "DNSName": str,
        "KmsKeyId": str,
        "ResourceARN": str,
        "LustreConfiguration": FileCacheLustreConfigurationTypeDef,
        "DataRepositoryAssociationIds": List[str],
    },
)

OntapFileSystemConfigurationTypeDef = TypedDict(
    "OntapFileSystemConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": int,
        "DailyAutomaticBackupStartTime": str,
        "DeploymentType": OntapDeploymentTypeType,
        "EndpointIpAddressRange": str,
        "Endpoints": FileSystemEndpointsTypeDef,
        "DiskIopsConfiguration": DiskIopsConfigurationOutputTypeDef,
        "PreferredSubnetId": str,
        "RouteTableIds": List[str],
        "ThroughputCapacity": int,
        "WeeklyMaintenanceStartTime": str,
        "FsxAdminPassword": str,
    },
)

CreateSnapshotResponseTypeDef = TypedDict(
    "CreateSnapshotResponseTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSnapshotsResponseTypeDef = TypedDict(
    "DescribeSnapshotsResponseTypeDef",
    {
        "Snapshots": List[SnapshotTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateSnapshotResponseTypeDef = TypedDict(
    "UpdateSnapshotResponseTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

OpenZFSVolumeConfigurationTypeDef = TypedDict(
    "OpenZFSVolumeConfigurationTypeDef",
    {
        "ParentVolumeId": str,
        "VolumePath": str,
        "StorageCapacityReservationGiB": int,
        "StorageCapacityQuotaGiB": int,
        "RecordSizeKiB": int,
        "DataCompressionType": OpenZFSDataCompressionTypeType,
        "CopyTagsToSnapshots": bool,
        "OriginSnapshot": OpenZFSOriginSnapshotConfigurationTypeDef,
        "ReadOnly": bool,
        "NfsExports": List[OpenZFSNfsExportOutputTypeDef],
        "UserAndGroupQuotas": List[OpenZFSUserOrGroupQuotaOutputTypeDef],
        "RestoreToSnapshot": str,
        "DeleteIntermediateSnaphots": bool,
        "DeleteClonedVolumes": bool,
    },
)

_RequiredCreateOpenZFSVolumeConfigurationTypeDef = TypedDict(
    "_RequiredCreateOpenZFSVolumeConfigurationTypeDef",
    {
        "ParentVolumeId": str,
    },
)
_OptionalCreateOpenZFSVolumeConfigurationTypeDef = TypedDict(
    "_OptionalCreateOpenZFSVolumeConfigurationTypeDef",
    {
        "StorageCapacityReservationGiB": int,
        "StorageCapacityQuotaGiB": int,
        "RecordSizeKiB": int,
        "DataCompressionType": OpenZFSDataCompressionTypeType,
        "CopyTagsToSnapshots": bool,
        "OriginSnapshot": CreateOpenZFSOriginSnapshotConfigurationTypeDef,
        "ReadOnly": bool,
        "NfsExports": Sequence[OpenZFSNfsExportTypeDef],
        "UserAndGroupQuotas": Sequence[OpenZFSUserOrGroupQuotaTypeDef],
    },
    total=False,
)


class CreateOpenZFSVolumeConfigurationTypeDef(
    _RequiredCreateOpenZFSVolumeConfigurationTypeDef,
    _OptionalCreateOpenZFSVolumeConfigurationTypeDef,
):
    pass


OpenZFSCreateRootVolumeConfigurationTypeDef = TypedDict(
    "OpenZFSCreateRootVolumeConfigurationTypeDef",
    {
        "RecordSizeKiB": int,
        "DataCompressionType": OpenZFSDataCompressionTypeType,
        "NfsExports": Sequence[OpenZFSNfsExportTypeDef],
        "UserAndGroupQuotas": Sequence[OpenZFSUserOrGroupQuotaTypeDef],
        "CopyTagsToSnapshots": bool,
        "ReadOnly": bool,
    },
    total=False,
)

UpdateOpenZFSVolumeConfigurationTypeDef = TypedDict(
    "UpdateOpenZFSVolumeConfigurationTypeDef",
    {
        "StorageCapacityReservationGiB": int,
        "StorageCapacityQuotaGiB": int,
        "RecordSizeKiB": int,
        "DataCompressionType": OpenZFSDataCompressionTypeType,
        "NfsExports": Sequence[OpenZFSNfsExportTypeDef],
        "UserAndGroupQuotas": Sequence[OpenZFSUserOrGroupQuotaTypeDef],
        "ReadOnly": bool,
    },
    total=False,
)

SnaplockConfigurationTypeDef = TypedDict(
    "SnaplockConfigurationTypeDef",
    {
        "AuditLogVolume": bool,
        "AutocommitPeriod": AutocommitPeriodOutputTypeDef,
        "PrivilegedDelete": PrivilegedDeleteType,
        "RetentionPeriod": SnaplockRetentionPeriodOutputTypeDef,
        "SnaplockType": SnaplockTypeType,
        "VolumeAppendModeEnabled": bool,
    },
)

_RequiredCreateSnaplockConfigurationTypeDef = TypedDict(
    "_RequiredCreateSnaplockConfigurationTypeDef",
    {
        "SnaplockType": SnaplockTypeType,
    },
)
_OptionalCreateSnaplockConfigurationTypeDef = TypedDict(
    "_OptionalCreateSnaplockConfigurationTypeDef",
    {
        "AuditLogVolume": bool,
        "AutocommitPeriod": AutocommitPeriodTypeDef,
        "PrivilegedDelete": PrivilegedDeleteType,
        "RetentionPeriod": SnaplockRetentionPeriodTypeDef,
        "VolumeAppendModeEnabled": bool,
    },
    total=False,
)


class CreateSnaplockConfigurationTypeDef(
    _RequiredCreateSnaplockConfigurationTypeDef, _OptionalCreateSnaplockConfigurationTypeDef
):
    pass


UpdateSnaplockConfigurationTypeDef = TypedDict(
    "UpdateSnaplockConfigurationTypeDef",
    {
        "AuditLogVolume": bool,
        "AutocommitPeriod": AutocommitPeriodTypeDef,
        "PrivilegedDelete": PrivilegedDeleteType,
        "RetentionPeriod": SnaplockRetentionPeriodTypeDef,
        "VolumeAppendModeEnabled": bool,
    },
    total=False,
)

_RequiredUpdateFileSystemRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFileSystemRequestRequestTypeDef",
    {
        "FileSystemId": str,
    },
)
_OptionalUpdateFileSystemRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFileSystemRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "StorageCapacity": int,
        "WindowsConfiguration": UpdateFileSystemWindowsConfigurationTypeDef,
        "LustreConfiguration": UpdateFileSystemLustreConfigurationTypeDef,
        "OntapConfiguration": UpdateFileSystemOntapConfigurationTypeDef,
        "OpenZFSConfiguration": UpdateFileSystemOpenZFSConfigurationTypeDef,
    },
    total=False,
)


class UpdateFileSystemRequestRequestTypeDef(
    _RequiredUpdateFileSystemRequestRequestTypeDef, _OptionalUpdateFileSystemRequestRequestTypeDef
):
    pass


_RequiredUpdateStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStorageVirtualMachineRequestRequestTypeDef",
    {
        "StorageVirtualMachineId": str,
    },
)
_OptionalUpdateStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStorageVirtualMachineRequestRequestTypeDef",
    {
        "ActiveDirectoryConfiguration": UpdateSvmActiveDirectoryConfigurationTypeDef,
        "ClientRequestToken": str,
        "SvmAdminPassword": str,
    },
    total=False,
)


class UpdateStorageVirtualMachineRequestRequestTypeDef(
    _RequiredUpdateStorageVirtualMachineRequestRequestTypeDef,
    _OptionalUpdateStorageVirtualMachineRequestRequestTypeDef,
):
    pass


StorageVirtualMachineTypeDef = TypedDict(
    "StorageVirtualMachineTypeDef",
    {
        "ActiveDirectoryConfiguration": SvmActiveDirectoryConfigurationTypeDef,
        "CreationTime": datetime,
        "Endpoints": SvmEndpointsTypeDef,
        "FileSystemId": str,
        "Lifecycle": StorageVirtualMachineLifecycleType,
        "Name": str,
        "ResourceARN": str,
        "StorageVirtualMachineId": str,
        "Subtype": StorageVirtualMachineSubtypeType,
        "UUID": str,
        "Tags": List[TagOutputTypeDef],
        "LifecycleTransitionReason": LifecycleTransitionReasonTypeDef,
        "RootVolumeSecurityStyle": StorageVirtualMachineRootVolumeSecurityStyleType,
    },
)

CreateDataRepositoryAssociationResponseTypeDef = TypedDict(
    "CreateDataRepositoryAssociationResponseTypeDef",
    {
        "Association": DataRepositoryAssociationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDataRepositoryAssociationsResponseTypeDef = TypedDict(
    "DescribeDataRepositoryAssociationsResponseTypeDef",
    {
        "Associations": List[DataRepositoryAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateDataRepositoryAssociationResponseTypeDef = TypedDict(
    "UpdateDataRepositoryAssociationResponseTypeDef",
    {
        "Association": DataRepositoryAssociationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateFileCacheResponseTypeDef = TypedDict(
    "CreateFileCacheResponseTypeDef",
    {
        "FileCache": FileCacheCreatingTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFileCachesResponseTypeDef = TypedDict(
    "DescribeFileCachesResponseTypeDef",
    {
        "FileCaches": List[FileCacheTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFileCacheResponseTypeDef = TypedDict(
    "UpdateFileCacheResponseTypeDef",
    {
        "FileCache": FileCacheTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FileSystemTypeDef = TypedDict(
    "FileSystemTypeDef",
    {
        "OwnerId": str,
        "CreationTime": datetime,
        "FileSystemId": str,
        "FileSystemType": FileSystemTypeType,
        "Lifecycle": FileSystemLifecycleType,
        "FailureDetails": FileSystemFailureDetailsTypeDef,
        "StorageCapacity": int,
        "StorageType": StorageTypeType,
        "VpcId": str,
        "SubnetIds": List[str],
        "NetworkInterfaceIds": List[str],
        "DNSName": str,
        "KmsKeyId": str,
        "ResourceARN": str,
        "Tags": List[TagOutputTypeDef],
        "WindowsConfiguration": WindowsFileSystemConfigurationTypeDef,
        "LustreConfiguration": LustreFileSystemConfigurationTypeDef,
        "AdministrativeActions": List["AdministrativeActionTypeDef"],
        "OntapConfiguration": OntapFileSystemConfigurationTypeDef,
        "FileSystemTypeVersion": str,
        "OpenZFSConfiguration": OpenZFSFileSystemConfigurationTypeDef,
    },
)

_RequiredCreateFileSystemOpenZFSConfigurationTypeDef = TypedDict(
    "_RequiredCreateFileSystemOpenZFSConfigurationTypeDef",
    {
        "DeploymentType": OpenZFSDeploymentTypeType,
        "ThroughputCapacity": int,
    },
)
_OptionalCreateFileSystemOpenZFSConfigurationTypeDef = TypedDict(
    "_OptionalCreateFileSystemOpenZFSConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": int,
        "CopyTagsToBackups": bool,
        "CopyTagsToVolumes": bool,
        "DailyAutomaticBackupStartTime": str,
        "WeeklyMaintenanceStartTime": str,
        "DiskIopsConfiguration": DiskIopsConfigurationTypeDef,
        "RootVolumeConfiguration": OpenZFSCreateRootVolumeConfigurationTypeDef,
    },
    total=False,
)


class CreateFileSystemOpenZFSConfigurationTypeDef(
    _RequiredCreateFileSystemOpenZFSConfigurationTypeDef,
    _OptionalCreateFileSystemOpenZFSConfigurationTypeDef,
):
    pass


OntapVolumeConfigurationTypeDef = TypedDict(
    "OntapVolumeConfigurationTypeDef",
    {
        "FlexCacheEndpointType": FlexCacheEndpointTypeType,
        "JunctionPath": str,
        "SecurityStyle": SecurityStyleType,
        "SizeInMegabytes": int,
        "StorageEfficiencyEnabled": bool,
        "StorageVirtualMachineId": str,
        "StorageVirtualMachineRoot": bool,
        "TieringPolicy": TieringPolicyOutputTypeDef,
        "UUID": str,
        "OntapVolumeType": OntapVolumeTypeType,
        "SnapshotPolicy": str,
        "CopyTagsToBackups": bool,
        "SnaplockConfiguration": SnaplockConfigurationTypeDef,
    },
)

_RequiredCreateOntapVolumeConfigurationTypeDef = TypedDict(
    "_RequiredCreateOntapVolumeConfigurationTypeDef",
    {
        "SizeInMegabytes": int,
        "StorageVirtualMachineId": str,
    },
)
_OptionalCreateOntapVolumeConfigurationTypeDef = TypedDict(
    "_OptionalCreateOntapVolumeConfigurationTypeDef",
    {
        "JunctionPath": str,
        "SecurityStyle": SecurityStyleType,
        "StorageEfficiencyEnabled": bool,
        "TieringPolicy": TieringPolicyTypeDef,
        "OntapVolumeType": InputOntapVolumeTypeType,
        "SnapshotPolicy": str,
        "CopyTagsToBackups": bool,
        "SnaplockConfiguration": CreateSnaplockConfigurationTypeDef,
    },
    total=False,
)


class CreateOntapVolumeConfigurationTypeDef(
    _RequiredCreateOntapVolumeConfigurationTypeDef, _OptionalCreateOntapVolumeConfigurationTypeDef
):
    pass


UpdateOntapVolumeConfigurationTypeDef = TypedDict(
    "UpdateOntapVolumeConfigurationTypeDef",
    {
        "JunctionPath": str,
        "SecurityStyle": SecurityStyleType,
        "SizeInMegabytes": int,
        "StorageEfficiencyEnabled": bool,
        "TieringPolicy": TieringPolicyTypeDef,
        "SnapshotPolicy": str,
        "CopyTagsToBackups": bool,
        "SnaplockConfiguration": UpdateSnaplockConfigurationTypeDef,
    },
    total=False,
)

CreateStorageVirtualMachineResponseTypeDef = TypedDict(
    "CreateStorageVirtualMachineResponseTypeDef",
    {
        "StorageVirtualMachine": StorageVirtualMachineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeStorageVirtualMachinesResponseTypeDef = TypedDict(
    "DescribeStorageVirtualMachinesResponseTypeDef",
    {
        "StorageVirtualMachines": List[StorageVirtualMachineTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateStorageVirtualMachineResponseTypeDef = TypedDict(
    "UpdateStorageVirtualMachineResponseTypeDef",
    {
        "StorageVirtualMachine": StorageVirtualMachineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFileSystemFromBackupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFileSystemFromBackupRequestRequestTypeDef",
    {
        "BackupId": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateFileSystemFromBackupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFileSystemFromBackupRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "SecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "WindowsConfiguration": CreateFileSystemWindowsConfigurationTypeDef,
        "LustreConfiguration": CreateFileSystemLustreConfigurationTypeDef,
        "StorageType": StorageTypeType,
        "KmsKeyId": str,
        "FileSystemTypeVersion": str,
        "OpenZFSConfiguration": CreateFileSystemOpenZFSConfigurationTypeDef,
        "StorageCapacity": int,
    },
    total=False,
)


class CreateFileSystemFromBackupRequestRequestTypeDef(
    _RequiredCreateFileSystemFromBackupRequestRequestTypeDef,
    _OptionalCreateFileSystemFromBackupRequestRequestTypeDef,
):
    pass


_RequiredCreateFileSystemRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFileSystemRequestRequestTypeDef",
    {
        "FileSystemType": FileSystemTypeType,
        "StorageCapacity": int,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateFileSystemRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFileSystemRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "StorageType": StorageTypeType,
        "SecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "WindowsConfiguration": CreateFileSystemWindowsConfigurationTypeDef,
        "LustreConfiguration": CreateFileSystemLustreConfigurationTypeDef,
        "OntapConfiguration": CreateFileSystemOntapConfigurationTypeDef,
        "FileSystemTypeVersion": str,
        "OpenZFSConfiguration": CreateFileSystemOpenZFSConfigurationTypeDef,
    },
    total=False,
)


class CreateFileSystemRequestRequestTypeDef(
    _RequiredCreateFileSystemRequestRequestTypeDef, _OptionalCreateFileSystemRequestRequestTypeDef
):
    pass


VolumeTypeDef = TypedDict(
    "VolumeTypeDef",
    {
        "CreationTime": datetime,
        "FileSystemId": str,
        "Lifecycle": VolumeLifecycleType,
        "Name": str,
        "OntapConfiguration": OntapVolumeConfigurationTypeDef,
        "ResourceARN": str,
        "Tags": List[TagOutputTypeDef],
        "VolumeId": str,
        "VolumeType": VolumeTypeType,
        "LifecycleTransitionReason": LifecycleTransitionReasonTypeDef,
        "AdministrativeActions": List["AdministrativeActionTypeDef"],
        "OpenZFSConfiguration": OpenZFSVolumeConfigurationTypeDef,
    },
)

_RequiredCreateVolumeFromBackupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVolumeFromBackupRequestRequestTypeDef",
    {
        "BackupId": str,
        "Name": str,
    },
)
_OptionalCreateVolumeFromBackupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVolumeFromBackupRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "OntapConfiguration": CreateOntapVolumeConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateVolumeFromBackupRequestRequestTypeDef(
    _RequiredCreateVolumeFromBackupRequestRequestTypeDef,
    _OptionalCreateVolumeFromBackupRequestRequestTypeDef,
):
    pass


_RequiredCreateVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVolumeRequestRequestTypeDef",
    {
        "VolumeType": VolumeTypeType,
        "Name": str,
    },
)
_OptionalCreateVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVolumeRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "OntapConfiguration": CreateOntapVolumeConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
        "OpenZFSConfiguration": CreateOpenZFSVolumeConfigurationTypeDef,
    },
    total=False,
)


class CreateVolumeRequestRequestTypeDef(
    _RequiredCreateVolumeRequestRequestTypeDef, _OptionalCreateVolumeRequestRequestTypeDef
):
    pass


_RequiredUpdateVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)
_OptionalUpdateVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVolumeRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "OntapConfiguration": UpdateOntapVolumeConfigurationTypeDef,
        "Name": str,
        "OpenZFSConfiguration": UpdateOpenZFSVolumeConfigurationTypeDef,
    },
    total=False,
)


class UpdateVolumeRequestRequestTypeDef(
    _RequiredUpdateVolumeRequestRequestTypeDef, _OptionalUpdateVolumeRequestRequestTypeDef
):
    pass


AdministrativeActionTypeDef = TypedDict(
    "AdministrativeActionTypeDef",
    {
        "AdministrativeActionType": AdministrativeActionTypeType,
        "ProgressPercent": int,
        "RequestTime": datetime,
        "Status": StatusType,
        "TargetFileSystemValues": Dict[str, Any],
        "FailureDetails": AdministrativeActionFailureDetailsTypeDef,
        "TargetVolumeValues": Dict[str, Any],
        "TargetSnapshotValues": Dict[str, Any],
    },
)

BackupTypeDef = TypedDict(
    "BackupTypeDef",
    {
        "BackupId": str,
        "Lifecycle": BackupLifecycleType,
        "FailureDetails": BackupFailureDetailsTypeDef,
        "Type": BackupTypeType,
        "ProgressPercent": int,
        "CreationTime": datetime,
        "KmsKeyId": str,
        "ResourceARN": str,
        "Tags": List[TagOutputTypeDef],
        "FileSystem": "FileSystemTypeDef",
        "DirectoryInformation": ActiveDirectoryBackupAttributesTypeDef,
        "OwnerId": str,
        "SourceBackupId": str,
        "SourceBackupRegion": str,
        "ResourceType": ResourceTypeType,
        "Volume": VolumeTypeDef,
    },
)

CreateVolumeFromBackupResponseTypeDef = TypedDict(
    "CreateVolumeFromBackupResponseTypeDef",
    {
        "Volume": VolumeTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateVolumeResponseTypeDef = TypedDict(
    "CreateVolumeResponseTypeDef",
    {
        "Volume": VolumeTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeVolumesResponseTypeDef = TypedDict(
    "DescribeVolumesResponseTypeDef",
    {
        "Volumes": List[VolumeTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateVolumeResponseTypeDef = TypedDict(
    "UpdateVolumeResponseTypeDef",
    {
        "Volume": VolumeTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CopyBackupResponseTypeDef = TypedDict(
    "CopyBackupResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateBackupResponseTypeDef = TypedDict(
    "CreateBackupResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeBackupsResponseTypeDef = TypedDict(
    "DescribeBackupsResponseTypeDef",
    {
        "Backups": List[BackupTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
