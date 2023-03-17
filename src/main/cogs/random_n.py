import random

import disnake
from disnake.ext import commands
from MyEmbed import MyEmbed


class RandomN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="random")
    async def random_n(inter: disnake.AppCmdInter, min: commands.Range[2, ...] = 1, max: commands.Range[2, ...] = 10):
        """指定した最小値と最大値の範囲内の自然数をランダム生成(初期値は2~10)"""
        if max < min:
            max = min
        n = random.randint(min, max)
        embed = MyEmbed(inter=inter, title=n, description="", color=disnake.Color.dark_orange())
        await inter.response.send_message(embed=embed)
