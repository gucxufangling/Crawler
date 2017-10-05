# *_*coding:utf-8 *_*
import requests
from bs4 import BeautifulSoup
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

reload(sys)
sys.setdefaultencoding('utf8') #解决错误：ascii' codec can't encode characters in position 0-22: ordinal not in range(128)

headers = {
            "user-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
             "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests":"1",
            "Connection":"keep-alive"
        }
def to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# find the next page button or return None
def find_next_page_or_none(driver):
    try:
        next_page = driver.find_element_by_link_text('下一页')
        return next_page
    except:
        return None

def get_urls():
    needs=[[u'财经','http://business.sohu.com/'],[u'军事','http://mil.sohu.com/']
        ,[u'科技','http://it.sohu.com/'],[u'体育','http://sports.sohu.com/'],[u'教育','http://learning.sohu.com/']
        ,[u'娱乐','http://yule.sohu.com/'],[u'旅游','http://travel.sohu.com/']]
    for item in needs:
        newstype=item[0]
        baseurl=item[1]
        result=get_content(baseurl)
        f=open('urls.txt','a')
        for news in result:
            line=newstype+'|'+str(news[0])+'|'+news[1]
            f.write(line.replace('\r','').replace('\n','')+'\n')
        f.close()
        print(newstype,'ok')

def get_content(baseurl):
    driver = webdriver.Chrome()
    driver.get(baseurl)
    for i in range(10):#下拉10次数
        time.sleep(5)
        to_bottom(driver)
    soup = BeautifulSoup(driver.page_source, 'xml')
    info = soup.find_all('div', attrs={'data-role':'news-item'})
    result = []
    for i in info:
        title = i.find('h4').text
        url = i.find('a')['href']
        result.append([title, url])
        print title,url
    return  result

get_urls()