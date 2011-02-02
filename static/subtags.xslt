<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="tag-listing">
	<html>
		<head>
		</head>
		<body>
			<h1>
			<xsl:for-each select="tags/tag">
				<xsl:value-of select="name" /> /
			</xsl:for-each>
			(<xsl:value-of select="bookmark-count" />)
			</h1>
			
			<ul>
			<xsl:for-each select="subtags/tag">
				<li>
					<a>
						<xsl:attribute name="href"><xsl:value-of select="tags-url" /></xsl:attribute>
						<xsl:value-of select="name" />
					</a>
					(<a>
						<xsl:attribute name="href"><xsl:value-of select="bookmarks-url" /></xsl:attribute>
						<xsl:value-of select="bookmark-count" />
					</a>)
				</li>
			</xsl:for-each>
			</ul>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>
