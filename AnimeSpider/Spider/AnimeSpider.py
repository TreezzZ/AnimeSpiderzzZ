# -*- coding:utf-8 -*-

import bs4
import requests
import re
import time
from bs4 import BeautifulSoup
from AnimeSpider.Spider.Anime import Anime
from AnimeSpider.Database.AnimeDatabase import AnimeDatabase

# 生成url链接
# @param pageNum 访问的页数
# @return 要访问的url 
def generateUrl(pageNum):
    return r'http://www.36dm.com/sort-2-' + str(pageNum) + r'.html'

# 得到所有动漫的页数
def getAllPagesNum():
    response = visitUrl(r'http://www.36dm.com/sort-2-2.html')
    soup = BeautifulSoup(response, 'html.parser')
    lastPage = soup.find_all('a', attrs={'class':'pager-last active'})
    return int(lastPage[0].string)

# 访问url
# @param url 要访问的url
def visitUrl(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        print('网络错误')

# 提取动漫信息，写入数据库
# @param text 待处理的信息
def handleUrl(text):
    soup = BeautifulSoup(text, 'html.parser')
    AnimeInfo = soup.find_all('tr', attrs={'class':'alt1'})
    AnimeInfo.extend(soup.find_all('tr', attrs= {'class':'alt2'}))

    for tr in AnimeInfo:
        # 去掉非Tag子节点
        childrenNodes = [item for item in tr.contents if type(item) is bs4.element.Tag]

        db = AnimeDatabase()

        try:
            AnimeDate = handleDate(childrenNodes[0].string.strip())
            AnimeType = childrenNodes[1].contents[0].string.strip()
            AnimeName = escapeCharacter(childrenNodes[2].contents[1].string.strip())
            AnimeSize = childrenNodes[3].string.strip()

            print('正在处理: 动漫名称: ' + AnimeName)

            # 这两个数据是js生成的，暂时不好提取
            AnimeDownload = ''
            AnimeFinish = ''

            AnimeMagnet = getManget(r'http://www.36dm.com/' + childrenNodes[2].contents[1].get('href')).strip()
            anime = Anime(AnimeName, AnimeType, AnimeDate, AnimeSize, AnimeDownload, AnimeFinish, AnimeMagnet)

            db.insertData(anime)

        except:
            continue


# 提取网页中的磁力链接
# @param url 待访问网页
# @return 磁力链接
def getManget(url):
    text = visitUrl(url)
    soup = BeautifulSoup(text, 'html.parser')
    magnet = soup.find('a', id='magnet').get('href')
    return magnet

# 处理提取的日期
# @param AnimeDate 待处理日期
# @return python格式日期
def handleDate(AnimeDate):
    dateList = re.match(r'([01][0-9])/([0-3][0-9]) ([0-2][0-9]):([0-5][0-9])', AnimeDate)
    month = dateList.group(1)
    day = dateList.group(2)
    year = time.strftime('%Y')
    return year + '-' + month + '-' + day

# 对动漫名称中含有'和"进行转义，否则插入失败
# @param AnimeName 待转义名称
# @return 转义后的名称
def escapeCharacter(AnimeName):
    AnimeName = AnimeName.replace("'", "&0")
    AnimeName = AnimeName.replace('"', "&0")
    return AnimeName
