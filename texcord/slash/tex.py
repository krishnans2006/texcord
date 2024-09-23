import io

import discord
from discord import ApplicationContext, SlashCommand, SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command
import sympy

import matplotlib.pyplot as plt


def render_latex(formula: str) -> io.BytesIO:
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, "${}$".format(formula), fontsize=12)

    buffer = io.BytesIO()
    fig.savefig(buffer, dpi=300, transparent=True, format="png", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buffer.seek(0)
    return buffer


class Tex(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @slash_command(
        name="tex",
        description="Render LaTeX code",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def tex(self, context: ApplicationContext, tex: Option(str, "Valid LaTeX code")) -> None:
        await context.defer(ephemeral=True)

        image = render_latex(tex)
        discord_file = discord.File(fp=image, filename="latex.png")

        await context.respond(
            content="",
            ephemeral=True,
            file=discord_file,
        )


def setup(client) -> None:
    client.add_cog(Tex(client))
