import discord
import requests
import asyncio
import json
import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from discord.ext import commands
from 花朝月夕_Token import Token
from 花朝月夕_Token import RToken
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
#client = discord.Client()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd)
    await bot.change_presence(activity=discord.Game(name='패치'))
    print('花朝月夕 enabled.')

@bot.event
async def on_disconnect():
    await bot.change_presence(status=discord.Status.offline)
    await bot.change_presence(activity=discord.Game(name='충전'))
    print('花朝月夕 disabled.')

@bot.event
async def on_message(msg):
    if msg.author.bot: return None
    await bot.process_commands(msg)

@bot.event
async def on_msesage(message):

    if message.content.startswitch('티어'):
        start = time.time()
        Name = message.contnet[4:len(message.content)]
        FName = Name.Replace(" ","+")

bot.run(Token)