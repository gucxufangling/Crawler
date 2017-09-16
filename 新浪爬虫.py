# *_*coding:utf-8 *_*

from bs4 import BeautifulSoup
import urllib2
import urllib
import cookielib
import time
import  os

cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


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
        print u"登录失败"



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
    pic = driver.find_elements_by_xpath('//div[@class="WB_media_wrap clearfix"]')
    # pic = driver.find_elements_by_xpath('//li[@class="WB_pic li_1 S_bg1 S_line2 bigcursor"]')
    for x in e:
        try:
            output1.write(x.text.encode('utf8'))
            output1.write("\n")
            print x.text
        except:
            print u"抓取文字失败"

    pic_url= []
    for y in pic:
        try:
            all_img = y.find_elements_by_tag_name("img")  # 某一条微博下的所有图片
            for img in all_img:
                pic_url.append(img.get_attribute('src'))
        except:
            print u"图片下载失败"
        finally:
            # 保存图片到本地以该girl标题命名的目录中
            save_pictures(output2, pic_url)
def main(account, password,  pages=10, one_page_try=6):
    driver = webdriver.Chrome()
    driver.get('https://weibo.com/')

    time.sleep(3)
    login(driver, account, password)
    # # 获得cookie信息
    # cookie = driver.get_cookies()
    # print cookie
    # driver.add_cookie(cookie)

    driver.get('https://weibo.com/stormstormstorm?profile_ftype=1&is_pic=1#_0')

    output1 = open(os.getcwd() + "/sina/yalu.txt", "wb")
    output2 = os.getcwd() + "/sina/yalu_img/"

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
            # driver.add_cookie(cookie)
            driver.get(next_url)
            # login(driver, account, password)
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
    account = "15"
    password = ""
    main(account, password)