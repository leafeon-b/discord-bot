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


intents = disnake.Intents.all()
bot = Bot(intents)
bot.add_cog(RandomWord(bot))
bot.add_cog(Denpo(bot))
bot.add_cog(Shuffle(bot))
bot.add_cog(Poll(bot))
bot.add_cog(RandomHiragana(bot))
bot.add_cog(RandomN(bot))
bot.add_cog(RandomTwice(bot))
bot.add_cog(Dice(bot))
bot.add_cog(Help(bot))

bot.run(settings.TOKEN)
