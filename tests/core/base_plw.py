"""В файле base_plw.py находятся функции, которые работают с html страницей"""
import csv
import json
from time import sleep

from bs4 import BeautifulSoup as bs

from files.minus_lists import MinusLists
from files.plus_lists import PlusLists
from utils.elements import *


# from dict_vacancy import vacancy as vac # Remove
# from dict_sort_plus import sort as sort # Remove


class BasePage:
    path_project = "./"

    # vacancy_no_doubles = vac  # Remove
    # vacancy_sort_title_plus = sort  # Remove

    def __init__(self, config, setup_browser):
        self.vacancy_sort_title_plus = {}  # Uncomment ! don't remove
        self.intermediate_dict = {}
        self.vacancy = {}
        self.sorted_vacancy = {}
        self.vacancy_no_doubles = {}  # Uncomment ! don't remove
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
        self.dd = {
            "vacancy_no_doubles": self.vacancy_no_doubles,
            "vacancy_sort_title_plus": self.vacancy_sort_title_plus,
        }
        self.content_plus_list = PlusLists().content_tester_python_web_plus_list
        self.content_minus_list = MinusLists().content_tester_python_web_minus_list
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

    def get_page_data(self, html, index, step):
        # выборка списка вакансий со страницы и запись в словарь self.vacancy_dict
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
            # Фильтр вакансии по заголовку
            if self.title_filter(title, step):
                key = f"{str(index)}{str(k)}"
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
            else:
                print(f"По заголовку {title} вакансия не включена в словарь Step {step}_3_{index}")
        print(self.vacancy_dict)

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

    def title_filter(self, title, step) -> bool:
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

    def sort_salary_and_delete_doubles(self, step):
        count_sorted_dict = self.sorted_for_salary(step)
        # Фильтр по одинаковому заголовку. Проверка текста вакансии.
        count_deleted = 0
        for i in range(count_sorted_dict):
            j = i + 1
            for j in range(j, count_sorted_dict):
                s_i = self.vacancy.get(i)[1] + self.vacancy.get(i)[3]
                s_j = self.vacancy.get(j)[1] + self.vacancy.get(j)[3]
                if s_i == s_j:
                    print(i, j, self.vacancy.get(i)[1])
                    sleep(2)
                    self.page.goto(self.vacancy.get(i)[2], timeout=120000)
                    text_summ1 = self.get_vac_content(self.page, i, j, self.vacancy.get(i)[2])[:500]

                    context2 = self.browser.new_context()
                    page2 = context2.new_page()
                    text_summ2 = self.get_vac_content(page2, i, j, self.vacancy.get(i)[2])[:500]

                    if text_summ1 == text_summ2:
                        count_deleted = self.delete_double_vacancy(context2, count_deleted, i)
                        break
                    context2.close()
        print(f"Удалено по одинаковому содержанию {count_deleted} вакансий.")
        print(self.vacancy)
        for i, key in enumerate(self.vacancy):
            self.vacancy_no_doubles[i] = self.vacancy.get(key)
        print(self.vacancy_no_doubles)
        self.save_results(self.vacancy_no_doubles, "hh_2022_salary")

    def sorted_for_salary(self, step):
        # сортировка по ЗП
        print(f"Всего вакансий {len(self.vacancy_dict)} step {step}_salary_sort_1")
        print(self.vacancy_dict)
        self.sorted_vacancy = dict(sorted(self.vacancy_dict.items(), key=lambda item: item[1]))
        assert len(self.vacancy_dict) == len(self.sorted_vacancy), "Сортировка произведена с ошибкой step {step}_salary_error_1"
        print(len(self.sorted_vacancy), f"step {step}_salary_sort_2")
        print(f"step {step}_salary_sort_3", self.sorted_vacancy)
        a = list(self.sorted_vacancy.keys())
        b = a[::-1]
        for i in range(len(a)):
            self.vacancy.update({i: self.sorted_vacancy.get(b[i])})
        print(f"step {step}_salary_sort_3", self.vacancy)
        assert len(self.vacancy) == len(self.sorted_vacancy), "Реверс произведен с ошибкой step {step}_salary_error_2"
        return len(a)

    def delete_double_vacancy(self, context2, count_deleted, i):
        print(f"Delete double key {i} url {self.vacancy.get(i)} ")
        self.vacancy.pop(i)
        print(len(self.vacancy))
        count_deleted += 1
        context2.close()
        return count_deleted

    def save_results(self, dict_file, file_save_name):
        for i in range(len(dict_file)):
            self.data_to_file(
                file_save_name,
                dict_file.get(i)[1],
                dict_file.get(i)[0],
                dict_file.get(i)[2],
                dict_file.get(i)[3]
            )

    def sort_for_plus_words_title(self, file_name):
        cou = 0
        for plus_word in self.content_plus_list: # Перебираем плюс слова
            for i in range(len(self.vacancy_no_doubles)):
                if self.vacancy_no_doubles.get(i) is None:
                    continue
                if self.vacancy_no_doubles.get(i)[4] == 1:
                    continue
                title = self.vacancy_no_doubles.get(i)[1].lower()
                if plus_word.lower() in title: # Если хоть одно плюс слово есть в заголовке
                    vacancy_text = self.get_vac_content(self.page, i, cou, self.vacancy_no_doubles.get(i)[2])
                    """ ???? А может добавлять текст описания вакансии в выходной файл?
                             Тогда можно просматривать вакансии без перехода по ссылке?"""
                    if self.content_plus_list[0] in vacancy_text: # Если первое слово есть в заголовке, то берем
                        print(i, title, "Vacancy add to sort_title")
                        self.vacancy_sort_title_plus[cou] = self.vacancy_no_doubles.get(i)
                        self.vacancy_no_doubles.get(i)[4] = 1
                        cou += 1
                    else:  # Плюс слова нет в заголовке. Проверяем есть ли минус слово в описании?
                        self.check_content_for_minus_word(i, vacancy_text)
        self.intermediate_sorting("vacancy_sort_title_plus")
        self.intermediate_sorting("vacancy_no_doubles")
        print(cou, self.vacancy_sort_title_plus)
        print(self.vacancy_no_doubles)
        self.save_results(self.vacancy_sort_title_plus, file_name)
        print("PASS STEP 'When sort for plus words title save to sort_plus_title_hh_2022'")
        return cou
        #   Отсортированы по заголовку cou = 35 позиций, дальше по содержанию

    def sort_for_plus_words_in_content(self, cou):
        cou = int(cou)
        for i in range(len(self.vacancy_no_doubles)):
            if self.vacancy_no_doubles.get(i)[4] == 0:
                #   1.Получить текст описания вакансии с vac.get(i)[4] = 0
                vacancy_text = self.get_vac_content(self.page, i, cou, self.vacancy_no_doubles.get(i)[2])
                #   2.Найти 2 плюс слова. Если есть - запись и  vac.get(i)[4] = 1
                if self.content_plus_list[0] in vacancy_text and self.content_plus_list[1] in vacancy_text:
                    self.get_employer(cou, i)
                    self.vacancy_sort_title_plus[cou] = self.vacancy_no_doubles.get(i)
                    cou += 1
                    print(i, cou, self.vacancy_no_doubles.get(i), "1 sort content Plus word")

        print("1 transiton on content end")
        print(self.vacancy_no_doubles)
        print(cou, self.vacancy_sort_title_plus)
        self.intermediate_sorting("vacancy_sort_title_plus")
        self.save_results(self.vacancy_sort_title_plus, "short_list_34")
        #   3.Найти хоть одно плюс слово в вакансии
        # xpath_c = "//div[contains(@class,'g-user-content')]"
        # for i in range(len(self.vacancy_no_doubles)):
        #     if self.vacancy_no_doubles.get(i)[4] == 0:
        #         vacancy_text = self.get_vac_content(self.page, i, cou, self.vacancy_no_doubles.get(i)[2])
        #         for plus_word in self.content_plus_list:
        #             if plus_word in vacancy_text in vacancy_text:
        #                 self.get_employer(cou, i)
        #                 self.vacancy_sort_title_plus[cou] = self.vacancy_no_doubles.get(i)
        #                 cou += 1
        #                 print(i, cou, self.vacancy_no_doubles.get(i), "2 sort content Plus word")
        #                 break
        #         if self.vacancy_no_doubles.get(i)[4] == 0:
        #             self.check_content_for_minus_word(i, vacancy_text)
        # self.intermediate_sorting("vacancy_no_doubles")
        # self.intermediate_sorting("vacancy_sort_title_plus")
        # print("2 transition on content end")
        # print(self.vacancy_no_doubles)
        # print(cou, self.vacancy_sort_title_plus)
        # #   4.Найти минус слова. Если есть - удалить вакансию
        # #   5.Если нет плюс и минус слов, то наверно вакансия не соответствует поиску и ее тоже надо удалить.
        # print("Final sort")
        # print(self.vacancy_no_doubles)
        # print(self.vacancy_sort_title_plus)
        # self.intermediate_sorting("vacancy_sort_title_plus")
        # self.save_results(self.vacancy_sort_title_plus, "long_list_all")

        pass

    def check_content_for_minus_word(self, i, vacancy_text):
        for minus_word in self.content_minus_list:
            if minus_word in vacancy_text:  # Если есть минус слово, то удаляем вакансию совсем.
                print(f"Удалена вакансия {i} {self.vacancy_no_doubles.get(i)[1]} по минус слову")
                self.vacancy_no_doubles.pop(i)
                break

    def get_employer(self, cou, i):
        self.vacancy_no_doubles.get(i)[4] = 1
        if self.vacancy_no_doubles.get(i)[3] == "":
            xpath_e = "//span[contains(@class,'bloko-header-section-2 bloko-header-section-2_lite')]"
            try:
                self.vacancy_no_doubles.get(i)[3] = self.page.locator(xpath_e).all_inner_texts()[2].lower()
            except:
                print(i, cou, self.vacancy_no_doubles.get(i), "Не получен работодатель")

    def get_vac_content(self, page, i: int, cou: int, url: str) -> str:
        page.goto(url, timeout=240000)
        tmpl = self.page.locator("//div[contains(@class,'tmpl_hh_wrapper')]").all_inner_texts()
        if not tmpl:
            try:
                vacancy_text = self.page.locator("//div[contains(@class,'g-user-content')]").all_inner_texts()[0].lower()
            except:
                print(i, cou, self.vacancy_no_doubles.get(i)[2])
                vacancy_text = ""
        else:
            vacancy_text = tmpl[0].lower()
        return vacancy_text

    def intermediate_sorting(self, dict_name: str):
        dictionary = {}
        if dict_name == "vacancy_no_doubles":
            dictionary = self.vacancy_no_doubles
            print("vacancy_no_doubles before", self.vacancy_no_doubles)
        elif dict_name == "vacancy_sort_title_plus":
            dictionary = self.vacancy_sort_title_plus
            print("vacancy_sort_title_plus before", self.vacancy_sort_title_plus)
        self.intermediate_dict = {}
        for i, key in enumerate(dictionary):
            self.intermediate_dict[i] = dictionary.get(key)
        if dict_name == "vacancy_no_doubles":
            self.vacancy_no_doubles = self.intermediate_dict
            print("vacancy_no_doubles after", self.vacancy_no_doubles)
        elif dict_name == "vacancy_sort_title_plus":
            self.vacancy_sort_title_plus = self.intermediate_dict
            print("vacancy_sort_title_plus after", self.vacancy_sort_title_plus)
        dictionary = self.intermediate_dict
        print("dictionary", dictionary)
        print("intermediate_sorting done")

    def for_plus_list_remove_vacancy(self, dict_name):
        for i, key in enumerate(self.dd.get(dict_name)):
            vacancy_text = self.get_vac_content(self.page, i, 0, self.dd.get(dict_name).get(i)[2])
            for plus_word in self.content_plus_list:
                if plus_word in vacancy_text in vacancy_text:
                    pass
