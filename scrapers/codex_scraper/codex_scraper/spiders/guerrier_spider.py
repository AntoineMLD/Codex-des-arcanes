import scrapy


class GuerrierSpider(scrapy.Spider):
    name = "guerrier_spider"
    start_urls = ["https://www.aidedd.org/regles/classes/guerrier/"]

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

        # Extraire le tableau des capacités
        class_features = []
        rows = response.xpath("(//table)[1]//tr")
        for row in rows:
            cells = row.xpath(".//th|.//td")
            if len(cells) == 3:  # Vérifie que la ligne a exactement 3 colonnes
                class_features.append(
                    {
                        "Niv": cells[0].xpath("string()").get().strip(),
                        "Bonus de maîtrise": cells[1].xpath("string()").get().strip(),
                        "Capacités": cells[2].xpath("string()").get().strip(),
                    }
                )

        # Extraire le tableau des sorts
        spell_slots = []
        rows = response.xpath("(//table)[2]//tr")
        for row in rows:
            cells = row.xpath(".//th|.//td")
            if len(cells) >= 4:  # Vérifie que la ligne a au moins 4 colonnes
                spell_slots.append(
                    {
                        "Niv": (
                            cells[0].xpath("string()").get().strip() if len(cells) > 0 else None
                        ),
                        "Sorts mineurs connus": (
                            cells[1].xpath("string()").get().strip() if len(cells) > 1 else None
                        ),
                        "Sorts connus": (
                            cells[2].xpath("string()").get().strip() if len(cells) > 2 else None
                        ),
                        "1": (cells[3].xpath("string()").get().strip() if len(cells) > 3 else None),
                        "2": (cells[4].xpath("string()").get().strip() if len(cells) > 4 else None),
                        "3": (cells[5].xpath("string()").get().strip() if len(cells) > 5 else None),
                        "4": (cells[6].xpath("string()").get().strip() if len(cells) > 6 else None),
                    }
                )

        # Retourner les données extraites
        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "tables": {
                "class_features": class_features,
                "spell_slots": spell_slots,
            },
        }
