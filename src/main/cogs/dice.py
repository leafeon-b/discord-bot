import random

import disnake
from components.MyEmbed import MyEmbed
from disnake.ext import commands


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="dice")
    async def dice(inter: disnake.AppCmdInter, number: commands.Range[1, ...]):
        """指定した数を最大値としたサイコロを振る(自分だけに表示)"""
        n = random.randint(1, number)
        embed = MyEmbed(inter=inter, title=n, description="", color=disnake.Color.fuchsia())
        await inter.response.send_message(embed=embed, ephemeral=True)
