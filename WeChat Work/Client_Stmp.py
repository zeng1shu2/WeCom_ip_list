# coding:utf-8

from email.header import Header
from email.mime.text import MIMEText
import smtplib
import base64
import configs
# 获取配置信息
address = configs.mali_config['address']
username = configs.mali_config['username']
password = configs.mali_config['password']
sender = configs.mali_config['sender']


def client_main(fo_email):
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
    msg['To'] = Header(fo_email)
    subject = 'IP_list_update'
    msg['Subject'] = Header(subject, 'utf-8')

    # 连接发送服务器
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(address)
        smtpObj.login(username, password_str)
        smtpObj.sendmail(sender, fo_email, msg.as_string())
        smtpObj.close()
        print('邮箱发送成功')
    except smtplib.SMTPException:
        print('邮箱发送失败')