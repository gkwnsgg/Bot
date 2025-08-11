import discord
import requests
import asyncio
import time
import aiohttp
import json
import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from discord import app_commands, File
from discord.ext import commands
from tabulate import tabulate
from Sah_Yang_image import save_sah_df_img
from Sah_Yang_Schedule import Sah_filtered_dataframe
from 花朝月夕_Token import Token, RToken, YToken, SahYang_User, chyeonz_User, leechunhyang_User, ao_o5_User, SahYang_Youtube
from 花朝月夕_Subscribers import save_Ssubcribers, load_Ssubcribers, save_CHsubcribers, load_CHsubcribers, save_cz_subcribers, load_cz_subcribers, save_ao_subcribers, load_ao_subcribers, save_SYsubcribers, load_SYsubcribers
from 花朝月夕_URL import URL_SahYang, URL_SahYang0, URL_leechunhyang, URL_leechunhyang0, URL_chyeonz_, URL_chyeonz0, URL_ao_05, URL_ao_050, URL_Notion, URL_Notion1
from 花朝月夕_Youtube import Sah_save_last_video_id, Sah_load_last_video_id

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
headers_lol = {"X-Riot-Token":RToken}
headers_chzzk = {'User-Agent': 'Mozilla/5.0'}
youtube = build('youtube', 'v3', developerKey=YToken)
Ssubscribers_users = set()

SahYang_task_started = False
leechunhyang_task_started = False
chyeonz_task_started = False
ao_o5_task_started = False
Sah_Yang_new_video_task_started = False

def log_error(context, error):
    with open("sahyang_error.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] [{context}] {str(error)}\n")

def get_status_message(bot):
    server_count = len(bot.guilds)

    subs_files = [
        'ao_o5.subs.json',
        'chyeonz_.subs.json',
        'leechunhyang.subs.json',
        'Sah_Yang.subs.json',
        'Sah_Yang_Ysubs.json'
    ]

    user_ids = set()
    for file_name in subs_files:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                user_ids.update(data)
        except Exception as e:
            print(f"{file_name} 읽기 중 오류 발생: {e}")

    user_count = len(user_ids)
    return f"{server_count}개의 서버에서 {user_count}명의 유저가 사용중"

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    status_message = get_status_message(bot)
    await bot.change_presence(activity=discord.CustomActivity(name=status_message))
    await bot.tree.sync()
    global Ssubscribers_users
    global Csubscribers_users
    global z_subscribers_users
    global ao_subscribers_users
    global SYsubscribers_users
    Ssubscribers_users = load_Ssubcribers()
    Csubscribers_users = load_CHsubcribers()
    z_subscribers_users = load_cz_subcribers()
    ao_subscribers_users = load_ao_subcribers()
    SYsubscribers_users = load_SYsubcribers()
    print(f'花朝月夕 enabled.')
    global SahYang_task_started
    if not SahYang_task_started:
        bot.loop.create_task(checking_SahYang())
        SahYang_task_started = True
    global leechunhyang_task_started
    if not leechunhyang_task_started:
        bot.loop.create_task(checking_leechunhyang())
        leechunhyang_task_started = True
    global chyeonz_task_started
    if not chyeonz_task_started:
        bot.loop.create_task(checking_chyeonz_())
        chyeonz_task_started = True
    global ao_o5_task_started
    if not ao_o5_task_started:
        bot.loop.create_task(checking_ao_o5())
        ao_o5_task_started = True
    global Sah_Yang_new_video_task_started
    if not Sah_Yang_new_video_task_started:
        bot.loop.create_task(Sah_Yang_new_video())
        Sah_Yang_new_video_task_started = True

@bot.command()
async def 패치노트(ctx):
    embed = discord.Embed(
        title="패치 노트",
        description="[Notion으로 이동합니다.]", url=(URL_Notion),
        color=discord.Color.dark_red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def 정보(ctx):
    embed = discord.Embed(
        title="정보",
        description="[Notion으로 이동합니다.]", url=(URL_Notion1),
        color=discord.Color.dark_red()
    )
    await ctx.send(embed=embed)

@bot.tree.command(name="채널", description="전용 채팅 채널을 생성합니다.")
async def slash(interaction: discord.Interaction):
    await interaction.guild.create_text_channel(name="花朝月夕")
    await interaction.response.send_message("채널을 생성했습니다.", ephemeral=True)

@bot.tree.command(name="랭크", description="닉네임과 태그를 정확하게 입력해주세요.")
async def slash1(interaction: discord.Interaction, 닉네임:str, 태그:str):
     URL_puuid = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{닉네임}/{태그}?api_key={RToken}"
     r = requests.get(URL_puuid,headers=headers_lol)
     Puuid = (r.json()['puuid'])
     if r.status_code == 200:
         URL_summoner = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{Puuid}?api_key={RToken}"
         r = requests.get(URL_summoner, headers=headers_lol)
         Icon = str(r.json()['profileIconId'])
         Level = str(r.json()['summonerLevel'])
         URL_league = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{Puuid}?api_key={RToken}"
         r = requests.get(URL_league, headers=headers_lol)
         RankS = json.loads(r.text)
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
                 URL_champion = f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{Puuid}?api_key={RToken}"
                 r = requests.get(URL_champion, headers=headers_lol)
                 player_mastery = json.loads(r.text)
                 for i in player_mastery:
                     most_champion_id = int(i["championId"])
                     most_champion_points = str(i["championPoints"])
                     URL_ddragon1 = f"https://ddragon.leagueoflegends.com/cdn/15.10.1/data/ko_KR/champion.json"
                     r = requests.get(URL_ddragon1)
                     champion_name = json.loads(r.text)
                     champion_name_list = champion_name["data"]
                     global most_champion_name
                     for i in champion_name_list:
                         if(champion_name["data"][i]["key"])==str(most_champion_id):
                             most_champion_name = champion_name["data"][i]["name"]
                             break
                     embed = discord.Embed(title="", description="", color=0xEB459F)
                     embed.set_author(name=닉네임 +"님의 랭크 정보", url=f"https://lol.ps/summoner/{닉네임}_{태그}?region=kr", icon_url="https://ddragon.leagueoflegends.com/cdn/15.10.1/img/profileicon/"+Icon+".png")
                     embed.add_field(name=tier+" "+rank+" | "+leaguepoints+" LP", value=wins+"승"+" "+losses +"패"+" | "+ratio+"%", inline=False)
                     embed.add_field(name="최고 숙련도",value= most_champion_name +" "+ most_champion_points +" 점", inline=False)
                     embed.set_footer(text='lol.ps')
                     await interaction.response.send_message(embed=embed)
                     break
     else:
         await interaction.response.send_message("소환사가 존재하지 않습니다.")

@bot.tree.command(name="금사향_방송_알림_활성화", description="방송 알림을 메시지로 받아요.")
async def slash2(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    Ssubscribers_users.add(interaction.user.id)
    save_Ssubcribers(Ssubscribers_users)
    await interaction.followup.send("방송 알림을 활성화했습니다.", ephemeral=True)

@bot.tree.command(name="금사향_방송_알림_비활성화", description="방송 알림을 메시지로 받지 않아요.")
async def slash3(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id in Ssubscribers_users:
        Ssubscribers_users.remove(interaction.user.id)
        save_Ssubcribers(Ssubscribers_users)
        await interaction.followup.send("방송 알림을 비활성화했습니다.", ephemeral=True)
    else:
        await interaction.followup.send("방송 알림이 활성화되어있지 않습니다.", ephemeral=True)

@bot.tree.command(name="채현찌_방송_알림_활성화", description="방송 알림을 메시지로 받아요.")
async def slash4(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    z_subscribers_users.add(interaction.user.id)
    save_cz_subcribers(z_subscribers_users)
    await interaction.followup.send("방송 알림을 활성화했습니다.", ephemeral=True)

@bot.tree.command(name="채현찌_방송_알림_비활성화", description="방송 알림을 메시지로 받지 않아요.")
async def slash5(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id in z_subscribers_users:
        z_subscribers_users.remove(interaction.user.id)
        save_cz_subcribers(z_subscribers_users)
        await interaction.followup.send("방송 알림을 비활성화했습니다.", ephemeral=True)
    else:
        await interaction.followup.send("방송 알림이 활성화되어있지 않습니다.", ephemeral=True)

@bot.tree.command(name="이춘향_방송_알림_활성화", description="방송 알림을 메시지로 받아요.")
async def slash6(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    Csubscribers_users.add(interaction.user.id)
    save_CHsubcribers(Csubscribers_users)
    await interaction.followup.send("방송 알림을 활성화했습니다.", ephemeral=True)

@bot.tree.command(name="이춘향_방송_알림_비활성화", description="방송 알림을 메시지로 받지 않아요.")
async def slash7(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id in Csubscribers_users:
        Csubscribers_users.remove(interaction.user.id)
        save_CHsubcribers(Csubscribers_users)
        await interaction.followup.send("방송 알림을 비활성화했습니다.", ephemeral=True)
    else:
        await interaction.followup.send("방송 알림이 활성화되어있지 않습니다.", ephemeral=True)

@bot.tree.command(name="임나은_방송_알림_활성화", description="방송 알림을 메시지로 받아요.")
async def slash8(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    ao_subscribers_users.add(interaction.user.id)
    save_ao_subcribers(ao_subscribers_users)
    await interaction.followup.send("방송 알림을 활성화했습니다.", ephemeral=True)

@bot.tree.command(name="임나은_방송_알림_비활성화", description="방송 알림을 메시지로 받지 않아요.")
async def slash7(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id in ao_subscribers_users:
        ao_subscribers_users.remove(interaction.user.id)
        save_ao_subcribers(ao_subscribers_users)
        await interaction.followup.send("방송 알림을 비활성화했습니다.", ephemeral=True)
    else:
        await interaction.followup.send("방송 알림이 활성화되어있지 않습니다.", ephemeral=True)

@bot.tree.command(name="금사향_방송_일정", description="이번달의 방송 일정을 알려줄게요.")
async def slash8(interaction: discord.Interaction):
    await interaction.response.defer()
    df = Sah_filtered_dataframe()
    save_sah_df_img(df, filename="2508schedule.png", background_image="1747197564.219887.PNG")
    await interaction.followup.send(file=File("2508schedule.png"))

@bot.tree.command(name="금사향_유튜브_알림_활성화", description="유튜브 새 영상 알림을 메시지로 받아요.")
async def slash9(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    SYsubscribers_users.add(interaction.user.id)
    save_SYsubcribers(SYsubscribers_users)
    await interaction.followup.send("유튜브 새 영상 알림을 활성화했습니다.", ephemeral=True)

@bot.tree.command(name="금사향_유튜브_알림_비활성화", description="유튜브 새 영상 알림을 메시지로 받지 않아요.")
async def slash10(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id in SYsubscribers_users:
        SYsubscribers_users.remove(interaction.user.id)
        save_SYsubcribers(SYsubscribers_users)
        await interaction.followup.send("유튜브 새 영상 알림을 비활성화했습니다.", ephemeral=True)
    else:
        await interaction.followup.send("유튜브 알림이 활성화되어있지 않습니다.", ephemeral=True)

last_check_SahYang = 0
MAX_CONCURRENT_SENDS = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_SENDS)
async def send_sahyang_dm(user_id, embed):
    async with semaphore:
        try:
            user_obj = await bot.fetch_user(user_id)
            await user_obj.send(embed=embed)
        except Exception as e:
            error_message = f"{user_id} 금사향 DM 실패: {e}"
            print(error_message)
            log_error("send_sahyang_dm", error_message)
async def checking_SahYang():
    global last_check_SahYang
    await bot.wait_until_ready()
    last_check_SahYang = 0

    async with aiohttp.ClientSession(headers=headers_chzzk) as session:
        while not bot.is_closed():
            try:
                async with session.get(URL_SahYang) as resp:
                    data = await resp.json()
                content = data.get("content", {})
                check = 1 if content.get("openLive") else 0

                if check != last_check_SahYang:
                    if check == 1:
                        try:
                            async with session.get(URL_SahYang0) as resp:
                                data = await resp.json()
                                Title = data.get('content', {}).get('liveTitle', '제목 없음')
                                live_url = f"https://chzzk.naver.com/live/{SahYang_User}"
                            embed = discord.Embed(
                                title="금사향님의 방송이 시작됐습니다.",
                                description=f"**{Title}**\n[방송 보러가기]({live_url})",
                                color=discord.Color.yellow()
                            )
                            embed.set_footer(text="ㅇㅇㄴ! ㅇㅇㄴ!")
                            embed.timestamp = discord.utils.utcnow()

                            tasks = [send_sahyang_dm(user_id, embed) for user_id in Ssubscribers_users]
                            await asyncio.gather(*tasks)

                        except Exception as e:
                            log_error("Embed 전송 오류", e)

                    last_check_SahYang = check

            except Exception as e:
                log_error("금사향 API 오류", e)

            await asyncio.sleep(30)

last_check_leechunhyang = 0
async def checking_leechunhyang():
    global last_check_leechunhyang
    await bot.wait_until_ready()
    last_check_leechunhyang = 0
    async with aiohttp.ClientSession(headers=headers_chzzk) as session:
        while not bot.is_closed():
            try:
                async with session.get(URL_leechunhyang) as resp:
                    data = await resp.json()
                content = data.get("content", {})
                check = 1 if content.get("openLive") else 0
            
                if check != last_check_leechunhyang:
                    if check == 1:
                        try:
                            async with session.get(URL_leechunhyang0) as resp:
                                data = await resp.json()
                                Title = data.get('content', {}).get('liveTitle', '제목 없음')
                                live_url = f"https://chzzk.naver.com/live/{leechunhyang_User}"
                            embed = discord.Embed(
                                title="이춘향님의 방송이 시작됐습니다.",
                                description=f"**{Title}**\n[방송 보러가기]({live_url})",
                                color=discord.Color.yellow()
                            )
                            embed.set_footer(text="花朝月夕")
                            embed.timestamp = discord.utils.utcnow()
                            for user_id in Csubscribers_users:
                                try:
                                    user_obj = await bot.fetch_user(user_id)
                                    await user_obj.send(embed=embed)
                                    await asyncio.sleep(1)
                                except Exception as e:
                                    print(f"{user_id} 이춘향 DM 실패: {e}")
                        except Exception as e:
                            print(f"{user_id} 이춘향 Embed 오류: {e}")
                    else:
                        pass                    
                    
                    
                    last_check_leechunhyang = check
            except Exception as e:
                print(f"이춘향 API 오류: {e}")
            await asyncio.sleep(30)

last_check_chyeonz_ = 0
async def checking_chyeonz_():
    global last_check_chyeonz_
    await bot.wait_until_ready()
    last_check_chyeonz_ = 0
    async with aiohttp.ClientSession(headers=headers_chzzk) as session:
        while not bot.is_closed():
            try:
                async with session.get(URL_chyeonz_) as resp:
                    data = await resp.json()
                content = data.get("content", {})
                check = 1 if content.get("openLive") else 0
            
                if check != last_check_chyeonz_:
                    if check == 1:
                        try:
                            async with session.get(URL_chyeonz0) as resp:
                                data = await resp.json()
                                Title = data.get('content', {}).get('liveTitle', '제목 없음')
                                live_url = f"https://chzzk.naver.com/live/{chyeonz_User}"
                            embed = discord.Embed(
                                title="채현찌님의 방송이 시작됐습니다.",
                                description=f"**{Title}**\n[방송 보러가기]({live_url})",
                                color=discord.Color.yellow()
                            )
                            embed.set_footer(text="花朝月夕")
                            embed.timestamp = discord.utils.utcnow()
                            for user_id in z_subscribers_users:
                                try:
                                    user_obj = await bot.fetch_user(user_id)
                                    await user_obj.send(embed=embed)
                                    await asyncio.sleep(1)
                                except Exception as e:
                                    print(f"{user_id} 채현찌 DM 실패: {e}")
                        except Exception as e:
                            print(f"{user_id} 채현찌 Embed 오류: {e}")
                    else:
                        pass                    
                    
                    
                    last_check_chyeonz_ = check
            except Exception as e:
                print(f"채현찌 API 오류: {e}")
            await asyncio.sleep(30)

last_check_ao_o5 = 0
async def checking_ao_o5():
    global last_check_ao_o5
    await bot.wait_until_ready()
    last_check_ao_o5 = 0
    async with aiohttp.ClientSession(headers=headers_chzzk) as session:
        while not bot.is_closed():
            try:
                async with session.get(URL_ao_05) as resp:
                    data = await resp.json()
                content = data.get("content", {})
                check = 1 if content.get("openLive") else 0
            
                if check != last_check_ao_o5:
                    if check == 1:
                        try:
                            async with session.get(URL_ao_050) as resp:
                                data = await resp.json()
                                Title = data.get('content', {}).get('liveTitle', '제목 없음')
                                live_url = f"https://chzzk.naver.com/live/{ao_o5_User}"
                            embed = discord.Embed(
                                title="임나은님의 방송이 시작됐습니다.",
                                description=f"**{Title}**\n[방송 보러가기]({live_url})",
                                color=discord.Color.yellow()
                            )
                            embed.set_footer(text="花朝月夕")
                            embed.timestamp = discord.utils.utcnow()
                            for user_id in ao_subscribers_users:
                                try:
                                    user_obj = await bot.fetch_user(user_id)
                                    await user_obj.send(embed=embed)
                                    await asyncio.sleep(1)
                                except Exception as e:
                                    print(f"{user_id} 임나은 DM 실패: {e}")
                        except Exception as e:
                            print(f"{user_id} 임나은 Embed 오류: {e}")
                    else:
                        pass                    
                    
                    
                    last_check_ao_o5 = check
            except Exception as e:
                print(f"임나은 API 오류: {e}")
            await asyncio.sleep(30)

async def Sah_Yang_new_video():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            channel_response = youtube.channels().list(
                part = "contentDetails",
                id = SahYang_Youtube
            ).execute()
            uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            playlist_response = youtube.playlistItems().list(
                part = "snippet",
                playlistId = uploads_playlist_id,
                maxResults = 1
            ).execute()
            latest_video = playlist_response["items"][0]["snippet"]
            video_id = latest_video["resourceId"]["videoId"]
            title = latest_video["title"]
            thumbnail = latest_video["thumbnails"]["high"]["url"]
            published_at = latest_video["publishedAt"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            last_saved_video_id = Sah_load_last_video_id()           
            if video_id != last_saved_video_id:
                Sah_save_last_video_id(video_id)
                embed = discord.Embed(
                    title = "금사향님의 새 영상이 업로드되었습니다.",
                    description=title,
                    url=video_url,
                    color=discord.Color.red()
                )
                embed.set_image(url=thumbnail)
                embed.set_footer(text="금사향 유튜브 알림")
                for user_id in SYsubscribers_users:
                    try:
                        user_obj = await bot.fetch_user(user_id)
                        await user_obj.send(embed=embed)
                        await asyncio.sleep(1)
                    except Exception as e:
                        print(f"{user_id} 금사향 유튜브 DM 실패: {e}")
            else:
                pass
        except Exception as e:
            print(f"[금사향 에러 발생] {e}")
        await asyncio.sleep(300)

bot.run(Token)
