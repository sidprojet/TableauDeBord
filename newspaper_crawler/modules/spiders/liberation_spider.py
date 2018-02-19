from modules.loaders.liberation_loader import LiberationLoader
from modules.parentspider import NewspaperSpider
from modules.items import NewspaperItem
from modules.database import Database


class LiberationSpider(NewspaperSpider):
    """
        This class inherits from NeswpaperSpider and personalize the extraction of
        information for articles from Liberation.
    """
    name = "liberation"

    def parse(self, response):
        """
            This method take a response in parameter and call the different
            processes involve in the scrapping task and then save the
            informations in a JSON file.
        """
        loader = LiberationLoader(item=NewspaperItem(), selector=response)
        loader.add_value("newspaper", "Liberation")
        loader.add_xpath("description", "//h2[@class='article-standfirst read-left-padding']//text()")
        if response.xpath("//time//@datetime").extract_first(default='') != '':
            loader.add_xpath("date", "//time//@datetime")
        loader.add_xpath("author", "//span[@class='author']//span//text()")
        loader.add_xpath("body", "//div[@class='article-body read-left-padding']/*[not(script)][not(img)][not(video)][not(span[@class='author']//a)]//text()")
        item = self.load_item(loader, response)
        self.save('Liberation', item)