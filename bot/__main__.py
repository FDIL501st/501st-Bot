import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os

# load enviroment
load_dotenv(".dev.env")

# get TOKEN
TOKEN = os.environ.get("TOKEN")


intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = './', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready.")

# load the legacy cogs
bot.load_extensions(
    names=[
        ".random_facts", 
        ".test"
        ],
        package="cogs.legacy"
    )

@bot.command()
@commands.is_owner()
async def load(ctx, cog_name :str):
    """Putting in a cog"""
    cog_path = "cogs." + cog_name
    bot.load_extension(cog_path) 
    await ctx.send(f"{cog_name} has been loaded.")

@bot.command()
@commands.is_owner()
async def unload(ctx, cog_name :str):
    """Taking out a cog"""
    cog_path = "cogs." + cog_name
    bot.unload_extension(cog_path)
    await ctx.send(f"{cog_name} has been unloaded.")

@bot.command()
@commands.is_owner()
async def refresh(ctx, cog_name : str):
    """Unloads, then loads the cog."""
    load = bot.get_command("load")
    unload = bot .get_command("unload")
    await unload(ctx, cog_name)
    await load(ctx, cog_name)

@load.error
@unload.error
async def cog_errors(ctx, error: commands.errors):
    if isinstance(error, commands.errors.ExtensionAlreadyLoaded):
        await ctx.send("The extension is already loaded.")
    if isinstance(error, commands.errors.ExtensionNotLoaded):
        await ctx.send("The extension is not loaded.")
    if isinstance(error, commands.errors.ExtensionNotFound):
        await ctx.send("Extension not found.")
    else:
        print(error)
    

#About load and unload, name of class doesn't matter, 
# what matters is giving path to file that contains cog
# and the file has a setup function

#Currently can't add cogs from within another cog.

#Also currently been unable to export commands from another file that isn't a cog, 
# aka another main file

bot.run(TOKEN)