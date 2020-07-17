# Author: Pablo Cortez
# Date: 07/17/2020
# The purpose of this program is to scrape data from glassesshop.com, specifically from
# the best sellers page. It will collect the product name, image url, product url, and
# the price. This program will start at the first page of the "best sellers" and continue
#  to the last page. An expample of scraped data can be found in data.csv. 
# -*- coding: utf-8 -*-
import scrapy


class GlassesspSpider(scrapy.Spider):
    name = 'glassesSP'
    allowed_domains = ['www.glassesshop.com']
    #start_urls = ['http://www.glassesshop.com/bestsellers/']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})

    def parse(self, response):
        # Iterate through each product on the page
        for product in response.xpath("//div[@id='product-lists']/div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row']"):
            yield{
                'product_name': product.xpath(".//div[@class='p-title']/a/@title").get(),
                'image_url': product.xpath(".//img[@class='lazy d-block w-100 product-img-default']/@src").get(),
                'url': product.xpath(".//div[@class='product-img-outer']/a[1]/@href").get(),
                'price': product.xpath(".//div[@class='p-price']/div/span/text()").get()
            }

        next_page = response.xpath("//li[@class='page-item col-6 p-0']/a[@class='page-link']/@href").get()
        

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
