import scrapy


class ObjetsMagiquesSpider(scrapy.Spider):
    name = "objets_magiques_spider"
    start_urls = ["https://www.aidedd.org/regles/liste-objets-magiques/"]

    def parse(self, response):
        # Extraire tous les liens des objets magiques
        objets_links = response.xpath('//div[@class="liste"]//a/@href').getall()

        for lien in objets_links:
            absolute_url = response.urljoin(lien)
            yield scrapy.Request(url=absolute_url, callback=self.parse_objet)

    def parse_objet(self, response):
        # Titre de l'objet
        titre = response.xpath("//h1/text()").get()

        # Traduction anglaise si disponible
        traduction = response.xpath('//div[@class="trad"]/a/text()').get()

        # Type et rareté
        type_rarete = response.xpath('//div[@class="type"]/text()').get()

        # Description complète
        description = response.xpath('//div[@class="description"]//text()').getall()
        description = " ".join(description).strip()

        # Source
        source = response.xpath('//div[@class="source"]/text()').get()

        # Image
        image_url = response.xpath('//div[@class="picture"]//img/@src').get()
        if image_url:
            image_url = response.urljoin(image_url)

        yield {
            "titre": titre.strip() if titre else "Inconnu",
            "traduction": traduction.strip() if traduction else "Non spécifié",
            "type_rarete": type_rarete.strip() if type_rarete else "Non spécifié",
            "description": description,
            "source": source.strip() if source else "Non spécifié",
            "image_url": image_url,
            "url": response.url,
        }
