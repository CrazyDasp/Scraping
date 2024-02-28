import requests
import fake_headers
import bs4
from pprint import pprint

URL = "https://spb.hh.ru/search/vacancy?text=Python+django+flask&salary=&ored_clusters=true&area=1&area=2&page"

def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()

for x in range(100):
    response = requests.get(f'{URL}={x}', headers=gen_headers())
    html_data = bs4.BeautifulSoup(response.text, "lxml")

    main_page = html_data.find('main', class_="vacancy-serp-content")
    
    vacancy_list = main_page.find_all('div', class_="serp-item serp-item_link")
    
    if vacancy_list != []:
        print(f'Страница {x + 1}')
    else:
        break

    for vacancy in vacancy_list:
        title = vacancy.find("span", class_="serp-item__title serp-item__title-link").text
        company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' ')
        salary = ''
        if vacancy.find("span", class_="bloko-header-section-2") != None:
            salary = vacancy.find("span", class_="bloko-header-section-2").text.replace('\u202f', ' ')
        city = vacancy.find("div", {'data-qa':'vacancy-serp__vacancy-address'}).text.split(',')[0]
        link = vacancy.find("a", class_="bloko-link")['href']
        if salary != '':
            pprint({'Компания': company, 'Должность': title, 'Город': city, 'ЗП': salary, 'Ссылка': link})
        else:
            pprint({'Компания': company, 'Должность': title,'Город': city, 'ЗП': 'Не указано', 'Ссылка': link})
    
    print()
    
