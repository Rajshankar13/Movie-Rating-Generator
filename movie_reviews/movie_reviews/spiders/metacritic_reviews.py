# -*- coding: utf-8 -*-
import scrapy


class MetacriticReviewsSpider(scrapy.Spider):
	name = "metacritic_reviews"

	def start_requests(self):
		url = 'http://www.metacritic.com/movie/avengers-infinity-war/user-reviews'
		yield scrapy.Request(url = url, callback = self.parse)

	def parse(self, response):
		reviews = response.selector.xpath("//div[@class='review_body']")

		for selector in reviews:
			yield {
				'content': selector.xpath("span/text()").extract(),
				'expanded_content': selector.xpath("span/span[@class='blurb blurb_expanded']/text()").extract()
			}

		next_page = response.selector.xpath("//span[@class='flipper next']/a/@href").extract_first()
		if next_page is not None:
			next_page_link = response.urljoin(next_page)
			yield scrapy.Request(url = next_page_link, callback = self.parse)		