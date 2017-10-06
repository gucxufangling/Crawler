# *_*coding:utf-8 *_*

import requests
import json
import  codecs
import xlwt

headers = {
            "user-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
             "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept-Encoding": "gzip, deflate, br"
        }

def get_request(url):
    html = requests.get(url, headers=headers).text
    data = json.loads(html)
    return data

def main():
    url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=100'
    data = get_request(url)
    # print len(data)
    # f = codecs.open('douban.json', 'wb', encoding='utf-8')
    # for i in range(len(data)):
    #     line = json.dumps(data[i],ensure_ascii=False)+'\n'
    #     f.write(line)
    # f.close()

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('电影', cell_overwrite_ok=True)
    col = ('rank', 'rating',  'title', 'url', 'release_date',  'regions',  'vote_count',  'types')
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(len(data)):
        item = data[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, item[col[j]])  # 数据
    book.save(u'电影ajax.xls')  # 保存




main()