import logging
import os
import sqlite3

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import demjson
import aiohttp

load_dotenv()
TOKEN = os.getenv('DISCORD_LAMB_BOT_TOKEN')
GUILDS = os.getenv('DISCORD_CONNECTED_GUILDS')
DEBUG = os.getenv('DEBUG')
BASE = os.getenv('BASE_URL')
GOLONIEL_AUTH_TOKEN = os.getenv('GOLONIEL_AUTH_TOKEN')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


REQUEST_HEADERS = {
    'Authorization': f'Token {GOLONIEL_AUTH_TOKEN}'
}


CASH_DB = sqlite3.connect(":memory:")
CASH_DB.row_factory = sqlite3.Row

BOT_SERVER_ID = 12


with open(os.path.join(BASE_DIR,'descriptions.json'),'r') as file:
    DESCRIPTIONS = demjson.decode(file.read())


logging.basicConfig(level=logging.INFO)


def get_intents():
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    return intents


class CustomBot(commands.Bot):

    SESSION = None

    async def start(self, *args, **kwargs):
        async with aiohttp.ClientSession(headers=REQUEST_HEADERS) as session:
            CustomBot.SESSION = session
            await super().start(*args, **kwargs)


CAN_READ_PRIVAT = ('admin', 'sacrificed', 'Мастер Области', 'Мастер')
CAN_UPDATE_CHAR = ('admin', 'Мастер')
CAN_INCREMENTATE_NOTE = ('admin', 'Мастер', 'Мастер Области')
CAN_READ_NOTES = ('admin', 'Мастер Области', 'Мастер', )
CAN_UPDATE_NOTE = ('admin', 'Мастер Области')
CAN_INCREMENTATE_STATUS = ('admin', 'Мастер Области')


bot = CustomBot(
    command_prefix='.',
    descriotion=DESCRIPTIONS['botdescription'],
    intents = get_intents(),
)
