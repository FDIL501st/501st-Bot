import nextcord
from nextcord.ext import commands, application_checks
from dotenv import load_dotenv
import os
import psutil
from bot.shared.errors import *

# set intents, match ones set on discord

# may not need these lines
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

# load environment variables
load_dotenv(".env")

DEV: bool = bool(os.environ.get("DEV", "False"))
TOKEN: str = os.environ.get("TOKEN", "")
if TOKEN == "": 
    print("TOKEN needs to be passed in ")
SINGLE_SERVER: bool = bool(os.environ.get("SINGLE_SERVER", "False"))
# SERVER_ID, used to quickly get club server set up with slash commands
SERVER_ID: int = int(os.environ.get("GUILD_ID", 0))

if SINGLE_SERVER and SERVER_ID != 0:
    # set for slash commands default server to register in the testing
    bot: commands.Bot = commands.Bot(command_prefix='./', intents=intents, default_guild_ids=[SERVER_ID])
else:
    # set slash commands for all servers (this takes some hours to register)
    bot: commands.Bot = commands.Bot(command_prefix='./', intents=intents)


# print to terminal when Bot is ready
@bot.event
async def on_ready():
    print("Bot is ready.")

COGS_DIR = "bot.cogs"

loaded_cogs: list[str] = []

# load new cogs
loaded = bot.load_extensions(
    names=[
        ".basic",
        ".calculator",
    ],
    package=COGS_DIR
)
loaded_cogs.extend(loaded)

# load the legacy cogs
loaded = bot.load_extensions_from_module(source_module=COGS_DIR+".legacy")
loaded_cogs.extend(loaded)

# load cogs from statistics
loaded = bot.load_extensions_from_module(source_module=COGS_DIR+".statistics")
loaded_cogs.extend(loaded)

# load cogs from gpt4all
loaded = bot.load_extensions_from_module(source_module= COGS_DIR+".gpt4all")
loaded_cogs.extend(loaded)

print(loaded_cogs)

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
async def reload(ctx: commands.Context, cog_name: str):
    """Reloads a cog."""
    bot.reload_extension(cog_name)
    await ctx.send(f"{cog_name} reloaded.")


@bot.command()
@commands.is_owner()
async def battery(ctx: commands.Context):
    """Tries to the battery info of the machine running the bot."""
    battery = psutil.sensors_battery()

    # unable to get battery information, can occur depending on the machine running the bot
    if not battery:
        await ctx.send("Battery information not available")
        return
    
    battery_percent = battery.percent
    battery_secsleft = battery.secsleft
    battery_plugged = battery.power_plugged
    
    # get the battery_time_left which is a readable version of battery_secsleft

    if battery_secsleft == psutil.POWER_TIME_UNKNOWN:
        battery_time_left = "Unknown"
    elif battery_secsleft == psutil.POWER_TIME_UNLIMITED:
        battery_time_left = "Unlimited"
    else:
        # convert seconds to hours and minutes
        # hours, mins = secs_to_hours_and_mins(battery_secsleft)
        # battery_time_left = f"{hours}h {mins}m"
        battery_time_left = f"{battery_secsleft}s"

    # have all info, now we display it all
    battery_info: str = f"Battery remaining: {battery_percent}%\nBattery time remaining: {battery_time_left}\nPlugged in: {'Yes' if battery_plugged else 'No'}"
    await ctx.send(battery_info)

def secs_to_hours_and_mins(seconds: int) -> tuple[int, int]:
    """Converts seconds to hours and minutes."""
    hours, remainder_secs = divmod(seconds, 3600)
    mins, _ = divmod(remainder_secs, 60)

    return hours, mins


@load.error
@unload.error
async def cog_errors(ctx: commands.Context, error: nextcord.DiscordException):
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


# slash command version of reload
@bot.slash_command()
@application_checks.is_owner()
async def refresh(interaction: nextcord.Interaction, cog_name: str):
    """
    Reloads a cog.
    Slash command version of ./reload
    """
    bot.reload_extension(cog_name)
    await interaction.send(f"{cog_name} reloaded.")


# command not found error handling
# looking for when command_error event occurs in bot
@bot.event
async def on_command_error(ctx: commands.Context, error: commands.errors.CommandError):
    # commandInvokeErrors should be caught by command error handlers
    if isinstance(error, commands.errors.CommandInvokeError):
        return

    if DEV:
        print("In on_command_error, caught exception of type: {0}".format(type(error)))

    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Command does not exist.")
    elif isinstance(error, commands.errors.NotOwner):
        await ctx.send("You attempted to run an owner only command. You do not own this bot.")
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
