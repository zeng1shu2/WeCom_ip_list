# coding:utf-8

from email.header import Header
from email.mime.text import MIMEText
import smtplib
import base64
import config
# 获取配置信息
address = config.mali_config['address']
username = config.mali_config['username']
password = config.mali_config['password']
sender = config.mali_config['sender']
# to_addr = ['收件人邮箱地址']
to_addr = '收件人邮箱地址'


def client_main():
    # 解码
    password_str = str(base64.b64decode(password), 'utf-8')
    # 读取文件
    with open('ip_list.txt') as f:
        ip_list = f.read()
    with open('domain.txt') as f:
        domain = f.read()

    # 构建邮件类容
    msg = MIMEText(ip_list, 'plain', 'utf-8')
    msg['From'] = Header('system', 'utf-8')
    msg['To'] = Header(','.join(to_addr))
    subject = 'IP_list_update'
    msg['Subject'] = Header(subject, 'utf-8')

    # 连接发送服务器
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(address)
        smtpObj.login(username, password_str)
        smtpObj.sendmail(sender, to_addr, msg.as_string())
        smtpObj.close()
        print('发送成功')
    except smtplib.SMTPException:
        print('发送失败')