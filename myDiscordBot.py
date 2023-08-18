
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

os.chdir(os.path.dirname(os.path.abspath(__file__)))
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents = intents)
ctree = app_commands.CommandTree(bot)
clfile = ''
censoredlist = []

load_dotenv()
#fetching api token, change .env variable to change token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


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

    print("bot online")

#Wave command
@ctree.command(name = "wave", description = "Send a wave!")
async def appCommandA(interaction):
    await interaction.response.send_message("\**waves*\*")
    

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
        print(message.content)
        if message.content != "\**waves*\*": #To be changed
            await message.delete(delay = 5)
        
                    
bot.run(DISCORD_TOKEN)
