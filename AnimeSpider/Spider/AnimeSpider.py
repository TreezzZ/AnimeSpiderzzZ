# -*- coding:utf-8 -*-

import bs4
import requests
import re
import time
import configparser
from itertools import chain
from bs4 import BeautifulSoup
from AnimeSpider.Spider.Anime import Anime
from AnimeSpider.Database.AnimeDatabase import AnimeDatabase
from AnimeSpider.Logging.Logging import AnimeLog


class AnimeSpider(object):
    def __init__(self, MsgQueue):
        # 日志
        self.__log = AnimeLog()
        self.__log.info('配置爬虫')

        conf = configparser.ConfigParser()
        self.__configpath = r'./Spider/spider.conf'
        conf.read(self.__configpath, 'utf-8')
        # 最新爬取的链接
        self.__lastlink = conf.get('spider', 'last_link')
        self.__log.info('上次爬取至: ' + self.__lastlink)

        # 停止爬取
        self.__stop = False

        # 本次爬取第一个链接
        self.__first = True

        # 本地爬取完成后作为最新爬取的连接
        self.__newlastlink = self.__lastlink

        # 数据库
        self.__database = AnimeDatabase()
        self.__log.info('数据库初始化')

        # 与主线程通信的消息队列
        self.__msg = MsgQueue

        # 关注内容，有更新会发送到邮箱
        self.__follow = list(conf.get('spider', 'follow').split(';'))

    def __del__(self):
        conf = configparser.ConfigParser()
        conf.set('spider', 'last_link', self.__newlastlink)
        conf.write(open(self.__configpath), 'w')


    # 开始爬取
    def start(self):
        self.__log.info('开始爬取')
        pageNums = self.__getAllPagesNum()
        self.__log.info('获取全部页数: ' + str(pageNums))
        for pageNum in range(1, pageNums+1):
            if self.__stop == True:
                break
            url = self.__generateUrl(pageNum)
            page = self.__visitUrl(url)
            self.__handleUrl(page)
        self.__log.info('爬取结束')

    # 生成url链接
    # @param pageNum 访问的页数
    # @return 要访问的url
    def __generateUrl(self, pageNum):
        return r'http://www.36dm.com/sort-2-' + str(pageNum) + r'.html'
    
    # 得到所有动漫的页数
    def __getAllPagesNum(self):
        response = self.__visitUrl(r'http://www.36dm.com/sort-2-2.html')
        soup = BeautifulSoup(response, 'html.parser')
        lastPage = soup.find_all('a', attrs={'class':'pager-last active'})
        return int(lastPage[0].string)
    
    # 访问url
    # @param url 要访问的url
    def __visitUrl(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
            return r.text
        except:
            self.__log.warning('网络错误')

    # 提取动漫信息，写入数据库
    # @param text 待处理的信息
    def __handleUrl(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        AnimeInfo1 = soup.find_all('tr', attrs={'class':'alt1'})
        AnimeInfo2 = soup.find_all('tr', attrs= {'class':'alt2'})
        # 交错合并两个list
        AnimeInfo = chain.from_iterable(zip(AnimeInfo1, AnimeInfo2))

        for tr in AnimeInfo:
            # 去掉非Tag子节点
            childrenNodes = [item for item in tr.contents if type(item) is bs4.element.Tag]
    
            try:
                AnimeDate = self.__handleDate(childrenNodes[0].string.strip())
                AnimeType = childrenNodes[1].contents[0].string.strip()
                AnimeName = self.__escapeCharacter(childrenNodes[2].contents[1].string.strip())
                AnimeSize = childrenNodes[3].string.strip()
                AnimeUrl = r'http://www.36dm.com/' + childrenNodes[2].contents[1].get('href')
                AnimeMagnet = self.__getManget(AnimeUrl).strip()

                # 通过分析网页发现，这两个数据是后台通过调用random()随机生成的，无参考意义
                AnimeDownload = ''
                AnimeFinish = ''

                anime = Anime(AnimeName, AnimeType, AnimeDate, AnimeSize, AnimeDownload, AnimeFinish, AnimeMagnet)

                # 爬到上次更新的位置，终止爬取
                if AnimeUrl == self.__lastlink:
                    __stop = True
                    break

                # 设置新的最新爬取位置
                if self.__first == True:
                    self.__first = False
                    self.__newlastlink = AnimeUrl

                # 有关注内容出现
                for follow in self.__follow:
                    if follow in AnimeName:
                        self.__msg.put((AnimeName, AnimeMagnet))

                self.__database.insertData(anime)

                self.__log.info('动漫名称: ' + AnimeName)
                self.__log.info('动漫链接: ' + AnimeUrl)
    
            except:
                continue
    
    # 提取网页中的磁力链接
    # @param url 待访问网页
    # @return 磁力链接
    def __getManget(self, url):
        text = self.__visitUrl(url)
        soup = BeautifulSoup(text, 'html.parser')
        magnet = soup.find('a', id='magnet').get('href')
        return magnet
     
    # 处理提取的日期
    # @param AnimeDate 待处理日期
    # @return python格式日期
    def __handleDate(self, AnimeDate):
        dateList = re.match(r'([01][0-9])/([0-3][0-9]) ([0-2][0-9]):([0-5][0-9])', AnimeDate)
        month = dateList.group(1)
        day = dateList.group(2)
        year = time.strftime('%Y')
        return year + '-' + month + '-' + day
    
    # 对动漫名称中含有'和"进行转义，否则插入失败
    # @param AnimeName 待转义名称
    # @return 转义后的名称
    def __escapeCharacter(self, AnimeName):
        AnimeName = AnimeName.replace("'", "&0")
        AnimeName = AnimeName.replace('"', "&0")
        return AnimeName
