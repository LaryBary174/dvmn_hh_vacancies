import requests
from itertools import count

from utils_for_search_vacancies import predict_salary, average_amount, print_vacancies_table


def predict_rub_salary(vacancy):
    salary = vacancy.get('salary')

    if not salary or salary.get('currency') != 'RUR':
        return None
    salary_from = salary.get('from')
    salary_to = salary.get('to')
    return predict_salary(salary_from, salary_to)


def get_all_vacancies_from_hh(language: str):
    vacancies = []
    moscow_area_id = '1'
    programmer_role_id = '96'
    search_period_in_days = '30'
    vacancies_per_page = '100'
    for page in count(0):
        url = 'https://api.hh.ru/vacancies'
        params = {
            'professional_role': programmer_role_id,
            'area': moscow_area_id,
            'period': search_period_in_days,
            'page': page,
            'per_page': vacancies_per_page,
            'text': f'Программист {language}',

        }
        page_response = requests.get(url=url, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        vacancies.extend(page_payload.get('items'))
        count_of_vacancies = page_payload['found']
        if page >= page_payload.get('pages') - 1:
            break
    return vacancies, count_of_vacancies



def get_vacancies_with_amount(vacancies: list):
    amounts = []
    for vacancy in vacancies:
        amount = predict_rub_salary(vacancy)
        if amount:
            amounts.append(amount)

    return amounts


def get_vacancies_hh_for_languages_and_print_table():
    popular_languages = ['Python', 'JavaScript', 'Java', 'PHP', 'C++', 'Go']
    comparison_vacancies_hh = {}
    for language in popular_languages:
        vacancies, vacancies_found = get_all_vacancies_from_hh(language)
        vacancies_with_amount = get_vacancies_with_amount(vacancies)

        comparison_vacancies_hh[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(vacancies_with_amount),
            'average_salary': average_amount(vacancies_with_amount)
        }
    print_vacancies_table(comparison_vacancies_hh)

