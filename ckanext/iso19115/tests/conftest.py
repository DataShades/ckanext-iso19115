
from pathlib import Path
import pytest
from ckanext.iso19115 import utils
import ckan.plugins.toolkit as tk

@pytest.fixture(scope="session")
def examples():
    return Path(__file__).parent / "examples"

@pytest.fixture()
def example(examples, request):
    name  = next(m.args[0] for m in request.node.own_markers if m.name == 'xml_example')
    path = examples / name
    return path.open("rb").read()

@pytest.fixture()
def schema_errors(example):
    try:
        utils.validate_schema("metadata", example)
    except tk.ValidationError as e:
        return e.error_dict["schema"]
    return []

@pytest.fixture()
def schematron_errors(example):
    try:
        utils.validate_schematron("metadata", example)
    except tk.ValidationError as e:
        return e.error_dict["schematron"]
    return []
