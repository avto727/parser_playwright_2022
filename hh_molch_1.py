import requests
from bs4 import BeautifulSoup as bs
import csv
# План
#1. Выяснить количество страниц
#2. Сформировать список урлов на страницы выдачи
#3. собрать данные
#

# Функция вывода html кода всей страницы
def get_html(base_url):
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
               }
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        return request.content

#Выясняем количество страниц
def get_total_pages(html):
    soup = bs(html, 'html.parser')
    #Класс = значению из html кода (следующая страница)
    total_pages = soup.find_all('a', class_='bloko-button HH-Pager-Control')[-1].text
    return int(total_pages)
#Функция сохранения данных в файл  csv
def write_csv(date):
    with open('hh.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        writer.writerow( (date['name'], date['schedule'], date['compensation'], date['href']) )

# функция сбора данных со страницы поиска
def get_page_data(html):
    # выборка нужных данных
    soup = bs(html, 'html.parser')
    #print(soup)
    ads = soup.find('div', class_='vacancy-serp')#.find_all('div', class_='vacancy-serp-item  vacancy-serp-item_premium')
    # print(ads)
    for ad in ads:
        try:
            name = ad.find('div', class_='resume-search-item__name').text
        except:
            name = ''
        try:
            schedule = ad.find('div', class_='vacancy-list-work-schedule HH-Vacancy-Work-Schedule').text
        except:
            schedule = ''

        try:
            compensation = ad.find('div', class_='vacancy-serp-item__compensation').text
        except:
            compensation = ''
        try:
            href = ad.find('a', class_='bloko-link HH-LinkModifier').get('href')
        except:
            href = ''
        if 'дома' in schedule:
            print(name, ' ', schedule, ' ', compensation, ' ', href)

            data = {'name':name,
                    'schedule':schedule,
                    'compensation':compensation,
                    'href':href}

            write_csv(data)

def main():
    #Начало url
    keyword = 'тестировщик'
    base_url = 'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true'
    #Номер страницы
    page_part = '&page='
    # Поисковый запрос
    query_part = '&text=' # '?text='
    total_pages = get_total_pages(get_html(base_url))
    print('total_pages = ', total_pages)
    for i in range(0, total_pages):#задаем диапазон просматриваемых страниц. вместо total_pages  ставим 3
        #   Формирование url (склеивание)
        url_gen = base_url + query_part + keyword + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()