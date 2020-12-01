"""Main module."""
import csv
import json
import os
import time
from pathlib import Path
import pandas as pd

from funcverbnet.model import FuncCategory, Verb, PhasePattern, FuncPattern, FuncVerb, Role, Sentence

root_path = os.path.abspath(os.path.dirname(__file__)).split('model.py')[0]
path = Path(root_path)
SEMANTIC_ROLE_PATH = str(path / "data" / "semantic_role.json")
CATEGORY_DATA_PATH = str(path / "data" / "functionality_category.json")
VERB_DATA_PATH = str(path / "data" / "verb.json")
PATTERN_DATA_PATH = str(path / "data" / "phrase_pattern.json")
F_PATTERN_DATA_PATH = str(path / "data" / "f_pattern.json")
F_VERB_DATA_PATH = str(path / "data" / "f_verb.json")
SENTENCES_DATA_PATH = str(path / "data" / "sentences_with_annotation.csv")


class FuncVerbNet:

    def __init__(self, semantic_role_path=SEMANTIC_ROLE_PATH,
                 category_data_path=CATEGORY_DATA_PATH,
                 verb_data_path=VERB_DATA_PATH,
                 pattern_data_path=PATTERN_DATA_PATH,
                 f_pattern_data_path=F_PATTERN_DATA_PATH,
                 f_verb_data_path=F_VERB_DATA_PATH, sentences_data_path=SENTENCES_DATA_PATH):
        ## todo: load all the data from json.
        self.role_list = []
        self.cate_list = []
        self.verb_list = []
        self.f_verb_list = []
        self.f_pattern_list = []
        self.pattern_list = []
        self.sentences = []
        self.init_role_list(semantic_role_path)
        self.init_cate_list(category_data_path)
        self.init_verb_list(verb_data_path)
        self.init_pattern_list(pattern_data_path)
        self.init_f_pattern_list(f_pattern_data_path)
        self.init_f_verb_list(f_verb_data_path)
        self.init_sentences(sentences_data_path)

        pass

    def init_cate_list(self, category_data_path=CATEGORY_DATA_PATH):
        # category_data_path = "./data/functionality_category.json"
        with open(category_data_path, 'r', encoding='utf-8') as category_data_file:
            category_data = json.load(category_data_file)  # json.load()用于从json文件中读取数据
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

    def init_verb_list(self, verb_data_path=VERB_DATA_PATH):
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

    def init_pattern_list(self, pattern_data_path=PATTERN_DATA_PATH):
        with open(pattern_data_path, 'r', encoding='utf-8') as pattern_file:
            pattern_data = json.load(pattern_file)
        for pattern in range(0, len(pattern_data)):
            id = pattern_data[pattern]['id']
            syntax = pattern_data[pattern]['syntax']
            example = pattern_data[pattern]['example']
            description = pattern_data[pattern]['description']
            included_roles = pattern_data[pattern]['included_roles']
            create_time = pattern_data[pattern]['create_time']
            version = pattern_data[pattern]['version']
            new_pattern = PhasePattern(id, syntax, example, description, included_roles, create_time, version)
            self.pattern_list.append(new_pattern)

        pass

    def init_f_pattern_list(self, f_pattern_data_path=F_PATTERN_DATA_PATH):
        with open(f_pattern_data_path, 'r', encoding='utf-8') as f_pattern_file:
            f_pattern_data = json.load(f_pattern_file)
        for f_pattern in range(0, len(f_pattern_data)):
            id = f_pattern_data[f_pattern]['id']
            qualified_name = f_pattern_data[f_pattern]['qualified_name']
            example = f_pattern_data[f_pattern]['example']
            description = f_pattern_data[f_pattern]['description']
            included_roles = f_pattern_data[f_pattern]['included_roles']
            create_time = f_pattern_data[f_pattern]['create_time']
            version = f_pattern_data[f_pattern]['version']

            new_f_pattern = FuncPattern(id, qualified_name, example, description, included_roles, create_time, version)
            self.f_pattern_list.append(new_f_pattern)
        pass

    def init_f_verb_list(self, f_verb_data_path=F_VERB_DATA_PATH):
        with open(f_verb_data_path, 'r', encoding='utf-8') as f_verb_file:
            f_verb_data = json.load(f_verb_file)
        for f_verb in range(0, len(f_verb_data)):
            id = f_verb_data[f_verb]['id']
            qualified_name = f_verb_data[f_verb]['qualified_name']
            name = f_verb_data[f_verb]['name']
            description = f_verb_data[f_verb]['description']
            example = f_verb_data[f_verb]['example']
            create_time = f_verb_data[f_verb]['create_time']
            version = f_verb_data[f_verb]['version']
            new_f_verbs = FuncVerb(id, qualified_name, name, description, example, create_time, version)
            self.f_verb_list.append(new_f_verbs)
        pass

    def init_role_list(self, semantic_role_path=SEMANTIC_ROLE_PATH):
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

    def init_sentences(self, sentences_data_path=SENTENCES_DATA_PATH):
        # with open(sentences_data_path,'r',encoding='utf-8') as sentence_file:
        #     sentences_data = csv.reader(sentence_file)
        #     sentences_data_list = list(sentences_data)
        #     for sentence in sentences_data_list:
        #         print(sentence)
        #         single_description=sentences_data_list[3]
        df = pd.read_csv(sentences_data_path, header=0)
        for i in range(len(df)):
            single_description = str(df['single_description'][i])
            category = str(df['final_annotation_type'][i])
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            version = '1.0'
            new_sentence = Sentence(single_description, category, create_time, version)
            self.sentences.append(new_sentence)

    def get_sentences(self):
        return self.sentences

    def is_valid_verb(self, verb):
        if str.isalpha(verb) is True:
            for v in self.verb_list:
                if v.name == verb:
                    return True
            return False
        else:
            return False

    def is_valid_category_id(self, category_id):
        if isinstance(category_id, int):
            if len(self.cate_list) >= category_id >= 0:
                return True
            return False
        else:
            return False

    def is_valid_pattern_name(self, pattern_name):
        if isinstance(pattern_name, str):
            for pattern in self.pattern_list:
                if pattern.syntax == pattern_name:
                    return True
            return False
        else:
            return False

    def is_valid_pattern_id(self, p_id):
        if isinstance(p_id, int):
            for pattern in self.pattern_list:
                if pattern.id == p_id:
                    return True
            return False
        else:
            return False

    def is_valid_role_name(self, role_name):
        if str.isalpha(role_name) is True:
            for role in self.role_list:
                if role.name == role_name:
                    return True
            return False
        else:
            return False

    def is_valid_role_id(self, role_id):
        if isinstance(role_id, int):
            for role in self.role_list:
                if role.id == role_id:
                    return True
            return False
        else:
            return False

    def is_valid_f_verb(self, f_verb):
        if str.isalpha(f_verb) is True:
            verbs = []
            for cate in self.cate_list:
                if self.find_all_verb_name_by_cate_id(cate.id) is not None:
                    for v in self.find_all_verb_name_by_cate_id(cate.id):
                        verbs.append(v)
            for verb in verbs:
                if verb == f_verb:
                    return True
            return False
        else:
            return False

    def is_valid_f_pattern(self, f_pattern):
        if isinstance(f_pattern, str):
            patterns = []
            for cate in self.cate_list:
                if self.find_all_pattern_name_by_cate_id(cate.id) is not None:
                    for p in self.find_all_pattern_name_by_cate_id(cate.id):
                        patterns.append(p)
            for pattern in patterns:
                if pattern == f_pattern:
                    return True
            return False
        else:
            return False

    def is_role_included_in_pattern(self, role_name):
        if self.is_valid_role_name(role_name):
            roles = []
            for pattern in self.pattern_list:
                for r in self.find_included_roles_by_pattern_id(pattern.id):
                    roles.append(r)
            for role in roles:
                if role == role_name:
                    return True
            return False
        else:
            return False

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

    def find_role_by_name(self, r_name):
        for role in self.role_list:
            if role.name == r_name:
                return role
        # return None

    def find_cate_by_pattern(self, included_pattern):
        for cate in self.cate_list:
            for pattern in cate.included_pattern:
                # print(j)
                if pattern == included_pattern:
                    return cate
        return None

    def find_all_verb_by_cate_id(self, cate_id):
        if self.is_valid_category_id(cate_id) is True:
            verbs = []
            for cate in self.cate_list:
                if cate.id == cate_id:
                    included_verb = cate.included_verb
            for verb in included_verb:
                verbs.append(self.find_verb_by_name(verb))
            return verbs
        else:
            return None

    def find_all_verb_name_by_cate_id(self, cate_id):
        if self.is_valid_category_id(cate_id) is True:
            for cate in self.cate_list:
                if cate.id == cate_id:
                    return cate.included_verb
        else:
            return None

    def find_all_pattern_by_cate_id(self, cate_id):
        if self.is_valid_category_id(cate_id) is True:
            patterns = []
            for cate in self.cate_list:
                if cate.id == cate_id:
                    included_pattern = cate.included_pattern
            for p_syntax in included_pattern:
                patterns.append(self.find_pattern_by_syntax(p_syntax))
            return patterns
        else:
            return None

    def find_all_pattern_name_by_cate_id(self, cate_id):
        if self.is_valid_category_id(cate_id) is True:
            for cate in self.cate_list:
                if cate.id == cate_id:
                    return cate.included_pattern
        else:
            return None

    def find_included_roles_by_pattern_id(self, p_id):
        if self.is_valid_pattern_id(p_id) is True:
            for pattern in self.pattern_list:
                if pattern.id == p_id:
                    return pattern.included_roles
        else:
            return None

    def find_all_roles_by_cate_id(self, cate_id):
        if self.is_valid_category_id(cate_id) is True:
            role_list = []
            result = []
            patterns = self.find_all_pattern_name_by_cate_id(cate_id)
            for pattern_name in patterns:
                pattern = self.find_pattern_by_syntax(pattern_name)
                roles = self.find_included_roles_by_pattern_id(pattern.id)
                for role in roles:
                    role_list.append(role)
            role_name = list(set(role_list))
            for role in role_name:
                a_role = self.find_role_by_name(role)
                result.append(a_role)
            return result
        else:
            return None

    def get_category_number(self):
        cate_number = -1
        for cate in self.cate_list:
            cate_number += 1
        # print(cate_number)
        return cate_number

    def get_included_verb_number_by_cateid(self, cateid):
        if self.is_valid_category_id(cateid):
            cate = self.find_cate_by_id(cateid)
            verbs = self.find_all_verb_name_by_cate_id(cate.id)
            verb_num = 0
            for verb in verbs:
                verb_num += 1
            return verb_num
        else:
            return None

    def get_included_roles_number_by_pattern_id(self, p_id):
        if self.is_valid_pattern_id(p_id):
            pattern = self.find_pattern_by_id(p_id)
            roles = self.find_included_roles_by_pattern_id(pattern.id)
            role_num = 0
            for verb in roles:
                role_num += 1
            return role_num
        else:
            return None

    def get_included_pattern_number_by_cateid(self, cateid):
        if self.is_valid_category_id(cateid):
            cate = self.find_cate_by_id(cateid)
            patterns = self.find_all_pattern_name_by_cate_id(cate.id)
            pattern_num = 0
            for verb in patterns:
                pattern_num += 1
            return pattern_num
        else:
            return None

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

    def find_f_verb_by_name(self, v_name):
        for verb in self.f_verb_list:
            if verb.name == v_name:
                return verb
        return None

    def find_f_verb_by_id(self, v_id):
        for verb in self.f_verb_list:
            if verb.id == v_id:
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
        if self.is_valid_role_name(role_name):
            role = self.find_role_by_name(role_name)
            return role.definition
        else:
            return None

    def find_role_definition_by_id(self, role_id):
        if self.is_valid_role_id(role_id):
            role = self.find_role_by_id(role_id)
            return role.definition
        else:
            return None

    def find_role_name_by_id(self, role_id):
        if self.is_valid_role_id(role_id):
            role = self.find_role_by_id(role_id)
            return role.name
        else:
            return None

    def find_cates_by_pattern(self, pattern):
        if self.is_valid_pattern_name(pattern):
            cates = []
            for cate in self.cate_list:
                for p in cate.included_pattern:
                    if p == pattern:
                        cates.append(cate)
            return cates
        else:
            return None

    def find_cates_by_verb(self, verb):
        if self.is_valid_verb(verb):
            cates = []
            for cate in self.cate_list:
                for v in cate.included_verb:
                    if v == verb:
                        cates.append(cate)
            return cates
        else:
            return None

    def find_patterns_by_role_id(self, r_id):
        if self.is_valid_role_id(r_id):
            r_name = self.find_role_name_by_id(r_id)
            patterns = []
            for pattern in self.pattern_list:
                for role in pattern.included_roles:
                    if role == r_name:
                        patterns.append(pattern)
            return patterns
        else:
            return None

    def find_patterns_by_role_name(self, r_name):
        if self.is_valid_role_name(r_name):
            patterns = []
            for pattern in self.pattern_list:
                for role in pattern.included_roles:
                    if role == r_name:
                        patterns.append(pattern)
            return patterns
        else:
            return None

    def find_patterns_with_two_roles_id(self, role1_id, role2_id):
        if self.is_valid_role_id(role1_id) and self.is_valid_role_id(role2_id) is True:
            patterns = []
            pattern1 = self.find_patterns_by_role_id(role1_id)
            pattern2 = self.find_patterns_by_role_id(role2_id)
            for p1 in pattern1:
                for p2 in pattern2:
                    if p1 == p2:
                        patterns.append(p1)
                        continue
            return patterns
        else:
            return None

    def find_patterns_with_two_roles_name(self, role1_name, role2_name):
        if self.is_valid_role_name(role1_name) and self.is_valid_role_name(role2_name) is True:
            patterns = []
            pattern1 = self.find_patterns_by_role_name(role1_name)
            pattern2 = self.find_patterns_by_role_name(role2_name)
            for p1 in pattern1:
                for p2 in pattern2:
                    if p1 == p2:
                        patterns.append(p1)
                        continue
            return patterns
        else:
            return None

    def find_cates_with_two_verbs(self, verb1, verb2):
        if self.is_valid_verb(verb1) and self.is_valid_verb(verb2) is True:
            cates = []
            cates1 = self.find_cates_by_verb(verb1)
            cates2 = self.find_cates_by_verb(verb2)
            for cate1 in cates1:
                for cate2 in cates2:
                    if cate1.id == cate2.id:
                        cates.append(cate1)
                    continue
            if cates is not None:
                return cates
            else:
                return None
        else:
            return None

    def find_cates_by_role(self, role_name):
        if self.is_valid_role_name(role_name):
            patterns = self.find_patterns_by_role_name(role_name)
            result = []
            categories = []
            for pattern in patterns:
                cates = self.find_cate_by_pattern(pattern.syntax)
                result.append(cates)
            for cate in result:
                if cate not in categories:
                    print(cate)
                    categories.append(cate)
            return categories
        else:
            return None

    def find_common_verbs_by_cates(self, cate1, cate2):
        if self.is_valid_category_id(cate1) and self.is_valid_category_id(cate2) is True:
            verbs1 = self.find_all_verb_name_by_cate_id(cate1)
            verbs2 = self.find_all_verb_name_by_cate_id(cate2)
            common_verbs = []
            for verb1 in verbs1:
                for verb2 in verbs2:
                    if verb1 == verb2:
                        common_verbs.append(verb1)
                    continue
            return common_verbs
        else:
            return None

    def find_common_patterns_by_cates(self, cate1, cate2):
        if self.is_valid_category_id(cate1) and self.is_valid_category_id(cate2):
            patterns1 = self.find_all_pattern_name_by_cate_id(cate1)
            patterns2 = self.find_all_pattern_name_by_cate_id(cate2)
            common_patterns = []
            for pattern1 in patterns1:
                for pattern2 in patterns2:
                    if pattern1 == pattern2:
                        common_patterns.append(pattern1)
                    continue
            return common_patterns
        else:
            return None

    def find_common_roles_by_pattern_id(self, p_id1, p_id2):
        if self.is_valid_pattern_id(p_id1) and self.is_valid_pattern_id(p_id2) is True:
            roles1 = self.find_included_roles_by_pattern_id(p_id1)
            roles2 = self.find_included_roles_by_pattern_id(p_id2)
            common_roles = []
            for role1 in roles1:
                for role2 in roles2:
                    if role1 == role2:
                        common_roles.append(role1)
                    continue
            return common_roles
        else:
            return None

    def find_sentences_by_category(self, category_id):
        if self.is_valid_category_id(category_id):
            sentences = []
            for sentence in self.sentences:
                # print(sentence.category)
                # print(category_id)
                if int(sentence.category) == category_id:
                    # print(sentence.category)
                    sentences.append(sentence)

            return sentences
        else:
            return None

