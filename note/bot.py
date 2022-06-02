from discord.ext import commands

from conf.configs import (
                    DESCRIPTIONS,
                    CAN_INCREMENTATE_NOTE,
                    CAN_UPDATE_NOTE,
                    bot
                )

from library.decor import prerun
from library.shortcuts import send_over_2000
from library.sql_master import make_cash

from .controllers import NotesController
from .templates import short_note_template


NOTES_CONTROLLER = NotesController()


@prerun()
@bot.command(name='cnotes', help=DESCRIPTIONS['cnote'])
async def cnotes (ctx, id: int, post_here: bool = False):
    if not post_here and ctx.guild:
        ctx.channel = await ctx.author.create_dm()

    answer = await NOTES_CONTROLLER.search_trought_char(
        f'notes/api/?character__id={id}',
        ctx,
        template=short_note_template
        )

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='note', help=DESCRIPTIONS['note'])
async def note (ctx, id: int , post_here: bool = False):
    if not post_here and ctx.guild:
        ctx.channel = await ctx.author.create_dm()

    answer = await NOTES_CONTROLLER.absolute_search(f'notes/api/{id}/', ctx)

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='createnote', help=DESCRIPTIONS['createnote'])
async def createnote (ctx):

    if ctx.message.content == f'.{ctx.command}':
        await ctx.send(DESCRIPTIONS['note_creation_hellper'])
        return 0

    answer = await NOTES_CONTROLLER.create(
        'notes/api/',
        ctx)

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='unote', help=DESCRIPTIONS['unote'])
async def unote (ctx, id: int):

    if ctx.message.content == f'.{ctx.command}':
        await ctx.send(DESCRIPTIONS['note_updating_hellper'])
        return 0

    answer = await NOTES_CONTROLLER.update(
        f'notes/api/{id}/',
        ctx)
    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='delnote', help=DESCRIPTIONS['delnote'])
async def delnote (ctx, id: int):

    answer = await NOTES_CONTROLLER.delete(
        f'notes/api/{id}/',
        ctx)

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='inote', help=DESCRIPTIONS['inote'])
async def inote (ctx, id: int, gain: int):

    if ctx.message.content == f'.{ctx.command}':
        await ctx.send(DESCRIPTIONS['note_incrementing_hellper'])
        return 0

    answer = await NOTES_CONTROLLER.incrementate(
            ctx.author.id,
            'notes/api',
            id,
            gain,
            'amount'
        )

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='Ainote')
@commands.has_any_role(*CAN_INCREMENTATE_NOTE)
async def ainote (ctx, id:int, gain: int):
    answer = await NOTES_CONTROLLER.incrementate(
            ctx.author.id,
            'notes/api',
            id,
            gain,
            'amount',
            is_superuser = True
        )

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='Aunote')
@commands.has_any_role(*CAN_UPDATE_NOTE)
async def aunote (ctx, id:int, gain: int):
    answer = await NOTES_CONTROLLER.update(
            f'notes/api/{id}/',
            ctx,
            is_superuser = True
        )

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='noteto')
async def noteto (ctx, note_id:int, char_id: int):
    answer = await NOTES_CONTROLLER.updateline(
            f'notes/api/{note_id}/',
            'character',
            char_id,
            ctx
        )

    await send_over_2000(ctx, answer)


@prerun()
@bot.command(name='noteprivat')
async def noteprivat (ctx, note_id:int):
    answer = await NOTES_CONTROLLER.updateline(
            f'notes/api/{note_id}/',
            'is_public',
            False,
            ctx
        )

    await send_over_2000(ctx, answer)



@prerun()
@bot.command(name='notepublic')
async def notepublic (ctx, note_id:int):
    answer = await NOTES_CONTROLLER.updateline(
            f'notes/api/{note_id}/',
            'is_public',
            True,
            ctx
        )

    await send_over_2000(ctx, answer)
