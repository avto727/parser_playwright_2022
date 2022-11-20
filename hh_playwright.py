import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup as bs

import csv


# План
# 1. Выяснить количество страниц
# 2. Сформировать список урлов на страницы выдачи
# 3. собрать данные
#


# Функция вывода html кода всей страницы
def get_html(base_url):
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
               }
    # session = requests.Session()
    # request = session.get(base_url, headers=headers)
    # if request.status_code == 200:

    #     print(page.content())
    # return request.content


# Выясняем количество страниц
def get_total_pages(html):
    pass


#     return int(total_pages)
# Функция сохранения данных в файл  csv
def write_csv(date):
    with open('hh_2022.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        writer.writerow((date['title'], date['compensation'], date['href']))
# //span[@class="vacancy-serp__vacancy-compensation"]
# //div[@class="vacancy-serp-content"]

# функция сбора данных со страницы поиска
def get_page_data(html):
    # выборка нужных данных
    soup = bs(html, 'html.parser')
    table = soup.find('div', id='a11y-main-content')  # .find_all('div', class_='vacancy-serp-item  vacancy-serp-item_premium')
    for i, ad in enumerate(table):
        try:
            title = ad.find('a', class_='serp-item__title').text
        except:
            title = ''
        try:
            schedule = ad.find('div', class_='vacancy-serp-item__label').find('div', class_='search-result-label search-result-label_work-schedule').find('div', class_='bloko-text').text
        except:
            schedule = ''
        try:
            compensation = ad.find('span', class_='bloko-header-section-3').text
        except:
            compensation = ''
        try:
            href = ad.find('a', class_='serp-item__title').get('href')
        except:
            href = ''
        if title != "":
            print(i, title, ' ', schedule, ' ', compensation, ' ', href)

            data = {'title': title,
                    'schedule': schedule,
                    'compensation': compensation,
                    'href': href}

            write_csv(data)


def test_main(playwright: Playwright):
    # Поисковый запрос
    keyword = 'тестировщик'
    # keyword = 'swift'
    # keyword = 'python'
    base_url = f"https://hh.ru/search/vacancy?schedule=remote&text={keyword}"

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url)

    # Close modal window confirm city
    page.locator("span", has_text="Всё верно").click()

    paginator_all = page.locator("//span[contains(@class,'pager-item-not-in-short-range')]")
    total_pages = int(paginator_all.last.inner_text()) # Сколько всего страниц
    print(f"всего страниц total_pages = {total_pages}")

    index = 0
    while index < total_pages:
        remote_url = f"https://hh.ru/search/vacancy?schedule=remote&text={keyword}&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={index}&hhtmFrom=vacancy_search_list"
        print(f"\nПроход по стр {index}")

        data = {
                'title': f"страница {index}",
                'schedule': "",
                'compensation': "",
                'href': ""
                }
        write_csv(data)

        page.goto(remote_url)
        html = page.content()
        get_page_data(html)
        index = index + 1
    pass
    # total_pages = get_total_pages(get_html(base_url))
    # print('total_pages = ', total_pages)
    # for i in range(0, total_pages):  # задаем диапазон просматриваемых страниц. вместо total_pages  ставим 3
    #     #   Формирование url (склеивание)
    #     url_gen = base_url + query_part + keyword + page_part + str(i)
    #     # print(url_gen)
    #     html = get_html(url_gen)
    #     get_page_data(html)

# if __title__ == '__main__':
#     main()
