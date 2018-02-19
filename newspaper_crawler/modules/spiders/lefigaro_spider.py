from modules.loaders.lefigaro_loader import LeFigaroLoader
from modules.parentspider import NewspaperSpider
from modules.items import NewspaperItem
from modules.database import Database


class LeFigaroSpider(NewspaperSpider):
    """
        This class inherits from NeswpaperSpider and personalize the extraction of
        information for articles from Le Figaro.
    """
    name = "lefigaro"

    def parse(self, response):
        """
            This method take a response in parameter and call the different
            processes involve in the scrapping task and then save the
            informations in a JSON file.
        """
        loader = LeFigaroLoader(item=NewspaperItem(), selector=response)
        loader.add_value("newspaper", "Le Figaro")
        loader.add_xpath("description", "//p[@itemprop='about']//text()")
        if response.xpath("//time//text()").extract_first(default='') != '':
            loader.add_xpath("date", "//time//text()")
        loader.add_xpath("author", "//a[@itemprop='name']//text()")
        loader.add_xpath("body", "//div[@itemprop='articleBody']/*[not(script)][not(img)][not(video)]//text()")
        item = self.load_item(loader, response)
        self.save('Le Figaro', item)