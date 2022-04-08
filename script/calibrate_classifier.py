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
import json

from funcverbnet.nodes.funcverbnet import FuncVerbNet
from funcverbnet.classifier.sentence_classifier import FuncSentenceClassifier
from funcverbnet.classifier.sentence_classifier_base_farm import SentenceClassifier
from funcverbnet.utils import load_tmp, LogsUtil

logger = LogsUtil.get_log_util()

if __name__ == '__main__':
    sent_classifier_fasttext = FuncSentenceClassifier()
    sent_classifier_bert = SentenceClassifier()
    net = FuncVerbNet()
    collect_sent = []
    with open(load_tmp("sentences.csv"), 'r') as f:
        df = pd.read_csv(f)
    for i, text in enumerate(df['single_description'][0:100]):
        try:
            cate_id, p = sent_classifier_fasttext.new_predict(text)
            result = sent_classifier_bert.predict(text)['label'].split('__label__')[1][0:-2]
            if str(cate_id) != result:
                # print(cate_id, '|', result, '|', text)
                logger.info('conflict: ' + cate_id + ' | ' + result + ' | ' + text)
            if p <= 0.8:
                cate = net.find_cate_by_id(cate_id)
                collect_sent.append({
                    'from_fasttext': net.find_cate_by_id(cate_id).name,
                    'from_bert': net.find_cate_by_id(int(result)).name,
                    'sentence': text
                })
        except Exception as e:
            logger.info('id: ' + df['id'][i] + ' | ' + text, e.__class__.__name__, e)
    with open(load_tmp('conflict_sentences.json'), 'w') as f:
        json.dump(collect_sent, f)
