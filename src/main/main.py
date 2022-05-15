# At the top of the file.
import datetime
import random

import disnake
from disnake.ext import commands

import settings
from DenpoView import DenpoView
from MyEmbed import MyEmbed


class Bot(commands.Bot):
    def __init__(self, intents: disnake.Intents):
        super().__init__(command_prefix=commands.when_mentioned, intents=intents, test_guilds=settings.GUILD_IDS)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


intents = disnake.Intents.all()
bot = Bot(intents)


@bot.slash_command()
async def denpo(inter: disnake.AppCmdInter):
    """Starts Denpo game."""
    view = DenpoView()
    await inter.send(embed=view.embed, view=view)


@bot.slash_command()
async def shuffle(inter: disnake.AppCmdInter, vc: disnake.VoiceChannel = None):
    """Shuffle vc members(default vc is "一般")."""
    if vc is None:
        vc = disnake.utils.get(inter.guild.voice_channels, name="一般")
    member_names = [f"{i + 1}: **{member.mention}**" for i, member in enumerate(vc.members)]
    random.shuffle(member_names)
    embed = MyEmbed(inter=inter, title="", color=disnake.Color.brand_green())
    embed.add_field(name=f"Members in \"{vc.name}\"", value="\n".join(member_names), inline=False)
    await inter.response.send_message(embed=embed)


@bot.slash_command(name="hiragana")
async def random_hiragana(inter: disnake.AppCmdInter):
    """Creates random Hiragana."""
    hiraganas = ["あ","い","う","え","お","か","き","く","け","こ","さ","し","す","せ","そ","た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ","ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ","ろ","わ","を","ん"]
    h = random.choice(hiraganas)
    embed = MyEmbed(inter=inter, title=h, color=disnake.Color.dark_gold())
    await inter.response.send_message(embed=embed)


@bot.slash_command(name="ito")
async def random_n(inter: disnake.AppCmdInter):
    """Creates random natural number <= 100. This message is shown to only you."""
    n = random.randint(1, 100)
    embed = MyEmbed(inter=inter, title=n, color=disnake.Color.dark_orange())
    await inter.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command()
async def dice(inter: disnake.AppCmdInter, number: commands.Range[1, ...]):
    """Show the result of dice roll only to you."""
    n = random.randint(1, number)
    embed = MyEmbed(inter=inter, title=n, color=disnake.Color.fuchsia())
    await inter.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command()
async def d(inter: disnake.AppCmdInter, number: commands.Range[1, ...]):
    """Alias of dice."""
    await dice(inter, number)


bot.run(settings.TOKEN)
