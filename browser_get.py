#!/usr/bin/env python
# coding:utf-8
"""
__title__ = ''
__author__ = 'David Ao'
__mtime__ = '2017/6/24'
# sudo apt-get install libfontconfig 在linux上先安装这个包
"""

from selenium import webdriver
import time
import random

from selenium.webdriver.common.proxy import ProxyType
from logger_mgr import Logger
Logger.initialize('line', filePath='/', withConsole=True, level='INFO')
log = Logger.getInstance()

# browser_path = r"D:\DownLoad\phantomjs-2.1.1-windows\bin\phantomjs.exe"
browser_path = r'/opt/src/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
}

headers2 = {
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}

headers_list = [headers1, headers2]


def browser_get(url, http_proxy):
    count = len(headers_list)
    index = random.randint(0, count - 1)
    headers = headers_list[index]
    for key, value in headers.items():
        if key != 'User-Agent':
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = headers['User-Agent']

    driver = webdriver.PhantomJS(executable_path=browser_path)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)

    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = http_proxy
    # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    log.info('starting open {}'.format(url))
    driver.get(url)
    # log.info('0: {}'.format(url))
    log.info('1: {}'.format(driver.session_id))
    # log.info('2: {}'.format(driver.page_source))
    print('2:', driver.page_source)
    # log.info('3: ', driver.get_cookies())

# url = r'http://www.toutiao.com/i6432649786859454978/'
# for i in range(20):
#     s = random.randint(1, 4)
#     browser_get(url, '113.245.184.227:8081')
#     time.sleep(s)
#     print(i, s)
