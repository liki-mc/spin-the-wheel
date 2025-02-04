import discord
from discord.ext import commands

from bot.bot import Bot
from .arcade_wheel import spin, quickspin

import emoji
import re
import shlex

RANGE_REGEX = r"\s*(\d+) ?- ?(\d+)\s*"

class SpinTheWheel(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")
    
    def parse_args(self, args: str) -> list[str]:
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
    
        for option in options:
            if re.match(RANGE_REGEX, option):
                start, end = map(int, re.match(RANGE_REGEX, option).groups())
                index = options.index(option)
                options.remove(option)
                options[index:index] = map(str, range(start, end + 1))
        
        return options

    @commands.command()
    async def quickspin(self, ctx: commands.Context, *, args: str):
        options = self.parse_args(args)
        
        avatar = ctx.author.display_avatar
        with open("data/avatar.png", "wb") as file:
            await avatar.save(file)

        newline = "\n"
        await ctx.send(f"Options: {newline}- {f'{newline}- '.join(options)}")
        await ctx.send("Spinning the wheel...")

        quickspin(options, "data/wheel.png")
        await ctx.send(file = discord.File("data/wheel.png"))
    
    
    @commands.command()
    async def spin(self, ctx: commands.Context, *, args: str):
        options = self.parse_args(args)
        
        avatar = ctx.author.display_avatar
        with open("data/avatar.png", "wb") as file:
            await avatar.save(file)
        
        newline = "\n"
        await ctx.send(f"Options: {newline}- {f'{newline}- '.join(options)}")
        await ctx.send("Spinning the wheel...")

        spin(options, "data/wheel.mp4")
        await ctx.send(file = discord.File("data/wheel.mp4"))

async def setup(bot: Bot):
    await bot.add_cog(SpinTheWheel(bot))
