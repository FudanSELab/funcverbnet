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
import json
import os
import csv
import random

import pandas as pd
# from funcverbnet.classifier.sentence_classifier_base_farm import SentenceClassifier
from funcverbnet.nodes.funcverbnet import FuncVerbNet, FuncCategory
from funcverbnet.utils import load_tmp

if __name__ == '__main__':
    # cuda_visible = input('CUDA_VISIBLE: ')
    # os.environ['CUDA_VISIBLE_DEVICES'] = cuda_visible
    # sentence_classifier = SentenceClassifier()
    # sentence_classifier.train()
    net = FuncVerbNet()
    cate_map = {}
    for index in range(1, 89):
        cate: FuncCategory = net.find_f_category_by_id(index)
        for verb in cate.included_verb:
            cate_map.setdefault(index, {})[verb] = 0
    with open(load_tmp('new_train_data.csv'), 'r') as rf:
        reader = csv.reader(rf, delimiter='\t')
        for row in reader:
            cate_id = int(row[1][9:])
            if cate_id == -1:
                continue
            for verb in cate_map[cate_id].keys():
                if verb in row[0]:
                    cate_map[cate_id][verb] += 1
    data = []
    for cate_id, cate in cate_map.items():
        desc_reader = pd.read_csv(load_tmp(f'eliminate_method_desc.csv'), iterator=True, chunksize=10000)
        filter_cate = dict(filter(lambda x: x[1] <= 2, cate.items()))
        if not filter_cate:
            continue
        print(cate_id, filter_cate)
        sentence_dic = {}
        for find_cate in filter_cate.keys():
            print('    ' + find_cate)
        # for chunk in desc_reader:
        #     for index, row in chunk.iterrows():
        #         for find_cate in filter_cate.keys():
        #             if find_cate in row[1].lower():
        #                 sentence_dic.setdefault(find_cate, []).append(row[1])
        # for k, v in sentence_dic.items():
        #     if len(v) > 5:
        #         sentence_dic[k] = random.sample(v, 5)
        # data.append(sentence_dic)
    # with open(load_tmp('random_desc_data.json'), 'w') as file:
    #     json.dump(data, file)
