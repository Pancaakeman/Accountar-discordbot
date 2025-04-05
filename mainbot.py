import discord
import asyncio
from discord.ext import tasks,commands
from itertools import cycle
from Database_Managers import Assister, Worker
import datetime
import os
import dotenv
discord.utils.setup_logging()

#Variables
env = dotenv.load_dotenv()
token = os.environ.get("TOKEN")


k = Worker("Databases/Warehouse.db")
a = Assister("Databases/Warehouse.db")





statuses = [
    "Counting💸",
    "I am the master of savings!",
    "No Money?",
    "Man, I love Money",
    "Sponsored by [Insert Company]"
]

status = cycle(statuses)

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!",intents=intents)
bot.owner_id = 732513701147574322
  
    
#------------------------------------------
#SUBPROGRAMS
#------------------------------------------                
   

    
async def load():
    for filename in os.listdir('./cogs'):  
        if filename.endswith('.py'): 
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
            
async def main():
    async with bot:
        print("Tree Synced")
        await load()
        await bot.start(token=token)


        
        
#------------------------------------------
#EVENTS
#------------------------------------------
@tasks.loop(seconds=30)
async def change_status(): 
    await bot.change_presence(activity=discord.CustomActivity(name=next(status)),status=discord.Status.idle)
    


async def setup_hook():
    await bot.tree.sync()
    print("Synced")


@bot.event
async def on_ready(): 
    await change_status.start()



    
asyncio.run(main=main())




