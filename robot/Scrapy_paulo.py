
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 10:26:46 2018

@author: MacBookPro
"""

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor, IGNORED_EXTENSIONS


class MySpider(CrawlSpider):
    name = 'lemonde_bot'
    allowed_domains = ['lemonde.fr']
    start_urls = ['http://www.lemonde.fr/international/','http://www.lemonde.fr/politique/','http://www.lemonde.fr/societe/','http://www.lemonde.fr/economie/'
                  ,'http://www.lemonde.fr/culture/','http://www.lemonde.fr/idees/','http://www.lemonde.fr/planete/','http://www.lemonde.fr/sciences/']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('.*\/article\/[1900-2100]\/.*\/\.html', ), deny_extensions = IGNORED_EXTENSIONS.append('js')),process_links='canabilink'),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(), process_links='canabilink'),
    )
        
    def parse_item(self, response):
        self.logger.info('Hi, this is an article page! %s', response.url)
        item = scrapy.Item()
        item['title'] = response.xpath("//meta[@property='og:title']/@content")[0].extract()
        item['subtitle'] = response.xpath("//meta[@property='og:description']/@content")[0].extract()
        print('***************************************')
        print(item['title'])
        return item
    
    def canabilink(self, list_links):
        keywords=['cannabis','marijuana']
        _links = [x for x in list_links if any(y in str(x.url) for y in keywords) ]
        print(_links)
        return _links