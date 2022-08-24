#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/07/28
------------------------------------------
@Modify: 2022/07/28
------------------------------------------
@Description:
"""
import json
import time
import re
from funcverbnet.utils import load_tmp

from funcverbnet.data_handler.concept_extractor import ConceptExtractor


def load_jl(jl_file_path):
    data_list = []
    with open(jl_file_path) as file:
        line = file.readline()
        while line != "":
            data_list.append(json.loads(line))
            line = file.readline()
    return data_list


def cal_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        print("%s running time: %s sec." % (func.__name__, t2 - t1))
        return result

    return wrapper


if __name__ == '__main__':
    concept_extractor = ConceptExtractor()
    # data = load_jl(load_tmp('node_info_2.jl'))

    # for item in data:
    #     # print(json.dumps(item, indent=4))
    #     if not item:
    #         continue
    #     for relation in item['relations']:
    #         # if 'return_value' not in relation['relation_name']:
    #         #     continue
    #         if 'has_parameter' not in relation['relation_name']:
    #             continue
    #         if not relation['relation_node']:
    #             continue
    #         if 'description' not in relation['relation_node']['node_info']:
    #             continue
    #         # print(json.dumps(relation['relation_node'], indent=4))
    #         node_info = relation['relation_node']['node_info']
    #         sentence = node_info['description']
    #         sentence = re.compile(r'<[^>]*>|\([^\)]*\)|\[[^\]]*\]|\{[^\}]*\}', re.S).sub('', sentence)
    #         print(json.dumps(sentence), concept_extractor.extract_noun_chunks(sentence))
    #         # for sub_relation in relation['relation_node']['relations']:
    #         #     if 'functionality' not in sub_relation['relation_name']:
    #         #         continue
    #         #     print(sub_relation['relation_node'])

    # data = load_jl(load_tmp('class_with_description.jl'))
    # for item in data:
    # print(item['description'])
    # print(concept_extractor.extract_noun_chunks(item['description']))

    # text = 'the returned logger will be named after clazz'
    # text = 'A key string.'
    # text = 'key to store in the multimap.'
    # text = 'either an absolute or relative URI'
    # text = 'the second argument'
    # text = 'root of a tree of s'
    # text = 'The object to append. It can be null, or a Boolean, Number,\n  String, JSONObject, or JSONArray, or an object that implements JSONString.'
    # text = 'the element that needs to be added to the array.'
    # text = 'the '
    # text = 'A long.'
    # text = 'One of the LOG_LEVEL_XXX constants defining the log level'
    # text = 'name of the member that is being requested.'
    # text = 'the index of the element that is being sought.'
    # text = 'the String to check, may be null'
    # text = "the index of the first '%' character in the string"
    # text = "The metadata object to populate from the response's headers."
    # text = "The rule ID of this object's expiration configuration"
    # text = "The specific genericized type of src. You can obtain this type by using the {@link com.google.gson.reflect.TypeToken} class. For example, to get the type for {@code Collection<Foo>}, you should use: <pre> Type typeOfT = new TypeToken&lt;Collection&lt;Foo&gt;&gt;(){}.getType(); </pre>"
    # text = "A {@link List} of groups that are included/excluded in a given &lt;test&gt;"
    # text = "Represents a Key/Value pair of dynamically defined groups by the user. For e.g., <pre> &lt;groups&gt; <br> &lt;define name='dynamicGroup'&gt; <br> &lt;include name='regressionMethod'/&gt; <br> &lt;/define&gt; <br> &lt;/groups&gt; <br> </pre>"
    # text = "Object codec to use for stream-based object conversion through parser/generator interfaces. If null, such methods cannot be used."
    # text = "the host name/IP"
    # text = "The file to download the object's data to."
    # text = "the local host name/IP to bind the socket to"
    # text = "a list of 3 or more arguments"
    # text = "Subject-Alt fields of type 2 ('DNS'), as extracted from the X.509 certificate."
    # text = "receiver of notifications of blocking I/O operations."
    # text = "An optional HTTP/S or RTMP resource path that restricts which distribution and S3 objects will be accessible in a signed URL. For standard distributions the resource URL will be <tt>'http://' + distributionName + '/' + objectKey</tt> (may also include URL parameters. For distributions with the HTTPS required protocol, the resource URL must start with <tt>'https://'</tt>. RTMP resources"
    # text = "The {@link UIComponent} (if any) to which this element corresponds. <span class='changed_added_2_2'> This component is inspected for its pass through attributes as described in the standard HTML_BASIC {@code RenderKit} specification.</span>"
    # text = "A string representation of an Amazon S3 permission, eg. <code>FULL_CONTROL</code>"
    # text = "Effective property base type to use; may differ from actual type of property; for structured types it is content (value) type and NOT structured type."
    # text = "the host name/IP"
    # text = "("
    text = "names of columns be of own entity"
    text = "Locate an object in {@literal JNDI} by name"
    text = "GsonBuilder"
    text = "return column iterator"
    print(concept_extractor.extract_noun_chunks(text))

    # texts = [
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP",
    #     "the host name/IP"
    # ]
    #
    #
    # @cal_time
    # def run(data):
    #     for item in data:
    #         concept_extractor.extract_noun_chunks(item)
    #
    #
    # run(texts)
