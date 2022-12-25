# -*- coding: utf-8 -*-
import discord
import pyqrcode
import png
from threading import Thread
from discord.ext import commands
from pytube import YouTube, Search
from time import sleep
from bs4 import BeautifulSoup
import re
import requests as req


import os
import shutil
from google_images_download import google_images_download
import random
import subprocess

# responsible for handling all of the image commands


class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.download_folder = 'downloads'

        self.response = google_images_download.googleimagesdownload()
        self.arguments = {
            "keywords": "",
            "limit": 10,
            "format": "jpg",
            "size": "medium",
            "no_directory": True,
            "print_urls": True,
            "no_download": True
        }

        self.image_names = []
        self.images_qr = []
        # get the latest in the folder
        self.update_images()

    # @commands.command(name="get", help="Exibe imagem aleatória dos downloads")
    # async def get(self, ctx):
    #     try:
    #       await self.update_images()
    #       img = self.image_names[random.randint(0, len(self.image_names) - 1)]
    #       await ctx.send(file=discord.File(img))
    #     except:
    #       await ctx.send("Imagem Não Encontrada")

    @commands.command(name="getall", help="Exibe todas as imagem dos downloads")
    async def getall(self, ctx):
        for img in self.image_names:
            try:
                await ctx.send(file=discord.File(img))
            except:
                await ctx.send("Imagem Não Encontrada")
            # sleep(1)

    async def clear_folder(self):
        for filename in os.listdir(self.download_folder):
            file_path = os.path.join(self.download_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Falha ao excluir %s. Razão: %s' % (file_path, e))

    def update_images(self):
        # store all the names to the files
        self.image_names = []
        path = os.getcwd()
        direct = f"{path}\\{self.download_folder}"
        if os.listdir(direct):
            for filename in os.listdir(f"{path}\\{self.download_folder}"):
                self.image_names.append(os.path.join(
                    self.download_folder, filename))

    @commands.command(name="search", help="Pesquisa uma imagem no Google")
    async def search(self, ctx, *args):
        await self.clear_folder()
        print(f"ARGS: {args}")

        # fill the folder with new images
        self.arguments['keywords'] = " ".join(args)
        try:
            res, _ = self.response.download(self.arguments)
            for img in res[self.arguments['keywords']]:
                await ctx.send(img)
                sleep(0.5)
        except Exception as e:
            print(f"ERRO: {e}")

    @commands.command(name="qrgenerate", help="Gera uma imagem qr a partir de um texto")
    async def generate(self, ctx, *args):
        arguments = " ".join(args)
        img = pyqrcode.create(arguments)
        img.png('code.png', scale=12, module_color=[
                0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
        # img = qrcode.make(data=arguments)
        # file_img = "myqrcode.png"
        # img.save(file_img)
        # print(img)
        await ctx.send(file=discord.File('code.png'))

    @commands.command(name="video", help="Retorna o video do YouTube")
    async def view_video(self, ctx, *args):
        arguments = " ".join(args)
        if 'http' in arguments:
            video = YouTube(arguments)
        else:
            video = Search(arguments)
            video = video.results[0]
        direc = video.streams.filter(
            progressive=True).order_by('resolution').desc()

        file = None
        count_ok = 0
        title = ''
        for i in direc:
            if int(i.filesize/1000/1000) > 8:
                continue

            ext = i.mime_type.split('/')[-1]
            title = i.default_filename.replace(
                '  ', ' ').replace(' ', '_').replace(f'.{ext}', '').replace(
                "(", "").replace(")", "")

            directory = f'{title}.{ext}'
            file = i.download(filename=directory)

            if i.mime_type.split('/')[-1] == '3gpp':
                try:
                    subprocess.call(f'ffmpeg -i {directory} {title}.mp4')
                except:
                    os.system(f'ffmpeg -i {directory} {title}.mp4')
                    os.system(f'clear')
                finally:
                    try:
                        tmp = file.split('/')
                        tmp[-1] = f'{directory}'
                        tmp = '/'.join(tmp)
                        if os.path.exists(tmp):
                            os.remove(tmp)
                        file = file.replace('.3gpp', '.mp4')
                        print(file)
                    except Exception as e:
                        print(f'ERRO 1: {e}')

            try:
                await ctx.send(file=discord.File(file))
                if os.path.exists(file):
                    os.remove(file)
                count_ok += 1
                break
            except Exception as e:
                print(f"ERRO: {e}")
                if os.path.exists(file):
                    os.remove(file)
                continue
        if count_ok == 0:
            await ctx.send(f"ERRO: O video é superior a 8MB qtd_testados: {len(direc)}")

    @commands.command(name="kwai", help="Retorna o video do YouTube")
    async def download_kwai(self, ctx, *args):
        arguments = " ".join(args)
        if 'http' not in arguments:
            await ctx.send('Somente link')
        else:
            try:
                scr = req.get(arguments, allow_redirects=True)
                soup = BeautifulSoup(scr.text, 'html.parser')
                soup.prettify()
                link = soup.find(id="videoPlayer").get('src')
                file = req.get(link, allow_redirects=True)
                title = re.findall(r"\/([a-zA-Z0-9_-]*).mp4", link)[0]
                r = req.get(link, allow_redirects=True)
                content = r.content
                if content:
                    with open(f"{title}.mp4", 'wb') as f:
                        f.write(content)
                    await ctx.send(file=discord.File(f"{title}.mp4"))
                else:
                    print("NOT FOUND")
            except Exception as e:
                await ctx.send(f'ERROR {e}')
                print(f'ERROR {e}')
            finally:
                pass
                # if os.path.exists(f"{title}.mp4"):
                #     os.remove(f"{title}.mp4")
