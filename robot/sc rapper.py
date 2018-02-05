import scrapy
keyword = ["cannabis","marijuana"]
fetch_flag = False
class leMondeBot(scrapy.Spider):
    name = 'lemondebot'
    allowed_domains = ["www.lemonde.fr"]
    start_url = ["www.lemonde.fr"]

    def parse(self, response):
        title = response.xpath("//meta[@property='og:title']/@content")[0].extract()
        desc = response.xpath("//meta[@property='og:description']/@content")[0].extract()
        for word in keyword:
            if word in title or word in desc:
                fetch_flag = True
                break
            continue
        if fetch_flag:
            theHTML = response.body