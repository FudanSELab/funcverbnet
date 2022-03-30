#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/29
------------------------------------------
@Modify: 2022/03/29
------------------------------------------
@Description:
"""
import pandas as pd

from funcverbnet.nodes.funcverbnet import FuncVerbNet
from funcverbnet.classifier.sentence_classifier import FuncSentenceClassifier
from funcverbnet.utils import load_pdata

if __name__ == '__main__':
    # sent_classifier = FuncSentenceClassifier()
    # net = FuncVerbNet()
    # with open(load_pdata("sentences.csv"), 'r') as f:
    #     df = pd.read_csv(f)
    # for i, text in enumerate(df['single_description']):
    #     try:
    #         cate_id, p = sent_classifier.new_predict(text)
    #         if p <= 0.6:
    #             cate = net.find_cate_by_id(cate_id)
    #             print(cate.name, ':', text, p)
    #     except Exception as e:
    #         print(df['id'][i], text)
    #         print(e, e.__class__.__name__)
    label = ['__label__-1'] + ['__label__' + str(_) for _ in range(1, 89)]
    print(label)
