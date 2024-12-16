from __future__ import annotations

from dataclasses import dataclass

from .base import Atomic


@dataclass
class FileName(Atomic):
    value: str


@dataclass
class MimeFileType(Atomic):
    value: str
