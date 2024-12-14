import scrapy


class PaladinSpiderSpider(scrapy.Spider):
    name = "paladin_spider"
    allowed_domains = ["aidedd.org"]
    start_urls = ["https://www.aidedd.org/regles/classes/paladin/"]

    def parse(self, response):
        # Extraire le titre
        title = response.xpath("//h1/text()").get(default="No title").strip()

        # Extraire l'introduction
        introduction = response.xpath("//div[@class='content']/p[1]//text()").getall()
        introduction = " ".join([text.strip() for text in introduction])

        # Extraire les sections (H3 et H4) avec leur contenu
        sections = response.xpath(
            "//div[@class='content']//h3 | //div[@class='content']//h4"
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
                        "content": " ".join(
                            [content.strip() for content in section_content]
                        ),
                    }
                )

        # Extraire les tableaux
        tables = []
        for table in response.xpath("//table"):
            # Extraire les en-têtes de colonnes
            headers = table.xpath(".//tr[3]//th/text()").getall()
            headers = [
                header.strip() for header in headers if header.strip()
            ]  # Nettoyer les en-têtes

            # Extraire les lignes de données
            rows = []
            for row in table.xpath(".//tr[position() > 3]"):
                cells = row.xpath(".//td/text()").getall()
                cells = [cell.strip() for cell in cells]  # Nettoyer les cellules
                if cells:  # Ignorer les lignes vides
                    # Transformer chaque ligne en dictionnaire basé sur les headers
                    row_dict = {
                        headers[i]: cells[i] if i < len(cells) else ""
                        for i in range(len(headers))
                    }
                    rows.append(row_dict)

            # Ajouter les données structurées
            if headers and rows:
                tables.append({"name": "Progression du paladin", "data": rows})

            # Extraire les images
            images = response.xpath("//div[@class='content']//img/@src").getall()
            images = [response.urljoin(img) for img in images]

            # Extraire les liens
            links = response.xpath("//div[@class='content']//a/@href").getall()
            links = [response.urljoin(link) for link in links if link.startswith("/")]

        # Passer les données au pipeline
        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "tables": tables,
            "images": images,
            "links": links,
        }
