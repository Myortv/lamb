from conf.configs import DESCRIPTIONS
from library.sql_master import make_cash, get_value
from library.request_maker import post

from library.base_controllers import BaseController
from .parsers import UserParser


class UserController(BaseController):
    def __init__(self):
        super().__init__(parser=UserParser)


    async def create(self, url, ctx):
        answer = await super().create(url, ctx)
        await make_cash()
        return answer


    async def delete(self, url, ctx):
        _, server_id = get_value('user_relations', ('discord_id', ctx.author.id))
        answer = await super().delete(f'{url}{server_id}/')
        await make_cash()
        return answer
