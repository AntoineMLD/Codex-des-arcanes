import scrapy


class HistoriqueSpider(scrapy.Spider):
    name = "historique_spider"
    start_urls = [
        "https://www.aidedd.org/regles/historiques/",
        "https://www.aidedd.org/regles/historiques/acolyte/",
        "https://www.aidedd.org/regles/historiques/artisan-de-guilde/",
        "https://www.aidedd.org/regles/historiques/artiste/",
        "https://www.aidedd.org/regles/historiques/charlatan/",
        "https://www.aidedd.org/regles/historiques/criminel/",
        "https://www.aidedd.org/regles/historiques/enfant-des-rues/",
        "https://www.aidedd.org/regles/historiques/ermite/",
        "https://www.aidedd.org/regles/historiques/heros-du-peuple/",
        "https://www.aidedd.org/regles/historiques/marin/",
        "https://www.aidedd.org/regles/historiques/noble/",
        "https://www.aidedd.org/regles/historiques/sage/",
        "https://www.aidedd.org/regles/historiques/sauvageon/",
        "https://www.aidedd.org/regles/historiques/soldat/",
        "https://www.aidedd.org/regles/equipement/",
        "https://www.aidedd.org/regles/equipement/armes/",
        "https://www.aidedd.org/regles/equipement/armures/",
        "https://www.aidedd.org/regles/equipement/materiel/",
        "https://www.aidedd.org/regles/equipement/outils/",
        "https://www.aidedd.org/regles/equipement/montures-et-marchandises/",
        "https://www.aidedd.org/regles/equipement/depenses/",
        "https://www.aidedd.org/regles/equipement/babioles/",
        "https://www.aidedd.org/regles/personnalisation/multiclassage/",
        "https://www.aidedd.org/regles/caracteristiques/",
        "https://www.aidedd.org/regles/aventure/",
        "https://www.aidedd.org/regles/combat/",
        "https://www.aidedd.org/regles/magie/",
        "https://www.aidedd.org/regles/rencontres/",
        "https://www.aidedd.org/regles/objets-magiques/",
        "https://www.aidedd.org/regles/objets-magiques/intelligents/",
        "https://www.aidedd.org/regles/objets-magiques/artefacts/",
        "https://www.aidedd.org/regles/objets-magiques/creation/",
        "https://www.aidedd.org/regles/pieges/",
        "https://www.aidedd.org/regles/temps-morts/",
        "https://www.aidedd.org/regles/objets/",
        "https://www.aidedd.org/regles/maladies/",
        "https://www.aidedd.org/regles/poisons/",
        "https://www.aidedd.org/regles/folie/",
        "https://www.aidedd.org/regles/pieges-xgte/",
        "https://www.aidedd.org/regles/comparses/",
    ]

    def parse(self, response):
        # Extraire le titre de la page
        title = response.xpath("//h1/text()").get(default="No title").strip()

        # Extraire l'introduction
        introduction = response.xpath("//div[@class='content']/p[1]//text()").getall()
        introduction = " ".join([text.strip() for text in introduction])

        # Extraire les sections principales (H2 et H3) et leur contenu
        sections = response.xpath("//div[@class='content']//h2 | //div[@class='content']//h3")
        section_data = []
        for section in sections:
            section_title = section.xpath(".//text()").get(default="").strip()
            section_content = section.xpath(
                "./following-sibling::p[1]//text() | ./following-sibling::ul[1]//li//text()"
            ).getall()
            section_content = " ".join([text.strip() for text in section_content])
            if section_title and section_content:
                section_data.append({"title": section_title, "content": section_content})

        # Extraire les tables de données
        tables = response.xpath("//table")
        table_data = []
        for table in tables:
            # Extraire les en-têtes
            headers = table.xpath(".//tr[1]/td | .//tr[1]/th").xpath("string()").getall()
            headers = [header.strip() for header in headers]

            # Extraire les lignes
            rows = []
            for row in table.xpath(".//tr[position()>1]"):
                cells = row.xpath(".//td").xpath("string()").getall()
                cells = [cell.strip() for cell in cells]
                row_data = dict(zip(headers, cells))
                rows.append(row_data)
            table_data.append({"headers": headers, "rows": rows})

        yield {
            "title": title,
            "introduction": introduction,
            "sections": section_data,
            "tables": table_data,
        }
