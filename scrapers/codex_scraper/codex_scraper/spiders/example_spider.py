import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example_spider'
    allowed_domains = ['aidedd.org']
    start_urls = ['https://www.aidedd.org']

    def parse(self, response):
        # Exemple : Extraire des titres
        for title in response.css('h1::text'):
            yield {'title': title.get()}
