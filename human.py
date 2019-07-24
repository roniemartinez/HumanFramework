#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import logging
import os
from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path

import requests

from human_framework.action_loader import ActionLoader

logger = logging.getLogger(__name__)
session = requests.Session()
loader = ActionLoader()
context = {}


@lru_cache()
def get_intent(query) -> dict:
    """
    Get the intent of the sentence
    :param query: Sentence
    :return: intent object
    """
    global session
    logger.info(f'Parsing intent for "{query}"')
    for _ in range(3):
        try:
            response = session.get(os.getenv('LUIS_ENDPOINT') + query)
            response.raise_for_status()
            intent = response.json()
            logging.info(f'Intent: {intent}')
            return intent
        except Exception as e:
            logger.exception(e)
    return {}


def execute_intent(query):
    global context
    global loader
    context['QUERY'] = query
    intent = get_intent(query)
    module, action = intent.get('topScoringIntent').get('intent').rsplit('.', 1)
    loader.load_action_module(module)
    return loader.execute_action(module, action, intent.get('entities'), context)


def run_test_string(test_string):
    for line in test_string.splitlines():
        line = line.strip()
        if line:
            try:
                execute_intent(line)
            except AssertionError as e:
                logger.exception(e)
                raise
    return True


def run_test(test_name):
    logger.info(f"Testing: {test_name}")
    if isinstance(test_name, str):
        for file in Path('trials').iterdir():
            if file.name.startswith(test_name):
                test_name = file
                break
    with open(test_name, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            try:
                if line:
                    execute_intent(line)
                    logger.info(f"Line executed: {line}")
            except Exception as e:
                logger.exception(e)
                return False
    return True


def run_trials(arguments):  # pragma: no cover
    excluded = arguments.excluded or []
    if isinstance(excluded, str):
        excluded = [excluded]
    print(" human trials started ".center(80, '='), flush=True)
    print(flush=True)
    passed = failed = 0

    files = arguments.test
    if not files:
        files = ['trials']
    for file in files:
        path = Path(file)
        if path.is_dir():
            for file_ in path.iterdir():
                if file_.name.startswith('test_') and file_.name.rsplit('.', 1)[0] not in excluded:
                    print(file_, end=' ', flush=True)
                    if run_test(file_):
                        print(" - PASSED", flush=True)
                        passed += 1
                    else:
                        print(" - FAILED", flush=True)
                        failed += 1
        else:
            if path.name.startswith('test_') and path.name.rsplit('.', 1)[0] not in excluded:
                print(path, end=' ', flush=True)
                if run_test(path):
                    print(" - PASSED", flush=True)
                    passed += 1
                else:
                    print(" - FAILED", flush=True)
                    failed += 1
    print(flush=True)
    result = f" {passed} passed "
    if failed:
        result += f"and {failed} failed "
    print(result.center(80, '='), flush=True)
    if failed:
        return False
    return True


def main():  # pragma: no cover
    parser = ArgumentParser(description="Human Framework")
    parser.add_argument('test', nargs='*', help='Test files')
    parser.add_argument('excluded', nargs='*', help='Excluded files')
    arguments = parser.parse_args()
    if not run_trials(arguments):
        exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
