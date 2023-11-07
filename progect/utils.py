import psycopg2
import requests

def get_load_company_url(companies):
    url_company = {}
    full_vakancy = []
    for i in companies:
        response = requests.get(f'https://api.hh.ru/employers/{i}',
                                params={'per_page': 1, 'only_with_vacancies': True}).json()
        url_company[response['vacancies_url']] = response['name']

    for vakancy, name_company in url_company.items():
        data = requests.get(f'{vakancy}', params={'per_page': 10, 'only_with_salary': True}).json()
        for item in data['items']:
            full_vakancy.append({'name_vacancy': item['name'],
                                 'url_vacancy': item['alternate_url'],
                                 'salary_from': item['salary']['from'],
                                 'salary_to': item['salary']['to']
                                 })
    return full_vakancy


def create_database(database_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute('CREATE TABLE companies (company_id SERIAL PRIMARY KEY, name_company VARCHAR(300))')

    with conn.cursor() as cur:
        cur.execute('CREATE TABLE job (job_id SERIAL PRIMARY KEY, company_id INT REFERENCES companies(company_id),job_title VARCHAR(300),solary_ot INT,solary_do INT,link_vakansy VARCHAR(500))')

    conn.commit()
    conn.close()



