import os
import openai
from discord.ext import commands
from time import sleep

# ids = [i["id"] for i in openai.Model.list()["data"]]

class BotCog(commands.Cog):
    def __init__(self, bot):
        openai.api_key = os.getenv("OPENAPI_APIKEY")
        openai.organization = os.getenv("OPENAPI_ORG")
        
        self.bot = bot
    
    @commands.command(name="chatgpt", help="Integração com o ChatGPT")
    async def chatgpt(self, ctx, *args):
        query = " ".join(args)

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=query,
                temperature=0.7,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            result = response["choices"][0]["text"] if "choices" in response else None

            if(result is None):
                raise Exception("Tente Novamente")
            
            sleep(1)
            await ctx.send(f"```{result}```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="chatgptimg", help="Integração com o ChatGPT Imagem")
    async def chatgptimg(self, ctx, *args):
        query = " ".join(args)

        try:
            response = openai.Image.create(
                prompt=query,
                n=1,
                size="1024x1024"
            )
            
            result = response["data"][0]["url"]
            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"Erro: {e}")
