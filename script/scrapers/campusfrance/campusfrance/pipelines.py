# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.exporter import CsvItemExporter


class CampusfrancePipeline(object):
    def open_spider(self, spider):
        self.file = open("campusfrance_domaine.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
