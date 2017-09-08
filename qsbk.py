__author__ = 'CQC'
# -*- coding:utf-8 -*-
#爬取糗事百科的段子，此为最简单的爬虫，不需要登录信息

import codecs
import requests
from bs4 import BeautifulSoup

#糗事百科爬虫类
class QSBK:

    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        #初始化headers
        self.headers = { 'User-Agent' : self.user_agent }
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False
    #传入某一页的索引获得页面代码
    
    def getPage(self,url):
        try:
           
            data = requests.get(url, headers=self.headers).content
            return data
        except Exception, e:
            print e
            
    
    def parse_html(self, html):
        soup = BeautifulSoup(html) #使用bs解析页面，测试可以 print soup.pretiffy()
        content_list_soup = soup.find('div', attrs={'class':'main', 'id':'content'})
        content_list = []
        #for content_li in content_list.findAll(text=re.compile("<span>.*</span>")):
        for content_li in content_list_soup.findAll('div', attrs={'class':'content'}):
           detail = content_li.find('span').text
           content_list.append(detail)
                    
        return content_list
     
    
    #开始方法
    def start(self):
        url = 'http://www.qiushibaike.com/hot/page/' 
        #使用codecs.open读入时直接解码
        nextPage = 2
        with codecs.open(u'qsbk.txt','wb',encoding='utf-8') as fp:
            while url:
                html = self.getPage(url)
                page_content = self.parse_html(html)
                print  page_content
                if(page_content==None):
                    break
                url = url + str(nextPage)
                fp.write(u'{page_content}\n'.format(page_content='\r\n'.join(page_content)))
        
                fp.write('\n')
                     
            
       
     

spider = QSBK()
spider.start()