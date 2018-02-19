from modules.parentloader import NewspaperLoader
from scrapy.loader.processors import Compose


class NouvelObsLoader(NewspaperLoader):
    """
        This class inherits from NewspaperLoader and personalize the processes
        to apply on scrapped informations for articles from Nouvel Obs.
    """
    def clean_date(rawdata):
        date = rawdata[len(rawdata)-11:len(rawdata)-1]
        date = date.split('/')
        date[2], date[0] = date[0], date[2]
        date = '/'.join(date)
        return date

    def clean_title(rawdata):
        title = rawdata[0].replace(' - L\'Obs', '')
        title = title.replace(' - O', '')
        return title

    date_in = Compose(lambda v: v[0], clean_date)
    title_in = Compose(clean_title)