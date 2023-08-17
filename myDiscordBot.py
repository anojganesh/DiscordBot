
#Values
#Application ID: 1141267102485987410
#Public Key: 9d8fcffefaf9843a7dd0d5603b822ea64801823f9c8bf15e718b390397291f37
#Bot Token: MTE0MTI2NzEwMjQ4NTk4NzQxMA.GTIwW0.hCocZA4oITUtk3MOv3aeFdIs_IrdoDl1bL8og4
#Invite Link: https://discord.com/api/oauth2/authorize?client_id=1141267102485987410&permissions=2048&scope=bot
#General Channel.id: 1141267769334186036
#Bot Updates Channel.id: 1141564136107548775
#Guild.id: 1141267768218492929
import discord
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents = intents)
ctree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == "BotTestingServer":
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
            print(discord.StickerPack)

        elif smessage in ["disconnectbot", "botdisconnect"]:
            for guild in bot.guilds:
                if guild.name == "BotTestingServer":
                    for channel in guild.channels:
                        if channel.name == "bot-updates":
                            await channel.send("Bot is now Offline.")
            await bot.close()
        
bot.run('MTE0MTI2NzEwMjQ4NTk4NzQxMA.GTIwW0.hCocZA4oITUtk3MOv3aeFdIs_IrdoDl1bL8og4')
