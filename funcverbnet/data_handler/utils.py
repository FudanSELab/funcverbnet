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

ROOT_PATH = Path(os.path.abspath(os.path.dirname(__file__)))


def read_data(filename):
    return str(ROOT_PATH / "data" / filename)

# if __name__ == '__main__':
#     with open(read_data('heuristic_rules.txt'), 'r') as file:
#         lines = file.readlines()
#     # print(type(lines))
#     # for i in range(1, len(lines)):
#     #     print(lines[i].split('\t')[0])
#     sort_lines = lines[1:]
#     g = lambda x: int(x.split('\t')[0])
#     sort_lines.sort(key=g)
#     lines[1:] = sort_lines
#     with open(read_data('new_heuristic_rules.txt'), 'w') as file:
#         lines = file.writelines(lines)
