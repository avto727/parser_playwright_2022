"""В файле base_plw.py находятся функции, которые работают с html страницей"""
from utils.elements import *


class BasePage:
    path_project = "./"

    def __init__(self, setup_browser):
        self.page = setup_browser.page
        self.elem = Elem()
        self.xp = self.elem.xp
        self.text = self.elem.text

    def open(self, url):
        self.page.goto(url)

    def click(self, keyword, step):
        selector = ""
        if self.xp.get(keyword) is not None:
            selector = self.xp(keyword)
        if keyword in self.text:
            selector = self.text.get(keyword)
        if type(selector) == dict:
            self.page.locator(selector).click()
        elif type(selector) == list:
            self.page.locator(selector[0], has_text=selector[1]).click()
        else:
            print("Undefined selector")
        print(f"Step {step}. Click {keyword} done.")
