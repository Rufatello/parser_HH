import json
from utils import get_load_company_url, create_database
from config import config

companies = [1740]
def main():

    params = config()
    data = get_load_company_url(companies)
    create_database('coursework', params)
    print(data)
    with open('/home/geydarovr/Загрузки/db_course_work/1.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

if __name__=='__main__':
    main()