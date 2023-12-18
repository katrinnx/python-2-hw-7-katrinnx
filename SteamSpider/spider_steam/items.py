# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderSteamItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    num_of_reviews = scrapy.Field()
    total_grade = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    available_platforms = scrapy.Field()