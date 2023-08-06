# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field


class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    responseUrl = Field()
    statusCode = Field()
    success = Field()
    exception = Field()
    encoding = Field()
    attrs = Field()


class MenuResponseItem(RawResponseItem):
    playgroundId = Field()
    groupCategoryName = Field()
    groupName = Field()
    groupUrl = Field()


class ProductResponseItem(RawResponseItem):
    playgroundId = Field()
    productUrl = Field()
    groupId = Field()
    price = Field()


class ProductDetailsResponseItem(RawResponseItem):
    playgroundId = Field()
    productUrl = Field()
    groupId = Field()
    imageUrl = Field()
    name = Field()
    description = Field()
    details = Field()


class ReviewResponseItem(RawResponseItem):
    technoBlogId = Field()
    reviewUrl = Field()
    name = Field()
    imageUrl = Field()


class ReviewDetailsResponseItem(RawResponseItem):
    technoBlogId = Field()
    reviewUrl = Field()
    createDate = Field()
    author = Field()
    name = Field()
    description = Field()
    pros = Field()
    cons = Field()
    productName = Field()
    productParameters = Field()
    verdict = Field()
    baseParameters = Field()
    keywords = Field()
    category = Field()
