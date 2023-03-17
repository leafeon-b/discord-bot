import random

import disnake
import settings
from cogs.denpo import Denpo
from cogs.poll import Poll
from cogs.random_hiragana import RandomHiragana
from cogs.random_n import RandomN
from cogs.random_twice import RandomTwice
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
bot.add_cog(RandomHiragana(bot))
bot.add_cog(RandomN(bot))
bot.add_cog(RandomTwice(bot))


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
