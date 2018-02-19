from ..spiders.lemonde_spider import LeMondeSpider
from modules.parentcrawl import CrawlSite
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class CrawlLeMonde(CrawlSite):
	"""
		This class inherits from CrawlSite and is responsible for executing
		the process of crawling Le Monde's articles.
	"""
	site = 'lemonde'
	rss_feeds = [
	'http://www.lemonde.fr/rss/une.xml',
	'http://www.lemonde.fr/international/rss_full.xml',
	'http://www.lemonde.fr/politique/rss_full.xml',
	'http://www.lemonde.fr/les-decodeurs/rss_full.xml',
	'http://www.lemonde.fr/societe/rss_full.xml',
	'http://www.lemonde.fr/m-actu/rss_full.xml',
	'http://www.lemonde.fr/football/rss_full.xml',
	'http://www.lemonde.fr/afrique/rss_full.xml',
	'http://www.lemonde.fr/ameriques/rss_full.xml',
	'http://www.lemonde.fr/argent/rss_full.xml',
	'http://www.lemonde.fr/asie-pacifique/rss_full.xml',
	'http://www.lemonde.fr/culture/rss_full.xml',
	'http://www.lemonde.fr/emploi/rss_full.xml',
	'http://www.lemonde.fr/europe/rss_full.xml',
	'http://www.lemonde.fr/idees/rss_full.xml',
	'http://www.lemonde.fr/jeux-video/rss_full.xml',
	'http://www.lemonde.fr/pixels/rss_full.xml',
	'http://www.lemonde.fr/planete/rss_full.xml'
	'http://www.lemonde.fr/proche-orient/rss_full.xml',
	'http://www.lemonde.fr/sante/rss_full.xml',
	'http://www.lemonde.fr/sciences/rss_full.xml',
	'http://www.lemonde.fr/sport/rss_full.xml',
	'http://www.lemonde.fr/m-styles/rss_full.xml',
	]

	@classmethod
	def crawl_lemonde(cls):
		"""
			Crawl Le Monde with articles which have not been crawled and when
			it's done, wait an hour and call itself.
		"""
		urls = cls.get_urls_to_crawl()
		if urls != []:
			runner = CrawlerRunner()
			runner.crawl(LeMondeSpider, start_urls = urls)
		reactor.callLater(3600, cls.crawl_lemonde)