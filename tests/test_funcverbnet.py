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
    print(net.find_cate_by_name())


def test_get_category_number():
    net = FuncVerbNet()
    print(net.get_category_number())


def test_find_cate_by_verb():
    net = FuncVerbNet()
    print(net.find_cate_by_verb('print'))


def test_find_cate_by_id():
    net = FuncVerbNet()
    print(net.find_cate_by_id(10))


def test_find_cate_by_pattern():
    net = FuncVerbNet()
    print(net.find_cate_by_pattern("V {patient} about {topic}"))


def test_find_all_verb_by_cate():
    net = FuncVerbNet()
    print(net.find_all_verb_by_cate(3))


def test_find_all_pattern_by_cate():
    net = FuncVerbNet()
    print(net.find_all_pattern_by_cate(3))


def test_get_category_number():
    net = FuncVerbNet()
    print(net.get_category_number())


def test_get_included_verb_number_by_cateid():
    net = FuncVerbNet()
    print(net.get_included_verb_number_by_cateid(3))


def test_get_included_pattern_number_by_cateid():
    net = FuncVerbNet()
    print(net.get_included_pattern_number_by_cateid(4))


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
    print(net.find_verb_by_id(3))


def test_find_verb_by_name():
    net = FuncVerbNet()
    print(net.find_verb_by_name("stop"))


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


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'funcverbnet.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
