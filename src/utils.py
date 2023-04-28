from src.hh_sj_classes import HeadHunterAPI, SuperJobAPI, Vacancy, JSONSaver


def user_interaction():
    hh_api = HeadHunterAPI()
    sj_api = SuperJobAPI()

    search_query = input("Введите поисковое слово: ")
    num_vacancies = int(input("Введите количество вакансий: "))
    sort_by = input("Введите 'asc' для сортировки по возрастанию зарплаты, 'desc' для сортировки по убыванию: ")

    hh_vacancies = hh_api.get_vacancies(search_query)
    hh_vacancies = [Vacancy(v["name"], v["alternate_url"], v.get("salary", ""), v.get("description", "")) for v in
                    hh_vacancies]

    sj_vacancies = sj_api.get_vacancies(search_query)
    sj_vacancies = [Vacancy(v["profession"], v.get("href", ""),
                            str(v.get("payment_from", "")) + "-" + str(v.get("payment_to", "")) + " руб./мес.",
                            v["description"], "SuperJob") for v in sj_api.get_vacancies(search_query) if "href" in v]

    if sort_by == "asc":
        vacancies = sorted(vacancies, key=lambda x: int(getattr(x, "salary", "").split("-")[0].replace(" ", ""))
        if getattr(x, "salary", None) and "руб." in getattr(x, "salary", "") else float('inf'))
    elif sort_by == "desc":
        vacancies = sorted(vacancies, key=lambda x: int(getattr(x, "salary", "").split("-")[0].replace(" ", ""))
        if getattr(x, "salary", None) and "руб." in getattr(x, "salary", "") else float('-inf'), reverse=True)

    for v in vacancies[:num_vacancies]:
        print(f"{v.title}\n{v.url}\n{v.salary}\n{v.description}\n")
