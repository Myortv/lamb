from discord.ext import commands

from conf.configs import DESCRIPTIONS, bot, CAN_READ_PRIVAT, CAN_UPDATE_CHAR
from library.decor import prerun
from library.shortcuts import send_over_2000

from .controllers import CharacterController
from .templates import short_character_template


CHARACTER_CONTROLLER = CharacterController()


@prerun()
@bot.command(name='mychars', help=DESCRIPTIONS['mychars'])
async def mychars(ctx):

    answer = await CHARACTER_CONTROLLER.search(
        f'char/api/short/?owner__discord_id={ctx.author.id}',
        template=short_character_template)

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='smychar', help=DESCRIPTIONS['smychar'])
async def smychar(ctx, search_field, post_here: bool = False):

    if not post_here and ctx.guild:
        ctx.channel = await ctx.author.create_dm()

    answer = await CHARACTER_CONTROLLER.search(
        f'char/api/?owner__discord_id={ctx.author.id}&search={search_field}')

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='schar', help=DESCRIPTIONS['schar'])
async def schar(ctx, search_field):

    answer = await CHARACTER_CONTROLLER.search(
        f'char/api/short/?search={search_field}',
        template=short_character_template)

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='Aschar', help=DESCRIPTIONS['Aschar'])
@commands.has_any_role(*CAN_READ_PRIVAT)
async def aschar(ctx, search_field, post_here: bool = False):

    if not post_here and ctx.guild:
        ctx.channel = await ctx.author.create_dm()

    answer = await CHARACTER_CONTROLLER.search(
        f'char/api/?search={search_field}')
    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='createchar', help=DESCRIPTIONS['createchar'])
async def createchar(ctx):

    if ctx.message.content == f'.{ctx.command}':
        await ctx.send(DESCRIPTIONS['character_creation_hellper'])
        return 0
    answer = await CHARACTER_CONTROLLER.create(
        'char/api/',
        ctx)

    await send_over_2000(ctx, answer)



@prerun()
@bot.command(name='uchar', help=DESCRIPTIONS['updatechar'])
async def uchar(ctx, id: int):
    if ctx.message.content == f'.{ctx.command}':
        await ctx.send(DESCRIPTIONS['character_updating_hellper'])
        return 0

    if ctx.guild:
        ctx.channel = await ctx.author.create_dm()

    answer = await CHARACTER_CONTROLLER.update(
        f'char/api/{id}/',
        ctx.message.content,
        ctx,
        id
    )
    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='delete_my_char')
async def delete_my_char(ctx, id: int):
    answer = await CHARACTER_CONTROLLER.delete(f'char/api/{id}/', ctx, id)
    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='Auchar')
@commands.has_any_role(*CAN_UPDATE_CHAR)
async def auchar(ctx, id: int):

    if ctx.guild:
        ctx.channel = await ctx.author.create_dm()

    answer = await CHARACTER_CONTROLLER.update(
        f'char/api/{id}/',
        ctx.message.content,
        ctx,
        id,
        is_super_user=True
    )
    await send_over_2000(ctx, answer)
