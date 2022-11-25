"""В файле base_plw.py находятся функции, которые работают с html страницей"""
import csv
import json
from bs4 import BeautifulSoup as bs

from files.minus_lists import MinusLists
from utils.elements import *


class BasePage:
    path_project = "./"

    def __init__(self, setup_browser):
        self.page = setup_browser.page
        self.elem = Elem()
        self.xp = self.elem.xp
        self.text = self.elem.text
        self.vacancy_dict: dict = {}

    def open(self, url):
        self.page.goto(url)

    def click(self, keyword, step):
        self.choose_selector(keyword).click()
        print(f"Step {step}. Click {keyword} done.")

    def determ_last_element(self, keyword):
        el = self.choose_selector(keyword)
        if not el.last.all_inner_texts():
            res = "0"
        else:
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

    def get_page_data(self, config, html, index):
        # выборка нужных данных
        soup = bs(html, 'html.parser')
        table = soup.find('div', id='a11y-main-content')
        k = 0
        index += 1 # Вместо индекса цифры поставить букву.
        for i, ad in enumerate(table):
            try:
                title = ad.find('a', class_='serp-item__title').text
            except:
                title = ''
            try:
                schedule = ad.find(
                    'div', class_='vacancy-serp-item__label'
                ).find(
                    'div', class_='search-result-label search-result-label_work-schedule'
                ).find(
                    'div', class_='bloko-text').text
            except:
                schedule = ''
            try:
                compensation = ad.find('span', class_='bloko-header-section-3').text
            except:
                compensation = ''
            try:
                href = ad.find('a', class_='serp-item__title').get('href').split("?")[0]
            except:
                href = ''
            # Filters
            if self.title_filter(config, title):
                key = f"{str(index)}{str(k)}"
                # print(i, title, schedule, compensation, href)
                print(key, title, compensation)
                if compensation != "":
                    # print(self.processing_compensation(compensation))
                    compensation = self.processing_compensation(compensation)
                self.vacancy_dict[key] = [title, compensation, href]
                k += 1

        # print(self.vacancy_dict)
    #     processing compensation
        comp = self.vacancy_dict.get("10")[1]
        print(comp)
        pass
    #         Sort

    # Save to file
    #   self.data_to_file(i, title, compensation, href)

    @staticmethod
    def processing_compensation(compensation):
        sum_string = ""
        for lit in compensation:
            if lit.isdecimal():
                sum_string += lit
                if "usd" in compensation.lower() or "eur" in compensation.lower():
                    if len(sum_string) == 4:
                        sum_string = str(int(sum_string) * 60)
                        break
                else:
                    if len(sum_string) == 6:
                        if sum_string[5] != "0":
                            sum_string = sum_string[0:5]
                        break
        return sum_string
    @staticmethod
    def data_to_file(el1, el2, el3, el4):
        data = {
            'title': el1,
            'schedule': el2,
            'compensation': el3,
            'href': el4
        }
        with open('hh_2022.csv', 'a', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerow((data['title'], data['schedule'], data['compensation'], data['href']))

    @staticmethod
    def title_filter(config, title) -> bool:
        pass
        title_auto_tester_python_minus_list = MinusLists.title_auto_tester_python_minus_list
        flag = True
        for minus_word in title_auto_tester_python_minus_list:
            if minus_word.lower() in title.lower():
                flag = False
                break
        if title != "" and flag:
            return True
        else:
            return False

    def sort_and_save_results(self):
        # parsed = json.loads(str(self.vacancy_dict))
        # print(json.dumps(parsed, indent=4))
        print(self.vacancy_dict)
        pass