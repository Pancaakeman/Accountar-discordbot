import discord
from discord.ext import commands
from discord import app_commands
from config import Configs
from itertools import cycle

c = Configs


token = ""
statuses = ["Gready atm","I am the sin of Greed","🤑💶💸💳","Slide me the money","Dead from your Poison"]


intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



@client.event
async def on_ready():
    activity = discord.Game(name=cycle(statuses))
    await client.change_presence(status=discord.Status.online, activity=activity)
    await tree.sync()
    print("Ready!")
    
