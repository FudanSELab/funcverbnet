#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/11
------------------------------------------
@Modify: 2022/03/11
------------------------------------------
@Description:
"""
import spacy
from spacy.tokens import Doc, Token
import textdistance
from tqdm import tqdm
import pandas as pd

from funcverbnet.nodes.funcverbnet import FuncVerbNet
from funcverbnet.utils import load_pdata
from funcverbnet.classifier.sentence_classifier import FuncSentenceClassifier

HEURISTIC_RULES_PATH = load_pdata("heuristic_rules.txt")
SPLIT_STR = ' - '


# import time


# def cal_time(func):
#     def wrapper(*args, **kwargs):
#         t1 = time.perf_counter()
#         result = func(*args, **kwargs)
#         t2 = time.perf_counter()
#         print("%s running time: %s sec." % (func.__name__, t2 - t1))
#         return result
#
#     return wrapper


class TemplateExtractor:
    def __init__(self):
        self.net = FuncVerbNet()
        self.classifier = FuncSentenceClassifier()
        self.nlp = spacy.load('en_core_web_sm')

    def preprocess_sentence(self, sentence: str) -> str:
        """
        Preprocess sentence, remove '[icu]', '-', replace 'in to' with 'into'
        :param sentence:
        :return:
        """
        if not sentence:
            return sentence
        sentence = sentence.split(';')[0].replace('[icu]', '').replace('-', '').replace(' in to ', ' into ').strip()
        if sentence[0].isupper():
            sentence = sentence[0].lower() + sentence[1:]
        sentence = self.eliminate_bracket(sentence)
        return sentence

    @staticmethod
    def eliminate_bracket(sentence: str):
        """
        Eliminate the brackets and the contents in brackets.
        :param sentence:
        :return:
        """
        if not sentence:
            return None
        while '(' in sentence and ')' in sentence:
            l_bracket, r_bracket = sentence.find('('), sentence.find(')')
            l_bracket += sentence[l_bracket + 1: r_bracket].rfind('(') + 1
            sentence = sentence.replace(sentence[l_bracket: r_bracket + 1], '')
        return sentence

    @staticmethod
    def __load_heuristic_rules(heuristic_rule_path=HEURISTIC_RULES_PATH) -> dict:
        """
        Define some heuristic rules, load and format them based on the requirements of Spacy NLP.
        :param heuristic_rule_path:
        :return:
        """
        heuristic_rule_2_custom_patterns = {}
        if not heuristic_rule_path:
            return heuristic_rule_2_custom_patterns
        with open(heuristic_rule_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            line_str = line.replace('\n', '')
            cate_id, word, lemma, pos = line_str.split('\t')
            cate_id = int(cate_id)
            if cate_id not in heuristic_rule_2_custom_patterns:
                heuristic_rule_2_custom_patterns[cate_id] = [{
                    "patterns": [[{'ORTH': word}]],
                    "attrs": {'LEMMA': lemma, "POS": pos, 'TAG': pos}
                }]
                continue
            heuristic_rule_2_custom_patterns[cate_id].append({
                "patterns": [[{'ORTH': word}]],
                "attrs": {'LEMMA': lemma, "POS": pos, 'TAG': pos}
            })
        return heuristic_rule_2_custom_patterns

    def __run_heuristic_rules(self, cate_id, nlp):
        """
        Load heuristic rules to Spacy NLP according category.
        :param cate_id:
        :param nlp: custom_nlp
        :return:
        """
        heuristic_rule_2_custom_patterns = self.__load_heuristic_rules(HEURISTIC_RULES_PATH)
        if not cate_id or not heuristic_rule_2_custom_patterns:
            return nlp
        ruler = nlp.get_pipe('attribute_ruler')
        ruler.add_patterns(heuristic_rule_2_custom_patterns[cate_id] + heuristic_rule_2_custom_patterns[-1])
        return nlp

    @staticmethod
    def __is_in_categories(token: Token, f_category_incl_verbs: list):
        """
        Sentences will be classified into 88 categories, judge whether the parsed token is the core verb in category.
        :param token:
        :param f_category_incl_verbs:
        :return:
        """
        assert isinstance(token, Token)
        if not f_category_incl_verbs:
            return False
        if token.lemma_.lower() in f_category_incl_verbs:
            return True
        for _ in f_category_incl_verbs:
            if ' ' in _:
                _ = _.split(' ')[0]
            if textdistance.hamming.distance(token.lemma_.lower(), _) < 2:
                return True
        return False

    @staticmethod
    def list_token_with_pos(doc: Doc):
        return [(token, token.pos_, token.dep_) for token in doc]

    def construct_sentence_dependency(self, doc: Doc, f_category_incl_verbs: list):
        assert isinstance(doc, Doc)
        sentence_structure = []
        if not f_category_incl_verbs:
            return sentence_structure
        # print(self.list_token_with_pos(doc))
        root: Token = [token for token in doc if token.head == token][0]
        if not root:
            return sentence_structure
        flag = False
        # print('ROOT:', root, root.pos_, root.dep_)
        # >>> update root if root's pos_ is NOUN, traverse lefts (maybe in NOUN lefts
        if root.pos_ == 'NOUN' or not self.__is_in_categories(root, f_category_incl_verbs):
            for left in [_ for _ in root.lefts]:
                if self.__is_in_categories(left, f_category_incl_verbs):
                    root = left
                    flag = True
                    break
        # >>> update root if root's pos_ is not VERB or NOUN, traverse rights
        if root.pos_ != 'VERB' and not flag:
            for right in [_ for _ in root.rights]:
                if self.__is_in_categories(right, f_category_incl_verbs):
                    root = right
                    break
        # >>> no root, return []
        if root.pos_ != 'VERB':
            print('ROOT POS NOT VALID')
            return sentence_structure
        # >>> construct sentence dependency
        sentence_structure.append(root)
        # >>> verb usually the root of sentence, traverse rights for parsing.
        for right in [_ for _ in root.rights]:
            # print('RIGHT:', right, right.pos_, right.dep_)
            # >>> filter some non-conforming right(Token)
            if right.pos_ == 'PUNCT' or right.dep_ == 'punct':
                continue
            # if right.dep_ in ['amod', 'conj', 'cc']:
            #     continue
            if right.dep_ == 'amod':
                continue
            if right.pos_ not in ['NOUN', 'VERB', 'AUX', 'PROPN', 'PART', 'NUM', 'DET'] and right.dep_ != 'prep':
                continue
            # >>> process rights now
            # print('RIGHT:', right, right.pos_, right.dep_)
            if right.dep_ == 'prep':
                # filter (right.pos_ != 'ADP' or right.pos_ == 'SCONJ) and right.text != 'as'
                if right.pos_ != 'ADP' and right.text != 'as':
                    continue
                sentence_structure.append(right)
                sentence_structure.extend([_ for _ in right.rights if _.pos_ != 'PUNCT' or _.dep_ != 'punct'])
            elif right.pos_ == 'DET' or right.pos_ == 'NUM':
                if right.dep_ != 'dobj':
                    continue
                tmp = [right]
                while len(tmp) > 0:
                    last = tmp.pop()
                    sentence_structure.append(last)
                    tmp.extend([_ for _ in last.rights][::-1])
            # >>> process shared dependents and effective parents in coordination
            elif right.dep_ == 'conj' or right.dep_ == 'cc':
                continue
            elif right.pos_ == 'VERB' or right.pos_ == 'AUX':
                for rl in [_ for _ in right.lefts]:
                    # print('RIGHT_LEFT:', rl, rl.pos_, rl.dep_)
                    if rl.dep_ == 'mark':
                        sentence_structure.append(rl)
                        break
                    if rl.pos_ == 'ADV' and rl.dep_ == 'advmod' and rl.text == 'when':
                        sentence_structure.append(rl)
                        break
                if right.dep_ not in ['prep', 'acl', 'xcomp', 'pcomp', 'ccomp'] and 'advcl' not in right.dep_:
                    sentence_structure.append(right)
            elif right not in sentence_structure:
                sentence_structure.append(right)
        # print('HALF_SENTENCE:', sentence)
        last = sentence_structure[-1]
        # print('LASE:', last, last.pos_, last.dep_)
        last_lefts = [_ for _ in last.rights]
        while len(last_lefts) > 0:
            for left in last_lefts:
                if left.pos_ == 'PUNCT' and left.dep_ == 'punct':
                    continue
                # print('LEFT:', left, left.pos_, left.dep_)
                if 'obj' in left.dep_ or left.dep_ == 'cc':
                    sentence_structure.append(left)
                elif (left.dep_ == 'prep' and left.pos_ != 'VERB') or left.dep_ == 'conj' or left.dep_ == 'pcomp':
                    sentence_structure.append(left)
                    sentence_structure.extend([_ for _ in left.rights if _.pos_ != 'PUNCT' or _.dep_ != 'punct'])
            if last == sentence_structure[-1]:
                last_lefts = []
            else:
                last = sentence_structure[-1]
                last_lefts = [_ for _ in last.rights if _.pos_ != 'PUNCT' or _.dep_ != 'punct']
        # print('FINAL_SENTENCE:', sentence_structure)
        return sentence_structure

    @staticmethod
    def structure_token_pos_verb(sentence_structure):
        token_pos_list = []
        core_verb = None
        if not sentence_structure:
            return token_pos_list, core_verb
        # root: Token = sentence_structure[0]
        # print('ROOT:', root, root.pos_)
        # if not self.__is_in_categories(root, f_category_incl_verbs):
        #     core_verb = root.text
        #     return token_pos_list, core_verb
        # >>> structure token with pos, judge the core verb
        flag = False
        for token in sentence_structure:
            token_pos_list.append([token, token.pos_])
            if token.pos_ == 'VERB' and not flag:
                core_verb = token.lemma_
                flag = True
        # print('ORIG_TOKEN_POS:', token_pos_list)
        # >>> process conj.(e.g. and, or) and form them to phrase
        cc_indexes = [_ for _ in range(len(token_pos_list)) if token_pos_list[_][0].dep_ == 'cc']
        # print('CC_INDEXES:', cc_indexes)
        cc_compound_list = []
        for cc_index in cc_indexes:
            cc = sentence_structure[cc_index]
            # print('CC:', cc)
            cc_compound = []
            for (token, pos) in token_pos_list:
                token_rights = [_ for _ in token.rights]
                if cc not in token_rights:
                    continue
                # print('TOKEN_RIGHTS:', token_rights)
                cc_in_rights_index = token_rights.index(cc)
                if cc_in_rights_index == -1:
                    continue
                cc_compound.append(token)
                cc_compound.extend(token_rights[:cc_in_rights_index + 1])
                children_queue = token_rights[cc_in_rights_index + 1:][::-1]
                while len(children_queue) > 0:
                    child = children_queue.pop()
                    if child.dep_ == 'conj' or child in sentence_structure:
                        cc_compound.append(child)
                        children_queue.extend([_ for _ in child.rights][::-1])
                # print('CC_COMPOUND:', cc_compound)
            cc_compound_list.append(cc_compound)
        # print('CC_COMPOUND_LIST:', cc_compound_list)
        # >>> tokens replace with cc_compound
        tokens_pos_list = []
        if len(cc_compound_list) > 0:
            i, j, count = 0, 0, 0
            while i < len(token_pos_list) and j < len(cc_compound_list):
                token = token_pos_list[i]
                i += 1
                if token[0] not in cc_compound_list[j]:
                    tokens_pos_list.append(token)
                    continue
                count += 1
                if count == len(cc_compound_list[j]):
                    tokens_pos_list.append([cc_compound_list[j], 'cc_compound'])
                    j += 1
                    count = 0
            # TODO: 处理cc_compound包含token_pos_list
            while j < len(cc_compound_list):
                tokens_pos_list.append([cc_compound_list[j], 'cc_compound'])
                j += 1
        else:
            tokens_pos_list = token_pos_list
        # if not tokens_pos_list:
        #     print('NO TOKENS POS')
        #     return tokens_pos_list, core_verb
        # print('HALF_TOKENS_POS:', tokens_pos_list)
        # >>> convert pos identifiers to the same representation
        for i, (token, pos) in enumerate(tokens_pos_list):
            if pos in ['n', 'PROPN', 'PRON', 'ADJ', 'DET', 'X']:
                tokens_pos_list[i][1] = 'NOUN'
            elif pos == 'ADP':
                tokens_pos_list[i][1] = 'PREP'
            elif pos == 'v':
                tokens_pos_list[i][1] = 'VERB'
            elif pos == 'SCONJ':
                if token.text == 'as':
                    tokens_pos_list[i][1] = 'PREP'
            elif pos == 'VERB':
                for left in [_ for _ in token.lefts]:
                    if (left.pos_ == 'DET' or left.dep_ == 'det') and left.text != 'that':
                        tokens_pos_list[i][1] = 'NOUN'
                        break
            elif pos == 'cc_compound':
                cc_index = [_ for _ in range(len(token)) if token[_].dep_ == 'cc'][0]
                # print('INDEX:', cc_index)
                if cc_index + 1 < len(token):
                    tmp: Token = token[cc_index + 1]
                    if tmp.pos_ == 'VERB':
                        tokens_pos_list[i][1] = 'VERB - NOUN'
                    elif tmp.pos_ == 'ADP':
                        tokens_pos_list[i][1] = 'PREP - NOUN'
                    elif tmp.pos_ == 'NOUN' or tmp.pos_ == 'PROPN' or tmp.pos_ == 'PRON':
                        tokens_pos_list[i][1] = 'NOUN'
                    else:
                        tokens_pos_list[i][1] = 'NOUN'
                else:
                    tokens_pos_list[i][1] = 'NOUN'
            tokens_pos_list[i][0] = token if type(token) == list else [token]
        # print('HALF_TOKENS_POS:', tokens_pos_list)
        # >>> combine the continuous tokens with the same pos to form a phrase
        final_tokens_pos_list = []
        pre_pos = tokens_pos_list[0]
        pos_group = pre_pos
        for i, (tokens, pos) in enumerate(tokens_pos_list[1:]):
            if pos == pre_pos[1]:
                pos_group[0].extend(tokens)
                continue
            final_tokens_pos_list.append(pos_group)
            pre_pos = tokens_pos_list[i + 1]
            pos_group = pre_pos
        if not final_tokens_pos_list or pos_group[1] != final_tokens_pos_list[-1][1]:
            final_tokens_pos_list.append(pos_group)
        # print('FINAL_TOKENS_POS:', final_tokens_pos_list)
        return final_tokens_pos_list, core_verb

    def structure_sentence(self, sentence, nlp, f_category_incl_verbs: list):
        """

        :param sentence:
        :param nlp:
        :param f_category_incl_verbs:
        :return: tokens_pos_list, core_verb
        """
        if not sentence:
            return None
        doc: Doc = nlp(sentence)
        return self.structure_token_pos_verb(self.construct_sentence_dependency(doc, f_category_incl_verbs))

    @staticmethod
    def __has_of_in_sentence(token_pos_list: list):
        if not token_pos_list:
            return False
        for i, (tokens, pos) in enumerate(token_pos_list):
            for token in tokens:
                if token.text == 'of':
                    return True
        return False

    @staticmethod
    def __is_token_already_in(token, token_pos_list: list):
        if not token or not token_pos_list:
            return False
        for i, (tokens, pos) in enumerate(token_pos_list):
            if token in tokens:
                return True
        return False

    @staticmethod
    def construct_of_in_phrase(tokens_pos_list: list):
        """
        :param tokens_pos_list: List[Tuple[List[Token], str]]
        :return:
        """
        if not tokens_pos_list:
            return []
        of_indexes = []
        for i, (tokens, pos) in enumerate(tokens_pos_list):
            if pos == 'PREP' and (tokens[0].text == 'of' or tokens[0].text == 'per'):
                of_indexes.append(i)
        if not of_indexes:
            return tokens_pos_list
        # print('OF_INDEXES', of_indexes)
        # >>> combine the index of the 'of' phrase
        for of_index in of_indexes.copy():
            left = of_index - 1
            if 0 <= left < len(tokens_pos_list) and left not in of_indexes:
                of_indexes.append(left)
            right = of_index + 1
            if 0 <= right < len(tokens_pos_list) and right not in of_indexes:
                of_indexes.append(right)
        of_indexes.sort()
        # print('OF_INDEXES', of_indexes)
        # >>> split 'of' indexes list with discontinuous index
        of_indexes_list = []
        pre = 0
        for i in range(1, len(of_indexes)):
            if of_indexes[i] - of_indexes[i - 1] == 1:
                continue
            of_indexes_list.append(of_indexes[pre: i])
            pre = i
        of_indexes_list.append(of_indexes[pre:])
        # >>> combine the 'of' to form a 'of' phrase
        # if of_indexes_list == [[]]:
        #     return token_pos_list
        final_tokens_pos_list = []
        i, j = 0, 0
        while i < len(tokens_pos_list) and j < len(of_indexes_list):
            while i < of_indexes_list[j][0]:
                final_tokens_pos_list.append(tokens_pos_list[i])
                i += 1
            of_compound = []
            [of_compound.extend(_[0]) for _ in tokens_pos_list[of_indexes_list[j][0]: of_indexes_list[j][-1] + 1]]
            final_tokens_pos_list.append([of_compound, 'COMPOUND_NOUN'])
            i = of_indexes_list[j][-1] + 1
            j += 1
        if i < len(tokens_pos_list):
            final_tokens_pos_list.extend(tokens_pos_list[i:])
        # print('FINAL_TOKENS_POS:', final_tokens_pos_list)
        return final_tokens_pos_list

    def process_noun(self, tokens: list, tokens_pos_list: list):
        stop_words = ['a', 'an', 'the', 'that', 'these', 'those']
        noun_sequence = ''
        new_tokens = []
        if not tokens or not tokens_pos_list:
            return noun_sequence, [new_tokens, 'COMPOUND_NOUN']
        # print('TOKENS:', tokens)
        if len(tokens) == 1:
            # >>> traverse lefts
            for left in [_ for _ in tokens[0].lefts]:
                if left.text in stop_words:
                    continue
                # print('LEFT:', left, left.pos_, left.dep_)
                left_children = [_ for _ in left.lefts]
                # print('LEFT_CHILDREN:', left_children)
                if len(left_children) > 0:
                    tmp = ' '
                    for left_child in left_children:
                        if left_child.text in stop_words:
                            continue
                        tmp += left_child.text + ' '
                        new_tokens.append(left_child)
                    tmp += left.text + ' '
                    noun_sequence += tmp
                    new_tokens.append(left)
                else:
                    noun_sequence += left.text + ' '
                    new_tokens.append(left)
            # >>> append tokens[0] into last
            noun_sequence += tokens[0].text + ' '
            new_tokens.append(tokens[0])
            # print('HALF_TOKENS', new_tokens)
            # >>> traverse rights
            for right in [_ for _ in tokens[0].rights]:
                if right.dep_ == 'prep' and not self.__is_token_already_in(right, tokens_pos_list):
                    noun_sequence += right.text + ' '
                    new_tokens.append(right)
                    for right_child in [_ for _ in right.rights]:
                        noun_sequence += right_child.text + ' '
                        new_tokens.append(right_child)
            # print('FINAL_TOKENS', new_tokens)
        else:
            for token in tokens:
                # print('EVERY_TOKEN', token)
                for left in token.lefts:
                    if left.text in stop_words:
                        continue
                    # print('LEFT:', left, left.pos_, left.dep_)
                    noun_sequence += left.text + ' '
                    new_tokens.append(left)
                # print('STEP_TOKENS_FOR_' + token.text, new_tokens)
                noun_sequence += token.text + ' '
                new_tokens.append(token)
                # print('STEP_TOKENS_FOR_' + token.text, new_tokens)
                for right in token.rights:
                    if right in tokens:
                        continue
                    # print('RIGHT:', right)
                    noun_sequence += right.text + ' '
                    new_tokens.append(right)
            # print('FINAL_TOKENS', new_tokens)
        return noun_sequence.strip(), [new_tokens, 'COMPOUND_NOUN']

    def generate_sentence_template(self, sentence) -> dict:
        """
        Main function to generate sentence template
        :param sentence:
        :return:
        """
        if not sentence:
            return {}
        cate_id = self.classifier.predict(sentence)
        custom_nlp = self.__run_heuristic_rules(cate_id, self.nlp)
        f_category_incl_verbs = self.net.find_cate_by_id(cate_id).included_verb
        preprocessed_sentence = self.preprocess_sentence(sentence)
        tokens_pos_list, core_verb = self.structure_sentence(preprocessed_sentence, custom_nlp, f_category_incl_verbs)
        if not tokens_pos_list:
            return {}
        if self.__has_of_in_sentence(tokens_pos_list):
            tokens_pos_list = self.construct_of_in_phrase(tokens_pos_list)
        final_tokens_pos_list = []
        for (tokens, pos) in tokens_pos_list.copy():
            if pos == 'NOUN' or pos == 'COMPOUND_NOUN':
                noun_sequence, new_tokens_pos = self.process_noun(tokens, tokens_pos_list)
                final_tokens_pos_list.append(new_tokens_pos)
                continue
            final_tokens_pos_list.append([tokens, pos])
        # print('INPUT_TOKENS_POS:', final_tokens_pos_list)
        template, tokens_pos_list = self.construct_template(final_tokens_pos_list)
        return {'cate_id': cate_id, 'sentence': sentence, 'template': template, 'tokens_pos_list': tokens_pos_list}

    @staticmethod
    def construct_template(tokens_pos_list: list):
        template = []
        if not tokens_pos_list:
            return '', tokens_pos_list
        template.append(tokens_pos_list[0][1] if tokens_pos_list[0][1] != 'COMPOUND_NOUN' else 'NOUN')
        # print('FIRST_TEMP:', template)
        # if len(tokens_pos_list) == 1:
        #     return template, tokens_pos_list
        for i, (tokens, pos) in enumerate(tokens_pos_list[1:]):
            if pos == 'COMPOUND_NOUN':
                template.append('NOUN')
            elif pos in ['PART', 'ADV', 'SCONJ', 'PREP']:
                template.append(tokens[0].text)
            elif pos in ['VERB', 'VERB-NOUN']:
                # >>> VERB after PREP
                # print('VERB after PREP')
                if tokens_pos_list[i][1] == 'PREP':
                    template.extend(['doing', 'NOUN'] if 'NOUN' in pos else ['doing'])
                    continue
                flag = True
                # >>> VERB after PART
                print('VERB after PART')
                # print([(_, _.pos_) for _ in tokens[0].lefts])
                for left in [_ for _ in tokens[0].lefts]:
                    if left.pos_ == 'PART' and left.dep_ == 'aux':
                        template.extend(['to', 'do', 'NOUN'] if 'NOUN' in pos else ['to', 'do'])
                        flag = False
                        break
                if flag:
                    template.append(pos)
            else:
                template.append(pos)
        # print('FINAL_TEMP:', SPLIT_STR.join(template))
        # print('FINAL_TOKENS_POS:', tokens_pos_list)
        return SPLIT_STR.join(template), tokens_pos_list


if __name__ == '__main__':
    template_extractor = TemplateExtractor()
    # text = 'Use this function to retrieve the number.'
    # text = 'Prints a string representation of this digest output stream and its associated message digest object.'
    # text = "End the scope of a prefix-URI mapping."
    # text = "How can I send an email by Java application using Gmail, Yahoo?"
    # text = "How can I send an SMTP message from Java"
    text = "open or create a file and write in file"
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
    # text = "Stops dispatching events using this EventQueue."
    temp = template_extractor.generate_sentence_template(text)
    print(temp)
    # with open(read_data("sentences.csv"), 'r') as f:
    #     df = pd.read_csv(f)
    # for i, text in enumerate(df['single_description'][2000:3000]):
    #     try:
    #         temp = template_extractor.generate_sentence_template(text)
    #         print(temp['sentence'], temp['template'])
    #     except Exception as e:
    #         print(df['id'][i])
    #         print(e, e.__class__.__name__)
