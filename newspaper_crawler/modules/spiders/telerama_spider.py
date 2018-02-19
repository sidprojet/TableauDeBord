from modules.loaders.telerama_loader import TeleramaLoader
from modules.parentspider import NewspaperSpider
from modules.items import NewspaperItem
from modules.database import Database


class TeleramaSpider(NewspaperSpider):
    """
        This class inherits from NewspaperSpider and personalize the extraction of
        information for articles from Telerama.
    """
    name = "telerama"

    def parse(self, response):
        """
            This method take a response in parameter and call the different
            processes involve in the scrapping task and then save the
            informations in a JSON file.
        """
        loader = TeleramaLoader(item=NewspaperItem(), selector=response)
        loader.add_value("newspaper", "Telerama")
        loader.add_xpath("description", "//div[@class='article--intro']//text()")
        if response.xpath("//span[@itemprop='datePublished']//text()").extract_first(default='') != '':
            loader.add_xpath("date", "//span[@itemprop='datePublished']//text()")
        loader.add_xpath("author", "//span[@class='author--name']//text()")
        loader.add_xpath("body", "//div[@class='article--wysiwyg wysiwyg']/*[not(script)][not(img)][not(video)]//text()")
        item = self.load_item(loader, response)
        self.save('Telerama', item)