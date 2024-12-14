import scrapy


class OccultisteSpider(scrapy.Spider):
    name = "occultiste_spider"
    start_urls = ["https://www.aidedd.org/regles/classes/occultiste/"]

    def parse(self, response):
        # Extraire le titre principal
        title = response.xpath("//h1/text()").get().strip()

        # Extraire le contenu introductif
        introduction = response.xpath(
            "//div[@class='content']/p[not(preceding-sibling::h2)]//text()"
        ).getall()
        introduction = " ".join([p.strip() for p in introduction if p.strip()])

        # Extraire les sections principales et leurs contenus
        sections = response.xpath(
            "//div[@class='content']//h2 | //div[@class='content']//h3 | //div[@class='content']//h4"
        )
        section_data = []

        for section in sections:
            section_title = section.xpath(".//text()").get()
            section_content = section.xpath(
                "./following-sibling::p[1]//text() | ./following-sibling::ul[1]//li//text()"
            ).getall()
            section_content = " ".join(
                [content.strip() for content in section_content if content.strip()]
            )
            if section_title and section_content:
                section_data.append({"title": section_title.strip(), "content": section_content})

        # Extraire le tableau
        tables = response.xpath("//table")
        table_data = []

        for table in tables:
            headers = table.xpath(".//tr[1]/th//text()").getall()
            headers = [header.strip() for header in headers]

            rows = []
            for row in table.xpath(".//tr[position() > 1]"):
                cells = row.xpath(".//td//text()").getall()
                cells = [cell.strip() for cell in cells]
                rows.append(dict(zip(headers, cells)))

            table_data.append({"headers": headers, "rows": rows})

        # Extraire les liens présents dans le contenu
        links = response.xpath("//div[@class='content']//a/@href").getall()
        links = [
            "https://www.aidedd.org" + link if link.startswith("/") else link for link in links
        ]

        # Extraire les images
        images = response.xpath("//div[@class='content']//img/@src").getall()
        images = ["https://www.aidedd.org" + img if img.startswith("/") else img for img in images]

        # Structurer les données
        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "tables": table_data,
            "images": images,
            "links": links,
        }
