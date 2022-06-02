from conf.configs import BOT_SERVER_ID


class UserParser:
    def creation(ctx):
        data = {
            "username" : ctx.author.name,
            "email" : 'noemail@email.com',
            "discord" : str(ctx.author),
            "discord_id" : ctx.author.id,
            "is_discord_verified" : True,
            "creator__id" : BOT_SERVER_ID}
        return data
