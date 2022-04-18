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
@Description: This file defines the basic model class for FuncVerbNet.
"""


# TODO: define all the property of all those FuncCategory based on the OWL we define.


class FuncCategory:
    def __init__(
        self,
        id,
        name,
        create_time,
        definition,
        description,
        modified_time,
        representative_verb,
        antisense_category,
        antisense_category_id,
        included_verb,
        included_pattern,
        version,
        example
    ):
        self.id = id
        self.name = name
        self.create_time = create_time
        self.definition = definition
        self.description = description
        self.modified_time = modified_time
        self.representative_verb = representative_verb
        self.antisense_category = antisense_category
        self.antisense_category_id = antisense_category_id
        self.included_verb = included_verb
        self.included_pattern = included_pattern
        self.version = version
        self.example = example

    def __str__(self):
        return f"<FuncCategory: id={self.id}>"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.id) + self.name)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_create_time(self):
        return self.create_time

    def get_definition(self):
        return self.definition

    def get_description(self):
        return self.description

    def get_modified_time(self):
        return self.modified_time

    def get_representative_verb(self):
        return self.representative_verb

    def get_included_verb(self):
        return self.included_verb

    def get_all_verbs(self):
        return self.included_verb

    def get_included_pattern(self):
        return self.included_pattern

    def get_version(self):
        return self.version


class FuncVerb:
    def __init__(
        self,
        id,
        qualified_name,
        name,
        description,
        example,
        create_time,
        version
    ):
        self.id = id
        self.qualified_name = qualified_name
        self.name = name
        self.description = description
        self.example = example
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return f"<FuncVerb: id={self.id}>"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.id) + self.name)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.id

    def get_qualified_name(self):
        return self.qualified_name

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_example(self):
        return self.example

    def get_create_time(self):
        return self.create_time

    def get_version(self):
        return self.version


class Verb:
    def __init__(
        self,
        id,
        name,
        description,
        create_time,
        version
    ):
        self.id = id
        self.name = name
        self.description = description
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return f"<Verb: id={self.id}>"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.id) + self.name)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_create_time(self):
        return self.create_time

    def get_version(self):
        return self.version


class FuncPattern:
    def __init__(
        self,
        id,
        qualified_name,
        example,
        description,
        included_roles,
        create_time,
        version
    ):
        self.id = id
        self.qualified_name = qualified_name
        self.example = example
        self.description = description
        self.included_roles = included_roles
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return f"<FuncPattern: id={self.id}>"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.id) + self.qualified_name)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.id

    def get_qualified_name(self):
        return self.qualified_name

    def get_example(self):
        return self.example

    def get_description(self):
        return self.description

    def get_create_time(self):
        return self.create_time

    def get_version(self):
        return self.version


class Pattern:
    def __init__(
        self,
        id,
        syntax,
        example,
        description,
        included_roles,
        create_time,
        version
    ):
        self.id = id
        self.syntax = syntax
        self.example = example
        self.description = description
        self.included_roles = included_roles
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return f"<PhasePattern: id={self.id}>"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.id) + self.syntax)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.id

    def get_syntax(self):
        return self.syntax

    def get_example(self):
        return self.example

    def get_description(self):
        return self.description

    def get_create_time(self):
        return self.create_time

    def get_version(self):
        return self.version


class Semantic:
    def __init__(
        self,
        id,
        name,
        definition,
        create_time,
        version
    ):
        self.id = id
        self.name = name
        self.definition = definition
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return f"<Role: id={self.id}>"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.id) + self.name)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_definition(self):
        return self.definition

    def get_create_time(self):
        return self.create_time

    def get_version(self):
        return self.version


class Sentence:
    def __init__(
        self,
        single_description,
        category,
        create_time,
        version
    ):
        self.single_description = single_description
        self.category = category
        self.create_time = create_time
        self.version = version

    def __str__(self):
        return f"<Sentence: id={self.single_description}>"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.single_description)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def get_single_description(self):
        return self.single_description

    def get_category(self):
        return self.category

    def get_create_time(self):
        return self.create_time

    def get_version(self):
        return self.version
