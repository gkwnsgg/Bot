import discord
import requests
import asyncio
import json
import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from discord import app_commands
from discord.ext import commands
from 花朝月夕_Token import Token, RToken

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
headers_lol = {"X-Riot-Token":RToken}
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd)
    await bot.change_presence(activity=discord.Game(name='패치'))
    await bot.wait_until_ready()
    await bot.tree.sync()
    print('花朝月夕 enabled.')

@bot.tree.command(name="전적검색", description="닉네임과 태그를 정확하게 입력해주세요.")
async def slash1(interaction: discord.Interaction, 닉네임:str, 태그:str):
    URL_puuid = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{닉네임}/{태그}?api_key={RToken}"
    r = requests.get(URL_puuid,headers=headers_lol)
    print(r.json()['puuid'])
    await interaction.response.send_message(r.json()['puuid'])
bot.run(Token) 