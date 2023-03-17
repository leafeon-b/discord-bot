import disnake
from components.MyEmbed import MyEmbed
from disnake import Embed


class WordView(disnake.ui.View):
    embed: Embed
    word: str
    viewr_ids: set[int]

    def __init__(self, word: str, *, timeout: float | None = 300):
        super().__init__(timeout=timeout)
        self.word = word
        self.viewr_ids = set()
        self.update_embed()

    @disnake.ui.button(label="お題を表示")
    async def show_word(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.viewr_ids.add(inter.author.id)
        self.update_embed()
        await inter.message.edit(embed=self.embed)
        embed = MyEmbed(inter=inter, title=self.word, description="", color=disnake.Color.dark_gold())
        await inter.response.send_message(embed=embed, ephemeral=True)

    def create_embed(self, *, title: str, description: str) -> disnake.Embed:
        return disnake.Embed(title=title, description=description, color=disnake.Color.blurple())

    def update_embed(self) -> None:
        self.embed = self.create_embed(
            title="Random Word",
            description=f"{len(self.viewr_ids)} 人が確認済",
        )
