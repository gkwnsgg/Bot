import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
TOKEN = 'MTM2NDM4MDc3OTk3ODY5MDc2MA.Gz49O5.wLhOmdYq3z0SueoIb_t9zaK9wbyZZa6flIX6SA'

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lose Control"))
    print('花朝月夕 enabled.')

@bot.event
async def on_message(msg):
    if msg.author.bot: return None
    await bot.process_commands(msg)

bot.run(TOKEN)