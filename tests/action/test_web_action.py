#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import os

from human import execute, run_test_string


def test_web():
    assert execute('open firefox')
    assert execute('close browser')


def test_web_url():
    assert execute('open chrome luis.ai')
    assert execute('title should be "LUIS (Language Understanding) – Cognitive Services – Microsoft Azure"')
    assert execute('close browser')


def test_local_file():
    html = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample.html')
    assert execute(f'open chrome file:///{html}')
    assert execute('title should be "Sample Page"')
    assert execute('page should contain "Hello World!"')
    assert execute('page should contain button "id:click-me"')
    assert execute('page should contain button "class:click-me"')
    assert execute('page should contain checkbox "name:male"')
    assert execute('page should contain checkbox "name:male"')
    assert execute('page should contain element "tag:form"')
    assert execute('page should contain element "xpath:/html/body/p"')
    assert execute('page should contain image "css:.my-image"')
    assert execute('page should contain link "Mountain"')
    assert execute('page should contain link "partial link:Mount"')
    assert execute('page should contain list "id:letters"')
    assert execute('page should contain radio button "id:agree"')
    assert execute('page should contain text field "name:name"')
    assert execute('page should contain element "name:password"')
    assert execute('input "Nikola" into text field "name:name"')
    assert execute('input "my-password" into element "name:password"')
    assert execute('click button "id:click-me"')
    assert execute('click element "xpath://*[@id="click-me"]"')
    assert execute('click image "css:.my-image"')
    assert execute('click link "Mountain"')
    assert execute('close browser')


def test_local_file_string():
    html = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample.html')
    result = run_test_string(f"""
open chrome file:///{html}
title should be "Sample Page"
page should contain "Hello World!"
page should contain button "id:click-me"
page should contain button "class:click-me"
page should contain checkbox "name:male"
page should contain checkbox "name:male"
page should contain element "tag:form"
page should contain element "xpath:/html/body/p"
page should contain image "css:.my-image"
page should contain link "Mountain"
page should contain link "partial link:Mount"
page should contain list "id:letters"
page should contain radio button "id:agree"
page should contain text field "name:name"
page should contain element "name:password"
input "Nikola" into text field "name:name"
input "my-password" into element "name:password"
click button "id:click-me"
click element "xpath://*[@id="click-me"]"
click image "css:.my-image"
click link "Mountain"
close browser""")
    assert result['STATUS']


def test_sample_page():
    result = run_test_string("""
open chrome "https://humanframework.easyaspy.org"
page title should be "Human Framework Test | Login"
element "name:username" should be visible
element "name:password" should be enabled
element "name:hidden-element" should be hidden
enter "username" into text field "name:username"
type "wrong password" into element "name:password"
click button "id:submit"
wait until page contains "Incorrect username/password"
enter "username" into text field "name:username"
type "password" into element "name:password"
click button "id:submit"
page title should be "Human Framework Test | Home"
checkbox "name:unchecked" should be unchecked
checkbox "name:checked" should be checked
close browser    
""")
    assert result['STATUS']
