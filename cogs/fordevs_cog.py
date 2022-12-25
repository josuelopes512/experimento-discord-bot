from fordev.generators.company import company
from fordev.generators import people
from discord.ext import commands


class FordevCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="people", help="Gerador de Pessoas 4Devs")
    async def people(self, ctx):
        try:
            response = people(sex='M', age=25, uf_code='SP')

            text = ""
            for k, v in response[0].items():
                text += f"{k}: {v}\n"
            
            await ctx.send(f"```{text}```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="company", help="Gerador de Empresas 4Devs")
    async def company(self, ctx):
        try:
            response = company()
            text = ""
            for k, v in response.items():
                text += f"{k}: {v}\n"
            
            await ctx.send(f"```{text}```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")

