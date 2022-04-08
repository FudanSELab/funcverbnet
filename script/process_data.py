#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/04/06
------------------------------------------
@Modify: 2022/04/06
------------------------------------------
@Description:
"""
import json
import csv

from funcverbnet.utils import load_tmp

if __name__ == '__main__':
    # with open(load_tmp('api_desc.json'), 'r') as f:
    #     data_list = json.load(f)
    # with open(load_tmp('api_desc.csv'), 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['id', 'full_description'])
    #     for item in data_list:
    #         writer.writerow([item['id'], item['full_description']])

    # with open(load_tmp('error.csv'), 'r') as f:
    #     f_csv = csv.reader(f)
    #     # for item in f_csv:
    #     #     print(item[0], item[1])
    #     with open(load_tmp('clean_error.csv'), 'w') as wf:
    #         writer = csv.writer(wf)
    #         writer.writerow(['id', 'full_description'])
    #         for item in f_csv:
    #             writer.writerow([int(item[0]), item[1]])

    with open(load_tmp('method_desc.csv'), 'r') as f:
        f_csv = csv.reader(f)
        next(f_csv)
        with open(load_tmp('clean_method_desc.csv'), 'w') as wf:
            writer = csv.writer(wf)
            writer.writerow(['id', 'description'])
            for item in f_csv:
                if not item[1]:
                    continue
                writer.writerow([int(item[0]), item[1]])
