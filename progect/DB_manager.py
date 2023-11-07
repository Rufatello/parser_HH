import psycopg2
from config import config

class DBManager:
    def __init__(self, database_name, params=config()):
        self.database_name = database_name
        self.params = params
        self.a = 'Специалист по работе с курьерами (удаленно) со знанием узбекского языка'

    def get_all_vacancies(self):
        """медот для вывода всех строк из обоих таблиц"""
        conn = psycopg2.connect(database=self.database_name, **self.params)
        with conn.cursor() as cur:

            cur.execute('SELECT* FROM companies INNER JOIN job USING(company_id)')
            data = cur.fetchall()
            conn.close()
        return data
    def get_avg_salary(self):
        """медот для нахождения средней зп"""
        conn = psycopg2.connect(database=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute('SELECT AVG(solary_do) as solary_avg_do FROM job')
            data_1 = cur.fetchall()
            conn.close()
        return data_1
    def get_vacancies_with_higher_salary(self):
        """вывод всех вакансий где зп больше средней"""
        conn = psycopg2.connect(database=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM job WHERE solary_do > (SELECT AVG(solary_do) FROM job)')
            data_2 = cur.fetchall()
            conn.close()
        return data_2

    def get_vacancies_with_keyword(self):
        '''вывод вакансий по названию'''
        """в качестве аргумента задана обычная переменная c вакансией 'Диспетчер чатов, удаленно'. но можно сделать и инпут"""
        conn = psycopg2.connect(database=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM job WHERE job_title = '{self.a}'")
            data_3 = cur.fetchall()
            conn.close()
        return data_3

    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(database=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f'SELECT companies.name_company, COUNT(job.job_id) FROM companies LEFT JOIN job ON companies.company_id = job.company_id GROUP BY companies.name_company')
            data_4 = cur.fetchall()
            conn.close()
        return data_4
