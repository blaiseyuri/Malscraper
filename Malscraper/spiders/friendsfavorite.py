from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Malscraper.items import FriendItem

import os
import pandas as pd

# get the number of files for the copy_count property
path, dirs, files = os.walk("logs/friend").next()
file_count = len(files)

path = 'C:/Users/2015/Development/Malscraper/logs/username/UniqueUsernames.csv'
df = pd.read_csv(path, index_col = 0)
df.link = df.profile+"/friends"

class FriendScraper(CrawlSpider):
  name = 'friend'
  allowed_domains = ['myanimelist.net']
  start_urls = df.link
  friendslist = '//*[@id="content"]/table/tr/td[2]/div[2]'


  def userFriends(link):
    return link+'/friends'

  rules = [
    Rule(LinkExtractor(
        allow=['/profile'],
        restrict_xpaths=friendslist,process_value=userFriends
        ),
        callback='parse_item',
        follow=True
        )
    ]

  copy_count = "Friends"
  if file_count != 0:
    copy_count = copy_count + "(" + str(file_count) + ")"

  def parse_start_url(self, response):
    return self.parse_item(response)

  def parse_item(self, response):
    friends =  response.xpath('//*[@class="friendBlock"]/div[2]/a/strong/text()').extract()
    favorites = response.xpath('//*[@id="content"]/table/tr/td[1]/div/table[2]/tr/td[2]/a[1]/text()').extract()
    item = FriendItem()
    item['friends'] = str(friends).replace("u","")
    item['favorites'] = str(favorites).replace("u","")
    item['profile'] = response.url
    item['username'] = response.url.replace("http://myanimelist.net/profile/","").replace("/friends","")
    yield item
