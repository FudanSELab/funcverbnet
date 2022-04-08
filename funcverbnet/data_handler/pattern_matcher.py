#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/23
------------------------------------------
@Modify: 2022/03/23
------------------------------------------
@Description:
"""
import re
import pandas as pd

from funcverbnet.nodes.funcverbnet import FuncVerbNet
from funcverbnet.data_handler.template_extractor import TemplateExtractor
from funcverbnet.utils import CustomError

from funcverbnet.utils import load_tmp

SPLIT_STR = ' - '


class TSlot:
    def __init__(
        self,
        slot_str: str,
        tokens: list,
        priority: int,
    ):
        self.slot_str = slot_str
        self.tokens = [_.text for _ in tokens]
        self.priority = priority

    def __str__(self):
        return '<TSlot %s>' % self.slot_str


class PSlot:
    def __init__(
        self,
        slot_str: str,
        role: str,
        preps: set,
        semantic: str,
    ):
        if not semantic:
            semantic = '.predicate' if role == 'V' else '.patient'
        self.slot_str = slot_str
        self.role = role
        self.preps = preps
        self.semantic = semantic

    def __str__(self):
        return '<PSlot %s>' % self.slot_str


class SentencePattern:
    def __init__(
        self,
        pattern: str,
        p_slots_dic: dict,
    ):
        self.pattern = pattern
        self.p_slots_dic = p_slots_dic

    def __str__(self):
        # return '<SentencePattern %s> #SLOTS# ' % self.pattern + ', '.join(
        #     [str(_) for i, _ in sorted(self.p_slots_dic.items(), key=lambda x: str(x[0]))]
        # )
        return '<SentencePattern %s>' % self.pattern

    def __eq__(self, other):
        return self.pattern == other.pattern

    def __hash__(self):
        return hash(self.pattern)


class Pattern:
    @staticmethod
    def deprocess_pattern(pattern):
        """
        V,NP => V {patient}
        :param pattern:
        :return:
        """
        reg = re.compile(r'(?P<slot>[A-Za-z_/]+)(?P<prep>(\([a-z\s/]*\))?)(?P<semantic>({.[a-z\-]+})?)')
        depattern = {"NP": "{patient}"}
        segments = pattern.split(',')
        desegments = []
        for segment in segments:
            match_group = reg.match(segment).groupdict()
            if not match_group['prep']:
                if not match_group['semantic']:
                    try:
                        desegments.append(depattern[match_group['slot']])
                    except KeyError:
                        desegments.append(match_group['slot'])
                    continue
                desegments.append(match_group['semantic'].replace('.', ''))
                continue
            desegments.append(match_group['prep'][1:-1])
            if match_group['semantic']:
                desegments.append(match_group['semantic'].replace('.', ''))
        return ' '.join(desegments)

    @staticmethod
    def enprocess_pattern(pattern):
        """
        V {patient} => V,NP
        :param pattern:
        :return:
        """
        reg = re.compile(r'\s([a-z\s/]+\s{.+?}|[a-z\s/]+\sS_ING)')
        enpattern = {"{patient}": "NP"}
        semantics = reg.findall(pattern)
        for semantic in semantics:
            if 'S_ING' in semantic:
                sub_prep = re.match(r'([a-z\s/]+)\sS_ING', semantic).group(1)
                pattern = pattern.replace(sub_prep, 'PP(' + sub_prep + ')')
                continue
            pattern = pattern.replace(semantic, 'PP(' + semantic.replace(' {', '){.'))
        reg = re.compile(r'[A-Za-z_/]+\s({.+?})')
        semantics = reg.findall(pattern)
        for semantic in semantics:
            try:
                pattern = pattern.replace(semantic, enpattern[semantic])
            except KeyError:
                pattern = pattern.replace(semantic, 'NP' + semantic.replace('{', '{.'))
        reg = re.compile(r'\(.+?\)')
        preps = reg.findall(pattern)
        for i, prep in enumerate(preps):
            pattern = pattern.replace(prep, str(i))
        pattern = ','.join(pattern.split(' '))
        for i, prep in enumerate(preps):
            pattern = pattern.replace(str(i), prep)
        return pattern

    @staticmethod
    def iterate_patterns(patterns, process_pattern):
        for pattern in patterns:
            yield process_pattern(pattern)


class PatternMatcher:
    def __init__(self):
        self.funcverbnet = FuncVerbNet()
        self.template_extractor = TemplateExtractor()

    @staticmethod
    def construct_sentence_pattern(pattern: str) -> SentencePattern or None:
        pattern = Pattern.enprocess_pattern(pattern)
        if not pattern:
            return None
        p_slots_dic = {}
        reg = re.compile(r'(?P<role>[A-Za-z_/]+)(?P<prep>(\([a-z\s/]*\))?)(?P<semantic>({.[a-z\-]+})?)')
        segment_list = pattern.split(',')
        for i, segment in enumerate(segment_list):
            match_group = reg.match(segment).groupdict()
            role = match_group['role']
            if True in [(_ in role) for _ in ['that', 'if', 'whether', 'when']]:
                preps = role.split('/')
                semantic = '.mark'
            elif role in ['S', 'S_INF', 'S_ING']:
                preps = []
                semantic = '.sequence'
            else:
                preps = match_group['prep'][1:-1].split('/') if match_group['prep'] else []
                semantic = match_group['semantic'][1:-1] if match_group['semantic'] else ''
            p_slots_dic[i] = PSlot(segment, role, set(preps), semantic)
        return SentencePattern(pattern, p_slots_dic)

    def encapsulate_sentence_patterns(self, patterns):
        if not patterns:
            return None
        verb_sentence_patterns = []
        for pattern in patterns:
            verb_sentence_pattern = self.construct_sentence_pattern(Pattern.enprocess_pattern(pattern))
            verb_sentence_patterns.append(verb_sentence_pattern)
        return verb_sentence_patterns

    @staticmethod
    def generate_template_slots(template):
        if not template:
            return None
        t_slots = template['template'].split(SPLIT_STR)
        tokens_pos_list = template['tokens_pos_list']
        # print('TOKEN_POS_LIST', tokens_pos_list)
        # print('T_SLOTS:', t_slots)
        t_slots_dic = {}
        pos = 0
        t_slot_compound = []
        tokens_pos_group = []
        for i in range(len(t_slots)):
            if t_slots[i] == 'VERB':
                t_slots_dic[pos] = TSlot(t_slots[i], tokens_pos_list[i][0], 0)
                pos += 1
                t_slot_compound = []
                tokens_pos_group = []
            elif t_slots[i] == 'NOUN':
                if t_slots[i - 1] == 'VERB':
                    t_slots_dic[pos] = TSlot(t_slots[i], tokens_pos_list[i][0], 0)
                    pos += 1
                    t_slot_compound = []
                    tokens_pos_group = []
                else:
                    t_slot_compound.append(t_slots[i])
                    tokens_pos_group.extend(tokens_pos_list[i][0])
            elif t_slots[i] == 'doing':
                t_slot_compound.append(t_slots[i])
                tokens_pos_group.extend(tokens_pos_list[i][0])
            elif i + 1 < len(t_slots) and t_slots[i] == 'to' and t_slots[i + 1] == 'do':
                t_slot_compound.extend([t_slots[i], t_slots[i + 1]])
                tokens_pos_group.extend(tokens_pos_list[i][0] + tokens_pos_list[i + 1][0])
                i += 1
            else:
                if t_slot_compound:
                    # core_word = t_slot_compound[0]
                    t_slots_dic[pos] = TSlot(SPLIT_STR.join(t_slot_compound), tokens_pos_group, 0)
                    pos += 1
                t_slot_compound = [t_slots[i]]
                tokens_pos_group = tokens_pos_list[i][0]
        if t_slot_compound:
            # core_word = t_slot_compound[0]
            t_slots_dic[pos] = TSlot(SPLIT_STR.join(t_slot_compound), tokens_pos_group, 0)
        # print('T_SLOTS_DIC:', t_slots_dic)
        # for i in range(len(t_slots_dic)):
        #     print(t_slots_dic[i])
        return t_slots_dic

    def aligned_with_sentence_pattern(self, template, verb_sentence_patterns):
        if not template or not verb_sentence_patterns:
            return None, None
        # >>> sorted by position
        aligned_list = []
        template_slots_dic = sorted(self.generate_template_slots(template).items(), key=lambda x: x[0])
        for verb_sentence_pattern in verb_sentence_patterns:
            sentence_pattern_slot_dic = {}
            # print(verb_sentence_pattern.sentence_pattern_str)
            for value in verb_sentence_pattern.p_slots_dic.values():
                sentence_pattern_slot_dic[value] = -1
            if abs(len(template_slots_dic) - len(sentence_pattern_slot_dic)) <= 2:
                for pos, template_slot in template_slots_dic:
                    for slot, slot_pos in sentence_pattern_slot_dic.items():
                        if template_slot.slot_str == 'VERB' and slot.role == 'V' and slot_pos == -1:
                            sentence_pattern_slot_dic[slot] = pos
                        elif template_slot.slot_str == 'NOUN' and slot.role == 'NP' and slot_pos == -1:
                            sentence_pattern_slot_dic[slot] = pos
                        elif template_slot.slot_str in [
                            'that',
                            'if',
                            'whether',
                            'when'
                        ] and template_slot.slot_str == slot.slot_str and slot_pos == -1:
                            sentence_pattern_slot_dic[slot] = pos
                        else:
                            template_prep = template_slot.slot_str.split(' - ')[0]
                            if template_prep in slot.preps and slot_pos == -1:
                                sentence_pattern_slot_dic[slot] = pos
                for slot, slot_pos in sentence_pattern_slot_dic.items():
                    if slot_pos != -1:
                        continue
                    if slot.role == 'S':
                        if True in [(_ in template) for _ in ['that', 'if', 'whether', 'when']]:
                            sentence_pattern_slot_dic[slot] = len(template_slots_dic)
                    if slot.role == 'S_ING':
                        for pos, template_slot in template_slots_dic:
                            if 'doing' in template_slot.slot_str:
                                sentence_pattern_slot_dic[slot] = pos
                count = 0
                for slot, slot_pos in sentence_pattern_slot_dic.items():
                    if slot_pos == -1:
                        count += 1
                if count == 0:
                    aligned_list.append((sentence_pattern_slot_dic, verb_sentence_pattern))
        aligned_pattern_mapping_list = []
        if len(aligned_list) == 0:
            return None, None
        aligned_pattern = sorted(aligned_list[-1][0].items(), key=lambda x: x[1])
        # print(aligned_pattern)
        for slot, slot_pos in aligned_pattern:
            aligned_pattern_mapping_list.append((
                slot,
                template_slots_dic[slot_pos][1] if slot_pos < len(template_slots_dic) else None
            ))
        # print(aligned_pattern_mapping_list)
        # print(aligned_list[-1][1].pattern)
        return aligned_pattern_mapping_list, aligned_list[-1][1]

    def mapping_template(self, sentence):
        template = self.template_extractor.generate_sentence_template(sentence)
        if not template:
            return None
        category = self.funcverbnet.find_cate_by_id(template['cate_id'])
        slot_mapping, aligned_pattern = self.aligned_with_sentence_pattern(
            template, self.encapsulate_sentence_patterns(category.included_pattern)
        )
        mapped_template = {
            'category': category.name,
            'pattern': Pattern.deprocess_pattern(aligned_pattern.pattern),
            'core_verb': template['core_verb'],
            'roles': []
        }
        if not slot_mapping:
            raise CustomError('PatternError')
        for p_slot, t_slot in slot_mapping:
            mapped_template['roles'].append({
                'role': p_slot.role,
                'semantic': p_slot.semantic,
                'value': ' '.join(t_slot.tokens)
            })
        return mapped_template


if __name__ == '__main__':
    funcverbnet = FuncVerbNet()
    template_extractor = TemplateExtractor()
    pattern_matcher = PatternMatcher()
    # text = "Version of onCreateView(String, Context, AttributeSet) that also supplies the parent that the view created view will be placed in."
    # text = 'Use this function to retrieve the number.'
    # text = 'Prints a string representation of this digest output stream and its associated message digest object.'
    # text = "End the scope of a prefix-URI mapping."
    # text = "How can I send an email by Java application using Gmail, Yahoo?"
    # text = "How can I send an SMTP message from Java"
    # text = "open or create a file and write in file"
    # text = "Version of onCreateView(String, Context, AttributeSet) that also supplies the parent that the view created view will be placed in."
    # text = 'Stops an action event and using this EventQueue.'
    # text = "Prints a long and then terminate the line"
    # text = "Propagates all row update, insert and delete changes to the data source backing this CachedRowSet object using the specified Connection object to establish a connection to the data source."
    # text = "This method is part of the SurfaceHolder. Callback2 interface, and is not normally called or subclassed by clients of GLSurfaceView."
    # text = "Called immediately before commiting the transaction."
    # text = "Called whenever a change of unknown type has occurred, such as the entire list being set to new values."
    # text = "Invoked before sending the specified notification to the listener."
    # text = "This method is invoked with this node locked."
    # text = "Report an intermediate result of the request, without completing it (the request is still active and the app is waiting for the final result), resulting in a call to VoiceInteractor.CommandRequest.onCommandResult with false for isCompleted."
    # text = "This is called whenever the current window attributes change."
    # text = "Notifies this component that it now has a parent component."
    # text = "disables file access within Service Workers, see setAllowFileAccess(boolean)."
    # text = 'Use this function to retrieve the number.'
    # text = "End the scope of a prefix-URI mapping."
    text = "open or create a file to write"
    # text = "Set a reference to task that caused this task to be run."
    # text = "Returns the list of currently running tasks on the node"
    # temp = template_extractor.generate_sentence_template(text)
    # print(temp)
    # cate = funcverbnet.find_cate_by_id(temp['cate_id'])
    # mapping, ap = pattern_matcher.aligned_with_sentence_pattern(
    #     temp, pattern_matcher.encapsulate_sentence_patterns(cate.included_pattern)
    # )
    # for p_slot, t_slot in mapping:
    #     print(p_slot, t_slot, t_slot.tokens)
    # print('-' * 60)
    # print(ap)
    pattern_matcher.mapping_template(text)
    # temp_dic = pm.template_extractor.generate_sentence_template(text)
    # temp = temp_dic['template']
    # cate = pm.funcverbnet.find_cate_by_id(temp_dic['cate_id'])
    # pm.aligned_with_sentence_pattern(temp, pm.encapsulate_sentence_patterns(cate.included_pattern))
    # pm.find_aligned_sentence_pattern(temp, pm.encapsulation(patterns, cateid))
    # pm.sentence_pattern_construction2("")
    # a = pm.encapsulate_sentence_patterns(patterns)
    # print(a)
    # net = FuncVerbNet()
    # with open(read_data("patterns.bin"), "rb") as f:
    #     data = pickle.load(f)
    # for key, value in data.items():
    #     # print(value)
    #     n_pattern = net.find_cate_by_id(key).included_pattern
    #     if len(n_pattern) != len(set(n_pattern)):
    #         print(key)
    #     if len(value) != len(n_pattern):
    #         print(key)
    # for key, value in data.items():
    #     print(key)
    #     for item in iterate_patterns(data[key]):
    #         print(item)
    # for item in iterate_patterns(data[7]):
    #     print(item)
    # for key, value in data.items():
    #     cate = net.find_cate_by_id(key)
    #     if len(value) != len(cate.included_pattern):
    #         print(key)
    #     # a = [_ for _ in iterate_patterns(value, deprocess_pattern)]
    #     # b = cate.included_pattern
    #     # c = set(a) - set(b)
    #     # if c:
    #     #     print('-' * 50)
    #     #     print(key, [_ for _ in iterate_patterns(c, enprocess_pattern)])
    #         # data[key].extend([_ for _ in iterate_patterns(c, enprocess_pattern)])
    #     a = [_ for _ in iterate_patterns(cate.included_pattern, enprocess_pattern)]
    #     b = value
    #     c = set(b) - set(a)
    #     if c:
    #         print(key)
    # print(a)
    # print(b)
    # # print(data[59])
    # # ps = ['V,S_INF', 'V,NP{.material}', 'V,NP{.material},PP(into/as/to){.product}', 'V,NP{.material},PP(in){.location}', 'V,NP{.material},PP(in){.location},PP(into/as/to){.product}', 'V,NP,PP(from){.material},PP(to/as/into){.product}', '']
    # a = [_ for _ in iterate_patterns(data[59], deprocess_pattern)]
    # iterate_patterns(data[59], deprocess_pattern)
    # for key, value in data.items():
    #     cate = net.find_cate_by_id(key)
    #     if len(cate.included_pattern) != len(value):
    #         # print([_ for _ in iterate_patterns(value, deprocess_pattern)])
    #         for pattern in iterate_patterns(value, deprocess_pattern):
    #             if pattern not in cate.included_pattern:
    #                 print("\"" + pattern + "\",")
    #         print(len(cate.included_pattern), len(value))
    #         for pattern in iterate_patterns(cate.included_pattern, enprocess_pattern):
    #             if pattern not in value:
    #                 print(pattern)
    #                 data[key].append(pattern)
    #         # print([_ for _ in iterate_patterns(value, deprocess_pattern)])
    # with open(read_data("patterns.bin"), "wb") as f:
    #     pickle.dump(data, f)
    # for i in range(1, 89):
    #     patterns = net.find_cate_by_id(i).included_pattern
    #     print('-' * 60)
    #     for item in iterate_patterns(patterns, enprocess_pattern):
    #         print(item)
    # result = {}
    # with open(read_data("sentence_pattern.txt"), 'r') as f:
    #     lines_str = f.read()
    # verb_category_pattern_str_list = lines_str.split('\n\n')
    # for each in verb_category_pattern_str_list:
    #     sentence_pattern_list = each.split('\n')
    #     cateid = net.find_cate_by_name(sentence_pattern_list[0].split('/')[0]).id
    #     for pattern in sentence_pattern_list[1:]:
    #         if not pattern:
    #             continue
    #         reg = re.compile(r'\(.+?\)')
    #         semantics = reg.findall(pattern)
    #         for i, semantic in enumerate(semantics):
    #             pattern = pattern.replace(semantic, str(i))
    #         pattern = ','.join(pattern.split(' '))
    #         for i, semantic in enumerate(semantics):
    #             pattern = pattern.replace(str(i), semantic)
    #         result.setdefault(cateid, []).append(pattern)
    # with open(read_data("patterns.bin"), "wb") as f:
    #     pickle.dump(data, f)
    # print(deprocess_pattern("V,NP,PP(by),S_ING"))
    # print("V,NP,PP(by),S_ING")
    # print("V {patient} by S_ING")
    # print(enprocess_pattern("'V {patient} for S_ING'"))
    # print(enprocess_pattern("V {patient} by S_ING"))
    # print("V {patient} from {material} to/as/into {product}")
    # print(deprocess_pattern("V,NP{.patient},PP(from){.material},PP(to/as/into){.product}"))
    # print("V,NP{.patient},PP(from){.material},PP(to/as/into){.product}")
    # print(enprocess_pattern("V {patient} from {material} to/as/into {product}"))
    # print(enprocess_pattern("V {patient} for {beneficiary}"))
    # sub_prep = re.match(r'\s([a-z\s/]+)\sS_ING', " by S_ING")
    # print(sub_prep.group(1))
    # print(enprocess_pattern("V out {patient}"))
    # print(deprocess_pattern("V,PP(out){.patient}"))

    # with open(load_pdata("sentences.csv"), 'r') as f:
    #     df = pd.read_csv(f)
    # for i, text in enumerate(df['single_description'][1000:2000]):
    #     try:
    #         temp = template_extractor.generate_sentence_template(text)
    #         # print(temp['cate_id'], text)
    #         cate = funcverbnet.find_cate_by_id(temp['cate_id'])
    #         _, aligned_pattern = pattern_matcher.aligned_with_sentence_pattern(
    #             temp['template'], pattern_matcher.encapsulate_sentence_patterns(cate.included_pattern)
    #         )
    #         Pattern.deprocess_pattern(aligned_pattern.pattern)
    #     except Exception as e:
    #         print(df['id'][i], text)
    #         print(e, e.__class__.__name__)
