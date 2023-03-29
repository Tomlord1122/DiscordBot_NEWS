import discord
from discord.ext import commands
import json #寫好設定檔 防止token被盜


with open('setting.json', 'r', encoding='utf8') as jfile:  #讀取json設定檔
    jdata = json.load(jfile)


bot = commands.Bot(command_prefix='.', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)  #bot 代表機器人 prefix = 命令字首，要有這個prefix才能命令機器人


@bot.event # @ = 裝飾器  
async def on_ready():  #async 協成應用函式
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata["welcome_channel"]))
    await channel.send(F'{member} join!')
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(jdata["1090560796171448330"]))
    await channel.send(F'{member} leave!')

@bot.command()
async def ping(ctx):
    await ctx.send(F'{round(bot.latency*1000)}(ms)') #回傳bot 的延遲 (ms)







bot.run(jdata["TOKEN"])  #放token並啟動




