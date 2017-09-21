# *_*coding:utf-8 *_*

from scrapy.spider import  Spider
from scrapy.selector import Selector
from tutorial.items import DmozItem

class DmozSpider(Spider):
    '''
    首先，Scrapy为爬虫的 start_urls属性中的每个URL创建了一个 scrapy.http.Request 对象 ，并将爬虫的parse 方法指定为回调函数。
    然后，这些 Request被调度并执行，之后通过parse()方法返回scrapy.http.Response对象，并反馈给爬虫。
    '''
    name = "dmoz"
    allowed_domains = ['dmoztools.net']

    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Arts/Design/Fashion/Magazines_and_E-zines/Women/"
    ]

    def parse(self, response):
        selector = Selector(response)
        # sites = selector.xpath('//div[@class="title-and-desc"]')
        sites = selector.xpath('//div[@class="title-and-desc"]')
        items =[]
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/div/text()').extract()
            item['link'] = site.xpath('a/@href').extrat()
            item['desc'] = site.xpath('div/text()').extract()
            items.append(item)
        return items
