# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonBooksItem(scrapy.Item):
    book_title = scrapy.Field()
    book_author = scrapy.Field()
    book_price = scrapy.Field()
    book_rating = scrapy.Field()
    book_users_rating = scrapy.Field()
    book_date = scrapy.Field()

