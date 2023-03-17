import disnake
from components.PollView import PollView
from disnake.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="poll")
    async def poll(inter: disnake.AppCmdInter, vc: disnake.VoiceChannel = None):
        """投票"""
        view = PollView(inter, vc)
        await inter.send(embed=view.embed, view=view)
