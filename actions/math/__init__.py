#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"


def add(entities, context):
    result = 0
    for entity in entities:
        assert entity['type'] == 'builtin.number'
        value = entity.get('resolution').get('value')
        try:
            number = int(value)
        except ValueError:
            number = float(value)
        result += number
    return result
