import discord
from discord.ext import commands

#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='./', intents=intents)

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')