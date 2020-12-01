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

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash("<FuncCategory>" + self.id)

    def __repr__(self):
        return "{id:" + str(
            self.id) + ", name:" + self.name + ", create_time:" + self.create_time + ", definition:" + self.definition + ", description:" + self.description + ", modified_time:" + self.modified_time + ", representative_verb:" + self.representative_verb + ", included_verb:" + str(
            self.included_verb) + ", included_pattern:" + str(
            self.included_pattern) + ", version:" + self.version + ", example:" + self.example + "}"

    def get_funcCategory_id(self):
        return self.id
        pass

    def get_funcCategory_name(self):
        return self.name
        pass

    def get_funccategory_create_time(self):
        return self.create_time
        pass

    def get_funccategory_definition(self):
        return self.definition
        pass

    def get_funccategory_description(self):
        return self.description
        pass

    def get_funccategory_modified_time(self):
        return self.modified_time

    def get_funccategory_representative_verb(self):
        return self.representative_verb
        pass

    def get_funccategory_included_verb(self):
        return self.included_verb

    def get_funccategory_all_verbs(self):
        return self.included_verb

    def get_funccategory_included_pattern(self):
        return self.included_pattern

    def get_funccategory_version(self):
        return self.version


class FuncVerb:
    def __init__(self, id, qualified_name, name, description, example, create_time, version):
        self.id = id
        self.qualified_name = qualified_name
        self.name = name
        self.description = description
        self.example = example
        self.create_time = create_time
        self.version = version
        pass

    def __str__(self):
        return "<FuncVerb>" + str(self.id)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash("<FuncVerb>" + self.id)

    def __repr__(self):
        return "{id:" + str(
            self.id) + ", qualified_name:" + self.qualified_name + ", name:" + self.name + ", description:" + self.description + ", example:" + self.example + ", create_time:" + self.create_time + ", version:" + self.version + "} "

    def get_funcverb_id(self):
        return self.id

    def get_funcverb_qualified_name(self):
        return self.qualified_name

    def get_funcverb_name(self):
        return self.name

    def get_funcverb_description(self):
        return self.description

    def get_funcverb_example(self):
        return self.example

    def get_funcverb_create_time(self):
        return self.create_time

    def get_funcverb_version(self):
        return self.version


class Verb:
    def __init__(self, id, name, description, create_time, version):
        self.id = id
        self.name = name
        self.description = description
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return "<Verb>" + str(self.id)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash("<Verb>" + self.id)

    def __repr__(self):
        return "{id:" + str(
            self.id) + ", name:" + self.name + ", description:" + self.description + ", create_time:" + self.create_time + ", version:" + self.version + "} "

    def get_verb_id(self):
        return self.id

    def get_verb_name(self):
        return self.name

    def get_verb_description(self):
        return self.description

    def get_verb_create_time(self):
        return self.create_time

    def get_verb_version(self):
        return self.version


class FuncPattern:
    def __init__(self, id, qualified_name, example, description, included_roles, create_time, version):
        self.id = id
        self.qualified_name = qualified_name
        self.example = example
        self.description = description
        self.included_roles = included_roles
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return "<FuncPattern>" + str(self.id)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash("<FuncPattern>" + self.id)

    def __repr__(self):
        return "{id:" + str(
            self.id) + ", qualified_name:" + self.qualified_name + ", description:" + self.description + ", example:" + self.example + ", create_time:" + self.create_time + ", version:" + self.version + "} "

    def get_funcpattern_id(self):
        return self.id

    def get_funcpattern_qualified_name(self):
        return self.qualified_name

    def get_funcpattern_example(self):
        return self.example

    def get_funcpattern_description(self):
        return self.description

    def get_funcpattern_create_time(self):
        return self.create_time

    def get_funcpattern_version(self):
        return self.version


class PhasePattern:
    def __init__(self, id, syntax, example, description, included_roles, create_time, version):
        self.id = id
        self.syntax = syntax
        self.example = example
        self.description = description
        self.included_roles = included_roles
        self.create_time = create_time
        self.version = version
        pass

    def __str__(self):
        return "<PhasePattern>" + str(self.id)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash("<PhasePattern>" + self.id)

    def __repr__(self):
        return "{id:" + str(
            self.id) + ", syntax:" + self.syntax + ", description:" + self.description + ", example:" + self.example + \
               ", create_time:" + self.create_time + ", version:" + self.version + "} "

    def get_phrase_pattern_id(self):
        return self.id

    def get_phrase_pattern_syntax(self):
        return self.syntax

    def get_phrase_pattern_example(self):
        return self.example

    def get_phrase_pattern_description(self):
        return self.description

    def get_phrase_pattern_create_time(self):
        return self.create_time

    def get_phrase_pattern_version(self):
        return self.version


class Role:
    def __init__(self, id, name, definition, create_time, version):
        self.id = id
        self.name = name
        self.definition = definition
        self.create_time = create_time
        self.version = version
        pass

    def __str__(self):
        return "<Role>" + str(self.id)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash("<Role>" + self.id)

    def __repr__(self):
        return "{id:" + str(
            self.id) + ", name:" + self.name + ", definition:" + self.definition + \
               ", create_time:" + self.create_time + ", version:" + self.version + "} "

    def get_role_id(self):
        return self.id

    def get_role_name(self):
        return self.name

    def get_role_definition(self):
        return self.definition

    def get_role_create_time(self):
        return self.create_time

    def get_role_version(self):
        return self.version


class Sentence:
    def __init__(self, single_description, category, create_time, version):
        self.single_description = single_description
        self.category = category
        self.create_time = create_time
        self.version = version
        pass

    def __str__(self):
        return "<Sentence>" + str(self.single_description)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash("<Sentence>" + self.single_description)

    def __repr__(self):
        return "{single_description:" + str(
            self.single_description) + ", category:" + self.category + \
               ", create_time:" + self.create_time + ", version:" + self.version + "} "

    def get_sentence_single_description(self):
        return self.single_description

    def get_sentence_category(self):
        return self.category

    def get_sentence_create_time(self):
        return self.create_time

    def get_sentence_version(self):
        return self.version
