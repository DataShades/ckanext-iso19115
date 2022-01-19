from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from . import bf

if TYPE_CHECKING:
    from .. import types


@dataclass
class MD_Identifier:
    code: str
    authority: Optional[types.cit.CI_Citation] = None
    codeSpace: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None


@dataclass
class MD_BrowseGraphic:
    fileName: str
    fileDescription: Optional[str] = None
    fileType: Optional[str] = None
    imageConstraints: list[types.mco.MD_Constraints] = field(
        default_factory=list
    )
    linkage: list[types.cit.CI_OnlineResource] = field(default_factory=list)


@dataclass
class MD_Scope:
    level: str  # codelist("MD_ScopeCode")
    # extent: list[types.gex.EX_Extent] = field(default_factory=list)
    levelDescription: list[MD_ScopeDescription] = field(default_factory=list)


@dataclass
class MD_ScopeDescription:
    attributes: str
    features: str
    featureInstances: str
    attributeInstances: str
    dataset: str
    other: str


@dataclass
class Abstract_ResourceDescription:
    citation: types.cit.CI_Citation
    abstract: str
    purpose: Optional[str] = None
    credit: list[str] = field(default_factory=list)
    status: list[str] = field(
        default_factory=list
    )  # codelit("MD_ProgressCode")
    pointOfContact: list[types.cit.CI_Responsibility] = field(
        default_factory=list
    )
    spatialRepresentationType: list[str] = field(
        default_factory=list
    )  # codelist("MD_SpatialRepresentationTypeCode")
    spatialResolution: list[types.mri.MD_Resolution] = field(
        default_factory=list
    )
    temporalResolution: list[types.gco.TM_PeriodDuration] = field(
        default_factory=list
    )
    topicCategory: list[str] = field(
        default_factory=list
    )  # codelist("MD_TopicCategoryCode")
    extent: list[types.gex.EX_Extent] = field(default_factory=list)
    additionalDocumentation: list[types.cit.CI_Citation] = field(
        default_factory=list
    )
    processingLevel: Optional[types.mcc.MD_Identifier] = None
    resourceMaintenance: list[types.mmi.MD_MaintenanceInformation] = field(
        default_factory=list
    )
    graphicOverview: list[types.mcc.MD_BrowseGraphic] = field(
        default_factory=list
    )
    resourceFormat: list[types.mrd.MD_Format] = field(default_factory=list)
    descriptiveKeywords: list[types.mri.MD_Keywords] = field(
        default_factory=list
    )
    resourceSpecificUsage: list[types.mri.MD_Usage] = field(
        default_factory=list
    )
    resourceConstraints: list[types.mco.MD_Constraints] = field(
        default_factory=list
    )
    associatedResource: list[types.mri.MD_AssociatedResource] = field(
        default_factory=list
    )

    def as_bf(self):
        return {
            "mri:citation": bf(self.citation),
            "mri:abstract": {
                "gco:CharacterString": {"$": "Line stop pretty."}
            },
        }
