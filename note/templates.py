from library.sql_master import get_value


def short_note_template(data):
    out = f'```\nPUB {"ID":4} {"SUM":4} {"TYPE":10} NAME```\n'
    for item in data:
        if item['is_public']:
            is_public = '✅'
        else:
            is_public = '❌'
        out += ( '```\n'
            f'{is_public:2} {item["id"]:<4} {item["amount"]:<4} {item["type"]:10} {item["title"]} '
        '```')
    return out


def full_note_template(data):
    out = ""
    if type(data) == dict:
        data = [data,]
    for item in data:
        if item['is_public']:
            is_public = '✅'
        else:
            is_public = '❌'
        out += ( '```\n'
            f'• ID: {item["id"]}\n\n'
            f'• Название: {item["title"]}\n\n'
            f'• Тип: {item["type"]}\n\n'
            f'• Количество: {item["amount"]}\n\n'
            f'• Cодержимое •\n {item["content"]}\n\n'

            f'• Запись публична: {is_public}\n'
        '```')
    return out
