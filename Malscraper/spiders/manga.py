from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Malscraper.items import MangaItem
import re
import os
# get the number of files for the copy_count property
path, dirs, files = os.walk("logs/Manga").next()
file_count = len(files)

class MangaSpider(CrawlSpider):
  name = 'Manga'
  allowed_domains = ['myanimelist.net']
  start_urls = ['http://myanimelist.net/manga.php?letter=.']
  pages = '//*[@id="content"]/div[2]/div[2]'
  header = '//*[@id="horiznav_nav"]/ul'
  rules = [
    Rule(LinkExtractor(
        allow=['/manga.php[?]letter=[?:\.|a-zA-Z]&show=\d*'],
        restrict_xpaths=pages),
        callback='parse_item',
        follow=True,
        ),
    Rule(LinkExtractor(
        allow=['[?]letter=[?:\.|a-zA-Z](?:(?!&))'],
        restrict_xpaths=header),
        callback='parse_item',
        follow=True,
        )
  ]
  copy_count = ""
  if file_count != 0:
    copy_count = "(" + str(file_count) + ")"

  def parse_item(self, response):
    manga_list = response.xpath('//*[@id="content"]/div[2]/table/tr[position()>1]/td[2]')
    for manga in manga_list:
      print manga
      item = MangaItem()
      item['name'] = manga.xpath('a[1]/strong/text()').extract_first()
      item['link'] = 'myanimelist.net'+manga.xpath('a[1]/@href').extract_first()
      item['location'] = response.url
      
      yield item