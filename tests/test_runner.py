#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from human import run_test_string, run_test


def test_run_string():
    assert run_test_string("""
add: 1, 2, 3 and 4
result should be equal to 10
""")


def test_run_string_fail():
    assert not run_test_string("""
add: 1, 2, 3 and 4
result should be equal to 11
""")


def test_run_test():
    assert run_test('test_simple')


def test_run_test_failing():
    assert not run_test('test_failing')
