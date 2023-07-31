
from keep_alive import keep_alive
from pathlib import Path
import argparse as ap
import platform
import logging
import os

if (platform.system() == 'Windows'):
    from dotenv import load_dotenv
    load_dotenv()

from discord.ext import commands
from cogs.image_cog import *
from cogs.music_cog import *
from cogs.music import *
from cogs.openapi_cog import *
from cogs.fordevs_cog import *

logging.basicConfig(
    level=logging.INFO, 
    filename="logger.txt", 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

server_status = False
tentativas = 1

while (not server_status):
    try:
        bot.run(os.getenv('TOKEN'))
        server_status = True
        break
    except Exception as e:
        logging.error(f"Error: {e}")
        logging.warning(f"Tentativas de Conexão: {tentativas}")
        print(f"Tentativas de Conexão: {tentativas}")
        server_status = False
        tentativas += 1
        sleep(605)
        continue
