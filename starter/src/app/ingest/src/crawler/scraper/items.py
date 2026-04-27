import scrapy
class MyScraperItem(scrapy.Item):
    url = scrapy.Field()
    filename = scrapy.Field()
    title = scrapy.Field()
