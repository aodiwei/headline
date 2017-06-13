#!/usr/bin/env python
# coding:utf-8
"""
__title__ = ''
__author__ = 'David Ao'
__mtime__ = '2017/6/11'
# 
"""
import time
from multiprocessing import dummy

from proxy import ProxyMng


def run():
    with open('urls.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:
            url = url.strip()
            if not url:
                continue
            ProxyMng.open_url(url=url)


def wrap(i):
    # while 1:
    print('flash {}'.format(i))
    run()
    time.sleep(60 * 20)


if __name__ == '__main__':
    # pool = dummy.Pool()
    # pool.map_async(wrap, range(200))
    # pool.close()
    # pool.join()
    # run()
    map(wrap, range(300))
