from __future__ import annotations
from dataclasses import dataclass, field


import datetime

from typing import TYPE_CHECKING, Any, Optional, Union
from . import bf, make, codelist
if TYPE_CHECKING:
    from .. import types


@dataclass
class CI_Date:
    date: Union[types.gco.Date, types.gco.DateTime]
    dateType: str

    def __post_init__(self):
        if isinstance(self.date, datetime.datetime):
            self.date = make("gco:DateTime", self.date)
        elif isinstance(self.date, datetime.date):
            self.date = make("gco:Date", self.date)


    def as_bf(self):
        data = {
            "cit:date": bf(self.date),
            "cit:dateType": {
                "cit:CI_DateTypeCode": codelist("CI_DateTypeCode", self.dateType)
            },
        }
        return data

@dataclass
class CI_Telephone:
     number: str
     numberType: Optional[str] = None # codelist("CI_TelephoneTypeCode")

@dataclass
class CI_Address:
     deliveryPoint: list[str] = field(default_factory=list)
     city: Optional[str] = None
     administrativeArea: Optional[str] = None
     postalCode: Optional[str] = None
     country: Optional[str] = None
     electronicMailAddress: list[str] = field(default_factory=list)


@dataclass
class CI_OnlineResource:
     linkage: str
     protocol: Optional[str] = None
     applicationProfile: Optional[str] = None
     name: Optional[str] = None
     description: Optional[str] = None
     function: Optional[str] = None # codelist("CI_OnLineFunctionCode")
     protocolRequest: Optional[str] = None


@dataclass
class CI_Contact:
    phone: list[CI_Telephone] = field(default_factory=list)
    address: list[CI_Address] = field(default_factory=list)
    onlineResource: list[CI_OnlineResource] = field(default_factory=list)
    hoursOfService: list[str] = field(default_factory=list)
    contactInstructions: Optional[str] = None
    contactType: Optional[str] = None


@dataclass
class AbstractCI_Party:
    name: Optional[str] = None
    contactInfo: list[CI_Contact] = field(default_factory=list)
    partyIdentifier: list[types.mcc.MD_Identifier] = field(default_factory=list)


@dataclass
class CI_Individual(AbstractCI_Party):
    positionName: Optional[str] = None

@dataclass
class CI_Organisation:
    logo: list[types.mcc.MD_BrowseGraphic] = field(default_factory=list)
    individual: list[CI_Individual] = field(default_factory=list)

@dataclass
class CI_Responsibility:
    role: str
    # cit:extent
    party: list[AbstractCI_Party] = field(default_factory=list)

    def as_bf(self):
        data = {
            "cit:role": {
                "cit:CI_RoleCode": codelist("CI_RoleCode", self.role)
            },
            "cit:party": [{
                "cit:CI_Individual": {}
            }]
        }
        return data


@dataclass
class CI_Series:
    name: Optional[str] = None
    issueIdentification: Optional[str] = None
    page: Optional[str] = None


@dataclass
class CI_Citation:
     title: str
     alternateTitle: list[str] = field(default_factory=list)
     date: list[CI_Date] = field(default_factory=list)
     edition: Optional[str] = None
     editionDate: Optional[types.gco.DateTime] = None
     identifier: list[types.mcc.MD_Identifier] = field(default_factory=list)
     citedResponsibleParty: list[CI_Responsibility] = field(default_factory=list)
     presentationForm: list[str] = field(default_factory=list) # codelist("CI_PresentationFormCode")
     series: Optional[CI_Series] = None
     otherCitationDetails: list[str] = field(default_factory=list)
     ISBN: Optional[str] = None
     ISSN: Optional[str] = None
     onlineResource: list[CI_OnlineResource] = field(default_factory=list)
     graphic: list[types.mcc.MD_BrowseGraphic] = field(default_factory=list)
