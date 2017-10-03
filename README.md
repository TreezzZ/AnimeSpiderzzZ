# 动漫爬虫

## 模块说明
`Database` 数据库模块 负责抓取动漫数据相关数据库操作 <br>
`Email` 邮件模块 当抓取到感兴趣的内容时，通过邮件发送提醒用户 <br>
`Logging`日志模块 负责日志记录 <br>
`Spider`爬虫模块 负责数据抓取 <br>

## 使用说明
基于python3
`Spider`目录下的`spider.conf`文件中的`follow`项是用户感兴趣内容的配置文件，在此项写入感兴趣的内容，`;`分隔，抓取到相关内容后会通过邮件提醒 <br>

`Email`目录下的`email.conf`文件是用户邮箱配置文件，其中`email_from`记录用户发送提醒的邮箱，`email_password`记录用户密码
或授权码，`email_to`记录用户想要发送到的邮箱，`email_port`记录smtp邮件服务器端口，`email_smtp`记录smtp邮件服务器地址，
具体可查阅相关邮箱帮助 <br>

`Database`目录下的`database.conf`文件是数据库配置文件，其中`db_user`为用户名,`db_password`为密码，`db_host`为数据库地址,
`db_port`为数据库端口配置好相关文件后，运行laucher.py即可 <br>
