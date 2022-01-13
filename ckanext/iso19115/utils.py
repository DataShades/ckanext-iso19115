from __future__ import annotations

import functools
import pickle
from pathlib import Path

import xmlschema
from lxml import isoschematron, etree
import ckan.plugins.toolkit as tk
from xmlschema import namespaces

_root = Path(__file__).parent.parent.parent

_codelists = _root / "namespaces/19115/resources/Codelists/cat/codelists.xml"

_ns = {
    "cat": "http://standards.iso.org/iso/19115/-3/cat/1.0",
    "cit": "http://standards.iso.org/iso/19115/-3/cit/2.0",
    "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",
    "gex": "http://standards.iso.org/iso/19115/-3/gex/1.0",
    "lan": "http://standards.iso.org/iso/19115/-3/lan/1.0",
    "mac": "http://standards.iso.org/iso/19115/-3/mac/2.0",
    "mas": "http://standards.iso.org/iso/19115/-3/mas/1.0",
    "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
    "mco": "http://standards.iso.org/iso/19115/-3/mco/1.0",
    "mdb": "http://standards.iso.org/iso/19115/-3/mdb/2.0",
    "mdq": "http://standards.iso.org/iso/19157/-2/mdq/1.0",
    "mmi": "http://standards.iso.org/iso/19115/-3/mmi/1.0",
    "mpc": "http://standards.iso.org/iso/19115/-3/mpc/1.0",
    "mrc": "http://standards.iso.org/iso/19115/-3/mrc/2.0",
    "mrd": "http://standards.iso.org/iso/19115/-3/mrd/1.0",
    "mri": "http://standards.iso.org/iso/19115/-3/mri/1.0",
    "mrl": "http://standards.iso.org/iso/19115/-3/mrl/2.0",
    "mrs": "http://standards.iso.org/iso/19115/-3/mrs/1.0",
    "msr": "http://standards.iso.org/iso/19115/-3/msr/2.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}
_schema_mapping = {
    "metadata": _root / "namespaces/19115/-3/mdb/2.0/mdb.xsd",
}

_schematron_mapping = {
    "metadata": _root / "schematron/mdb.xml",
    "identification": _root / "schematron/mri.xml",
    "constraints": _root / "schematron/mco.xml",
    "maintenance": _root / "schematron/mmi.xml",
    "extent": _root / "schematron/gex.xml",
    "medium": _root / "schematron/mrd.xml",
    "quality": _root / "schematron/dqm.xml",
    "service": _root / "schematron/srv.xml",
    "citation": _root / "schematron/cit.xml",
    "extended": _root / "schematron/mex.xml",
    "catalogue": _root / "schematron/mrc.xml",
    "measure": _root / "schematron/mdq.xml",
}

for f in _schema_mapping.values():
    assert (
        f.is_file()
    ), f"Schema {f} does not exists. Have you extracted namespaces.zip?"


for f in _schematron_mapping.values():
    assert (
        f.is_file()
    ), f"Schema {f} does not exists. Have you extracted namespaces.zip?"


def validate_schema(name: str, content: bytes):
    schema: xmlschema.XMLSchema
    cache = _root / "serialized" / f"{name}.pickle"
    if not cache.is_file():
        schema = xmlschema.XMLSchema(str(_schema_mapping[name]))
        with cache.open("wb") as dest:
            pickle.dump(schema, dest)
    with cache.open("rb") as src:
        schema = pickle.load(src)
    try:
        schema.validate(content)
    except xmlschema.XMLSchemaValidationError as e:
        raise tk.ValidationError({"schema": [e.message + " " + e.reason]})


def validate_schematron(name: str, content: bytes):
    path = str(_schematron_mapping[name])
    with open(path, "rb") as src:
        sch = isoschematron.Schematron(
            etree.XML(src.read()), store_report=True
        )
    if sch.validate(etree.XML(content)):
        return

    failed = sch.validation_report.xpath(
        "//*[local-name() = 'failed-assert']/*[text()]"
    )
    raise tk.ValidationError(
        {
            "schematron": [
                " ".join(l.strip() for l in f.itertext()) for f in failed
            ]
        }
    )


@functools.lru_cache()
def codelist(name: str):
    xml = etree.XML(_codelists.open("rb").read())
    xpath = f"//cat:codelistItem/cat:CT_Codelist[@id='{name}']/cat:codeEntry/cat:CT_CodelistValue"
    codes = xml.xpath(xpath, namespaces=_ns)
    return {
        code.find("cat:identifier/gco:ScopedName", namespaces=_ns)
        .text: code.find("cat:definition/gco:CharacterString", namespaces=_ns)
        .text
        for code in codes
    }
