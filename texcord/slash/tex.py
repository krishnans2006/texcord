import io

import discord
from discord import ApplicationContext, SlashCommand, SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command
import sympy

import matplotlib.pyplot as plt


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

        with io.BytesIO() as image:
            try:
                sympy.preview(
                    rf"${tex}$", viewer="BytesIO", outputbuffer=image, dvioptions=["-D", "500"]
                )
            except RuntimeError as e:
                error_string = str(e)

                line_1, output = error_string.split("\n", 1)

                error_section = output.replace('"', "")[1:].replace("\\n", "\n")

                with io.BytesIO(error_section.encode("utf-8")) as error_file:
                    discord_file = discord.File(fp=error_file, filename="error.txt")
                    await context.respond(
                        content=f"An error occurred while rendering the LaTeX code!",
                        ephemeral=True,
                        file=discord_file,
                    )
                    return
            image.seek(0)
            discord_file = discord.File(fp=image, filename="latex.png")

        await context.respond(
            content="",
            ephemeral=True,
            file=discord_file,
        )


def setup(client) -> None:
    client.add_cog(Tex(client))
