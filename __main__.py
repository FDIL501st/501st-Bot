import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv(".env")

DEV: bool = bool(os.environ.get("DEV"))

if DEV:
    # load the dev environment
    load_dotenv(".dev.env")

TOKEN: str = os.environ.get("TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

# TESTING_GUILD_ID, used to quickly get club server set up with slash commands
# otherwise, takes about an hour to register if don't specify server id
TESTING_GUILD_ID: int = int(os.environ.get("TESTING_GUILD_ID"))

# set for slash commands default server to register in the testing
bot: commands.Bot = commands.Bot(command_prefix='./', intents=intents, default_guild_ids=[TESTING_GUILD_ID])


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
    if isinstance(error, commands.errors.ExtensionAlreadyLoaded):
        await ctx.send("The extension is already loaded.")
    if isinstance(error, commands.errors.ExtensionNotLoaded):
        await ctx.send("The extension is not loaded.")
    if isinstance(error, commands.errors.ExtensionNotFound):
        await ctx.send("Extension not found.")
    else:
        print(error)


# About load and unload, name of class doesn't matter,
# what matters is giving path to file that contains cog
# and the file has a setup function

# Currently can't add cogs from within another cog.

# Also currently been unable to export commands from another file that isn't a cog,
# aka another main file

bot.run(TOKEN)