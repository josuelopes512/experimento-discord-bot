from google_images_download import google_images_download
from discord.ext import commands
from keep_alive import keep_alive
from pathlib import Path
from image_cog import *
from music import *
from music_cog import *
import os

Path('downloads').mkdir(exist_ok=True)

bot = commands.Bot('!', description='Somente um outro bot de música.')
# bot = commands.Bot(command_prefix= '!')
bot.add_cog(image_cog(bot))
bot.add_cog(music_cog(bot))
bot.add_cog(Music(bot))


@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

keep_alive()
bot.run(os.environ['TOKEN'])