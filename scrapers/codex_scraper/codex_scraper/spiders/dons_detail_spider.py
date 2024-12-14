import scrapy


class DonsDetailSpider(scrapy.Spider):
    name = "dons_detail_spider"
    start_urls = [
        # "https://www.aidedd.org/regles/personnalisation/dons/",
        # "https://www.aidedd.org/regles/sorts/",
        "https://www.aidedd.org/regles/liste-monstres/"
    ]

    def parse(self, response):
        # Extraire tous les liens des dons depuis la page principale
        links = response.xpath("//div[@class='liste']//a[@href]/@href").extract()

        for link in links:
            full_link = response.urljoin(link)
            yield scrapy.Request(url=full_link, callback=self.parse_don)

    def parse_don(self, response):
        # Extraire les informations du don depuis chaque page
        title = response.xpath("//h1/text()").get(default="No title").strip()
        prerequisites = (
            response.xpath("//div[contains(@class, 'prerequis')]/text()")
            .get(default="Aucun")
            .strip()
        )
        description = response.xpath("//div[contains(@class, 'description')]//text()").getall()
        description = " ".join([text.strip() for text in description if text.strip()])
        source = (
            response.xpath("//div[contains(@class, 'source')]/text()")
            .get(default="Non spécifié")
            .strip()
        )

        # Générer un dictionnaire avec les données
        yield {
            "title": title,
            "prerequisites": prerequisites,
            "description": description,
            "source": source,
            "url": response.url,
        }
