from typing import List
from nextcord import ButtonStyle, Interaction, Embed
import nextcord.ui as ui
from nextcord.ui import View, Button
from asyncio import Event

STYLE_BLURPLE: ButtonStyle = ButtonStyle.blurple


class CalculatorInputButton(Button):
    def __init__(self, label: str, row: int, equation: List[str],
                 input_embed: Embed, command_interaction: Interaction):
        super().__init__(label=label, row=row, style=STYLE_BLURPLE)
        self.input: List[str] = equation
        self.embed: Embed = input_embed
        self.command_interaction: Interaction = command_interaction

    async def callback(self, interaction: Interaction) -> None:
        self.input[0] += self.label

        # just update the embed in application,
        # not actually display the update to discord server
        self.embed.set_field_at(0, name="", value=self.input[0])

        # this is how to update original message, not the edit message
        # edit I think updates the response (which we never wrote yet)
        await self.command_interaction.edit_original_message(embed=self.embed, view=self.view)


class CalculatorMenu(View):
    def __init__(self, equation: List[str], input_embed: Embed, command_interaction: Interaction):
        super().__init__()
        self.command_interaction: Interaction = command_interaction
        self.input: List[str] = equation

        # now add the calculator input buttons, layout similar to online calculators

        # 3 x 3 layout of digits (except for 0 in row by itself at bottom)

        self.add_item(CalculatorInputButton(label="0", row=4, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))

        self.add_item(CalculatorInputButton(label="1", row=3, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="2", row=3, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="3", row=3, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))

        self.add_item(CalculatorInputButton(label="4", row=2, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="5", row=2, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="6", row=2, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))

        self.add_item(CalculatorInputButton(label="7", row=1, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="8", row=1, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="9", row=1, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))

        # decimal point
        self.add_item(CalculatorInputButton(label=".", row=4, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))

        # operations on the right side
        self.add_item(CalculatorInputButton(label="+", row=4, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="-", row=3, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="*", row=2, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))
        self.add_item(CalculatorInputButton(label="/", row=1, input_embed=input_embed,
                                            equation=self.input,
                                            command_interaction=command_interaction))

    # equal sign to stop, calculation done by command
    @ui.button(label="=", style=STYLE_BLURPLE, row=4)
    async def equals(self, button: Button, interaction: Interaction) -> None:
        self.stop()
