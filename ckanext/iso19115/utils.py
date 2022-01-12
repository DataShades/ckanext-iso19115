from __future__ import annotations

import pickle
from pathlib import Path

import xmlschema
from lxml import isoschematron, etree
import ckan.plugins.toolkit as tk

_root = Path(__file__).parent.parent.parent

_schema_mapping = {
    "metadata": _root / "namespaces/19115/-3/mda/2.0/mda.xsd",
}

_schematron_mapping = {
    "metadata": _root / "schematron/metadata.xml",
}

for f in _schema_mapping.values():
    assert f.is_file(), f"Schema {f} does not exists. Have you extracted namespaces.zip?"


for f in _schematron_mapping.values():
    assert f.is_file(), f"Schema {f} does not exists. Have you extracted namespaces.zip?"

def validate_schema(name: str, content: bytes):
    cache = _root / "serialized" / f"{name}.pickle"
    if not cache.is_file():
        schema = xmlschema.XMLSchema(str(_schema_mapping[name]))
        with cache.open("wb") as dest:
            pickle.dump(schema, dest)
    with cache.open("rb") as src:
        schema =  pickle.load(src)

    try:
        schema.validate(content)
    except xmlschema.XMLSchemaValidationError as e:
        raise tk.ValidationError({"schema": [
            e.message + e.reason
        ]})



def validate_schematron(name: str, content: bytes):
    path = str(_schematron_mapping[name])
    with open(path, "rb") as src:
        sch = isoschematron.Schematron(etree.XML(src.read()), store_report=True)

    if sch.validate(etree.XML(content)):
        return


    failed = sch.validation_report.xpath("//*[local-name() = 'failed-assert']/*[text()]")

    raise tk.ValidationError({"schematron": [
        " ".join(l.strip() for l in f.itertext())
        for f in failed
    ]})
