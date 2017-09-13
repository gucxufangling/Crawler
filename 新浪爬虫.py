# *_*coding:utf-8 *_*

# Accept:*/*
# Accept-Encoding:gzip, deflate, br
# Accept-Language:zh-CN,zh;q=0.8
# Connection:keep-alive
# Cookie:_s_tentry=www.liaoxuefeng.com; Apache=6685611027743.496.1499329798538; SINAGLOBAL=6685611027743.496.1499329798538; ULV=1499329798818:1:1:1:6685611027743.496.1499329798538:; login_sid_t=9d77a35c0cf60e3991d0f946acbf6f7e; UM_distinctid=15dfeb642c639b-02b009af89a27f-3a3e5e06-100200-15dfeb642c796e; cross_origin_proto=SSL; UOR=www.liaoxuefeng.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1505191588; SCF=As5M8pYdNXV8DsE1yRL0jHbx9i2edKOXMFWFttONxRbqgBUYInzCypvfMOTyojKk7-i2PdgYEfi_mQqQesPvd4Q.; SUB=_2A250sxb0DeRhGedJ71QV8S7EyziIHXVXyQ88rDV8PUNbmtAKLXfBkW9gwcR5feyRIWIeaw_rKlQkyVWtpg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFjH5gxyx174yF_-1A505lE5JpX5K2hUgL.Fo2NShqXeK5RehB2dJLoI79rUgSjTg7t; SUHB=0mxV2tkDyZGCYQ; ALF=1536727587; un=15222929709; wvr=6
# Host:contentrecommend-out.uve.weibo.com
# Referer:https://weibo.com/516571237/home?wvr=5&lf=reg
# User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36

from bs4 import BeautifulSoup
import urllib2
import urllib
import cookielib
import time
import  os

cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36',
          'Cookie':'_s_tentry=www.liaoxuefeng.com; Apache=6685611027743.496.1499329798538; SINAGLOBAL=6685611027743.496.1499329798538; ' \
                   'ULV=1499329798818:1:1:1:6685611027743.496.1499329798538:; login_sid_t=9d77a35c0cf60e3991d0f946acbf6f7e; ' \
                   'UM_distinctid=15dfeb642c639b-02b009af89a27f-3a3e5e06-100200-15dfeb642c796e; cross_origin_proto=SSL;' \
                   ' UOR=www.liaoxuefeng.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1505191588; ' \
                   'SCF=As5M8pYdNXV8DsE1yRL0jHbx9i2edKOXMFWFttONxRbqgBUYInzCypvfMOTyojKk7-i2PdgYEfi_mQqQesPvd4Q.; ' \
                   'SUB=_2A250sxb0DeRhGedJ71QV8S7EyziIHXVXyQ88rDV8PUNbmtAKLXfBkW9gwcR5feyRIWIeaw_rKlQkyVWtpg..; ' \
                   'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFjH5gxyx174yF_-1A505lE5JpX5K2hUgL.Fo2NShqXeK5RehB2dJLoI79rUgSjTg7t; ' \
                   'SUHB=0mxV2tkDyZGCYQ; ALF=1536727587; un=15222929709; wvr=6',
          'Host':'contentrecommend-out.uve.weibo.com',
          'Connection': 'keep-alive',
          'Referer':'https://weibo.com/516571237/home?wvr=5&lf=reg' }


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "http://www.weibo.com/login.php"


def login(driver, account, password):
    try:
        label = driver.find_element_by_link_text('登录')
        label.click()
    except:
        pass
    try:
        label = driver.find_element_by_link_text('帐号登录')
        label.click()
    except:
        pass
    try:
        login_name = driver.find_element_by_id("loginname")
        login_name.send_keys(account)
    except:
        pass
    try:
        login_pw = driver.find_element_by_name('password')
        login_pw.send_keys(password)
        login_pw.send_keys(Keys.RETURN)
    except:
        pass

def to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# find the next page button or return None
def find_next_page_or_none(driver):
    try:
        next_page = driver.find_element_by_link_text('下一页')
        return next_page
    except:
        return None


def save_page_content(driver, output1, output2):
    # 抓到所有微博
    e = driver.find_elements_by_xpath('//div[@class="WB_text W_f14"]')
    pic = driver.find_elements_by_xpath('//div[@class="WB_expand_media_box"]')
    for x in e:
        try:
            output1.write(x.text.encode('utf8'))
            output1.write("\n")
            print x.text
        except:
            print u"抓取文字失败"

    for y in pic:
        print y
        try:
            all_img = y.find_elements_by_tag_name("img")  # 某一条微博下的所有图片
            pic_url = [x.get_attribute('src') for x in all_img]

            # 保存图片到本地以该girl标题命名的目录中
            save_pictures(output2, pic_url)
        except:
            print
            u"图片下载失败"

def main(account, password,  pages=10, one_page_try=6):
    driver = webdriver.Chrome()
    driver.get('https://weibo.com/')
    time.sleep(3)
    login(driver, account, password)

    driver.get('https://weibo.com/stormstormstorm?profile_ftype=1&is_ori=1#_0')

    output1 = open(os.getcwd() + "/sina/yalu.txt", "wb")
    output2 = os.getcwd() + "/sina/yalu_img"

    for i in range(pages):
        for j in range(one_page_try):
            if find_next_page_or_none(driver) is None:
                # 拽到页面最下方
                time.sleep(5)
                to_bottom(driver)
            else:
                break

        save_page_content(driver, output1, output2)

        print u'正在进行第',  + 1, u'次停顿，防止访问次数过多'
        time.sleep(60)

        # 翻页
        try:
            next_url = find_next_page_or_none(driver)
            driver.get(next_url)
            login(driver, account, password)
            # 重新login
        except:
            print u"翻页失败"
            break

    output1.close()
    driver.close()

def save_pictures(path, url_list):
    """
    保存图片到本地指定文件夹
    :param path: 保存图片的文件夹，由mkdir_for_girl返回
    :param url_list: 待保存图片的url列表
    :return: none
    """
    for (index, url) in enumerate(url_list):
        try:
            print u'%s 正在保存第%d张图片' % (time.ctime(), index)
            pic_name = str(index) + '.jpg'
            file_name = os.path.join(path, pic_name)
            # 如果存在该图片则不保存
            if os.path.exists(file_name):
                print u'%s 该图片已经存在' % time.ctime()
                continue
            req = urllib2.Request(url, headers={'User-Agent':  r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'})
            data = urllib2.urlopen(req, timeout=30).read()
            f = open(file_name, 'wb')
            f.write(data)
            f.close()
        except Exception, e:
            print u'%s 第%d张图片保存失败，不处理，跳过继续处理下一张' % (time.ctime(), index)

def write_text(path, info):
    """
    在path目录中创建txt文件，将info信息（girl的文本描述和对话）写入txt文件中
    :param path: 保存txt文件的目录，由mkdir_for_girl返回
    :param info: 要写入txt的文本内容
    :return: none
    """
    # 创建/打开info.txt文件，并写入内容
    filename = os.path.join(path, 'info.txt')

    with open(filename, 'a+') as fp:
        fp.write(info.encode('utf-8'))
        fp.write('\n'.encode('utf-8'))
        fp.write('\n'.encode('utf-8'))

if __name__ == '__main__':
    account = "1"
    password = ""
    main(account, password)