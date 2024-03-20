# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BusinessItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    business_yelp_url = scrapy.Field()
    reviews = scrapy.Field()
