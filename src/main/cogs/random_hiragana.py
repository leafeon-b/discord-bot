import random

import disnake
from components.MyEmbed import MyEmbed
from disnake.ext import commands


class RandomHiragana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="random_hiragana")
    async def random_hiragana(inter: disnake.AppCmdInter):
        """ひらがな1文字をランダム生成"""
        hiraganas = [
            "あ",
            "い",
            "う",
            "え",
            "お",
            "か",
            "き",
            "く",
            "け",
            "こ",
            "さ",
            "し",
            "す",
            "せ",
            "そ",
            "た",
            "ち",
            "つ",
            "て",
            "と",
            "な",
            "に",
            "ぬ",
            "ね",
            "の",
            "は",
            "ひ",
            "ふ",
            "へ",
            "ほ",
            "ま",
            "み",
            "む",
            "め",
            "も",
            "や",
            "ゆ",
            "よ",
            "ら",
            "り",
            "る",
            "れ",
            "ろ",
            "わ",
            "を",
            "ん",
        ]
        h = random.choice(hiraganas)
        embed = MyEmbed(inter=inter, title=h, color=disnake.Color.dark_gold())
        await inter.response.send_message(embed=embed)
