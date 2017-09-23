# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql as db
class DoubanBookPipeline(object):
    def __init__(self):
        self.con = db.connect(user="root", passwd="guc", host="localhost", db="testdb", charset="utf8")
        self.cur = self.con.cursor()
        # self.cur.execute('drop table douban_books')
        self.cur.execute(
            "create table douban_books(id int auto_increment primary key,book_name varchar(200),book_star varchar(244),book_pl varchar(244),book_author varchar(200),book_publish varchar(200),book_date varchar(200),book_price varchar(200))")

    def process_item(self, item, spider):
        self.cur.execute(
            "insert into douban_books(id,book_name,book_star,book_pl,book_author,book_publish,book_date,book_price) values(NULL,%s,%s,%s,%s,%s,%s,%s)",
            (item['book_name'], item['book_star'], item['book_pl'], item['book_author'], item['book_publish'],
             item['book_date'], item['book_price']))
        self.con.commit()
        return item