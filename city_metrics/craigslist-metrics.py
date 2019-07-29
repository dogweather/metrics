#!/usr/bin/env python

import sys

from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

TOPIC_SLUGS = {
    'musicians': 'muc',
    'instruments':  'msa'
}


def make_web_driver() -> WebDriver:
    """Instantiate a new automated web browser"""
    options = Options()
    options.add_argument('--headless')
    return Chrome(options=options)


def get_post_count(driver: WebDriver, subdomain: str, topic: str) -> str:
    """Return the number of 'musicians' or 'music instruments for sale' posts in the given city"""
    domain = f'{subdomain}.craigslist.org'
    slug   = TOPIC_SLUGS[topic]
    driver.get(f'https://{domain}/search/{slug}')
    return driver.find_element_by_css_selector('span.totalcount').text


topic           = sys.argv[1]
city_subdomains = sys.argv[2:]
driver          = make_web_driver()

for subdomain in city_subdomains:
    try:
        total_count = get_post_count(driver, subdomain, topic)
    except NoSuchElementException:
        total_count = '0'

    print(f'{subdomain}, {total_count}')

driver.close()
