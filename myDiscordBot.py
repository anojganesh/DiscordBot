
#Values
#Application ID: *Omitted*
#Public Key: *Omitted*
#Bot Token: *Omitted*
#Invite Link: https://discord.com/api/oauth2/authorize?client_id=1141267102485987410&permissions=1101659139266&scope=bot
#General Channel.id: 1141267769334186036
#Bot Updates Channel.id: 1141564136107548775
#Guild.id: 1141267768218492929

import discord
from discord import app_commands
import os
import datetime
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv
import requests
import json
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents = intents)
ctree = app_commands.CommandTree(bot)
clfile = ''
censoredlist = []

load_dotenv()
#fetching api tokens, change .env variable to change token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

TENOR_TOKEN = os.getenv("TENOR_TOKEN")
search_term = ''


#reading censored words file
try:
    clfile = open('censoredwordslist.txt', 'r')
    for line in clfile.readlines():
        censoredlist.append(line.lower().replace("\n",""))
except Exception as e:
    print(e)
    print("Exception occured reading censored word list. Continued without it.")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == "BotSupportServer":
            for channel in guild.channels:
               if channel.name == "bot-updates":
                   await channel.send("Bot is now Online.")
    await ctree.sync()

async def getGifsReturnRandomURL(search_term, TENOR_TOKEN = TENOR_TOKEN, limit = 10):
    responseHTTP = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&limit=%s" % (search_term, TENOR_TOKEN, limit)) 
    if responseHTTP.status_code == 200:
        top_gifs = json.loads(responseHTTP.content)
        total_urls = len(top_gifs['results'])
        random_index = random.randint(0, total_urls - 1)
        random_url = top_gifs['results'][random_index]['media_formats']['gif']['url']
        return random_url
    else:
        print("Something went wrong getting GIFs: Status_Code " + str(responseHTTP.status_code))
        return None
    

#Wave command
@ctree.command(name = "wave", description = "Send a wave!")
async def appCommandA(interaction):
    gif_link = await getGifsReturnRandomURL('cartoon waving', TENOR_TOKEN)
    await interaction.response.send_message(gif_link)

#Laugh command
@ctree.command(name="laugh", description = 'Send a laugh!')
async def appCommandB(interaction): 
    gif_link = await getGifsReturnRandomURL('cartoon laugh', TENOR_TOKEN)
    await interaction.response.send_message(gif_link)

#Custom gif command
@ctree.command(name = "gif", description = "Send a custom GIF!")
@app_commands.describe(search_term = "What GIF would you like to send?")
async def appCommandC(interaction, search_term : str):
    gif_link = await getGifsReturnRandomURL(search_term, TENOR_TOKEN)
    await interaction.response.send_message(gif_link)

@bot.event
async def on_disconnect():
    print("bot disconnected")
    
@bot.event
async def on_message(message):
    if message.author.bot == False:
        smessage = message.content.lower().replace(" ", "")
        if smessage.find("hello") != -1:
            await message.channel.send("hello!")
            

        elif smessage in ["disconnectbot", "botdisconnect", "terminate", "disconnect"]:
            for guild in bot.guilds:
                if guild.name == "BotSupportServer":
                    for channel in guild.channels:
                        if channel.name == "bot-updates":
                            await channel.send("Bot is now Offline.")
            await bot.close()
        
        elif len(message.stickers) > 0:
            for sticker in message.stickers:
                print("sending")
                await message.channel.send(stickers = message.stickers)
        else:
            for badword in censoredlist:
                if badword in smessage:
                    if message.author.display_name == "Hypnotize Candy":
                        await message.reply("bad boy dominic!"+ " (<@" + str(message.author.id) + ">)")
                        await message.delete(delay = 0)
                        await message.author.timeout(datetime.timedelta(seconds=22), reason='Bad Language!')
                        break

                    else:
                        await message.reply("\**Message Redacted\**" + " (<@" + str(message.author.id) + ">)")
                        await message.delete(delay = 0)
                        if message.author.guild_permissions.administrator == False: #Owner ID, Admins can not get timed out (discord rule)
                            await message.author.timeout(datetime.timedelta(seconds=22), reason='Bad Language!') #Seems to have a constant loss of ~7s so 22-15 = timeout for 15 seconds
                        break
    else:
        print("Bot Response: " + message.content)
        if "https://" in message.content: #Longer deletion timer for gifs
            await message.delete(delay = 10)
        else:
            await message.delete(delay = 5)
        
        
bot.run(DISCORD_TOKEN)
