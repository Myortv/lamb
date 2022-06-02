def short_character_template(data):
    output = ""
    for i in data:
        output += f'''```\n
• ID: {i["id"]}
• Имя: {i["name"]}
• Внешние признаки: {i["signs"]}```'''
    return output


def full_character_template(data):
    output = ""
    if type(data) == dict:
        data = [data,]
    for i in data:
        output += f'''```
• ID: {i["id"]}\n
• Имя: {i["name"]}\n
• Раса: {i["race"]}\n
• Age: {i["age"]}\n
• Внешние признаки: {i["signs"]}\n
• Остальное •\n
{i["content"]}```'''
    return output
