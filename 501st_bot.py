import nextcord
from nextcord.ext import commands
import sys
sys.path.append("Helper_Classes")
# Add to paths for importing of classes in cog files

#If there is an error, I won't know as the terminal will just shut down. VS code will show where issue is.
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix = './', Intents=intents)

#For safety reasons, I saved bot token in a txt file which I read from and save to TOKEN
with open("TOKEN.txt", 'r') as f:
    TOKEN = f.readline()

@bot.event
async def on_ready():
    print("Bot is ready.")

#Made a txt file with every cog to load in at start of bot
#Helps by letting me place a cog I'm making in cog folder and run bot at same time
with open("cogs_to_load.txt", 'r') as f:
#If let a variable equal to the file's content, the for loop will go through each char, not line
# As that variable ends up as a string
# However, f is not a string, but rather a TextIOWrapper
    for cog_name in f:
        cog_name = "cogs." + cog_name.removesuffix("\n")
        bot.load_extension(cog_name) 

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