from tkinter.font import names

import requests
from itertools import count

from utils_for_search_vacancies import predict_salary, average_amount, print_vacancies_table


def predict_rub_salary(vacancy):
    salary_info = vacancy.get('salary')

    if not salary_info or salary_info.get('currency') != 'RUR':
        return None
    salary_from = salary_info.get('from')
    salary_to = salary_info.get('to')
    return predict_salary(salary_from, salary_to)


def check_vacancies(language: str):
    vacancies = []
    for page in count(0):
        url = 'https://api.hh.ru/vacancies'
        params = {
            'professional_role': '96',
            'area': '1',
            'period': '30',
            'page': page,
            'per_page': '100',
            'text': f'Программист {language}',

        }
        page_response = requests.get(url=url, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        vacancies.extend(page_payload.get('items'))
        if page >= page_payload.get('pages') - 1:
            break
    return vacancies


def calculating_vacancies_with_amount(vacancies: list):
    amounts = []
    for vacancy in vacancies:
        amount = predict_rub_salary(vacancy)
        if amount:
            amounts.append(amount)

    return amounts


Petya_dreams_of_becoming_a_programmer_like_me_hh = {
    'Python': {
        "vacancies_found": len(check_vacancies('Python')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies('Python'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies('Python'))),
    },
    'JavaScript': {
        "vacancies_found": len(check_vacancies('JavaScript')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies('JavaScript'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies('JavaScript'))),
    },
    'Java': {
        "vacancies_found": len(check_vacancies('Java')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies('Java'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies('Java'))),
    },
    'PHP': {
        "vacancies_found": len(check_vacancies('PHP')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies('PHP'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies('PHP'))),
    },
    'Ruby': {
        "vacancies_found": len(check_vacancies('Ruby')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies('Ruby'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies('Ruby'))),
    },
    'C++': {
        "vacancies_found": len(check_vacancies('C++')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies('C++'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies('C++'))),
    },
    'Go': {
        "vacancies_found": len(check_vacancies('Go')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies('Go'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies('Go'))),
    },
}

if __name__ == '__main__':
    print_vacancies_table(Petya_dreams_of_becoming_a_programmer_like_me_hh)
