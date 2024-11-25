import requests

from environs import Env
from utils_for_search_vacancies import predict_salary, average_amount, print_vacancies_table


def get_vacancies_data(language: str, secret_key: str):
    url = 'https://api.superjob.ru/2.0/vacancies/'

    headers = {
        'X-Api-App-Id': secret_key,
    }
    params = {
        'town': 'Москва',
        'keyword': f'Программист {language}'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data


def get_vacancies_from_superjob(language: str, secret_key: str):
    data = get_vacancies_data(language, secret_key)

    return data['objects']


def get_all_vacancies_count(language: str, secret_key: str):
    data = get_vacancies_data(language, secret_key)
    return data['total']


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


def main_superjob():
    env = Env()
    env.read_env()
    secret_key = env.str('SECRET_SJ_KEY')

    popular_languages = ['Python', 'JavaScript', 'Java', 'PHP', 'C++', 'Go']
    comparison_vacancies_sj = {}
    for language in popular_languages:
        vacancies = get_vacancies_from_superjob(language, secret_key)
        vacancies_found = get_all_vacancies_count(language, secret_key)
        vacancies_with_amount = get_vacancies_with_amount(vacancies)

        comparison_vacancies_sj[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(vacancies_with_amount),
            'average_salary': average_amount(vacancies_with_amount)
        }
    print_vacancies_table(comparison_vacancies_sj)



