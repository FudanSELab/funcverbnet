#!/usr/bin/env python

"""Tests for `funcverbnet` package."""

import pytest

from click.testing import CliRunner

from funcverbnet import cli
from funcverbnet.nodes.funcverbnet import FuncVerbNet


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: https://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    net = FuncVerbNet()
    print(net.f_categories)


def test_find_cate_by_name():
    net = FuncVerbNet()
    print(net.find_f_category_by_name('stop'))


def test_get_f_category_number():
    net = FuncVerbNet()
    print(net.get_f_category_number())


def test_find_f_category_by_verb():
    net = FuncVerbNet()
    print(net.find_f_category_by_verb('filter'))


def test_find_f_category_by_id():
    net = FuncVerbNet()
    print(net.find_f_category_by_id(1).name)


def test_find_semantic_by_name():
    net = FuncVerbNet()
    print(net.find_semantic_by_name('source'))


def test_find_f_category_by_pattern():
    net = FuncVerbNet()
    print(net.find_f_category_by_pattern("V {patient} about {topic}"))


def test_find_patterns_by_semantic_id():
    net = FuncVerbNet()
    print(net.find_patterns_by_semantic_id(3))


def test_find_patterns_by_semantics_name():
    net = FuncVerbNet()
    print(net.find_patterns_by_semantics_name("patient"))


def test_find_patterns_with_two_semantics_name():
    net = FuncVerbNet()
    print(net.find_patterns_with_two_semantics_name("location", "patient"))


def test_find_patterns_with_two_semantics_id():
    net = FuncVerbNet()
    print(net.find_patterns_with_two_semantics_id(5, 3))
    assert net.find_patterns_with_two_semantics_id(-8, 3) is None
    assert net.find_patterns_with_two_semantics_id(-8, -3) is None


def test_find_common_roles_with_two_pattern_ids():
    net = FuncVerbNet()
    print(net.find_common_roles_with_two_pattern_ids(1, 3))
    assert net.find_common_roles_with_two_pattern_ids(-6, 2) is None


def test_find_all_verb_by_f_category_id():
    net = FuncVerbNet()
    print(net.find_all_verb_by_f_category_id(3))
    print(net.find_all_verb_by_f_category_id("hhh"))


def test_find_all_pattern_by_f_category_id():
    net = FuncVerbNet()
    print(net.find_all_pattern_by_f_category_id(3))


def test_find_all_pattern_name_by_f_category_id():
    net = FuncVerbNet()
    print(net.find_all_pattern_name_by_f_category_id(3))


def test_get_included_roles_number_by_pattern_id():
    net = FuncVerbNet()
    print(net.get_included_semantics_number_by_pattern_id(233))


def test_find_included_roles_by_pattern_id():
    net = FuncVerbNet()
    print(net.find_included_semantics_by_pattern_id(3))
    print(net.find_included_semantics_by_pattern_id(-2))


def test_get_included_verb_number_by_f_category_id():
    net = FuncVerbNet()
    print(net.get_included_verb_number_by_f_category_id(3))


def test_get_included_pattern_number_by_f_category_id():
    net = FuncVerbNet()
    assert net.get_included_pattern_number_by_f_category_id(333) is None
    assert net.get_included_pattern_number_by_f_category_id(3) == 2


def test_get_semantic_number():
    net = FuncVerbNet()
    print(net.get_semantic_number())


def test_get_verb_number():
    net = FuncVerbNet()
    print(net.get_verb_number())


def test_get_pattern_number():
    net = FuncVerbNet()
    print(net.get_pattern_number())


def test_find_verb_by_id():
    net = FuncVerbNet()
    print(net.find_verb_by_id(-6))
    print(net.find_verb_by_id(2))


def test_find_verb_by_name():
    net = FuncVerbNet()
    print(net.find_verb_by_name("stop"))


def test_find_f_verb_by_name():
    net = FuncVerbNet()
    print(net.find_f_verb_by_name("stop"))


def test_find_pattern_by_id():
    net = FuncVerbNet()
    print(net.find_pattern_by_id(3))


def test_find_pattern_by_syntax():
    net = FuncVerbNet()
    print(net.find_pattern_by_syntax("V {patient} if/when S"))


def test_find_semantic_by_id():
    net = FuncVerbNet()
    print(net.find_semantic_by_id(5))


def test_find_semantic_definition_by_name():
    net = FuncVerbNet()
    print(net.find_semantic_definition_by_name("patient"))


def test_find_semantic_definition_by_id():
    net = FuncVerbNet()
    print(net.find_semantic_definition_by_id(5))


def test_find_semantic_name_by_id():
    net = FuncVerbNet()
    print(net.find_semantic_name_by_id(5))


def test_find_f_categories_by_pattern():
    net = FuncVerbNet()
    print(net.find_f_categories_by_pattern("V {patient}"))


def test_find_f_categories_by_verb():
    net = FuncVerbNet()
    print(net.find_f_categories_by_verb("end"))
    assert net.find_f_categories_by_verb("hello") is None


def test_find_f_categories_with_two_verbs():
    net = FuncVerbNet()
    print(net.find_f_categories_with_two_verbs("end", "stop"))


def test_find_common_verbs_with_two_f_categories():
    net = FuncVerbNet()
    print(net.find_common_verbs_with_two_f_categories(1, 18))
    print(net.find_common_verbs_with_two_f_categories(-6, 18))


def test_find_common_patterns_with_two_f_categories():
    net = FuncVerbNet()
    print(net.find_common_patterns_with_two_f_categories(1, 18))
    assert net.find_common_patterns_with_two_f_categories(-2, -6) is None
    print(net.find_common_patterns_with_two_f_categories(-2, 2))


def test_is_valid_verb():
    net = FuncVerbNet()
    assert net.is_valid_verb("admin") is False


def test_is_valid_f_category_id():
    net = FuncVerbNet()
    assert net.is_valid_f_category_id(105) is False


def test_is_valid_pattern():
    net = FuncVerbNet()
    assert net.is_valid_pattern("V {patient} if/when S") is True
    assert net.is_valid_pattern("Vs {patient}") is False


def test_is_valid_semantic_name():
    net = FuncVerbNet()
    assert net.is_valid_semantic_name("patient") is True
    assert net.is_valid_semantic_name("hello") is False


def test_is_valid_f_verb():
    net = FuncVerbNet()
    assert net.is_valid_f_verb("location") is False
    assert net.is_valid_f_verb("log") is True


def test_is_valid_f_pattern():
    net = FuncVerbNet()
    assert net.is_valid_f_pattern("V {jaj}") is False
    assert net.is_valid_f_pattern("V {patient} from {source}") is True


def test_is_semantic_included_in_pattern():
    net = FuncVerbNet()
    assert net.is_semantic_included_in_pattern("patient") is True
    assert net.is_semantic_included_in_pattern("topic") is True
    assert net.is_semantic_included_in_pattern("word") is False


def test_find_all_semantics_by_f_category_id():
    net = FuncVerbNet()
    print(net.find_all_semantics_by_f_category_id(5))


def test_find_f_categories_by_semantic():
    net = FuncVerbNet()
    print(net.find_f_categories_by_semantic("patient"))


def test_get_sentences():
    net = FuncVerbNet()
    print(net.get_sentences())


def test_find_sentences_by_f_category_id():
    net = FuncVerbNet()
    print(net.find_sentences_by_f_category_id(0))


def test_find_category_by_sentence():
    net = FuncVerbNet()
    print(net.find_category_by_sentence('how are you'))
    # print(net.find_category_by_any_sentence('Request an informative description of the key status for the session.'))


def test_find_antisense_categories_by_category():
    net = FuncVerbNet()
    print(net.find_antisense_categories_by_category(1))


def test_find_antisense_category_ids_by_category():
    net = FuncVerbNet()
    print(net.find_antisense_category_ids_by_category(1))


def test_find_antisense_category_by_verb():
    net = FuncVerbNet()
    print(net.find_antisense_categories_by_verb("stop"))


def test_find_antisense_category_ids_by_verb():
    net = FuncVerbNet()
    print(net.find_antisense_category_ids_by_verb("stop"))


def test_find_antisense_verbs_by_verb():
    net = FuncVerbNet()
    print(net.find_antisense_verbs_by_verb("stop"))


def test_find_similar_verbs_by_verb():
    net = FuncVerbNet()
    print(net.find_similar_verbs_by_verb("write"))


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
