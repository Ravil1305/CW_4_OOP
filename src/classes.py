import json
import os

import requests
from src.abc_class import Engine


class HeadHunterAPI(Engine):
    def __init__(self):
        self.base_url = "https://api.hh.ru/"

    def get_vacancies(self, search_query):
        url = self.base_url + "vacancies"
        params = {"text": search_query}
        response = requests.get(url, params=params)
        if response.ok:
            data = response.json()
            vacancies = []
            for item in data["items"]:
                salary = item.get("salary") or {"from": 0, "to": 0}
                vacancy = Vacancy(
                    item["name"],
                    item["alternate_url"],
                    salary.get("from", 0),
                    salary.get("to", 0),
                    item.get("description", ""),
                )
                vacancies.append(vacancy)
            return vacancies
        else:
            return []


class SuperJobAPI(Engine):
    api_key = os.getenv('SJ_API_KEY')

    def __init__(self):
        self.base_url = "https://api.superjob.ru/2.0/"

    def get_vacancies(self, search_query):
        url = self.base_url + "vacancies/"
        headers = {"X-Api-App-Id": api_key}
        params = {"keyword": search_query}
        response = requests.get(url, headers=headers, params=params)
        if response.ok:
            data = response.json()
            vacancies = []
            for item in data["objects"]:
                vacancy = Vacancy(
                    item["profession"],
                    item["link"],
                    item["payment_to"],
                    item["payment_from"],
                    item["candidat"],
                )
                vacancies.append(vacancy)
            return vacancies
        else:
            return []


class Vacancy:
    def __init__(self, title, url, salary_max, salary_min, description):
        self.title = title
        self.url = url
        self.salary_max = salary_max
        self.salary_min = salary_min
        self.description = description

    @property
    def salary(self):
        if self.salary_min and self.salary_max:
            return f"{self.salary_min}-{self.salary_max} руб."
        elif self.salary_min:
            return f"{self.salary_min} руб."
        elif self.salary_max:
            return f"до {self.salary_max} руб."
        else:
            return "не указана"


class JSONSaver:
    def __init__(self):
        self.file_path = "vacancies.json"
        self.vacancies = []

        try:
            with open(self.file_path) as f:
                data = json.load(f)
                for item in data:
                    vacancy = Vacancy(
                        item["title"],
                        item["url"],
                        item["salary_max"],
                        item["salary_min"],
                        item["description"],
                    )
                    self.vacancies.append(vacancy)
        except FileNotFoundError:
            pass

    def add_vacancy(self, vacancy):
        self.vacancies.append(vacancy)
        self._save_vacancies()

    def delete_vacancy(self, vacancy):
        self.vacancies.remove(vacancy)
        self._save_vacancies()

    def get_vacancies_by_salary(self, salary_range):
        salary_min, salary_max = map(int, salary_range.split("-"))
        filtered_vacancies = [
            v for v in self.vacancies if v.salary_max >= salary_min and v.salary_min <= salary_max
        ]
        return filtered_vacancies

    def _save_vacancies(self):
        data = []
        for vacancy in self.vacancies:
            item = {
                "title": vacancy.title,
                "url": vacancy.url,
                "salary_max": vacancy.salary_max,
                "salary_min": vacancy.salary_min,
                "description": vacancy.description,
            }
            data.append(item)

        with open(self.file_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
