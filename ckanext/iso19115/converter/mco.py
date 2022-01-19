from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .. import types


@dataclass
class MD_Constraints:
    useLimitation: list[str] = field(default_factory=list)
    constraintApplicationScope: Optional[types.mcc.MD_Scope] = None
    graphic: list[types.mcc.MD_BrowseGraphic] = field(default_factory=list)
    reference: list[types.cit.CI_Citation] = field(default_factory=list)
    releasability: Optional[MD_Releasability] = None
    responsibleParty: list[types.cit.CI_Responsibility] = field(
        default_factory=list
    )


@dataclass
class MD_Releasability:
    addressee: list[types.cit.CI_Responsibility] = field(default_factory=list)
    statement: Optional[str] = None
    disseminationConstraints: list[str] = field(
        default_factory=list
    )  # codelist("MD_RestrictionCode")
