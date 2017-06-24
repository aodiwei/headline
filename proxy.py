#!/usr/bin/env python
# coding:utf-8
"""
__title__ = ''
__author__ = 'AO.Diwei'
__mtime__ = '2016/1/7'
# some common function
"""

import random
import re

import js2py
import requests
from bs4 import BeautifulSoup
from browser_get import browser_get

from logger_mgr import Logger

log = Logger.getInstance()

class ProxyMng:
    """
    some proxy function
    """
    __ip_port_list = None
    __proxy_openers = None

    @classmethod
    def get_proxy_id_list(cls):
        ip_port_list = []
        # ip_port_list = [('113.245.184.227', '8081'), ('111.62.251.25', '8088'), ('180.110.4.141', '808'), ('111.22.86.134', '8081'), ('60.167.133.69', '808'), ('36.97.145.29', '9797'), ('221.237.154.57', '9797'), ('203.91.121.76', '3128'), ('210.29.26.250', '80'), ('183.222.102.96', '8080'), ('103.76.50.181', '8080'), ('183.222.102.98', '8080'), ('124.42.7.103', '80'), ('113.204.176.96', '8998'), ('123.7.82.20', '3128'), ('119.57.105.198', '8080'), ('117.135.251.209', '80'), ('112.238.191.85', '8888'), ('123.139.56.238', '9999'), ('117.143.109.164', '80'), ('121.248.112.20', '3128'), ('175.155.24.40', '808'), ('118.180.49.24', '8080'), ('117.143.109.141', '80'), ('58.62.207.54', '9999'), ('61.160.233.8', '8080'), ('218.86.128.25', '8118'), ('103.85.162.74', '8080'), ('183.222.102.106', '8080'), ('113.17.171.139', '8080'), ('119.57.105.235', '8080'), ('117.158.1.210', '9797'), ('123.206.184.186', '8088'), ('123.170.255.20', '808'), ('103.227.76.30', '8090')]
        # return ip_port_list
        try:
            req = requests.get("https://www.proxynova.com/proxy-server-list/country-cn/", timeout=10)
            context = req.text
            soup = BeautifulSoup(context, "html.parser")
            main = soup.find("table", id="tbl_proxy_list")
            # js = main.find_all('script')
            # ips = [js2py.eval_js(j.text.replace('document.write', '')) for j in js if 'substr' in j.text]
            if main:
                ip_list = main.contents[3].find_all("tr")
                for _, ip_ele in enumerate(ip_list):
                    js = ip_ele.find('script')
                    if not js:
                        continue
                    ip_js = js.text
                    if 'substr' not in ip_js:
                        continue
                    ip = js2py.eval_js(ip_js.replace('document.write', ''))
                    port = ip_ele.contents[3].text.strip()
                    ip_port_list.append((ip, port))
        except Exception as e:
            print("proxy website had exception", e)

        log.info('proxy hosts {}'.format(ip_port_list))
        return ip_port_list

    @classmethod
    def get_proxy_id_list_us(cls):
        ip_port_list = []
        try:
            req = requests.get("https://www.us-proxy.org", timeout=20)
            context = req.text
            soup = BeautifulSoup(context, "html.parser")
            main = soup.find("table", id="proxylisttable")
            if main:
                ip_list = main.contents[1].find_all("tr")
                for _, ip_ele in enumerate(ip_list):
                    ip, port = ip_ele.contents[0].text, ip_ele.contents[1].text
                    ip_port_list.append((ip, port))
        except Exception as e:
            print("proxy website had exception", e)
            # default
            cls.get_proxy_id_list()
        return ip_port_list

    @classmethod
    def get_random_pro_id(cls):
        """
        get random proxy id
        :return:
        """
        if not cls.__ip_port_list or len(cls.__ip_port_list) <= 10:
            cls.__ip_port_list = cls.get_proxy_id_list()

        if cls.__ip_port_list:
            index = random.randint(0, len(cls.__ip_port_list) - 1)
            ip_port = cls.__ip_port_list[index]
            proxy_host = {"http": "%s:%s" % (ip_port[0], ip_port[1])}
            return proxy_host, index

    @classmethod
    def open_url(cls, url, timeout=20):
        """
        open url use request lib
        :param url:
        :param timeout:
        :return:
        """
        context = ""
        retry = 0
        flag_reget = True
        proxies, index = "", 0
        error_msg = "out of range of retry connection"
        while 1:
            # if retry > 4:  # retry url
            # raise ValueError(error_msg)
            try:
                # when retry a opener 2 times and it still unavailable, then remove it
                if retry > 0:
                    log.info("del proxy %s %s" % (proxies, index))
                    flag_reget = True
                    if cls.__ip_port_list:
                        cls.__ip_port_list.pop(index)

                if flag_reget:  # re get opener
                    proxies, index = cls.get_random_pro_id()
                    flag_reget = False
                if proxies:
                    browser_get(url, http_proxy=proxies['http'])
                    # req = requests.get(url, timeout=timeout, proxies=proxies)
                    break
                else:
                    req = requests.get(url, timeout=timeout)
                #
                # if req.status_code == 200:
                #     # context = req.text.encode("utf-8")
                #     break
                # else:
                #     retry += 1
            except Exception as e:
                retry += 1
                print(e)
        # log.info('open url:{}'.format(url))
        return context

    @classmethod
    def get_newest_proxy_ip_list(cls):
        ProxyMng.__ip_port_list = ProxyMng.get_proxy_id_list()
        ProxyMng.__proxy_openers = None
        return "run"


if __name__ == '__main__':
    pro = ProxyMng()
    # pro.get_proxy_id_list()
    pro.open_url('http://www.toutiao.com/i6429289350877413890/')
