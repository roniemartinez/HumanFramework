#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import logging
import os
from functools import lru_cache

import requests

from action_loader import ActionLoader

logger = logging.getLogger(__name__)
session = requests.Session()


@lru_cache()
def get_intent(query) -> dict:
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
    intent = get_intent(query)
    module, action = intent.get('topScoringIntent').get('intent').split('.', 1)
    loader = ActionLoader()
    loader.load_action_module(module)
    return loader.execute_action(module, action, intent.get('entities'))
