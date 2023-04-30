import json
import os

import requests
from src.abc_class import Engine
from src.vacancy_class import Vacancy


class HeadHunterAPI(Engine):
    def __init__(self):
        self.url_hh = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query):
        params = {
            'text': search_query,
            'per_page': 100,
            'area': 113
        }
        response = requests.get(self.url_hh, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies_data = data['items']
            vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['name']
                salary = HeadHunterAPI.get_salary(vacancy['salary'])
                description = vacancy['snippet']['requirement']
                url = vacancy['alternate_url']
                vacancy = Vacancy(title, salary, description, url)
                vacancies.append(vacancy)
            return vacancies
        else:
            return f'Error: {response.status_code}'

    def get_salary(salary_data, **kwargs):
        if salary_data is None:
            salary = {'from': 0, 'currency': 'RUR'}
        elif 'to' not in salary_data or salary_data['to'] is None:
            salary = {'from': salary_data.get('from', 0), 'currency': salary_data.get('currency', 'RUR')}
        elif 'from' not in salary_data or salary_data['from'] is None:
            salary = {'from': salary_data['to'], 'currency': salary_data.get('currency', 'RUR')}
        else:
            salary = {'from': salary_data['from'], 'to': salary_data['to'],
                      'currency': salary_data.get('currency', 'RUR')}
        return salary


class SuperJobAPI(Engine):
    __slots__ = ("api_key", "headers", "url")
    def __init__(self):
        self.api_key = os.getenv('SJ_API_KEY')
        self.headers = {'X-Api-App-Id': self.api_key}
        self.url = "https://api.superjob.ru/2.0/vacancies/"

    def get_vacancies(self, search_query):
        params = {
            'keyword': search_query,
            'count': 100,
        }

        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies_data = data['objects']
            vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['profession']
                salary = SuperJobAPI.get_salary(vacancy)
                description = vacancy['candidat']
                url = vacancy['link']
                vacancy = Vacancy(title, salary, description, url)
                vacancies.append(vacancy)
            return vacancies
        else:
            return f'Error: {response.status_code}'

    def get_salary(vacancy, **kwargs):
        if vacancy.get('payment_to') == 0:
            salary = {'from': vacancy['payment_from'], 'currency': vacancy['currency']}
        elif vacancy.get('payment_from') == 0:
            salary = {'from': vacancy['payment_to'], 'currency': vacancy['currency']}
        else:
            salary = {'from': vacancy.get('payment_from', 0), 'to': vacancy.get('payment_to', 0),
                      'currency': vacancy.get('currency', 'rub')}
        return salary


class JSONSaver:
    def __init__(self):
        self.__file_name = 'FILE.json'

    @property
    def filename(self):
        return self.__filename

    def save_in_file(self, headhunter=None, superjob=None):
        if headhunter is not None and superjob is None:
            with open(self.__file_name, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in headhunter], key=lambda x: x['salary']['from'], reverse=True),
                    file,
                    ensure_ascii=False,
                    indent=4
                )
        elif superjob is not None and headhunter is None:
            with open(self.__file_name, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in superjob], key=lambda x: x['salary']['from'], reverse=True),
                    file,
                    ensure_ascii=False,
                    indent=4
                )
        else:
            print('Нет вакансий для сохранения')

    def get_vacancies_by_salary(self, salary_input):
        with open(self.__file_name, 'r', encoding='utf-8') as file:
            vacancy = json.load(file)
        test_dict = []
        try:
            salary, currency = salary_input.split(' ')
        except:
            salary = salary_input
            currency = ['руб', 'rur', 'rub', 'RUR']

        if currency in ['руб', 'RUR', 'rub']:
            currency = ['руб', 'rur', 'rub', 'RUR']

        for tugrik in vacancy:
            try:
                if int(tugrik['salary']['from']) >= int(salary) and tugrik['salary']['currency'] in currency:
                    test_dict.append(tugrik)
                elif tugrik['salary']['currency'] in ['usd', 'USD'] and int(tugrik['salary']['from']) * 80 >= int(
                        salary):
                    test_dict.append(tugrik)
                elif tugrik['salary']['currency'] in ['eur', 'EUR'] and int(tugrik['salary']['from']) * 90 >= int(
                        salary):
                    test_dict.append(tugrik)
            except:
                continue

        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(test_dict, file, ensure_ascii=False, indent=4)

    def search_words(self, search_words):
        if not isinstance(search_words, str):
            return "Error: запрос должен быть строкой"
        if search_words == '':
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
            return vacancies
        else:
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
            result = []
            for vacancy in vacancies:
                for word in search_words.split():
                    if vacancy['description'] is not None and search_words in vacancy['description'].lower():
                        result.append(vacancy)
                        break
            return result

    def json_results(self):
        with open(self.__file_name, 'r', encoding='utf-8') as file:
            final_result = json.load(file)
        return final_result
