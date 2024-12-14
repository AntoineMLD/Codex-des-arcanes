import scrapy


class BarbareSpider(scrapy.Spider):
    name = "barbare_spider"
    start_urls = ["https://www.aidedd.org/regles/classes/barbare/"]

    def parse(self, response):
        # Extraire les informations principales
        title = response.xpath("//h1/text()").get()
        introduction = response.xpath("//div[@class='content']/p[1]/text()").get()

        # Extraire les sous-sections
        sections = response.xpath("//div[@class='content']//h3 | //div[@class='content']//h4")
        section_data = []

        for section in sections:
            section_title = section.xpath(".//text()").get()
            section_content = section.xpath(
                "./following-sibling::p[1]//text() | ./following-sibling::ul[1]//li//text()"
            ).getall()
            if section_content:
                section_data.append(
                    {
                        "title": section_title.strip() if section_title else "",
                        "content": " ".join(section_content).strip(),
                    }
                )

        # Extraire la table des capacités de classe
        table_rows = response.xpath("//table//tr")
        class_abilities = []

        for row in table_rows[1:]:
            columns = row.xpath(".//td")
            if len(columns) == 5:
                class_abilities.append(
                    {
                        "level": columns[0].xpath("text()").get().strip(),
                        "proficiency_bonus": columns[1].xpath("text()").get().strip(),
                        "features": columns[2].xpath("text()").get().strip(),
                        "rages": columns[3].xpath("text()").get().strip(),
                        "rage_damage": columns[4].xpath("text()").get().strip(),
                    }
                )

        # Générer le JSON
        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "class_abilities": class_abilities,
        }
