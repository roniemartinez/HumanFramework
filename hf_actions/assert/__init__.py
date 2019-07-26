#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"


def equal(entities, context):
    assert len(entities) == 2
    values = []
    for entity in entities:
        if entity['type'] == 'last_result':
            values.append(context['LAST_RESULT'])
        elif entity['type'] == 'builtin.number':
            value = entity.get('resolution').get('value')
            try:
                values.append(int(value))
            except ValueError:
                values.append(float(value))
    a, b = values
    assert a == b, f"{a} is not equal to {b}"
    return True


def not_equal(entities, context):
    assert len(entities) == 2
    values = []
    for entity in entities:
        if entity['type'] == 'last_result':
            values.append(context['LAST_RESULT'])
        elif entity['type'] == 'builtin.number':
            value = entity.get('resolution').get('value')
            try:
                values.append(int(value))
            except ValueError:
                values.append(float(value))
    a, b = values
    assert a != b, f"{a} is equal to {b}"
    return True
