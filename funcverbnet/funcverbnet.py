"""Main module."""
import json
import os

from funcverbnet.model import *

root_path = os.path.abspath(os.path.dirname(__file__)).split('model.py')[0]


class FuncVerbNet:

    def __init__(self, semantic_role_path=os.path.join(root_path, "data/semantic_role.json"),
                 category_data_path=os.path.join(root_path, "data/functionality_category.json"),
                 verb_data_path=os.path.join(root_path, "data/verb.json"),
                 pattern_data_path=os.path.join(root_path, "data/phrase_pattern.json"),
                 f_pattern_data_path=os.path.join(root_path, "data/f_pattern.json"),
                 f_verb_data_path=os.path.join(root_path, "data/f_verb.json")):
        ## todo: load all the data from json.
        self.role_list = []
        self.cate_list = []
        self.verb_list = []
        self.f_verb_list = []
        self.f_pattern_list = []
        self.pattern_list = []
        self.init_role_list(semantic_role_path)
        self.init_cate_list(category_data_path)
        self.init_verb_list(verb_data_path)
        self.init_pattern_list(pattern_data_path)
        self.init_f_pattern_list(f_pattern_data_path)
        self.init_f_verb_list(f_verb_data_path)

        pass

    def init_cate_list(self, category_data_path=os.path.join(root_path, "data/functionality_category.json")):
        # category_data_path = "./data/functionality_category.json"
        with open(category_data_path, 'r', encoding='utf-8') as category_data_file:
            category_data = json.load(category_data_file)
        for cate in category_data:
            name = cate['name']
            id = cate['id']
            create_time = cate['create_time']
            definition = cate['definition']
            description = cate['description']
            modified_time = cate['modified_time']
            representative_verb = cate['representative_verb']
            included_verb = cate['included_verb']
            included_pattern = cate['included_pattern']
            version = cate['version']
            example = cate['example']

            new_cates = FuncCategory(id, name, create_time, definition, description, modified_time,
                                     representative_verb, included_verb, included_pattern, version, example)
            self.cate_list.append(new_cates)

    def init_verb_list(self, verb_data_path=os.path.join(root_path, "data/verb.json")):
        with open(verb_data_path, 'r', encoding='utf-8') as verb_file:
            verb_data = json.load(verb_file)
        for verb in range(0, len(verb_data)):
            id = verb_data[verb]['id']
            name = verb_data[verb]['name']
            description = verb_data[verb]['description']
            create_time = verb_data[verb]['create_time']
            version = verb_data[verb]['version']
            new_verbs = Verb(id, name, description, create_time, version)
            self.verb_list.append(new_verbs)
            pass

    def init_pattern_list(self, pattern_data_path=os.path.join(root_path, "data/phrase_pattern.json")):
        with open(pattern_data_path, 'r', encoding='utf-8') as pattern_file:
            pattern_data = json.load(pattern_file)
        for pattern in range(0, len(pattern_data)):
            id = pattern_data[pattern]['id']
            syntax = pattern_data[pattern]['syntax']
            example = pattern_data[pattern]['example']
            description = pattern_data[pattern]['description']
            create_time = pattern_data[pattern]['create_time']
            version = pattern_data[pattern]['version']
            new_pattern = PhasePattern(id, syntax, example, description, create_time, version)
            self.pattern_list.append(new_pattern)

        pass

    def init_f_pattern_list(self, f_pattern_data_path=os.path.join(root_path, "data/f_pattern.json")):
        with open(f_pattern_data_path, 'r', encoding='utf-8') as f_pattern_file:
            f_pattern_data = json.load(f_pattern_file)
        for f_pattern in range(0, len(f_pattern_data)):
            id = f_pattern_data[f_pattern]['id']
            qualified_name = f_pattern_data[f_pattern]['qualified_name']
            example = f_pattern_data[f_pattern]['example']
            description = f_pattern_data[f_pattern]['description']
            create_time = f_pattern_data[f_pattern]['create_time']
            version = f_pattern_data[f_pattern]['version']

            new_f_pattern = FuncPattern(id, qualified_name, example, description, create_time, version)
            self.f_pattern_list.append(new_f_pattern)
        pass

    def init_f_verb_list(self, f_verb_data_path=os.path.join(root_path, "data/f_verb.json")):
        with open(f_verb_data_path, 'r', encoding='utf-8') as f_verb_file:
            f_verb_data = json.load(f_verb_file)
        for f_verb in range(0, len(f_verb_data)):
            id = f_verb_data[f_verb]['id']
            qualified_name = f_verb_data[f_verb]['qualified_name']
            description = f_verb_data[f_verb]['description']
            example = f_verb_data[f_verb]['example']
            create_time = f_verb_data[f_verb]['create_time']
            version = f_verb_data[f_verb]['version']
            new_f_verbs = FuncVerb(id, qualified_name, description, example, create_time, version)
            self.f_verb_list.append(new_f_verbs)
        pass

    def init_role_list(self, semantic_role_path=os.path.join(root_path, "data/semantic_role.json")):
        with open(semantic_role_path, 'r', encoding='utf-8') as semantic_role_file:
            semantic_role_data = json.load(semantic_role_file)
        for semantic_role in range(0, len(semantic_role_data)):
            id = semantic_role_data[semantic_role]['id']
            name = semantic_role_data[semantic_role]['name']
            definition = semantic_role_data[semantic_role]['definition']
            create_time = semantic_role_data[semantic_role]['create_time']
            version = semantic_role_data[semantic_role]['version']
            new_semantic_role = Role(id, name, definition, create_time, version)
            self.role_list.append(new_semantic_role)
        pass

    def find_cate_by_name(self, name):
        for cate in self.cate_list:
            if cate.name == name:
                return cate
        return None

    def find_cate_by_verb(self, included_verb):
        for cate in self.cate_list:
            for verb in cate.included_verb:
                # print(j)
                if verb == included_verb:
                    return cate
        return None

    def find_cate_by_id(self, id):
        for cate in self.cate_list:
            if cate.id == id:
                return cate
        return None

    def find_cate_by_pattern(self, included_pattern):
        for cate in self.cate_list:
            for pattern in cate.included_pattern:
                # print(j)
                if pattern == included_pattern:
                    return cate
        return None

    def find_all_verb_by_cate(self, cate_id):
        for cate in self.cate_list:
            if cate.id == cate_id:
                return cate.included_verb

    def find_all_pattern_by_cate(self, cate_id):
        for cate in self.cate_list:
            if cate.id == cate_id:
                return cate.included_pattern

    def get_category_number(self):
        cate_number = -1
        for cate in self.cate_list:
            cate_number += 1
        # print(cate_number)
        return cate_number

    def get_included_verb_number_by_cateid(self, cateid):
        cate = self.find_cate_by_id(cateid)
        verbs = self.find_all_verb_by_cate(cate.id)
        verb_num = 0
        for verb in verbs:
            verb_num += 1
        return verb_num

    def get_included_pattern_number_by_cateid(self, cateid):
        cate = self.find_cate_by_id(cateid)
        patterns = self.find_all_pattern_by_cate(cate.id)
        pattern_num = 0
        for verb in patterns:
            pattern_num += 1
        return pattern_num

    def get_role_number(self):
        role_num = 0
        for role in self.role_list:
            role_num += 1
        return role_num

    def get_verb_number(self):
        verb_num = 0
        for verb in self.verb_list:
            verb_num += 1
        return verb_num

    def get_pattern_number(self):
        pattern_number = 0
        for pattern in self.pattern_list:
            pattern_number += 1
        return pattern_number

    def find_verb_by_id(self, verb_id):
        for verb in self.verb_list:
            if verb.id == verb_id:
                return verb
        return None

    def find_verb_by_name(self, v_name):
        for verb in self.verb_list:
            if verb.name == v_name:
                return verb
        return None

    def find_pattern_by_id(self, p_id):
        for pattern in self.pattern_list:
            if pattern.id == p_id:
                return pattern
        return None

    def find_pattern_by_syntax(self, p_syntax):
        for pattern in self.pattern_list:
            if pattern.syntax == p_syntax:
                return pattern
        return None

    def find_role_by_id(self, role_id):
        for role in self.role_list:
            if role.id == role_id:
                return role
        return None

    def find_role_by_name(self, role_name):
        for role in self.role_list:
            if role.name == role_name:
                return role
        return None

    def find_role_definition_by_name(self, role_name):
        role = self.find_role_by_name(role_name)
        return role.definition

    def find_role_definition_by_id(self, role_id):
        role = self.find_role_by_id(role_id)
        return role.definition

    def find_role_name_by_id(self, role_id):
        role = self.find_role_by_id(role_id)
        return role.name

    def find_cates_by_pattern(self, pattern):
        cates = []
        for cate in self.cate_list:
            for p in cate.included_pattern:
                if p == pattern:
                    cates.append(cate)
        return cates

    def find_cates_by_verb(self, verb):
        cates = []
        for cate in self.cate_list:
            for v in cate.included_verb:
                if v == verb:
                    cates.append(cate)
        return cates


if __name__ == '__main__':
    net = FuncVerbNet()
    f2 = os.path.abspath(os.path.dirname(__file__)).split('model.py')[0]

    print(net.find_cate_by_name('stop'))
    # print(net.find_cate_by_verb('cancel'))
    # print(net.cates[1].name)
    # print(net.verbs[1].id)
