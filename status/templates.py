def status_template(data):
    if isinstance(data, list):
        data = data[0]
    order = calculate_order(data["level_points"])
    output = ( '```\n'
    f'⚪ {data["white_points"]}\n'
    f'⚫ {data["black_points"]}\n\n'
    f'☯️ Порядок: {order[0]} ☯️\n'
    f'  {data["level_points"]}/{order[1]}\n'

    '```'
    )

    return output

def meditation_ended_template(data):
    output = ( '```\n'
    f'Ты медитировал: {data["interval"]/180} ч \n'
    f'⚪ {data["white_points"]} (+{data["white_points_profit"]})\n'
    f'⚫ {data["black_points"]} (+{data["black_points_profit"]})'
    '```'
    )

    return output



def calculate_order(level_points):
    if level_points >= 0 and level_points < 100:
        return (0, 100)
    if level_points >= 100 and level_points < 1000:
        return (1, 1000)
    if level_points >= 1000 and level_points < 5000:
        return (2, 5000)
    if level_points >= 5000 and level_points < 15000:
        return (3, 15000)
