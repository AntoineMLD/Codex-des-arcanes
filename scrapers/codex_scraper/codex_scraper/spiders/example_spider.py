import scrapy


class CreationPersoSpider(scrapy.Spider):
    name = "example_spider"
    start_urls = [
        "https://www.aidedd.org/regles/creation-de-perso",
        "https://www.aidedd.org/regles/creation-de-perso/suite",
        "https://www.aidedd.org/regles/races/",
        "https://www.aidedd.org/regles/races/elfe/",
        "https://www.aidedd.org/regles/races/halfelin/",
        "https://www.aidedd.org/regles/races/humain/",
        "https://www.aidedd.org/regles/races/nain/",
        "https://www.aidedd.org/regles/races/demi-elfe/",
        "https://www.aidedd.org/regles/races/demi-orc/",
        "https://www.aidedd.org/regles/races/drakeide/",
        "https://www.aidedd.org/regles/races/gnome/",
        "https://www.aidedd.org/regles/races/tieffelin/"
    ]

    def parse(self, response):
        self.logger.info(f"Parsing URL: {response.url}")

        title = response.css("h1::text").get()

        sections = []
        for section in response.css("div.content"):
            headers = section.css("h3::text").getall()
            paragraphs = section.css("p::text").getall()
            sections.append({"headers": headers, "paragraphs": paragraphs})

        special_boxes = response.css("p.encadre").getall()

        links = response.css("a::attr(href)").getall()
        internal_links = [link for link in links if link.startswith("/regles/")]

        table = []
        table_rows = response.css("table tr")
        if table_rows:
            for row in table_rows[1:]:
                cells = row.css("td::text").getall()
                if len(cells) >= 3:
                    table.append(
                        {
                            "points_experience": cells[0].strip(),
                            "niveau": cells[1].strip(),
                            "bonus_maitrise": cells[2].strip(),
                        }
                    )

        yield {
            "url": response.url,
            "title": title,
            "sections": sections,
            "special_boxes": special_boxes,
            "internal_links": internal_links,
            "table": table if table else None,
        }
