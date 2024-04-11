import math
import nextcord
from nextcord.ext import commands
import random
import asyncio
from bot.shared.constants import CLUB_SERVER_ID
UI = nextcord.ui


class ButtonOptions(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None  # initialize label value here

    @UI.button(label="Option 1", style=nextcord.ButtonStyle.blurple)
    async def choice_1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You chose Option 1", ephemeral=True)
        # ephemeral = True makes message only visible to user.
        self.value = 1  # a label to let u know which option was chosen for post button press action
        self.stop()  # stops from registering another click on the button

    @UI.button(label="Option 2", style=nextcord.ButtonStyle.blurple)
    async def choice_2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You chose Option 2", ephemeral=True)
        self.value = 2
        self.stop()

    @UI.button(label="Option 3", style=nextcord.ButtonStyle.blurple)
    async def choice_3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You chose Option 3", ephemeral=True)
        self.value = 3
        self.stop()


class Legacy_Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Lets me use bot. commands within my cog!

        self.guilds: set[int] = set()

    @commands.command()
    async def yourmom(self, ctx):
        """Command requested by deadpool."""

        async def wait_type(ctx, message: str):
            """Helper function to send messages with pauses and typing within this command."""
            async with ctx.channel.typing():
                await asyncio.sleep(5)
            await ctx.send(message)

        if ctx.guild.id in self.guilds:
            await ctx.send("Anti-spam measure initiated.\nOnly 1 use of this command per server at a time.")
            return

        self.guilds.add(ctx.guild.id)

        # Actual command starts here
        await ctx.send("Attempting to initiate bad joke...")
        for x in range(1, 4):
            await wait_type(ctx, f"Attempt {x}...")
            await wait_type(ctx, "Failed.")
        await wait_type(ctx, "Rebooting...")
        await wait_type(ctx, "Reboot Failed.")
        await wait_type(ctx, "Bad joke unable to initialize.")
        await wait_type(ctx, "Termination sequence starting...")
        for x in range(1, 101):
            y = format(50 * math.log10(x), '.2f')
            await wait_type(ctx, f"Termination sequence {y}% done...")
        await wait_type(ctx,
                        "Termination sequence successfully finished.\nThe bad joke has been terminated from the server.")
        self.guilds.remove(ctx.guild.id)

    @commands.command()
    @commands.is_owner()
    async def members(self, ctx: commands.Context):
        """Test command to check if I can access all members in a server."""
        # works now after setting intents.members to True
        for member in ctx.guild.members:
            await ctx.send(str(member))
        async for member in ctx.guild.fetch_members():
            await ctx.send(str(member))

    @commands.command()
    async def ping2(self, ctx):
        """Attempt at calling a different command."""
        command = self.bot.get_command("ping")
        await command.__call__(ctx)
        await ctx.send("Other ping command.")
        # Calling of command was successful

    @commands.command()
    @commands.is_owner()
    async def guess2(self, ctx: commands.Context):
        """Attempt to calling a command from a different cog without using bot.get_command."""
        try:
            game = Economy(self.bot)
            await game.guess(ctx, attempts=5)
        except:
            await ctx.send("This command no longer works")
        # Was able to call a function from a different class

        # await game.guessing_game(context=ctx)
        # Unable to call a command without using bot.get_command
        # The # await above did not work due to argument issues
        # Only accepts context, however doesn't accepts arguments for the command itself

    @commands.command(aliases=["Ping"])
    async def ping(self, ctx):
        """Shows ping/latency of connection bot has, 
        usually equivalent to FDIL's ping as his laptop runs the bot."""
        ping = round(1000 * self.bot.latency)
        if ping < 200:
            await ctx.send(f"Bot ping is : {ping}.")
        else:
            await ctx.send(f"Bot is currently facing some pain. Its ping is : {ping}.")

    @commands.command(aliases=["8ball"])
    # aliases here is other names to call the command in discord other than method/function name
    # Command that gives a random response, no matter if a question is asked or not
    async def __8ball__(self, ctx):
        """An opensource command testing out discord.py/nextcord."""
        # Took out question argument as I wasn't using it

        # responses are something I made up
        responses = ["Placeholder",
                     "Of course, it totally true. Totally not being sarcastic here.",
                     "Nothing ever is 100%, but at least the chance is not 0%",
                     "Hello there, \nGeneral Kenobi",
                     "So I think your chances are pretty high considering you got this message.",
                     "What an unlucky bastard you are, getting this message signifies your lack of luck.",
                     "Placeholder2?",
                     "Placeholder4, where did Placeholder3 go?",
                     "Placeholder PI, now we are using constants?? So decimals are fair game at counting a number of "
                     "thing??? How does that makes sense? Is this where 3 went?",
                     "So then, I'll give you a probability of 0.2.",
                     "As you will realize, this is testing some simple codes about displaying a message. Not actually "
                     "8ball.",
                     "There are a lot of filler messages, so your questions aren't actually being answered."]
        await ctx.send(f"{random.choice(responses)}")

    @commands.command(aliases=["alive", "hello"])
    async def Hello(self, ctx):
        """Simple command to test if the bot is online."""
        await ctx.send("Hello! The bot is indeed online right now.")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild.id == CLUB_SERVER_ID:
                # Any message sent to just you(hidden messages) don't have a guild association
                # aka emphemeral message
                # Errors when bot sends a hidden message as message.guild = None
                if message.content.lower() == "hello":
                    channel = message.guild.get_channel(message.channel.id)
                    # Don't use bot.get_channel(), won't find the channel
                    # message.guild gets guild the message is from, guild has method get_channel()
                    await channel.send("{0} said hello in the club server.".format(message.author.global_name))
        except:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id == 790291109506973696 and payload.channel_id == 866082676582252564:
            # Need to somehow get a guild object, member has guild attribute and payload has member
            # Need to use guild.get_channel as bot.get_channel doesn't work.
            channel = payload.member.guild.get_channel(payload.channel_id)
            # This worked!
            await channel.send(f"{payload.member.name} just reacted in {channel.name} with {payload.emoji.name}.")

    @commands.command()
    async def role(self, ctx):
        """Testing how to give a role"""
        """It seems first use id to get role object back,
        then give the role object"""
        try:
            role_to_give = ctx.guild.get_role(902788782955307008)
            await ctx.author.add_roles(role_to_give)
            await ctx.send("Sending message to tell command worked.")
        except:
            await ctx.send("You used the command in the wrong server.")

    @commands.command()
    async def embed(self, ctx):
        """Testing on making embeds with the bot."""
        emb = nextcord.Embed(title="Red October Winners!")
        emb.add_field(name="Year", value="2020: \n 2021: ", inline=True)
        emb.add_field(name="__Creepypasta Winners__", value="seskran \n N/A", inline=True)
        emb.add_field(name="__Memepasta Winners__", value="N/A \n Gilbert", inline=True)
        await ctx.send(embed=emb)
        # How to send an embed,
        # there is a parameter called embed that you make your embed object equal to

    @commands.command(aliases=["button"])
    async def button_test(self, ctx):
        view = ButtonOptions()
        await ctx.send("This is a test command for buttons, choose an option.", view=view)

        await view.wait()

        if view.value is None:
            print("No response.")

        if view.value == 1:
            com = self.bot.get_command("alive")
            await com.__call__(ctx)

        if view.value == 2:
            com = self.bot.get_command("ping")
            # Line above returns command,
            # lets you take a command name and get a command object out of it
            await com.__call__(ctx)
            # .__call__() is a function of command class that lets you run the command.
            # Be warned that is skips all checks so must give proper arguments

        if view.value == 3:
            await ctx.send("Congrats, you know how to press a button on discord.")


def setup(bot):
    bot.add_cog(Legacy_Test(bot))
