#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/04/07
------------------------------------------
@Modify: 2022/04/07
------------------------------------------
@Description:
"""
import csv
import json
import pandas as pd
from tqdm import tqdm

from funcverbnet.errors import DataHandlerError
from funcverbnet.data_handler.pattern_matcher import PatternMatcher
from funcverbnet.data_handler.template_extractor import TemplateExtractor
from funcverbnet.utils import load_tmp, LogsUtil, walk_dir, tmp_folder

logger = LogsUtil.get_log_util()


def run1(filename):
    pattern_matcher = PatternMatcher()
    count = 0
    data = []
    with open(load_tmp(f'clean_{filename}.csv'), 'r') as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for item in tqdm(f_csv):
            try:
                mapped_template = pattern_matcher.mapping_template(item[1])
                if mapped_template:
                    data.append({
                        'id': item[0],
                        'functionality': mapped_template
                    })
                    count += 1
                if count % 5000 != 0:
                    continue
                tag = int(count / 5000)
                with open(load_tmp(f'{filename}_functionality_{tag}.json'), 'w') as json_f:
                    json.dump(data, json_f)
                data = []
            except DataHandlerError as ce:
                logger.info(ce, item[1])
            except Exception as e:
                logger.info(e)
    if count % 5000 != 0:
        tag = int(count / 5000) + 1
        with open(load_tmp(f'{filename}_functionality_{tag}.json'), 'w') as json_f:
            json.dump(data, json_f)
    print(count)


def run2(filename, chunksize):
    pattern_matcher = PatternMatcher()
    reader = pd.read_csv(load_tmp(f'eliminate_{filename}.csv'), iterator=True, chunksize=chunksize)
    count = 0
    tag = 0
    tags = list_tags(filename)
    for chunk in reader:
        count += len(chunk)
        data = []
        tag += 1
        if tag in tags:
            print(f'already processed {count} rows')
            continue
        print(f'processing {count} rows now')
        for index, row in tqdm(chunk.iterrows()):
            try:
                mapped_template = pattern_matcher.mapping_template_copy(row[1])
                if not mapped_template:
                    continue
                mapped_template['id'] = row[0]
                data.append(mapped_template)
            except DataHandlerError as ce:
                logger.info(ce, row[1])
            except Exception as e:
                logger.info(e)
        print(f'already processed {count} rows')
        with open(load_tmp(f'{filename}_functionality_2,{tag}.json'), 'w') as json_f:
            json.dump(data, json_f)


def list_tags(filename):
    match_file = f'{filename}_functionality_2,'
    tags = []
    for filename_ext in walk_dir(tmp_folder()):
        if match_file in filename_ext:
            tags.append(int(filename_ext[:-5].split(match_file)[-1]))
    return tags


if __name__ == '__main__':
    # run2('method_desc', 100)
    pattern_matcher = PatternMatcher()
    # print(pattern_matcher.mapping_template_copy('Same as <noun>Object,</noun> but without the trouble of relations or date-specific options..'))
    # text = 'Aborts this http request. Any active execution of this method should return immediately. If the request has not started, it will abort after the next execution. Aborting this request will cause all subsequent executions with this request to fail.'
    # text = "gets value"
    # text = "Returns the URI this request uses, such as <noun>http://example.org/path/to/file</noun>. Note that the URI may be absolute URI (as above) or may be a relative URI. Implementations are encouraged to return the URI that was initially requested. To find the final URI after any redirects have been processed, please see the section entitled HTTP execution context in the "
    # text = "convenience method to get this element as a primitive integer."
    # print(TemplateExtractor.preprocess_sentence(text))
    # text = "Returns a copy of the specified iterable sorted by this ordering. The input is not modified. The returned list is modifiable, serializable, and has random access. Unlike <noun>Sets#newTreeSet(Iterable)</noun>, this method does not collapse elements that compare as zero, and the resulting collection does not maintain its own sort order."
    # text = "Get the number of elements in the JSONArray, included nulls."
    # text = "Get the long value associated with a key."
    text = "Returns a request header identifying what version of the state management specification is understood. May be <noun>null</noun> if the cookie specification does not support <noun>Cookie2</noun> header."
    # text = "Returns a request header identifying what version of the state management specification is understood."
    # text = "May be <noun>null</noun> if the cookie specification does not support <noun>Cookie2</noun> header."
    # text = "write Header"
    # text = "post Deregister"
    print(pattern_matcher.mapping_template_copy(text))
