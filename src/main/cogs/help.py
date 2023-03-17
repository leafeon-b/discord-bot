import disnake
from components.MyEmbed import MyEmbed
from disnake.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="help")
    async def help(self, inter: disnake.AppCmdInter):
        """このBOTの定義コマンド一覧(自分だけに表示)"""
        all_commands: set[commands.slash_core.InvokableSlashCommand] = self.bot.slash_commands
        embed = MyEmbed(inter=inter, title="コマンド一覧", description="このBOTの定義コマンド一覧", color=disnake.Color.dark_blue())
        for command in all_commands:
            embed.add_field(name=command.name, value=command.description, inline=False)
        await inter.response.send_message(embed=embed, ephemeral=True)
