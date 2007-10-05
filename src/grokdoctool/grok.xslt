<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:date="http://exslt.org/dates-and-times"
    extension-element-prefixes="date" >
    <xsl:include href="rst2html.xslt"/>
    <xsl:output indent="yes" method="html"/>
    <xsl:template match="/document" priority="10">
        <html>
            <head>
            <xsl:comment>
                <xsl:text>Generated from</xsl:text>
                <xsl:value-of select="@source"/>
            </xsl:comment>
            <style type="text/css">

/* some default styles from grok layout */
body {
    font-family: verdana;
}

h1 {
    font-family: verdana;
    font-size: 15px;
    line-height: 20px;
    color: #CC9900;
    width: 100%;
    margin: 23px auto 8px auto;
    border-bottom: 1px solid #CC9900;
}
h2 {
    font-family: verdana;
    font-size: 13px;
    line-height: 20px;
    color: #CC9900;
    width: 100%;
    margin: 16px auto 8px auto;
    border-bottom: 1px dotted #cccccc;
}
h3 {
    font-family: verdana;
    font-size: 12px;
    line-height: 12px;
    color: #555555;
    width: 100%;
    margin: 16px auto -4px auto;
}
p {
    font-size: 13px;
    line-height: 20px;
    color: #555555;
    width: 540px;
    margin: 8px auto;
}

pre {
    font-size: 11px;
    line-height: 18px;
    color: #A90101;
    width: 540px;
    margin: 8px auto;
    padding: 16px 8px;
    border-top: 1px solid #cccccc;
    border-bottom: 1px solid #dddddd;
    background: #eeeeee;
}
ul {
    font-size: 11px;
    line-height: 20px;
    color: #555555;
    width: 540px;
    margin: 16px auto;
    list-style-type: none;
}
li {
    margin: 0 50px 0 0;
    left: 0;
    padding: 0;
}

a:link {
    color: #555555;
    text-decoration: none;
    border-bottom-style: dotted;
    border-bottom-width: 1px;
}

a:hover {
    color: #CC9900;
    border-bottom-style: dotted;
    background-color: #ffffff;
    border-width: 1px;
}

a:visited {
    color: #555555;
    text-decoration: none;
    border-bottom-style: dotted;
    border-bottom-width: 1px;
}

/* custom documentation styles */

span.pointing-finger {
    color:#55555;
}

span.pointing-finger span {
    font-size:10px;
}

.header h1 {
    font-size:20px;
    border:none;
}
.footer {
    border-top:1px dotted #ccccc;
}
.footer span {
    font-size:10px;
    font-style:italic;
    color:55555;
}
div.function-description{
    font-size:14px;
    margin-left:2em;
}

div.function-classname {
    float:left;
    font-weight:bold;
}
div.function-name {
    float:left;
    font-weight:bold;
}
div.function-argument {
    font-style:italic
}
div.function-arguments {
    float:left;
    width:30em;
}

            </style>
            <title><xsl:value-of select="title"/></title>
            </head>
            <body>
                <div class="header">
                    <h1>Grok reference documentation</h1>
                </div>
                <xsl:apply-templates/>
                <div class="footer">
                    <span>
        <xsl:text>Grok reference documentation, generated on </xsl:text>
        <xsl:value-of select="concat(date:day-name(), ' ', date:month-name(), ' ', date:day-in-month(), ' ', date:year(), ', ', date:time())"/>
                    </span>
                </div>
            </body>
        </html>
    </xsl:template>


</xsl:stylesheet>
