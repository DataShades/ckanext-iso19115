import pytest
from ckanext.iso19115 import utils


@pytest.mark.schematron_metadata
@pytest.mark.schematron_identification
@pytest.mark.schematron_constraints
@pytest.mark.schematron_maintenance
@pytest.mark.schematron_extent
@pytest.mark.schematron_medium
@pytest.mark.schematron_quality
@pytest.mark.schematron_service
@pytest.mark.schematron_citation
@pytest.mark.schematron_extended
@pytest.mark.schematron_catalogue
@pytest.mark.schematron_measure
@pytest.mark.xml_example("v3.2/basic.xml")
def test_basic(schema_errors, schematron_errors):
    errors = schema_errors + schematron_errors
    assert not errors, "\n".join(errors)


@pytest.mark.schematron_metadata
@pytest.mark.schematron_identification
@pytest.mark.schematron_constraints
@pytest.mark.schematron_maintenance
@pytest.mark.schematron_extent
@pytest.mark.schematron_medium
@pytest.mark.schematron_quality
@pytest.mark.schematron_service
@pytest.mark.schematron_citation
@pytest.mark.schematron_extended
@pytest.mark.schematron_catalogue
@pytest.mark.schematron_measure
@pytest.mark.xml_example("v3.2/minimal.xml")
def test_minimal(schema_errors, schematron_errors):
    errors = schema_errors + schematron_errors
    assert not errors, "\n".join(errors)


@pytest.mark.schematron_metadata
@pytest.mark.schematron_identification
@pytest.mark.schematron_constraints
@pytest.mark.schematron_maintenance
@pytest.mark.schematron_extent
@pytest.mark.schematron_medium
@pytest.mark.schematron_quality
@pytest.mark.schematron_service
@pytest.mark.schematron_citation
@pytest.mark.schematron_extended
@pytest.mark.schematron_catalogue
@pytest.mark.schematron_measure
@pytest.mark.xml_example("v3.2/identification.xml")
def test_identification(schema_errors, schematron_errors):
    errors = schema_errors + schematron_errors
    assert not errors, "\n".join(errors)


class TestXsd:
    pass


@pytest.mark.schematron_metadata
class TestSchMetadata:
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


@pytest.mark.schematron_identification
class TestSchIdentification:
    @pytest.mark.xml_example("v3.2/identification_no_geo.xml")
    def test_identification_dataset_no_geo(self, schematron_errors):
        assert schematron_errors

    @pytest.mark.xml_example("v3.2/identification_no_category.xml")
    def test_identification_no_category(self, schematron_errors):
        assert schematron_errors
