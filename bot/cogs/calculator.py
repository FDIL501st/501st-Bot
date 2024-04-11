import nextcord
from nextcord.ext import commands
from .calculatorUI.calculatorMenu import CalculatorMenu


class Calculator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @nextcord.slash_command()
    async def calculator(self, interaction: nextcord.Interaction):
        """Calculator"""
        # current goal is to get the embed to be edited when
        embed: nextcord.Embed = nextcord.Embed().add_field(name="", value="")
        equation: List[str] = [""]
        calculator_menu: CalculatorMenu = CalculatorMenu(equation=equation, input_embed=embed,
                                                         command_interaction=interaction)

        await interaction.send(embed=embed, view=calculator_menu)

        # at the moment, unable to view input being typed until press equal and get error
        await calculator_menu.wait()

        # got the equation in equation[0], eval and return
        try:
            result: float = eval(equation[0])
            msg: str = "{0} = {1}".format(equation[0], result)
        except SyntaxError:
            msg: str = "Not a valid expression: {0}".format(equation[0])

        await interaction.send(msg)


def setup(bot: commands.Bot):
    bot.add_cog(Calculator(bot))
