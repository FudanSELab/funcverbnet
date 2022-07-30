#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/07/28
------------------------------------------
@Modify: 2022/07/28
------------------------------------------
@Description:
"""
import json
import re
from funcverbnet.utils import load_tmp

from funcverbnet.data_handler.concept_extractor import ConceptExtractor


def load_jl(jl_file_path):
    data_list = []
    with open(jl_file_path) as file:
        line = file.readline()
        while line != "":
            data_list.append(json.loads(line))
            line = file.readline()
    return data_list


if __name__ == '__main__':
    concept_extractor = ConceptExtractor()
    data = load_jl(load_tmp('node_info_2.jl'))

    for item in data:
        # print(json.dumps(item, indent=4))
        if not item:
            continue
        for relation in item['relations']:
            # if 'return_value' not in relation['relation_name']:
            #     continue
            if 'has_parameter' not in relation['relation_name']:
                continue
            if not relation['relation_node']:
                continue
            if 'description' not in relation['relation_node']['node_info']:
                continue
            # print(json.dumps(relation['relation_node'], indent=4))
            node_info = relation['relation_node']['node_info']
            sentence = node_info['description']
            sentence = re.compile(r'<[^>]*>|\([^\)]*\)|\[[^\]]*\]|\{[^\}]*\}', re.S).sub('', sentence)
            print(json.dumps(sentence), concept_extractor.extract_noun_chunks(sentence))
            # for sub_relation in relation['relation_node']['relations']:
            #     if 'functionality' not in sub_relation['relation_name']:
            #         continue
            #     print(sub_relation['relation_node'])

    # text = 'the returned logger will be named after clazz'
    # text = 'A key string.'
    # text = 'key to store in the multimap.'
    # text = 'either an absolute or relative URI'
    # text = 'the second argument'
    # text = 'root of a tree of s'
    # text = 'The object to append. It can be null, or a Boolean, Number,\n  String, JSONObject, or JSONArray, or an object that implements JSONString.'
    # text = 'the element that needs to be added to the array.'
    # text = 'the '
    # text = 'A long.'
    # text = 'One of the LOG_LEVEL_XXX constants defining the log level'
    # text = 'name of the member that is being requested.'
    # text = 'the index of the element that is being sought.'
    # text = 'the String to check, may be null'
    # print(concept_extractor.extract_noun_chunks(text))
