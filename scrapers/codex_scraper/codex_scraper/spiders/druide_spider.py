import scrapy


class DruideSpider(scrapy.Spider):
    name = "druide_spider"
    start_urls = ["https://www.aidedd.org/regles/classes/druide/"]

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
                section_data.append(
                    {"title": section_title.strip(), "content": section_content}
                )

        # Extraire les tables spécifiques aux cercles
        tables = response.xpath("//table[caption]")
        circle_data = []

        for table in tables:
            # Extraire le titre (caption) du tableau
            caption = table.xpath(".//caption/text()").get(default="").strip()

            # Extraire les en-têtes
            headers = table.xpath(".//tr[1]//th//text()").getall()
            headers = [header.strip() for header in headers if header.strip()]

            # Extraire les données des lignes
            rows = []
            for row in table.xpath(".//tr[position()>1]"):
                cells = row.xpath(".//td")
                row_data = {}
                for idx, cell in enumerate(cells):
                    key = headers[idx] if idx < len(headers) else f"col_{idx+1}"
                    value = cell.xpath(".//text()").get(default="").strip()
                    row_data[key] = value
                rows.append(row_data)

            # Ajouter le tableau extrait
            circle_data.append(
                {
                    "circle_name": caption,
                    "headers": headers,
                    "rows": rows,
                }
            )

        # Générer les données au format JSON
        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "circle_tables": circle_data,
        }
