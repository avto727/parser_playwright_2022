"""В файле base_plw.py находятся функции, которые работают с html страницей"""
from utils.elements import *


class BasePage:
    path_project = "./"

    def __init__(self, setup_browser):
        self.page = setup_browser.page
        self.elem = Elem()

    def open(self, url):
        self.page.goto(url)

