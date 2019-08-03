#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import time


def sleep(entities, context):
    for entity in entities:
        if entity['type'] == 'builtin.datetimeV2.duration':
            values = entity.get('resolution').get('values')
            for value in values:
                if value.get('type') == 'duration':
                    duration = int(value.get('value'))
                    time.sleep(duration)
                    return True
    return False
