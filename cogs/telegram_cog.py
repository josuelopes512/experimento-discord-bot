from discord.ext import commands
from pyngrok import ngrok
import telebot
import os

telegrambot = telebot.TeleBot(os.getenv("TELEGRAM_BOT"), parse_mode=None)

list_chat_ids = []
list_ctx_ids = []

class TelegramCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook = self.get_tunnel()
        self.telegrambot = telebot.TeleBot(os.getenv("TELEGRAM_BOT"), parse_mode=None)
        
        start_dict = dict(
            function=lambda msg, obj=self: obj.start_handler(msg),
            filters=dict(
                commands=["start"],
            )
        )
        
        self.telegrambot.add_message_handler(start_dict)
        self.telegrambot.polling(none_stop=True)
    
    def start_handler(self, mensagem):
        self.telegrambot.send_message(
                mensagem.chat.id,
                "Saindo a pizza pra sua casa: Tempo de espera em 20min"
        )

    def get_tunnel(self):
        http_tunnel = ngrok.connect()
        return http_tunnel.public_url
    
    @commands.command(name="mastercodebot", help="Gerador de Pessoas 4Devs")
    async def mastercodebot(self, ctx):
        try:
            await ctx.send(f"```hdfhfghdgdgh```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
