import sqlite3

def create_sql(name_bn):
    # Создание соединения с базой данных
    connection = sqlite3.connect(name_bn)
    cursor = connection.cursor()

    # Создание таблицы, если она не существует
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS vacancy (
        id INTEGER PRIMARY KEY,
        vacancy VARCHAR(25) NOT NULL
    )
    ''')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS skill(
        id INTEGER PRIMARY KEY,
        skill VARCHAR(15) NOT NULL
    )
    ''')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS town(
        id INTEGER PRIMARY KEY,
        town VARCHAR(15) UNIQUE NOT NULL
    )
    ''')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS requests(
        id_req INTEGER PRIMARY KEY,
        town_id INTEGER,
        vacancy_id INTEGER,
        skill_id INTEGER,
        count INTEGER,
        FOREIGN KEY (vacancy_id) REFERENCES vacancy(id),
        FOREIGN KEY (town_id) REFERENCES town(id),
        FOREIGN KEY (skill_id) REFERENCES skill(id))
    ''')

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()

def insert_to_bd(name_bn, name, value):

    # Создание соединения с базой данных
    connection = sqlite3.connect(name_bn)
    cursor = connection.cursor()

    # Проверим, есть ли в наличии
    res = select_from_table(name_bn, name)
    res = [i for _, i in res]
    if value not in res:

        query = f'INSERT INTO {name} ({name}) VALUES (?)'

        cursor.execute(query, (value,))
        print(f'Добавлено - {value}')

        # Сохранение изменений
        connection.commit()

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()

def insert_to_requests(name_bn, value):
    # Создание соединения с базой данных
    connection = sqlite3.connect(name_bn)
    cursor = connection.cursor()
    town = select_id(name_bn,'town', 'town',  value[0])
    vacancy = select_id(name_bn,'vacancy', 'vacancy', value[1])
    skill = select_id(name_bn,'skill', 'skill', value[2])

    delete_request(path_bd, town, vacancy)
    query = f'INSERT INTO requests (town_id, vacancy_id, skill_id, count) VALUES (?, ?, ?, ?)'

    cursor.execute(query, (town, vacancy, skill, value[3]))

    # Сохранение изменений
    connection.commit()

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()


def select_from_table(name_bn, name):
    connection = sqlite3.connect(name_bn)
    cursor = connection.cursor()

    # Извлечение всех данных из таблицы name
    cursor.execute(f'SELECT * FROM {name}')
    res =  cursor.fetchall()

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()
    return res

def select_id(name_bn, table_name, name,  value):
    connection = sqlite3.connect(name_bn)
    cursor = connection.cursor()
    # Извлечение всех данных из таблицы name
    cursor.execute(f'SELECT id FROM {table_name} WHERE {name} = ?', (value,))
    res =  cursor.fetchone()[0]

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()
    return res

def delete_request(name_bn, town, vacancy):
    connection = sqlite3.connect(name_bn)
    cursor = connection.cursor()

    cursor.execute('''
    DELETE FROM requests
    WHERE town_id = ? AND vacancy_id =  ?
    ''', (town, vacancy))

    # Сохранение изменений
    connection.commit()

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()



if __name__ == '__main__':
    path_bd = 'bd_sql'
    create_sql('bd_sql')
    insert_to_bd(path_bd, 'skill', 'Программирование')
    result = select_from_table(path_bd, 'town')
    for r in result:
        print(r)

    result = select_from_table(path_bd, 'skill')
    for r in result:
        print(r)

    result = select_from_table(path_bd, 'vacancy')
    for r in result:
        print(r)

    insert_to_requests(path_bd, ('Москва', 'Аналитик', 'Работа с клиентами', 10))
    # insert_to_requests(path_bd, ('Perm', 'Менеджер', 'Работа с клиентами', 8))
    delete_request(path_bd, 1, 1)

    result = select_from_table(path_bd, 'requests')
    for r in result:
        print(r)

    insert_to_bd(path_bd, 'town', 'Москва')