import discord
import asyncio
from discord.ext import tasks,commands
from discord import app_commands
from itertools import cycle
from Database_Managers import Assister, Worker
import datetime
import random
import os

#Variables


RESET_TIME = datetime.time(hour=0,minute=0,second=0)



k = Worker("src code/Databases/Warehouse.db")
a = Assister("src code/Databases/Warehouse.db")
error = discord.Embed( title="🚨 Internal Error 🚨", description="Something went wrong! Please open a ticket to report the issue and we'll get it resolved as soon as possible.", color=discord.Colour.red())



with open("token.txt","r") as t:
    token = t.read()

statuses = ["Gready atm","I am the sin of Greed","🤑💶💸💳","Dead from your Poison","Sponsored by I.M.P","I eat Money for Breakfast"]

status = cycle(statuses)

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!",intents=intents)

  
    
#------------------------------------------
#SUBPROGRAMS
#------------------------------------------                
async def check_collect_reset():
    while True:
        current = datetime.datetime.now()
        reset_time = datetime.datetime(year=current.year, month=current.month, day=current.day, hour=0, minute=0, second=0)
        
        if current >= reset_time:
            reset_time = reset_time + datetime.timedelta(days=1)
        
        time_until_reset = (reset_time - current).total_seconds()
        print(f"Time until reset: {time_until_reset} seconds")
        await asyncio.sleep(time_until_reset)
        await a.daily_reset_collect()
        await asyncio.sleep(86400)
        

    
async def load():
    for filename in os.listdir('./cogs'):  
        if filename.endswith('.py'): 
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
async def main():
    async with bot:
        await load()
        await bot.start(token)

        
        
#------------------------------------------
#EVENTS
#------------------------------------------
@tasks.loop(seconds=30)
async def change_status(): 
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.CustomActivity(name=next(status)))
    


    

@bot.event 
async def on_ready(): 
    change_status.start()
    await check_collect_reset()
    await bot.tree.sync()
    await print("Tree Synced")
    
    
asyncio.run(main=main())




