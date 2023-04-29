from src.hh_sj_classes import HeadHunterAPI, SuperJobAPI, Vacancy, JSONSaver


def user_interaction():
    print("Добро пожаловать! Выберите платформу для поиска вакансий:")
    print("1. HeadHunter")
    print("2. SuperJob")
    platform_choice = input("Введите номер платформы: ")

    if platform_choice == "1":
        platform = {"hh": HeadHunterAPI()}
    elif platform_choice == "2":
        platform = {"sj": SuperJobAPI()}
    else:
        print("Выбрана некорректная платформа.")
        return

    search_query = input("Введите запрос для поиска вакансий: ")
    num_vacancies = input("Введите количество вакансий для вывода в топ: ")
    try:
        num_vacancies = int(num_vacancies)
    except ValueError:
        print("Некорректное значение количества вакансий.")
        return

    keywords = input("Введите ключевые слова для фильтрации вакансий (если нужно): ")
    if keywords.strip():
        keywords = keywords.split(",")
    else:
        keywords = None

    for platform_name, platform_instance in platform.items():
        print(f"\nРезультаты поиска на {platform_name}:")
        vacancies = platform_instance.get_vacancies(search_query)
        if keywords:
            vacancies = [vacancy for vacancy in vacancies if
                         all(keyword.lower() in vacancy.description.lower() for keyword in keywords)]
        vacancies = sorted(vacancies, key=lambda v: v.salary, reverse=True)[:num_vacancies]
        for vacancy in vacancies:
            print(f"Название вакансии: {vacancy.title}")
            print(f"Зарплата: {vacancy.salary}")
            print(f"Ссылка на вакансию: {vacancy.url}")
            print(f"Описание: {vacancy.description}")
            print("--------------------")
