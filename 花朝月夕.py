import discord
from discord.ext import commands
from 花朝月夕_Token import Token
#from 花朝月夕_command import cmd

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

@bot.command()
async def 큐브(ctx):
    embed = discord.Embed(title='명령어',
                          description='명령어는 !를 통해 사용합니다.', 
                          colour=0xEB459E)
    embed.add_field(name='>니케', value='!니케이름 + 큐브\r\ex.!크라운 큐브')
    
    await ctx.channel.send(embed=embed)
bot.run(Token)