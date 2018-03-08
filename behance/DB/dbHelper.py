# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings


class DBHelper():

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    # 创建数据库
    def insert(self, item):
        sql = "insert into behance_tag(tag_name,tag_id,pic_url,tag_words) values(%s,%s,%s,%s)"
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._conditional_insert, sql, item)
        # 调用异常处理方法
        query.addErrback(self._handle_error)

        return item

    # 写入数据库中
    def _conditional_insert(self, tx, sql, item):
        params = (item["tag_name"], item["tag_id"], item["pic_url"], item["tag_words"])
        tx.execute(sql, params)

    # 错误处理方法

    def insert_author(self, item):
        sql = "insert into behance_author(author_name,author_url) values(%s,%s)"
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._conditional_insert_author, sql, item)
        # 调用异常处理方法
        query.addErrback(self._handle_error)

        return item

    def _conditional_insert_author(self, tx, sql, item):
        params = (item["author_name"], item["author_url"])
        tx.execute(sql, params)


    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)

