# -*- coding:utf-8 -*-

import logging

# 日志类
class AnimeLog(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='./Logging/AnimeLog.log',
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)

    def warning(self, msg):
        logging.warning(msg)
