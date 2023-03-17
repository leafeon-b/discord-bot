import random

import disnake
from disnake.ext import commands
from MyEmbed import MyEmbed


class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog loaded.")

    @commands.slash_command(name="shuffle")
    async def shuffle(inter: disnake.AppCmdInter, vc: disnake.VoiceChannel = None):
        """VCにいるメンバーをシャッフルする.
        VCを指定しない場合はコマンドの使用者が入っているVCが適用される.
        コマンドの使用者がVCに入っていない場合は"一般"チャンネルが適用される.
        """
        if vc is None:
            vc = inter.author.voice.channel
        if vc is None:
            vc = disnake.utils.get(inter.guild.voice_channels, name="一般")
        members = vc.members
        random.shuffle(members)
        member_names = [f"{i + 1}: **{member.mention}**" for i, member in enumerate(members)]
        embed = MyEmbed(inter=inter, title="", description="", color=disnake.Color.brand_green())
        embed.add_field(name=f'Members in VC "{vc.name}"', value="\n".join(member_names), inline=False)
        await inter.response.send_message(embed=embed)
