
import pickle
from pathlib import Path
import pytest
import xmlschema

from lxml import isoschematron, etree

_root = Path(__file__).parent.parent.parent.parent

@pytest.fixture(scope="session")
def examples():
    return Path(__file__).parent / "examples"

def _repo_schema() -> xmlschema.XMLSchema:
    return xmlschema.XMLSchema(str(_root / "XML/standards.iso.org/iso/19115/-3/mds/2.0/mds.xsd"))


def _download_schema(schema: xmlschema.XMLSchema):
    schema.export(str(Path(__file__).parent / "xsd"), True)


def _downloaded_schema() -> xmlschema.XMLSchema:
    return xmlschema.XMLSchema(str(Path(__file__).parent / "xsd/mds.xsd"))

def _serialize_schema(schema: xmlschema.XMLSchema):
    with (Path(__file__).parent / "mds.pkl").open("wb") as dest:
        pickle.dump(schema, dest)


def _serialized_schema() -> xmlschema.XMLSchema:
    with (Path(__file__).parent / "mds.pkl").open("rb") as src:
        return pickle.load(src)



def _namespace_schema() -> xmlschema.XMLSchema:
    return xmlschema.XMLSchema(str(_root / "namespaces/19115/-3/mda/2.0/mda.xsd"))


@pytest.fixture(scope="session")
def mds_schema():
    return _serialized_schema()
    schema =  _namespace_schema()
    _serialize_schema(schema)
    return schema

@pytest.fixture(scope="session")
def mdb_schematron():
    schema = str(_root / "namespaces/19115/-3/mdb/2.0/mdb.sch")
    with open(schema, "rb") as src:
        return isoschematron.Schematron(etree.XML(src.read()), store_report=True)
