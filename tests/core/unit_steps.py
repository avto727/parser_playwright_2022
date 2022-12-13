from time import sleep

from pytest_bdd import given, parsers, when
from dict_vacancy import vacancy
from tests.core.store import Store

store = Store()


@when(parsers.parse("check def choose_selector step {step}"))
def check_def_choose_selector(base_page, step):
    xps = base_page.xp
    texts = base_page.text
    for xp_key in xps.keys():
        locator = base_page.choose_selector(xp_key)
        # print(xp_key, locator)
        assert xps.get(xp_key) in str(locator), f"def_choose_selector wrong in xp"
        assert texts.get(xp_key) is None, f"key {xp_key} have not to in text"
    for text_key in texts.keys():
        locator = base_page.choose_selector(text_key)
        # print(text_key, locator)
        assert texts.get(text_key)[0] in str(locator), f"def_choose_selector wrong in text"
        assert xps.get(text_key) is None, f"key {text_key} have not to in xp"
    print(f"Step {step} PASS")


@when(parsers.parse("check def pass_for_one_list_vacancies_page {index}, {keyword}, step {step}"))
def check_def_pass_for_one_list_vacancies_page(base_page, config, index, keyword, step):
    # получение вакансий с 2-х страниц, запись в словарь self.vacancy_dict
    index = 0
    while index < 2:
        html = base_page.get_content_vacancies_list_page(config, index, keyword, step)
        base_page.get_page_data(html, index, step)
        index = index + 1
        sleep(1.5)
    print(f"Step {step} from unit_steps.py PASS")


@when(parsers.parse("check def title_filter step {step}"))
def check_def_title_filter(base_page, config, step):
    vac_dict = base_page.vacancy_dict
    title_auto_tester_python_minus_list = base_page.minus_list_dict.get(base_page.name_suit)
    for key in vac_dict.keys():
        title = vac_dict.get(key)[1]
        flag = base_page.title_filter(title)
        assert flag, f"Find minus word in title {title}, key {key}"
        # another way check titles
        for minus_word in title_auto_tester_python_minus_list:
            assert minus_word.lower() not in title.lower(), f"minus_word {minus_word.lower()} is in title {title.lower()}"
    print(f"Step {step}_1 from unit_steps.py PASS")


@when(parsers.parse("check def dict_sorting step {step}"))
def check_def_dict_sorting(base_page, config, step):
    base_page.dict_sorting(vacancy)

@when(parsers.parse("check def delete_doubles step {step}"))
def check_def_delete_doubles(base_page, config, step):
    vac_sorted_dict = vacancy
    same_dict = base_page.create_same_dict(vac_sorted_dict, len(vac_sorted_dict), step)
    base_page.delete_doubles(vac_sorted_dict, same_dict, step)
