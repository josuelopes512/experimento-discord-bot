from dotenv import load_dotenv
from keep_alive import keep_alive
from pathlib import Path
import argparse as ap
import os

from discord.ext import commands
from cogs.image_cog import *
from cogs.music_cog import *
from cogs.music import *
from cogs.openapi_cog import *
from cogs.fordevs_cog import *

load_dotenv()

Path('downloads').mkdir(exist_ok=True)

intents = discord.Intents(messages=True, guilds=True)

bot = commands.Bot(
    command_prefix='[', 
    description='Somente um outro bot de música.', 
    intents=intents
)

# bot = commands.Bot(command_prefix= '!')
bot.add_cog(ImageCog(bot))
bot.add_cog(MusicCog(bot))
bot.add_cog(Music(bot))
bot.add_cog(BotCog(bot))
bot.add_cog(FordevCog(bot))


@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

keep_alive()
bot.run(debug=os.getenv('TOKEN'))
