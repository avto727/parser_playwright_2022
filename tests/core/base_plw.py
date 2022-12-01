"""В файле base_plw.py находятся функции, которые работают с html страницей"""
import csv
import json
from time import sleep

from bs4 import BeautifulSoup as bs

from files.minus_lists import MinusLists
from files.plus_lists import PlusLists
from utils.elements import *
from dict_vacancy import vacancy as vac # Remove


class BasePage:
    path_project = "./"
    vacancy_no_doubles = vac # Remove

    def __init__(self, config, setup_browser):
        self.vacancy_sort_title_plus = {}
        # self.vacancy_no_doubles = {} # Uncomment !
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
        self.page.goto(url, timeout=90000)

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
        employer_red = ''
        soup = bs(html, 'html.parser')
        table = soup.find('div', id='a11y-main-content')
        k = 0
        index += 100  # Вместо индекса цифры поставить букву.
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
            try:
                employer = ad.find('a', class_='bloko-link bloko-link_kind-tertiary').text
            except:
                employer = ''
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
                if employer.startswith("ООО"):
                    employer_red = f"ООО {employer[4:]}"
                flag = 0
                self.vacancy_dict[key] = [int(compensation), title, href, employer_red, flag]
                k += 1

        print(self.vacancy_dict)
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
    def data_to_file(file_save_name, el1, el2, el3, el4):
        data = {
            'title': el1,
            'schedule': el2,
            'compensation': el3,
            'href': el4
        }
        with open(f'{file_save_name}.csv', 'a', encoding='utf-8-sig') as f:
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

    def sort_salary_and_delete_doubles(self):
        a = self.sorted_for_salary()

        # Фильтр по одинаковому заголовку. Проверка текста вакансии.
        count_deleted = 0
        for i in range(len(a)):
            j = i + 1
            for j in range(j, len(a)):
                s_i = self.vacancy.get(i)[1] + self.vacancy.get(i)[3]
                s_j = self.vacancy.get(j)[1] + self.vacancy.get(j)[3]
                if s_i == s_j:
                    print(i, j, self.vacancy.get(i)[1])
                    sleep(2)
                    self.page.goto(self.vacancy.get(i)[2], timeout=120000)
                    content1 = self.page.content()
                    soup1 = bs(content1, 'html.parser')
                    p_all1 = soup1.find('div', class_='g-user-content').find_all('p')
                    text_summ1 = ""
                    for ind in range(3):
                        try:
                            text_summ1 += p_all1[ind].text
                        except:
                            continue

                    context2 = self.browser.new_context()
                    page2 = context2.new_page()
                    page2.goto(self.vacancy.get(j)[2], timeout=120000)
                    sleep(2)
                    content2 = page2.content()
                    soup2 = bs(content2, 'html.parser')
                    text_summ2 = ""

                    try:
                        p_all2 = soup2.find('div', class_='g-user-content').find_all('p')
                    except:
                        print("      !!!    Текст со страницы не получен!!!")
                    for ind in range(3):
                        try:
                            text_summ2 += p_all2[ind].text
                        except:
                            text_summ2 += ""

                    if text_summ1 == text_summ2:
                        count_deleted = self.delete_double_vacancy(context2, count_deleted, i)
                        break
                    context2.close()
        print(f"Удалено по одинаковому содержанию {count_deleted} вакансий.")
        print(self.vacancy)
        for i, key in enumerate(self.vacancy):
            self.vacancy_no_doubles[i] = self.vacancy.get(key)
        print(self.vacancy_no_doubles)

    def sorted_for_salary(self):
        # сортировка по ЗП
        print(f"Всего вакансий {len(self.vacancy_dict)}")
        print(self.vacancy_dict)
        self.sorted_vacancy = dict(sorted(self.vacancy_dict.items(), key=lambda item: item[1]))
        assert len(self.vacancy_dict) == len(self.sorted_vacancy), "Сортировка произведена с ошибкой"
        print(len(self.sorted_vacancy))
        print(self.sorted_vacancy)
        self.vacancy = {}
        a = list(self.sorted_vacancy.keys())
        b = a[::-1]
        for i in range(len(a)):
            self.vacancy.update({i: self.sorted_vacancy.get(b[i])})
        print(self.vacancy)
        assert len(self.vacancy) == len(self.sorted_vacancy), "Реверс произведен с ошибкой"
        return a

    def delete_double_vacancy(self, context2, count_deleted, i):
        print(f"Delete vacancy key {i} url {self.vacancy.get(i)} ")
        self.vacancy.pop(i)
        print(len(self.vacancy))
        count_deleted += 1
        context2.close()
        return count_deleted

    def save_results(self, dict_name, file_save_name):
        dd = {
            "vacancy_no_doubles": self.vacancy_no_doubles,
            "vacancy_sort_title_plus": self.vacancy_sort_title_plus,
        }
        for i in range(len(dd.get(dict_name))):
            self.data_to_file(
                file_save_name,
                dd.get(dict_name).get(i)[1],
                dd.get(dict_name).get(i)[0],
                dd.get(dict_name).get(i)[2],
                dd.get(dict_name).get(i)[3]
            )

    def sort_for_plus_words_title(self, file_name):
        plus_list = PlusLists().content_tester_python_web_plus_list
        cou = 0
        for plus_word in plus_list:
            for i in range(len(self.vacancy_no_doubles)):
                if self.vacancy_no_doubles.get(i)[4] == 1:
                    continue
                title = self.vacancy_no_doubles.get(i)[1].lower()
                if plus_word.lower() in title:
                    print(i, title)
                    self.vacancy_sort_title_plus[cou] = self.vacancy_no_doubles.get(i)
                    self.vacancy_no_doubles.get(i)[4] = 1
                    cou += 1
        print(cou, self.vacancy_sort_title_plus)
        print(self.vacancy_no_doubles)
        self.save_results("vacancy_sort_title_plus", file_name)
        #   Отсортированы по заголовку cou = 35 позиций, дальше по содержанию
        for i in range(len(self.vacancy_no_doubles)):
            if self.vacancy_no_doubles.get(i)[4] == 0:
        #   1.Получить текст описания вакансии с vac.get(i)[4] = 0
                self.page.goto(self.vacancy_no_doubles.get(i)[2], timeout=240000)
                try:
                    vacancy_text = self.page.locator("//div[contains(@class,'g-user-content')]").all_inner_texts()[0].lower()
                except:
                    print(i, cou, self.vacancy_no_doubles.get(i)[2])
                    continue
       #   2.Найти 2 плюс слова. Если есть - запись и  vac.get(i)[4] = 1
                if plus_list[0] in vacancy_text and plus_list[1] in vacancy_text:
                    self.vacancy_no_doubles.get(i)[4] = 1
                    self.vacancy_sort_title_plus[cou] = self.vacancy_no_doubles.get(i)
                    cou += 1
                    print(i, cou, self.vacancy_no_doubles.get(i), "sort content Plus word")

        print("1 transiton on content end")
        print(cou, self.vacancy_sort_title_plus)
        #   3.Найти хоть одно плюс слово в вакансии
        xpath_c = "//div[contains(@class,'g-user-content')]"
        for i in range(len(self.vacancy_no_doubles)):
            if self.vacancy_no_doubles.get(i)[4] == 0:
                self.page.goto(self.vacancy_no_doubles.get(i)[2], timeout=120000)
                vacancy_text = self.page.locator(xpath_c).all_inner_texts()[0].lower()
                for plus_word in plus_list:
                    if plus_word in vacancy_text in vacancy_text:
                        self.vacancy_no_doubles.get(i)[4] = 1
                        self.vacancy_sort_title_plus[cou] = self.vacancy_no_doubles.get(i)
                        cou += 1
                        print(i, cou, self.vacancy_no_doubles.get(i), "sort content Plus word")
                        break
        print("2 transiton on content end")
        print(cou, self.vacancy_sort_title_plus)
        self.save_results("vacancy_sort_title_plus", "sort_content_hh")
        #   3.Найти минус слова. Если есть - удалить вакансию
        #   4.Если нет плюс и минус слов, то наверно вакансия не соответствует поиску и ее тоже надо удалить.
