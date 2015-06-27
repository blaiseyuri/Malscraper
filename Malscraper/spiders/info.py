from scrapy.spiders import Spider
from Malscraper.items import InfoItem
# import re
import pandas as pd
import os
# get the number of files for the copy_count property
a = 0
n = 35837

listrange = '['+str(a)+'-'+str(n)+']'
name = "Mangalist"+listrange

path, dirs, files = os.walk("logs/info").next()
file_count = len([csv for csv in files if csv.find(name) != -1])

path = 'C:/Users/2015/Development/Malscraper/logs/Manga/Mangalist.csv'
df = pd.read_csv(path)
df.link = "http://"+df.link

class MangaInfoScraper(Spider):
  name = 'info'
  allowed_domains = ['animelist.net']
  
  
  start_urls = df.link.ix[a:n]
  copy_count = listrange
  
  if file_count != 0:
    copy_count = copy_count + "(" + str(file_count) + ")"
  
  def parse(self, response):
    information = response.xpath('//*[@id="content"]/table/tr/td[1]/div')
    item = InfoItem()
    itemdict = {
    'Type': 0,
    'Volumes': 0,
    'Chapters': 0,
    'Status': 0,
    'Published': 0,
    'Genres': 0,
    'Authors': 0,
    'Serialization': 0,

    # Statistics
    'Ranked': 0,
    'Popularity': 0,
    'Members': 0,
    'Favorites': 0

    }
    for key in itemdict:
      value = information.xpath('span[contains(text(),'"\""+key+"\""')]/../text()').extract()
      
      if len(value) > 1:
        infolist = information.xpath('span[contains(text(),'"\""+key+"\""')]/../a/text()').extract()
        item[key] = str(infolist).replace("u","")
      elif key == "Genres":
        infolist = information.xpath('span[contains(text(),'"\""+key+"\""')]/../a/text()').extract()
        item[key] = str(infolist).replace("u","")
      elif key == 'Serialization':
        item[key] = information.xpath('span[contains(text(),'"\""+key+"\""')]/../a/text()').extract()
        if len(item[key]) == 0:
          item[key] = value
      else:
        item[key] = value

    item['link'] = response.url
    item['name'] = response.xpath('//*[@id="contentWrapper"]/h1/text()').extract()
    item['Score'] = information.xpath('span[contains(text(),"Score")]/../text()').extract()
    yield item




# Type: Manga
# Volumes: Unknown
# Chapters: Unknown
# Status: Publishing
# Published: Apr 22, 2010 to ?
# Genres: Action, Adventure, Fantasy
# Authors: Tashiro, Tetsuya (Art), Takahiro (Story)
# Serialization: Gangan Joker

# Statistics
# Score: 8.461 (scored by 17309 users)
# Ranked: #1732
# Popularity: #40
# Members: 39,757
# Favorites: 4,071
