#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/14
------------------------------------------
@Modify: 2022/03/14
------------------------------------------
@Description:
"""
import os
from pathlib import Path
import time
import logging
import re

ROOT_PATH = Path(os.path.abspath(os.path.dirname(__file__)))


def load_data(filename):
    return str(ROOT_PATH / 'data' / filename)


def tmp_folder():
    return str(ROOT_PATH / 'tmp')


def load_tmp(filename):
    return str(ROOT_PATH / 'tmp' / filename)


def save_logs(ml_tag=None):
    path = ROOT_PATH / 'logs'
    path.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d%H", time.localtime())
    path = path / f'mlruns_{ml_tag}_{timestamp}' if ml_tag else path / f'{timestamp}.log'
    return str(path)


def walk_dir(folder):
    for dir_path, dirs, files in os.walk(folder):
        for filename_ext in files:
            yield filename_ext


class LogsUtil:
    __is_console = False
    __log_level = logging.INFO
    __log_file = save_logs()

    __log_util = None

    def __init__(self, is_console=__is_console, log_level=__log_level, log_file=__log_file):
        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(log_level)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        if is_console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(fmt)
            stream_handler.setLevel(log_level)
            self.logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(fmt)
        file_handler.setLevel(log_level)
        self.logger.addHandler(file_handler)

    @classmethod
    def set_log_util(cls, is_console=__is_console, log_level=__log_level, log_file=__log_file):
        cls.__log_util: LogsUtil = LogsUtil(is_console=is_console, log_level=log_level, log_file=log_file)

    @classmethod
    def get_log_util(cls):
        if cls.__log_util is None:
            cls.__log_util: LogsUtil = LogsUtil()
        return cls.__log_util

    def info(self, *msgs):
        for _ in msgs:
            self.logger.info(_)
