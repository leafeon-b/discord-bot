import collections
from dataclasses import dataclass

import disnake
from disnake import Member

from MyEmbed import MyEmbed


@dataclass
class Vote():
    vote_from: Member
    vote_to: Member

    def __str__(self) -> str:
        return f"**{self.vote_to.mention}** <- **{self.vote_from.mention}**"
    

class PollView(disnake.ui.View):
    inter: disnake.AppCmdInter
    vc_name: str
    vc_members: list[Member]
    embed: disnake.Embed
    votes: list[Vote]

    def __init__(self, inter: disnake.AppCmdInter, vc: disnake.VoiceChannel, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.inter = inter
        if vc is None:
            vc = inter.author.voice.channel
        if vc is None:
            vc = disnake.utils.get(inter.guild.voice_channels, name="一般")
        self.vc_name = vc.name
        self.vc_members = vc.members
        self.votes = []
        self.init_embed()

    async def append_vote(self, vote: Vote):
        self.votes.append(vote)
        await self.refresh_embed()

    def init_embed(self) -> disnake.Embed:
        member_names = [f"**{member.mention}**" for member in self.vc_members]
        self.embed = MyEmbed(inter=self.inter, title="Poll", description=self.make_embed_description(), color=disnake.Color.magenta())
        self.embed.add_field(name=f"Members in \"{self.vc_name}\"", value="\n".join(member_names), inline=False)
        for member in self.vc_members:
            button = disnake.ui.Button(label=member.display_name, style=disnake.ButtonStyle.blurple)
            async def callback(tmp_inter: disnake.MessageInteraction):
                author_id = tmp_inter.author.id
                if author_id in [vote.vote_from.id for vote in self.votes]:
                    await tmp_inter.response.send_message(f"{tmp_inter.author.display_name} はすでに投票済みです.", ephemeral=True)
                    return
                vote = Vote(tmp_inter.author, member)
                await self.append_vote(vote)
                await tmp_inter.response.send_message(f"**{member.mention}** に投票しました.", ephemeral=True)
            button.callback = callback
            self.add_item(button)

    async def refresh_embed(self):
        self.embed.description = self.make_embed_description()
        await self.inter.edit_original_message(view=self, embed=self.embed)

    @disnake.ui.button(label="結果を表示", style=disnake.ButtonStyle.green)
    async def start(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        poll_result = self.make_poll_result()
        poll_result_str = self.make_poll_result_str(poll_result)
        description = "\n".join([str(v) for v in self.votes])
        embed = MyEmbed(inter=inter, title="投票結果", description=description, color=disnake.Color.blue())
        embed.add_field(name="集計結果", value=poll_result_str)
        await inter.response.send_message(embed=embed)
    
    def make_poll_result(self) -> list[tuple[Member, int]]:
        member_ids: list[int] = [member.id for member in self.vc_members]
        counter = collections.Counter(member_ids)
        most_common: list[tuple[int, int]] = counter.most_common()
        member_and_count_list = [(self.find_member_by_id(id), count) for id, count in most_common]
        return member_and_count_list

    def make_poll_result_str(self, poll_result: list[tuple[Member, int]]):
        max_vote_count = poll_result[0][1]
        mention_and_count_list = [(member.mention, count) for member, count in poll_result]
        mention_and_count_str_list = []
        for mention, count in mention_and_count_list:
            suffix = "**(吊り)** " if count == max_vote_count else "" # 最多得票は全員吊り対象
            mention_and_count_str_list.append(f"**{mention}**: {count}票 {suffix}")
        result = "\n".join(mention_and_count_str_list)
        return result

    def find_member_by_id(self, id: int) -> Member:
        member_ids = [member.id for member in self.vc_members]
        index = member_ids.index(id)
        return self.vc_members[index]

    def make_embed_description(self):
        return f"投票先を選択してください.\n**{len(self.votes)}** 人が投票済み"
