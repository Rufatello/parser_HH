import psycopg2
import requests

def get_load_company_url(companies):
    url_company = []
    full_vakancy = []
    for i in companies:
        response = requests.get(f'https://api.hh.ru/employers/{i}',
                                params={'per_page': 1, 'only_with_vacancies': True}).json()
        url_company.append(response['vacancies_url'])

    for vakancy in url_company:
        data = requests.get(f'{vakancy}', params={'per_page': 1, 'only_with_salary':True}).json()
    full_vakancy.append({'name_vakancy': data['items'][0]['name'],
                         'name_company': data['items'][0]['department']['name'],
                         'url_vakancy': data['items'][0]['alternate_url'],
                         'solary_ot': data['items'][0]['salary']['from'],
                         'solary_do': data['items'][0]['salary']['to']
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



