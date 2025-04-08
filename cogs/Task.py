import random
from turtle import title
import discord
from discord.ext import commands
from discord import Button, app_commands
import json
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker

with open("Databases/GIFS.json","r") as f:
    data = json.load(f)

class Task(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__, "Cog has been loaded")

    @app_commands.command(name="slap",description="Slap a user!")
    async def slap(self, interaction: discord.Interaction,user: discord.Member):
        num = random.randint(0, 9)
        embed = discord.Embed(description=f"{interaction.user.mention} slapped {user.mention}!!",color=discord.Color.random())
        embed.set_image(url=data["slapping"][num])
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hug",description="Hug a user!")
    async def hug(self, interaction: discord.Interaction,user: discord.Member):
        num = random.randint(0, 9)
        embed = discord.Embed(description=f"{interaction.user.mention} hugged {user.mention}!!",color=discord.Color.random())
        embed.set_image(url=data["hugging"][num])
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="high-five",description="Punch a user!")
    async def slap(self, interaction: discord.Interaction,user: discord.Member):
        num = random.randint(0, 9)
        embed = discord.Embed(description=f"{interaction.user.mention} high-fived {user.mention}!!",color=discord.Color.random())
        embed.set_image(url=data["high-five"][num])
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="punch",description="Punch a user!")
    async def slap(self, interaction: discord.Interaction,user: discord.Member):
        num = random.randint(0, 9)
        embed = discord.Embed(description=f"{interaction.user.mention} punched {user.mention}!!",color=discord.Color.random())
        embed.set_image(url=data["punch"][num])
        await interaction.response.send_message(embed=embed)
        
    

async def setup(bot):
    await bot.add_cog(Task(bot))    

