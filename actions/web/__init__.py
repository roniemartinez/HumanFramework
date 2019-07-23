#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"


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
    if browser == 'firefox':
        from selenium import webdriver
        driver = webdriver.Firefox()
    elif browser == 'chrome':
        from selenium import webdriver
        driver = webdriver.Chrome()
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
    driver = context.get('WEBDRIVER')
    if driver:
        driver.quit()
        return True
    return False


def assert_title(entities, context):
    driver = context.get('WEBDRIVER')
    title = None
    if driver:
        for entity in entities:
            if entity['type'] == 'string':
                title = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
        assert driver.title == title, f'"{driver.title}" is not equal to "{title}"'
        return True
    return False


def assert_contain_text(entities, context):
    driver = context.get('WEBDRIVER')
    text = None
    if driver:
        for entity in entities:
            if entity['type'] == 'string':
                text = context['QUERY'][int(entity['startIndex']) + 1:int(entity['endIndex'])]
        assert text in driver.page_source, f'page does not contain "{text}"'
        return True
    return False
