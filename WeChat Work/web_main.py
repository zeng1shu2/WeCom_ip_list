# coding:utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configs
import time


def web_main(url):
    path = './chrome/chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path)
    # 全屏显示
    browser.maximize_window()
    browser.get(url)
    browser.implicitly_wait(60)
    # 跳过证书验证
    # browser.find_element_by_id('details-button').click()
    # browser.find_element_by_id('proceed-link').click()
    # 读取账号信息
    username = configs.ac_user_info['user']
    password = configs.ac_user_info['password']
    # 登陆账号
    browser.find_element_by_id('user').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)
    time.sleep(1)
    browser.find_element_by_class_name('button').click()
    # 加载首页检测延长时间
    WebDriverWait(browser, 30, 0.5).until(EC.presence_of_element_located((By.ID, 'ext-gen282')))
    # 设置
    browser.find_element_by_xpath('//span[contains(text(),"对象定义")]').click()
    browser.find_element_by_xpath('//a[contains(text(),"URL分类库")]').click()
    WebDriverWait(browser, 30, 1).until(lambda x: x.find_element_by_xpath('//span[contains(text(),"赌博")]'))
    # 跳转到底部
    jq = '$(".x-grid3-scroller").scrollTop(2000);'
    browser.execute_script(jq)
    # 获取微信白名单
    browser.find_element_by_xpath('//span[contains(text(),"企业微信白名单2")]').click()
    time.sleep(2)
    # 清空原有的内容
    browser.find_element_by_name('url').clear()
    time.sleep(2)
    # 读取最新的IP地址，并写入提交保存。
    file = open('ip_list.txt')
    file_ip = file.read()
    browser.find_element_by_name('url').send_keys(file_ip)
    time.sleep(2)
    browser.find_element_by_xpath('//button[contains(text(),"提交")]').click()
    time.sleep(3)
    # 刷新页面
    # browser.find_element_by_xpath('//button[@title="刷新当前页面"]').click()
    # WebDriverWait(browser, 30, 1).until(lambda x: x.find_element_by_xpath('//span[contains(text(),"赌博")]'))
    # time.sleep(2)
    # 跳转到底部
    browser.execute_script(jq)
    browser.find_element_by_xpath('//span[contains(text(),"企业微信白名单1")]').click()
    time.sleep(4)
    # 清空原有的内容
    browser.find_element_by_name("url").clear()
    time.sleep(1)
    # 读取最新的域名地址，并写入提交保存。
    file = open('domain.txt')
    file_ip = file.read()
    browser.find_element_by_name('url').send_keys(file_ip)
    time.sleep(2)
    browser.find_element_by_xpath('//button[contains(text(),"提交")]').click()
    # 刷新页面
    browser.find_element_by_xpath('//button[@title="刷新当前页面"]').click()
    WebDriverWait(browser, 30, 1).until(lambda x: x.find_element_by_xpath('//span[contains(text(),"赌博")]'))
    # 立即生效配置
    browser.find_element_by_xpath('//button[@title="立即生效配置"]').click()
    time.sleep(3)
    print('处理完成')


# if __name__ == '__main__':
#     url = 'https://172.16.100.250:25840'
#     web_main(url)