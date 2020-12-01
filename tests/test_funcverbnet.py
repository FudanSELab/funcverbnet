#!/usr/bin/env python

"""Tests for `funcverbnet` package."""

import pytest

from click.testing import CliRunner

from funcverbnet import funcverbnet
from funcverbnet import cli
from funcverbnet.funcverbnet import FuncVerbNet


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_find_cate_by_name():
    net = FuncVerbNet()
    print(net.find_cate_by_name(1))


def test_get_category_number():
    net = FuncVerbNet()
    print(net.get_category_number())


def test_find_cate_by_verb():
    net = FuncVerbNet()
    print(net.find_cate_by_verb('print'))


def test_find_cate_by_id():
    net = FuncVerbNet()
    print(net.find_cate_by_id(10))


def test_find_role_by_name():
    net = FuncVerbNet()
    print(net.find_role_by_name('patient'))


def test_find_cate_by_pattern():
    net = FuncVerbNet()
    print(net.find_cate_by_pattern("V {patient} about {topic}"))


def test_find_patterns_by_role_id():
    net = FuncVerbNet()
    print(net.find_patterns_by_role_id(3))


def test_find_patterns_by_role_name():
    net = FuncVerbNet()
    print(net.find_patterns_by_role_name("patient"))


def test_find_patterns_with_two_roles_name():
    net = FuncVerbNet()
    print(net.find_patterns_with_two_roles_name("location", "patient"))


def test_find_patterns_with_two_roles_id():
    net = FuncVerbNet()
    print(net.find_patterns_with_two_roles_id(5, 3))
    assert net.find_patterns_with_two_roles_id(-8, 3) is None
    assert net.find_patterns_with_two_roles_id(-8, -3) is None


def test_find_common_roles_by_pattern_id():
    net = FuncVerbNet()
    print(net.find_common_roles_by_pattern_id(1, 3))
    assert net.find_common_roles_by_pattern_id(-6, 2) is None


def test_find_all_verb_by_cate_id():
    net = FuncVerbNet()
    print(net.find_all_verb_by_cate_id(3))
    print(net.find_all_verb_by_cate_id("hhh"))


def test_find_all_pattern_by_cate_id():
    net = FuncVerbNet()
    print(net.find_all_pattern_by_cate_id(3))


def test_find_all_pattern_name_by_cate_id():
    net = FuncVerbNet()
    print(net.find_all_pattern_name_by_cate_id(3))


def test_get_included_roles_number_by_pattern_id():
    net = FuncVerbNet()
    print(net.get_included_roles_number_by_pattern_id(233))


def test_find_included_roles_by_pattern_id():
    net = FuncVerbNet()
    print(net.find_included_roles_by_pattern_id(3))
    print(net.find_included_roles_by_pattern_id(-2))


def test_get_category_number():
    net = FuncVerbNet()
    print(net.get_category_number())


def test_get_included_verb_number_by_cateid():
    net = FuncVerbNet()
    print(net.get_included_verb_number_by_cateid(3))


def test_get_included_pattern_number_by_cateid():
    net = FuncVerbNet()
    assert net.get_included_pattern_number_by_cateid(333) is None
    assert net.get_included_pattern_number_by_cateid(3) == 2


def test_get_role_number():
    net = FuncVerbNet()
    print(net.get_role_number())


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


def test_find_role_by_id():
    net = FuncVerbNet()
    print(net.find_role_by_id(5))


def test_find_role_by_name():
    net = FuncVerbNet()
    print(net.find_role_by_name("patient"))


def test_find_role_definition_by_name():
    net = FuncVerbNet()
    print(net.find_role_definition_by_name("patient"))


def test_find_role_definition_by_id():
    net = FuncVerbNet()
    print(net.find_role_definition_by_id(5))


def test_find_role_name_by_id():
    net = FuncVerbNet()
    print(net.find_role_name_by_id(5))


def test_find_cates_by_pattern():
    net = FuncVerbNet()
    print(net.find_cates_by_pattern("V {patient}"))


def test_find_cates_by_verb():
    net = FuncVerbNet()
    print(net.find_cates_by_verb("end"))
    assert net.find_cates_by_verb("hello") is None


def test_find_cates_with_two_verbs():
    net = FuncVerbNet()
    print(net.find_cates_with_two_verbs("end", "stop"))


def test_find_common_verbs_by_cates():
    net = FuncVerbNet()
    print(net.find_common_verbs_by_cates(1, 18))
    print(net.find_common_verbs_by_cates(-6, 18))


def test_find_common_patterns_by_cates():
    net = FuncVerbNet()
    print(net.find_common_patterns_by_cates(1, 18))
    assert net.find_common_patterns_by_cates(-2, -6) is None
    print(net.find_common_patterns_by_cates(-2, 2))


def test_is_valid_verb():
    net = FuncVerbNet()
    assert net.is_valid_verb("admin") == False
    # print(net.is_valid_verb("admin"))


def test_is_valid_category_id():
    net = FuncVerbNet()
    assert net.is_valid_category_id(105) == False


def test_is_valid_pattern_name():
    net = FuncVerbNet()
    assert net.is_valid_pattern_name("V {patient} if/when S") == True
    assert net.is_valid_pattern_name("Vs {patient}") == False


def test_is_valid_role_name():
    net = FuncVerbNet()
    assert net.is_valid_role_name("patient") == True
    assert net.is_valid_role_name("hello") == False


def test_is_valid_f_verb():
    net = FuncVerbNet()
    assert net.is_valid_f_verb("location") == False
    assert net.is_valid_f_verb("log") == True


def test_is_valid_f_pattern():
    net = FuncVerbNet()
    assert net.is_valid_f_pattern("V {jaj}") == False
    assert net.is_valid_f_pattern("V {patient} from {source}") == True


def test_is_role_included_in_pattern():
    net = FuncVerbNet()
    assert net.is_role_included_in_pattern("patient") is True
    assert net.is_role_included_in_pattern("topic") is True
    assert net.is_role_included_in_pattern("word") is False


def test_find_all_roles_by_cate_id():
    net = FuncVerbNet()
    print(net.find_all_roles_by_cate_id(5))


def test_find_cates_by_role():
    net = FuncVerbNet()
    print(net.find_cates_by_role("patient"))


def test_get_sentences():
    net = FuncVerbNet()
    print(net.get_sentences())


def test_find_sentences_by_category():
    net = FuncVerbNet()
    print(net.find_sentences_by_category(1))


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
