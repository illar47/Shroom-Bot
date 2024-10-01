import discord
from discord.ext import commands

import holdificatorControlCenter as hcc

#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='./', intents=intents)

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client)) #TODO make actual log message

@client.command(name="ping", help= "Test command for ensuring the bot is functioning as intended. Will respond with pong")
async def ping(ctx):
    await ctx.send('Pong!')

#Get Specific Item
@client.command(name="grabItem", help="Returns information about specified item.")
async def grabItem(ctx, itemName): #need checking for argument that has spaces.
    #check bag of Hoarding for Item
    toOutput = hcc.controlCenter.findItem(itemName)
    print(toOutput)
    #format accordingly
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(137, 204, 185), 
        description="Testing if this even works", 
        title= itemName
    )
    await ctx.send(embed=embed)

#Commands - use discord embeds for these
#Get Random Item (with params)
#Get Specific item (param: item name)
#Get Random NPC
#Get Random Location / Quest
#Add Item / NPC / Location Data
#Remove Item /NPC / Location Data