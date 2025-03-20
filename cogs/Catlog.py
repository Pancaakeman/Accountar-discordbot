import discord
from discord import app_commands
from discord import SelectOption
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker
import json

with open("Databases/Licenses.json","r") as f:
    data = json.load(f)

def get_license_by_value(license_value): 
    for license in data['licenses']: 
        if license['name'] == license_value: 
            return license 
    return None


class License_Catalog_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)      
    options = [ SelectOption(label='Fishing License', value='Fishing_License', description="Views the Fishing license"), SelectOption(label='Hunting License', value='Hunting_License', description="Views the Hunting License Data"), SelectOption(label='Business License', value='Business_License', description="Views the Business License Data"), SelectOption(label='Marriage License', value='Marriage_License', description="Views the Business License Data") ]
    @discord.ui.select(placeholder="Choose a license to view",options=options)
    async def license_select(self,interaction: discord.Interaction, Select: discord.ui.Select):
        return Select.values

class Catlog(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        #await self.bot.tree.sync()  
        #self.isready = True 
    #@app_commands.command(name="license_catalogue",description="Shows you a catalogue with every single license")
    '''async def license_catlog(self,interaction: discord.Interaction):
        try:
            #acc_check = await self.a.account_check(interaction=interaction,user=interaction.user.id)
            #if acc_check is not None:      
            view = License_Catalog_view()        
            specific_license = get_license_by_value(license_value=license_type) 
            if specific_license: 
                price =  specific_license['price']
                description = specific_license['description'] 
            await interaction.response.send_message(view=view)
                
        except Exception as e:
            print(e)
'''
        
    
           
async def setup(bot):
    await bot.add_cog(Catlog(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))
    