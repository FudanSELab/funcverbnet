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


class CodeUtil:
    PATTERN_24 = re.compile(r'([A-Za-z])([24])([A-CE-Za-ce-z])')
    PATTERN_SPLIT = re.compile(r'([A-Z]+)([A-Z][a-z]+)')
    PATTERN_NUM = re.compile(r'([0-9]?[A-Z]+)')

    PATTERN_SENT = re.compile(r'(?<=[.!?])\s+')

    @staticmethod
    def simplify_qualified_name(qualified_name: str):
        if not qualified_name:
            return None
        unqualified_name = qualified_name.split('(')[0].split('.')[-1].strip()
        return unqualified_name

    @staticmethod
    def simplify_class_qualified_name(qualified_name: str):
        if not qualified_name:
            return None
        qualified_name = qualified_name.replace('\n', ' ')
        unqualified_name = qualified_name.strip('.').split(' ')[-1].split('(')[0].split('<')[0].split('.')
        if len(unqualified_name) > 1:
            return unqualified_name[-2].strip(), [unqualified_name[-1].strip()]
        return None, [unqualified_name[-1].strip()]

    @staticmethod
    def simplify_method_qualified_name(qualified_name: str):
        if not qualified_name:
            return None
        unqualified_name = qualified_name.strip('.').split('(')[0].split('<')[0].split(' ')[-1].split('.')
        if len(unqualified_name) > 1:
            return unqualified_name[-2].strip(), [unqualified_name[-1].strip(), unqualified_name[-1].strip() + '()']
        return None, [unqualified_name[-1].strip(), unqualified_name[-1].strip() + '()']

    @staticmethod
    def process_qualified_name(name: str):
        if not name:
            return None
        split_parentheses = name.split('(')
        qualified_name = split_parentheses[0].strip()
        unqualified_name = qualified_name.split('.')[-1].strip()
        parameters = []
        if '(' in name and '(' in name:
            parameters = split_parentheses[1].split(')')[0].strip().split(',')
        for index, parameter in enumerate(parameters):
            parameter = parameter.strip()
            if parameter:
                parameters[index] = parameter.split(' ')[0].strip()
        return qualified_name, unqualified_name, parameters

    @classmethod
    def decamelize(cls, name):
        if not name:
            return None
        name = re.sub(cls.PATTERN_24, r'\1 \2 \3', name).strip()
        name = name.replace('_', ' ')
        name = re.sub(cls.PATTERN_SPLIT, r'\1 \2', name)
        name = re.sub(cls.PATTERN_NUM, r' \1', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    @classmethod
    def decamelize_from_qualified_name(cls, qualified_name: str):
        if not qualified_name:
            return None
        return cls.decamelize(cls.simplify_qualified_name(qualified_name))

    @classmethod
    def decamelize_from_unqualified_name(cls, unqualified_name: str):
        if not unqualified_name:
            return None
        return cls.decamelize(unqualified_name)

    @classmethod
    def decamelize_by_substitute_verb(cls, parent: str, unqualified_name: str):
        if not unqualified_name:
            return None
        if unqualified_name == parent or unqualified_name[0].isupper():
            return 'create ' + cls.decamelize(unqualified_name)
        elif unqualified_name.startswith('is'):
            return cls.decamelize(unqualified_name.replace('is', 'check', 1))
        elif unqualified_name.startswith('to'):
            return cls.decamelize(unqualified_name).replace('to', 'convert to', 1)
        else:
            return cls.decamelize(unqualified_name)

    @staticmethod
    def count_parameter_num(split_code: str):
        split_code = split_code.split(')')[0]
        if '(' not in split_code.strip():
            return -1
        return 0 if split_code.strip() == '(' else len(split_code.split('(')[1].split(','))


class LogsUtil:
    __is_console = True
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
