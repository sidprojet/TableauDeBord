from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import Compose
from scrapy.loader.processors import Join
from scrapy.loader import ItemLoader


class NewspaperLoader(ItemLoader):
	"""
		This class is responsible for defining general processes to apply on
		scrapped informations.
	"""
	def clean_theme(rawdata):
		theme = str(rawdata).split('/')
		theme = theme[3]
		theme = theme.replace('-', ' ')
		return theme

	theme_in = Compose(clean_theme)
	default_output_processor = TakeFirst()
	author_out = Join(', ')
	body_out = Join(' ')