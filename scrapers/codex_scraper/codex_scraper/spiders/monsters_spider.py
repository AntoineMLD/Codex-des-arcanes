import scrapy


class MonstresSpider(scrapy.Spider):
    name = "monstres_spider"
    start_urls = ["https://www.aidedd.org/dnd-filters/monstres.php"]

    def parse(self, response):
        # Extraire les liens vers les monstres
        for monstre in response.css('a[href*="monstres.php?vf="]'):
            page_url = response.urljoin(monstre.attrib["href"])
            yield scrapy.Request(page_url, callback=self.parse_monstre)

    def parse_monstre(self, response):
        # Extraire les informations générales
        title = response.css("h1::text").get()
        prerequisites = response.css(".type::text").get()
        description = (
            response.css(".description").xpath("string(.)").get(default="Non spécifié").strip()
        )
        source = response.css(".source::text").get()
        image_url = response.css(".picture img::attr(src)").get()
        url = response.url

        # Extraire les statistiques, traits spéciaux, actions et réactions
        stats = self.extract_stats(response)
        skills = self.extract_skills(response)
        actions = self.extract_section(response, "Actions")
        reactions = self.extract_section(response, "Réactions")

        yield {
            "title": title.strip() if title else "Inconnu",
            "prerequisites": prerequisites.strip() if prerequisites else "Aucun",
            "description": description.strip() if description else "",
            "source": source.strip() if source else "Inconnu",
            "image_url": response.urljoin(image_url) if image_url else None,
            "url": url,
            "stats": stats,
            "skills": skills,
            "actions": actions,
            "reactions": reactions,
        }

    def extract_stats(self, response):
        """
        Extract the stats block of the monster.
        """
        stats_block = response.css(".red").get()
        if stats_block:
            stats_lines = scrapy.Selector(text=stats_block).xpath("//text()").getall()
            return [line.strip() for line in stats_lines if line.strip()]
        return []

    def extract_skills(self, response):
        """
        Extract skills or special traits of the monster.
        """
        skills = []
        # Localiser les traits spéciaux avant "Actions" ou "Réactions"
        skills_section = response.xpath(
            '//div[@class="red"]/following-sibling::p['
            'preceding-sibling::div[@class="rub" and contains(text(), "Actions")]'
            "]"
        )

        for skill in skills_section:
            skill_text = skill.xpath("string(.)").get()
            if skill_text:
                skills.append(skill_text.strip())
        return skills

    def extract_section(self, response, section_title):
        """
        Extract content of a specific section (e.g., Actions, Réactions).
        """
        section_content = []
        # Localiser les sections par leur titre
        section = response.xpath(
            f'//div[@class="rub" and contains(text(), "{section_title}")]/'
            'following-sibling::*[not(@class="rub") and not(self::div[@class="orange"])]'
        )

        for node in section:
            # Extraire et nettoyer le texte
            text = node.xpath("string(.)").get()
            if text:
                section_content.append(text.strip())

        return section_content
