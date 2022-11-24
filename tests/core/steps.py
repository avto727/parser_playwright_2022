import os
from datetime import datetime
from time import sleep

from pytest_bdd import given, parsers, when, then


@given("Open browser")
def open_browser(config, base_page):
    schedule = config["tester_python_web"]["schedule"]
    print(schedule)
    base_page.open("https://hh.ru/search/vacancy")
    pass

