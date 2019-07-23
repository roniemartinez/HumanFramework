#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from human import execute_intent


def test_assert_math_add():
    assert 10 == execute_intent('add: 1, 2, 3 and 4')
    assert execute_intent('result should be equal to 10')
