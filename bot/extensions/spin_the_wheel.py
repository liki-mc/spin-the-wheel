import discord
from discord.ext import commands

from bot.bot import Bot
from .arcade_wheel import spin, quickspin

import shlex

class SpinTheWheel(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @commands.command()
    async def quickspin(self, ctx: commands.Context, *, args: str):
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
