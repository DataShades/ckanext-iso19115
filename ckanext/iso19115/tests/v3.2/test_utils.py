import pytest
from ckanext.iso19115 import utils

@pytest.mark.xml_example("v3.2/basic.xml")
def test_basic(schema_errors, schematron_errors):
    errors = schema_errors + schematron_errors
    assert not errors, '\n'.join(errors)


@pytest.mark.xml_example("v3.2/minimal.xml")
def test_minimal(schema_errors, schematron_errors):
    errors = schema_errors + schematron_errors
    assert not errors, '\n'.join(errors)


class TestXsd:
    @pytest.mark.xml_example("v3.2/minimal.xml")
    def test_minimal(self, schema_errors):
        assert not schema_errors, '\n'.join(schema_errors)


class TestSch:
    @pytest.mark.xml_example("v3.2/minimal.xml")
    def test_minimal(self, schematron_errors):
        assert not schematron_errors, '\n'.join(schematron_errors)

    @pytest.mark.xml_example("v3.2/sch_no_default_locale.xml")
    def test_no_encoding(self, schematron_errors):
        assert schematron_errors
        assert "default locale" in schematron_errors[0]

    @pytest.mark.xml_example("v3.2/sch_no_root.xml")
    def test_no_root(self, schematron_errors):
        assert schematron_errors
        assert "root element" in schematron_errors[0]

    @pytest.mark.xml_example("v3.2/sch_non_dataset_scope.xml")
    def test_non_dataset_scope(self, schematron_errors):
        assert schematron_errors
        assert "scope code is not" in schematron_errors[0]
        assert "dataset" in schematron_errors[0]

    @pytest.mark.xml_example("v3.2/sch_no_creation_date.xml")
    def test_no_creation_date(self, schematron_errors):
        assert schematron_errors
        assert "creation date" in schematron_errors[0]
