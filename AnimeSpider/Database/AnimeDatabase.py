# -*- coding:utf-8 -*-

import pymysql.cursors
import configparser
from AnimeSpider.Spider.Anime import Anime

# 数据库类
class AnimeDatabase(object):
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read(r'./Database/database.conf')

        self.__user = conf.get('db', 'db_user')
        self.__password = conf.get('db', 'db_password')
        self.__host = conf.get('db', 'db_host')
        self.__port = int(conf.get('db', 'db_port'))
        self.__charset = 'utf8mb4'
        self.__connectMysql()

        if self.__checkdb() == False:
            self.__createdb()


    def __del__(self):
        self.__conn.close()

    # 连接数据库
    def __connectMysql(self):
        self.__conn = False
        try:
            self.__conn = pymysql.connect(host=self.__host,
                                          user=self.__user,
                                          password=self.__password,
                                          charset=self.__charset)
        except:
            print('数据库连接错误')
            self.__conn = False

    # 判断数据库是否存在
    def __checkdb(self):
        with self.__conn.cursor() as cursor:
            sql = 'show databases'
            cursor.execute(sql)
            rows = cursor.fetchall()
            for db in rows:
                if 'animedatabase' in db:
                    return True
            return False

    # 创建数据库
    def __createdb(self):
        with self.__conn.cursor() as cursor:
            createDatabaseSql = 'create database animedatabase'
            cursor.execute(createDatabaseSql)
            useSql = 'use animedatabase'
            cursor.execute(useSql)
            createTableSql = 'create table animetable(' \
                          'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,' \
                          'name VARCHAR(200) NOT NULL,' \
                          'type VARCHAR(20),' \
                          'date DATE,' \
                          'size VARCHAR(20),' \
                          'download INT,' \
                          'finish INT,' \
                          'magnet VARCHAR(200) NOT NULL,' \
                          'UNIQUE(name)' \
            ')'
            cursor.execute(createTableSql)
            self.__conn.commit()

    # 插入数据
    def insertData(self, anime):
        with self.__conn.cursor() as cursor:
            useSql = 'use animedatabase'
            cursor.execute(useSql)
            insertSql = "INSERT INTO animetable (name, type, date, size, download, finish, magnet) " \
                        "VALUES ('%s', '%s', '%s', '%s', '%d', '%d', '%s')" % (anime.getName(),anime.getType(), anime.getDate(),
                                               anime.getSize(), anime.getDownload(), anime.getFinish(), anime.getMagnet())
            try:
                cursor.execute(insertSql)
                self.__conn.commit()
            except:
                print('插入数据异常')
