import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker
import random



class Gambling(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        #await self.bot.tree.sync()
        #self.isready = True
    @app_commands.command(name="gamble",description="Gamble virtual money for a chance to double your money or lose it all")
    async def coinflip(self,interaction: discord.Interaction, wager: int):
        try:
            acc_check = await self.a.account_check(interaction=interaction,user=interaction.user.id)
            if acc_check is not None:
                mon_check = await self.a.check_bal(user= interaction.user.id,amount= wager)
                if mon_check is not None:
                    flip = random.randint(0,1)
                    if flip == 0:
                        await self.k.coinflip_lose(user= interaction.user.id,amount=wager)
                        embed = discord.Embed(title="❌ You Lost!",description=f"Money lost: £{wager}",color=discord.Color.brand_red())
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/6448/6448481.png")
                        embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                        await interaction.response.send_message(embed=embed)
                    else:
                        await self.k.coinflip_win(user=interaction.user.id,amount=wager * 2)
                        embed = discord.Embed(title="🥇 You Won!",description=f"Money won: £{wager * 2}",color=discord.Color.blue())
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/12841/12841754.png")
                        embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                        await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="😷Too Poor!",description=f"Earn More money or lower your wager",color=discord.Color.brand_red())
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/8125/8125441.png")
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    await interaction.response.send_message(embed=embed)
    

        except Exception as e:
            print(e)
            
async def setup(bot):
    await bot.add_cog(Gambling(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))    
        