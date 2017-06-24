#!/usr/bin/env python
# coding:utf-8
"""
__title__ = ''
__author__ = 'David Ao'
__mtime__ = '2017/6/11'
# 
"""
import time
import random
from multiprocessing import dummy
import requests

from logger_mgr import Logger

Logger.initialize('line', filePath='/', withConsole=True, level='INFO')
log = Logger.getInstance()

from proxy import ProxyMng


def run():
    with open('urls.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:
            url = url.strip()
            if not url:
                continue
            # sl = random.randint(0, 3)
            # log.info('open sleep {}'.format(sl))
            # time.sleep(sl)
            ProxyMng.open_url(url=url)


def wrap(i):
    # while 1:
    log.info('flash {}'.format(i))
    run()
    sl = random.randint(1, 3)
    log.info('loop sleep {}'.format(sl))
    time.sleep(sl)

def parse_content(content):
    pass


if __name__ == '__main__':
    # pool = dummy.Pool()
    # pool.map_async(wrap, range(200))
    # pool.close()
    # pool.join()
    # run()
    for i in range(3000):
        wrap(i)
