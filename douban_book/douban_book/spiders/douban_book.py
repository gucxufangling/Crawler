# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import DoubanBookItem

class BookspiderSpider(scrapy.Spider):
    name = "douban_book"

    allowed_domains = ["book.douban.com"]
    # start_urls = ['https://book.douban.com/tag/%E5%8E%86%E5%8F%B2']
    start_urls = ['https://book.douban.com/tag/?view=cloud']

    def __init__(self):
        self.base_url = 'https://book.douban.com'
        self.finish_tags = set()  # 记录已爬的微博ID
        self.scrawl_tags = set(self.start_urls)  # 记录待爬的微博ID


    def parse(self, response):
        seletor = Selector(response)
        all_tag = seletor.xpath('//table[@class="tagCol"]//@href').extract()
        for tag in all_tag:
            print u"开始爬取书的分类链接："
            print self.base_url + tag
            # tag_ = self.scrawl_tags.pop()
            self.finish_tags.add(tag)
            # self.scrawl_tags.add(self.base_url + str(tag))

            print "b"
            url_book = self.base_url + unicode(tag)
            yield  scrapy.Request(url=url_book, callback=self.parse1)



    def parse1(self, response):
        print "a"
        sel = Selector(response)
        book_list = sel.css('#subject_list > ul > li')
        for book in book_list:
            item = DoubanBookItem()
            try:
                # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
                item['book_name'] = book.xpath('div[@class="info"]/h2/a/text()').extract()[0].strip()
                item['book_star'] = book.xpath("div[@class='info']/div[2]/span[@class='rating_nums']/text()").extract()[
                    0].strip()
                item['book_pl'] = book.xpath("div[@class='info']/div[2]/span[@class='pl']/text()").extract()[0].strip()
                pub = book.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].strip().split('/')
                item['book_price'] = pub.pop()
                item['book_date'] = pub.pop()
                item['book_publish'] = pub.pop()
                item['book_author'] = '/'.join(pub)
                yield item
            except:
                pass
                #
        nextPage = sel.xpath('//div[@id="subject_list"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()[
            0].strip()
        if nextPage:
            next_url = 'https://book.douban.com' + nextPage
            yield scrapy.http.Request(next_url, callback=self.parse1)

    def parseTag(self, response):
        sel = scrapy.Selector(response)

        urls = sel.xpath(
            '//*[@id="subject_list"]//li[@class="subject-item"]//h2/a/@href').extract()
        for url in urls:
            print "crawl book link: ", url, ", id: ", url[32:-1]
            # url = https://book.douban.com/subject/3070863/
            subject_id = url[32:-1]
            # 先存在本地文件再逐步抓取书籍信息
            if self.books_number < 1000:
                f = open('bookid_list_' + bytes(self.txt_id) + '.txt', 'a')

                f.write(subject_id + "\n")
                self.books_number += 1
            else:
                self.txt_id += 1
                self.books_number = 0
        tagurl = sel.xpath(
            '//*[@id="subject_list"]/div[@class="paginator"]/span[@class="thispage"]/following-sibling::a[1]/@href').extract()
        if tagurl:
            print "crawl booktag link: ", self.baseurl + tagurl[0]
            yield scrapy.Request(self.baseurl + tagurl[0], callback=self.parseTag)