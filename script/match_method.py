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
import json
import csv
import re
import pandas as pd
from tqdm import tqdm
from funcverbnet.utils import load_tmp, CodeUtil

from funcverbnet.classifier.sentence_classifier import FuncSentenceClassifier
from funcverbnet.nodes.funcverbnet import FuncVerbNet


# from funcverbnet.data_handler.pattern_matcher import PatternMatcher


def load_jl(jl_file_path):
    data_list = []
    with open(jl_file_path) as file:
        line = file.readline()
        while line != "":
            data_list.append(json.loads(line))
            line = file.readline()
    return data_list


if __name__ == '__main__':
    classifier = FuncSentenceClassifier()
    net = FuncVerbNet()
    # pattern_matcher = PatternMatcher()
    # reader = pd.read_csv(load_tmp('method_qualified_name_data.csv'), iterator=True, chunksize=1000)
    # for chunk in tqdm(reader):
    #     for index, row in chunk.iterrows():
    #         # try:
    #         #     data = pattern_matcher.mapping_template_from_qualified_name(row[1])
    #         #     print(data)
    #         # except Exception as e:
    #         #     # print(e, traceback.print_exc())
    #         #     print(e.__class__.__name__, row[1])
    #         data = pattern_matcher.mapping_template_from_qualified_name(row[1])
    #         # print(data)

    data = load_jl(load_tmp('node_info_2.jl'))

    # for item in data:
    #     print(json.dumps(item, indent=4))
    #     for relation in item['relation_end_node_info_list']:
    #         if 'has_functionality' not in relation['relation_name']:
    #             continue
    #         sentence = relation['end_node_info']['sentence']
    #         sentence = re.compile(r'<[^>]*>|\([^\)]*\)|\[[^\]]*\]|\{[^\}]*\}', re.S).sub('', sentence)
    #         print(relation['end_node_info']['sentence'])
    #         cate_id = classifier.predict(sentence)
    #         print(relation['end_node_info']['category_id'], relation['end_node_info']['category'], cate_id)

    for item in data:
        # print(json.dumps(item, indent=4))
        if not item:
            continue
        for relation in item['relations']:
            if 'functionality' not in relation['relation_name']:
                continue
            # print(json.dumps(relation, indent=4))
            if not relation['relation_node']:
                continue
            if 'sentence' not in relation['relation_node']['node_info']:
                continue
            # print(json.dumps(relation['relation_node'], indent=4))
            node_info = relation['relation_node']['node_info']
            sentence = node_info['sentence']
            sentence = re.compile(r'<[^>]*>|\([^\)]*\)|\[[^\]]*\]|\{[^\}]*\}', re.S).sub('', sentence)
            # cate_id = classifier.predict(sentence)
            # cate = net.find_f_category_by_id(cate_id).name
            # print(sentence, node_info['category_id'], node_info['category'], '#', cate_id, cate)
            for sub_relation in relation['relation_node']['relations']:
                if 'functionality' not in sub_relation['relation_name']:
                    continue
                print(sub_relation['relation_node'])

    # sent_set = set()
    # with open(load_tmp('node.csv'), 'w') as wf:
    #     writer = csv.writer(wf)
    #     writer.writerow(['sentence', 'label'])
    #     for item in data:
    #         # print(json.dumps(item, indent=4))
    #         for relation in item['relation_end_node_info_list']:
    #             if 'has_functionality' not in relation['relation_name']:
    #                 continue
    #             sentence = relation['end_node_info']['sentence']
    #             sentence = re.compile(r'<[^>]*>|\([^\)]*\)|\[[^\]]*\]|\{[^\}]*\}', re.S).sub('', sentence)
    #             if sentence in sent_set:
    #                 continue
    #             # print(relation['end_node_info']['sentence'])
    #             # print(relation['end_node_info']['category_id'], relation['end_node_info']['category'])
    #             writer.writerow([sentence, relation['end_node_info']['category_id']])
    #             sent_set.add(sentence)

    # with open(load_tmp('new_train_data.csv'), 'w') as wf:
    #     writer = csv.writer(wf, delimiter='\t')
    #     with open(load_tmp('final_train_data.csv'), 'r') as rf:
    #         reader = csv.reader(rf, delimiter='\t')
    #         for row in reader:
    #             writer.writerow([row[0], row[1]])
    #     with open(load_tmp('node_train_data.csv'), 'r') as rf:
    #         reader = csv.reader(rf)
    #         for row in reader:
    #             writer.writerow([row[0], '__label__' + row[1]])
    # print(classifier.predict('get URI'))
    # print(pattern_matcher.mapping_template_from_qualified_name('setName'))
