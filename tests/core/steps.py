from time import sleep

from pytest_bdd import given, parsers, when

from tests.core.store import Store

store = Store()
schedule_dict = {"удаленка": "remote", "гибрид": "flexible", "удаленка+гибрид": "remote&schedule=flexible"}


@given(parsers.parse("Open browser base_url keyword={keyword} schedule={schedule_ru}"))
def open_browser(config, base_page, keyword, schedule_ru):
    base_url = config["MAIN"]["url"]
    schedule = schedule_dict.get(schedule_ru)
    print(keyword)
    base_url.replace("schedule=", f"schedule={schedule}")
    base_page.open(f"{base_url}{keyword}")
    store["keyword"] = keyword


@when(parsers.parse("click {key_locator} step {step}"))
def click(base_page, key_locator, step):
    base_page.click(key_locator, step)


@when("determinate total_pages to store")
def determ_total_pages(base_page):
    total_pages = int(base_page.determ_last_element("paginator"))  # Сколько всего страниц
    print(f"всего страниц total_pages = {total_pages}")
    store["total_pages"] = total_pages


@when("pages processing")
def pages_processing(base_page, config):
    total_pages = int(store["total_pages"])
    keyword = store["keyword"]
    s_url = config["MAIN"]["search_url"]

    index = 0
    while index < total_pages:
    # while index < 2:
        search_url = s_url.replace("text=1", f"text={keyword}").replace("page=1", f"page={index}")
        print(f"\nПроход по стр {index}")
        base_page.open(search_url)
        html = base_page.page.content()
        base_page.get_page_data(config, html, index)
        index = index + 1
        sleep(1.5)


@when("sort salary and delete doubles")
def sort_salary_and_delete_doubles(base_page):
    base_page.sort_salary_and_delete_doubles()


@when(parsers.parse("sort for plus words title save to {file_name}"))
def sort_for_plus_words_title(base_page, file_name):
    cou = base_page.sort_for_plus_words_title(file_name)
    store["cou"] = cou




@when(parsers.parse("save results {dict_name} in {file_save_name}"))
def save_results(base_page, dict_name, file_save_name):
    base_page.save_results(dict_name, file_save_name)


@when("sort for plus words description vacancy")
def sort_for_plus_words_in_content(base_page):
    cou = store["cou"]
    base_page.sort_for_plus_words_in_content(cou)