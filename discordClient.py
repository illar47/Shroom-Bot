import discord
import os
from pathlib import Path
from discord.ext import commands

import holdificatorControlCenter as hcc
import holdificators as h

#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True
clientErrorStr = "<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465>"

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

    #check if item exists
    if item: 
        print(item)
        #format accordingly
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            url=item.link,
            #description=item.properties, 
            title= itemName
        )
        embed.add_field(name = "", value=item.properties, inline=False)
        embed.add_field(name="Item Type:", value=item.itemType, inline=True)
        embed.add_field(name="Rarity:", value=item.rarity, inline=True)
        embed.add_field(name="Must Attune:", value=item.reqAttunement, inline=True)
        

        #aggressive mutations to account for space and any item types that have "item" in them
        itemFilename:str = item.itemType
        itemFilename= ''.join(itemFilename.split()).lower()
        itemFilename = itemFilename.replace("item", "")
        itemFilename = os.getcwd() + "\\itemTypeIcons\\" + itemFilename + "ItemIcon.png"

        #TODO - check that image exists
        filepath = Path(itemFilename)
        if filepath.is_file():
            itemFile = discord.File(itemFilename, filename="itemImage.png")
            embed.set_image(url="attachment://itemImage.png")
            #embed.set_thumbnail(url="attachment://itemImage.png")
            await ctx.send(file=itemFile, embed=embed)
        else: 
            #error message
            await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Something went wrong with fetching the item type")  
    else: 
         await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Sorry the item you have requested doesn't exist. Please try again")

#Commands - use discord embeds for these
#Get Random Item (with params)
#Get Specific item (param: item name)
#Get Random NPC
#Get Random Location / Quest
#Add Item / NPC / Location Data
#Remove Item /NPC / Location Data

#TODO: Find way to specify what channel to send messages in.