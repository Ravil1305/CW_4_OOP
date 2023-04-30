from src.classes import HeadHunterAPI, SuperJobAPI, JSONSaver, Vacancy


def user_interaction():
    hh_api, sj_api = choice_platform()
    hh_vacancies, sj_vacancies = get_from_platform(hh_api, sj_api)
    filter_word_input = filter_words()
    salary_input = salary_sort()
    get_result(hh_vacancies, sj_vacancies, filter_word_input, salary_input)


def choice_platform():
    while True:
        platform_ = input("Выберите платформу (HeadHunter.ru - 1, Superjob.ru - 2): ")
        if platform_ == '1':
            print('Вы выбрали HeadHunter.ru')
            hh_api = HeadHunterAPI()
            return hh_api, None
        elif platform_ == "2":
            print('Вы выбрали Superjob.ru')
            sj_api = SuperJobAPI()
            return sj_api, None
        else:
            print('Введите 1 или 2, других вариантов к сожалению нет.')
            continue


def get_from_platform(hh_api, sj_api):
    try:
        search_query = input("Введите поисковый запрос: ")
        if hh_api:
            hh_vacancies = hh_api.get_vacancies(search_query)
            return hh_vacancies, None
        elif sj_api:
            sj_vacancies = sj_api.get_vacancies(search_query)
            return sj_vacancies, None
    except:
        print('Некорректный запрос')


def filter_words():
    user_input = input("Введите ключевые слова для фильтрации вакансий в описании: ")
    return user_input


def salary_sort():
    while True:
        salary_min = input("Введите минимальную зарплату для поиска (в рублях): ")
        if not salary_min.strip():
            print("Вы не ввели минимальную зарплату. Минимальное значение будет равно 0")
            return '0'
        try:
            salary_min = int(salary_min)
            return salary_min
        except ValueError:
            print("Некорректное значение. Минимальное значение будет равно 0")
            return '0'


def print_top_vacancies(final):
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    if len(final) > 0:
        for n in range(top_n):
            if final[n]['salary']['from'] == 0:
                salary_text = 'Зарплата не указана'
            else:
                salary_text = f"Зарплата: {final[n]['salary']['from']} руб"

            print(
            f"{final[n]['title']} \n{salary_text} \n Описание вакансии:\n{final[n]['description']} \nСсылка: {final[n]['url']}")
            if n < top_n - 1:
                print("=" * 200)
    else:
        print('Вакансий по вашему запросу нет')


def get_result(hh_vacancies, sj_vacancies, filter_word_input, salary_input):
    json_saver = JSONSaver()
    json_saver.save_in_file(headhunter=hh_vacancies, superjob=sj_vacancies)
    json_saver.search_words(filter_word_input)
    json_saver.get_vacancies_by_salary(salary_input)
    final = json_saver.json_results()
    print_top_vacancies(final)
