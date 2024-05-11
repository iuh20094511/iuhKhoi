# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
import json
# from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv

class MongoDBUnitopPipeline:
    def __init__(self):  
        self.client = pymongo.MongoClient('mongodb+srv://khoi2404:minhkhoi2404@unitop.pen6gvu.mongodb.net/')
        self.db = self.client['lawnet']
        pass
    
    def process_item(self, item, spider):
        collection =self.db['dbunitop']
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")
        pass

class JsonDBUnitopPipeline:
    def process_item(self, item, spider):
        self.file = open('jsondataunitop.json','a',encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        self.file.close
        return item

class CSVDBUnitopPipeline:
    '''
    Viết code để xuất ra file csv, thông tin item trên dòng
    mỗi thông tin cách nhau với dấu $
    Ví dụ: coursename$lecturer$intro$describe$courseUrl
    Sau đó, cài đặt cấu định để ưu tiên Pipline này đầu tiên
    '''
    def process_item(self, item, spider):
        with open('csvdataunitop.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='$')
            # Write header if the file is empty
            if file.tell() == 0:
                writer.writerow(item.keys())
            writer.writerow(item.values())
        return item