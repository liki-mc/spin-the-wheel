import discord
from discord.ext import commands

from bot.bot import Bot
from .schemdraw_custom_elms import CirclePart, EquilateralTriangle
from .arcade_wheel import choose

from colorsys import hls_to_rgb
import matplotlib.pyplot as plt
import numpy as np
import random
import schemdraw
import schemdraw.elements as elm
import shlex

def quickchoose(options: list[str]) -> str:
    theta = random.randint(0, 359)
    N = len(options)
    alpha = 360 / N
    d = schemdraw.Drawing()
    for i in range(N):
        base_angle = i * alpha + theta
        d += CirclePart(radius = 5, alpha = alpha, theta = base_angle, fill = hls_to_rgb(i * (N//2 + (1 if N != 2 else 0)) / N, 0.75, 0.35), color = "white").linewidth(0.2)
        angle = (i * alpha + theta + alpha / 2) * np.pi / 180
        option_text = options[i]
        if len(option_text) > 25:
            option_text = option_text[:23] + "..."
        d += elm.Label().at((np.cos(angle) * 4.5, np.sin(angle) * 4.5)).label(option_text, rotate = base_angle + alpha / 2, loc = "right")

    d += EquilateralTriangle(side_length = 2, fill = "#cccccc", theta = 90).at((5, 0)).linewidth(0.7)
    d.save("wheel.png")
    plt.close()

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
        
        newline = "\n"
        await ctx.send(f"Options: {newline}- {f'{newline}- '.join(options)}")
        await ctx.send("Spinning the wheel...")

        quickchoose(options)
        await ctx.send(file = discord.File("wheel.png"))
    
    
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
        
        newline = "\n"
        await ctx.send(f"Options: {newline}- {f'{newline}- '.join(options)}")
        await ctx.send("Spinning the wheel...")

        choose(options, "data/wheel.mp4")
        await ctx.send(file = discord.File("data/wheel.mp4"))

async def setup(bot: Bot):
    await bot.add_cog(SpinTheWheel(bot))
