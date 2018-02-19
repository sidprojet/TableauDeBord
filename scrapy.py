import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "lemonde"
    start_urls = ['http://www.lemonde.fr/']
