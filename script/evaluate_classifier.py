#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/31
------------------------------------------
@Modify: 2022/03/31
------------------------------------------
@Description:
"""
import os
from funcverbnet.classifier.sentence_classifier_base_farm import SentenceClassifier

if __name__ == '__main__':
    # cuda_visible = input('CUDA_VISIBLE: ')
    # os.environ['CUDA_VISIBLE_DEVICES'] = cuda_visible
    sentence_classifier = SentenceClassifier()
    sentence_classifier.evaluate('test_data.csv')
