import nextcord
from nextcord.ext import commands, application_checks
from dotenv import load_dotenv
import os
from bot.shared.errors import *

# set intents, match ones set on discord

# may not need these lines
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

# load environment variables
load_dotenv(".env")

DEV: bool = bool(os.environ.get("DEV", "False"))
TOKEN: str = os.environ.get("TOKEN")
SINGLE_SERVER: bool = bool(os.environ.get("SINGLE_SERVER", "False"))

if SINGLE_SERVER:
    # SERVER_ID, used to quickly get club server set up with slash commands
    SERVER_ID: int = int(os.environ.get("GUILD_ID"))
    # set for slash commands default server to register in the testing
    bot: commands.Bot = commands.Bot(command_prefix='./', intents=intents, default_guild_ids=[SERVER_ID])
else:
    # set slash commands for all servers (this takes some hours to register)
    bot: commands.Bot = commands.Bot(command_prefix='./', intents=intents)


# print to terminal when Bot is ready
@bot.event
async def on_ready():
    print("Bot is ready.")


# load the legacy cogs
bot.load_extensions(
    names=[
        ".random_facts",
        ".test"
    ],
    package="bot.cogs.legacy"
)

# load new cogs
bot.load_extensions(
    names=[
        ".basic",
        ".calculator"
    ],
    package="bot.cogs"
)

# load cogs from statistics
bot.load_extensions(
    names=[
        ".pair_different"
    ],
    package="bot.cogs.statistics"
)


@bot.command()
@commands.is_owner()
async def load(ctx: commands.Context, cog_name: str):
    """Putting in a cog"""
    cog_path = "bot.cogs." + cog_name
    bot.load_extension(cog_path)
    await ctx.send(f"{cog_name} has been loaded.")


@bot.command()
@commands.is_owner()
async def unload(ctx: commands.Context, cog_name: str):
    """Taking out a cog"""
    cog_path = "bot.cogs." + cog_name
    bot.unload_extension(cog_path)
    await ctx.send(f"{cog_name} has been unloaded.")


@bot.command()
@commands.is_owner()
async def refresh(ctx: commands.Context, cog_name: str):
    """Unloads, then loads the cog."""
    load_command = bot.get_command("load")
    unload_command = bot.get_command("unload")
    await unload_command(ctx, cog_name)
    await load_command(ctx, cog_name)


@load.error
@unload.error
async def cog_errors(ctx: commands.Context, error: commands.errors):
    if not isinstance(error, commands.CommandInvokeError):
        return

    # this only handles error occurring during command

    e: Exception = error.original

    if DEV:
        print("In cog_errors, caught exception of type {}".format(type(e)))

    if isinstance(e, commands.ExtensionAlreadyLoaded):
        await ctx.send("The extension is already loaded.")
    if isinstance(e, commands.ExtensionNotLoaded):
        await ctx.send("The extension is not loaded.")
    if isinstance(e, commands.ExtensionNotFound):
        await ctx.send("Extension not found.")
    else:
        print(error)


# slash command version of load, unload and refresh
@bot.slash_command()
@application_checks.is_owner()
async def refresh(interaction: nextcord.Interaction, cog_name: str):
    """
    Unloads, then loads a cog.
    Slash command version of ./refresh
    """
    await interaction.send("At this moment, the command does nothing.")


# command not found error handling
# looking for when command_error event occurs in bot
@bot.event
async def on_command_error(ctx: commands.Context, error: commands.errors):
    # commandInvokeErrors should be caught by command error handlers
    if isinstance(error, commands.CommandInvokeError):
        return

    if DEV:
        print("In on_command_error, caught exception of type: {0}".format(type(error)))

    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Command does not exist.")
    else:
        print(error)


# it seems errors from commands are now similar to application commands part of commands.errors.CommandInvokeError
# which has a variable which is the type of error called

# catching any uncaught application command error handling
@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error: nextcord.ApplicationError):
    if DEV:
        print("In on_application_command_error, caught exception of type: {0}".format(type(error)))

    if isinstance(error, application_checks.ApplicationNotOwner):
        await interaction.send("Only the bot owner is allowed to run this command.")
        return

    if not isinstance(error, nextcord.ApplicationInvokeError):
        print(error)
        return

    # Catching exceptions thrown during application command, type ApplicationInvokeError
    e: Exception = error.original
    print(e)

    # deal with all custom defined exceptions by printing back the message
    if isinstance(e, BotException):
        await interaction.send(e.message)
        return

    print(e)


# About load and unload, name of class doesn't matter,
# what matters is giving path to file that contains cog
# and the file has a setup function

# Currently can't add cogs from within another cog.

# Also currently been unable to export commands from another file that isn't a cog,
# aka another main file

bot.run(TOKEN)
