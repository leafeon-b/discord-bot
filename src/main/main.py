import disnake
import settings
from cogs.denpo import Denpo
from cogs.dice import Dice
from cogs.help import Help
from cogs.poll import Poll
from cogs.random_hiragana import RandomHiragana
from cogs.random_n import RandomN
from cogs.random_twice import RandomTwice
from cogs.random_word import RandomWord
from cogs.shuffle import Shuffle
from disnake.ext import commands


class Bot(commands.Bot):
    def __init__(self, intents: disnake.Intents):
        super().__init__(command_prefix=commands.when_mentioned, intents=intents, test_guilds=settings.GUILD_IDS)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


def main():
    cogs = [
        RandomWord,
        Denpo,
        Shuffle,
        Poll,
        RandomHiragana,
        RandomN,
        RandomTwice,
        Dice,
        Help,
    ]
    intents = disnake.Intents.all()
    bot = Bot(intents)
    for cog in cogs:
        bot.add_cog(cog(bot))

    bot.run(settings.TOKEN)


if __name__ == "__main__":
    main()
