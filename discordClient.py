import discord
import os
from pathlib import Path
from discord.ext import commands
from typing import Literal, Union

import holdificatorControlCenter as hcc
import holdificators as h
import tableUtils as util

intents = discord.Intents.default()
intents.message_content = True
clientErrorStr = "<:errorIcon:1290854428991033465> **Error Occured** <:errorIcon:1290854428991033465> \n" #error msg
clientInfoStr = "<:infoIcon:1290854447722790963> **Success** <:infoIcon:1290854447722790963> \n" #infoIcon

#collection of player names 
s_players = ["petros", "abearron", "julien", "stormcaller"]

s_allowedItemLevelOptions = Literal["trinket","low", "medium", "high"]
s_allowedItemRarityOptions = Literal["common", "uncommon", "rare", "very rare", "legendary"]

s_allowedEncTypes = Literal["Non-Combat", "Combat"]

client = commands.Bot(command_prefix='s/', intents=intents)

#Helper Command - formats an embed to be nice. 
def embedFormatter(holderItem): 
    #Return an Item
    if isinstance(holderItem, h.BagOfHoardingItem):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            url=holderItem.link,
            #description=item.properties, 
            title= holderItem.name
        )
        embed.add_field(name = "", value=holderItem.properties, inline=False)
        embed.add_field(name="Item Type:", value=holderItem.itemType, inline=True)
        embed.add_field(name="Rarity:", value=holderItem.rarity, inline=True)
        embed.add_field(name="Must Attune:", value=holderItem.reqAttunement, inline=True)
        embed.add_field(name="URL:", value=holderItem.link, inline=False)

         #aggressive mutations to account for space and any item types that have "item" in them
        itemFilename:str = holderItem.itemType
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
    
    #Return an encounter
    if isinstance(holderItem, h.encounterItem):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            title= holderItem.name
        )
        embed.add_field(name="Encounter Type:", value=holderItem.type, inline=True)
        embed.add_field(name="creatures:", value=holderItem.creatures, inline=True)
        embed.add_field(name="Description:", value=holderItem.description, inline=False)

        #check that image exists
        itemFilename = os.getcwd() + "\\itemTypeIcons\\" + "scroll" + "ItemIcon.png"
        filepath = Path(itemFilename)
        itemFile = None
        if filepath.is_file():
            itemFile = discord.File(itemFilename, filename="itemImage.png")
            embed.set_thumbnail(url="attachment://itemImage.png")

        return embed, itemFile
    
    #Return an NPC
    if isinstance(holderItem, h.NPC):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            title= holderItem.name
        )
        embed.add_field(name="Species:", value=holderItem.species, inline=True)
        embed.add_field(name="gender:", value=holderItem.gender, inline=True)
        embed.add_field(name="Descriptive Trait:", value=holderItem.description, inline=True)

        #check that image exists
        itemFilename = os.getcwd() + "\\itemTypeIcons\\" + "armour" + "ItemIcon.png"
        filepath = Path(itemFilename)
        itemFile = None
        if filepath.is_file():
            itemFile = discord.File(itemFilename, filename="itemImage.png")
            embed.set_thumbnail(url="attachment://itemImage.png")

        return embed, itemFile
    
    #Somehow we're requesting an embed format that DNE
    else: 
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            title= "You Done Fucked Up"
        )
        embed.add_field(name="Seriously:", value="How the hell did you get this message? Fix your code", inline=True)
        return embed

def playerUpdateMessage():
    print("Player List Updated:")
    for player in s_players:
        print("Player Name: " + player)

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
    await client.tree.sync()

########### Commands - use discord embeds for these ###########

#### TEST COMMANDS ####

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

#### UTILITY COMMANDS ####

#Util - add a new player to campaign
@client.hybrid_command(name="player-add", help="Allows user to add a new player to campaign")
async def addNewPlayer(ctx, new_player_name):
    if (new_player_name in s_players):
        await ctx.send(clientErrorStr + "That User Already Exists. Please run player-update instead.")
    else:
        s_players.append(new_player_name); 
        #TODO: find a better place to store like the database instead of in the code under s_players

        playerUpdateMessage()
        await ctx.send(clientInfoStr + " New Player **" + new_player_name +"** added " + clientInfoStr)

@client.hybrid_command(name="player-remove", help="Allows user to remove player from campaign")
async def removePlayer(ctx, player_name:str): 
    if (player_name in s_players):
        s_players.remove(player_name)
        playerUpdateMessage()
        await ctx.send(clientInfoStr + "Player **" + player_name + "** has been removed from the campaign. " + clientInfoStr) 
    else:
        await ctx.send(clientErrorStr + "That User Doesn't exist... Git Gud ig?")

@client.hybrid_command(name="player-getall", help="outputs a list of active players and their associated channel")
async def getPlayerList(ctx): 
    print ("Getting Player Table... ")
    embed = discord.Embed(
            colour=discord.Colour.from_rgb(137, 204, 185), 
            title= "The All Knowing Player Table"
        )
    embed.add_field(name="Player Name", value="", inline=True)
    embed.add_field(name= "", value="", inline=True)
    embed.add_field(name="Channel ID", value="", inline=True)
    
    for player in s_players:
        embed.add_field(name="", value=player, inline=True)
        
        print("Player Name: " + player)
    
    await ctx.send(embed=embed)

#### ITEM COMMANDS ####

#Item Command - Get Specific Item
@client.hybrid_command(name="item-grab", help="Returns information about specified item.")
async def grabitem(ctx, item_name): 
    #check bag of Hoarding for Item
    item:h.BagOfHoardingItem = hcc.controlCenter.findItem(item_name)

    #check if item exists
    if item and item_name: 
        embed, itemFile = embedFormatter(item)
        if itemFile:
            await ctx.send(file=itemFile, embed=embed)
        else:
            await ctx.send(embed=embed)
    else: 
         await ctx.send(clientErrorStr + "Sorry the item you have requested doesn't exist. Please try again")

#Item Command - Get Random Item (with params)
@client.hybrid_command(name="item-grab-random", help="Grabs a random item that meets the parameters expectations")
async def grabRandomItem(ctx, level:s_allowedItemLevelOptions=None, 
                         rarity:s_allowedItemRarityOptions=None, 
                         character:str=None): 
    
    #TODO: check if item has been used yet
    if util.checkItemParamValidity(level, rarity) and (character in s_players or character is None):
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
            await ctx.send(clientErrorStr + "Sorry an error occured. Please try again momentarily")
        #abitrarily select item until one with matching specs appears
        #cred embed and send it
    else:
        await ctx.send(clientErrorStr + "Invalid Inputs provided. Please try again with different inputs")

#Item Command - sends a requested item to a specified player
@client.hybrid_command(name="item-request", help="sends requested item to specified player")
# async def reqItem(ctx, item_name, player_name:str):
async def reqItem(ctx, item_name, rx_channel: discord.TextChannel):
    item:h.BagOfHoardingItem = hcc.controlCenter.findItem(item_name)

    #check if item exists
    if item and item_name: 
        embed, itemFile = embedFormatter(item)
        if itemFile:
            await rx_channel.send(file=itemFile, embed=embed)
        else:
            await rx_channel.send(embed=embed)
        await ctx.send(clientInfoStr + "Item Requested, our finest merchants are delivering it now!")
    else: 
        await ctx.send(clientErrorStr + "Sorry the item you have requested doesn't exist. Please try again")

#### LOCATION COMMANDS ####

#Location Command - Get Random Location / Quest
@client.hybrid_command(name="encounter-grab-random", help="Grabs a random encounter that meets the parameters expectations")
async def grabRandomEncounter(ctx, encounter_type:s_allowedEncTypes=None): 
    if util.checkEncounterParamValidity(encounter_type):
        encounter:h.encounterItem = hcc.controlCenter.pickRandomEncounter(encounter_type)
          #check if item exists
        if encounter: 
            embed, itemFile = embedFormatter(encounter)
            if itemFile:
                await ctx.send(file=itemFile, embed=embed)
            else:
                await ctx.send(embed=embed)
        else: 
            await ctx.send(clientErrorStr + "Sorry an error occured. Please try again momentarily")
    else:
        await ctx.send(clientErrorStr + "Invalid Inputs provided. Please try again with different inputs")

#### NPC COMMANDS ####
#NPC Command - Generate Random NPC
@client.hybrid_command(name="npc-create", help="Generates a Random NPC")
async def createNPC(ctx, species=None, gender=None, description=None):
    #TODO: option to add name
    npc:h.NPC = hcc.controlCenter.generateNPC(species, gender, description)        
    if npc: 
        embed, itemFile = embedFormatter(npc)
        if itemFile:
            await ctx.send(file=itemFile, embed=embed)
        else:
            await ctx.send(embed=embed)
    else: 
        await ctx.send(clientErrorStr + "Sorry an error occured. Please try again momentarily")
