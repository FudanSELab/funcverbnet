#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/06/16
------------------------------------------
@Modify: 2022/06/16
------------------------------------------
@Description:
"""
import pandas as pd
from tqdm import tqdm
from funcverbnet.utils import load_tmp
from funcverbnet.data_handler.pattern_matcher import PatternMatcher

if __name__ == '__main__':
    pattern_matcher = PatternMatcher()
    reader = pd.read_csv(load_tmp('method_qualified_name_data.csv'), iterator=True, chunksize=1000)
    for chunk in tqdm(reader):
        for index, row in chunk.iterrows():
            try:
                data = pattern_matcher.mapping_template_from_qualified_name(row[1])
                print(data)
            except Exception as e:
                # print(e, traceback.print_exc())
                print(e.__class__.__name__, row[1])
