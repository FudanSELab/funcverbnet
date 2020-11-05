#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: isky
@Email: 19110240019@fudan.edu.cn
@Created: 2020/10/21
------------------------------------------
@Modify: 2020/10/21
------------------------------------------
@Description: This file define the basic model class for FuncVerbNet.
"""


# TODO: define all the property of all those FuncCategory based on the OWL we define.


class FuncCategory:
    def __init__(self, id, name, create_time, definition, description, modified_time, representative_verb,
                 included_verb, included_pattern, version, example):
        self.id = id
        self.name = name
        self.create_time = create_time
        self.definition = definition
        self.description = description
        self.modified_time = modified_time
        self.representative_verb = representative_verb
        self.included_verb = included_verb
        self.included_pattern = included_pattern
        self.version = version
        self.example = example
        pass

    def __str__(self):
        # f_category = {
        #     "id": self.id,
        #     "name": self.name,
        #     "create_time": self.create_time,
        #     "definition": self.definition,
        #     "description": self.description,
        #     "modified_time": self.modified_time,
        #     "representative_verb": self.representative_verb,
        #     "included_verb": self.included_verb,
        #     "included_pattern": self.included_pattern,
        #     "version": self.version,
        #     "example": self.example
        # }
        return "<FuncCategory>" + str(self.id)

    def get_representative_verb(self):
        return self.representative_verb
        pass

    def get_all_verbs(self):
        return self.included_verb

    def get_included_pattern(self):
        return self.included_pattern


class FuncVerb:
    def __init__(self, id, qualified_name, description, example, create_time, version):
        self.id = id
        self.qualified_name = qualified_name
        self.description = description
        self.example = example
        self.create_time = create_time
        self.version = version
        pass

    def __str__(self):
        return "<FuncVerb>" + self.id

    def get_funcverb_example(self):
        return self.example


class Verb:
    def __init__(self, id, name, description, create_time, version):
        self.id = id
        self.name = name
        self.description = description
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return "<Verb>" + self.id


class FuncPattern:
    def __init__(self, id, qualified_name, example, description, create_time, version):
        self.id = id
        self.qualified_name = qualified_name
        self.example = example
        self.description = description
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return "<FuncPattern>" + self.id

    def get_funcpattern_example(self):
        return self.example


class PhasePattern:
    def __init__(self, id, syntax, example, description, create_time, version):
        self.id = id
        self.syntax = syntax
        self.example = example
        self.description = description
        self.create_time = create_time
        self.version = version
        pass

    def __str__(self):
        return "<PhasePattern>" + self.id

    def get_phrase_pattern_example(self):
        return self.example


class Role:
    def __init__(self, id, name, definition, create_time, version):
        self.id = id
        self.name = name
        self.definition = definition
        self.create_time = create_time
        self.version = version
        pass

    def get_role_definition(self):
        return self.definition

    def __str__(self):
        return "<Role>" + self.id
