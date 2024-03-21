<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/PLAY">
        <html>
            <head>
                <title>
                    <xsl:value-of select="TITLE" />
                </title>
                <link rel="stylesheet" type="text/css" href="/static/play.css" />
            </head>
            <body class="play">
                <h1>
                    <xsl:value-of select="TITLE" />
                </h1>


                <xsl:for-each select="ACT">
                    <section class="act">
                        <h2>
                            <xsl:value-of select="TITLE" />
                        </h2>
                        <xsl:for-each select="SCENE">
                            <section>
                                <h3>
                                    <xsl:value-of select="TITLE" />
                                </h3>
                                <xsl:apply-templates />
                            </section>
                        </xsl:for-each>
                    </section>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="SPEECH">
        <div class="speech">
            <xsl:apply-templates />
        </div>
    </xsl:template>


    <xsl:template match="SPEAKER">
        <b>
            <xsl:value-of select="." />
        </b>
    </xsl:template>

    <xsl:template match="LINE">
        <p class="line">
            <xsl:apply-templates />
        </p>
    </xsl:template>

    <xsl:template match="STAGEDIR">
        <p class="stagedir">
            <xsl:apply-templates />
        </p>
    </xsl:template>
    <xsl:template match="LINE/STAGEDIR">
        <span class="stagedir">[<xsl:apply-templates />]</span>
    </xsl:template>

    <xsl:template match="SUBHEAD">
        <p class="subhead">
            <xsl:apply-templates />
        </p>
    </xsl:template>


</xsl:stylesheet>