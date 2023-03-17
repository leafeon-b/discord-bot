import disnake
from disnake import Embed

from MyEmbed import MyEmbed


class WordView(disnake.ui.View):
    embed: Embed
    word: str

    def __init__(self, word: str, *, timeout: float | None = 300):
        super().__init__(timeout=timeout)
        self.word = word
        self.embed = disnake.Embed(
            title="Random Word", description="お題が出るよ", color=disnake.Color.blurple()
        )

    @disnake.ui.button(label="お題を表示", custom_id="show_word")
    async def show_word(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = MyEmbed(inter=inter, title=self.word, description="", color=disnake.Color.dark_gold())
        await inter.response.send_message(embed=embed, ephemeral=True)
