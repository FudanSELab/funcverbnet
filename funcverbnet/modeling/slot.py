#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/04/15
------------------------------------------
@Modify: 2022/04/15
------------------------------------------
@Description:
"""


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
