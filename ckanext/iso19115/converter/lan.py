from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from ckanext.iso19115.converter import bf, make

if TYPE_CHECKING:
    from .. import types


@dataclass
class PT_Locale:
    language: str  # codelist("LanguageCode")
    country: Optional[str] = None  # codelist("CountryCode")
    characterEncoding: Optional[str] = None  # codelist("MD_CharacterSetCode")
