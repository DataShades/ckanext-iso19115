from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from ckanext.iso19115.converter import bf, make

if TYPE_CHECKING:
    from .. import types


@dataclass
class SV_CoupledResource:
    ...


@dataclass
class SV_OperationMetadata:
    ...


@dataclass
class SV_OperationChainMetadata:
    ...


from .mcc import Abstract_ResourceDescription


@dataclass
class SV_ServiceIdentification(Abstract_ResourceDescription):
    serviceType: Optional[str] = None
    serviceTypeVersion: list[str] = field(default_factory=list)
    accessProperties: Optional[types.mrd.MD_StandardOrderProcess] = None
    couplingType: Optional[str] = None  # codelist("SV_CouplingType")
    coupledResource: list[SV_CoupledResource] = field(default_factory=list)
    operatedDataset: list[types.cit.CI_Citation] = field(default_factory=list)
    profile: list[types.cit.CI_Citation] = field(default_factory=list)
    serviceStandard: list[types.cit.CI_Citation] = field(default_factory=list)
    containsOperations: list[SV_OperationMetadata] = field(
        default_factory=list
    )
    operatesOn: list[types.mri.MD_DataIdentification] = field(
        default_factory=list
    )
    containsChain: list[SV_OperationChainMetadata] = field(
        default_factory=list
    )
