from configparser import ConfigParser

"""в filename передается название файла, section передаем секцию, для парсинга"""
def config(filename='/home/geydarovr/Загрузки/db_course_work/progect/database.ini', section='postgresql'):
    """обявляем экземпляр класса ConfigParser"""
    parser = ConfigParser()
    # читаем файл с помощью: read
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db