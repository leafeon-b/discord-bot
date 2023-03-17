import disnake
from disnake.ext import commands
from WordView import WordView


class RandomWord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    # @commands.slash_command()
    # async def hello(self, ctx, *, member: disnake.Member = None):
    #     """Says hello"""
    #     print("hello")

    @commands.slash_command(name="random_word")
    async def random_word(inter: disnake.AppCmdInter):
        """ランダムなお題を出す"""
        view = WordView("foo")
        await inter.send(embed=view.embed, view=view)
