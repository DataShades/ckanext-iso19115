from __future__ import annotations

from xmlschema import etree_tostring

import ckanext.iso19115.converter as c
import ckanext.iso19115.types as t
import ckanext.iso19115.utils as utils


def print_xml(el):
    print(etree_tostring(el, namespaces=utils.ns))


class TestConverter:
    def test_bf(self, faker, mocker):
        word = faker.random_element(
            utils.codelist_options("CI_DateTypeCode")
        ).name
        dt = faker.date_time()
        el = c.make("cit:CI_Date", dt, word)
        assert c.bf(el, False) == {
            "cit:date": {"gco:DateTime": {"$": dt.isoformat()}},
            "cit:dateType": {
                "cit:CI_DateTypeCode": {
                    "$": word,
                    "@codeListValue": word,
                    "@codeList": mocker.ANY,
                }
            },
        }

    def test_full(self, faker, mocker):
        el: t.mdb.MD_Metadata = c.make("mdb:MD_Metadata")

        word1 = faker.random_element(
            utils.codelist_options("CI_DateTypeCode")
        ).name
        dt1 = faker.date_time()
        word2 = faker.random_element(
            utils.codelist_options("CI_DateTypeCode")
        ).name
        dt2 = faker.date_time()

        el.add_dateInfo(dt1, word1)
        el.add_dateInfo(dt2, word2)
        assert c.bf(el, False) == {
            "mdb:contact": {},
            "mdb:dateInfo": [
                {
                    "cit:CI_Date": {
                        "cit:date": {"gco:DateTime": {"$": dt1.isoformat()}},
                        "cit:dateType": {
                            "cit:CI_DateTypeCode": {
                                "$": word1,
                                "@codeListValue": word1,
                                "@codeList": mocker.ANY,
                            }
                        },
                    }
                },
                {
                    "cit:CI_Date": {
                        "cit:date": {"gco:DateTime": {"$": dt2.isoformat()}},
                        "cit:dateType": {
                            "cit:CI_DateTypeCode": {
                                "$": word2,
                                "@codeListValue": word2,
                                "@codeList": mocker.ANY,
                            }
                        },
                    }
                },
            ],
            "mdb:identificationInfo": {},
        }

    def test_minimal_xml(self, faker):
        el: t.mdb.MD_Metadata = c.make("mdb:MD_Metadata")
        dt1 = faker.date_time()
        el.add_dateInfo(dt1, "creation")
        data = c.bf(el, False)
        builder = utils.get_builder("mdb:MD_Metadata")
        assert builder.build(data)

    def test_with_party(self, faker):
        el: t.mdb.MD_Metadata = c.make("mdb:MD_Metadata")
        el.add_dateInfo(faker.date_time().date(), "creation")
        el.add_contact("author")

        builder = utils.get_builder("mdb:MD_Metadata")
        data = c.bf(el, False)
        builder.build(data)

    def test_with_identification(self, faker):
        el: t.mdb.MD_Metadata = c.make("mdb:MD_Metadata")
        el.add_dateInfo(faker.date_time().date(), "creation")
        el.add_identificationInfo(
            abstract=faker.sentence(),
            citation=c.make("cit:CI_Citation", faker.sentence()),
        )

        builder = utils.get_builder("mdb:MD_Metadata")
        data = c.bf(el, False)
        builder.build(data)
