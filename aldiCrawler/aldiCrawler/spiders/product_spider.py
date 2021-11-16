import re

import scrapy
from scrapy.selector import Selector
from ..items import AldicrawlerItem
class ProductSpider(scrapy.Spider):
    name = 'products'
    start_urls = [
        'https://www.aldi.com.au/'
    ]
    search = "Groceries"


    def parse(self, response):
        # Parse Main and extract categories links under Groceries.
        # These include the links inside the category pages too.
        # In case of aldi, source code of the main page holds information of grandchildren
        hxs = Selector(response)
        #urls = hxs.xpath('descendant::li[contains(.,"'+self.search+'")]/descendant::ul[@class="main-nav--level m-level-sub"]/li/div[@class = "main-nav-item--inner-wrapper"]/descendant::a[contains(@class,"main-nav--item--link")][1]/@href').extract()
        urls = hxs.xpath('descendant::li[contains(.,"'+self.search+'")]/descendant::a/@href').extract()
        for url in urls:
            self.log('Found category url: %s' % url)
            yield response.follow(url, callback=self.parseCategory)

    def parseCategory(self, response):

        # Creating a container to temp store the value
        items = AldicrawlerItem()
        # For each link, Parse the page and extract product details.'''
        hxs = Selector(response)

        # Extract the list of products
        product_details = hxs.xpath('//div[@class = "box m-text-image"]')

        # Check if there any products in the page
        if product_details:

            # Extract the required details about the product
            for product in product_details:
                title = product.xpath('descendant::div[@class = "box--description--header"]/text()').extract()

                # Preprocessing the data i.e removing unnecessary characters using regex
                regex = re.compile(r'[\n\r\t]')
                title = regex.sub("", ''.join(title))

                img_src = product.xpath('descendant::img/@src').extract_first()
                price_details = product.xpath('descendant::div[@class="box--price"]')
                quantity = price_details.xpath('child::span[@class = "box--amount"]/text()').extract_first()
                price = price_details.xpath('child::span[@class = "box--value"]/text()').extract_first()
                decimal = price_details.xpath('child::span[@class = "box--decimal"]/text()').extract_first()
                unit_price = price_details.xpath('child::span[@class = "box--baseprice"]/text()').extract_first()

                # Handling Null values by imputing with empty or a single value.
                if title:
                    items['Product_title'] = title
                else:
                    items['Product_title'] = ""
                if img_src:
                    items['Product_image'] = img_src
                else:
                    items['Product_image'] = ""
                if quantity:
                    items['PackSize'] = quantity
                else:
                    items['PackSize'] = "1 unit"
                if price and decimal:
                    items['Price'] = price + decimal
                elif price:
                    items['Price'] = price
                else:
                    items['Price'] = ""
                if unit_price:
                    items['Price_per_unit'] = unit_price
                else:
                    items['Price_per_unit'] = ""
                yield items