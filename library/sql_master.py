import sqlite3 as sqlite

from conf import configs
from conf.configs import CASH_DB
from .request_maker import get


def create_user_table():
    # discord_id -> server_id
    name = 'user_relations'

    cursor = CASH_DB.cursor()
    cursor.execute(f"CREATE TABLE if not exists {name} (discord_id integer, id integer) ")
    return name


def create_notes_table():
    # title server_id  character owner
    name = 'notes'

    cursor = CASH_DB.cursor()
    cursor.execute(f"CREATE TABLE if not exists {name} (title text, id integer, character integer, owner integer, is_public integer)")
    return name


def create_status_table():
    # status_id, character_id
    name = 'status'

    cursor = CASH_DB.cursor()
    cursor.execute(f"CREATE TABLE if not exists {name} (character integer, id integer)")
    return name


def create_charactrer_owner_table():
    name = 'character_owner'

    cursor = CASH_DB.cursor()
    cursor.execute(f"CREATE TABLE if not exists {name} (id integer, owner integer)")
    return name


def _print_cash_error(response):
    if not response.ok:
        print('\n\tCASH NOT LOADED\nstatus code:', response.status, '\nurl:',
            response.url)
        raise UserWarning()


def _insert_values_in_table(table, data):
    cursor = CASH_DB.cursor()
    placeholders = '?'+', ?'*(len(data[0])-1)
    cursor.executemany(f"INSERT INTO {table} VALUES ({placeholders})", data)
    CASH_DB.commit()


def _drop_tables():
    cursor = CASH_DB.cursor()
    cursor.execute('DROP table if exists user_relations')
    cursor.execute('DROP table if exists character_owner')
    cursor.execute('DROP table if exists notes')
    cursor.execute('DROP table if exists staus')

    CASH_DB.commit()


async def make_cash():
    print('\t--------------\n\tmake cash  ', end='')

    relations = []
    _drop_tables()

    response, content = await get('account/api/')
    _print_cash_error(response)

    for i in content:
        relations.append((i['discord_id'], i['id']))
    table_name = create_user_table()
    _insert_values_in_table(table_name, relations)

    relations.clear()

    response, content = await get('char/api/')
    _print_cash_error(response)

    for i in content:
        relations.append((i['id'], i['owner']))
    table_name = create_charactrer_owner_table()
    _insert_values_in_table(table_name, relations)

    relations.clear()

    response, content = await get('notes/api/')
    _print_cash_error(response)

    for i in content:
        relations.append((i['title'], i['id'], i['character'], i['owner'], i['is_public']))
    table_name = create_notes_table()
    _insert_values_in_table(table_name, relations)

    relations.clear()

    response, content = await get('status/api/')
    _print_cash_error(response)

    for i in content:
        relations.append((i['character'], i['id']))
    table_name = create_status_table()
    _insert_values_in_table(table_name, relations)

    print('[O]\n')
    return 1


def get_value(table_name, search):
    # search = ('field name', 'field content')
    # table_name - str
    cursor = CASH_DB.cursor()
    cursor.execute(f'SELECT * FROM {table_name} WHERE {search[0]}=?', (search[1], ))
    return cursor.fetchone()
