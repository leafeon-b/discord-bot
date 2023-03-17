import random

import disnake
import settings
from cogs.denpo import Denpo
from cogs.poll import Poll
from cogs.random_word import RandomWord
from cogs.shuffle import Shuffle
from disnake.ext import commands
from MyEmbed import MyEmbed


class Bot(commands.Bot):
    def __init__(self, intents: disnake.Intents):
        super().__init__(command_prefix=commands.when_mentioned, intents=intents, test_guilds=settings.GUILD_IDS)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


intents = disnake.Intents.all()
bot = Bot(intents)
bot.add_cog(RandomWord(bot))
bot.add_cog(Denpo(bot))
bot.add_cog(Shuffle(bot))
bot.add_cog(Poll(bot))


@bot.slash_command(name="hiragana")
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


@bot.slash_command(name="random")
async def random_n(inter: disnake.AppCmdInter, min: commands.Range[2, ...] = 1, max: commands.Range[2, ...] = 10):
    """指定した最小値と最大値の範囲内の自然数をランダム生成(初期値は2~10)"""
    if max < min:
        max = min
    n = random.randint(min, max)
    embed = MyEmbed(inter=inter, title=n, description="", color=disnake.Color.dark_orange())
    await inter.response.send_message(embed=embed)


@bot.slash_command(name="random_twice")
async def random_n_twice(inter: disnake.AppCmdInter, min: commands.Range[1, ...] = 1, max: commands.Range[1, ...] = 6):
    """指定した最小値と最大値の範囲内の自然数を2回ランダム生成(初期値は1~6)"""
    if max < min:
        max = min
    n1 = random.randint(min, max)
    n2 = random.randint(min, max)
    embed = MyEmbed(inter=inter, title=f"{n1}, {n2}", description="", color=disnake.Color.dark_orange())
    await inter.response.send_message(embed=embed)


@bot.slash_command()
async def dice(inter: disnake.AppCmdInter, number: commands.Range[1, ...]):
    """指定した数を最大値としたサイコロを振る(自分だけに表示)"""
    n = random.randint(1, number)
    embed = MyEmbed(inter=inter, title=n, description="", color=disnake.Color.fuchsia())
    await inter.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command()
async def help(inter: disnake.AppCmdInter):
    """このBOTの定義コマンド一覧(自分だけに表示)"""
    all_commands: set[commands.slash_core.InvokableSlashCommand] = bot.slash_commands
    embed = MyEmbed(inter=inter, title="コマンド一覧", description="このBOTの定義コマンド一覧", color=disnake.Color.dark_blue())
    for command in all_commands:
        embed.add_field(name=command.name, value=command.description, inline=False)
    await inter.response.send_message(embed=embed, ephemeral=True)


bot.run(settings.TOKEN)
