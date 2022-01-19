from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from ckanext.iso19115.converter import bf, make

if TYPE_CHECKING:
    from .. import types


@dataclass
class MD_Resolution:
    ...


@dataclass
class MD_Keywords:
    ...


@dataclass
class MD_Usage:
    ...


@dataclass
class MD_AssociatedResource:
    ...


from .mcc import Abstract_ResourceDescription


@dataclass
class MD_DataIdentification(Abstract_ResourceDescription):
    defaultLocale: Optional[types.lan.PT_Locale] = None
    otherLocale: list[types.lan.PT_Locale] = field(default_factory=list)
    environmentDescription: Optional[str] = None
    supplementalInformation: Optional[str] = None
