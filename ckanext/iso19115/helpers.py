from __future__ import annotations

import functools
import re
import logging
from typing import Any, Optional, TypedDict, Union

import pycountry
import ckan.plugins.toolkit as tk
from . import utils

_swap_case = re.compile("(?<=[a-z])(?=[A-Z])")

CONFIG_LANGUAGES = "ckanext.iso19115.metadata.supported_languages"
DEFAULT_LANGUAGES = "eng"

log = logging.getLogger(__name__)

def get_helpers():
    return {
        "iso19115_implementation_as_options": implementations,
        "iso19115_codelist_as_options": codelist,
        "iso19115_languages": languages,
        "iso19115_option_label": option_label,
    }


class AnnotatedOption(TypedDict):
    value: str
    label: str
    annotation: Optional[str]


def languages(field: dict[str, Any]):
    return _get_languages()


@functools.lru_cache(1)
def _get_languages() -> list[AnnotatedOption]:
    supported = tk.aslist(tk.config.get(CONFIG_LANGUAGES, DEFAULT_LANGUAGES))
    languages = (
        map(pycountry.languages.lookup, supported)
        if supported
        else pycountry.languages
    )

    return [
        AnnotatedOption(value=l.alpha_3, label=l.name, annotation=None)
        for l in languages
    ]


@functools.lru_cache()
def _get_implementations(el: str) -> list[AnnotatedOption]:
    from ckanext.iso19115.utils import get_builder

    base = get_builder(el)
    options = []
    for impl in base.implementations():
        name = impl.name(False)
        if not name:
            continue
        label = _uncamelize(name.split(":")[-1].replace("_", " "))
        options.append(
            AnnotatedOption(
                value=name, label=label, annotation=impl.annotation()
            )
        )

    return options


def implementations(field: dict[str, Any]):
    return _get_implementations(field["iso19115_source"])


@functools.lru_cache()
def _get_codelist(name: str) -> list[AnnotatedOption]:
    return [
        AnnotatedOption(
            value=code.name,
            label=_uncamelize(code.name).capitalize(),
            annotation=code.definition,
        )
        for code in utils.codelist_options(name)
    ]


def codelist(field: dict[str, Any]):
    return _get_codelist(field["iso19115_source"])


def _uncamelize(v):
    return _swap_case.sub(" ", v)


def option_label(type_: str, field: Union[str, list[str]], value: str, entity: str = "dataset"):
    schema = tk.h.scheming_get_schema(entity, type_)
    if not schema:
        log.warning("Schema for %s type %s is not defined", entity, type_)
        return value

    if isinstance(field, str):
        field = [field]
    fields = schema['dataset_fields']
    field_data = {}

    for step in field:
        field_data = tk.h.scheming_field_by_name(fields, step)
        if not field_data:
            log.warning("Field %s is not defined inside %s schema", field, type_)
            return value
        if "repeating_subfields" in field_data:
            fields = field_data['repeating_subfields']

    choices = tk.h.scheming_field_choices(field_data)
    if not choices:
        log.warning("Field %s from the %s schema does not have choices", field, type_)
        return value

    return tk.h.scheming_choices_label(choices, value)
