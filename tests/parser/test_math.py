#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from human_framework import get_intent


def test_math_add():
    assert get_intent('add: 1, 2, 3 and 4').get('topScoringIntent').get('intent') == 'math.add'
    assert get_intent('sum of 55.3, 6, 3').get('topScoringIntent').get('intent') == 'math.add'
    assert get_intent('calculate the sum of -10 and 5').get('topScoringIntent').get('intent') == 'math.add'
    assert get_intent('add 10,000,300 and 20.3').get('topScoringIntent').get('intent') == 'math.add'
    assert get_intent('add 10,00,00,00, 300, and 20.3').get('topScoringIntent').get('intent') == 'math.add'
