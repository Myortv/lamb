from random import choice

from library.request_maker import get, post, patch, delete
from library.shortcuts import check_ownership
from conf.configs import DESCRIPTIONS
from library.sql_master import make_cash


class BaseController:
    def __init__(self, template=None, parser=None):
        self.template = template
        self.parser = parser
        self.search_good_answers = DESCRIPTIONS['search_good_answers']
        self.search_bad_answers = DESCRIPTIONS['search_bad_answers']
        self.post_good_answers = DESCRIPTIONS['post_good_answers']
        self.post_bad_answers = DESCRIPTIONS['post_bad_answers']
        self.update_good_anwers = DESCRIPTIONS['update_good_answers']
        self.update_bad_anwers = DESCRIPTIONS['update_bad_answers']
        self.delete_good_answers = DESCRIPTIONS['delete_good_answers']
        self.delete_bad_answers = DESCRIPTIONS['delete_bad_answers']
        self.not_exists_answers = DESCRIPTIONS['not_exists_answers']
        self.error_answers = DESCRIPTIONS['error_answers']


    async def search(self, url, template = None): # -> text to send
        if not template:
            template = self.template
        response, content = await get(url)
        status = response.status
        if content and status == 200:
            return (
            f'{choice(self.search_good_answers)}\n{template(content)}')
        elif not content and status == 200:
            return (
                f'{choice(self.search_bad_answers)}'
                '```\nstatus code: 404```')
        else:
            return (
                f'{choice(self.search_bad_answers)}'
                f'```\nstatus code: {status}```')


    async def create(self, url, data, **kwargs): # -> text to send
        response, _ = await post(url, self.parser.creation(data, **kwargs))
        if response.ok:
            await make_cash()
            return (f'{choice(self.post_good_answers)}')
        else:
            return (
                f'{choice(self.post_bad_answers)}'
                f'```\nstatus code: {response.status}```')


    async def update(self, url, data):
        # мне будут давать ссылку типа api/char/<id>/
        # и я буду апдейтить его просто направляя данные и
        # выводить пререндеренный ответ
        # data - message content
        response, content = await patch(url, self.parser.updation(data))
        if response.ok:
            return (
                f'{choice(self.update_good_anwers)}\nВот что получилось:'
                f'\n{self.template(content)}' )
        else:
            return(
                f'{choice(self.update_bad_anwers)}\n'
                f'```status code: {response.status}```'
                f'```\n{content} ```')


    async def delete(self, url):
        response, _ = await delete(url)
        if response.ok:
            await make_cash()
            return choice(self.delete_good_answers)
        else:
            return (
                f'{choice(self.delete_bad_answers)}\n'
                f'```\nstatus code: {response.status}```')


class Controller(BaseController):
    def __init__(self, template=None, parser=None):
        super().__init__(template=template, parser=parser)
        self.db = 'character_owner'
        self.not_owner_answers = DESCRIPTIONS['not_owner_answers']


    async def update(self, url, data, is_superuser=False, is_owner=False):

        if is_owner or is_superuser:
            return await super().update(url, data)
        else:
            return choice(self.not_owner_answers)


    async def delete(self, url, is_superuser=False, is_owner=False):
        if  is_owner or is_superuser:
            return await super().delete(url)
        else:
            return choice(self.not_owner_answers)


class IncrementationMixin:
    def __init__(self):
        self.search_bad_answers = ''
        self.update_good_answers = ''


    async def incrementate(self, url, gain, incrementate_field):
        response, content = await get(url)

        if not response.ok:
            return f'{self.search_bad_answers}\n```\n{response}```\n'

        final = sum((content[incrementate_field], gain))
        data = {incrementate_field : final}

        response, content = await patch(url, data)

        if response.ok:
            return (f'```{content[incrementate_field]}```' )
        else:
            return (
                f'{choice(self.update_bad_anwers)}\n'
                f'```{content}```'
            )


class UpdateLineMixin:

    async def updateline(self, url, field, data):
        response, content = await patch(url, {field : data})
        if response.ok:
            return f"```{content[field]}```"
        else:
            return f"error```\nstatus code:{response.status}```"
