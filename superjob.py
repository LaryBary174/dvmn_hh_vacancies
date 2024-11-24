import requests

from environs import Env
from utils_for_search_vacancies import predict_salary, average_amount, print_vacancies_table

env = Env()
env.read_env()


def check_vacancies_from_superjob(language: str):
    url = 'https://api.superjob.ru/2.0/vacancies/'

    headers = {
        'X-Api-App-Id': env.str('SECRET_SJ_KEY'),
    }
    params = {

        'town': 'Москва',
        'keyword': f'Программист {language}'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    vacancies = response.json()['objects']

    return vacancies


def predict_salary_sj(vacancy):
    salary_from = vacancy.get('payment_from')
    salary_to = vacancy.get('payment_to')
    return predict_salary(salary_from, salary_to)


def calculating_vacancies_with_amount(vacancies: list):
    amounts = []
    for vacancy in vacancies:
        amount = predict_salary_sj(vacancy)
        if amount:
            amounts.append(amount)

    return amounts


Petya_dreams_of_becoming_a_programmer_like_me_sj = {
    'Python': {
        "vacancies_found": len(check_vacancies_from_superjob('Python')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies_from_superjob('Python'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies_from_superjob('Python'))),
    },
    'JavaScript': {
        "vacancies_found": len(check_vacancies_from_superjob('JavaScript')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies_from_superjob('JavaScript'))),
        "average_salary": average_amount(
            calculating_vacancies_with_amount(check_vacancies_from_superjob('JavaScript'))),
    },
    'Java': {
        "vacancies_found": len(check_vacancies_from_superjob('Java')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies_from_superjob('Java'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies_from_superjob('Java'))),
    },
    'PHP': {
        "vacancies_found": len(check_vacancies_from_superjob('PHP')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies_from_superjob('PHP'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies_from_superjob('PHP'))),
    },
    'Ruby': {
        "vacancies_found": len(check_vacancies_from_superjob('Ruby')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies_from_superjob('Ruby'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies_from_superjob('Ruby'))),
    },
    'C++': {
        "vacancies_found": len(check_vacancies_from_superjob('C++')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies_from_superjob('C++'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies_from_superjob('C++'))),
    },
    'Go': {
        "vacancies_found": len(check_vacancies_from_superjob('Go')),
        "vacancies_processed": len(calculating_vacancies_with_amount(check_vacancies_from_superjob('Go'))),
        "average_salary": average_amount(calculating_vacancies_with_amount(check_vacancies_from_superjob('Go'))),
    },
}

if __name__ == '__main__':
    print_vacancies_table(Petya_dreams_of_becoming_a_programmer_like_me_sj)
