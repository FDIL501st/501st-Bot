import nextcord
from nextcord.ext import commands
from asyncio import Event
from .calculatorUI.calculatorMenu import CalculatorMenu


class Calculator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @nextcord.slash_command()
    async def calculator(self, interaction: nextcord.Interaction):
        """Calculator"""

        click_button_event: Event = Event()

        embed: nextcord.Embed = nextcord.Embed().add_field(name="", value="")
        equation: List[str] = [""]
        calculator_menu: CalculatorMenu = CalculatorMenu(equation=equation, input_embed=embed,
                                                         command_interaction=interaction,
                                                         click_event=click_button_event)

        await interaction.send(embed=embed, view=calculator_menu)

        # need to be able to send some signal here to update, else stop

        while True:
            # reset flag to false, so have to wait for a button press
            # this does nothing for first button press, however when coming back from loop
            # this is needed to cause to wait again
            click_button_event.clear()
            # wait for a button to be clicked
            await click_button_event.wait()

            # if calculator_menu is finished,
            # leave loop as can continue with evaluation
            if calculator_menu.is_finished():
                break

        # got the equation in equation[0], eval and return
        try:
            result: float = eval(equation[0])
            msg: str = "{0} = {1}".format(equation[0], result)
        except SyntaxError:
            msg: str = "Not a valid expression: {0}".format(equation[0])

        await interaction.send(msg)


def setup(bot: commands.Bot):
    bot.add_cog(Calculator(bot))
