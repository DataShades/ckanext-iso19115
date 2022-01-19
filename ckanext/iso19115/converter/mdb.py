from __future__ import annotations

import dataclasses
import datetime
import enum
from typing import TYPE_CHECKING, Any

from ckanext.iso19115.converter import bf, make

if TYPE_CHECKING:
    from .. import types


@dataclasses.dataclass
class MD_Metadata:
    contact: list[types.cit.CI_Responsibility] = dataclasses.field(
        default_factory=list
    )
    dateInfo: list[types.cit.CI_Date] = dataclasses.field(default_factory=list)
    identificationInfo: list[
        types.mcc.Abstract_ResourceDescription
    ] = dataclasses.field(default_factory=list)

    # ?mdb:metadataIdentifier
    # ?mdb:defaultLocale
    # ?mdb:parentMetadata
    # ?mdb:metadataScope
    # ?mdb:metadataStandard
    # ?mdb:metadataProfile
    # ?mdb:alternativeMetadataReference
    # ?mdb:otherLocale
    # ?mdb:metadataLinkage
    # ?mdb:spatialRepresentationInfo
    # ?mdb:referenceSystemInfo
    # ?mdb:metadataExtensionInfo
    # ?mdb:contentInfo
    # ?mdb:distributionInfo
    # ?mdb:dataQualityInfo
    # ?mdb:resourceLineage
    # ?mdb:portrayalCatalogueInfo
    # ?mdb:metadataConstraints
    # ?mdb:applicationSchemaInfo
    # ?mdb:metadataMaintenance
    # ?mdb:acquisitionInformation

    def as_bf(self):
        return {
            "mdb:contact": bf(self.contact),
            "mdb:dateInfo": bf(self.dateInfo),
            "mdb:identificationInfo": bf(self.identificationInfo),
        }

    def add_dateInfo(self, *args, **kwargs):
        self.dateInfo.append(make("cit:CI_Date", *args, **kwargs))

    def add_contact(self, *args, **kwargs):
        self.contact.append(make("cit:CI_Responsibility", *args, **kwargs))

    def add_identificationInfo(self, *args, **kwargs):
        # citation(title)
        # abstract
        self.identificationInfo.append(
            make("mri:MD_DataIdentification", *args, **kwargs)
        )
        # TODO: choose between
        # self.identificationInfo.append(make("srv:SV_ServiceIdentification", *args, **kwargs))
