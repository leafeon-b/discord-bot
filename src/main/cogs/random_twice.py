import random

import disnake
from disnake.ext import commands
from MyEmbed import MyEmbed


class RandomTwice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="random_twice")
    async def random_n_twice(
        inter: disnake.AppCmdInter, min: commands.Range[1, ...] = 1, max: commands.Range[1, ...] = 6
    ):
        """指定した最小値と最大値の範囲内の自然数を2回ランダム生成(初期値は1~6)"""
        if max < min:
            max = min
        n1 = random.randint(min, max)
        n2 = random.randint(min, max)
        embed = MyEmbed(inter=inter, title=f"{n1}, {n2}", description="", color=disnake.Color.dark_orange())
        await inter.response.send_message(embed=embed)
