
import pickle
from pathlib import Path
import pytest
import xmlschema

@pytest.fixture(scope="session")
def examples():
    return Path(__file__).parent / "examples"

def _repo_schema() -> xmlschema.XMLSchema:
    return xmlschema.XMLSchema(Path(__file__).parent.parent.parent.parent / "XML/standards.iso.org/iso/19115/-3/mdb/2.0/mdb.xsd")


def _download_schema(schema: xmlschema.XMLSchema):
    schema.export(str(Path(__file__).parent / "xsd"), True)


def _downloaded_schema() -> xmlschema.XMLSchema:
    return xmlschema.XMLSchema(Path(__file__).parent / "xsd/mdb.xsd")

def _serialize_schema(schema: xmlschema.XMLSchema):
    with (Path(__file__).parent / "mdb.pkl").open("wb") as dest:
        pickle.dump(schema, dest)


def _serialized_schema() -> xmlschema.XMLSchema:
    with (Path(__file__).parent / "mdb.pkl").open("rb") as src:
        return pickle.load(src)


def _namespace_schema() -> xmlschema.XMLSchema:
    return xmlschema.XMLSchema(Path(__file__).parent.parent.parent.parent / "namespaces/19115/-3/mdb/2.0/mdb.xsd")


@pytest.fixture(scope="session")
def mdb_schema():
    schema =  _serialized_schema()
    return schema
