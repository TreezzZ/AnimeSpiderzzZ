# -*- coding:utf-8 -*-

from email.mime.text import MIMEText
from email.header import Header
import smtplib
import configparser

# 构造邮件
# @param AnimeName 动漫名称
# @param AnimeMagnet 动漫链接
# @return 邮件
def createEmail(AnimeName, AnimeMagnet):
    content = '动漫更新: ' + AnimeName + ', 你好: ' + AnimeMagnet
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header('动漫更新···来自人工智障AI酱', 'utf-8').encode()
    return msg

# 发送邮件
# @param msg 邮件
def sendEmail(msg):
    conf = configparser.ConfigParser()
    conf.read(r'./Email/email.conf')
    emailFrom = conf.get('email', 'email_from')
    emailPassword = conf.get('email', 'email_password')
    emailPort = conf.get('email', 'email_port')
    emailTo = conf.get('email', 'email_to')
    emailServer = conf.get('email', 'email_stmp')

    server = smtplib.SMTP(emailServer, emailPort)
    server.starttls()
    #server.set_debuglevel(1)
    server.login(emailFrom, emailPassword)
    server.sendmail(emailFrom, [emailTo], msg.as_string())
    server.quit()
