# -*- coding:utf-8 -*-

from AnimeSpider.Spider.AnimeSpider import *

for pageNum in range(1, 2):
    url = generateUrl(pageNum)
    text = visitUrl(url)
    handleUrl(text)
