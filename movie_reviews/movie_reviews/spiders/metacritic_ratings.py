# -*- coding: utf-8 -*-
import scrapy


class MetacriticRatingsSpider(scrapy.Spider):
	name = "metacritic_ratings"

	def start_requests(self):
		url = 'http://www.metacritic.com/movie/joker/user-reviews'
		yield scrapy.Request(url = url, callback = self.parse)

	def parse(self, response):
		ratings = response.selector.xpath("//div[@class='left fl']")

		for selector in ratings:
			yield {
				'rating': selector.xpath("div/text()").extract_first()
			}

		next_page = response.selector.xpath("//span[@class='flipper next']/a/@href").extract_first()
		if next_page is not None:
			next_page_link = response.urljoin(next_page)
			yield scrapy.Request(url = next_page_link, callback = self.parse)	