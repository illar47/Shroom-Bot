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
def embedFormatter(self, p_holderItem): 
    print("test")
    #TODO: formats an embed given a holdificator item and returns the embed - returns something else if failed
    #can differentiate beteen holder types

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client)) #TODO make actual log message

@client.command(name="ping", help= "Test command for ensuring the bot is functioning as intended. Will respond with pong")
async def ping(ctx):
    await ctx.send('Pong!')

#Get Specific Item
@client.command(name="grabItem", help="Returns information about specified item.")
async def grabItem(ctx, p_itemName): 
    #check bag of Hoarding for Item
    item:h.BagOfHoardingItem = hcc.controlCenter.findItem(p_itemName)

    #check if item exists
    if item: 
        print(item)
        #format accordingly
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            url=item.link,
            #description=item.properties, 
            title= p_itemName
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

        #check that image exists
        filepath = Path(itemFilename)
        if filepath.is_file():
            itemFile = discord.File(itemFilename, filename="itemImage.png")
            embed.set_thumbnail(url="attachment://itemImage.png")
            await ctx.send(file=itemFile, embed=embed)
        else: 
            #error message
            await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Something went wrong with fetching the item type")  
    else: 
         await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Sorry the item you have requested doesn't exist. Please try again")

#Commands - use discord embeds for these
#Get Random Item (with params)
@client.command(name="grabRandomItem", help="Grabs a random item that meets the parameters expectations")
async def grabRandomItem(ctx, p_itemLevel, p_assocChar): 
    print("boopS")

#Get Specific item (param: item name)
#Get Random NPC
#Get Random Location / Quest
#Add Item / NPC / Location Data
#Remove Item /NPC / Location Data

#TODO: Find way to specify what channel to send messages in.

#Accept input


############ IDEATION ###########################

#determine if user is attempting to find a random location, item, or NPC

    #if looking for item:

        #determine identifying information: i.e. level, type (weapon, equipable etc), player tags (who it would suit)

        #output random item that meets the criteria

    #if looking for location

        #determine if specific biome necessary (cave, beach, etc.)

        #output random location that meets the criteria. 

    #if looking for NPC
        #determine identifying information: gender, age, career, etc. 

        #randomly select name from list

        #randomly select remaining information that was not specified by user (gender, age, career etc)

        #maybe bug AI to quickly generate a 2 - 3 sentence character description? 
        
        #output results. 