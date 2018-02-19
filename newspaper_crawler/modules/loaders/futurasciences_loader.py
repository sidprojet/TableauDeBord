from modules.parentloader import NewspaperLoader
from scrapy.loader.processors import Compose
from scrapy.loader.processors import Join


class FuturaSciencesLoader(NewspaperLoader):
    """
        This class inherits from NewspaperLoader and personalize the processes
        to apply on scrapped informations for articles from Futura Sciences.
    """
    def clean_date(rawdata):
        return rawdata[len(rawdata)-10:]

    def clean_body(rawdata):
        body = rawdata
        position = body.rfind('Lien externe ')
        if position == -1:
            position = body.rfind('Liens externes ')
        if position == -1:
            position = body.rfind('Vous avez aimé cet article ? N\'hésitez pas à le partager avec')
        if position != -1:
            body = body[0:position]
        position = body.rfind('( function () { var vs')
        position2 = body.rfind('s.parentNode.insertBefore(vs, s); })();')
        if (position != -1) and (position2 != -1):
            body = body[0:position] + body[position2+39:len(body)]
        return body

    date_in = Compose(lambda v: v[0], clean_date)
    body_out = Compose(Join(' '), clean_body)