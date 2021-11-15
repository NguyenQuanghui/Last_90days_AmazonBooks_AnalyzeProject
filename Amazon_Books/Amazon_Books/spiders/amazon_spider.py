import scrapy
import os
from ..items import AmazonBooksItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    if os.path.exists("Amazon_Books\\last_90_days_books.csv"):
        os.remove("Amazon_Books\\last_90_days_books.csv")
    else:
        custom_settings = { 'FEEDS' : {'last_90_days_books.csv':{'format':'csv'}}}
        page_number = 2
        start_urls = [
            "https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250227011&dc&qid=1635075803&rnid=1250225011&ref=sr_pg_1"
            ]

        def parse(self, response):
            items = AmazonBooksItem()
            all_books = response.css(".sg-col-12-of-20 > .sg-col-inner")
            for book in all_books:
                book_title = book.css(".a-size-medium.a-color-base.a-text-normal").css("::text").extract()
                book_author = book.css(".a-color-secondary .a-row span.a-size-base+ .a-size-base , .a-color-secondary .a-size-base.a-link-normal").css("::text").extract()
                book_price = [''.join(book.css(".a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole").css("::text").extract())]
                book_rating = [rating.replace(' out of 5 stars','') for rating in book.css(".a-icon-alt::text").extract()]
                book_users_rating = book.css(".a-size-small .a-size-base").css("::text").extract()
                book_date =  book.css(".a-color-secondary.a-text-normal").css("::text").extract()

                items['book_title'] = book_title
                items['book_author'] = book_author
                items['book_price'] = book_price
                items['book_rating'] = book_rating
                items['book_users_rating'] = book_users_rating
                items['book_date'] = book_date

                yield items

            
            next_page  = "https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250227011&dc&page=" + str(AmazonSpiderSpider.page_number) + "&qid=1635075072&rnid=1250225011&ref=sr_pg_2"
            if AmazonSpiderSpider.page_number <= 75:
                AmazonSpiderSpider.page_number += 1
                yield response.follow(next_page,callback=self.parse)                