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
        if license['name'] == license_value: 
            return license 
    return None



class Button_view(discord.ui.View):
    def __init__(self,license_type,license_cost,k):
        super().__init__(timeout=60)
        self.license_type = license_type
        self.license_cost = license_cost
        self.k = k        
    @discord.ui.button(label="Confirm Purchase?",style=discord.ButtonStyle.primary)
    async def yes_button(self,interaction: discord.Interaction,Button: discord.ui.Button):
        check = await self.k.license_add(user=interaction.user.id,license_name=self.license_type,license_cost = self.license_cost)  
        if check is False:
            embed = discord.Embed(title="😷Too Poor!",description=f"Earn More money or lower your wager",color=discord.Color.brand_red())
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/8125/8125441.png")
            embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
            await interaction.response.send_message(embed=embed)
            
        elif check 
    @discord.ui.button(label="Cancel",style=discord.ButtonStyle.red)
    async def no_button(self,interaction: discord.Interaction,Button: discord.ui.Button):
        await interaction.response.send_message(embed = discord.Embed(title="Cancelled",description=" ",color=discord.Colour.brand_red()))
        
class Licensing(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        await self.bot.tree.sync()
        self.isready = True
        
    @app_commands.command(name="acquire_license",description="Acquire a Specific License from the available options")
    @app_commands.describe(license_type="Pick a license to buy")
    @app_commands.choices(license_type=[Choice(name='Fishing_License', value='Fishing_License'), Choice(name='Hunting_License', value='Hunting_License'), Choice(name='Business_License', value='Business_License'), Choice(name='Marriage_License', value='Marriage_License')])
    async def acquire_license(self,interaction: discord.Interaction,license_type: str):
        try:
            acc_check = await self.a.account_check(interaction=interaction,user=interaction.user.id)
            if acc_check is not None:
                print(license_type)
                
                specific_license = get_license_by_value(license_type) 
                if specific_license: 
                    price =  specific_license['price']
                    description = specific_license['description'] 
                view = Button_view(license_type=license_type,k= Worker("Databases/Warehouse.db"),license_cost=price)
                
                
                embed = discord.Embed(title=f"License applying for:",description=f"{license_type}",color=discord.Color.greyple())
                embed.add_field(name="Description: ",value=description)
                embed.add_field(name="Price",value=f"£{price}")
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/9835/9835724.png")
                await interaction.response.send_message(embed = embed,view=view)        
        except Exception as e:
            print(e)

        
async def setup(bot):
    await bot.add_cog(Licensing(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))    
        