import json
import os

import requests
from src.abc_class import Engine


class HeadHunterAPI(Engine):
    def __init__(self):
        self.api_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query):
        response = requests.get(self.api_url, params={"text": search_query})
        if response.status_code == 200:
            return json.loads(response.text)["items"]
        else:
            return []


class SuperJobAPI(Engine):
    def __init__(self):
        self.api_url = "https://api.superjob.ru/2.0/vacancies/"
        self.my_app_id = os.getenv("SJ_API_KEY")

    def get_vacancies(self, search_query):
        headers = {"X-Api-App-Id": self.my_app_id}
        response = requests.get(self.api_url, headers=headers, params={"keyword": search_query})
        if response.status_code == 200:
            return json.loads(response.text)["objects"]
        else:
            return []


class Vacancy:
    def __init__(self, title, url, salary, description):
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description


class JSONSaver:
    def __init__(self):
        self.file_path = "vacancies.json"
        self.vacancies = []

    def add_vacancy(self, vacancy):
        self.vacancies.append(
            {"title": vacancy.title, "url": vacancy.url, "salary": vacancy.salary, "description": vacancy.description})
        self.save_vacancies()

    def delete_vacancy(self, vacancy):
        self.vacancies = [v for v in self.vacancies if not (v["title"] == vacancy.title and v["url"] == vacancy.url)]
        self.save_vacancies()

    def get_vacancies_by_salary(self, salary_range):
        min_salary, max_salary = map(int, salary_range.split("-"))
        filtered_vacancies = [v for v in self.vacancies if "руб." in v["salary"]]
        matching_vacancies = [v for v in filtered_vacancies if
                              min_salary <= int(v["salary"].split("-")[0].replace(" ", "")) <= max_salary]
        return matching_vacancies

    def save_vacancies(self):
        with open(self.file_path, "w") as f:
            json.dump(self.vacancies, f)
