# file with checks that can be used for commands
import nextcord
from nextcord.ext import commands, application_checks
from .constants import CLUB_SERVER_ID


def is_in_club_server():
    """Command check to see if the command was called from the club server"""
    async def predicate(ctx: commands.Context):
        return ctx.guild.id == CLUB_SERVER_ID

    return commands.check(predicate)

