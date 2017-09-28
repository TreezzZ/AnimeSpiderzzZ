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
        self.connectMysql()

        if self.checkdb() == False:
            self.createdb()

    def __del__(self):
        self.__conn.close()

    # 连接数据库
    def connectMysql(self):
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
    def checkdb(self):
        with self.__conn.cursor() as cursor:
            sql = 'show databases'
            cursor.execute(sql)
            rows = cursor.fetchall()
            for db in rows:
                if 'animedatabase' in db:
                    return True
            return False

    # 创建数据库
    def createdb(self):
        with self.__conn.cursor() as cursor:
            createDatabaseSql = 'create database animedatabase'
            cursor.execute(createDatabaseSql)
            useSql = 'use animedatabase'
            cursor.execute(useSql)
            createTableSql = 'create table animetable(' \
                          'id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY ,' \
                          'name VARCHAR(100) NOT NULL,' \
                          'type VARCHAR(20),' \
                          'date VARCHAR(20),' \
                          'size VARCHAR(20),' \
                          'download INT,' \
                          'finish INT,' \
                          'magnet VARCHAR(200) NOT NULL' \
            ')'
            cursor.execute(createTableSql)
            self.__conn.commit()

    # 插入数据
    def insertData(self, anime):
        with self.__conn.cursor() as cursor:
            useSql = 'use animedatabase'
            cursor.execute(useSql)
            insertSql = 'INSERT INTO animetable(name, type, date, size, download, finish, magnet) ' \
                        'VALUES (%s, %s, %s, %s, %d, %d, %s)'
            try:
                print(anime.getName())
                print(anime.getType())
                print(anime.getDate())
                print(anime.getDownload())
                print(anime.getFinish())
                print(anime.getSize())
                print(anime.getMagnet())

                print(str(type(anime.getDownload())))
                rs = cursor.execute(insertSql, (anime.getName(),anime.getType(), anime.getDate(),
                                               anime.getSize(), anime.getDownload(), anime.getFinish(), anime.getMagnet()))
                self.__conn.commit()
            except:
                print('插入数据异常')
