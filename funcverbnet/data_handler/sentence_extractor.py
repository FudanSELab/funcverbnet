#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/11
------------------------------------------
@Modify: 2022/03/11
------------------------------------------
@Description:
"""
import spacy
from spacy.tokens import Doc, Token
import textdistance

from funcverbnet.data_handler.funcverb import FuncVerbNet
from funcverbnet.data_handler.utils import read_data


# import time


# def cal_time(func):
#     def wrapper(*args, **kwargs):
#         t1 = time.perf_counter()
#         result = func(*args, **kwargs)
#         t2 = time.perf_counter()
#         print("%s running time: %s sec." % (func.__name__, t2 - t1))
#         return result
#
#     return wrapper


class SentenceExtractor:
    def __init__(self):
        self.net = FuncVerbNet()
        self.legal_pos_s = ['NOUN', 'VERB', 'AUX', 'PROPN', 'PART', 'NUM', 'DET']
        self.illegal_dep_s = ['prep', 'acl', 'xcomp', 'pcomp', 'advcl', 'ccomp']

    def preprocess_sentence(self, sentence: str):
        """

        :param sentence:
        :return:
        """
        if not sentence:
            return None
        sentence = sentence.split(';')[0].replace('[icu]', '').replace('-', '').replace(' in to ', ' into ').strip()
        if sentence[0].isupper():
            sentence = sentence[0].lower() + sentence[1:]
        sentence = self.eliminate_bracket(sentence)
        return sentence

    @staticmethod
    def eliminate_bracket(sentence: str):
        """

        :param sentence:
        :return:
        """
        if not sentence:
            return None
        while '(' in sentence and ')' in sentence:
            l_bracket, r_bracket = sentence.find('('), sentence.find(')')
            # update l_bracket
            l_bracket += sentence[l_bracket + 1: r_bracket].rfind('(') + 1
            sentence = sentence.replace(sentence[l_bracket: r_bracket + 1], '')
        return sentence

    # @staticmethod
    # def get_doc_root(doc: Doc) -> Token:
    #     assert isinstance(doc, Doc)
    #     return [token for token in doc if token.head == token][0]

    @staticmethod
    def is_in_categories(token: Token, f_category_incl_verbs: list):
        assert isinstance(token, Token)
        if not f_category_incl_verbs:
            return False
        if token.lemma_.lower() in f_category_incl_verbs:
            return True
        for _ in f_category_incl_verbs:
            if ' ' in _:
                _ = _.split(' ')[0]
            if textdistance.hamming.distance(token.lemma_.lower(), _) < 2:
                return True
        return False

    def dependency_parser(self, doc: Doc, f_category_incl_verbs: list):
        assert isinstance(doc, Doc)
        if not f_category_incl_verbs:
            return []
        root: Token = [token for token in doc if token.head == token][0]
        if not root:
            return []
        sentence = []
        flag = False
        if root.pos_ == 'NOUN' or not self.is_in_categories(root, f_category_incl_verbs):
            root_lefts = [_ for _ in root.lefts]
            for left in root_lefts:
                if self.is_in_categories(left, f_category_incl_verbs):
                    root = left
                    flag = True
                    break
        if root.pos_ != 'VERB' and not flag:
            root_rights = [_ for _ in root.rights]
            for right in root_rights:
                if self.is_in_categories(right, f_category_incl_verbs):
                    root = right
                    break
        # if root.pos_ != 'VERB' and len(sentence) == 0:
        #     return sentence
        if root.pos_ != 'VERB':
            return []
        # >>> sentence
        sentence.append(root)
        root_rights = [_ for _ in root.rights]
        for right in root_rights:
            # print(right, right.pos_, right.dep_)
            if right.pos_ == 'PUNCT' or right.dep_ == 'punct':
                continue
            if right.dep_ in ['amod', 'conj', 'cc']:
                continue
            if right.pos_ not in ['NOUN', 'VERB', 'AUX', 'PROPN', 'PART', 'NUM', 'DET'] and right.dep_ != 'prep':
                continue
            # >>> right
            if right.dep_ == 'prep':
                if right.pos_ != 'ADP' or right.pos_ != 'SCONJ' and right.text != 'as':
                    continue
                sentence.append(right)
                sentence.extend([_ for _ in right.rights if _.pos_ != 'PUNCT' or _.dep_ != 'punct'])
            elif right.pos_ == 'DET' or right.pos_ == 'NUM':
                if right.dep_ != 'dobj':
                    continue
                tmp = [right]
                while len(tmp) > 0:
                    last = tmp.pop()
                    sentence.append(last)
                    tmp.extend([_ for _ in last.rights][::-1])
            elif right.pos_ == 'VERB' or right.pos_ == 'AUX':
                for rl in [_ for _ in right.lefts]:
                    # print(rl.pos_, rl.dep_, rl.text)
                    if rl.dep_ == 'mark':
                        sentence.append(rl)
                        break
                    if rl.pos_ == 'ADV' and rl.dep_ == 'advmod' and rl.text == 'when':
                        sentence.append(rl)
                        break
                if right.dep_ not in ['prep', 'acl', 'xcomp', 'pcomp', 'advcl', 'ccomp']:
                    sentence.append(right)
            elif right not in sentence:
                sentence.append(right)
        last = sentence[-1]
        last_lefts = [_ for _ in last.rights]
        while len(last_lefts) > 0:
            for ll in last_lefts:
                if ll.pos_ == 'PUNCT' or ll.dep_ == 'punct':
                    continue
                if 'obj' in ll.dep_ or ll.dep_ == 'cc':
                    sentence.append(ll)
                elif (ll.dep_ == 'prep' and ll.pos_ != 'VERB') or ll.dep_ == 'conj' or ll.dep_ == 'pcomp':
                    sentence.append(ll)
                    sentence.extend([_ for _ in ll.rights if _.pos_ != 'PUNCT' or _.dep_ != 'punct'])
            if last == sentence[-1]:
                last_lefts = []
            else:
                last = sentence[-1]
                last_lefts = [_ for _ in last.rights]
        return sentence

    def generate_token_pos(self, tokenized_sentence, f_category_incl_verbs: list):
        if not tokenized_sentence or not f_category_incl_verbs:
            return [], ''
        pos_list = []
        root: Token = tokenized_sentence[0]
        if not self.is_in_categories(root, f_category_incl_verbs):
            return pos_list, root.text
        flag = False
        core_verb = None
        for token in tokenized_sentence:
            pos_list.append([token, token.pos_])
            if token.pos_ == 'VERB' and not flag:
                core_verb = token.lemma_
                flag = True
        # >>> pos list
        cc_index_list = [_ for _ in range(len(pos_list)) if pos_list[_][0].dep_ == 'cc']
        cc_compound_list = []
        for index in cc_index_list:
            cc = tokenized_sentence[index]
            cc_compound = []
            for each in pos_list:
                each_rights = [_ for _ in each[0].rights]
                if cc not in each_rights:
                    continue
                cc_in_each_rights_index = each_rights.index(cc)
                if cc_in_each_rights_index == -1:
                    continue
                cc_compound.append(each[0])
                cc_compound.extend(each_rights[:cc_in_each_rights_index + 1])
                each_queue = each_rights[cc_in_each_rights_index + 1:][::-1]
                while len(each_queue) > 0:
                    child = each_queue.pop()
                    if child.dep_ == 'conj' or child in tokenized_sentence:
                        cc_compound.append(child)
                        each_queue.extend([_ for _ in child.rights][::-1])
            cc_compound_list.append(cc_compound)
        # >>> cc_compound
        new_pos_list = []
        if len(cc_compound_list) > 0:
            i, j, count = 0, 0, 0
            while i < len(pos_list) and j < len(cc_compound_list):
                token = pos_list[i]
                i += 1
                if token[0] not in cc_compound_list[j]:
                    new_pos_list.append(token)
                    continue
                count += 1
                if count == len(cc_compound_list[j]):
                    new_pos_list.append([cc_compound_list[j], 'cc_compound'])
                    j += 1
                    count = 0
        else:
            new_pos_list = pos_list
        # >>> new post list
        for i, (token, pos) in enumerate(new_pos_list):
            if pos == 'n' or pos == 'PROPN' or pos == 'PRON':
                new_pos_list[i][1] = 'NOUN'
            elif pos == 'ADP':
                new_pos_list[i][1] = 'PREP'
            elif pos == 'v':
                new_pos_list[i][1] = 'VERB'
            elif pos == 'ADJ':
                new_pos_list[i][1] = 'NOUN'
            elif pos == 'DET':
                new_pos_list[i][1] = 'NOUN'
            elif pos == 'X':
                new_pos_list[i][1] = 'NOUN'
            elif pos == 'SCONJ':
                if token.text == 'as':
                    new_pos_list[i][1] = 'PREP'
            elif pos == 'VERB':
                token_lefts = [_ for _ in token.lefts]
                for left in token_lefts:
                    if (left.pos_ == 'DET' or left.dep_ == 'det') and left.text != 'that':
                        new_pos_list[i][1] = 'NOUN'
                        break
            elif pos == 'cc_compound':
                conj_index = [_ for _ in range(len(token)) if token[_].dep_ == 'cc'][0]
                if conj_index + 1 < len(token):
                    tmp: Token = token[conj_index + 1]
                    if tmp.pos_ == 'VERB':
                        new_pos_list[i][1] = 'VERB - NOUN'
                    elif tmp.pos_ == 'ADP':
                        new_pos_list[i][1] = 'PREP - NOUN'
                    elif tmp.pos_ == 'NOUN' or tmp.pos_ == 'PROPN' or tmp.pos_ == 'PRON':
                        new_pos_list[i][1] = 'NOUN'
                    else:
                        new_pos_list[i][1] = 'NOUN'
                else:
                    new_pos_list[i][1] = 'NOUN'
            new_pos_list[i][0] = token if type(token) == list else [token]
        # >>> format pos list
        format_pos_list = []
        pre_pos = new_pos_list[0]
        pos_group = pre_pos
        for i, (token, pos) in enumerate(new_pos_list[1:]):
            if pos == pre_pos[1]:
                pos_group[0].extend(token)
                continue
            format_pos_list.append(pos_group)
            pre_pos = new_pos_list[i + 1]
            pos_group = pre_pos
        if not format_pos_list or pos_group[1] != format_pos_list[-1][1]:
            format_pos_list.append(pos_group)
        return format_pos_list, core_verb

    def structure_sentence(self, sentence, nlp, f_category_incl_verbs: list):
        if not sentence:
            return None
        doc: Doc = nlp(sentence)
        # for token in doc:
        #     print(token, token.pos_, token.dep_, type(token.norm_))
        #     for child in token.children:
        #         print(child)
        return self.generate_token_pos(self.dependency_parser(doc, f_category_incl_verbs), f_category_incl_verbs)

    @staticmethod
    def construct_template(token_pos_list: list):
        template = ''
        if not token_pos_list:
            return template
        for token, pos in token_pos_list:
            if pos == 'PREP':
                template += token[0].text + ' - '
            elif pos == 'PREP - NOUN':
                template += token[0].text + ' - NOUN'
            else:
                template += pos + ' - '
        return template[-3:] if template[-3:] == ' - ' else template

    @staticmethod
    def load_heuristic_rules(filename) -> dict:
        heuristic_rule_2_custom_patterns = {}
        if not filename:
            return heuristic_rule_2_custom_patterns
        with open(read_data(filename), 'r') as file:
            lines = file.readlines()
        for line in lines:
            line_str = line.replace('\n', '')
            category_id, word, lemma, pos = line_str.split('\t')
            category_id = int(category_id)
            if category_id not in heuristic_rule_2_custom_patterns:
                heuristic_rule_2_custom_patterns[category_id] = [{
                    "patterns": [[{'ORTH': word}]],
                    "attrs": {'LEMMA': lemma, "POS": pos, 'TAG': pos}
                }]
                continue
            heuristic_rule_2_custom_patterns[category_id].append({
                "patterns": [[{'ORTH': word}]],
                "attrs": {'LEMMA': lemma, "POS": pos, 'TAG': pos}
            })
        return heuristic_rule_2_custom_patterns

    @staticmethod
    def run_heuristic_rules(category_id, nlp, heuristic_rule_2_custom_patterns: dict):
        if not category_id:
            return None
        custom_patterns = heuristic_rule_2_custom_patterns[category_id] + heuristic_rule_2_custom_patterns[-1]
        # print('custom_patterns: ', custom_patterns)
        ruler = nlp.get_pipe('attribute_ruler')
        ruler.add_patterns(custom_patterns)
        return nlp

    def generate_single_sentence_template(self, sentence, f_category_incl_verbs: list, nlp):
        if not sentence or not f_category_incl_verbs:
            return None
        preprocessed_sentence = self.preprocess_sentence(sentence)
        token_pos_list, core_verb = self.structure_sentence(sentence, nlp, f_category_incl_verbs)
        template = self.construct_template(token_pos_list)
        return {
            'origin_sentence': sentence,
            'preprocessed_sentence': preprocessed_sentence,
            'token_pos_list': token_pos_list,
            'core_verb': core_verb,
            'template': template
        }

    def generate_sentence_template(self, sentence):
        for category_id, category_incl_verbs in self.net.iterate_category_set():
            print('-' * 80, category_id)
            hr_2_custom_patterns = self.load_heuristic_rules('new_heuristic_rules.txt')
            custom_nlp = self.run_heuristic_rules(category_id, spacy.load('en_core_web_sm'), hr_2_custom_patterns)
            template = self.generate_single_sentence_template(sentence, category_incl_verbs, custom_nlp)
            if template['token_pos_list']:
                print(template)
                pass

    @staticmethod
    def construct_of_noun_phrase(token_pos_list):
        """
        :param token_pos_list: List[Tuple[List[Token], str]]
        :return:
        """
        if not token_pos_list:
            return []
        of_index_list = []
        for i, (token, pos) in enumerate(token_pos_list):
            if pos == 'PREP' and (token[0].text == 'of' or token[0].text == 'per'):
                of_index_list.append(i)
        if not of_index_list:
            return token_pos_list
        # >>> of index list
        for of_index in of_index_list.copy():
            left = of_index - 1
            if 0 <= left < len(token_pos_list) and left not in of_index_list:
                of_index_list.append(left)
            right = of_index + 1
            if 0 <= right < len(token_pos_list) and right not in of_index_list:
                of_index_list.append(right)
        of_index_list.sort()
        # >>> split of index list
        of_indexes_list = []
        pre = 0
        for i in range(1, len(of_index_list)):
            if of_index_list[i] - of_index_list[i - 1] == 1:
                continue
            of_indexes_list.append(of_index_list[pre: i])
            pre = i
        of_indexes_list.append(of_index_list[pre:])
        # >>> construct format token pos list
        # if of_indexes_list == [[]]:
        #     return token_pos_list
        format_token_pos_list = []
        i, j = 0, 0
        while i < len(token_pos_list) and j < len(of_indexes_list):
            while i < of_indexes_list[j][0]:
                format_token_pos_list.append(token_pos_list[i])
                i += 1
            of_compound = []
            [of_compound.extend(_[0]) for _ in token_pos_list[of_indexes_list[j][0]: of_indexes_list[j][-1] + 1]]
            format_token_pos_list.append([of_compound, 'COMPOUND_NOUN'])
            i = of_indexes_list[j][-1] + 1
            j += 1
        if i < len(token_pos_list):
            format_token_pos_list.extend(token_pos_list[i:])
        return format_token_pos_list


if __name__ == '__main__':
    tse = SentenceExtractor()
    # print(tse.preprocess_sentence('R in to (1)2'))
    # print(tse.eliminate_bracket(
    #     "Version of onCreateView(String, Context, AttributeSet) that also supplies the parent that the view created view will be placed in."))
    # nlp = spacy.load('en_core_web_sm')
    c_id = 1
    custom_nlp = tse.run_heuristic_rules(c_id, spacy.load('en_core_web_sm'),
                                         tse.load_heuristic_rules('new_heuristic_rules.txt'))
    cate = tse.net.find_cate_by_id(c_id).included_verb
    # text = 'Use this function to retrieve the number of bits per pixel of an ImageFormat.'
    # text = 'Prints a string representation of this digest output stream and its associated message digest object.'
    text = "End the scope of a prefix-URI mapping."
    d = custom_nlp(tse.preprocess_sentence(text))
    token_pos_l, c_verb = tse.generate_token_pos(tse.dependency_parser(d, cate), cate)
    print(token_pos_l)
    print(tse.construct_of_noun_phrase(token_pos_l))
    # cates = [
    #     "inflate",
    #     "extend"
    # ]
    # cates = [
    #     "open",
    #     "turn on"
    # ]
    # tl = tse.dependency_parser(d, cates)
    # print(tl)
    # print(tse.generate_token_pos(tl, cates))
    # for item in tse.net.iterate_category_set():
    #     print(item)
    # hd = tse.load_heuristic_rules('new_heuristic_rules.txt')
    # print(hd)
    # print([(w.text, w.pos_, w.lemma_) for w in d])
    # tse.generate_sentence_template(text)
