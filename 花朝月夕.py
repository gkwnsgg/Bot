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
#     print(r.text)
     Puuid = (r.json()['puuid'])
#     print(r.status_code)
     if r.status_code == 200:
         URL_summoner = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{Puuid}?api_key={RToken}"
         r = requests.get(URL_summoner, headers=headers_lol)
#         print(r.text)
         Icon = str(r.json()['profileIconId'])
         Level = str(r.json()['summonerLevel'])
#         print(Icon)
#         print(Level)
         URL_league = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{Puuid}?api_key={RToken}"
         r = requests.get(URL_league, headers=headers_lol)
#         print(r.text)
         RankS = json.loads(r.text)
#         print(RankS)
         if len(RankS) == 0:
             await interaction.response.send_message("소환사님의 랭크 정보가 없습니다.")
         for i in RankS:
             if i["queueType"] == "RANKED_SOLO_5x5":
                 rank = str(i["rank"])
                 tier = str(i["tier"])
                 leaguepoints = str(i["leaguePoints"])
                 wins = str(i["wins"])
                 losses = str(i["losses"])
                 ratio = str(round(int(wins)*100/(int(wins)+int(losses)), 1))
#                 print(rank)
#                 print(tier)
                 URL_champion = f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{Puuid}?api_key={RToken}"
                 r = requests.get(URL_champion, headers=headers_lol)
                 player_mastery = json.loads(r.text)
#                 print(player_mastery)
                 for i in player_mastery:
                     most_champion_id = int(i["championId"])
                     most_champion_points = str(i["championPoints"])
                     URL_ddragon1 = f"https://ddragon.leagueoflegends.com/cdn/15.9.1/data/ko_KR/champion.json"
                     r = requests.get(URL_ddragon1)
                     champion_name = json.loads(r.text)
                     #print(champion_name)
                     champion_name_list = champion_name["data"]
                     #print(type(champion_name_list))
                     global most_champion_name
                     for i in champion_name_list:
                         if(champion_name["data"][i]["key"])==str(most_champion_id):
                             most_champion_name = champion_name["data"][i]["name"]
                             break
                     print(most_champion_name)
                     print(most_champion_points)

                     embed = discord.Embed(title="", description="", color=0xEB459F)
                     embed.set_author(name=닉네임) +"님의 전적 검색", URL_GG=f"https://lol.ps/summoner/{닉네임}_{태그}", URL_icon="https://ddragon.leagueoflegends.com/cdn/15.9.1/img/profileicon/"Icon"+.png"
                     embed.add_field(name=tier+" "+rank+" | "+leaguepoints+" LP", vlaue=wins+"승"+" "+losses +"패"+" | "+ratio+"%", inline=False)
                     embed.add_field(name="가장 높은 숙련도",value= most_champion_name +" "+ most_champion_points +" 점", inline=False)
                     embed.set_footer(text='Gkwns_GG')
                     await interaction.response.send_message(embed=embed)
                     break
     else:
         await interaction.response.send_message("소환사가 존재하지 않습니다.")

                                                
bot.run(Token) 