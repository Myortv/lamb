from discord.ext import commands
from .shortcuts import is_allowed, debug_stuff


def check_permission(allow_dm=True):
    def predicate(ctx):
        return is_allowed(ctx, allow_dm)
    return commands.check(predicate)

def prerun(allow_dm=True):
    def predicate(ctx):
        debug_stuff(ctx)
        return is_allowed(ctx, allow_dm)
    return commands.check(predicate)
