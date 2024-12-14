import scrapy


class EtatsSpider(scrapy.Spider):
    name = "etats_spider"
    start_urls = [  # "https://www.aidedd.org/regles/etats/",
        "https://www.aidedd.org/regles/objets-magiques/autres-recompenses/"
    ]

    def parse(self, response):
        # Extraire le titre principal
        title = response.xpath("//h1/text()").get()

        # Extraire les sections de la page (chaque état)
        etats = response.xpath("//h4")
        data = []

        for etat in etats:
            etat_name = etat.xpath("text()").get()
            description_items = etat.xpath("following-sibling::ul[1]/li/text()").getall()

            data.append(
                {
                    "etat": etat_name,
                    "description": description_items,
                }
            )

        # Inclure des informations supplémentaires
        exhaustion_section = response.xpath(
            "//p[contains(@class, 'encadre')]/strong[contains(text(), 'ÉPUISEMENT')]/.."
        ).get()

        yield {
            "title": title,
            "etats": data,
            "exhaustion": exhaustion_section,
        }
