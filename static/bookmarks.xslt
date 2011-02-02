<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="bookmark-listing">
	<html>
		<head>
		</head>
		<body>
			<h1>
			<xsl:for-each select="tags/tag">
				<xsl:value-of select="name" /> /
			</xsl:for-each>
			</h1>
			
			<ul>
			<xsl:for-each select="bookmarks/bookmark">
				<li>
					<a>
						<xsl:attribute name="href"><xsl:value-of select="url" /></xsl:attribute>
						<xsl:value-of select="url" />
					</a>
				</li>
			</xsl:for-each>
			</ul>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>
