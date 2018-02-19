from modules.loaders.futurasciences_loader import FuturaSciencesLoader
from modules.parentspider import NewspaperSpider
from modules.items import NewspaperItem
from modules.database import Database


class FuturaSciencesSpider(NewspaperSpider):
    """
        This class inherits from NewspaperSpider and personalize the extraction of
        information for articles from Futura Sciences.
    """
    name = "futurasciences"

    def parse(self, response):
        """
            This method take a response in parameter and call the different
            processes involve in the scrapping task and then save the
            informations in a JSON file.
        """
        loader = FuturaSciencesLoader(item=NewspaperItem(), selector=response)
        loader.add_value("newspaper", "Futura Sciences")
        loader.add_xpath("description", "//p[@class='delta py0p5']//text()")
        if response.xpath("//time//text()").extract_first(default='') != '':
            loader.add_xpath("date", "//time//text()")
        loader.add_xpath("author", "//h3[@itemprop='author']//text()")
        loader.add_xpath("body", "//section[@class='module article-text article-text-classic bg-white']/*[not(script)][not(img)][not(video)]//text()")
        item = self.load_item(loader, response)
        self.save('Futura Sciences', item)