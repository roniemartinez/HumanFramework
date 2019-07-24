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
    assert execute_intent('page should contain button "id:click-me"')
    assert execute_intent('page should contain button "class:click-me"')
    assert execute_intent('page should contain checkbox "name:male"')
    assert execute_intent('page should contain checkbox "name:male"')
    assert execute_intent('page should contain element "tag:form"')
    assert execute_intent('page should contain element "xpath:/html/body/p"')
    assert execute_intent('page should contain image "css:.my-image"')
    assert execute_intent('page should contain link "link:Mountain"')
    assert execute_intent('page should contain link "partial link:Mount"')
    assert execute_intent('page should contain list "id:letters"')
    assert execute_intent('page should contain radio button "id:agree"')
    assert execute_intent('page should contain text field "name:name"')
    assert execute_intent('close browser')
