import scrapy


class ClercSpider(scrapy.Spider):
    name = "clerc_spider"
    start_urls = ["https://www.aidedd.org/regles/classes/clerc/"]

    def parse(self, response):
        # Extraire le titre de la page
        title = response.xpath("//h1/text()").get(default="No title").strip()

        # Extraire l'introduction
        introduction = response.xpath("//div[@class='content']/p[1]//text()").getall()
        introduction = " ".join([text.strip() for text in introduction])

        # Extraire les sections principales (H2, H3, H4) et leur contenu
        sections = response.xpath(
            "//div[@class='content']//h2 | "
            "//div[@class='content']//h3 | "
            "//div[@class='content']//h4"
        )
        section_data = []
        for section in sections:
            section_title = section.xpath(".//text()").get(default="").strip()
            section_content = section.xpath(
                "./following-sibling::p[1]//text() | ./following-sibling::ul[1]//li//text()"
            ).getall()
            if section_content:
                section_data.append(
                    {
                        "title": section_title,
                        "content": " ".join([content.strip() for content in section_content]),
                    }
                )

        # Extraire la table des données
        tables = response.xpath("//table")
        extracted_tables = []
        for table in tables:
            # Extraire les en-têtes
            headers = table.xpath(".//tr[1]/th")
            formatted_headers = [
                " ".join(header.xpath(".//text()").getall()).strip().lower() for header in headers
            ]

            # Extraire les lignes
            rows = []
            for row in table.xpath(".//tr[position()>1]"):  # Sauter la ligne des en-têtes
                cells = row.xpath(".//td")
                row_data = {}
                for i, cell in enumerate(cells):
                    key = formatted_headers[i] if i < len(formatted_headers) else f"col_{i}"
                    value = " ".join(cell.xpath(".//text()").getall()).strip()
                    row_data[key] = value
                rows.append(row_data)

            extracted_tables.append({"headers": formatted_headers, "rows": rows})

        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "tables": extracted_tables,
        }
