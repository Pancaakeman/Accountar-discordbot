import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker



class Errors(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        #await self.bot.tree.sync()
        self.isready = True

               
async def setup(bot):
    await bot.add_cog(Errors(bot,a = Assister("Warehouse.db"),k = Worker("Warehouse.db")))