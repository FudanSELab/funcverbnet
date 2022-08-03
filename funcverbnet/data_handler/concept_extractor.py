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
import re
import spacy
from spacy.tokens import Doc
from funcverbnet.utils import load_data


class ConceptExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def preprocess_sentence(sentence: str) -> str:
        if not sentence:
            return sentence
        sentence = sentence.replace('\n', '').replace('-', '').strip()
        if sentence[0].isupper():
            sentence = sentence[0].lower() + sentence[1:]
        sentence = re.sub(' +', " ", sentence)
        sentence = re.compile(r'<[^>]*>|\([^\)]*\)|\[[^\]]*\]|\{[^\}]*\}', re.S).sub('', sentence)
        return sentence

    def extract_noun_chunks(self, sentence):
        sentence = self.preprocess_sentence(sentence)
        doc: Doc = self.nlp(sentence)
        noun_chunks = set()
        for chunk in doc.noun_chunks:
            # print(chunk.text, '-', chunk.root.text, '-', chunk.root.dep_, '-', chunk.root.pos_)
            noun_chunk_tokens = []
            if chunk.root == chunk.root.head:
                if chunk.root.lefts:
                    # print([(_.text, _.pos_) for _ in chunk.root.lefts])
                    for token in [_ for _ in chunk.root.lefts] + [chunk.root]:
                        if token.pos_ in ['DET']:
                            continue
                        if token.pos_ in ['CCONJ', 'PUNCT', 'PRON']:
                            if noun_chunk_tokens:
                                noun_chunks.add(' '.join([_.lemma_ for _ in noun_chunk_tokens]))
                            noun_chunk_tokens = []
                            continue
                        noun_chunk_tokens.append(token)
                    if noun_chunk_tokens:
                        noun_chunks.add(' '.join([_.lemma_ for _ in noun_chunk_tokens]))
                else:
                    noun_chunks.add(chunk.text)
                continue
            # print([(_.text, _.pos_) for _ in doc[chunk.start:chunk.end]])
            for token in doc[chunk.start:chunk.end]:
                if token.pos_ in ['DET']:
                    continue
                if token.pos_ in ['CCONJ', 'PUNCT', 'PRON', 'ADP']:
                    if noun_chunk_tokens:
                        noun_chunks.add(' '.join([_.lemma_ for _ in noun_chunk_tokens]))
                    noun_chunk_tokens = []
                    continue
                noun_chunk_tokens.append(token)
            if noun_chunk_tokens:
                noun_chunks.add(' '.join([_.lemma_ for _ in noun_chunk_tokens]))
        return set([_.lower() for _ in noun_chunks])
