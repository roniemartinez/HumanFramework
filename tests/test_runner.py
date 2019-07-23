#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import pytest

from human import run_test_string


def test_run_string():
    assert run_test_string("""
add: 1, 2, 3 and 4
result should be equal to 10
""")


def test_run_string_fail():
    with pytest.raises(AssertionError):
        run_test_string("""
add: 1, 2, 3 and 4
result should be equal to 11
""")
