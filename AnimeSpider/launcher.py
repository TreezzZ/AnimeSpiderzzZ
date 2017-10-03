# -*- coding:utf-8 -*-

from AnimeSpider.Spider.AnimeSpider import AnimeSpider
from AnimeSpider.Email.Email import Email
from AnimeSpider.Logging.Logging import AnimeLog
import threading
import queue

def main():
    msgQueue = queue.Queue()
    log = AnimeLog()

    while True:
        # 开启子线程发送邮件
        taskEmail = threading.Thread(target=checkMsg, name='email', args=(msgQueue, log))
        taskEmail.start()

        # 开启子线程爬取
        spider = AnimeSpider(msgQueue)
        taskSpider = threading.Thread(target=spider.start, name='spider')
        taskSpider.start()
        taskSpider.join()

# 检查消息队列，发送邮件啊
def checkMsg(msgQueue, log):
    while True:
        if not msgQueue.empty():
            msg = msgQueue.get()
            email = Email()
            email.sendEmail(msg[0], msg[1])
            log.info('发送邮件: 内容: ' + str(msg))

if __name__ == '__main__':
    main()