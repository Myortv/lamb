from random import choice

from library.base_controllers import (
                        Controller,
                        IncrementationMixin,
                        UpdateLineMixin
                    )
from library.request_maker import get, patch
from library import sql_master
from library.shortcuts import check_ownership

from conf.configs import DESCRIPTIONS

from .templates import full_note_template
from .parsers import NoteParser


class NotesController(Controller, IncrementationMixin, UpdateLineMixin):
    def __init__(self, template=full_note_template, parser=NoteParser()):
        super().__init__(template=template, parser=parser)
        self.db = 'notes'


    async def create(self, url, ctx):
        _, server_id = sql_master.get_value(
                'user_relations',
                ('discord_id', ctx.author.id)
            )
        return await super().create(
            url, data=ctx.message.content, owner=server_id)


    async def search_trought_char(self, url, ctx, template=None):
        # сначала мы определяем какой тип запроса на сервер нужно будет отправить
        # если указаг id персонажа автора поста, то нужно вывести все заметки
        # если же нет, то только публичные
        _, user_id = sql_master.get_value(
            'user_relations', ('discord_id', ctx.author.id) )
        _, character_owner_id = sql_master.get_value(
            'character_owner', ('id', ctx.args[1]) )

        if character_owner_id == user_id:
            return await self.search(url, template)
        else:
            return await self.search(f'{url}&is_public=true', template)


    async def absolute_search(self, url, ctx, *args, **kwargs):
        is_char_owner = check_note_character_owner(ctx.author.id, ctx.args[1])
        note = sql_master.get_value('notes', ('id', ctx.args[1]))

        if is_char_owner or note['is_public']:
            return await self.search(url, *args, **kwargs)
        return choice(self.not_owner_answers)


    async def update(self, url, ctx, is_super_user=None):
        is_char_owner = check_note_character_owner(ctx.author.id, ctx.args[1])
        return await super().update(
            url, data=ctx.message.content, is_owner=is_char_owner)


    async def create(self, url, ctx):
        _, server_id = sql_master.get_value(
            'user_relations', ('discord_id', ctx.author.id))
        return await super().create(
            url, data=ctx.message.content, owner=server_id)


    async def delete(self, url, ctx):
        is_char_owner = check_note_character_owner(ctx.author.id, ctx.args[1])
        return await super().delete(
            url, is_owner=is_char_owner)


    async def incrementate(self, author, url, note_id, *args, is_superuser=False):
        if check_note_character_owner(author, note_id) or is_superuser:
            return await super().incrementate(f'{url}/{note_id}/', *args)
        return choice(self.not_owner_answers)


    async def updateline(self, url, field, data, ctx):
        if check_note_character_owner(ctx.author.id, ctx.args[1]):
            return await super().updateline(url, field, data)
        return choice(self.not_owner_answers)


def check_note_character_owner(discord_id, note_id):
    note = sql_master.get_value('notes', ('id', note_id))
    if note is None:
        return None
    _, character_owner_id = sql_master.get_value(
            'character_owner',
            ('id', note["character"])
        )
    _, user_id = sql_master.get_value(
            'user_relations',
            ('discord_id', discord_id)
        )
    return user_id == character_owner_id
