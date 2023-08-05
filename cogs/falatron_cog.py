import os
import discord
from .utils.utils import contabilizar_caracteres_por_linha
from discord.ext import commands
from falatron.falatron import Falatron
from falatron.voice_list import data_dict_ind

class FalatronCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.falatron = Falatron()
    
    @commands.command(name="getaudio", help="Ex: [getaudio 120 texto - Integração com o Falatron")
    async def getaudio(self, ctx, *args):
        query = " ".join(args[1:])
        voice_name= data_dict_ind[int(args[0])] 
        
        try:
            task = self.falatron.request_audio(query, voice_name)
            task_id = task.get("task_id", None)
            voice = self.falatron.get_audio(task_id, task["cookie"])
            
            audio = voice.get("audio", None)
            self.falatron.save_audio(task_id, audio)
            
            await ctx.send(file=discord.File(f"./audios/{task_id}.mp3"))
        except Exception as e:
            await ctx.send(f"Erro: {e}")
        finally:
            if os.path.exists(f"./audios/{task_id}.mp3"):
                os.remove(f"./audios/{task_id}.mp3")
    
    @commands.command(name="getaudiolist", help="Integração com o Falatron")
    async def getaudiolist(self, ctx, *args):
        try:
            data = ""
            for k, v in data_dict_ind.items():
                data += f"{k}-{v}\n"
            
            lista_de_listas = contabilizar_caracteres_por_linha(data)
            for i, lista in enumerate(lista_de_listas, start=1):
                total_caracteres = sum(caracteres for caracteres, _ in lista)
                print(f"Lista {i} (Total de caracteres: {total_caracteres}):")
                new_data = ""
                
                for _, linha in lista:
                    new_data += f"{linha}"
                print(len(new_data))
                await ctx.send(f"```{new_data}```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="addtokenfalatron", help="Integração com o Falatron")
    async def addtokenfalatron(self, ctx, *args):
        query = " ".join(args)
        try:
            del self.falatron
            del os.environ["FALATRON_CF_CLEARANCE"]
            
            os.environ["FALATRON_CF_CLEARANCE"] = query
            self.falatron = Falatron(cf_clearance=query)
            
            await ctx.send(f"OK Token Configurado")
        except Exception as e:
            await ctx.send(f"Erro: {e}")