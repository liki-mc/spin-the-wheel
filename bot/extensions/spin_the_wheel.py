import discord
from discord.ext import commands
import shlex

from bot.bot import Bot
from .arcade_wheel import choose


class SpinTheWheel(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")

    @commands.command()
    async def spin(self, ctx: commands.Context, *, args: str):
        if "\n" in args:
            options = args.split("\n")
        elif ";" in args:
            options = args.split(";")
        elif "\"" in args:
            options = shlex.split(args)
        elif "," in args:
            options = args.split(",")
        else:
            options = args.split()
        
        k = "\n-"
        await ctx.send(f"Options: \n - {k.join(options)}")
        await ctx.send("Spinning the wheel...")

        choose(options, "data/wheel.mp4")
        await ctx.send(file = discord.File("data/wheel.mp4"))
        
    @commands.Cog.listener("on_message")
    async def example_listener(self, msg: discord.Message):
        """
        https://discordpy.readthedocs.io/en/stable/api.html#event-reference for a list of events
        """

        if msg.author.bot:
            return

        if self.bot.user in msg.mentions:
            await msg.reply("hello")


async def setup(bot: Bot):
    await bot.add_cog(SpinTheWheel(bot))
