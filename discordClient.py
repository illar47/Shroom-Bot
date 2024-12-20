import discord
import os
from pathlib import Path
from discord.ext import commands

import holdificatorControlCenter as hcc
import holdificators as h

intents = discord.Intents.default()
intents.message_content = True
clientErrorStr = "<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465>"

client = commands.Bot(command_prefix='./', intents=intents)
def embedFormatter(p_holderItem): 
    #TODO: formats an embed given a holdificator item and returns the embed - returns something else if failed
    #can differentiate beteen holder types
    if isinstance(p_holderItem, h.BagOfHoardingItem):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            url=p_holderItem.link,
            #description=item.properties, 
            title= p_holderItem.name
        )
        embed.add_field(name = "", value=p_holderItem.properties, inline=False)
        embed.add_field(name="Item Type:", value=p_holderItem.itemType, inline=True)
        embed.add_field(name="Rarity:", value=p_holderItem.rarity, inline=True)
        embed.add_field(name="Must Attune:", value=p_holderItem.reqAttunement, inline=True)

         #aggressive mutations to account for space and any item types that have "item" in them
        itemFilename:str = p_holderItem.itemType
        itemFilename= ''.join(itemFilename.split()).lower()
        itemFilename = itemFilename.replace("item", "")
        itemFilename = os.getcwd() + "\\itemTypeIcons\\" + itemFilename + "ItemIcon.png"

        #check that image exists
        filepath = Path(itemFilename)
        itemFile = None
        if filepath.is_file():
            itemFile = discord.File(itemFilename, filename="itemImage.png")
            embed.set_thumbnail(url="attachment://itemImage.png")

        return embed, itemFile

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client)) #TODO make actual log message

@client.command(name="ping", help= "Test command for ensuring the bot is functioning as intended. Will respond with pong")
async def ping(ctx):
    await ctx.send('Pong!')

#Get Specific Item
@client.command(name="grabItem", help="Returns information about specified item.")
async def grabItem(ctx, p_itemName=None): 
    #check bag of Hoarding for Item
    item:h.BagOfHoardingItem = hcc.controlCenter.findItem(p_itemName)
    #TODO: return an error message if no item name provided
    #check if item exists
    if item and p_itemName: 
        embed, itemFile = embedFormatter(item)
        if itemFile:
            await ctx.send(file=itemFile, embed=embed)
        else:
            await ctx.send(embed=embed)
    else: 
         await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Sorry the item you have requested doesn't exist. Please try again")

#Commands - use discord embeds for these
#Get Random Item (with params)
@client.command(name="grabRandomItem", help="Grabs a random item that meets the parameters expectations")
async def grabRandomItem(ctx, p_level=None, p_rarity=None, p_character=None): 
    item:h.BagOfHoardingItem = hcc.controlCenter.pickRandomItem(p_level, p_rarity, p_character)
    #maybe instead asks for params from user one at a time?
    
    #check if item exists
    if item: 
        embed, itemFile = embedFormatter(item)
        if itemFile:
            await ctx.send(file=itemFile, embed=embed)
        else:
            await ctx.send(embed=embed)
    else: 
         await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Sorry an error occured. Please try again momentarily")
    #abitrarily select item until one with matching specs appears
    #cred embed and send it

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

#### TEST LAND ####
@client.command(name="testOptionalParams", help="debugging method for optional parameters")
async def testOptionalParams(ctx, *args): 
    print("testing")
    print(args)
    print("done")
    #await ctx.send(f'You passed {arg1} and {arg2}')
    #need list of dictionary values that could autofill