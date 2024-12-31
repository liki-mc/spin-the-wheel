from discord import app_commands, Interaction, Message
from discord.ext import commands

from bot.bot import Bot


class Example(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")
        
    @commands.Cog.listener("on_message")
    async def example_listener(self, msg: Message):
        """
        https://discordpy.readthedocs.io/en/stable/api.html#event-reference for a list of events
        """

        if msg.author.bot:
            return

        if self.bot.user in msg.mentions:
            await msg.reply("hello")


async def setup(bot: Bot):
    await bot.add_cog(Example(bot))
