import os
from datetime import datetime
from time import sleep

from pytest_bdd import given, parsers, when, then


@given("Open browser base_url")
def open_browser(config, base_page):
    keyword = config["tester_python_web"]["keyword"]
    base_url = config["MAIN"]["url"]
    schedule = config["tester_python_web"]["schedule"]
    print(schedule)
    base_page.open(f"{base_url}{keyword}")

@when(parsers.parse("click {key_locator} step {step}"))
def click(base_page, key_locator, step):
    base_page.click(key_locator, step)