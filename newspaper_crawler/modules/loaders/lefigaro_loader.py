import re
from modules.parentloader import NewspaperLoader
from scrapy.loader.processors import Compose
from scrapy.loader.processors import Join


class LeFigaroLoader(NewspaperLoader):
    """
        This class inherits from NewspaperLoader and personalize the processes
        to apply on scrapped informations for articles from Le Figaro.
    """
    def clean_date(rawdata):
        date = re.sub('[^0-9/]', '', rawdata)
        date = date[0:len(date)-4]
        return date

    def clean_author(rawdata):
        return rawdata.replace('lefigaro.fr', '')

    date_in = Compose(lambda v: v[0], clean_date)
    author_out = Compose(Join(', '), clean_author)