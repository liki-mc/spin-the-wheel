from discord.ext import commands

from bot.bot import Bot

import shlex

class SpinTheWheel(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @commands.command()
    async def spin(self, ctx: commands.Context, *, args: str):
        if "\n" in args:
            options = args.split("\n")
        elif ";" in args:
            options = args.split(";")
        elif "\"" in args:
            options = shlex.split(args)
        else:
            options = args.split(",")
        
        await ctx.send(f"Options: \n- {"\n- ".join(options)}")
        await ctx.send("Spinning the wheel...")


async def setup(bot: Bot):
    await bot.add_cog(SpinTheWheel(bot))
