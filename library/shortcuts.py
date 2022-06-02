from datetime import datetime

from conf import configs
from library import sql_master


dt = datetime.now

def is_allowed(ctx, allow_direct=False):
    if ctx.guild:
        if ctx.guild.name in configs.GUILDS:
            return True
        else:
            return False
    else:
        return allow_direct


def debug_stuff(ctx):
    print(f'{dt().strftime("%d-%m %H:%M:%S")}  {ctx.command}  {ctx.author}/{ctx.guild}')


async def send_over_2000(ctx, text):
    while len(text) > 1996:
        await ctx.send(f'{text[:1996]}```\n')
        text = f'```\n{text[1996:]}'
    await ctx.send(text)


def generate_url(url, kwargs):
    for i in kwargs:
        url += f'&{i}={kwargs[i]}'
    return url


def check_ownership(table, ctx, obj_id):
    _, author_id = sql_master.get_value(
        'user_relations',('discord_id', ctx.author.id))


    real_owner_id = sql_master.get_value(table, ('id', obj_id))['owner']
    return author_id == real_owner_id
