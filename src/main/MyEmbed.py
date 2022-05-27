from datetime import datetime

import disnake
from disnake.embeds import _EmptyEmbed


class MyEmbed(disnake.Embed):
    def __init__(self, *, inter: disnake.AppCmdInter, title: str, description: str = None, color: int | disnake.Colour | _EmptyEmbed):
        super().__init__(title=title, color=color, timestamp=datetime.now(), description=description)
        self.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar)
