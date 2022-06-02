from library.base_controllers import Controller

from conf.configs import DESCRIPTIONS
from library import sql_master
from library.request_maker import get
from library.shortcuts import check_ownership

from .templates import full_character_template
from .parsers import CharacterParser


class CharacterController(Controller):
    def __init__(self, template=full_character_template, parser=CharacterParser()):
        super().__init__(template=template, parser=parser)
        self.db = 'character_owner'


    async def create(self, url, ctx):
        _, server_id = sql_master.get_value(
            'user_relations', ('discord_id', ctx.author.id))
        return await super().create(url, data=ctx.message.content, owner=server_id)
