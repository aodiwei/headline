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

import requests
from bs4 import BeautifulSoup


class ProxyMng:
    """
    some proxy function
    """
    __ip_port_list = None
    __proxy_openers = None
    @classmethod
    def get_proxy_id_list(cls):
        ip_port_list = []
        try:
            req = requests.get("http://www.proxynova.com/proxy-server-list", timeout=10)
            context = req.text
            soup = BeautifulSoup(context, "html5lib")
            main = soup.find("table", id="tbl_proxy_list")
            if main:
                ip_list = main.find_all("span", class_="row_proxy_ip")
                for x, ip_ele in enumerate(ip_list):
                    try:
                        parent = ip_ele.parent.parent
                        if parent:
                            # get the best status ip
                            status = parent.find("span", text=re.compile(r"%"))
                            status_value = status.text.encode().strip("%")
                            if int(status_value) < 70:
                                continue
                            speed_ele = parent.find("div", class_="progress-bar")
                            speed = 0
                            if speed_ele:
                                speed = speed_ele["data-value"].encode("utf-8")
                            if float(speed) > 80:
                                ip = ip_ele.text.encode()
                                port = ip_ele.find_next().text.strip().encode()
                                ip_port_list.append((ip, port))
                    except Exception as e:
                        pass
        except Exception as e:
            print("proxy website had exception")

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
            print("proxy website had exception")
            # default
            cls.get_proxy_id_list()
        return ip_port_list

    @classmethod
    def get_random_pro_id(cls):
        """
        get random proxy id
        :return:
        """
        if not cls.__ip_port_list:
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
                    print("del proxy %s %s" % (proxies, index))
                    flag_reget = True
                    if cls.__ip_port_list:
                        cls.__ip_port_list.pop(index)

                if flag_reget:  # re get opener
                    proxies, index = cls.get_random_pro_id()
                    flag_reget = False
                if proxies:
                    req = requests.get(url, timeout=timeout, proxies=proxies)
                else:
                    req = requests.get(url, timeout=timeout)

                if req.status_code == 200:
                    context = req.text.encode("utf-8")
                    break
                else:
                    retry += 1
            except Exception as e:
                retry += 1
                print(e)
        print('open url:{}'.format(url))
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