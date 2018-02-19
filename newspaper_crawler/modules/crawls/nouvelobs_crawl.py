from ..spiders.nouvelobs_spider import NouvelObsSpider
from modules.parentcrawl import CrawlSite
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class CrawlNouvelObs(CrawlSite):
	"""
		This class inherits from CrawlSite and is responsible for executing
		the process of crawling Nouvel Obs's articles.
	"""
	site = 'nouvelobs'
	rss_feeds = [
	'http://tempsreel.nouvelobs.com/rss.xml',
	'http://tempsreel.nouvelobs.com/politique/rss.xml',
	'http://tempsreel.nouvelobs.com/societe/rss.xml',
	'http://tempsreel.nouvelobs.com/monde/rss.xml',
	'http://tempsreel.nouvelobs.com/economie/rss.xml',
	'http://tempsreel.nouvelobs.com/culture/rss.xml',
	'http://o.nouvelobs.com/high-tech/rss.xml',
	'http://tempsreel.nouvelobs.com/education/rss.xml',
	'http://tempsreel.nouvelobs.com/sport/rss.xml',
	'http://tempsreel.nouvelobs.com/rue89/rss.xml',
	'http://tempsreel.nouvelobs.com/rue89/rue89-nos-vies-connectees/rss.xml',
	'http://tempsreel.nouvelobs.com/rue89/rue89-sur-les-reseaux/rss.xml',
	'http://tempsreel.nouvelobs.com/rue89/sur-le-radar/rss.xml',
	]

	@classmethod
	def crawl_nouvelobs(cls):
		"""
			Crawl Nouvel Obs with articles which have not been crawled and when
			it's done, wait an hour and call itself.
		"""
		urls = cls.get_urls_to_crawl()
		if urls != []:
			runner = CrawlerRunner()
			runner.crawl(NouvelObsSpider, start_urls = urls)
		reactor.callLater(3600, cls.crawl_nouvelobs)