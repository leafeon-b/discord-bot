import collections
from dataclasses import dataclass

import disnake
from components.MyEmbed import MyEmbed
from disnake import Member


@dataclass
class Vote:
    vote_from: Member
    vote_to: Member

    def __str__(self) -> str:
        return f"{self.vote_to.display_name} <- {self.vote_from.display_name}"


class PollView(disnake.ui.View):
    inter: disnake.AppCmdInter
    vc_name: str
    vc_members: list[Member]
    embed: disnake.Embed
    votes: list[Vote]

    def __init__(self, inter: disnake.AppCmdInter, vc: disnake.VoiceChannel, *, timeout: float | None = None):
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
        self.embed = MyEmbed(
            inter=self.inter, title="投票先を選択", description=self.make_embed_description(), color=disnake.Color.magenta()
        )
        for member in self.vc_members:
            button = disnake.ui.Button(
                label=member.display_name, style=disnake.ButtonStyle.blurple, custom_id=str(member.id)
            )

            async def callback(tmp_inter: disnake.MessageInteraction):
                author_id = tmp_inter.author.id
                if author_id in [vote.vote_from.id for vote in self.votes]:
                    await tmp_inter.response.send_message(
                        f"{tmp_inter.author.display_name} はすでに投票済みです.", ephemeral=True
                    )
                    return
                vote_to_id = tmp_inter.component.custom_id
                vote_to = self.find_member_by_id(int(vote_to_id))
                vote = Vote(tmp_inter.author, vote_to)
                await self.append_vote(vote)
                await tmp_inter.response.send_message(f"**{vote_to.display_name}** に投票しました.", ephemeral=True)

            button.callback = callback
            self.add_item(button)

    async def refresh_embed(self):
        self.embed.description = self.make_embed_description()
        await self.inter.edit_original_message(view=self, embed=self.embed)

    @disnake.ui.button(label="結果を表示", style=disnake.ButtonStyle.green)
    async def start(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        poll_result = self.make_poll_result()
        try:
            poll_result_str = self.make_poll_result_str(poll_result)
        except IndexError:
            embed = MyEmbed(
                inter=inter, title="まだ誰も投票していません.", description="投票が終わってから結果を表示してください.", color=disnake.Color.red()
            )
            return await inter.response.send_message(embed=embed, ephemeral=True)
        description = "\n".join([str(v) for v in self.votes])
        embed = MyEmbed(inter=inter, title="投票結果", description=f"```{description}```", color=disnake.Color.blue())
        embed.add_field(name="集計結果", value=f"```{poll_result_str}```")
        await inter.response.send_message(embed=embed)

    def make_poll_result(self) -> list[tuple[Member, int]]:
        vote_to_id_list: list[int] = [vote.vote_to.id for vote in self.votes]
        counter = collections.Counter(vote_to_id_list)
        most_common: list[tuple[int, int]] = counter.most_common()
        member_and_count_list = [(self.find_member_by_id(id), count) for id, count in most_common]
        return member_and_count_list

    def make_poll_result_str(self, poll_result: list[tuple[Member, int]]):
        max_vote_count = poll_result[0][1]
        display_name_and_count_list = [(member.display_name, count) for member, count in poll_result]
        display_name_and_count_str_list = []
        for display_name, count in display_name_and_count_list:
            suffix = "(吊り) " if count == max_vote_count else ""  # 最多得票は全員吊り対象
            display_name_and_count_str_list.append(f"{display_name}: {count}票 {suffix}")
        result = "\n".join(display_name_and_count_str_list)
        return result

    def find_member_by_id(self, id: int) -> Member:
        member_ids = [member.id for member in self.vc_members]
        index = member_ids.index(id)
        return self.vc_members[index]

    def make_embed_description(self):
        return f"**{len(self.votes)}** 人が投票済み"
