<?xml version = "1.0" encoding = "UTF-8"?>
<!--
  #%L
  OME Data Model transforms
  %%
  Copyright (C) 2009 - 2016 Open Microscopy Environment:
    - Massachusetts Institute of Technology
    - National Institutes of Health
    - University of Dundee
    - Board of Regents of the University of Wisconsin-Madison
  %%
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
  POSSIBILITY OF SUCH DAMAGE.
  #L%
  -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:OME="http://www.openmicroscopy.org/Schemas/OME/2015-01"
                xmlns:Bin="http://www.openmicroscopy.org/Schemas/BinaryFile/2015-01"
                xmlns:SPW="http://www.openmicroscopy.org/Schemas/SPW/2015-01"
                xmlns:SA="http://www.openmicroscopy.org/Schemas/SA/2015-01"
                xmlns:ROI="http://www.openmicroscopy.org/Schemas/ROI/2015-01"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xml="http://www.w3.org/XML/1998/namespace"
                xmlns:str="http://exslt.org/strings"
                exclude-result-prefixes="OME Bin SPW SA ROI"
                xmlns:exsl="http://exslt.org/common"
                extension-element-prefixes="exsl" version="1.0">

  <xsl:variable name="newOMENS">http://www.openmicroscopy.org/Schemas/OME/2016-06</xsl:variable>
  <xsl:variable name="newSPWNS">http://www.openmicroscopy.org/Schemas/OME/2016-06</xsl:variable>
  <xsl:variable name="newBINNS">http://www.openmicroscopy.org/Schemas/OME/2016-06</xsl:variable>
  <xsl:variable name="newROINS">http://www.openmicroscopy.org/Schemas/OME/2016-06</xsl:variable>
  <xsl:variable name="newSANS">http://www.openmicroscopy.org/Schemas/OME/2016-06</xsl:variable>

  <xsl:output method="xml" indent="yes"/>
  <xsl:preserve-space elements="*"/>

  <!-- Actual schema changes -->

  <!-- Rewrite abstract elements for Shape and LightSource -->
  <xsl:template name="tokenize">
    <xsl:param name="string"/>
    <xsl:param name="separator" select="','"/>
    <xsl:choose>
      <xsl:when test="contains($string,$separator)">
        <token>
          <xsl:value-of select="substring-before($string,$separator)"/>
        </token>
        <xsl:call-template name="tokenize">
          <xsl:with-param name="string" select="substring-after($string,$separator)"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <token><xsl:value-of select="$string"/></token>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:variable name="lightSources">
    <xsl:call-template name="tokenize">
      <xsl:with-param name="string" select="'Laser,Arc,Filament,LightEmittingDiode,GenericExcitationSource'"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="shapes">
    <xsl:call-template name="tokenize">
      <xsl:with-param name="string" select="'Line,Rectangle,Mask,Ellipse,Point,Polyline,Polygon,Label'"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:template match="OME:LightSource">
    <xsl:variable name="lightSourceRoot" select="." />
    <xsl:variable name="lightSourceType"  >
      <xsl:for-each select="exsl:node-set($lightSources)/*">
        <xsl:variable name="lightSource" select="." />
        <xsl:if test="($lightSourceRoot/*[name()= $lightSource]) or ($lightSourceRoot/*[name()= concat('OME:',$lightSource)])">
          <xsl:value-of select="."/>
        </xsl:if>
      </xsl:for-each>
    </xsl:variable>
    <xsl:element name="{$lightSourceType}"  namespace="{$newOMENS}">
      <xsl:apply-templates select="@*|*[name()=$lightSourceType]/@*|*[name()=concat('OME:',$lightSourceType)]/@*"/>
      <xsl:apply-templates select="node()"/>
      <xsl:apply-templates select="*[name()=$lightSourceType]/node()"/>
      <xsl:apply-templates select="*[name()=concat('OME:',$lightSourceType)]/node()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="OME:Laser"/>
  <xsl:template match="OME:Arc"/>
  <xsl:template match="OME:Filament"/>
  <xsl:template match="OME:LightEmittingDiode"/>
  <xsl:template match="OME:GenericExcitationSource"/>

  <xsl:template match="ROI:Shape">
    <xsl:variable name="shapeRoot" select="." />
    <xsl:variable name="shapeType"  >
      <xsl:for-each select="exsl:node-set($shapes)/*">
        <xsl:variable name="shape" select="." />
        <xsl:if test="($shapeRoot/*[name()= $shape]) or ($shapeRoot/*[name()= concat('ROI:',$shape)])">
          <xsl:value-of select="."/>
        </xsl:if>
      </xsl:for-each>
    </xsl:variable>
    <xsl:element name="{$shapeType}" namespace="{$newROINS}">
      <xsl:apply-templates select="@*|*[name()=$shapeType]/@*|*[name()=concat('ROI:',$shapeType)]/@*"/>
      <xsl:apply-templates select="node()"/>
      <xsl:apply-templates select="*[name()=$shapeType]/node()"/>
      <xsl:apply-templates select="*[name()=concat('ROI:',$shapeType)]/node()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="ROI:Line"/>
  <xsl:template match="ROI:Rectangle"/>
  <xsl:template match="ROI:Mask"/>
  <xsl:template match="ROI:Ellipse"/>
  <xsl:template match="ROI:Point"/>
  <xsl:template match="ROI:Polyline"/>
  <xsl:template match="ROI:Polygon"/>
  <xsl:template match="ROI:Label"/>

  <!-- strip Namespace from ROI -->
  <xsl:template match="ROI:ROI/@Namespace"/>

  <!-- strip LineCap from Shape -->
  <xsl:template match="ROI:Shape/@LineCap"/>

  <!-- strip Visible from Shape -->
  <xsl:template match="ROI:Shape/@Visible"/>

  <!-- for MarkerStart from Line have all markers be Arrow -->
  <xsl:template match="ROI:Line/@MarkerStart">
    <xsl:attribute name="MarkerStart">
      <xsl:text>Arrow</xsl:text>
    </xsl:attribute>
  </xsl:template>

  <!-- for MarkerEnd from Line have all markers be Arrow -->
  <xsl:template match="ROI:Line/@MarkerEnd">
    <xsl:attribute name="MarkerEnd">
      <xsl:text>Arrow</xsl:text>
    </xsl:attribute>
  </xsl:template>

  <!-- for MarkerStart from Polyline have all markers be Arrow -->
  <xsl:template match="ROI:Polyline/@MarkerStart">
    <xsl:attribute name="MarkerStart">
      <xsl:text>Arrow</xsl:text>
    </xsl:attribute>
  </xsl:template>

  <!-- for MarkerEnd from Polyline have all markers be Arrow -->
  <xsl:template match="ROI:Polyline/@MarkerEnd">
    <xsl:attribute name="MarkerEnd">
      <xsl:text>Arrow</xsl:text>
    </xsl:attribute>
  </xsl:template>

  <!-- Rewrite all namespaces -->

  <xsl:template match="OME:OME">
    <OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06"
         xmlns:OME="http://www.openmicroscopy.org/Schemas/OME/2016-06"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06
                             http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd">
      <xsl:apply-templates select="@UUID|@Creator|node()"/> <!-- copy UUID and Creator attributes and nodes -->
    </OME>
  </xsl:template>

  <!-- Move all BinaryFile, SA, SPW and ROI elements into the OME namespace -->

  <xsl:template match="OME:*">
    <xsl:element name="{local-name()}" namespace="{$newOMENS}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="Bin:*">
    <xsl:element name="{local-name()}" namespace="{$newBINNS}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="SA:*">
    <xsl:element name="{local-name()}" namespace="{$newSANS}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="SPW:*">
    <xsl:element name="{local-name()}" namespace="{$newSPWNS}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="ROI:*">
    <xsl:element name="{local-name()}" namespace="{$newROINS}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
  </xsl:template>

  <!-- Default processing -->

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
