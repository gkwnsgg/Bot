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

headers_lol = {"X-Riot-Token":RToken}
Name_lol = ' '
Tag_lol = ' ' 
URL_puuid = "https://assia.api.riotgames.com/riot/account/v1/account/by-riot-id/"+Name_lol/+Tag_lol+'api_key=+RToken'

print(URL_puuid)
#class match():
#    def __init__(self,game_duration,game_creaction,game_Mode,player):
#        self.duration=str(datetime.timedelta(seconds=game_duration))