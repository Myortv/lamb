from discord import utils
from discord.ext import commands

from conf.configs import DESCRIPTIONS, CAN_INCREMENTATE_STATUS
from conf.configs import bot

from library.decor import prerun
from library.request_maker import get

from .controllers import LevelingController
from .templates import meditation_ended_template, status_template


LEVELING_CONTROLLER = LevelingController()


@prerun()
@bot.command(name='status')
async def status (ctx, char_id:int):

    answer = await LEVELING_CONTROLLER.search(
        f'status/api/?character__id={char_id}&character__owner__discord_id={ctx.author.id}'
    )
    await ctx.send(answer)



@prerun()
@bot.command(name='Aiblack')
@commands.has_any_role(*CAN_INCREMENTATE_STATUS)
async def aiblack (ctx, char_id:int, gain: int):

    answer = await LEVELING_CONTROLLER.incrementate(
        f'status/api/',
        char_id,
        'black_points',
        gain
    )
    await ctx.send(answer)


@prerun()
@bot.command(name='Aiwhite')
@commands.has_any_role(*CAN_INCREMENTATE_STATUS)
async def aiwhite (ctx, char_id:int, gain: int):

    answer = await LEVELING_CONTROLLER.incrementate(
        f'status/api/',
        char_id,
        'white_points',
        gain
    )
    await ctx.send(answer)


@prerun()
@bot.command(name='statusmeditate')
async def statusmeditate (ctx, char_id:int):
    response, content = await get(f'status/api/change-activity-status/{char_id}/meditation')
    if not response.ok:
        return f'```\n\nerror: {response.status}```'
    active = utils.get(ctx.guild.roles, name="игрок (активный)")
    passive = utils.get(ctx.guild.roles, name="игрок (пассивный)")
    if content['HEAD'] == 'status setted':
        answer = f'Вы начали медитацию!'
        await ctx.author.remove_roles(active)
        await ctx.author.add_roles(passive)

    else:
        answer = meditation_ended_template(content)
        await ctx.author.remove_roles(passive)
        await ctx.author.add_roles(active)
    await ctx.send(answer)



@prerun()
@bot.command(name='statusmerge')
async def statusmerge (ctx, char_id:int):
    response, content = await get(f'status/api/merge-points/{char_id}')
    if not response.ok:
        return f'```\n\nerror: {response.status}```'
    await ctx.send(status_template(content))










# @prerun()
# @bot.command(name='statusmerge')
# async def aiwhite (ctx, char_id:int):
#
#
#     await ctx.send(answer)
