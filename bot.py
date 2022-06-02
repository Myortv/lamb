from discord.ext import tasks
from art import text2art
import aiohttp
import asyncio

from conf import configs
from conf.configs import DESCRIPTIONS
from conf.configs import bot

from library import sql_master
from library.decor import prerun

from user.bot import *
from character.bot import *
from note.bot import *
from status.bot import *
from archive.bot import *


@bot.event
async def on_ready():
    print(text2art(f'{bot.user.name}    started', font='small'))
    _connect_guilds()

    print()
    make_cash.start()

@prerun()
@bot.command(name='check', help=DESCRIPTIONS['check'])
async def check(ctx):
    await ctx.send('checked')


@prerun()
@bot.command(name='make_cash', help=DESCRIPTIONS['check'])
async def make_cash(ctx):
    await sql_master.make_cash()


@tasks.loop(seconds=60)
async def make_cash():
    await sql_master.make_cash()
    return 1


def _connect_guilds():
    for guild in bot.guilds:
        connected = "O" if guild.name in configs.GUILDS else "X"
        print(f'\t[{connected}] {guild.name}:{guild.id}')




if __name__ == "__main__":
    bot.run(configs.TOKEN)
