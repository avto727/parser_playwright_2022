import os
from datetime import datetime
from time import sleep

from pytest_bdd import given, parsers, when, then
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
        base_page.data_to_file(f"страница {index}", "", "", "")
        base_page.open(search_url)
        html = base_page.page.content()
        base_page.get_page_data(config, html, index)
        index = index + 1

@when("sort and save results")
def sort_and_save_results(base_page):
    base_page.sort_and_save_results()
