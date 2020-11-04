"""Main module."""
import json
import os

from Funcverbnet.model import *

root_path = os.path.abspath(os.path.dirname(__file__)).split('model.py')[0]


class FuncVerbNet:

    def __init__(self, category_data_path=os.path.join(root_path, "data/functionality_category.json"),
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
        print(category_data)
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
        print(verb_data)
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


if __name__ == '__main__':
    net = FuncVerbNet()
    f2 = os.path.abspath(os.path.dirname(__file__)).split('model.py')[0]

    print(net.find_cate_by_name('stop'))
    # print(net.find_cate_by_verb('cancel'))
    # print(net.cates[1].name)
    # print(net.verbs[1].id)
