import discord
from discord.ext import commands
import json #寫好設定檔 防止token被盜
import random
import os
import datetime

import requests
import asyncio

import keep_alive


#開啟json檔案 用jdata把它存起來
with open('setting.json', 'r', encoding='utf8') as jfile:  #讀取json設定檔
    jdata = json.load(jfile)


bot = commands.Bot(command_prefix='.', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)  #bot 代表機器人 prefix = 命令字首，要有這個prefix才能命令機器人


news_api_key = '2557e419edd64bcc868213207d54d895'
news_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
news_sources = ['abc-news', 'associated-press', 'bbc-news', 'cnn', 'fox-news', 'reuters', 'the-new-york-times']


#機器上線會通知
@bot.event # @ = 裝飾器  
async def on_ready():  #async 協成應用函式
    print(">> Bot is online <<")
    await post_news()

async def post_news():
    channel = bot.get_channel(int(jdata['every_news']))
    news_items = []
    for category in news_categories:
        url = 'https://newsapi.org/v2/top-headlines?country=us&category={0}&pageSize=5&apiKey={1}'.format(category, news_api_key)
        response = requests.get(url)
        news_data = json.loads(response.text)
        news_items += news_data['articles']
    random.shuffle(news_items)
    for i in range(10):
        if i < len(news_items):
            news_item = news_items[i]
            title = news_item['title']
            description = news_item['description']
            url = news_item['url']
            source = news_item['source']['name']
            embed = discord.Embed(title=title, description=description, url=url)
            embed.set_author(name=source)
            await channel.send(embed=embed)
    await asyncio.sleep(24 * 60 * 60)  # Wait for 24 hours
    await post_news()







#member加入會通知
@bot.event
async def on_member_join(member): #join
    channel = bot.get_channel(int(jdata["welcome_channel"]))
    await channel.send(F'{member} join!')


#member離開會通知
@bot.event
async def on_member_remove(member): # remove
    channel = bot.get_channel(int(jdata["leave_channel" ]))
    await channel.send(F'{member} leave!')

#輸入ping指令回傳機器延遲時間
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} (ms)')


#隨機傳照片
@bot.command()
async def pic(ctx):
    random_pic = random.choice(jdata['pic'])
    pic = discord.File(random_pic)
    await ctx.send(file = pic)


#網路上的embed  => discord embed generator
@bot.command()
async def em(ctx):
    embed=discord.Embed(title="News_bot", url="https://github.com/Tomlord1122/DiscordBot_NEWS", description="This robot can send ten news everyday to the chatroom. ", timestamp=datetime.datetime.now())
    embed.set_author(name="Tom Liu",url="https://github.com/Tomlord1122",icon_url="https://i.imgur.com/gi1ylT6.jpg")
    embed.set_thumbnail(url="https://i.imgur.com/5AAIb0l.png")
    embed.add_field(name="1", value="5", inline=False)
    embed.add_field(name="2", value="6", inline=False)
    embed.add_field(name="3", value="7", inline=False)
    embed.add_field(name="4", value="8", inline=False)
    await ctx.send(embed=embed)



keep_alive.keep_alive()
bot.run(jdata["TOKEN"])  #放token並啟動




