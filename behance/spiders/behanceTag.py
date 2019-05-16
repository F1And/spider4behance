#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 业务包：爬出behance作品集

import scrapy
from behance.item.tagItems import tagItem, authorItem, zcoolPictureItem
import constants as cs
import behance.common.selectUrl as sel
import json


class portfolioSpider(scrapy.Spider):
    name = "portfolio"
    allowed_domains = ["behance.net"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }
    save_portfolio_ids = set()

    def start_requests(self):
        for tag in cs.BEHANCE_SEARCH_TAG:
            for ordinal in range(1, 10):
                url = "https://www.behance.net/search?ordinal=%s&content=projects&sort=appreciations&time=all&schema_tags=%s&user_tags=%s"
                yield scrapy.Request(url=url % (ordinal, tag, tag), callback=self.parse, headers=self.headers)

    def parse(self, response):
        if "html" not in response.body:
            return
        html = json.loads(response.body)["html"]
        portfolio_urls = sel.get_urls(html)

        for idx in range(0, len(portfolio_urls)):
            portfolio_url = portfolio_urls[idx]
            portfolio_id = portfolio_url.split("/")[4]

            self.save_portfolio_ids.add(int(portfolio_id))
            yield scrapy.Request(url=portfolio_url, callback=self.picture_parse, headers=self.headers)
        pass

    def picture_parse(self, response):
        if "view" not in response.body:
            return
        data = json.loads(response.body)["view"]["project"]
        tag_words = json.loads(response.body)["view"]["site"]["meta"]
        tags = data["tags"]
        module = data["modules"]
        for i in range(0, len(tags)):
            item = tagItem()
            tag_name = tags[i]["title"]
            tag_id = tags[i]["id"]
            pic_url = module[i]["src"]
            tag_word = tag_words["keywords"]
            item["tag_name"] = tag_name
            item["tag_id"] = tag_id
            item["pic_url"] = pic_url
            item["tag_words"] = tag_word
            yield item


class authorSpider(scrapy.Spider):
    name = "author"
    allowed_domains = ["behance.net"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }

    per_page = 48

    def start_requests(self):
        for ordinal in range(0, 10):
            _ordinal = self.per_page * ordinal
            url = "https://www.behance.net/search?ordinal=%s&per_page=48&content=users&sort=appreciations&time=all&country=CN"
            yield scrapy.Request(url=url % _ordinal, callback=self.parse, headers=self.headers)

    def parse(self, response):
        if "html" not in response.body:
            return
        html = json.loads(response.body)["html"]
        author_names = sel.get_author_names(html)
        author_urls = sel.get_author_urls(html)

        for i in range(0, self.per_page):
            # item 一定要放循环中 不然数据库会出现大量重复数据
            item = authorItem()
            item["author_name"] = author_names[i]
            item["author_url"] = author_urls[i]
            yield item


class zcoolAuthorSpider(scrapy.Spider):
    name = "zcoolAuthor"
    allowed_domains = ["zcool.com.cn"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }


    def start_requests(self):
        for ordinal in range(1, 100):
            url = "https://www.zcool.com.cn/discover/1!0!0!0!0!!!!3!-1!%d"
            yield scrapy.Request(url=url % ordinal, callback=self.parse, headers=self.headers)

    def parse(self, response):
        per_page = 25
        if "html" not in response.body:
            return
        html = response.body
        author_urls =  sel.get_zcool_author_url(html)
        author_names = sel.get_zcool_author_name(html)

        for i in range(0, per_page):
            item = authorItem()
            item["author_name"] = author_names[i]
            item["author_url"] = author_urls[i]
            yield item

class zcoolPictureSpider(scrapy.Spider):
    name = "zcoolPicture"
    allowed_domains = ["zcool.com.cn"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        for ordinal in range(1, 100):
            url = "https://www.zcool.com.cn/discover/8!0!0!0!0!!!!2!-1!%d"
            yield scrapy.Request(url=url % ordinal, callback=self.parse, headers=self.headers)

    def parse(self, response):
        per_page = 25
        if "html" not in response.body:
            return
        html = response.body
        picture_urls = sel.get_zcool_picture_urls(html)

        for i in range(0, per_page):
            picture_url = picture_urls[i]
            yield scrapy.Request(url=picture_url, callback=self.picture_parse, headers=self.headers)

    def picture_parse(self, response):
        if "html" not in response.body:
            return
        html = response.body
        picture_urls = sel.get_zcool_picture_url(html)

        for picture_url in picture_urls:
            item = zcoolPictureItem()
            item["pic_url"] = picture_url.split('@')[0]
            yield item