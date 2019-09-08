#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import json
import logging
import os
import sys
import webbrowser
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from platform import platform

import diskcache
import requests
from dotenv import load_dotenv, set_key
from jinja2 import Environment, select_autoescape, PackageLoader

from human_framework import __version__
from human_framework.action_loader import ActionLoader

LOG_FORMAT = '%(asctime)s %(levelname)s %(module)s %(message)s'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.humanframework')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config')

logger = logging.getLogger(__name__)
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR, exist_ok=True)
if not os.path.exists(CONFIG_FILE):
    open(CONFIG_FILE, 'a').close()
session = requests.Session()
loader = ActionLoader()
context = {}
is_env_loaded = False
cache = diskcache.Cache(directory=CONFIG_DIR)  # type: diskcache.Cache


def get_intent(query) -> dict:
    """
    Get the intent of the sentence
    :param query: Sentence
    :return: intent object
    """
    global session
    global cache
    global is_env_loaded
    if not is_env_loaded:
        load_dotenv(dotenv_path=CONFIG_FILE)
        is_env_loaded = True
    logger.info(f'Parsing intent for "{query}"')
    q = ' '.join(query.lower().split())
    cached_intent = cache.get(q)
    if cached_intent:
        logger.info(f'Found cached intent: {cached_intent.get("topScoringIntent").get("intent")}')
        return cached_intent
    for _ in range(3):
        try:
            response = session.get(os.getenv('LUIS_ENDPOINT') + query)
            response.raise_for_status()
            intent = response.json()
            logging.info(f'Resolved intent: {intent.get("topScoringIntent").get("intent")}')
            cache.set(q, intent)
            return intent
        except Exception as e:
            logger.exception(e)
    return {}


def execute_intent(intent):
    global context
    global loader
    context['QUERY'] = intent.get('query')
    module, action = intent.get('topScoringIntent').get('intent').rsplit('.', 1)
    entities = intent.get('entities')
    loader.load_action_module(module)
    return loader.execute_action(module, action, entities, context)


def execute(query):
    global context
    context['QUERY'] = query
    intent = get_intent(query)
    return execute_intent(intent)


def run_test_string(test_string) -> dict:
    result = {'CONTENT': test_string}
    line_number = 1
    try:
        for line_number, intent in get_intents(test_string):
            logger.info('Executing test: %s', intent.get('query'))
            if not execute_intent(intent):
                logger.error(f"Failed on test: query={intent.get('query')}, "
                             f"intent={intent.get('topScoringIntent').get('intent')}")
                result['STATUS'] = False
                result['LINE_NUMBER'] = line_number
                return result
    except Exception as e:
        result['ERROR'] = str(e)
        result['STATUS'] = False
        result['LINE_NUMBER'] = line_number
        return result
    result['STATUS'] = True
    return result


def get_intents(test_string):
    intents = []
    line_number = 1
    for line in test_string.splitlines():
        line = line.strip()
        if line:
            try:
                intents.append((line_number, get_intent(line)))
            except AssertionError as e:
                logger.exception(e)
                raise
        line_number += 1
    return intents


def run_test(test_name) -> dict:
    logger.info(f"Testing: {test_name}")
    if isinstance(test_name, str):
        for file in Path('trials').iterdir():
            if file.name.startswith(test_name):
                test_name = file
                break
    with open(test_name, encoding='utf-8') as f:
        return run_test_string(f.read())


def run_trials(arguments):  # pragma: no cover
    report = []
    current_datetime = datetime.now()
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
                    result = run_test(file_)
                    if result['STATUS']:
                        print(" - PASSED", flush=True)
                        passed += 1
                    else:
                        print("- FAILED", flush=True)
                        failed += 1
                    result['TEST_NAME'] = str(file_)
                    result['STATUS'] = 'PASSED' if result['STATUS'] else 'FAILED'
                    report.append(result)

        else:
            if path.name.startswith('test_') and path.name.rsplit('.', 1)[0] not in excluded:
                print(path, end=' ', flush=True)
                result = run_test(path)
                if result['STATUS']:
                    print(" - PASSED", flush=True)
                    passed += 1
                else:
                    print("- FAILED", flush=True)
                    failed += 1
                result['TEST_NAME'] = str(path)
                result['STATUS'] = 'PASSED' if result['STATUS'] else 'FAILED'
                report.append(result)
    print(flush=True)
    result = f" {passed} passed "
    if failed:
        result += f"and {failed} failed "
    print(result.center(80, '='), flush=True)

    os.makedirs('reports', exist_ok=True)
    env = Environment(
        loader=PackageLoader('human_framework', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('report.html')
    html_report_name = f'report-{current_datetime.strftime("%Y%m%d%H%M%S")}.html'
    report_path = os.path.join('reports', html_report_name)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(template.render(json_data=json.dumps(report), date=current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                platform=platform(), passed=passed, failed=failed, version=__version__))
    webbrowser.open_new_tab('file://' + os.path.abspath(report_path))
    if failed:
        return False
    return True


def main():  # pragma: no cover
    global is_env_loaded
    parser = ArgumentParser(description="Human Framework")
    parser.add_argument('-t', '--test', nargs='*', dest='test', help='Test files')
    parser.add_argument('-x', '--excluded', nargs='*', dest='excluded', help='Excluded files')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
    sub_commands = parser.add_subparsers()
    config_parser = sub_commands.add_parser('config', help="Human Framework configuration")
    config_parser.add_argument('--luis-endpoint', nargs='?', dest='luis_endpoint', required=True,
                               help='Endpoint from LUIS.ai', )
    arguments = parser.parse_args()
    try:
        if arguments.luis_endpoint:
            set_key(dotenv_path=CONFIG_FILE, key_to_set='LUIS_ENDPOINT',
                    value_to_set=arguments.luis_endpoint)
        else:
            load_dotenv(dotenv_path=CONFIG_FILE)
            luis_endpoint = os.getenv('LUIS_ENDPOINT')
            if luis_endpoint:
                print(f"\nYour LUIS.ai endpoint is '{luis_endpoint}'")
            else:
                print_configuration_warning()
        return
    except AttributeError:
        pass

    load_dotenv(dotenv_path=CONFIG_FILE)
    is_env_loaded = True
    if not os.getenv('LUIS_ENDPOINT'):
        print_configuration_warning()
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format=LOG_FORMAT)

    if not run_trials(arguments):
        exit(1)


def print_configuration_warning():
    print('\nWARNING: LUIS.ai endpoint is not yet configured properly.'
          '\nRun the following command to configure Human Framework:\n'
          '\nhuman config --luis-endpoint <endpoint>')
    exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
