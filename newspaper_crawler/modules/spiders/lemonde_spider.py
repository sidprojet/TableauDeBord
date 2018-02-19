from modules.loaders.lemonde_loader import LeMondeLoader
from modules.parentspider import NewspaperSpider
from modules.items import NewspaperItem
from modules.database import Database


class LeMondeSpider(NewspaperSpider):
    """
        This class inherits from NewspaperSpider and personalize the extraction of
        information for articles from Le Monde.
    """
    name = "lemonde"

    def parse(self, response):
        """
            This method take a response in parameter and call the different
            processes involve in the scrapping task and then save the
            informations in a JSON file.
        """
        loader = LeMondeLoader(item=NewspaperItem(), selector=response)
        loader.add_value("newspaper", "Le Monde")
        loader.add_css("description", "p.txt3.description-article::text")
        if response.xpath("//time//text()").extract_first(default='') != '':
            loader.add_xpath("date", "//time//text()")
        loader.add_css("author", "a.auteur::text")
        loader.add_xpath("body", "//div[@itemprop='articleBody']/*[not(script)][not(img)][not(video)]//text()")
        item = self.load_item(loader, response)
        self.save('Le Monde', item)