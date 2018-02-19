import re
from modules.parentloader import NewspaperLoader
from scrapy.loader.processors import Compose


class LeMondeLoader(NewspaperLoader):
    """
        This class inherits from NewspaperLoader and personalize the processes
        to apply on scrapped informations for articles from Le Monde.
    """
    def clean_date(rawdata):
        date = re.sub('[^0-9.]', '', rawdata)
        date = date[0:len(date)-4]
        date = date.replace('.', '/')
        return date

    date_in = Compose(lambda v: v[0], clean_date)