# -*- coding: utf-8 -*-
import scrapy
from musicComment.items import MusiccommentItem
from musicComment.items import UserItem
import json
from jsonpath import jsonpath
import time
from scrapy_redis.spiders import RedisSpider


class FriendconmentSpider(RedisSpider):
    name = 'friendConment'
    allowed_domains = ['music.163.com']
    redis_key = "friendConment:start_url"

    # start_urls = ['http://music.163.com/api/v1/resource/comments/R_SO_4_437250607?limit=15&offset=15']
    url = "http://music.163.com/api/v1/resource/comments/R_SO_4_437250607?limit={}&offset={}"
    user_url = "http://music.163.com/api/playlist/detail?id={}"
    offset = 15
    limit = 15

    def parse(self, response):
        music_comment = MusiccommentItem()
        obj = json.loads(response.text)
        total = int(jsonpath(obj, '$.total')[0])
        hotComments = jsonpath(obj, "$.comments")[0]
        for hotComment in hotComments:
            music_comment['userId'] = jsonpath(hotComment, "$.user.userId")[0]
            music_comment['nickname'] = jsonpath(hotComment, "$.user.nickname")[0]
            music_comment['commentId'] = jsonpath(hotComment, "$.commentId")[0]
            music_comment['likedCount'] = jsonpath(hotComment, "$.likedCount")[0]
            music_comment['content'] = jsonpath(hotComment, "$.content")[0]
            timestamp = jsonpath(hotComment, "$.time")[0]
            dateArray = time.localtime(timestamp/1000)
            music_comment['time'] = time.strftime("%Y-%m-%d %H:%M:%S", dateArray)
            yield music_comment

            if self.offset <= total:
                self.offset = self.limit + self.offset
                page_url = self.url.format(self.limit, self.offset)
                yield scrapy.Request(url=page_url, callback=self.parse)
            user = UserItem()
            user['userId'] = music_comment['userId']
            yield scrapy.Request(url=self.user_url.format(music_comment['userId']), callback=self.parse_user, meta={'user': user})

    def parse_user(self, response):
        user = response.meta["user"]
        userJson = json.loads(response.text)
        userInfo = jsonpath(userJson, '$.result.creator')
        if userInfo:
            image = jsonpath(userInfo[0], "$.avatarUrl")
            nickname = jsonpath(userInfo[0], "$.nickname")
            province = jsonpath(userInfo[0], "$.province")
            city = jsonpath(userInfo[0], "$.city")
            gender = jsonpath(userInfo[0], "$.gender")
            signature = jsonpath(userInfo[0], "$.signature")
            if signature:
                user['person_introduce'] = signature[0]
            if gender:
                user['gender'] = gender[0]
            if city:
                user['city'] = city[0]
            if province:
                user['province'] = province[0]
            if nickname:
                user['nickname'] = nickname[0]
            if image:
                user['image'] = image[0]
            yield user
