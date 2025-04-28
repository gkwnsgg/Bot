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
async def on_message(msg):
    if message.content.startswith('전적검색'):
        Ntg = ' '.join(args)
        URL_puuid = 'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{/KR33?api_key='+RToken

        
bot.run(Token) 