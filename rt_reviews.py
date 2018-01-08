# -*- coding: utf-8 -*-
import scrapy


class RtReviewsSpider(scrapy.Spider):
    name = 'rt_reviews'
    allowed_domains = ['https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/?page=1']
    start_urls = ['http://https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/?page=1/']

    def parse(self, response):
        pass
