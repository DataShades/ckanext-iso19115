"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import pytest
from ckan.plugins import plugin_loaded
from lxml.etree import XML, dump
import ckanext.iso19115.plugin as plugin

# @pytest.mark.ckan_config("ckan.plugins", "iso19115")
# @pytest.mark.usefixtures("with_plugins")
# def test_plugin():
#     assert plugin_loaded("iso19115")


def test_valid_mds(mds_schema, examples, mdb_schematron):
    path = examples / "basic2.xml"
    mds_schema.validate(path)
    mds_schema.validate(path)
    if not mdb_schematron.validate(XML(path.open("rb").read())):
        report = mdb_schematron.validation_report
        failed = report.xpath("//*[local-name() = 'failed-assert']")
        errors = '\n'.join(
            "".join(f.itertext())
            for f in failed
        )
        assert False, errors
