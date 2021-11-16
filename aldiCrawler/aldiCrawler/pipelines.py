# -*- coding: utf-8 -*-
import csv
import itertools

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AldicrawlerPipeline(object):

    def __init__(self):
        self.csvwriter = csv.writer(open('items.csv', 'w'), delimiter=',')
        self.csvwriter.writerow(['Product Title', 'Product Image Source', 'Package Size', 'Price', 'Unit Price'])

    def process_item(self, item, spider):


        row = [item['Product_title'], item['Product_image'], item['PackSize'], item['Price'], item['Price_per_unit']]


        self.csvwriter.writerow(row)

        return item
