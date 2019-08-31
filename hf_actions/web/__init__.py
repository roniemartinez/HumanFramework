#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import logging

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# TODO: add more boolean attributes
# Mapping non-existing (antonym) to existing boolean attributes
ATTRIBUTE_MAP = {
    'enabled': 'disabled',
    'visible': 'hidden',
    'unchecked': 'checked',
}

logger = logging.getLogger(__name__)


def open_browser(entities, context):
    browser = 'chrome'  # default browser
    url = None
    driver = None
    for entity in entities:
        if entity['type'] == 'browser':
            browser = entity['entity']
        elif entity['type'] == 'builtin.url':
            url = entity.get('resolution', {}).get('value')
        elif entity['type'] == 'local_url':
            url = entity['entity'].replace('\\', '/')
        elif entity['type'] == 'string' and not url:
            url = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
    if browser == 'firefox':
        driver = webdriver.Firefox()
    elif browser == 'chrome':
        driver = webdriver.Chrome()
    elif browser == 'internet explorer':
        driver = webdriver.Ie()
    elif browser == 'safari':
        driver = webdriver.Safari()
    elif browser == 'opera':
        driver = webdriver.Opera()
    if driver:
        context['WEBDRIVER'] = driver
        driver.implicitly_wait(10)
        if url:
            if not url.startswith('http') and not url.startswith('file://'):
                url = 'http://' + url
            driver.get(url)
        return True
    return False


def close_browser(entities, context):
    driver = context.get('WEBDRIVER')  # type: WebDriver
    if driver:
        driver.quit()
        return True
    return False


def assert_title(entities, context):
    driver = context.get('WEBDRIVER')  # type: WebDriver
    title = None
    if driver:
        for entity in entities:
            if entity['type'] == 'string':
                title = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
        assert driver.title == title, f'"{driver.title}" is not equal to "{title}"'
        return True
    return False


def _find_element(driver, selector, element_type=None):
    element = None
    if selector.startswith('id:'):
        id_ = selector.split(':', 1)[1].strip()
        element = driver.find_element_by_id(id_)
    elif selector.startswith('class:'):
        class_ = selector.split(':', 1)[1].strip()
        element = driver.find_element_by_class_name(class_)
    elif selector.startswith('name:'):
        name = selector.split(':', 1)[1].strip()
        element = driver.find_element_by_name(name)
    elif selector.startswith('tag:'):
        tag = selector.split(':', 1)[1].strip()
        element = driver.find_element_by_tag_name(tag)
    elif selector.startswith('xpath:'):
        xpath = selector.split(':', 1)[1].strip()
        element = driver.find_element_by_xpath(xpath)
    elif selector.startswith('css:'):
        css = selector.split(':', 1)[1].strip()
        element = driver.find_element_by_css_selector(css)
    elif selector.startswith('partial link:') or element_type == 'partial link':
        try:
            link = selector.split(':', 1)[1].strip()
        except IndexError:
            link = selector
        element = driver.find_element_by_partial_link_text(link)
    elif selector.startswith('link:') or element_type == 'link':
        try:
            link = selector.split(':', 1)[1].strip()
        except IndexError:
            link = selector
        element = driver.find_element_by_link_text(link)
    return element


def assert_contain_element(entities, context):
    driver = context.get('WEBDRIVER')  # type: WebDriver
    element_type = 'text'  # default element_type
    selector = ''  # type: str
    if driver:
        for entity in entities:
            # NOTE: button and radio button entities are detected at the same time
            if entity['type'] == 'element_type' and not element_type == 'radio button':
                element_type = entity['entity']
            elif entity['type'] == 'selector':
                selector = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
            elif entity['type'] == 'string' and not selector:
                selector = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
        wait = WebDriverWait(driver, 10)
        if element_type == 'text':
            wait.until(lambda x: selector in driver.page_source)
            return True
        elif element_type == 'button':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element and (element.tag_name == element_type or (
                        element.tag_name == 'input' and element.get_attribute('type') == element_type))

            wait.until(element_found)
            return True
        elif element_type == 'checkbox':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element and element.tag_name == 'input' and element.get_attribute('type') == element_type

            wait.until(element_found)
            return True
        elif element_type == 'element':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element

            wait.until(element_found)
            return True
        elif element_type == 'image':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element and element.tag_name == 'img'

            wait.until(element_found)
            return True
        elif element_type == 'link':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element and element.tag_name == 'a'

            wait.until(element_found)
            return True
        elif element_type == 'list':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element and element.tag_name in ('ul', 'ol')

            wait.until(element_found)
            return True
        elif element_type == 'radio button':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element and element.tag_name == 'input' and element.get_attribute('type') == 'radio'

            wait.until(element_found)
            return True
        elif element_type == 'text field':
            def element_found(param):
                element = _find_element(driver, selector, element_type)
                return element and element.tag_name == 'input' and element.get_attribute('type') == 'text'

            wait.until(element_found)
            return True
    return False


def click_element(entities, context):
    driver = context.get('WEBDRIVER')  # type: WebDriver
    element_type = 'text'  # default element_type
    selector = ''  # type: str
    element = None
    if driver:
        for entity in entities:
            # NOTE: button and radio button entities are detected at the same time
            if entity['type'] == 'element_type' and not element_type == 'radio button':
                element_type = entity['entity']
            elif entity['type'] == 'selector':
                selector = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
            elif entity['type'] == 'string' and not selector:
                selector = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
        if element_type == 'button':
            element = _find_element(driver, selector, element_type)
            assert element and (element.tag_name == element_type or (
                    element.tag_name == 'input' and element.get_attribute('type') == element_type))
        elif element_type == 'element':
            element = _find_element(driver, selector, element_type)
            assert element
        elif element_type == 'image':
            element = _find_element(driver, selector, element_type)
            assert element and element.tag_name == 'img'
        elif element_type == 'link':
            element = _find_element(driver, selector, element_type)
            assert element and element.tag_name == 'a'
        if element:
            wait = WebDriverWait(driver, 10)
            wait.until_not(lambda x: element.get_attribute('hidden') or element.get_attribute('disabled'))
            element.click()
            return True
    return False


# noinspection PyShadowingBuiltins
def input(entities, context):
    driver = context.get('WEBDRIVER')  # type: WebDriver
    element_type = 'element'  # default element_type
    input_string = ''  # type: str
    selector = ''  # type: str
    if driver:
        for entity in entities:
            # NOTE: button and radio button entities are detected at the same time
            if entity['type'] == 'element_type':
                element_type = entity['entity']
            elif entity['type'] == 'string':
                input_string = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
            elif entity['type'] == 'selector':
                selector = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
        if element_type in ('element', 'text field'):
            element = _find_element(driver, selector, element_type)
            assert element
            element.send_keys(input_string)
            return True
    return False


def assert_element_status(entities, context):
    driver = context.get('WEBDRIVER')  # type: WebDriver
    selector = ''  # type: str
    boolean_attribute = ''  # type: str
    element_type = 'element'
    if driver:
        for entity in entities:
            # NOTE: button and radio button entities are detected at the same time
            if entity['type'] == 'element_type' and not element_type == 'radio button':
                element_type = entity['entity']
            elif entity['type'] == 'selector':
                selector = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
            elif entity['type'] == 'boolean_attribute':
                boolean_attribute = entity['entity']
        element = _find_element(driver, selector, element_type)
        if element:
            wait = WebDriverWait(driver, 10)
            if boolean_attribute in ATTRIBUTE_MAP.keys():
                wait.until_not(lambda x: element.get_attribute(ATTRIBUTE_MAP.get(boolean_attribute)))
                return True
            elif boolean_attribute in ATTRIBUTE_MAP.values():
                wait.until(lambda x: element.get_attribute(boolean_attribute))
                return True
    return False
