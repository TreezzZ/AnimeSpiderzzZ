# -*- coding:utf-8 -*-


# 动漫类，用于存储动漫实体
class Anime(object):
    # @param mname 动漫名称
    # @param mtype 动漫类型
    # @param mdate 发布日期
    # @param msize 资源大小
    # @param mdownload 下载数
    # @param mfinish 完成数
    # @param mmagnet 磁力链接
    def __init__(self, mname, mtype, mdate, msize, mdownload, mfinish, mmagnet):
        self.__name = mname
        self.__type = mtype
        self.__date = mdate
        self.__size = msize
        #self.__download = mdownload
        #self.__finish = mfinish
        self.__download = 0
        self.__finish = 0
        self.__magnet = mmagnet

    def getName(self):
        return self.__name

    def getType(self):
        return self.__type

    def getDate(self):
        return self.__date

    def getSize(self):
        return self.__size

    def getDownload(self):
        return self.__download

    def getFinish(self):
        return self.__finish

    def getMagnet(self):
        return self.__magnet