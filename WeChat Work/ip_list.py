# coding:utf-8

import json
import httplib2
import os
import sys
import Client_Stmp
import web_main


def exit_app():
    print("暂无更新的IP列表")
    sys.exit()


def uptime_write(j_data):
    path = os.getcwd()
    file = 'update_time.txt'
    new_path = os.path.join(path, file)
    if os.path.exists(new_path):
        if os.path.getsize(new_path) != 0:
            with open(new_path, 'r+') as f:
                data = f.read()
                return data
        else:
            with open(new_path, 'w+') as f:
                f.write(j_data)
                return j_data
    else:
        with open(new_path, 'w+') as f:
            f.write(j_data)


def data_write(ip_data, domain_data):
    path = os.getcwd()
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
        j_dada = data_processing()
        data_write(j_dada[0], j_dada[1])
        web_main.web_main(_url)
        Client_Stmp.client_main(fo_email)


if __name__ == '__main__':
    _fo_email = str(input('请输入接收通知的邮箱地址：'))
    if _fo_email.endswith('@xx.xx'):
        _url = str(input("请输入AC管理地址："))
        if _url.endswith(':xxxx'):
            main(_fo_email, _url)
        else:
            raise TypeError('输入的格式不正确')
    else:
        raise TypeError('输入的格式不正确')
