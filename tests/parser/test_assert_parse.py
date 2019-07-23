#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from human import get_intent


def test_assert_equal():
    assert get_intent('result should be 3K').get('topScoringIntent').get('intent') == 'assert.equal'
