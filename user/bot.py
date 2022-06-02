from conf.configs import DESCRIPTIONS
from conf.configs import bot

from library.decor import prerun
from library import sql_master

from .controllers import UserController


USER_CONTROLLER = UserController()


@prerun()
@bot.command(name='signup', help=DESCRIPTIONS['signup'])
async def signup(ctx):
    couple = sql_master.get_value('user_relations',('discord_id', ctx.author.id))
    if couple:
        await ctx.send('Отклонено. Аккаунт уже существует.')
    else:
        await ctx.send(
            await USER_CONTROLLER.create(
                r'account/api/',
                ctx
            )
        )


@prerun()
@bot.command(name='deleteme', help=DESCRIPTIONS['deleteme'])
async def deleteme(ctx):
    couple = sql_master.get_value('user_relations',('discord_id', ctx.author.id))
    if not couple:
        await ctx.send('Отклонено. Вы не существуете в системе.')
    else:
        await ctx.send(
            await USER_CONTROLLER.delete(
                r'account/api/',
                ctx
            )
        )
