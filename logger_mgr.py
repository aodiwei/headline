#!/usr/bin/env python3
# coding:utf-8
"""
__title__ = ''
__author__ = 'David Ao'
__mtime__ = '2017/5/19'
#
"""

import os
import sys
import logging
import logging.handlers
import re

import pprint


class UninitializedError(Exception):
    pass


class Logger(object):
    __inited = False
    __inst = None

    __fileHandler = None

    @classmethod
    def initialize(cls, name, filePath=None, withConsole=True, level=logging.INFO):
        if Logger.__inited:
            return
        Logger.__inst = logging.getLogger(name)
        Logger.__inst.setLevel(level)

        logFile = "%s.log" % name
        if filePath:
            if not os.path.exists(filePath):
                os.mkdir(filePath)
            logFile = '%s/%s' % (filePath, logFile)
        Logger.__fileHandler = logging.handlers.TimedRotatingFileHandler(filename=logFile, when="D", interval=1, backupCount=5)
        Logger.__fileHandler.suffix = "%Y%m%d_%H%M"
        Logger.__fileHandler.extMatch = re.compile(r"^\d{4}\d{2}\d{2}_\d{2}\d{2}$")
        # Logger.__fileHandler = logging.handlers.RotatingFileHandler(logFile, 'a', 1024 * 1024 * 10, 10)
        fmt = logging.Formatter("%(asctime)s %(levelname)-5s[%(filename)s:%(lineno)s-%(funcName)s-%(threadName)s]:%(message)s")
        Logger.__fileHandler.setFormatter(fmt)
        Logger.__inst.addHandler(Logger.__fileHandler)
        if withConsole:
            consoleHandler = logging.StreamHandler(sys.stdout)
            consoleHandler.setFormatter(fmt)
            Logger.__inst.addHandler(consoleHandler)
        Logger.__inited = True

    @classmethod
    def getInstance(cls):
        if not Logger.__inited:
            raise UninitializedError()
        return Logger.__inst
