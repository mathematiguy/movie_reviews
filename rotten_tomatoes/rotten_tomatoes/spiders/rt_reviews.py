# -*- coding: utf-8 -*-
import scrapy


class RtReviewsSpider(scrapy.Spider):
	name = 'rt_reviews'
	allowed_domains = ['rottentomatoes.com']
	start_urls = ['https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/?page=1&type=user']

	def parse(self, response):
		# get the names for each reviewer
		names = response.xpath('//*[@id="reviews"]/div[3]/div/div[1]/div[3]/a/span/text()').extract()
		# get the text from each review
		reviews = ['\n\n'.join(response.xpath('//*[@id="reviews"]/div[3]/div[%d]/div[2]/div/text()' % (i + 1)).extract()).strip() for i in range(len(names))]
		# get the date for each review
		dates = [x for x in response.xpath('//*[@id="reviews"]/div[3]/div/div[2]/span/text()').extract() if x not in [' ', u'\xbd', u' \xbd']]
		# get the star count for each review
		star_counts = [len(response.xpath('//*[@id="reviews"]/div[3]/div[%d]/div[2]/span[1]/span' %(i + 1)).extract()) for i in range(len(names))]
		# get the half star count for each review
		half_counts = [x == u' \xbd' for x in ''.join(response.xpath('//*[@id="reviews"]/div[3]/div/div[2]/span/text()').extract()).split('December 24, 2017')]
		# calculate the star rating for each review
		star_ratings = [star_count + 0.5 * half_count if half_count else star_count for star_count, half_count in zip(star_counts, half_counts)]

		for name, review, date, star_rating in zip(names, reviews, dates, star_ratings):
			yield dict(name = name, review = review, date = date, star_rating = star_rating)

		page_links = response.xpath('//*[@id="reviews"]/div[4]/a[2]/@href').extract()
		if len(page_links) > 0:
			# get the link to the next page
			next_page = response.xpath('//*[@id="reviews"]/div[4]/a[2]/@href').extract()[0]
			# go to the next page
			yield scrapy.Request(response.urljoin(next_page), callback = self.parse)