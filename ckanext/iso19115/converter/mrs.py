from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .. import types


@dataclass
class MD_ReferenceSystem:

    referenceSystemIdentifier: Optional[types.mcc.MD_Identifier] = None
    referenceSystemType: Optional[
        str
    ] = None  # codelist("MD_ReferenceSystemTypeCode")
