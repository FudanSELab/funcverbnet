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
from funcverbnet.modeling.slot import TSlot, PSlot, SentencePattern
from funcverbnet.nodes.funcverbnet import FuncVerbNet
from funcverbnet.data_handler.template_extractor import TemplateExtractor
from funcverbnet.errors import DataHandlerError
from funcverbnet.utils import CodeUtil

SPLIT_STR = ' - '


class PatternProcess:
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
        pattern = PatternProcess.enprocess_pattern(pattern)
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
            verb_sentence_pattern = self.construct_sentence_pattern(PatternProcess.enprocess_pattern(pattern))
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
        return aligned_pattern_mapping_list, aligned_list[-1][1]

    def mapping_template(self, sentence):
        template = self.template_extractor.generate_sentence_template(sentence)
        if not template:
            return None
        category = self.funcverbnet.find_f_category_by_id(template['cate_id'])
        slot_mapping, aligned_pattern = self.aligned_with_sentence_pattern(
            template, self.encapsulate_sentence_patterns(category.included_pattern)
        )
        mapped_template = {
            'category': category.name,
            'pattern': PatternProcess.deprocess_pattern(aligned_pattern.pattern),
            'core_verb': template['core_verb'],
            'roles': []
        }
        if not slot_mapping:
            raise DataHandlerError('PatternError')
        for p_slot, t_slot in slot_mapping:
            mapped_template['roles'].append({
                'role': p_slot.role,
                'semantic': p_slot.semantic,
                'value': ' '.join(t_slot.tokens)
            })
        return mapped_template

    def mapping_template_copy(self, sentence):
        template = self.template_extractor.generate_sentence_template(sentence)
        category = self.funcverbnet.find_f_category_by_id(template['cate_id'])
        mapped_template = {
            'sentence': sentence,
            'category': category.name,
            'category_id': template['cate_id'],
            'pattern': None,
            'pattern_id': None,
            'core_verb': None,
            'roles': []
        }
        if not template['template']:
            return mapped_template
        included_pattern = category.included_pattern
        if template['cate_id'] == -1:
            included_pattern = list(self.funcverbnet.patterns_map.keys())
        slot_mapping, aligned_pattern = self.aligned_with_sentence_pattern(
            template, self.encapsulate_sentence_patterns(included_pattern)
        )
        if not aligned_pattern:
            return mapped_template
        syntax = PatternProcess.deprocess_pattern(aligned_pattern.pattern)
        mapped_template['pattern'] = syntax
        mapped_template['pattern_id'] = self.funcverbnet.get_pattern_id_by_syntax(syntax)
        mapped_template['core_verb'] = template['core_verb']
        if slot_mapping:
            for p_slot, t_slot in slot_mapping:
                mapped_template['roles'].append({
                    'role': p_slot.role,
                    'semantic': p_slot.semantic[1:],
                    'value': ' '.join(t_slot.tokens) if not p_slot.preps else ' '.join(t_slot.tokens[1:])
                })
        return mapped_template

    def mapping_template_from_qualified_name(self, qualified_name: str):
        if not qualified_name:
            return None
        parent, unqualified_name = CodeUtil.simplify_method_qualified_name(qualified_name)
        decamelized_name = CodeUtil.decamelize_by_substitute_verb(parent, unqualified_name[0])
        return self.mapping_template_copy(decamelized_name)
