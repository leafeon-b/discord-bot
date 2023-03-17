import disnake
from components.DenpoView import DenpoView
from disnake.ext import commands


class Denpo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="denpo")
    async def random_word(inter: disnake.AppCmdInter):
        """デンポー!!ゲームを開始する"""
        view = DenpoView()
        await inter.send(embed=view.embed, view=view)
