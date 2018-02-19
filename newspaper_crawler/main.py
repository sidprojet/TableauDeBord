from modules.crawls.futurasciences_crawl import CrawlFuturaSciences
from modules.crawls.liberation_crawl import CrawlLiberation
from modules.crawls.nouvelobs_crawl import CrawlNouvelObs
from modules.crawls.lefigaro_crawl import CrawlLeFigaro
from modules.crawls.telerama_crawl import CrawlTelerama
from modules.crawls.lemonde_crawl import CrawlLeMonde
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


configure_logging()
runner = CrawlerRunner()
CrawlLeMonde.crawl_lemonde()
CrawlLeFigaro.crawl_lefigaro()
CrawlTelerama.crawl_telerama()
CrawlNouvelObs.crawl_nouvelobs()
CrawlLiberation.crawl_liberation()
CrawlFuturaSciences.crawl_futurasciences()
reactor.run()