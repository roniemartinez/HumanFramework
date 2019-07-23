#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from human import execute_intent


def test_web():
    assert execute_intent('open firefox')
    assert execute_intent('close browser')


def test_web_url():
    assert execute_intent('open chrome luis.ai')
    assert execute_intent('close browser')
