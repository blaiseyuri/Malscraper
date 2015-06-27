# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MangaItem(Item):
    # define the fields for your item here like:
    name = Field()
    link = Field()
    location = Field()

class InfoItem(Item):
    name = Field()
    link = Field()
    
    # Information
    Type = Field()
    Volumes = Field()
    Chapters =Field()
    Status = Field()
    Published =Field()
    Genres = Field()
    Authors = Field()
    Serialization = Field()

    # Statistics
    Score =Field()
    Ranked = Field()
    Popularity = Field()
    Members = Field()
    Favorites = Field()

class UserItem(Item):
  username = Field()
  profile = Field()

class FriendItem(Item):
  username = Field()
  profile = Field()
  friends = Field()
  favorites = Field()