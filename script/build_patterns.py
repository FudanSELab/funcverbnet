#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/04/28
------------------------------------------
@Modify: 2022/04/28
------------------------------------------
@Description:
"""
import json
import pickle
import re
from funcverbnet.utils import load_data
from funcverbnet.nodes.funcverbnet import FuncVerbNet

F_CATEGORY_DATA_PATH = load_data("f_category.json")
PATTERN_DATA_PATH = load_data("patterns.json")

if __name__ == '__main__':
    # with open(F_CATEGORY_DATA_PATH, 'r', encoding='utf-8') as f_category_data_file:
    #     category_data = json.load(f_category_data_file)
    # f_patterns = set()
    # patterns = set()
    # for item in category_data:
    #     # print(item['included_pattern'])
    #     for pattern in item['included_pattern']:
    #         f_patterns.add(pattern)

    # patterns = dict()
    # with open(PATTERN_DATA_PATH, 'r', encoding='utf-8') as pattern_file:
    #     pattern_data = json.load(pattern_file)
    # for item in pattern_data:
    #     patterns[item['syntax']] = item['id']

    # print(f_patterns - patterns)

    # add = []
    # index = 523
    # for item in f_patterns - patterns:
    #     index += 1
    #     add.append({
    #         "id": index,
    #         "syntax": item,
    #         "example": "null",
    #         "description": "null",
    #         "included_roles": re.compile(r'\{(.*?)\}').findall(item),
    #         "create_time": "2022-04-28 23:30:12",
    #         "version": "1.0"
    #     })
    # print(json.dumps(add))

    # with open(load_data('patterns.bin'), 'wb') as wf:
    #     pickle.dump(patterns, wf)
    #
    # with open(load_data('patterns.bin'), 'rb') as rf:
    #     print(pickle.load(rf))

    net = FuncVerbNet()
    print(net.get_pattern_id_by_syntax('V {patient} with {instrument}'))
