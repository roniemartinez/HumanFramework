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
    assert execute_intent('title should be "LUIS (Language Understanding) – Cognitive Services – Microsoft Azure"')
    assert execute_intent('close browser')


def test_local_file():
    import os
    html = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample.html')
    assert execute_intent(f'open chrome file:///{html}')
    assert execute_intent('title should be "Sample Page"')
    assert execute_intent('page should contain "Hello World!"')
    assert execute_intent('close browser')