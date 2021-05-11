# coding:utf-8
from toosl import Client_Stmp, web_main
import logging
import json
import httplib2
import os
import sys
from ctypes import *


def lock():
    """锁定鼠标键盘"""
    lock_ = windll.LoadLibrary('user32.dll')
    lock_.BlockInput(True)


def unlock():
    """解锁鼠标键盘"""
    lock_ = windll.LoadLibrary('user32.dll')
    lock_.BlockInput(False)


def log_info():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
                        filename='log/system.log',
                        filemode='a'
                        )
    return logging


def exit_app():
    log_info().info('暂无任何可更新的IP与域名，程序将退出。')
    sys.exit()


def check_dir():
    if os.path.exists('log'):
        path = os.path.abspath('log')
        file = 'update_time.txt'
        new_path = os.path.join(path, file)
        return new_path
    else:
        os.mkdir('log')
        log_info().info("log目录已创建成功")
        path = os.path.abspath('log')
        file = 'update_time.txt'
        new_path = os.path.join(path, file)
        return new_path


def uptime_write(j_data):
    new_path = check_dir()
    if os.path.exists(new_path):
        if os.path.getsize(new_path) != 0:
            with open(new_path, 'r+') as f:
                data = f.read()
                log_info().info('update_time存在，正在读取更新时间。')
            return data
        else:
            with open(new_path, 'w+') as f:
                j_data = f.write(j_data)
                return j_data
    else:
        with open(new_path, 'w+') as f:
            j_data = f.write(j_data)
            return j_data


def data_write(ip_data, domain_data):
    path = os.path.abspath('log')
    ip_addr = os.path.join(path, 'ip_list.txt')
    domain = os.path.join(path, 'domain.txt')
    if os.path.exists(ip_addr and domain):
        with open(ip_addr, 'w+') as f:
            f.write('\n'.join(ip_data))
        with open(domain, 'w+') as f:
            f.write('\n'.join(domain_data))
    else:
        with open(ip_addr, 'w') as f:
            f.write('\n'.join(ip_data))
        with open(domain, 'w') as f:
            f.write('\n'.join(domain_data))


def update_time():
    client = httplib2.Http(disable_ssl_certificate_validation=True)
    response, content = client.request('https://res.mail.qq.com/zh_CN/wework_ip/latest.json')
    date_time = response.get('last-modified')
    return date_time


def data_processing():
    client = httplib2.Http(disable_ssl_certificate_validation=True)
    response, content = client.request('https://res.mail.qq.com/zh_CN/wework_ip/latest.json')
    j_data = json.loads(content)
    ip_list = set([ip for j_data in j_data for ip in j_data.get('IPList').get('cnet') or []])
    domain_list = set(
        [domain for j_data in j_data for domain in j_data.get('Domain') or j_data.get('OnlyDomain')
         if domain not in '无域名']
    )
    return ip_list, domain_list


def main(fo_email, _url):
    new_time = update_time()
    time = uptime_write(new_time)
    if new_time == time:
        exit_app()
    else:
        new_path = check_dir()
        with open(new_path, 'w') as f:
            log_info().info('正在写入新的更新时间')
            f.write(new_time)

        log_info().info('正在写入新的IP和域名。')
        j_dada = data_processing()
        data_write(j_dada[0], j_dada[1])
        log_info().info('正在发送邮箱通知。')
        log_info().info('正在调用浏览器。')
        lock()
        web_main.web_main(_url)
        log_info().info('调用浏览器完成。')
        unlock()
        Client_Stmp.client_main(fo_email)


if __name__ == '__main__':
    check_dir()
    _fo_email = str(input('请输入接收通知的邮箱地址：'))
    name = '邮箱地址为：'
    data_info = name, _fo_email
    log_info().info(''.join(data_info))
    if _fo_email.endswith('@zlg.cn'):
        _url = str(input("请输入AC管理地址："))
        name = 'AC地址为：'
        data_info = name, _url
        log_info().info(''.join(data_info))
        if _url.endswith(':25840'):
            main(_fo_email, _url)
        else:
            log_info().warning('请输入正确的格式')
            raise TypeError('输入的格式不正确')
    else:
        log_info().warning('请输入正确的格式')
        raise TypeError('输入的格式不正确')
