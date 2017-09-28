# -*- coding:utf-8 -*-

import bs4
import requests
from bs4 import BeautifulSoup

from Anime import Anime


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

    cnt = 1
    for tr in AnimeInfo:
        # 去掉非Tag子节点
        childrenNodes = [item for item in tr.contents if type(item) is bs4.element.Tag]

        try:
            AnimeDate = childrenNodes[0].string.strip()
            AnimeType = childrenNodes[1].contents[0].string.strip()
            AnimeName = childrenNodes[2].contents[1].string.strip()
            AnimeSize = childrenNodes[3].string.strip()

            # 这两个数据是js生成的，暂时不好提取
            AnimeDownload = ''
            AnimeFinish = ''

            AnimeMagnet = getManget(r'http://www.36dm.com/' + childrenNodes[2].contents[1].get('href')).strip()
            anime = Anime(AnimeName, AnimeType, AnimeDate, AnimeSize, AnimeDownload, AnimeFinish, AnimeMagnet)

            with open('data.txt', 'a') as f:
                f.write(anime.getName())
                f.write(anime.getMagnet())
                f.write('\n')

            print('------------------------')
            print('cnt:' + str(cnt))
            print('AnimeName: ' + anime.getName())
            print('AnimeMagnet: ' + anime.getMagnet())
            print('------------------------')
            cnt += 1
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

def main():
    #pageNums = getAllPagesNum()

    # 访问某一页
    for pageNum in range(1, 2):
        url = generateUrl(pageNum)
        text = visitUrl(url)
        handleUrl(text)

if __name__ == '__main__':
    main()
