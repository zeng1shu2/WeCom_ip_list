# coding:utf-8

from email.header import Header
from email.mime.text import MIMEText
from config import user_config
from toosl import Logging
import smtplib
import base64
import os


# 获取配置信息
address = user_config.mali_config['address']
username = user_config.mali_config['username']
password = user_config.mali_config['password']
sender = user_config.mali_config['sender']


def client_main(fo_email):
    # 解码
    password_str = str(base64.b64decode(password), 'utf-8')
    # 读取文件
    try:
        path = os.path.abspath('log')
        list_ip = 'ip_list.txt'
        domain = 'domain.txt'
        list_ip = os.path.join(path, list_ip)
        domain = os.path.join(path, domain)
        with open(list_ip) as f:
            ip_list = f.read()
        with open(domain) as f:
            domain = f.read()
    except FileNotFoundError as e:
        print(e)
    # 构建邮件类容
    msg = MIMEText(ip_list, 'plain', 'utf-8')
    msg['From'] = Header('system', 'utf-8')
    msg['To'] = Header(fo_email)
    subject = 'IP_list_update'
    msg['Subject'] = Header(subject, 'utf-8')

    # 连接发送服务器
    try:
        mali_object = smtplib.SMTP()
        mali_object.connect(address)
        mali_object.login(username, password_str)
        mali_object.sendmail(sender, fo_email, msg.as_string())
        mali_object.close()
        Logging.logs().info('邮箱发送成功')
    except smtplib.SMTPException:
        Logging.logs().error('邮箱发送错误')
