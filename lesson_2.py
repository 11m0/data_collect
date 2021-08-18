import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

search_query = input('Введите ключевое слово: ')
start_page = int(input('Введите страницу начала поиска: '))
end_page = int(input('Введите страницу окончания поиска: '))

main_url_1 = 'https://hh.ru'
main_url_2 = 'https://www.superjob.ru'

add_url_1 = f'/search/vacancy?text={search_query}&page={start_page - 1}'
add_url_2 = f'/vacancy/search/?keywords={search_query}&noGeo=1&page={start_page}'

vacancies = []

while add_url_1 and int(add_url_1.rpartition('=')[2]) < end_page:

    try:
        response = requests.get(main_url_1 + add_url_1, headers=headers)
    except OSError:
        print('Ошибка соединения')
        break

    if response.ok:
        soup = bs(response.text, 'html.parser')
        vacancies_list = soup.findAll('div', {'class': 'vacancy-serp-item'})
        print(f'Скраппинг {int(add_url_1.rpartition("=")[2]) + 1}-й страницы сайта {main_url_1}')
        for vacancy in vacancies_list:
            vacancy_data = {}
            vacancy_site = main_url_1
            vacancy_name = vacancy.find('a').getText()
            vacancy_link = vacancy.find('a')['href'].replace(f'?from=vacancy_search_list&query={search_query}', '')
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

            if vacancy_salary:
                vacancy_salary = vacancy_salary.getText().replace('\u202f', ' ')
                if vacancy_salary.startswith('до'):
                    vacancy_salary_min, vacancy_salary_max = None, vacancy_salary.partition(' ')[2].rpartition(' ')[0]
                    vacancy_salary_val = vacancy_salary.partition(' ')[2].rpartition(' ')[2]
                elif vacancy_salary.startswith('от'):
                    vacancy_salary_min, vacancy_salary_max = vacancy_salary.partition(' ')[2].rpartition(' ')[0], None
                    vacancy_salary_val = vacancy_salary.partition(' ')[2].rpartition(' ')[2]
                else:
                    vacancy_salary_min = vacancy_salary.partition(' – ')[0]
                    vacancy_salary_max = vacancy_salary.partition(' – ')[2].rpartition(' ')[0]
                    vacancy_salary_val = vacancy_salary.partition(' – ')[2].rpartition(' ')[2]
            else:
                vacancy_salary_min, vacancy_salary_max, vacancy_salary_val = None, None, None

            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['website'] = vacancy_site
            vacancy_data['salary_min'] = vacancy_salary_min
            vacancy_data['salary_max'] = vacancy_salary_max
            vacancy_data['salary_value'] = vacancy_salary_val

            vacancies.append(vacancy_data)

        try:
            add_url_1 = soup.find('a', {'data-qa': 'pager-next'})['href']
        except TypeError:
            print(f'Страницы закончились. Поиск на сайте {main_url_1} остановлен')
            add_url_1 = None

while add_url_2 and int(add_url_2.rpartition('=')[2]) <= end_page:

    try:
        response = requests.get(main_url_2 + add_url_2, headers=headers)
    except OSError:
        print('Ошибка соединения')
        break

    if response.ok:
        soup = bs(response.text, 'html.parser')
        vacancies_list = soup.findAll('div', {'class': 'f-test-vacancy-item'})
        print(f'Скраппинг {add_url_2.rpartition("=")[2]}-й страницы сайта {main_url_2}')
        for vacancy in vacancies_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a').getText()
            vacancy_link = main_url_2 + vacancy.find('a')['href']
            vacancy_site = main_url_2
            vacancy_salary = vacancy.find('span', {'class': '_2Wp8I'}).getText().replace('\xa0', ' ')

            if vacancy_salary.startswith('до'):
                vacancy_salary_min, vacancy_salary_max = None, vacancy_salary.partition(' ')[2].rpartition(' ')[0]
                vacancy_salary_val = vacancy_salary.partition(' ')[2].rpartition(' ')[2]
            elif vacancy_salary.startswith('от'):
                vacancy_salary_min, vacancy_salary_max = vacancy_salary.partition(' ')[2].rpartition(' ')[0], None
                vacancy_salary_val = vacancy_salary.partition(' ')[2].rpartition(' ')[2]
            elif vacancy_salary.startswith('По'):
                vacancy_salary_min, vacancy_salary_max, vacancy_salary_val = None, None, None
            elif (vacancy_salary.startswith('до') and vacancy_salary.startswith('от')) is False \
                    and vacancy_salary.find('—') == -1:
                vacancy_salary_min = vacancy_salary_max = vacancy_salary.rpartition(' ')[0]
                vacancy_salary_val = vacancy_salary.rpartition(' ')[2]
            else:
                vacancy_salary_min = vacancy_salary.partition(' — ')[0]
                vacancy_salary_max = vacancy_salary.partition(' — ')[2].rpartition(' ')[0]
                vacancy_salary_val = vacancy_salary.partition(' — ')[2].rpartition(' ')[2]

            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['website'] = vacancy_site
            vacancy_data['salary_min'] = vacancy_salary_min
            vacancy_data['salary_max'] = vacancy_salary_max
            vacancy_data['salary_value'] = vacancy_salary_val

            vacancies.append(vacancy_data)

        try:
            add_url_2 = soup.find('a', {'class': 'f-test-link-Dalshe'})['href']
        except TypeError:
            print(f'Страницы закончились. Поиск на сайте {main_url_2} остановлен')
            add_url_2 = None

df = pd.DataFrame(data=vacancies)
df.to_csv('lesson_2.csv', index=False)
