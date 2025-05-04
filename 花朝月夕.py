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
from 花朝月夕_Subscribers import save_subscribers, load_subscribers

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
headers_lol = {"X-Riot-Token":RToken}
headers_chzzk = {'User-Agent': 'Mozilla/5.0'}
SahYang_User = '5f800579267362c952f76f3c6fe695b2'
URL_SahYang = f"https://api.chzzk.naver.com/service/v1/channels/{SahYang_User}"
subscribers_users = set()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd)
    await bot.change_presence(activity=discord.Game(name='업데이트'))
    await bot.wait_until_ready()
    await bot.tree.sync()
    global subscribers_users
    subscribers_users = load_subscribers()
    print(f'花朝月夕 enabled. Subscribers: {len(subscribers_users)}')
    bot.loop.create_task(checking())
                
@bot.tree.command(name="채널", description="전용 채팅 채널을 생성합니다.")
async def slash(interaction: discord.Interaction):
    await interaction.guild.create_text_channel(name="花朝月夕")
    await interaction.response.send_message("채널을 생성했습니다.", ephemeral=True)

@bot.tree.command(name="랭크", description="닉네임과 태그를 정확하게 입력해주세요.")
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
                     #print(most_champion_name)
                     #print(most_champion_points)

                     embed = discord.Embed(title="", description="", color=0xEB459F)
                     embed.set_author(name=닉네임 +"님의 랭크 정보", url=f"https://lol.ps/summoner/{닉네임}_{태그}?region=kr", icon_url="https://ddragon.leagueoflegends.com/cdn/15.9.1/img/profileicon/"+Icon+".png")
                     embed.add_field(name=tier+" "+rank+" | "+leaguepoints+" LP", value=wins+"승"+" "+losses +"패"+" | "+ratio+"%", inline=False)
                     embed.add_field(name="최고 숙련도",value= most_champion_name +" "+ most_champion_points +" 점", inline=False)
                     embed.set_footer(text='lol.ps')
                     await interaction.response.send_message(embed=embed)
                     break
     else:
         await interaction.response.send_message("소환사가 존재하지 않습니다.")

@bot.tree.command(name="방송_알림_활성화", description="방송 알림을 메시지로 받아요.")
async def slash2(interaction: discord.Interaction):
    subscribers_users.add(interaction.user.id)
    save_subscribers(subscribers_users)
    await interaction.response.send_message("방송 알림을 활성화했습니다.", ephemeral=True)

@bot.tree.command(name="방송_알림_비활성화", description="방송 알림을 메시지로 받지 않아요.")
async def slash3(interaction: discord.Interaction):
    if interaction.user.id in subscribers_users:
        subscribers_users.remove(interaction.user.id)
        save_subscribers(subscribers_users)
        await interaction.response.send_message("방송 알림을 비활성화했습니다.", ephemeral=True)
    else:
        await interaction.response.send_message("방송 알림이 활성화되어있지 않습니다.", ephemeral=True)

async def checking():
    await bot.wait_until_ready()
    last_check = 0
    while not bot.is_closed():
        try:
            r = requests.get(URL_SahYang, headers=headers_chzzk)
            check = 1 if r.json()['content']['openLive'] else 0
        except Exception as e:
            print(f"API 오류: {e}")
            await asyncio.sleep(10)
            continue
        if check != last_check and check == 1:
            for user_id in subscribers_users:
                user = await bot.fetch_user(user_id)
                try:
                    await user.send("금사향님의 방송이 시작됐습니다.")
                except Exception as e:
                    print(f"{user_id} DM 실패: {e}")
        last_check = check
        await asyncio.sleep(3)


bot.run(Token)