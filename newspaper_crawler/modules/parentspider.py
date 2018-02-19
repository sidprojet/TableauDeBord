import scrapy
import json
from .database import Database
from datetime import datetime


class NewspaperSpider(scrapy.Spider):
    """
        This class is responsible for defining how to extract information from
        general newspaper pages and save this information.
    """
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def load_item(self, loader, response):
        """
            This method extract informations of an article from a response passed
            in parameter with a loader. Those informations are returned in an item
            thanks the loader.
        """
        loader.add_value("url", response.url)
        loader.add_value("title", response.css('title::text').extract_first())
        loader.add_value("theme", response.url)
        item = loader.load_item()
        return item
        
    def save(self, sitename, item):
        """
            This method save informations provided by an item in a json file
            located in a specified folder if conditions are respected.
        """
        if 'body' in item:
            if len(item['body']) > 2100:
                if 'date' not in item:
                    now = datetime.now()
                    item['date'] = '%s/%s/%s' % (now.day, now.month, now.year)
                id_article = Database.get_id()
                filename = '%s #%s.json' % (sitename, id_article)
                with open('pressarticles/%s/%s' % (self.name, filename), 'w', encoding='utf-8') as f:
                    json.dump(dict(item), f, indent=4)
                    self.log('Saved file %s' % filename)
                    fields = ['author', 'title', 'description', 'body']
                    for field in fields:
                        if field in item:
                            item[field] = item[field].replace(u'\xa0', u' ')
                        else:
                            item[field] = None
                    Database.insert(item['url'], self.name, item['author'], item['title'],
                        item['theme'], item['description'], item['date'], item['body'])