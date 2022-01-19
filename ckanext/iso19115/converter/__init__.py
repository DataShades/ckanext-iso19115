from __future__ import annotations

import dataclasses
from typing import Any

from werkzeug.utils import import_string


def _get(el) -> Any:
    return import_string(".".join([__package__, el]))


def make(el, *args, **kwargs):
    return _get(el)(*args, **kwargs)


def bf(el: Any, as_child: bool = True):
    if dataclasses.is_dataclass(el):
        return _bf(el, as_child)

    result = [_bf(el, as_child) for el in el]
    return result or {}


def _bf(el: Any, as_child: bool):
    data = el.as_bf()
    name = type(el).__name__
    ns = el.__module__.split(".")[-1]
    if as_child:
        data = {f"{ns}:{name}": data}
    return data


def codelist(name: str, value: str) -> dict[str, str]:
    from ..utils import codelist_options

    options = codelist_options(name)
    for option in options:
        if option.name == value:
            break
    else:
        raise ValueError(
            f"Codelist [name] does not contain value {value}:"
            f" {[o.name for o in options]}"
        )
    return {
        "$": value,
        "@codeList": option.location,
        "@codeListValue": value,
    }
