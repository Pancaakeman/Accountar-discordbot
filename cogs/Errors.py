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
    
    async def on_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        print("error")    
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            embed = discord.Embed(title="You are on cooldown!", description=f"{app_commands.errors.CommandOnCooldown}")
            embed.add_field(name="Recheck the User",value="If the error persists contact an Admin",inline=True)
            embed.set_author(name=f"{interaction.user.global_name}", icon_url=interaction.user.avatar.url )    
            await interaction.response.send_message(embed)
               
async def setup(bot):
    await bot.add_cog(Errors(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))