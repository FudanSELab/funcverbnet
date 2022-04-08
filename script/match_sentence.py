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
from tqdm import tqdm

from funcverbnet.data_handler.template_extractor import CustomError
from funcverbnet.data_handler.pattern_matcher import PatternMatcher
from funcverbnet.utils import load_tmp, LogsUtil

logger = LogsUtil.get_log_util()

if __name__ == '__main__':
    pattern_matcher = PatternMatcher()
    count = 0
    data = []
    with open(load_tmp('error.csv'), 'r') as f:
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
            except CustomError as ce:
                logger.info(ce, item[1])
            except Exception as e:
                logger.info(e)
            if count % 5000 == 0:
                tag = int(count / 5000)
                with open(load_tmp(f'method_desc_functionality_{tag}.json'), 'w') as json_f:
                    json.dump(data, json_f)
                data = []
        if data:
            tag = int(count / 5000) + 1
            with open(load_tmp(f'method_desc_functionality_{tag}.json'), 'w') as json_f:
                json.dump(data, json_f)
    print(count)
