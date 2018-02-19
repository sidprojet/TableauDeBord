from ..spiders.liberation_spider import LiberationSpider
from modules.parentcrawl import CrawlSite
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class CrawlLiberation(CrawlSite):
	"""
		This class inherits from CrawlSite and is responsible for executing
		the process of crawling Liberation's articles.
	"""
	site = 'liberation'
	rss_feeds = [
	'http://rss.liberation.fr/rss/latest/',
	'http://rss.liberation.fr/rss/58/',
	'http://rss.liberation.fr/rss/44/',
	'http://rss.liberation.fr/rss/60/',
	'http://rss.liberation.fr/rss/10/',
	'http://rss.liberation.fr/rss/11/',
	'http://rss.liberation.fr/rss/12/',
	'http://rss.liberation.fr/rss/14/',
	]

	@classmethod
	def crawl_liberation(cls):
		"""
			Crawl Liberation with articles which have not been crawled and
			when it's done, wait an hour and call itself.
		"""
		urls = cls.get_urls_to_crawl()
		if urls != []:
			runner = CrawlerRunner()
			runner.crawl(LiberationSpider, start_urls = urls)
		reactor.callLater(3600, cls.crawl_liberation)