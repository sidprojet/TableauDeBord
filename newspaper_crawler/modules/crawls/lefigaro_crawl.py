from ..spiders.lefigaro_spider import LeFigaroSpider
from modules.parentcrawl import CrawlSite
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class CrawlLeFigaro(CrawlSite):
	"""
		This class inherits from CrawlSite and is responsible for executing
		the process of crawling Le Figaro's articles.
	"""
	site = 'lefigaro'
	rss_feeds = [
	'http://www.lefigaro.fr/rss/figaro_actualites-a-la-une.xml',
	'http://www.lefigaro.fr/rss/figaro_politique.xml',
	'http://www.lefigaro.fr/rss/figaro_international.xml',
	'http://www.lefigaro.fr/rss/figaro_actualite-france.xml',
	'http://www.lefigaro.fr/rss/figaro_sciences.xml',
	'http://www.lefigaro.fr/rss/figaro_sante.xml',
	'http://www.lefigaro.fr/rss/figaro_economie.xml',
	'http://www.lefigaro.fr/rss/figaro_societes.xml',
	'http://www.lefigaro.fr/rss/figaro_secteur_high-tech.xml',
	'http://www.lefigaro.fr/rss/figaro_immobilier.xml',
	'http://www.lefigaro.fr/rss/figaro_bourse.xml',
	'http://www.lefigaro.fr/rss/figaro_culture.xml',
	'http://www.lefigaro.fr/rss/figaro_cinema.xml',
	'http://www.lefigaro.fr/rss/figaro_musique.xml',
	'http://www.lefigaro.fr/rss/figaro_livres.xml',
	'http://www.lefigaro.fr/rss/figaro_lifestyle.xml',
	]

	@classmethod
	def crawl_lefigaro(cls):
		"""
			Crawl Le Figaro with articles which have not been crawled and when
			it's done, wait an hour and call itself.
		"""
		urls = cls.get_urls_to_crawl()
		if urls != []:
			runner = CrawlerRunner()
			runner.crawl(LeFigaroSpider, start_urls = urls)
		reactor.callLater(3600, cls.crawl_lefigaro)