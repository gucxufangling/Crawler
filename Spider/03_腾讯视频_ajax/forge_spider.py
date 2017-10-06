# *_*coding:utf-8 *_*
#功能：	爬取腾讯视频播放链接
#  读取一个随机的头部User-Agent 信息 添加到请求中此作为基础的伪造,

import requests
import random,re, os
headers = {
            "user-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
             "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept-Encoding": "gzip, deflate, br"
        }
def get_request(url):
    try:
        # 字符串连接成命令,注意保留空格
        common = 'phantomjs ' + 'forge_xforward.js ' + url
        print common
        str_body = str(os.popen(common).read())
        print str_body
        return str_body
    except Exception, e:
        print Exception,e
        return  -1

if __name__ == '__main__':
    url = "https://v.qq.com/x/cover/u3cgw9e383hnl7z/n0022y6dfv7.html"

    html_body = get_request(url)

    print html_body

    print re.findall('https://imgcache.qq.com/tencentvideo_v1/.*=0', html_body)
