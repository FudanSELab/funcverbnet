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
import pandas as pd
from tqdm import tqdm

from funcverbnet.utils import load_tmp


def count_csv(filename):
    with open(load_tmp(f'{filename}.csv'), 'r') as rf:
        print(len(rf.readlines()))


def clean_csv(filename):
    with open(load_tmp(f'{filename}.csv'), 'r') as rf:
        reader = csv.reader(rf)
        next(reader)
        with open(load_tmp(f'clean{filename}.csv'), 'w') as wf:
            writer = csv.writer(wf)
            writer.writerow(['id', 'description'])
            for row in reader:
                if not row[1]:
                    continue
                writer.writerow([int(row[0]), row[1]])


def eliminate_csv(filename, chunksize=10000):
    reader = pd.read_csv(load_tmp(f'clean_{filename}.csv'), iterator=True, chunksize=chunksize)
    count = 0
    with open(load_tmp(f'eliminate_{filename}.csv'), 'w') as wf:
        writer = csv.writer(wf)
        writer.writerow(['id', 'description'])
    for chunk in reader:
        count += len(chunk)
        with open(load_tmp(f'eliminate_{filename}.csv'), 'a') as wf:
            writer = csv.writer(wf)
            pre_text = None
            for index, row in chunk.iterrows():
                if row[1] == pre_text:
                    continue
                pre_text = row[1]
                writer.writerow([row[0], row[1]])
    print(count)


def combine_json(filename, sun):
    data = []
    count = 0
    for tag in tqdm(range(1, sun + 1)):
        try:
            with open(load_tmp(f'{filename}_functionality_2,{tag}.json'), 'r') as file:
                tmp = json.load(file)
                data.extend(tmp)
                count += len(tmp)
        except FileNotFoundError as e:
            print(e)
    with open(load_tmp(f'{filename}_functionality_2.json'), 'w') as file:
        json.dump(data, file)
    print(count)


if __name__ == '__main__':
    # count_csv('method_desc')
    # clean_csv('method_desc')
    # count_csv('clean_method_desc')
    # eliminate_csv('method_desc')
    # count_csv('eliminate_method_desc')
    combine_json('method_desc', 71)
