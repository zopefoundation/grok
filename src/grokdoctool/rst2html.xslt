<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output indent="yes" mode="html"/>

    <xsl:template match="/document">
        <html>
            <head>
            <xsl:comment>
                <xsl:text>Generated from</xsl:text>
                <xsl:value-of select="@source"/>
            </xsl:comment>
            <title><xsl:value-of select="title"/></title>
            </head>
            <body>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="document/title">
        <h1><xsl:apply-templates/></h1>
    </xsl:template>

    <xsl:template match="section/title">
        <h2>
            <a name="{../@ids}">
                <xsl:value-of select="."/>
            </a>
        </h2>   
    </xsl:template>

    <xsl:template match="title_reference">
        <strong><xsl:apply-templates/></strong>
    </xsl:template>

    <xsl:template match="paragraph">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="section">
        <div class="section"><xsl:apply-templates/></div>
    </xsl:template>

    <xsl:template match="pending_xref">
        <a href="#{@reftarget}" class="{@reftype}-link">
            <xsl:apply-templates/>
        </a>
    </xsl:template>

    <xsl:template match="literal">
        <code>
            <xsl:apply-templates/>
        </code>
    </xsl:template>

    <xsl:template match="block_quote">
        <quote>
            <xsl:apply-templates/>
        </quote>
    </xsl:template>

    <xsl:template match="seealso">
        <div class="seealso">
            <p>
                <span class="pointingfinger">
                    <span>see also: </span>
                    <xsl:text>&#9755; </xsl:text> 
                </span>
                <xsl:apply-templates/>
            </p>
        </div>
    </xsl:template>

    <xsl:template match="seealso/paragraph">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="literal_block">
        <pre>
            <xsl:apply-templates/>
        </pre>
    </xsl:template>

    <xsl:template match="desc">
        <div  class="{@desctype}-description">
            <dl>
                <xsl:apply-templates/>
            </dl>
        </div>
    </xsl:template>

    <xsl:template match="desc_signature">
        <a name="{@ids}">
        <dt>
            <div class="function-classname">
                <xsl:value-of select="desc_classname"/>
            </div>
            <div class="function-name">
                <xsl:value-of select="desc_name"/>
            </div>
            <div class="function-arguments">
                <xsl:text>(</xsl:text>
                <xsl:for-each select="desc_parameterlist//desc_parameter">
                    <xsl:if test="name(..) = 'desc_optional'">
                        <xsl:text>[</xsl:text>
                    </xsl:if>
                    <span class="function-argument">
                        <xsl:value-of select="."/>
                    </span>
                    <xsl:if test="name(..) = 'desc_optional'">
                        <xsl:text>]</xsl:text>
                    </xsl:if>

                    <xsl:if test="position()!=last()">
                        <xsl:text>, </xsl:text>
                    </xsl:if>
                </xsl:for-each>
                <xsl:text>)</xsl:text>
            </div>
            <br clear="both"/>
        </dt>
        </a>
    </xsl:template>

    <xsl:template match="desc_content">
        <dd>
            <xsl:apply-templates/>
        </dd>
    </xsl:template>

    <xsl:template match="definition_list">
        <div class="definition-list">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="definition_list_item">
        <dl>
            <xsl:apply-templates/>
        </dl>
    </xsl:template>

    <xsl:template match="term">
        <dt>
            <xsl:apply-templates/>
        </dt>
    </xsl:template>

    <xsl:template match="definition">
        <dd>
            <xsl:apply-templates/>
        </dd>
    </xsl:template>
    <!-- attributes -->

    <xsl:template match="@classes">
        <xsl:attribute name="class">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>

    <xsl:template match="text()">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="*">
        <xsl:message>
            <xsl:text>Unknown element: </xsl:text>
            <xsl:value-of select="."/>
        </xsl:message>
    </xsl:template>
</xsl:stylesheet>
