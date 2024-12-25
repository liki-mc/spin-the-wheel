import discord
from discord.ext import commands

from bot.bot import Bot
from .schemdraw_custom_elms import CirclePart, EquilateralTriangle

from colorsys import hls_to_rgb
import numpy as np
import random
import schemdraw
import schemdraw.elements as elm
import shlex

def choose(options: list[str]) -> str:
    theta = random.randint(0, 359)
    N = len(options)
    alpha = 360 / N
    d = schemdraw.Drawing()
    for i in range(N):
        base_angle = i * alpha + theta
        d += CirclePart(radius = 5, alpha = alpha, theta = base_angle, fill = hls_to_rgb(i * (N//2 + 1) / N, 0.75, 0.35), color = "white").linewidth(0.2)
        angle = (i * alpha + theta + alpha / 2) * np.pi / 180
        d += elm.Label(options[i]).at((np.cos(angle), np.sin(angle))).theta(base_angle + alpha / 2)

    d += EquilateralTriangle(side_length = 2, fill = "#cccccc", theta = 90).at((5, 0)).linewidth(0.7)
    d.save("wheel.png")

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

        choose(options)
        await ctx.send(file = discord.File("wheel.png"))


async def setup(bot: Bot):
    await bot.add_cog(SpinTheWheel(bot))
