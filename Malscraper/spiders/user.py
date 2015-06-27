from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Malscraper.items import UserItem

import os
import pandas as pd
import re
# get the number of files for the copy_count property
path, dirs, files = os.walk("logs/username").next()
file_count = len(files)

path = 'C:/Users/2015/Development/Malscraper/logs/info/Mangalist[0-35837].csv'
df = pd.read_csv(path)
df.link = df.link+"/stats"

class UsernameScraper(CrawlSpider):
  name = 'username'
  allowed_domains = ['myanimelist.net']
  start_urls = df.link[0:35837]
  pages = '//*[@id="content"]/table/tr/td[2]/div[2]'


  def goFoward(link):
    shows = re.findall('show=\d*',link)
    if len(shows) > 1:
      greater = int(re.sub('show=','',shows[1]))
      less = int(re.sub('show=','',shows[0]))
      if less > greater:
        return None
      else:
        return link
    else:
      return None

  rules = [
    Rule(LinkExtractor(
        allow=['show=\d*'],
        restrict_xpaths=pages,process_value=goFoward
        ),
        callback='parse_item',
        follow=True
        )
    ]

  copy_count = "Users"
  if file_count != 0:
    copy_count = copy_count + "(" + str(file_count) + ")"

  def parse_start_url(self, response):
    return self.parse_item(response)

  def parse_item(self, response):
    table = response.xpath('//*[@id="content"]/table/tr/td[2]/div[2]/table[2]/tr[position()>1]')
    item = UserItem()
    for row in table:
      item['username'] = row.xpath('td[2]/a/text()').extract()
      item['profile'] = 'http://myanimelist.net' + row.xpath('td[2]/a/@href').extract_first()
      yield item


