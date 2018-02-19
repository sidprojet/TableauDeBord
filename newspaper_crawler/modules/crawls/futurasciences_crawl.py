from ..spiders.futurasciences_spider import FuturaSciencesSpider
from modules.parentcrawl import CrawlSite
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class CrawlFuturaSciences(CrawlSite):
	"""
		This class inherits from CrawlSite and is responsible for executing
		the process of crawling Futura Sciences's articles.
	"""
	site = 'futura-sciences'
	rss_feeds = [
	'http://www.futura-sciences.com/rss/actualites.xml',
	'http://www.futura-sciences.com/rss/sante/actualites.xml',
	'http://www.futura-sciences.com/rss/high-tech/actualites.xml',
	'http://www.futura-sciences.com/rss/espace/actualites.xml',
	'http://www.futura-sciences.com/rss/environnement/actualites.xml',
	'http://www.futura-sciences.com/rss/maison/actualites.xml',
	'http://www.futura-sciences.com/rss/nature/actualites.xml',
	'http://www.futura-sciences.com/rss/terre/actualites.xml',
	'http://www.futura-sciences.com/rss/matiere/actualites.xml',
	'http://www.futura-sciences.com/rss/mathematiques/actualites.xml',
	]

	@classmethod
	def crawl_futurasciences(cls):
		"""
			Crawl Futura Sciences with articles which have not been crawled and when
			it's done, wait an hour and call itself.
		"""
		urls = cls.get_urls_to_crawl()
		if urls != []:
			runner = CrawlerRunner()
			runner.crawl(FuturaSciencesSpider, start_urls = urls)
		reactor.callLater(3600, cls.crawl_futurasciences)