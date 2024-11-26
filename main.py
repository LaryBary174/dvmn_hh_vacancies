from head_hunter import get_vacancies_hh_for_languages_and_print_table
from superjob import get_vacancies_sj_for_languages_and_print_table
from environs import Env



if __name__ == '__main__':
    env = Env()
    env.read_env()
    secret_key = env.str('SECRET_SJ_KEY')
    get_vacancies_hh_for_languages_and_print_table()
    get_vacancies_sj_for_languages_and_print_table(secret_key)