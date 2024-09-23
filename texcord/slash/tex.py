import discord
from discord import ApplicationContext, SlashCommand, SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command


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
        await context.respond(
            content=f"```tex\n{tex}\n```",
            ephemeral=True,
        )

def setup(client) -> None:
    client.add_cog(Tex(client))
