import discord
import json
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker
from discord.app_commands import Choice


with open("Databases/Licenses.json","r") as f:
    data = json.load(f)
    
def get_license_by_value(license_value): 
    for license in data['licenses']: 
        if license['value'] == license_value: 
            return license 
    return None




    
class Licensing(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        await self.bot.tree.sync()
        
    @app_commands.command(name="acquire_license",description="Acquire a Specific License from the available options")
    @app_commands.describe(license_type="Pick a license to buy")
    @app_commands.choices(license_type=[Choice(name='Fishing License', value='Fishing License'), Choice(name='Hunting License', value='Hunting License'), Choice(name='Business License', value='Business License'), Choice(name='Marriage License', value='Marriage License')])
    async def acquire_license(self,interaction: discord.Interaction,license_type: str):
        
        view = discord.ui.View()
        
        specific_license = get_license_by_value(license_type) 
        if specific_license: 
            value = specific_license['value']
            price =  specific_license['price']
            description = specific_license['description']      


        
        
        embed = discord.Embed(title=f"License applying for:",description=f"{value}",color=discord.Color.greyple())
        embed.add_field(name=description)
        embed.add_field(name="Price",value=f"£{price}")
        embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/9835/9835724.png")
        await interaction.response.send_message(embed = embed)
        await interaction.response.send_message(view=view)        


        
async def setup(bot):
    await bot.add_cog(Licensing(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))    
        