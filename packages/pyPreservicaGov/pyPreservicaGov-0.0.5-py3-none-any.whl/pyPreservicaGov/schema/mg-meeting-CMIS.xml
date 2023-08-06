<?xml version="1.0" encoding="utf-8" standalone="yes"?>

<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:meeting="https://moderngov.gov.uk/meeting"
    xmlns="http://www.tessella.com/sdb/cmis/metadata"
    exclude-result-prefixes="meeting">

  <xsl:output method='xml' indent='yes'/>

  <xsl:template match="meeting:meeting">
    <group>
      <title>Civica Modern.Gov Meeting</title>
      <xsl:apply-templates/>
    </group>
  </xsl:template>

  <xsl:template match="meeting:refertocommittee|meeting:meetingstatus|meeting:agendaitemtitle|meeting:meetinglocation|meeting:title">
    <item>
      <name><xsl:value-of select="fn:replace(translate(local-name(), '_', ' '), '([a-z])([A-Z])', '$1 $2')"/></name>
      <value><xsl:value-of select="."/></value>
      <type><xsl:value-of select="fn:replace(translate(local-name(), '_', ' '), '([a-z])([A-Z])', '$1 $2')"/></type>
    </item>
  </xsl:template>

</xsl:stylesheet>
