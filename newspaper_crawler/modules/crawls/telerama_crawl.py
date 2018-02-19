from ..spiders.telerama_spider import TeleramaSpider
from modules.parentcrawl import CrawlSite
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class CrawlTelerama(CrawlSite):
	"""
		This class inherits from CrawlSite and is responsible for executing
		the process of crawling Telerama's articles.
	"""
	site = 'telerama'
	rss_feeds = [
	'http://www.telerama.fr/rss/une.xml',
	'http://www.telerama.fr/rss/medias.xml',
	'http://www.telerama.fr/rss/television.xml',
	'http://www.telerama.fr/rss/radio.xml',
	'http://www.telerama.fr/rss/cinema.xml',
	'http://www.telerama.fr/rss/series-tv.xml',
	'http://www.telerama.fr/rss/musique.xml',
	'http://www.telerama.fr/rss/livre.xml',
	'http://www.telerama.fr/rss/scenes.xml',
	'http://www.telerama.fr/rss/services/cinema.xml',
	'http://www.telerama.fr/rss/services/disque.xml',
	'http://www.telerama.fr/rss/services/livre.xml',
	'http://www.telerama.fr/rss/services/art.xml',
	]

	@classmethod
	def crawl_telerama(cls):
		"""
			Crawl Telerama with articles which have not been crawled and when
			it's done, wait an hour and call itself.
		"""
		urls = cls.get_urls_to_crawl()
		if urls != []:
			runner = CrawlerRunner()
			runner.crawl(TeleramaSpider, start_urls = urls)
		reactor.callLater(3600, cls.crawl_telerama)