#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/30
------------------------------------------
@Modify: 2022/03/30
------------------------------------------
@Description:
"""
import os
from pathlib import Path

import csv

ROOT_PATH = Path(os.path.abspath(os.path.dirname(__file__)))


def train_data_dir():
    return str(ROOT_PATH / 'data')


def save_model_dir(model_dir: str):
    return str(ROOT_PATH / 'model' / model_dir)


if __name__ == '__main__':
    headers = ['sentence', 'label']
    # with open(train_data_dir() + '/train_data.csv', 'r') as f:
    #     f_csv = csv.reader(f, delimiter='\t')
    #     # with open(train_data_dir() + '/clean_test_data.csv', 'w') as wf:
    #     #     writer = csv.writer(wf, delimiter='\t')
    #     #     writer.writerow(headers)
    #     #     for item in f_csv:
    #     #         writer.writerow(item)
    #     max_len = 0
    #     for item in f_csv:
    #         if len(item[0]) > max_len:
    #             max_len = len(item[0])
    #     print(max_len)

    # with open(train_data_dir() + '/train_data.csv', 'r') as f:
    #     f_csv = csv.reader(f, delimiter='\t')
    #     with open(train_data_dir() + '/clean_train_data.csv', 'w') as wf:
    #         writer = csv.writer(wf, delimiter='\t')
    #         count = 0
    #         pre = None
    #         for row in f_csv:
    #             if row != pre:
    #                 print(row)
    #                 writer.writerow(row)
    #                 pre = row
    #                 count = 0
    #                 continue
    #             if count == 5:
    #                 continue
    #             count += 1
    #             pre = row
    #             print(row)
    #             writer.writerow(row)

    # count_list = [10 for _ in range(89)]
    # with open(train_data_dir() + '/clean_train_data.csv', 'r') as f:
    #     next(f)
    #     f_csv = csv.reader(f, delimiter='\t')
    #     with open(train_data_dir() + '/test.csv', 'w') as wf:
    #         writer = csv.writer(wf, delimiter='\t')
    #         writer.writerow(headers)
    #         for (text, label) in f_csv:
    #             i = int(label[9:])
    #             if i == -1:
    #                 i += 1
    #             if count_list[i] > 0:
    #                 print(text, label)
    #                 writer.writerow([text, label])
    #                 count_list[i] -= 1
