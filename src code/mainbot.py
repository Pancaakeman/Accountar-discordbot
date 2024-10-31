import discord
from discord.ext import commands,tasks
from discord import app_commands
from config import Configs
from itertools import cycle

c = Configs


token = "MTI5MjkyNzAxMDc5NjIwODIzMA.G5Aqt1.ecmiT82DPzPlhxpkoCqkjHWknoLgoVj4c3AOBQ"

statuses = ["Gready atm","I am the sin of Greed","🤑💶💸💳","Dead from your Poison","Sponsored by I.M.P","I eat Money for Breakfasy"]

status = cycle(statuses)

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tasks.loop(seconds=30)
async def change_status(): 
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.CustomActivity(name=next(status)))

@client.event 
async def on_ready(): 
    change_status.start() 
    await tree.sync()
    await print(f'Logged in as {client.user}!') 
    
    
    
@tree.command(name="collect",description="collect your salary")
async def collect(userid,user_roles):
    return
    


    
    
client.run(token)
