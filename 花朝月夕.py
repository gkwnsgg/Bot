import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
TOKEN = 'MTM2NDM4MDc3OTk3ODY5MDc2MA.Gz49O5.wLhOmdYq3z0SueoIb_t9zaK9wbyZZa6flIX6SA'

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
async def 명령어(ctx):
    embed = discord.Embed(title='명령어',
                          description='명령어는 !를 통해 사용합니다.', 
                          colour=0xEB459E)
    embed.add_field(name='>니케', value='!니케이름 + 큐브\r\ex.!크라운 큐브')
    
    await ctx.channel.send(embed=embed)
bot.run(TOKEN)