#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"


def open_browser(entities, context):
    browser = 'firefox'  # default browser
    url = None
    driver = None
    for entity in entities:
        if entity['type'] == 'browser':
            browser = entity['entity']
        elif entity['type'] == 'builtin.url':
            url = entity.get('resolution', {}).get('value')
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
            if not url.startswith('http'):
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
