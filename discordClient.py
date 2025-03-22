import discord
import os
from pathlib import Path
from discord.ext import commands

import holdificatorControlCenter as hcc
import holdificators as h
import tableUtils as util

intents = discord.Intents.default()
intents.message_content = True
clientErrorStr = "<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465>"

client = commands.Bot(command_prefix='./', intents=intents)

#Helper Command - formats an embed to be nice. 
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
    
    if isinstance(p_holderItem, h.encounterItem):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            title= p_holderItem.name
        )
        embed.add_field(name="Encounter Type:", value=p_holderItem.type, inline=True)
        embed.add_field(name="creatures:", value=p_holderItem.creatures, inline=True)
        embed.add_field(name="Description:", value=p_holderItem.description, inline=False)

        #check that image exists
        itemFilename = os.getcwd() + "\\itemTypeIcons\\" + "scroll" + "ItemIcon.png"
        filepath = Path(itemFilename)
        itemFile = None
        if filepath.is_file():
            itemFile = discord.File(itemFilename, filename="itemImage.png")
            embed.set_thumbnail(url="attachment://itemImage.png")

        return embed, itemFile
    if isinstance(p_holderItem, h.NPC):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            title= p_holderItem.name
        )
        embed.add_field(name="Species:", value=p_holderItem.species, inline=True)
        embed.add_field(name="gender:", value=p_holderItem.gender, inline=True)
        embed.add_field(name="Descriptive Trait:", value=p_holderItem.description, inline=True)

        #check that image exists
        itemFilename = os.getcwd() + "\\itemTypeIcons\\" + "armour" + "ItemIcon.png"
        filepath = Path(itemFilename)
        itemFile = None
        if filepath.is_file():
            itemFile = discord.File(itemFilename, filename="itemImage.png")
            embed.set_thumbnail(url="attachment://itemImage.png")

        return embed, itemFile



@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client)) #TODO make actual log message
    await client.tree.sync()

########### Commands - use discord embeds for these ###########

#Test Command - Ping
@client.hybrid_command(name="ping", help= "Test command for ensuring the bot is functioning as intended. Will respond with pong")
async def ping(ctx):
    await ctx.send('Pong!')

#Test Command - testing Optional Params
@client.command(name="testOptionalParams", help="debugging method for optional parameters")
async def testOptionalParams(ctx, *args): 
    print("testing")
    print(args)
    print("done")
    #await ctx.send(f'You passed {arg1} and {arg2}')
    #need list of dictionary values that could autofill

#Item Command - Get Specific Item
@client.hybrid_command(name="grabitem", help="Returns information about specified item.")
async def grabitem(ctx, p_item_name=None): 
    #check bag of Hoarding for Item
    item:h.BagOfHoardingItem = hcc.controlCenter.findItem(p_item_name)
    #TODO: return an error message if no item name provided
    #check if item exists
    if item and p_item_name: 
        embed, itemFile = embedFormatter(item)
        if itemFile:
            await ctx.send(file=itemFile, embed=embed)
        else:
            await ctx.send(embed=embed)
    else: 
         await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Sorry the item you have requested doesn't exist. Please try again")

#Item Command - Get Random Item (with params)
@client.hybrid_command(name="grabrandomitem", help="Grabs a random item that meets the parameters expectations")
async def grabRandomItem(ctx, level=None, rarity=None, character=None): 
    #TODO: check if provided level, rarity, and characters are valid
    if util.checkItemParamValidity(level, rarity, character):
        item:h.BagOfHoardingItem = hcc.controlCenter.pickRandomItem(level, rarity, character)
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
    else:
        await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Invalid Inputs provided. Please try again with different inputs")

#Item Command - sends a requested item to a specified player
@client.hybrid_command(name="reqitem", help="sends requested item to specified player")
async def reqItem(ctx, item_name=None, username=None):
    #check that provided item exists - if no, then error
    #find associated chat for user. send sheet there if exists. 
    #error should be in bot channel, found sheet in character channel. 
    print("TODO")

#Location Command - Get Random Location / Quest
@client.hybrid_command(name="grabrandomencounter", help="Grabs a random encounter that meets the parameters expectations")
async def grabRandomEncounter(ctx, type=None): 
    if util.checkEncounterParamValidity(type):
        encounter:h.encounterItem = hcc.controlCenter.pickRandomEncounter(type)

          #check if item exists
        if encounter: 
            embed, itemFile = embedFormatter(encounter)
            if itemFile:
                await ctx.send(file=itemFile, embed=embed)
            else:
                await ctx.send(embed=embed)
        else: 
            await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Sorry an error occured. Please try again momentarily")
    else:
        await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Invalid Inputs provided. Please try again with different inputs")

#NPC Command - Generate Random NPC
@client.hybrid_command(name="createnpc", help="Generates a Random NPC")
async def createNPC(ctx, species=None, gender=None, description=None):
    npc:h.NPC = hcc.controlCenter.generateNPC(species, gender, description)        
    if npc: 
        embed, itemFile = embedFormatter(npc)
        if itemFile:
            await ctx.send(file=itemFile, embed=embed)
        else:
            await ctx.send(embed=embed)
    else: 
        await ctx.send("<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n Sorry an error occured. Please try again momentarily")
#TODO: Find way to specify what channel to send messages in.
