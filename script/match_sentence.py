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
import pandas as pd
from funcverbnet.data_handler.template_extractor import CustomError
from funcverbnet.data_handler.pattern_matcher import PatternMatcher
from funcverbnet.utils import load_tmp, LogsUtil

logger = LogsUtil.get_log_util()

if __name__ == '__main__':
    pattern_matcher = PatternMatcher()
    with open(load_tmp("error.csv"), 'r') as f:
        df = pd.read_csv(f)
    for i, text in enumerate(df['full_description'][1:]):
        try:
            mapped_template = pattern_matcher.mapping_template(text)
            if mapped_template:
                print(mapped_template)
        except CustomError as ce:
            logger.info(ce, text)
        except Exception as e:
            logger.info(e)
