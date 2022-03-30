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
import os
from funcverbnet.classifier.sentence_classifier_base_farm import SentenceClassifier
from funcverbnet.utils import LogsUtil

if __name__ == '__main__':
    cuda_visible = input('CUDA_VISIBLE: ')
    os.environ['CUDA_VISIBLE_DEVICES'] = cuda_visible
    LogsUtil()
    sentence_classifier = SentenceClassifier()
    sentence_classifier.train()
