#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from human import execute


def test_add():
    assert 1 + 2 + 3 + 4 == execute('add: 1, 2, 3 and 4')
    assert 55.3 + 6 + 3 == execute('sum of 55.3, 6, 3')
    assert -10 + 5 == execute('calculate the sum of -10 and 5')
    assert 10_000_300 + 20.3 == execute('add 10,000,300 and 20.3')
    assert 10_000_000 + 300 + 20.3 == execute('add 10,000,000, 300, and 20.3')
    assert 100_000 + 300 + 20.3 == execute('add 1e5, 300, and 20.3')
