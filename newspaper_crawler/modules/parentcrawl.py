import feedparser


class CrawlSite():
	"""
		This class is responsible for defining common tasks in the process of
		crawling regarldess the site which is crawled.
	"""
	@classmethod
	def get_urls_to_crawl(cls):
		"""
			Return a list of urls from articles which have not been crawled
			yet, and record their urls in a text file.
		"""
		urls = []
		for rss_feed in cls.rss_feeds:
			parsed_rss_feed = feedparser.parse(rss_feed)
			for post in parsed_rss_feed.entries:
				url = post.link
				if url.split('.')[1] == cls.site:
					with open('urls_met.txt', 'r') as f:
						urls_met = f.read().split('\n')
					if url not in urls_met:
						entry = "\n%s" % url
						with open('urls_met.txt', 'a', encoding='utf-8') as f:
							f.write(entry)
						urls.append(url)
		return urls