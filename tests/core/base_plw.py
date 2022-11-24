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
        self.choose_selector(keyword).click()
        print(f"Step {step}. Click {keyword} done.")

    def determ_last_element(self, keyword):
        el = self.choose_selector(keyword)
        res = el.last.all_inner_texts()[0]
        return res


    def choose_selector(self, keyword):
        selector = ""
        if self.xp.get(keyword) is not None:
            selector = self.xp.get(keyword)
            return self.page.locator(selector)
        if keyword in self.text:
            selector = self.text.get(keyword)
            return self.page.locator(selector[0], has_text=selector[1])
        else:
            print("Undefined selector")

    def get_page_data(self, html):
        pass