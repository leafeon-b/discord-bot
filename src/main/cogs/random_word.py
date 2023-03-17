import csv
import random

import disnake
from components.WordView import WordView
from disnake.ext import commands


class RandomWord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="random_word")
    async def random_word(inter: disnake.AppCmdInter):
        """ランダムなお題を出す"""
        view = WordView(create_random_word())
        await inter.send(embed=view.embed, view=view)


def create_random_word() -> str:
    file_name = "src/data/codenames-online-original-pack-3-master.csv"
    with open(file_name) as f:
        rows = list(csv.reader(f))
        choice: str = random.choices(rows)[0][0]
        return choice
