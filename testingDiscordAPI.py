import discord
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client(intents=discord.Intents.all())

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

client.run(TOKEN)

