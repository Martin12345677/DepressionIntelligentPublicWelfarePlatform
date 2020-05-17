# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    intro = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    opentype = scrapy.Field()
    author = scrapy.Field()
    typeBook  = scrapy.Field()
    price = scrapy.Field()
    language = scrapy.Field()
    ISBN = scrapy.Field()
    press = scrapy.Field()
    time = scrapy.Field()
    englishName = scrapy.Field()
    pass

class PeopleItem(scrapy.Item):
    intro = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    opentype = scrapy.Field()
    englishName = scrapy.Field()
    from_ = scrapy.Field()
    birthplace = scrapy.Field()
    nation = scrapy.Field()
    occupation = scrapy.Field()
    pass

class GainianItem(scrapy.Item):
    intro = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    opentype = scrapy.Field()
    englishName = scrapy.Field()
    definition = scrapy.Field()
    explanation = scrapy.Field()
    extend = scrapy.Field()
    pass

class BaiduquestionItem(scrapy.Item):
    question = scrapy.Field()
    people = scrapy.Field()
    answer = scrapy.Field()
    url = scrapy.Field()
    pass