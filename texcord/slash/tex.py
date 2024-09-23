import io

import discord
from discord import ApplicationContext, Option
from discord.ext import commands
from discord.commands import slash_command
import sympy


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
        await context.defer()

        with io.BytesIO() as image:
            try:
                sympy.preview(
                    rf"${tex}$",
                    viewer="BytesIO",
                    outputbuffer=image,
                    dvioptions=["-D", "400", "-bg", "Transparent", "-fg", "rgb 0.5 0.5 0.5"],
                )
            except RuntimeError as e:
                error_string = str(e)

                line_1, output = error_string.split("\n", 1)

                error_section = output.replace('"', "")[1:].replace("\\n", "\n")

                with io.BytesIO(error_section.encode("utf-8")) as error_file:
                    discord_file = discord.File(fp=error_file, filename="error.txt")
                    await context.respond(
                        content=f"An error occurred while rendering the LaTeX code!",
                        file=discord_file,
                    )
                    return
            image.seek(0)
            discord_file = discord.File(fp=image, filename="latex.png")

        await context.respond(
            content="",
            file=discord_file,
        )


def setup(client) -> None:
    client.add_cog(Tex(client))
