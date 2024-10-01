import discord
from discord.ext import commands

import holdificatorControlCenter as hcc
import holdificators as h

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
    item:h.BagOfHoardingItem = hcc.controlCenter.findItem(itemName)
    print(item)
    #format accordingly
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(137, 204, 185), 
        url=item.link,
        #description=item.properties, 
        title= itemName
    )
    embed.add_field(name="Item Type", value=item.itemType, inline=True)
    embed.add_field(name="Rarity", value=item.rarity, inline=True)
    embed.add_field(name="Attunement", value=item.reqAttunement, inline=True)
    embed.add_field(name = "Properties", value=item.properties, inline=False)
    await ctx.send(embed=embed)

#Commands - use discord embeds for these
#Get Random Item (with params)
#Get Specific item (param: item name)
#Get Random NPC
#Get Random Location / Quest
#Add Item / NPC / Location Data
#Remove Item /NPC / Location Data

#TODO: Find way to specify what channel to send messages in.