# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
reload(sys)
from bs4 import BeautifulSoup
import re
import urllib2
import xlwt


class MovieTop250:
    def __init__(self):
        #设置默认编码格式为utf-8
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.start = 0
        self.param = '&filter=&type='
        self.headers =  {'Host':'sec.douban.com',
                         
                         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        self.movieList = []
        
    def download_page(self, url):
        #获取爬虫的页面内容
        request = urllib2.Request(url, headers=self.headers)
        try:
            response = urllib2.urlopen(request) #取得响应
            html = response.read().decode('utf-8')#获取网页内容
        except urllib2.URLError, e:
            if hasattr(e,'code'):
                print e.code
            if hasattr(e,'reason'):
                print e.reason
        return html

    def getData(self, html):
        soup = BeautifulSoup(html) #使用bs解析页面，测试可以 print soup.pretiffy()
        movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
        #根据css获得爬取页面的信息
        for movie_li in movie_list_soup.find_all('li') :#遍历页面中有关信息
            detail = movie_li.find('div',attrs={'class':'info'})#找到电影描述

            link = detail.a['href']#找到影片详情链接
            name = detail.find('div',attrs={'class':'hd'}).find("a").text   #找到所有名字
            #name = detail.div.a.text.strip()  #等同于上面
            name = name.split("/") #根据/分割
            movie_chinese_name = name[0]
            movie_foreign_name = name[1:]

            #找到影片相关内容：导演，主演，年份，地区，类别
            bd = detail.find('div',attrs={'class':'bd'}).find('p').text
            bd = bd.strip()
            bd = re.split(r'[:/]',str(bd))
            director = re.sub(r"[主演]", "", bd[1]).strip()
            actor = bd[2]
            year = bd[3].strip()
            country =  bd[4]
            type =  bd[5]

            rating = detail.find('span',attrs={'class':'rating_num', 'property':'v:average'}).getText() #找到评分
            findJudge=re.compile(r'<span>(\d*)人评价</span>')#找到评价人数
            inq=detail.find('span',attrs={'class':'inq'}).getText() #找到概况

            detail = str(detail)
            judgeNum = re.findall(findJudge, detail)[0]

            self.movieList.append([link, movie_chinese_name, movie_foreign_name, director, actor, year, country, type,rating,judgeNum, inq] )
            print self.movieList
        next_url = soup.find('span', attrs={'class': 'next'}).find('a')  # 查找下一页
        return next_url

    #数据写入excle中
    def saveData(self, datalist,savepath):
        book=xlwt.Workbook(encoding='utf-8',style_compression=0)
        sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
        col=('电影详情链接','影片中文名','影片外国名','导演','主演','年份','地区','类别', '评分','评价数','概况',)
        for i in range(0,11):
            sheet.write(0,i,col[i])#列名
        for i in range(0,250):
            data=datalist[i]
            for j in range(0,11):
                sheet.write(i+1,j,data[j])#数据
        book.save(savepath)#保存

    def main(self):
        print u"正在爬取豆瓣电影"
        url = 'https://movie.douban.com/top250'
        savepath = u'豆瓣电影Top250.xlsx'
        while True:
            html = self.download_page(url)
            next_url = self.getData(html)
            url = url + next_url
            if next_url == None:
                break
        self.saveData(self.movieList, savepath)


spider = MovieTop250()
spider.main()