"""Main module."""
import json
import pickle
import time
import pandas as pd

from funcverbnet.modeling.models import FuncCategory, Verb, Pattern, FuncPattern, FuncVerb, Semantic, Sentence
from funcverbnet.classifier.sentence_classifier import FuncSentenceClassifier
from funcverbnet.utils import load_data

F_CATEGORY_DATA_PATH = load_data("f_category.json")
F_VERB_DATA_PATH = load_data("f_verb.json")
VERB_DATA_PATH = load_data("verbs.json")
F_PATTERN_DATA_PATH = load_data("f_pattern.json")
PATTERN_DATA_PATH = load_data("patterns.json")
PATTERN_MAP_PATH = load_data("patterns.bin")
SEMANTIC_DATA_PATH = load_data("semantics.json")
SENTENCE_DATA_PATH = load_data("sentences.csv")


class FuncVerbNet:
    def __init__(
        self,
        f_category_data_path=F_CATEGORY_DATA_PATH,
        f_verb_data_path=F_VERB_DATA_PATH,
        verb_data_path=VERB_DATA_PATH,
        f_pattern_data_path=F_PATTERN_DATA_PATH,
        pattern_data_path=PATTERN_DATA_PATH,
        pattern_map_path=PATTERN_MAP_PATH,
        semantic_data_path=SEMANTIC_DATA_PATH,
        sentence_data_path=SENTENCE_DATA_PATH
    ):
        self.f_categories = []
        self.f_verbs = []
        self.verbs = []
        self.f_patterns = []
        self.patterns = []
        self.patterns_map = {}
        self.semantics = []
        self.sentences = []
        # >>> init list
        self.init_f_categories(f_category_data_path)
        self.init_f_verbs(f_verb_data_path)
        self.init_verbs(verb_data_path)
        self.init_f_patterns(f_pattern_data_path)
        self.init_patterns(pattern_data_path, pattern_map_path)
        self.init_semantics(semantic_data_path)
        self.init_sentences(sentence_data_path)
        # >>> cache
        self.similar_verbs_cache = {}
        self.category_verbs_cache = {}
        self.find_f_categories_by_verb_cache = {}
        self.antisense_verbs_cache = {}
        self.antisense_f_category_ids_cache = {}

    def init_f_categories(self, f_category_data_path=F_CATEGORY_DATA_PATH):
        with open(f_category_data_path, 'r', encoding='utf-8') as f_category_data_file:
            category_data = json.load(f_category_data_file)
        for f_category in category_data:
            self.f_categories.append(FuncCategory(
                id=f_category['id'],
                name=f_category['name'],
                create_time=f_category['create_time'],
                definition=f_category['definition'],
                description=f_category['description'],
                modified_time=f_category['modified_time'],
                representative_verb=f_category['representative_verb'],
                antisense_category=f_category['antisense_category'],
                antisense_category_id=f_category['antisense_category_id'],
                included_verb=f_category['included_verb'],
                included_pattern=f_category['included_pattern'],
                version=f_category['version'],
                example=f_category['example'],
            ))

    def init_f_verbs(self, f_verb_data_path=F_VERB_DATA_PATH):
        with open(f_verb_data_path, 'r', encoding='utf-8') as f_verb_file:
            f_verb_data = json.load(f_verb_file)
        for f_verb in f_verb_data:
            self.f_verbs.append(FuncVerb(
                id=f_verb['id'],
                qualified_name=f_verb['qualified_name'],
                name=f_verb['name'],
                description=f_verb['description'],
                example=f_verb['example'],
                create_time=f_verb['create_time'],
                version=f_verb['version']
            ))

    def init_verbs(self, verb_data_path=VERB_DATA_PATH):
        with open(verb_data_path, 'r', encoding='utf-8') as verb_file:
            verb_data = json.load(verb_file)
        for verb in verb_data:
            self.verbs.append(Verb(
                id=verb['id'],
                name=verb['name'],
                description=verb['description'],
                create_time=verb['create_time'],
                version=verb['version']
            ))

    def init_f_patterns(self, f_pattern_data_path=F_PATTERN_DATA_PATH):
        with open(f_pattern_data_path, 'r', encoding='utf-8') as f_pattern_file:
            f_pattern_data = json.load(f_pattern_file)
        for f_pattern in f_pattern_data:
            self.f_patterns.append(FuncPattern(
                id=f_pattern['id'],
                qualified_name=f_pattern['qualified_name'],
                example=f_pattern['example'],
                description=f_pattern['description'],
                included_roles=f_pattern['included_roles'],
                create_time=f_pattern['create_time'],
                version=f_pattern['version']
            ))

    def init_patterns(self, pattern_data_path=PATTERN_DATA_PATH, pattern_map_path=PATTERN_MAP_PATH):
        with open(pattern_data_path, 'r', encoding='utf-8') as pattern_file:
            pattern_data = json.load(pattern_file)
        for pattern in pattern_data:
            self.patterns.append(Pattern(
                id=pattern['id'],
                syntax=pattern['syntax'],
                example=pattern['example'],
                description=pattern['description'],
                included_roles=pattern['included_roles'],
                create_time=pattern['create_time'],
                version=pattern['version']
            ))
        with open(pattern_map_path, 'rb') as pattern_file:
            self.patterns_map = pickle.load(pattern_file)

    def init_semantics(self, semantic_data_path=SEMANTIC_DATA_PATH):
        with open(semantic_data_path, 'r', encoding='utf-8') as semantic_data_file:
            semantic_data = json.load(semantic_data_file)
        for semantic in semantic_data:
            self.semantics.append(Semantic(
                id=semantic['id'],
                name=semantic['name'],
                definition=semantic['definition'],
                create_time=semantic['create_time'],
                version=semantic['version']
            ))

    def init_sentences(self, sentence_data_path=SENTENCE_DATA_PATH):
        df = pd.read_csv(sentence_data_path)
        for index, row in df.iterrows():
            self.sentences.append(Sentence(
                single_description=row['single_description'],
                category=row['final_annotation_type'],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                version='1.0'
            ))

    @staticmethod
    def __is_valid_id(_id: int, _list: list):
        if not isinstance(_id, int):
            return False
        for item in _list:
            if item.id == _id:
                return True
        return False

    @staticmethod
    def __is_valid_name(_name: str, _list: list):
        if not str.isalpha(_name):
            return False
        for item in _list:
            if item.name == _name:
                return True
        return False

    # >>> f_category

    def is_valid_f_category_id(self, f_category_id: int):
        if isinstance(f_category_id, int):
            if 0 < f_category_id < len(self.f_categories):
                return True
            return False
        else:
            return False

    def get_f_category_number(self):
        return len(self.f_categories)

    def find_f_category_by_id(self, id: int):
        for cate in self.f_categories:
            if cate.id == id:
                return cate
        return None

    def find_f_category_by_name(self, name: str):
        for f_category in self.f_categories:
            if f_category.name == name:
                return f_category
        return None

    def find_f_category_by_verb(self, verb):
        for f_category in self.f_categories:
            for included_verb in f_category.included_verb:
                if included_verb == verb:
                    return f_category
        return None

    def find_f_category_by_pattern(self, pattern):
        for f_category in self.f_categories:
            for included_pattern in f_category.included_pattern:
                if included_pattern == pattern:
                    return f_category
        return None

    def find_f_categories_by_pattern(self, pattern):
        if self.is_valid_pattern(pattern):
            f_categories = []
            for f_category in self.f_categories:
                for p in f_category.included_pattern:
                    if p == pattern:
                        f_categories.append(f_category)
            return f_categories
        else:
            return []

    def find_f_categories_by_verb(self, verb):
        if self.is_valid_verb(verb):
            f_categories = []
            for cate in self.f_categories:
                for v in cate.included_verb:
                    if v == verb:
                        f_categories.append(cate)
            return f_categories
        else:
            return None

    def find_f_categories_with_two_verbs(self, verb1, verb2):
        if self.is_valid_verb(verb1) and self.is_valid_verb(verb2) is True:
            f_categories = []
            f_categories1 = self.find_f_categories_by_verb(verb1)
            f_categories2 = self.find_f_categories_by_verb(verb2)
            for cate1 in f_categories1:
                for cate2 in f_categories2:
                    if cate1.id == cate2.id:
                        f_categories.append(cate1)
            if f_categories is not None:
                return f_categories
            else:
                return []
        else:
            return []

    def find_f_categories_by_semantic(self, semantic):
        if self.is_valid_semantic_name(semantic):
            patterns = self.find_patterns_by_semantics_name(semantic)
            result = []
            f_categories = []
            for pattern in patterns:
                result.append(self.find_f_category_by_pattern(pattern.syntax))
            for f_category in result:
                if f_category not in f_categories:
                    f_categories.append(f_category)
            return f_categories
        else:
            return []

    @staticmethod
    def find_category_by_sentence(sentence):
        classifier = FuncSentenceClassifier()
        return classifier.predict(sentence)

    def find_antisense_categories_by_category(self, category_id):
        if self.is_valid_f_category_id(category_id):
            for cate in self.f_categories:
                if cate.id == category_id:
                    return cate.antisense_category
        else:
            return []

    def find_antisense_category_ids_by_category(self, category_id):
        if self.is_valid_f_category_id(category_id):
            for cate in self.f_categories:
                if cate.id == category_id:
                    return cate.antisense_category_id
        else:
            return []

    def find_antisense_categories_by_verb(self, verb):
        if self.is_valid_verb(verb):
            result = []
            f_categories = self.find_f_categories_by_verb(verb)
            for f_category in f_categories:
                antisense_categories = self.find_antisense_categories_by_category(f_category.id)
                for antisense_category in antisense_categories:
                    result.append(antisense_category)
            result = list(set(result))
            return result
        else:
            return []

    def find_antisense_category_ids_by_verb(self, verb):
        if self.is_valid_verb(verb):
            result = []
            f_categories = self.find_f_categories_by_verb(verb)
            for f_category in f_categories:
                antisense_category_ids = self.find_antisense_category_ids_by_category(f_category.id)
                for antisense_category_id in antisense_category_ids:
                    result.append(antisense_category_id)
            result = list(set(result))
            return result
        else:
            return []

    # >>> f_verb

    def is_valid_f_verb(self, f_verb):
        if str.isalpha(f_verb):
            for cate in self.f_categories:
                if f_verb in [_ for _ in self.find_all_verb_name_by_f_category_id(cate.id)]:
                    return True
            return False
        else:
            return False

    def find_f_verb_by_name(self, name):
        for f_verb in self.f_verbs:
            if f_verb.name == name:
                return f_verb
        return None

    def find_f_verb_by_id(self, id):
        for f_verb in self.f_verbs:
            if f_verb.id == id:
                return f_verb
        return None

    def is_valid_verb(self, verb):
        return self.__is_valid_name(verb, self.verbs)

    def get_verb_number(self):
        return len(self.verbs)

    def find_verb_by_id(self, id):
        for verb in self.verbs:
            if verb.id == id:
                return verb
        return None

    def find_verb_by_name(self, name):
        for verb in self.verbs:
            if verb.name == name:
                return verb
        return None

    def find_all_verb_by_f_category_id(self, f_category_id):
        verbs = []
        if self.is_valid_f_category_id(f_category_id) is True:
            for f_category in self.f_categories:
                if f_category.id == f_category_id:
                    for verb in f_category.included_verb:
                        verbs.append(self.find_verb_by_name(verb))
            return verbs
        else:
            return []

    def find_all_verb_name_by_f_category_id(self, f_category_id):
        if self.is_valid_f_category_id(f_category_id) is True:
            for f_category in self.f_categories:
                if f_category.id == f_category_id:
                    return f_category.included_verb
        else:
            return []

    def get_included_verb_number_by_f_category_id(self, f_category_id):
        if self.is_valid_f_category_id(f_category_id):
            f_category = self.find_f_category_by_id(f_category_id)
            return len(self.find_all_verb_name_by_f_category_id(f_category.id))
        else:
            return None

    def find_common_verbs_with_two_f_categories(self, f_category1, f_category2):
        if self.is_valid_f_category_id(f_category1) and self.is_valid_f_category_id(f_category2) is True:
            verbs1 = self.find_all_verb_name_by_f_category_id(f_category1)
            verbs2 = self.find_all_verb_name_by_f_category_id(f_category2)
            common_verbs = []
            for verb1 in verbs1:
                for verb2 in verbs2:
                    if verb1 == verb2:
                        common_verbs.append(verb1)
                    continue
            return common_verbs
        else:
            return []

    def find_antisense_verbs_by_verb(self, verb):
        if self.is_valid_verb(verb):
            if verb in self.antisense_verbs_cache.keys():
                return self.antisense_verbs_cache[verb]
            else:
                antisense_verbs = []
                if verb in self.antisense_f_category_ids_cache:
                    f_category_ids = self.antisense_f_category_ids_cache[verb]
                else:
                    f_category_ids = self.find_antisense_category_ids_by_verb(verb)
                for f_category_id in f_category_ids:
                    if f_category_id in self.category_verbs_cache.keys():
                        antisense_verbs.extend(self.category_verbs_cache[f_category_id])
                    else:
                        antisense_verbs.extend(self.find_all_verb_name_by_f_category_id(f_category_id))
                antisense_verbs = list(set(antisense_verbs))
                return antisense_verbs
        else:
            return []

    def find_similar_verbs_by_verb(self, verb):
        if self.is_valid_verb(verb):
            if verb in self.similar_verbs_cache.keys():
                return self.similar_verbs_cache[verb]
            similar_verbs = []
            if verb in self.find_f_categories_by_verb_cache.keys():
                categories = self.find_f_categories_by_verb_cache[verb]
            else:
                categories = self.find_f_categories_by_verb(verb)
                self.find_f_categories_by_verb_cache[verb] = categories
            if categories is None:
                return []
            for category in categories:
                if category.id in self.category_verbs_cache.keys():
                    similar_verbs.extend(self.category_verbs_cache[category.id])
                else:
                    similar_verbs.extend(self.find_all_verb_name_by_f_category_id(category.id))
            similar_verbs = list(set(similar_verbs))
            self.similar_verbs_cache[verb] = similar_verbs
            return self.similar_verbs_cache[verb]
        else:
            return []

    # >>> f_pattern

    def is_valid_f_pattern(self, f_pattern):
        if isinstance(f_pattern, str):
            for cate in self.f_categories:
                if f_pattern in [_ for _ in self.find_all_pattern_name_by_f_category_id(cate.id)]:
                    return True
            return False
        else:
            return False

    def is_valid_pattern_id(self, pattern_id):
        return self.__is_valid_id(pattern_id, self.patterns)

    def is_valid_pattern(self, syntax):
        if isinstance(syntax, str):
            if syntax in self.patterns_map:
                return True
            # for pattern in self.patterns:
            #     if pattern.syntax == syntax:
            #         return True
            return False
        else:
            return False

    def get_pattern_id_by_syntax(self, syntax):
        if not self.is_valid_pattern(syntax):
            return None
        return self.patterns_map[syntax]

    def get_pattern_number(self):
        return len(self.patterns)

    def find_pattern_by_id(self, id):
        for pattern in self.patterns:
            if pattern.id == id:
                return pattern
        return None

    def find_pattern_by_syntax(self, syntax):
        for pattern in self.patterns:
            if pattern.syntax == syntax:
                return pattern
        return None

    def find_all_pattern_by_f_category_id(self, f_category_id):
        if self.is_valid_f_category_id(f_category_id) is True:
            patterns = []
            for f_category in self.f_categories:
                if f_category.id == f_category_id:
                    for syntax in f_category.included_pattern:
                        patterns.append(self.find_pattern_by_syntax(syntax))
            return patterns
        else:
            return []

    def find_all_pattern_name_by_f_category_id(self, f_category_id):
        if self.is_valid_f_category_id(f_category_id) is True:
            for f_category in self.f_categories:
                if f_category.id == f_category_id:
                    return f_category.included_pattern
        else:
            return []

    def find_patterns_by_semantic_id(self, semantic_id):
        if self.is_valid_semantic_id(semantic_id):
            semantic_name = self.find_semantic_name_by_id(semantic_id)
            patterns = []
            for pattern in self.patterns:
                for role in pattern.included_roles:
                    if role == semantic_name:
                        patterns.append(pattern)
            return patterns
        else:
            return []

    def find_patterns_by_semantics_name(self, semantic_name):
        if self.is_valid_semantic_name(semantic_name):
            patterns = []
            for pattern in self.patterns:
                for role in pattern.included_roles:
                    if role == semantic_name:
                        patterns.append(pattern)
            return patterns
        else:
            return []

    def find_patterns_with_two_semantics_id(self, semantic1_id, semantic2_id):
        if self.is_valid_semantic_id(semantic1_id) and self.is_valid_semantic_id(semantic2_id) is True:
            patterns = []
            patterns1 = self.find_patterns_by_semantic_id(semantic1_id)
            patterns2 = self.find_patterns_by_semantic_id(semantic2_id)
            for pattern1 in patterns1:
                for pattern2 in patterns2:
                    if pattern1 == pattern2:
                        patterns.append(pattern1)
            return patterns
        else:
            return []

    def find_patterns_with_two_semantics_name(self, semantics1_name, semantics2_name):
        if self.is_valid_semantic_name(semantics1_name) and self.is_valid_semantic_name(semantics2_name) is True:
            patterns = []
            patterns1 = self.find_patterns_by_semantics_name(semantics1_name)
            patterns2 = self.find_patterns_by_semantics_name(semantics2_name)
            for pattern1 in patterns1:
                for pattern2 in patterns2:
                    if pattern1 == pattern2:
                        patterns.append(pattern1)
            return patterns
        else:
            return []

    def find_common_patterns_with_two_f_categories(self, f_category1, f_category2):
        if self.is_valid_f_category_id(f_category1) and self.is_valid_f_category_id(f_category2):
            patterns1 = self.find_all_pattern_name_by_f_category_id(f_category1)
            patterns2 = self.find_all_pattern_name_by_f_category_id(f_category2)
            common_patterns = []
            for pattern1 in patterns1:
                for pattern2 in patterns2:
                    if pattern1 == pattern2:
                        common_patterns.append(pattern1)
                    continue
            return common_patterns
        else:
            return []

    def get_included_pattern_number_by_f_category_id(self, cate_id):
        if self.is_valid_f_category_id(cate_id):
            cate = self.find_f_category_by_id(cate_id)
            return len(self.find_all_pattern_name_by_f_category_id(cate.id))
        else:
            return None

    # >> semantic

    def is_valid_semantic_id(self, semantic_id: int):
        return self.__is_valid_id(semantic_id, self.semantics)

    def is_valid_semantic_name(self, semantic_name):
        return self.__is_valid_name(semantic_name, self.semantics)

    def get_semantic_number(self):
        return len(self.semantics)

    def find_semantic_by_id(self, id):
        for role in self.semantics:
            if role.id == id:
                return role
        return None

    def find_semantic_by_name(self, name):
        for role in self.semantics:
            if role.name == name:
                return role
        return None

    def find_semantic_name_by_id(self, id):
        if self.is_valid_semantic_id(id):
            role = self.find_semantic_by_id(id)
            return role.name
        else:
            return None

    def find_semantic_definition_by_id(self, id):
        if self.is_valid_semantic_id(id):
            role = self.find_semantic_by_id(id)
            return role.definition
        else:
            return None

    def find_semantic_definition_by_name(self, role_name):
        if self.is_valid_semantic_name(role_name):
            role = self.find_semantic_by_name(role_name)
            return role.definition
        else:
            return None

    def is_semantic_included_in_pattern(self, semantic_name):
        if self.is_valid_semantic_name(semantic_name):
            for pattern in self.patterns:
                if semantic_name in [_ for _ in self.find_included_semantics_by_pattern_id(pattern.id)]:
                    return True
            return False
        else:
            return False

    def find_included_semantics_by_pattern_id(self, pattern_id):
        if self.is_valid_pattern_id(pattern_id) is True:
            for pattern in self.patterns:
                if pattern.id == pattern_id:
                    return pattern.included_roles
        else:
            return None

    def find_all_semantics_by_f_category_id(self, f_category_id):
        if self.is_valid_f_category_id(f_category_id) is True:
            role_list = []
            result = []
            patterns = self.find_all_pattern_name_by_f_category_id(f_category_id)
            for pattern_name in patterns:
                pattern = self.find_pattern_by_syntax(pattern_name)
                semantics = self.find_included_semantics_by_pattern_id(pattern.id)
                for role in semantics:
                    role_list.append(role)
            role_name = list(set(role_list))
            for role in role_name:
                result.append(self.find_semantic_by_name(role))
            return result
        else:
            return []

    def get_included_semantics_number_by_pattern_id(self, pattern_id):
        if self.is_valid_pattern_id(pattern_id):
            pattern = self.find_pattern_by_id(pattern_id)
            return len(self.find_included_semantics_by_pattern_id(pattern.id))
        else:
            return None

    def find_common_roles_with_two_pattern_ids(self, pattern_id1, pattern_id2):
        if self.is_valid_pattern_id(pattern_id1) and self.is_valid_pattern_id(pattern_id2) is True:
            roles1 = self.find_included_semantics_by_pattern_id(pattern_id1)
            roles2 = self.find_included_semantics_by_pattern_id(pattern_id2)
            common_roles = []
            for role1 in roles1:
                for role2 in roles2:
                    if role1 == role2:
                        common_roles.append(role1)
                    continue
            return common_roles
        else:
            return []

    # >>> sentence

    def find_sentences_by_f_category_id(self, f_category_id):
        if self.is_valid_f_category_id(f_category_id):
            sentences = []
            for sentence in self.sentences:
                if int(sentence.category) == f_category_id:
                    sentences.append(sentence)
            return sentences
        else:
            return []

    def get_sentences(self):
        return self.sentences
