import requests
from itertools import count
from utils_for_search_vacancies import predict_salary, average_amount, print_vacancies_table


def get_all_vacancies_and_count(language: str, secret_key: str):
    vacancies = []
    for page in count(0):

        url = 'https://api.superjob.ru/2.0/vacancies/'

        headers = {
            'X-Api-App-Id': secret_key,
        }
        params = {
            'town': 'Москва',
            'keyword': f'Программист {language}',
            'page': page
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        page_payload = response.json()
        vacancies.extend(page_payload['objects'])
        vacancies_count = page_payload['total']
        if not page_payload['more']:
            break
    return vacancies, vacancies_count


def predict_salary_sj(vacancy):
    salary_from = vacancy.get('payment_from')
    salary_to = vacancy.get('payment_to')
    return predict_salary(salary_from, salary_to)


def get_vacancies_with_amount(vacancies: list):
    amounts = []
    for vacancy in vacancies:
        amount = predict_salary_sj(vacancy)
        if amount:
            amounts.append(amount)

    return amounts


def get_vacancies_sj_for_languages_and_print_table(secret_key):
    popular_languages = ['Python', 'JavaScript', 'Java', 'PHP', 'C++', 'Go']
    comparison_vacancies_sj = {}
    for language in popular_languages:
        vacancies, vacancies_found = get_all_vacancies_and_count(language, secret_key)

        vacancies_with_amount = get_vacancies_with_amount(vacancies)

        comparison_vacancies_sj[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(vacancies_with_amount),
            'average_salary': average_amount(vacancies_with_amount)
        }
    print_vacancies_table(comparison_vacancies_sj)


