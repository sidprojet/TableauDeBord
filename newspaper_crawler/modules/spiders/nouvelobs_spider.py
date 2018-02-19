from modules.loaders.nouvelobs_loader import NouvelObsLoader
from modules.parentspider import NewspaperSpider
from modules.items import NewspaperItem
from modules.database import Database


class NouvelObsSpider(NewspaperSpider):
    """
        This class inherits from NewspaperSpider and personalize the extraction of
        information for articles from Nouvel Obs.
    """
    name = "nouvelobs"

    def parse(self, response):
        """
            This method take a response in parameter and call the different
            processes involve in the scrapping task and then save the
            informations in a JSON file.
        """
        loader = NouvelObsLoader(item=NewspaperItem(), selector=response)
        loader.add_value("newspaper", "Nouvel Obs")
        loader.add_xpath("description", "//h2[@itemprop='description']//text()")
        if response.xpath("//time//a//@href").extract_first(default='') != '':
            loader.add_xpath("date", "//time//a//@href")
        loader.add_xpath("author", "//span[@itemprop='name']//text()")
        loader.add_xpath("body", "//div[@id='js-article-body']/*[not(script)][not(img)][not(video)]//text()")
        item = self.load_item(loader, response)
        self.save('NouvelObs', item)