from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import types


@dataclass
class DQ_DataQuality:
    ...