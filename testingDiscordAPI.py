import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='./', intents=intents)

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.command()
async def ping(ctx):
    await ctx.send(':peach: Pong :peach:')

client.run(TOKEN)

