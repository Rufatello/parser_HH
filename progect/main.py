from utils import get_load_company_url, create_database, save_data_to_database
from config import config
from DB_manager import DBManager
companies = [1740, 2180, 2748, 78638, 3148, 3529, 749819, 6041, 2227671, 740]
# companies = [1740]
def main():

    params = config()
    data, url_company = get_load_company_url(companies)
    create_database('coursework', params)
    save_data_to_database(data, url_company, 'coursework', params)
    db_manager = DBManager('coursework')
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())
    print(db_manager.get_vacancies_with_keyword())
    print(db_manager.get_companies_and_vacancies_count())

if __name__=='__main__':
    main()