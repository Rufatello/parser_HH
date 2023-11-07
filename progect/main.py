import json
from utils import get_load_company_url, create_database, save_data_to_database
from config import config
companies = [1740, 2180, 2748, 78638, 3148, 3529, 749819, 6041, 2227671, 740]
# companies = [1740]
def main():

    params = config()
    data, url_company = get_load_company_url(companies)
    create_database('coursework', params)
    save_data_to_database(data, url_company, 'coursework', params)
    print(url_company)
    with open('/home/geydarovr/Загрузки/db_course_work/1.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

if __name__=='__main__':
    main()