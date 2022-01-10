

from pathlib import Path
import pytest
import xmlschema

@pytest.fixture(scope="session")
def examples():
    return Path(__file__).parent / "examples"

@pytest.fixture(scope="session")
def mdb_schema():
    # return xmlschema.XMLSchema(Path(__file__).parent.parent.parent.parent / "XML/standards.iso.org/iso/19115/-3/mdb/2.0/mdb.xsd")
    return xmlschema.XMLSchema(Path(__file__).parent / "xsd/mdb.xsd")
