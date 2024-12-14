import scrapy


class MoineSpider(scrapy.Spider):
    name = "moine_spider"
    start_urls = ["https://www.aidedd.org/regles/classes/moine/"]

    def parse(self, response):
        # Extraire le titre
        title = response.xpath("//h1/text()").get(default="No title").strip()

        # Extraire l'introduction
        introduction = response.xpath("//div[@class='content']/p[1]//text()").getall()
        introduction = " ".join([text.strip() for text in introduction])

        # Extraire les sections (H3 et H4) avec leur contenu
        sections = response.xpath("//div[@class='content']//h3 | //div[@class='content']//h4")
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
        table = response.xpath("//table")

        # Extraire les en-têtes
        headers = table.xpath(".//tr[1]/th")
        formatted_headers = []
        for header in headers:
            # Nettoyage des en-têtes pour les rendre compatibles avec les clés JSON attendues
            text = header.xpath(".//text()").get()
            text = text.lower().replace("\n", " ").replace("  ", " ").strip()
            if (
                "<br>" in text
            ):  # Gestion des sauts de ligne dans les colonnes (comme "bonus de maîtrise")
                text = " ".join(text.split("<br>"))
            formatted_headers.append(text)

        # Extraction des lignes
        rows = []
        for row in table.xpath(".//tr[position() > 1]"):  # Sauter la ligne des en-têtes
            cells = row.xpath(".//td")
            row_data = {}
            for i, cell in enumerate(cells):
                key = formatted_headers[i]
                value = cell.xpath(".//text()").get().strip()
                row_data[key] = value
            rows.append(row_data)

        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "table": {
                "headers": formatted_headers,
                "rows": rows,
            },
        }
