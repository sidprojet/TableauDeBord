import scrapy


class NewspaperItem(scrapy.Item):
    """
        This class define different fields that we want to store in each item.
    """
    url = scrapy.Field()
    newspaper = scrapy.Field()
    theme = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field() 
    author = scrapy.Field()
    body = scrapy.Field()