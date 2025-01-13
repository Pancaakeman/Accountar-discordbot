import discord
from discord import app_commands
from discord import SelectOption
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker



class License_Catalog_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)      
    options = [SelectOption(name='Fishing_License', value='Fishing_License'), SelectOption(name='Hunting_License', value='Hunting_License'), SelectOption(name='Business_License', value='Business_License'), SelectOption(name='Marriage_License', value='Marriage_License')]
    @discord.ui.select(placeholder="Choose a license to view",options=None)



class Catlogging(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        await self.bot.tree.sync()  
        #self.isready = True 
    @app_commands.command("license_catlog",description="Shows you a catlog with every single license")
    async def license_catlog(interaction: discord.Interaction):
    
           
async def setup(bot):
    await bot.add_cog(Catlogging(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))
    