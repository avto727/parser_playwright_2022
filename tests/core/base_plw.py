"""В файле base_plw.py находятся функции, которые работают с html страницей"""
import csv
import json
from time import sleep

from bs4 import BeautifulSoup as bs

from files.minus_lists import MinusLists
from utils.elements import *


class BasePage:
    path_project = "./"

    def __init__(self, config, setup_browser):
        self.page = setup_browser.page
        self.browser = setup_browser.browser
        self.elem = Elem()
        self.xp = self.elem.xp
        self.text = self.elem.text
        self.vacancy_dict: dict = {}
        self.minus_list_dict = {
            "tester_python_web": MinusLists.title_tester_python_web_minus_list,
            "dev_ios": MinusLists.title_dev_ios_minus_list,
        }
        self.name_suit = config["MAIN"]["name_suit"]

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
        index += 100 # Вместо индекса цифры поставить букву.
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
                else:
                    compensation = "0"
                self.vacancy_dict[key] = [int(compensation), title, href]
                k += 1

        # print(self.vacancy_dict)
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

    def title_filter(self, config, title) -> bool:
        pass
        title_auto_tester_python_minus_list = self.minus_list_dict.get(self.name_suit)
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
        # сортировка по ЗП
        print(f"Всего вакансий {len(self.vacancy_dict)}")
        print(self.vacancy_dict)
        sorted_vacancy = dict(sorted(self.vacancy_dict.items(), key=lambda item: item[1]))
        assert len(self.vacancy_dict) == len(sorted_vacancy), "Сортировка произведена с ошибкой"
        print(len(sorted_vacancy))
        print(sorted_vacancy)
        vacancy = {}
        a = list(sorted_vacancy.keys())
        b = a[::-1]
        for i in range(len(a)):
            vacancy.update({i: sorted_vacancy.get(b[i])})
        print(vacancy)
        assert len(vacancy) == len(sorted_vacancy), "Реверс произведен с ошибкой"
        # Фильтр по одинаковому заголовку. Проверка текста вакансии.
        count_deleted = 0
        for i in range(len(a)):
            j = i + 1
            for j in range(j, len(a)):
                if vacancy.get(i)[1] == vacancy.get(j)[1]:
                    print(vacancy.get(i)[1])
                    print(vacancy.get(j)[1])
                    self.page.goto(vacancy.get(i)[2])
                    context2 = self.browser.new_context()
                    page2 = context2.new_page()
                    page2.goto(vacancy.get(j)[2])
                    content1 = self.page.content()
                    soup1 = bs(content1, 'html.parser')
                    p_all1 = soup1.find('div', class_='g-user-content').find_all('p')
                    # sleep(3)
                    text_summ1 = ""
                    for ind in range(3):
                        try:
                            text_summ1 += p_all1[ind].text
                        except:
                            continue
                    content2 = page2.content()
                    soup2 = bs(content2, 'html.parser')
                    # sleep(3)
                    p_all2 = soup2.find('div', class_='g-user-content').find_all('p')
                    text_summ2 = ""
                    for ind in range(3):
                        try:
                            text_summ2 += p_all2[ind].text
                        except:
                            continue
                    if text_summ1 == text_summ2:
                        print(f"Delete vacancy key {i} url {vacancy.get(j)} ")
                        count_deleted += 1
                    else:
                        context2.close()

            pass
