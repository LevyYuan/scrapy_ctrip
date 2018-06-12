# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


# 组团游
class GroupItem(scrapy.Item):
    title = Field()
    type = Field()
    trans = Field()
    hotel = Field()
    date = Field()
    img = Field()
    seat = Field()
    discount = Field()
    price = Field()

# 自由行
class FreeItem(scrapy.Item):
    title = Field()
    type = Field()
    trans = Field()
    hotel = Field()
    date = Field()
    img = Field()
    seat = Field()
    discount = Field()
    price = Field()

# 门票
class TicketItem(scrapy.Item):
    title = Field()
    type = Field()
    trans = Field()
    date = Field()
    img = Field()
    seat = Field()
    discount = Field()
    price = Field()

# 一日游
class OnedayItem(scrapy.Item):
    title = Field()
    type = Field()
    trans = Field()
    hotel = Field()
    date = Field()
    img = Field()
    seat = Field()
    discount = Field()
    price = Field()

# 邮轮游
class CruiseItem(scrapy.Item):
    title = Field()
    type = Field()
    trans = Field()
    hotel = Field()
    date = Field()
    img = Field()
    seat = Field()
    discount = Field()
    price = Field()
