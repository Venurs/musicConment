# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusiccommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickname = scrapy.Field()
    commentId = scrapy.Field()
    userId = scrapy.Field()
    content = scrapy.Field()
    likedCount = scrapy.Field()
    time = scrapy.Field()


class UserItem(scrapy.Item):
    nickname = scrapy.Field()
    userId = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    gender = scrapy.Field()
    person_introduce = scrapy.Field()
    image = scrapy.Field()
