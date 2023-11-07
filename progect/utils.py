import psycopg2
import requests

def get_load_company_url(companies):
    url_company = {}
    list_company = []
    count = 0
    for i in companies:
        count += 1
        response = requests.get(f'https://api.hh.ru/employers/{i}',
                                params={'per_page': 1, 'only_with_vacancies': True}).json()
        list_company.append(response)
        for item in list_company:
            url_company[count] = item['vacancies_url']
    return list_company, url_company



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


def save_data_to_database(data, url_company, database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        count_1 = 0
        for i in data:
            count_1 += 1
            cur.execute('INSERT INTO companies VALUES (%s,%s) ON CONFLICT (company_id) DO NOTHING',
                        (count_1, i['name']))

        count = 0
        for i, url in url_company.items():
            data = requests.get(f'{url}', params={'per_page': 10, 'only_with_salary': True}).json()
            for item in data.get('items', []):
                count += 1
                cur.execute('INSERT INTO job VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (job_id) DO NOTHING',
                            (count, i, item.get('name'),
                             item['salary']['from'] if item.get('salary') else None,
                             item['salary']['to'] if item.get('salary') else None,
                             item.get('alternate_url')))

    conn.commit()
    conn.close()

