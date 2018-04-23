# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from musicComment.items import MusiccommentItem
from musicComment.items import UserItem


class MusiccommentPipeline(object):
    def __init__(self):
        super().__init__()
        self.con = pymongo.MongoClient(host="47.93.0.208", port=27017)
        # self.musicConment = open("musicComment.txt", mode="w", encoding="utf8")
        # self.user = open("user.txt", mode="w", encoding="utf8")

    def close_spider(self, spider):
        self.con.close()
        # self.musicConment.close()
        # self.user.close()

    def process_item(self, item, spider):
        obj = dict(item)
        db = self.con.musicConment
        # string = json.dumps(obj, ensure_ascii=False)
        if isinstance(item, MusiccommentItem):
            # self.musicConment.write(string + "\n")
            db.conments.insert(obj)
        elif isinstance(item, UserItem):
            # self.user.write(string + "\n")
            db.user.insert(obj)
        return item
