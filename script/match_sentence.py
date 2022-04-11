#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/04/07
------------------------------------------
@Modify: 2022/04/07
------------------------------------------
@Description:
"""
import csv
import json
import pandas as pd
from tqdm import tqdm

from funcverbnet.data_handler.template_extractor import CustomError
from funcverbnet.data_handler.pattern_matcher import PatternMatcher
from funcverbnet.utils import load_tmp, LogsUtil

logger = LogsUtil.get_log_util()


def run1(filename):
    pattern_matcher = PatternMatcher()
    count = 0
    data = []
    with open(load_tmp(f'clean_{filename}.csv'), 'r') as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for item in tqdm(f_csv):
            try:
                mapped_template = pattern_matcher.mapping_template(item[1])
                if mapped_template:
                    data.append({
                        'id': item[0],
                        'functionality': mapped_template
                    })
                    count += 1
                if count % 5000 != 0:
                    continue
                tag = int(count / 5000)
                with open(load_tmp(f'{filename}_functionality_{tag}.json'), 'w') as json_f:
                    json.dump(data, json_f)
                data = []
            except CustomError as ce:
                logger.info(ce, item[1])
            except Exception as e:
                logger.info(e)
    if count % 5000 != 0:
        tag = int(count / 5000) + 1
        with open(load_tmp(f'{filename}_functionality_{tag}.json'), 'w') as json_f:
            json.dump(data, json_f)
    print(count)


def run2(filename, chunksize):
    pattern_matcher = PatternMatcher()
    reader = pd.read_csv(load_tmp(f'eliminate_{filename}.csv'), iterator=True, chunksize=chunksize)
    count = 0
    tag = 0
    for chunk in reader:
        count += len(chunk)
        data = []
        print(f'processing {count} rows now')
        for index, row in tqdm(chunk.iterrows()):
            try:
                mapped_template = pattern_matcher.mapping_template(row[1])
                if not mapped_template:
                    continue
                data.append({
                    'id': row[0],
                    'functionality': mapped_template
                })
            except CustomError as ce:
                logger.info(ce, row[1])
            except Exception as e:
                logger.info(e)
        print(f'already processed {count} rows')
        tag += 1
        with open(load_tmp(f'{filename}_functionality_1,{tag}.json'), 'w') as json_f:
            json.dump(data, json_f)


if __name__ == '__main__':
    run2('method_desc', 10000)
