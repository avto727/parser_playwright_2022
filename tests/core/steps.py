from time import sleep

from pytest_bdd import given, parsers, when

from tests.core.store import Store

store = Store()
schedule_dict = {"удаленка": "remote", "гибрид": "flexible", "удаленка+гибрид": "remote&schedule=flexible"}


@given(parsers.parse("Open browser base_url keyword={keyword} schedule={schedule_ru} step {step}"))
def open_browser(config, base_page, keyword, schedule_ru, step):
    base_url = config["MAIN"]["url"]
    schedule = schedule_dict.get(schedule_ru)
    print(keyword)
    base_url.replace("schedule=", f"schedule={schedule}")
    base_page.open(f"{base_url}{keyword}")
    store["keyword"] = keyword
    print(f"Step {step} from steps.py done")


@when(parsers.parse("click {key_locator} step {step}"))
def click(base_page, key_locator, step):
    base_page.click(key_locator, step)


@when(parsers.parse("determinate total_pages to store step {step}"))
def determ_total_pages(base_page, step):
    total_pages = int(base_page.determ_last_element("paginator"))  # Сколько всего страниц
    print(f"всего страниц total_pages = {total_pages}")
    store["total_pages"] = total_pages
    print(f"Step {step} from steps.py done")


@when(parsers.parse("pages with list vacancy processing step {step}"))
def pages_processing(base_page, config, step):
    total_pages = int(store["total_pages"])
    keyword = store["keyword"]
    index = 0
    while index < total_pages:
        html = base_page.get_content_vacancies_list_page(config, index, keyword, step)
        base_page.get_page_data(html, index, step)
        index = index + 1
        sleep(1.5)
    print(f"Step {step} from steps.py done")


@when(parsers.parse("sort salary and delete doubles step {step}"))
def sort_salary_and_delete_doubles(base_page, step):
    vac_sorted_dict = base_page.sorted_for_salary(step)
    same_dict = base_page.create_same_dict(vac_sorted_dict, len(vac_sorted_dict), step)
    base_page.delete_doubles(vac_sorted_dict, same_dict, step)
    print(f"Step {step} from steps.py done")


@when(parsers.parse("sort for plus words title save to {file_name} step {step}"))
def sort_for_plus_words_title(base_page, file_name, step):
    cou = base_page.sort_for_plus_words_title(file_name)
    store["cou"] = cou
    print(f"Step {step} from steps.py done")


@when(parsers.parse("for plus_list {dict_name}"))
def for_plus_list_remove_vacancy(base_page, dict_name):
    base_page.for_plus_list_remove_vacancy(dict_name)


@when(parsers.parse("sort for plus words description vacancy step {step}"))
def sort_for_plus_words_in_content(base_page, step):
    cou = store["cou"]
    base_page.sort_for_plus_words_in_content(cou)
    print(f"Step {step} from steps.py done")
