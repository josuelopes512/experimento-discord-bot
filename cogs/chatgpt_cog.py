from discord.ext import commands
from UnlimitedGPT import ChatGPT
import os
import platform
from time import sleep
from threading import Thread

def divide_text(text, max_length):
    text_parts = []
    current_part = ""
    words = text.split()

    for word in words:
        if len(current_part) + len(word) + 1 <= max_length:  # +1 for the space after the word
            current_part += word + " "
        else:
            text_parts.append(current_part.strip())
            current_part = word + " "

    # Add the last part if it's not empty
    if current_part:
        text_parts.append(current_part.strip())

    return text_parts

def reload_chatgpt(session_token):
    return ChatGPT(session_token=session_token, verbose=True, headless=True)

class ChatGPTCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv("CHATGPT_TOKEN")
        self.conversation_id = os.getenv("CONVERSATION_ID")
        
        if platform.system() == "Linux":
            self.api = ChatGPT(session_token=self.token, verbose=True, headless=True, driver_executable_path='./chromedriver/chromedriver')
        else:
            self.api = ChatGPT(session_token=self.token, verbose=True, headless=True)
        
        if self.conversation_id:
            self.api.switch_conversation(self.conversation_id)
    
    @commands.command(name="sendmessage", help="Integração com o ChatGPT")
    async def sendmessage(self, ctx, *args):
        query = " ".join(args)

        try:
            response = self.api.send_message(query)
            
            if self.conversation_id is None:
                self.conversation_id = response.conversation_id if response else None

            result = response.response if response else None

            if(result is None):
                raise Exception("Tente Novamente")
            
            if len(result) > 2000:
                texts = divide_text(result, 1998)
                for text in texts:
                    await ctx.send(f"```{text}```")
                return
            
            sleep(1)
            await ctx.send(f"```{result}```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="switch_account", help="Integração com o ChatGPT")
    async def switch_account(self, ctx, *args):
        query = " ".join(args)

        try:
            self.api.switch_account(query)
            await ctx.send(f"```switch_account OK```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="switch_conversation", help="Integração com o ChatGPT")
    async def switch_conversation(self, ctx, *args):
        query = " ".join(args)

        try:
            self.api.switch_conversation(query)
            await ctx.send(f"```switch_conversation OK```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="logout", help="Integração com o ChatGPT")
    async def logout(self, ctx, *args):
        try:
            Thread(target=self.api.logout).start()
            await ctx.send(f"```switch_conversation OK```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="login", help="Integração com o ChatGPT")
    async def login(self, ctx, *args):
        query = " ".join(args)
        try:
            def log_in():
                self.api.__del__()
                self.api = reload_chatgpt(query)
            
            Thread(target=log_in).start()
            await ctx.send(f"```login OK```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="regenerate", help="Integração com o ChatGPT")
    async def regenerate(self, ctx, *args):
        try:
            response = self.api.regenerate_response()
            if self.conversation_id is None:
                self.conversation_id = response.conversation_id if response else None
            
            result = response.response if response else None

            if(result is None):
                raise Exception("Tente Novamente")
            
            if len(result) > 2000:
                texts = divide_text(result, 1998)
                for text in texts:
                    await ctx.send(f"```{text}```")
                return
            
            sleep(1)
            await ctx.send(f"```{result}```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")

    @commands.command(name="reload_chatgpt", help="Integração com o ChatGPT")
    async def reload_chatgpt(self, ctx, *args):
        try:
            def reload():
                self.api.__del__()
                self.api = reload_chatgpt(self.token)
            
            Thread(target=reload).start()
            
            await ctx.send(f"```reload_chatgpt OK```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="restart_chatgpt", help="Integração com o ChatGPT")
    async def restart_chatgpt(self, ctx, *args):
        try:
            def restart():
                self.api.__del__()
                self.token = os.getenv("CHATGPT_TOKEN")
                self.api = reload_chatgpt(self.token)
            
            Thread(target=restart).start()
            
            await ctx.send(f"```reload_chatgpt OK```")
        except Exception as e:
            await ctx.send(f"Erro: {e}")
