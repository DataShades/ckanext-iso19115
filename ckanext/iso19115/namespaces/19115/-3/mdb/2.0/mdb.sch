<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:ns prefix="cit" uri="http://standards.iso.org/iso/19115/-3/cit/2.0"/>
  <sch:ns prefix="mri" uri="http://standards.iso.org/iso/19115/-3/mri/1.0"/>
  <sch:ns prefix="mdb" uri="http://standards.iso.org/iso/19115/-3/mdb/2.0"/>
  <sch:ns prefix="mcc" uri="http://standards.iso.org/iso/19115/-3/mcc/1.0"/>
  <sch:ns prefix="lan" uri="http://standards.iso.org/iso/19115/-3/lan/1.0"/>
  <sch:ns prefix="gco" uri="http://standards.iso.org/iso/19115/-3/gco/1.0"/>
  <!--
    ISO 19115-3 base requirements for metadata instance documents

    See ISO19115-1:2014(E) page 10, Figure 5
  -->

  <!--
    Rule: Check root element.
    Ref: N/A
  -->
  <sch:pattern id="rule.mdb.root-element">
    <sch:title>Metadata document root element</sch:title>

    <sch:p>A metadata instance document conforming to
      this specification SHALL have a root MD_Metadata element
      defined in the http://standards.iso.org/iso/19115/-3/mdb/1.0 namespace.</sch:p>
    <sch:rule context="/">
      <sch:let name="hasOneMD_MetadataElement"
               value="count(/mdb:MD_Metadata) = 1"/>

      <sch:assert test="$hasOneMD_MetadataElement">The root element must be MD_Metadata.</sch:assert>

      <sch:report test="$hasOneMD_MetadataElement"/>
    </sch:rule>
  </sch:pattern>


  <!--
    Rule:
    Ref: {defaultLocale documented if not defined by the encoding}
    This can't be validated because the encoding is part of the default locale ? TODO-QUESTION

    Ref: {defaultLocale.PT_Locale.characterEncoding default value is UTF-8}
    Check that encoding is not empty.
  -->
  <sch:pattern id="rule.mdb.defaultlocale">
    <sch:title>Default locale</sch:title>

    <sch:p>The default locale MUST be documented if
      not defined by the encoding. The default value for the character
      encoding is "UTF-8".</sch:p>
    <sch:rule context="/mdb:MD_Metadata/mdb:defaultLocale|
                       /mdb:MD_Metadata/mdb:identificationInfo/*/mri:defaultLocale">

      <sch:let name="encoding"
        value="string(lan:PT_Locale/lan:characterEncoding/
                  lan:MD_CharacterSetCode/@codeListValue)"/>

      <sch:let name="hasEncoding"
        value="normalize-space($encoding) != ''"/>

      <sch:assert test="$hasEncoding">The default locale character encoding is "UTF-8".</sch:assert>
      <sch:report test="$hasEncoding"/>
    </sch:rule>
  </sch:pattern>


  <!--
    Rule:
    Ref: {count(MD_Metadata.parentMetadata) > 0 when there is an higher
    level object}
    Comment: Can't be validated using schematron AFA the existence
    of an higher level object can't be checked. TODO-QUESTION
  -->


  <!--
    Rule:
    Ref: {count(MD_Metadata.metadataScope) > 0 if
    MD_Metadata.metadataScope.MD_MetadataScope.resourceScope
    not equal to "dataset"}

    Ref: {name is mandatory if resourceScope not equal to "dataset"}
  -->
  <sch:pattern id="rule.mdb.scope-name">
    <sch:title>Metadata scope Name</sch:title>

    <sch:p>If a MD_MetadataScope element is present,
      the name property MUST have a value if resourceScope is not equal to "dataset"</sch:p>

    <sch:rule context="/mdb:MD_Metadata/mdb:metadataScope/
                          mdb:MD_MetadataScope[not(mdb:resourceScope/
                            mcc:MD_ScopeCode/@codeListValue = 'dataset')]">

      <sch:let name="scopeCode"
        value="mdb:resourceScope/mcc:MD_ScopeCode/@codeListValue"/>

      <sch:let name="scopeCodeName"
        value="normalize-space(mdb:name)"/>
      <sch:let name="hasScopeCodeName"
        value="normalize-space($scopeCodeName) != ''"/>

      <sch:let name="nilReason"
        value="mdb:name/@gco:nilReason"/>
      <sch:let name="hasNilReason"
        value="$nilReason != ''"/>

      <sch:assert test="$hasScopeCodeName or $hasNilReason">Specify a name for the metadata scope
      (required if the scope code is not "dataset"</sch:assert>

      <sch:report test="$hasScopeCodeName or $hasNilReason"/>
    </sch:rule>
  </sch:pattern>


  <!--
    Rule: At least one creation date
    Ref: {count(MD _Metadata.dateInfo.CI_Date.dateType.CI_DateTypeCode= "creation") > 0}
  -->
  <sch:pattern id="rule.mdb.create-date">
    <sch:title>Metadata create date</sch:title>

    <sch:p>A dateInfo property value with data type = "creation"
      MUST be present in every MD_Metadata instance.</sch:p>

    <sch:rule context="mdb:MD_Metadata">
      <sch:let name="creationDates"
        value="./mdb:dateInfo/cit:CI_Date[
                    normalize-space(cit:date/gco:DateTime) != '' and
                    cit:dateType/cit:CI_DateTypeCode/@codeListValue = 'creation']/
                  cit:date/gco:DateTime"/>

      <!-- Check at least one non empty creation date element is defined. -->
      <sch:let name="hasAtLeastOneCreationDate"
        value="count(./mdb:dateInfo/cit:CI_Date[
                    normalize-space(cit:date/gco:DateTime) != '' and
                    cit:dateType/cit:CI_DateTypeCode/@codeListValue = 'creation']
                    ) &gt; 0"/>

      <sch:assert test="$hasAtLeastOneCreationDate">
	Specify a creation date for the metadata record in the metadata section.
      </sch:assert>
      <sch:report test="$hasAtLeastOneCreationDate"/>
    </sch:rule>
  </sch:pattern>
</sch:schema>
