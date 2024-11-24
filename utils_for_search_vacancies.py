from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None


def average_amount(amounts: list):
    return int(sum(amounts) / len(amounts))


def print_vacancies_table(vacancy_dict):
    table_data = [
        ["Language", "Vacancies Found", "Vacancies Processed", "Average Salary"]
    ]

    for language, data in vacancy_dict.items():
        table_data.append([language, data["vacancies_found"], data["vacancies_processed"], data["average_salary"]])

    table = AsciiTable(table_data)
    print(table.table)
