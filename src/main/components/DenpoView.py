import re
from dataclasses import dataclass
from typing import ClassVar, Pattern

import disnake
from components.MyEmbed import MyEmbed
from disnake import Embed, MessageInteraction, TextInputStyle


@dataclass
class Hint:
    """TODO: プロセスが走り続ける間はorderが増え続けることでバグが発生するかも"""

    tmp_order: ClassVar[int] = 0

    author_id: int
    author: str
    phrase: str
    order: int

    @classmethod
    def get_tmp_order(cls):
        cls.tmp_order += 1
        return cls.tmp_order - 1

    def __init__(self, author_id: int, author: str, phrase: str):
        self.author_id = author_id
        self.author = author
        self.phrase = phrase
        self.order = self.get_tmp_order()


class DenpoView(disnake.ui.View):
    embed: Embed
    hints: list[Hint]

    def __init__(self, *, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.hints = []
        self.update_embed()

    def sort_hint(self) -> None:
        """ヒントのリストを文字数の少ない順、追加の早い順に並び替える"""
        self.hints.sort(key=lambda hint: (len(hint.phrase), hint.order))

    def append_hint(self, hint: Hint):
        self.hints.append(hint)
        self.sort_hint()
        self.update_embed()

        self.sort_hint()
        self.update_embed()

    def create_embed(self, *, title: str, description: str) -> disnake.Embed:
        return disnake.Embed(title=title, description=description, color=disnake.Color.blurple())

    def update_embed(self):
        self.embed = self.create_embed(
            title="Denpo!!",
            description=f"{len(self.hints)} 人が送信済み",
        )

    async def show_next_hint(self, inter: disnake.MessageInteraction, index: int = 0):
        async def next_hint_callback(tmp_inter: disnake.MessageInteraction):
            await self.show_next_hint(tmp_inter, index + 1)

        next_hint_button = disnake.ui.Button(label="次のヒントを表示")
        next_hint_button.callback = next_hint_callback
        if index == len(self.hints) - 1:  # 最後のヒントでは次のヒントを表示ボタンを非アクティブにする
            next_hint_button.disabled = True

        async def all_hint_callback(tmp_inter: disnake.MessageInteraction):
            next_hint_button.disabled = True  # 全てのヒントを表示する時は次のヒントを表示ボタンを非アクティブにする
            description = ""
            for hint in self.hints:
                description += f"{hint.phrase} ({hint.author})\n"
            embed = self.create_embed(title="All Hints", description=description)
            await tmp_inter.response.edit_message(view=view, embed=embed)

        all_hint_button = disnake.ui.Button(label="全てのヒントを表示")
        all_hint_button.callback = all_hint_callback

        view = disnake.ui.View()
        view.add_item(next_hint_button)
        view.add_item(all_hint_button)

        description = ""
        for i in range(index + 1):
            phrase = f"__{self.hints[i].phrase}__" if i == index else self.hints[i].phrase  # 最後に追加したヒントは下線で強調
            description += f"{phrase} ({self.hints[i].author})\n"
        embed = self.create_embed(title="Denpo!!", description=description)
        await inter.response.edit_message(view=view, embed=embed)

    @disnake.ui.button(label="ヒントを送信")
    async def start(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(modal=DenpoModal(inter, self))

    @disnake.ui.button(label="ヒントを表示", custom_id="show_hints")
    async def show_hints(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if len(self.hints) == 0:
            await inter.response.send_message("ヒントがありません.")
            return
        for child in self.children:
            if isinstance(child, disnake.ui.Button) and child.custom_id == "show_hints":
                child.disabled = True
                await inter.message.edit(view=self)
        await self.show_next_hint(inter)

    @disnake.ui.button(label="ゲームを終了")
    async def exit(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = MyEmbed(inter=inter, title="ゲームを終了しました.", color=disnake.Color.blurple())
        await inter.message.edit(view=None, embed=embed)


class DenpoModal(disnake.ui.Modal):
    inter: disnake.MessageInteraction
    view: DenpoView

    def __init__(self, inter: MessageInteraction, view: DenpoView):
        self.inter = inter
        self.view = view
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Hint",
                placeholder="ここにあなたのヒントを入力してください.",
                custom_id="hint",
                style=TextInputStyle.single_line,
                max_length=6,
            ),
        ]
        super().__init__(
            title="Denpo",
            custom_id="denpo",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="", color=disnake.Color.light_gray())
        embed.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar)
        for key, value in inter.text_values.items():
            if key == "hint":
                author_id = inter.author.id
                if author_id in [hint.author_id for hint in self.view.hints]:  # ユーザがすでにヒントを送信済みかチェック
                    await inter.response.send_message(f"{inter.author.display_name} はすでにヒントを送信済みです.")
                    return
                p: Pattern = re.compile(r"^[ぁ-ゖ]+$")
                if p.fullmatch(value) is None:  # ヒントにひらがな以外の文字が含まれていないかチェック
                    await inter.response.send_message("ヒントはひらがなのみ使用できます.")
                    return
                self.view.append_hint(Hint(inter.author.id, inter.author.display_name, value))
                await self.inter.message.edit(view=self.view, embed=self.view.embed)
            embed.add_field(
                name="Your Hint",
                value=value[:1024],  # 1024文字が上限
                inline=False,
            )
        await inter.response.send_message(embed=embed, ephemeral=True)
